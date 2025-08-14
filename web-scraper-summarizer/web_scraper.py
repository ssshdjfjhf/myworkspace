#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页内容爬取和AI总结工具
支持爬取网页内容并使用大模型进行智能总结
"""

import requests
from bs4 import BeautifulSoup
import re
import sys
import argparse
from urllib.parse import urljoin, urlparse
import time
import json
from datetime import datetime

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        # 设置请求头，模拟浏览器访问
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def fetch_content(self, url, timeout=10):
        """
        获取网页内容
        """
        try:
            print(f"🌐 正在访问: {url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            response.encoding = response.apparent_encoding or 'utf-8'
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"❌ 网页访问失败: {e}")
            return None

    def extract_text_content(self, html_content, url):
        """
        从HTML中提取主要文本内容
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # 移除不需要的标签
            for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'advertisement']):
                tag.decompose()

            # 获取标题
            title = ""
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text().strip()

            # 尝试找到主要内容区域
            main_content = None

            # 常见的主要内容选择器
            content_selectors = [
                'article', 'main', '.content', '.post-content', '.entry-content',
                '.article-content', '.post-body', '.content-body', '#content',
                '.main-content', '.article-body'
            ]

            for selector in content_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            # 如果没找到主要内容区域，使用body
            if not main_content:
                main_content = soup.find('body')

            if not main_content:
                main_content = soup

            # 提取文本
            text_content = main_content.get_text(separator='\n', strip=True)

            # 清理文本
            text_content = re.sub(r'\n\s*\n', '\n\n', text_content)  # 合并多个空行
            text_content = re.sub(r'[ \t]+', ' ', text_content)  # 合并多个空格

            return {
                'title': title,
                'content': text_content,
                'url': url,
                'length': len(text_content),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"❌ 内容提取失败: {e}")
            return None

    def save_content(self, content_data, filename=None):
        """
        保存爬取的内容到文件
        """
        if not filename:
            # 根据URL生成文件名
            parsed_url = urlparse(content_data['url'])
            domain = parsed_url.netloc.replace('.', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"scraped_content_{domain}_{timestamp}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(content_data, f, ensure_ascii=False, indent=2)
            print(f"💾 内容已保存到: {filename}")
            return filename
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='网页内容爬取工具')
    parser.add_argument('url', help='要爬取的网页URL')
    parser.add_argument('-o', '--output', help='输出文件名')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='请求超时时间（秒）')

    args = parser.parse_args()

    # 验证URL格式
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url

    scraper = WebScraper()

    # 爬取内容
    html_content = scraper.fetch_content(args.url, args.timeout)
    if not html_content:
        sys.exit(1)

    # 提取文本内容
    content_data = scraper.extract_text_content(html_content, args.url)
    if not content_data:
        sys.exit(1)

    print(f"📄 标题: {content_data['title']}")
    print(f"📊 内容长度: {content_data['length']} 字符")

    # 保存内容
    saved_file = scraper.save_content(content_data, args.output)

    # 显示内容预览
    preview_length = 500
    if content_data['content']:
        print(f"\n📖 内容预览 (前{preview_length}字符):")
        print("-" * 50)
        print(content_data['content'][:preview_length])
        if len(content_data['content']) > preview_length:
            print("...")
        print("-" * 50)

    print(f"\n✅ 爬取完成！内容已保存到: {saved_file}")
    print("💡 接下来可以使用AI总结工具对内容进行总结")

if __name__ == "__main__":
    main()
