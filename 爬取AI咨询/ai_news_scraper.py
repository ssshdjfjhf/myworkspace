#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI工具集网站爬虫
专门爬取最新AI项目资讯
基于实际HTML结构优化
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import os
from datetime import datetime
import logging
from urllib.parse import urljoin
import re

class AINewsScraper:
    def __init__(self):
        self.base_url = "https://ai-bot.cn"
        self.target_url = "https://ai-bot.cn/the-latest-ai-projects/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://ai-bot.cn/',
        })

        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_page_content(self, url, max_retries=3):
        """获取页面内容"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response.text
            except requests.RequestException as e:
                self.logger.warning(f"获取页面失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    self.logger.error(f"获取页面最终失败: {url}")
                    return None

    def parse_article_list(self, html_content):
        """解析文章列表 - 基于实际HTML结构"""
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []

        # 查找所有文章容器 - 基于提供的HTML结构
        article_containers = soup.find_all('div', class_='list-grid list-grid-padding')

        self.logger.info(f"找到 {len(article_containers)} 个文章容器")

        for container in article_containers:
            try:
                article_data = self.extract_article_info(container)
                if article_data:
                    articles.append(article_data)
            except Exception as e:
                self.logger.warning(f"解析文章信息失败: {e}")
                continue

        return articles

    def extract_article_info(self, container):
        """从容器中提取文章信息 - 基于实际HTML结构"""
        article = {}

        # 查找标题和链接
        title_link = container.find('a', class_='list-title')
        if not title_link:
            return None

        # 提取标题（去除"新"标签）
        title_text = title_link.get_text(strip=True)
        # 移除开头的"新"字符
        if title_text.startswith('新'):
            title_text = title_text[1:].strip()

        article['title'] = title_text
        article['url'] = title_link.get('href', '')

        # 确保URL是完整的
        if article['url'] and not article['url'].startswith('http'):
            article['url'] = urljoin(self.base_url, article['url'])

        # 查找描述
        desc_elem = container.find('div', class_='overflowClip_2')
        if desc_elem:
            article['description'] = desc_elem.get_text(strip=True)
        else:
            article['description'] = ''

        # 查找分类
        category_link = container.find('div', class_='list-footer').find('a')
        if category_link:
            article['category'] = category_link.get_text(strip=True)
        else:
            article['category'] = '未分类'

        # 查找发布时间
        time_elem = container.find('time')
        if time_elem:
            article['publish_time'] = time_elem.get_text(strip=True)
        else:
            article['publish_time'] = ''

        # 查找图片链接
        img_elem = container.find('a', class_='media-content')
        if img_elem and img_elem.get('data-src'):
            article['image_url'] = img_elem.get('data-src')
        else:
            article['image_url'] = ''

        # 检查是否为新文章
        new_badge = container.find('span', class_='badge vc-red')
        article['is_new'] = bool(new_badge and '新' in new_badge.get_text())

        # 添加爬取时间
        article['scraped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return article

    def get_article_detail(self, article_url):
        """获取文章详细内容"""
        html_content = self.get_page_content(article_url)
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')

        # 查找文章内容
        content_selectors = [
            '.entry-content', '.post-content', '.article-content',
            '.content', 'article .content', '.main-content'
        ]

        content = ''
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # 移除脚本和样式标签
                for script in content_elem(["script", "style"]):
                    script.decompose()
                content = content_elem.get_text(strip=True)
                if len(content) > 100:  # 确保内容有足够长度
                    break

        return content

    def scrape_articles(self, max_pages=5, include_content=False):
        """爬取文章"""
        all_articles = []

        for page in range(1, max_pages + 1):
            if page == 1:
                url = self.target_url
            else:
                url = f"{self.target_url}page/{page}/"

            self.logger.info(f"正在爬取第 {page} 页: {url}")

            html_content = self.get_page_content(url)
            if not html_content:
                self.logger.warning(f"跳过第 {page} 页")
                continue

            articles = self.parse_article_list(html_content)

            if not articles:
                self.logger.warning(f"第 {page} 页没有找到文章")
                break

            self.logger.info(f"第 {page} 页找到 {len(articles)} 篇文章")

            # 如果需要获取详细内容
            if include_content:
                for i, article in enumerate(articles):
                    self.logger.info(f"获取文章详细内容 ({i+1}/{len(articles)}): {article['title']}")
                    detail_content = self.get_article_detail(article['url'])
                    article['content'] = detail_content or ''
                    time.sleep(1)  # 避免请求过快

            all_articles.extend(articles)
            time.sleep(2)  # 页面间延迟

        return all_articles

    def save_to_json(self, articles, filename='ai_articles.json'):
        """保存为JSON格式"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        self.logger.info(f"已保存 {len(articles)} 篇文章到 {filename}")

    def save_to_csv(self, articles, filename='ai_articles.csv'):
        """保存为CSV格式"""
        if not articles:
            return

        fieldnames = ['title', 'url', 'description', 'category', 'publish_time', 'image_url', 'is_new', 'scraped_at']
        if 'content' in articles[0]:
            fieldnames.append('content')

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(articles)
        self.logger.info(f"已保存 {len(articles)} 篇文章到 {filename}")

    def print_summary(self, articles):
        """打印爬取结果摘要"""
        if not articles:
            print("没有爬取到任何文章")
            return

        print(f"\n=== 爬取结果摘要 ===")
        print(f"总文章数: {len(articles)}")

        # 统计分类
        categories = {}
        new_count = 0
        for article in articles:
            category = article.get('category', '未分类')
            categories[category] = categories.get(category, 0) + 1
            if article.get('is_new'):
                new_count += 1

        print(f"新文章数: {new_count}")
        print(f"分类统计:")
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count}篇")

        print(f"\n=== 最新文章示例 ===")
        for i, article in enumerate(articles[:5]):
            status = "🆕" if article.get('is_new') else "📄"
            print(f"\n{i+1}. {status} {article['title']}")
            print(f"   分类: {article['category']}")
            print(f"   时间: {article['publish_time']}")
            print(f"   链接: {article['url']}")
            if article['description']:
                desc = article['description'][:100] + "..." if len(article['description']) > 100 else article['description']
                print(f"   描述: {desc}")

    def run(self, max_pages=3, include_content=False, save_formats=['json', 'csv']):
        """运行爬虫"""
        self.logger.info("开始爬取AI工具集网站...")

        articles = self.scrape_articles(max_pages=max_pages, include_content=include_content)

        if not articles:
            self.logger.error("没有爬取到任何文章")
            return []

        self.logger.info(f"总共爬取到 {len(articles)} 篇文章")

        # 保存数据
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if 'json' in save_formats:
            self.save_to_json(articles, f'ai_articles_{timestamp}.json')

        if 'csv' in save_formats:
            self.save_to_csv(articles, f'ai_articles_{timestamp}.csv')

        # 打印摘要
        self.print_summary(articles)

        return articles

def main():
    """主函数"""
    scraper = AINewsScraper()

    # 配置参数
    MAX_PAGES = 3  # 爬取页数
    INCLUDE_CONTENT = False  # 是否包含文章详细内容（会显著增加爬取时间）
    SAVE_FORMATS = ['json', 'csv']  # 保存格式

    try:
        articles = scraper.run(
            max_pages=MAX_PAGES,
            include_content=INCLUDE_CONTENT,
            save_formats=SAVE_FORMATS
        )

        if articles:
            print(f"\n✅ 爬取完成！共获取 {len(articles)} 篇文章")
            print("📁 文件已保存到当前目录")

    except KeyboardInterrupt:
        print("\n❌ 用户中断爬取")
    except Exception as e:
        print(f"❌ 爬取过程中出现错误: {e}")
        logging.exception("详细错误信息:")

if __name__ == "__main__":
    main()
