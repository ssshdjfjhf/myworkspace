#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版AI文章爬虫
专门用于获取完整文章内容，为AI总结提供更丰富的数据
"""

import sys
import os
sys.path.append('.')

from ai_news_scraper import AINewsScraper
import json
import time
from datetime import datetime

class EnhancedAIScraper(AINewsScraper):
    """增强版AI文章爬虫"""

    def __init__(self):
        super().__init__()
        self.logger.info("初始化增强版AI文章爬虫...")

    def scrape_with_full_content(self, max_pages=2, delay_between_articles=2):
        """爬取文章并获取完整内容"""
        self.logger.info(f"开始爬取 {max_pages} 页文章，包含完整内容...")

        # 先获取文章列表
        articles = self.scrape_articles(max_pages=max_pages, include_content=False)

        if not articles:
            self.logger.error("没有获取到文章列表")
            return []

        self.logger.info(f"获取到 {len(articles)} 篇文章，开始获取详细内容...")

        # 为每篇文章获取详细内容
        enhanced_articles = []
        total = len(articles)

        for i, article in enumerate(articles, 1):
            try:
                self.logger.info(f"处理文章 {i}/{total}: {article['title']}")

                # 获取文章详细内容
                detail_content = self.get_article_detail(article['url'])
                article['content'] = detail_content or article.get('description', '')

                # 添加内容统计信息
                article['content_length'] = len(article['content'])
                article['has_full_content'] = len(article['content']) > 500

                enhanced_articles.append(article)

                # 延迟避免请求过快
                if i < total:
                    time.sleep(delay_between_articles)

            except Exception as e:
                self.logger.error(f"处理文章失败 {i}/{total}: {e}")
                # 即使失败也保留基本信息
                article['content'] = article.get('description', '')
                article['content_length'] = len(article['content'])
                article['has_full_content'] = False
                enhanced_articles.append(article)

        return enhanced_articles

    def analyze_content_quality(self, articles):
        """分析内容质量"""
        if not articles:
            return

        total = len(articles)
        with_full_content = sum(1 for a in articles if a.get('has_full_content', False))
        avg_length = sum(a.get('content_length', 0) for a in articles) / total if total > 0 else 0

        self.logger.info(f"内容质量分析:")
        self.logger.info(f"  总文章数: {total}")
        self.logger.info(f"  完整内容: {with_full_content} ({with_full_content/total*100:.1f}%)")
        self.logger.info(f"  平均长度: {avg_length:.0f} 字符")

        print(f"\n📊 内容质量分析:")
        print(f"  总文章数: {total}")
        print(f"  完整内容: {with_full_content} ({with_full_content/total*100:.1f}%)")
        print(f"  平均长度: {avg_length:.0f} 字符")

    def save_enhanced_data(self, articles, filename_prefix="enhanced_articles"):
        """保存增强数据"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 保存JSON格式
        json_filename = f"{filename_prefix}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)

        self.logger.info(f"增强数据已保存到: {json_filename}")

        # 生成内容预览报告
        report_filename = f"content_preview_{timestamp}.md"
        self.generate_content_preview(articles, report_filename)

        return json_filename

    def generate_content_preview(self, articles, filename):
        """生成内容预览报告"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# AI文章内容预览报告\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"文章总数: {len(articles)}\n\n")

            for i, article in enumerate(articles, 1):
                f.write(f"## {i}. {article.get('title', 'Unknown Title')}\n\n")
                f.write(f"**分类**: {article.get('category', '未分类')}\n")
                f.write(f"**时间**: {article.get('publish_time', '未知')}\n")
                f.write(f"**链接**: {article.get('url', '')}\n")
                f.write(f"**内容长度**: {article.get('content_length', 0)} 字符\n")
                f.write(f"**完整内容**: {'是' if article.get('has_full_content', False) else '否'}\n\n")

                # 显示内容预览
                content = article.get('content', '')
                if content:
                    preview = content[:300] + "..." if len(content) > 300 else content
                    f.write("**内容预览**:\n")
                    f.write(f"```\n{preview}\n```\n\n")
                else:
                    f.write("**内容预览**: 无内容\n\n")

                f.write("---\n\n")

        self.logger.info(f"内容预览报告已生成: {filename}")

def main():
    """主函数"""
    print("🚀 启动增强版AI文章爬虫...")
    print("📖 此版本会获取完整文章内容，适合AI总结分析")

    scraper = EnhancedAIScraper()

    # 配置参数
    MAX_PAGES = 2  # 减少页数，因为要获取完整内容
    DELAY = 2      # 文章间延迟（秒）

    try:
        # 爬取文章
        articles = scraper.scrape_with_full_content(
            max_pages=MAX_PAGES,
            delay_between_articles=DELAY
        )

        if articles:
            # 分析内容质量
            scraper.analyze_content_quality(articles)

            # 保存数据
            filename = scraper.save_enhanced_data(articles)

            print(f"\n✅ 增强版爬取完成！")
            print(f"📁 数据文件: {filename}")
            print(f"📊 共获取 {len(articles)} 篇文章")
            print(f"💡 可以使用此文件进行AI智能总结")

        else:
            print("❌ 没有获取到文章数据")

    except KeyboardInterrupt:
        print("\n❌ 用户中断爬取")
    except Exception as e:
        print(f"❌ 爬取过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
