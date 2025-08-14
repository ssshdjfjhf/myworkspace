#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版AI工具集爬虫
改进了对文章描述和时间信息的提取
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from datetime import datetime
import re

def get_ai_articles_enhanced(max_pages=3):
    """增强版爬取AI工具集的最新项目资讯"""

    base_url = "https://ai-bot.cn"
    target_url = "https://ai-bot.cn/the-latest-ai-projects/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    }

    all_articles = []

    for page in range(1, max_pages + 1):
        if page == 1:
            url = target_url
        else:
            url = f"{target_url}page/{page}/"

        print(f"正在爬取第 {page} 页: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')

            # 更精确地查找文章容器
            # 根据网站结构，查找包含"新"标记的文章
            article_containers = []

            # 查找所有包含链接的容器
            for link in soup.find_all('a', href=re.compile(r'https://ai-bot\.cn/[^/]+/$')):
                title_text = link.get_text(strip=True)

                # 过滤掉导航和无关链接
                if (title_text and len(title_text) > 10 and
                    not any(skip in link.get('href', '') for skip in [
                        '/favorites/', '/ai-app-store/', '/daily-ai-news/',
                        '/ai-tutorials/', '/about-us/', '/disclaimer/',
                        '/the-latest-ai-projects/', '/ai-column/', '/ai-question-and-answer/'
                    ]) and
                    # 查找带有"新"标记的文章
                    ('新' in title_text or any(keyword in title_text.lower() for keyword in [
                        'ai', '工具', '模型', '平台', '助手', '生成', '智能'
                    ]))):

                    # 查找文章的完整容器
                    container = link
                    parent = link.parent
                    while parent and parent.name != 'body':
                        # 查找包含更多信息的父容器
                        if parent.find('a') and len(parent.get_text()) > len(title_text) + 20:
                            container = parent
                            break
                        parent = parent.parent

                    article_containers.append((link, container))

            page_articles = []
            for link, container in article_containers:
                title = link.get_text(strip=True)
                url = link.get('href', '')

                # 提取描述信息
                description = ''
                container_text = container.get_text()

                # 尝试从容器中提取描述
                sentences = re.split(r'[。！？\n]', container_text)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if (len(sentence) > 20 and
                        sentence != title and
                        not re.match(r'^\d+[小时天分钟]前$', sentence) and
                        not sentence.startswith('AI工具') and
                        not sentence.startswith('Copyright')):
                        description = sentence[:200]
                        break

                # 提取时间信息
                time_info = ''
                time_patterns = [
                    r'(\d+)小时前', r'(\d+)天前', r'(\d+)分钟前',
                    r'\d{4}-\d{2}-\d{2}', r'\d{2}-\d{2}'
                ]

                for pattern in time_patterns:
                    match = re.search(pattern, container_text)
                    if match:
                        time_info = match.group()
                        break

                # 判断分类
                category = '未分类'
                if '/ai-tools/' in url:
                    category = 'AI工具'
                elif '/ai-research/' in url:
                    category = 'AI项目和框架'
                elif '/ai-column/' in url:
                    category = 'AI专栏'
                elif '新' in title:
                    category = '最新AI项目'

                # 提取关键词
                keywords = []
                keyword_patterns = [
                    r'AI\w*', r'人工智能', r'机器学习', r'深度学习', r'神经网络',
                    r'生成式', r'大模型', r'智能助手', r'自动化', r'开源'
                ]

                for pattern in keyword_patterns:
                    matches = re.findall(pattern, title + ' ' + description, re.IGNORECASE)
                    keywords.extend(matches)

                keywords = list(set(keywords))[:5]  # 去重并限制数量

                article = {
                    'title': title,
                    'url': url,
                    'description': description,
                    'category': category,
                    'publish_time': time_info,
                    'keywords': keywords,
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                page_articles.append(article)

            # 去重
            existing_urls = {article['url'] for article in all_articles}
            new_articles = [article for article in page_articles if article['url'] not in existing_urls]

            all_articles.extend(new_articles)
            print(f"第 {page} 页找到 {len(new_articles)} 篇新文章")

            if not new_articles:
                print("没有找到新文章，停止爬取")
                break

            time.sleep(2)  # 避免请求过快

        except Exception as e:
            print(f"爬取第 {page} 页时出错: {e}")
            continue

    return all_articles

def get_article_details(article_url):
    """获取单篇文章的详细信息"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        response = requests.get(article_url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取文章内容
        content_selectors = [
            '.entry-content', '.post-content', '.article-content',
            '.content', 'article', '.main-content'
        ]

        content = ''
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # 移除脚本和样式标签
                for script in content_elem(["script", "style"]):
                    script.decompose()
                content = content_elem.get_text(strip=True)[:500]  # 限制长度
                break

        # 提取标签
        tags = []
        tag_selectors = ['.tags', '.post-tags', '.entry-tags']
        for selector in tag_selectors:
            tag_elem = soup.select_one(selector)
            if tag_elem:
                tag_links = tag_elem.find_all('a')
                tags = [tag.get_text(strip=True) for tag in tag_links]
                break

        return {
            'content': content,
            'tags': tags
        }

    except Exception as e:
        print(f"获取文章详情失败 {article_url}: {e}")
        return {'content': '', 'tags': []}

def save_articles_enhanced(articles, format_type='both', include_details=False):
    """保存增强版文章数据"""
    if not articles:
        print("没有文章数据可保存")
        return

    # 如果需要获取详细内容
    if include_details:
        print("正在获取文章详细内容...")
        for i, article in enumerate(articles):
            print(f"处理第 {i+1}/{len(articles)} 篇文章: {article['title'][:30]}...")
            details = get_article_details(article['url'])
            article.update(details)
            time.sleep(1)  # 避免请求过快

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if format_type in ['json', 'both']:
        json_filename = f'ai_articles_enhanced_{timestamp}.json'
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"已保存到 {json_filename}")

    if format_type in ['csv', 'both']:
        csv_filename = f'ai_articles_enhanced_{timestamp}.csv'
        if articles:
            # 处理列表类型的字段
            csv_articles = []
            for article in articles:
                csv_article = article.copy()
                csv_article['keywords'] = ', '.join(article.get('keywords', []))
                csv_article['tags'] = ', '.join(article.get('tags', []))
                csv_articles.append(csv_article)

            fieldnames = csv_articles[0].keys()
            with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_articles)
            print(f"已保存到 {csv_filename}")

def main():
    """主函数"""
    print("开始爬取AI工具集网站的最新项目资讯（增强版）...")

    # 爬取文章
    articles = get_ai_articles_enhanced(max_pages=3)

    if articles:
        print(f"\n总共爬取到 {len(articles)} 篇文章")

        # 保存数据
        save_articles_enhanced(articles, format_type='both', include_details=False)

        # 显示统计信息
        categories = {}
        for article in articles:
            cat = article['category']
            categories[cat] = categories.get(cat, 0) + 1

        print("\n分类统计:")
        for cat, count in categories.items():
            print(f"  {cat}: {count} 篇")

        # 显示前几篇文章的信息
        print("\n文章预览:")
        for i, article in enumerate(articles[:5]):
            print(f"\n{i+1}. {article['title']}")
            print(f"   分类: {article['category']}")
            print(f"   时间: {article['publish_time']}")
            print(f"   关键词: {', '.join(article['keywords'])}")
            print(f"   链接: {article['url']}")
            if article['description']:
                print(f"   描述: {article['description'][:100]}...")
    else:
        print("没有爬取到任何文章")

if __name__ == "__main__":
    main()
