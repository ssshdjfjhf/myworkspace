#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版AI工具集爬虫
专门针对 https://ai-bot.cn/the-latest-ai-projects/ 页面结构优化
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from datetime import datetime
import re

def get_ai_articles(max_pages=3):
    """爬取AI工具集的最新项目资讯"""

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

            # 根据实际网站结构查找文章链接
            # 从提供的HTML内容可以看到，文章链接的模式
            article_links = soup.find_all('a', href=re.compile(r'https://ai-bot\.cn/[^/]+/$'))

            page_articles = []
            for link in article_links:
                title = link.get_text(strip=True)
                url = link.get('href', '')

                # 过滤掉导航链接和无效链接
                if title and len(title) > 5 and not any(skip in url for skip in [
                    '/favorites/', '/ai-app-store/', '/daily-ai-news/',
                    '/ai-tutorials/', '/about-us/', '/disclaimer/'
                ]):

                    # 查找描述信息
                    description = ''
                    parent = link.parent
                    if parent:
                        # 查找同级或父级的描述文本
                        desc_text = parent.get_text(strip=True)
                        if len(desc_text) > len(title) + 10:
                            # 移除标题部分，获取描述
                            description = desc_text.replace(title, '').strip()[:300]

                    # 查找时间信息
                    time_info = ''
                    time_patterns = [r'(\d+)小时前', r'(\d+)天前', r'(\d+)分钟前']
                    for pattern in time_patterns:
                        match = re.search(pattern, parent.get_text() if parent else '')
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

                    article = {
                        'title': title,
                        'url': url,
                        'description': description,
                        'category': category,
                        'publish_time': time_info,
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

def save_articles(articles, format_type='both'):
    """保存文章数据"""
    if not articles:
        print("没有文章数据可保存")
        return

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if format_type in ['json', 'both']:
        json_filename = f'ai_articles_{timestamp}.json'
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"已保存到 {json_filename}")

    if format_type in ['csv', 'both']:
        csv_filename = f'ai_articles_{timestamp}.csv'
        if articles:
            fieldnames = articles[0].keys()
            with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(articles)
            print(f"已保存到 {csv_filename}")

def main():
    """主函数"""
    print("开始爬取AI工具集网站的最新项目资讯...")

    # 爬取文章
    articles = get_ai_articles(max_pages=3)

    if articles:
        print(f"\n总共爬取到 {len(articles)} 篇文章")

        # 保存数据
        save_articles(articles, format_type='both')

        # 显示前几篇文章的信息
        print("\n文章预览:")
        for i, article in enumerate(articles[:5]):
            print(f"\n{i+1}. {article['title']}")
            print(f"   分类: {article['category']}")
            print(f"   时间: {article['publish_time']}")
            print(f"   链接: {article['url']}")
            if article['description']:
                print(f"   描述: {article['description'][:100]}...")
    else:
        print("没有爬取到任何文章")

if __name__ == "__main__":
    main()
