#!/usr/bin/env python3
"""
提取北京热映电影数据
从豆瓣HTML响应中提取正在热映的电影信息
"""

import json
import re
from datetime import datetime
from pathlib import Path

def extract_movies_from_html(html_content):
    """从HTML内容中提取电影信息"""
    movies = []

    # 正则表达式匹配电影信息
    movie_pattern = r'<li\s+id="(\d+)"\s+class="list-item[^"]*"\s+' \
                   r'data-title="([^"]*)"\s+' \
                   r'data-score="([^"]*)"\s+' \
                   r'data-star="[^"]*"\s+' \
                   r'data-release="([^"]*)"\s+' \
                   r'data-duration="([^"]*)"\s+' \
                   r'data-region="([^"]*)"\s+' \
                   r'data-director="([^"]*)"\s+' \
                   r'data-actors="([^"]*)"\s+' \
                   r'data-category="nowplaying"[^>]*>' \
                   r'.*?<img src="([^"]*)"[^>]*>' \
                   r'.*?<a[^>]*href="https://movie\.douban\.com/ticket/redirect/\?movie_id=(\d+)"'

    matches = re.findall(movie_pattern, html_content, re.DOTALL)

    for match in matches:
        (subject_id, title, score, year, duration, region, director, actors, poster_url, movie_id) = match

        # 处理评分
        rating = float(score) if score and score != '0' else 0

        # 处理演员列表
        casts = [actor.strip() for actor in actors.split(' / ') if actor.strip()]

        # 处理地区
        countries = [country.strip() for country in region.split(' / ') if country.strip()]

        # 处理导演
        directors = [director.strip()] if director.strip() else []

        # 处理类型（根据标题和演员推断）
        genres = []
        if any(word in title for word in ['动作', '战争', '战斗']):
            genres.append('动作')
        if any(word in title for word in ['爱情', '恋']):
            genres.append('爱情')
        if any(word in title for word in ['科幻', '未来']):
            genres.append('科幻')
        if any(word in title for word in ['悬疑', '谜']):
            genres.append('悬疑')
        if any(word in title for word in ['喜剧', '搞笑']):
            genres.append('喜剧')
        if any(word in title for word in ['剧情']) or not genres:
            genres.append('剧情')

        # 生成上映日期（简化处理）
        release_date = f"{year}-01-01" if year else "2024-01-01"

        movie = {
            "id": int(subject_id),
            "title": title,
            "originalTitle": title,
            "rating": rating,
            "ratingsCount": 0,  # 暂无评分人数数据
            "year": int(year) if year.isdigit() else 2024,
            "duration": duration if duration else "未知",
            "genres": genres,
            "directors": directors,
            "casts": casts,
            "countries": countries,
            "poster": poster_url,
            "summary": f"{title}是一部{year}年上映的电影，由{director}执导，{', '.join(casts[:2])}等主演。",
            "releaseDate": release_date,
            "status": "hot",
            "buyTicketUrl": f"https://movie.douban.com/ticket/redirect/?movie_id={movie_id}",
            "localPoster": f"images/movies/{subject_id}_{poster_url.split('/')[-1].replace('.webp', '.jpg')}"
        }

        movies.append(movie)

    return movies

def check_duplicates(new_movies, existing_movies):
    """检查重复电影"""
    existing_ids = {movie['id'] for movie in existing_movies}
    existing_titles = {movie['title'] for movie in existing_movies}

    unique_movies = []
    for movie in new_movies:
        if movie['id'] not in existing_ids and movie['title'] not in existing_titles:
            unique_movies.append(movie)
        else:
            print(f"跳过重复电影: {movie['title']} (ID: {movie['id']})")

    return unique_movies

def update_movies_json(new_movies):
    """更新movies.json文件"""
    try:
        # 读取现有数据
        with open('data/movies.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 获取现有的nowPlaying电影
        existing_movies = data.get('nowPlaying', [])

        # 检查重复
        unique_movies = check_duplicates(new_movies, existing_movies)

        if not unique_movies:
            print("没有新的电影需要添加")
            return

        # 添加到现有列表
        existing_movies.extend(unique_movies)
        data['nowPlaying'] = existing_movies

        # 创建备份
        backup_path = 'data/movies.json.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"已创建备份文件: {backup_path}")

        # 保存更新后的数据
        with open('data/movies.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ 成功添加 {len(unique_movies)} 部新电影")

        # 打印添加的电影信息
        for movie in unique_movies:
            print(f"  - {movie['title']} (评分: {movie['rating']}, ID: {movie['id']})")

    except FileNotFoundError:
        print("❌ 找不到movies.json文件")
    except json.JSONDecodeError:
        print("❌ JSON文件格式错误")
    except Exception as e:
        print(f"❌ 更新失败: {e}")

def main():
    """主函数"""
    print("🎬 开始提取北京热映电影数据...")
    print("=" * 50)

    try:
        # 读取HTML文件
        with open('data/北京热映.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 提取电影信息
        movies = extract_movies_from_html(html_content)

        print(f"📊 共提取到 {len(movies)} 部电影")

        if movies:
            # 更新JSON文件
            update_movies_json(movies)

            print("\n💡 使用说明:")
            print("- 新的电影已添加到nowPlaying列表")
            print("- 重复的电影已自动跳过")
            print("- 需要运行download_images.py下载新电影海报")
        else:
            print("⚠️ 未提取到任何电影数据")

    except FileNotFoundError:
        print("❌ 找不到北京热映.html文件")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
