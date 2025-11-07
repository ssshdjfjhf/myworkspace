#!/usr/bin/env python3
"""
电影海报图片下载脚本
从豆瓣下载所有电影海报并保存到本地
"""

import json
import os
import requests
import time
from urllib.parse import urlparse
from pathlib import Path

def download_image(url, save_path, max_retries=3):
    """下载单张图片"""
    if not url or url.startswith('data:'):
        return False

    for attempt in range(max_retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://movie.douban.com/'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # 确保目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # 保存图片
            with open(save_path, 'wb') as f:
                f.write(response.content)

            print(f"✅ 下载成功: {url} -> {save_path}")
            return True

        except Exception as e:
            print(f"❌ 下载失败 (尝试 {attempt + 1}/{max_retries}): {url} - {e}")
            if attempt < max_retries - 1:
                time.sleep(1)  # 重试前等待

    return False

def get_image_filename(url, movie_id, title):
    """生成图片文件名"""
    parsed = urlparse(url)
    path = parsed.path

    # 从URL中提取文件名
    if path and path != '/':
        original_name = os.path.basename(path)
        # 移除URL参数
        original_name = original_name.split('?')[0]
        if original_name:
            return f"{movie_id}_{original_name}"

    # 如果无法从URL获取，使用电影信息生成文件名
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
    return f"{movie_id}_{safe_title[:20]}.jpg"

def process_movies(movies_data, image_dir):
    """处理电影数据，下载所有图片"""
    downloaded_count = 0
    failed_count = 0

    # 创建图片目录
    os.makedirs(image_dir, exist_ok=True)

    # 处理正在热映的电影
    print("\n📽️  正在下载正在热映的电影海报...")
    for movie in movies_data.get('nowPlaying', []):
        if 'poster' in movie and movie['poster']:
            filename = get_image_filename(movie['poster'], movie['id'], movie['title'])
            save_path = os.path.join(image_dir, 'movies', filename)

            if download_image(movie['poster'], save_path):
                downloaded_count += 1
                # 更新数据中的图片路径
                movie['localPoster'] = f"images/movies/{filename}"
            else:
                failed_count += 1
                movie['localPoster'] = ''

    # 处理热门电影
    print("\n🔥 正在下载热门电影海报...")
    for category, movies in movies_data.get('hotMovies', {}).items():
        for movie in movies:
            if 'poster' in movie and movie['poster']:
                filename = get_image_filename(movie['poster'], movie['id'], movie['title'])
                save_path = os.path.join(image_dir, 'movies', filename)

                # 如果文件已存在，直接使用本地路径
                if os.path.exists(save_path):
                    movie['localPoster'] = f"images/movies/{filename}"
                    print(f"📁 使用已下载的图片: {movie['title']}")
                else:
                    if download_image(movie['poster'], save_path):
                        downloaded_count += 1
                        movie['localPoster'] = f"images/movies/{filename}"
                    else:
                        failed_count += 1
                        movie['localPoster'] = ''

    # 处理电视剧
    print("\n📺 正在下载电视剧海报...")
    for category, tv_shows in movies_data.get('hotTV', {}).items():
        for tv in tv_shows:
            if 'poster' in tv and tv['poster']:
                filename = get_image_filename(tv['poster'], tv['id'], tv['title'])
                save_path = os.path.join(image_dir, 'tv', filename)

                os.makedirs(os.path.dirname(save_path), exist_ok=True)

                if download_image(tv['poster'], save_path):
                    downloaded_count += 1
                    tv['localPoster'] = f"images/tv/{filename}"
                else:
                    failed_count += 1
                    tv['localPoster'] = ''

    return downloaded_count, failed_count

def update_json_data(movies_data, output_path):
    """更新JSON数据文件，添加本地图片路径"""
    try:
        # 创建备份
        backup_path = output_path + '.backup'
        if os.path.exists(output_path):
            os.rename(output_path, backup_path)
            print(f"💾 已创建备份文件: {backup_path}")

        # 保存更新后的数据
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(movies_data, f, ensure_ascii=False, indent=2)

        print(f"✅ JSON数据已更新: {output_path}")
        return True

    except Exception as e:
        print(f"❌ 更新JSON数据失败: {e}")
        return False

def main():
    """主函数"""
    print("🎬 开始下载电影海报图片...")
    print("=" * 50)

    # 配置路径
    json_file = 'data/movies.json'
    image_dir = 'images'

    try:
        # 读取JSON数据
        print(f"📖 读取数据文件: {json_file}")
        with open(json_file, 'r', encoding='utf-8') as f:
            movies_data = json.load(f)

        print(f"📊 数据加载成功，包含 {len(movies_data)} 个分类")

        # 下载图片
        downloaded, failed = process_movies(movies_data, image_dir)

        print(f"\n📈 下载统计:")
        print(f"✅ 成功下载: {downloaded} 张")
        print(f"❌ 下载失败: {failed} 张")
        print(f"📁 图片保存目录: {image_dir}")

        # 更新JSON文件
        if update_json_data(movies_data, json_file):
            print("\n🎉 所有操作完成！")
            print("\n💡 使用说明:")
            print("- 本地图片路径已添加到JSON数据中")
            print("- 在代码中使用 'localPoster' 字段替代 'poster' 字段")
            print("- 如果 localPoster 为空，系统会自动生成占位图")
        else:
            print("\n⚠️  JSON数据更新失败，但图片已下载")

    except FileNotFoundError:
        print(f"❌ 找不到数据文件: {json_file}")
        print("请确保在项目根目录下运行此脚本")
    except json.JSONDecodeError:
        print(f"❌ JSON文件格式错误: {json_file}")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
