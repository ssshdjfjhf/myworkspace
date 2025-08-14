#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式AI文章爬虫
先预览文章数量，让用户选择爬取策略
"""

import sys
import os
sys.path.append('.')

from ai_news_scraper import AINewsScraper
import json
import time
from datetime import datetime

class InteractiveScraper(AINewsScraper):
    """交互式AI文章爬虫"""

    def __init__(self):
        super().__init__()
        self.logger.info("初始化交互式AI文章爬虫...")

    def preview_articles(self, max_pages=5):
        """预览文章信息，不获取详细内容"""
        print("🔍 正在预览文章信息...")

        page_info = []
        total_articles = 0

        for page in range(1, max_pages + 1):
            if page == 1:
                url = self.target_url
            else:
                url = f"{self.target_url}page/{page}/"

            print(f"📄 检查第 {page} 页...")

            html_content = self.get_page_content(url)
            if not html_content:
                print(f"⚠️ 第 {page} 页无法访问")
                break

            articles = self.parse_article_list(html_content)

            if not articles:
                print(f"⚠️ 第 {page} 页没有找到文章")
                break

            # 统计分类
            categories = {}
            new_count = 0
            for article in articles:
                category = article.get('category', '未分类')
                categories[category] = categories.get(category, 0) + 1
                if article.get('is_new'):
                    new_count += 1

            page_info.append({
                'page': page,
                'article_count': len(articles),
                'new_count': new_count,
                'categories': categories,
                'articles': articles
            })

            total_articles += len(articles)
            print(f"   📊 找到 {len(articles)} 篇文章 (其中 {new_count} 篇新文章)")

            time.sleep(1)  # 预览时也要控制频率

        return page_info, total_articles

    def display_preview_summary(self, page_info, total_articles):
        """显示预览摘要"""
        print("\n" + "="*60)
        print("📊 文章预览摘要")
        print("="*60)

        print(f"🔢 总页数: {len(page_info)} 页")
        print(f"📰 总文章数: {total_articles} 篇")

        # 统计所有分类
        all_categories = {}
        total_new = 0

        for page in page_info:
            total_new += page['new_count']
            for category, count in page['categories'].items():
                all_categories[category] = all_categories.get(category, 0) + count

        print(f"🆕 新文章数: {total_new} 篇")

        print(f"\n📂 分类统计:")
        for category, count in sorted(all_categories.items(), key=lambda x: x[1], reverse=True):
            print(f"   {category}: {count} 篇")

        print(f"\n📄 各页详情:")
        for page in page_info:
            print(f"   第{page['page']}页: {page['article_count']}篇 (新文章: {page['new_count']}篇)")

    def display_recent_articles(self, page_info, show_count=5):
        """显示最新文章标题"""
        print(f"\n📋 最新 {show_count} 篇文章预览:")
        print("-" * 60)

        all_articles = []
        for page in page_info:
            all_articles.extend(page['articles'])

        for i, article in enumerate(all_articles[:show_count], 1):
            status = "🆕" if article.get('is_new') else "📄"
            print(f"{i}. {status} {article['title']}")
            print(f"   📂 {article['category']} | ⏰ {article['publish_time']}")
            if article['description']:
                desc = article['description'][:80] + "..." if len(article['description']) > 80 else article['description']
                print(f"   💬 {desc}")
            print()

    def get_user_choice(self, page_info, total_articles):
        """获取用户选择"""
        print("\n" + "="*60)
        print("🎯 请选择爬取策略:")
        print("="*60)

        print("1. 🚀 爬取所有页面 (获取完整内容)")
        print("2. 📝 爬取指定页数 (获取完整内容)")
        print("3. ⚡ 仅获取基本信息 (不获取完整内容，速度快)")
        print("4. 🔍 查看更多文章预览")
        print("5. ❌ 退出")

        while True:
            try:
                choice = input("\n请输入选择 (1-5): ").strip()

                if choice == "1":
                    return "all", len(page_info), True
                elif choice == "2":
                    max_pages = len(page_info)
                    while True:
                        try:
                            pages = int(input(f"请输入要爬取的页数 (1-{max_pages}): "))
                            if 1 <= pages <= max_pages:
                                return "custom", pages, True
                            else:
                                print(f"❌ 请输入 1-{max_pages} 之间的数字")
                        except ValueError:
                            print("❌ 请输入有效的数字")
                elif choice == "3":
                    max_pages = len(page_info)
                    while True:
                        try:
                            pages = int(input(f"请输入要爬取的页数 (1-{max_pages}): "))
                            if 1 <= pages <= max_pages:
                                return "basic", pages, False
                            else:
                                print(f"❌ 请输入 1-{max_pages} 之间的数字")
                        except ValueError:
                            print("❌ 请输入有效的数字")
                elif choice == "4":
                    self.display_recent_articles(page_info, show_count=10)
                    continue
                elif choice == "5":
                    return "exit", 0, False
                else:
                    print("❌ 请输入 1-5 之间的数字")
            except KeyboardInterrupt:
                print("\n❌ 用户中断操作")
                return "exit", 0, False

    def scrape_with_choice(self, pages, include_content=True):
        """根据用户选择进行爬取"""
        if include_content:
            print(f"🚀 开始爬取 {pages} 页文章 (包含完整内容)...")
            print("⏳ 这可能需要一些时间，请耐心等待...")
        else:
            print(f"⚡ 开始快速爬取 {pages} 页文章 (仅基本信息)...")

        articles = self.scrape_articles(max_pages=pages, include_content=include_content)

        if articles and include_content:
            # 分析内容质量
            with_content = sum(1 for a in articles if len(a.get('content', '')) > 500)
            avg_length = sum(len(a.get('content', '')) for a in articles) / len(articles)

            print(f"\n📊 内容质量分析:")
            print(f"   完整内容: {with_content}/{len(articles)} 篇 ({with_content/len(articles)*100:.1f}%)")
            print(f"   平均长度: {avg_length:.0f} 字符")

        return articles

    def save_results(self, articles, strategy):
        """保存结果"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 根据策略选择文件名前缀
        if strategy == "all":
            prefix = "full_articles"
        elif strategy == "custom":
            prefix = "custom_articles"
        elif strategy == "basic":
            prefix = "basic_articles"
        else:
            prefix = "articles"

        # 保存JSON文件
        json_filename = f"{prefix}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)

        # 保存CSV文件
        csv_filename = f"{prefix}_{timestamp}.csv"
        self.save_to_csv(articles, csv_filename)

        print(f"\n💾 数据已保存:")
        print(f"   📄 JSON: {json_filename}")
        print(f"   📊 CSV: {csv_filename}")

        return json_filename

def main():
    """主函数"""
    print("🎉 欢迎使用交互式AI文章爬虫！")
    print("📖 此工具可以让你先预览文章，再决定爬取策略")

    scraper = InteractiveScraper()

    try:
        # 第一步：预览文章
        print("\n🔍 第一步：预览文章信息")
        page_info, total_articles = scraper.preview_articles(max_pages=5)

        if not page_info:
            print("❌ 没有找到任何文章，请检查网络连接")
            return

        # 第二步：显示预览摘要
        scraper.display_preview_summary(page_info, total_articles)

        # 第三步：显示最新文章
        scraper.display_recent_articles(page_info)

        # 第四步：获取用户选择
        strategy, pages, include_content = scraper.get_user_choice(page_info, total_articles)

        if strategy == "exit":
            print("👋 感谢使用，再见！")
            return

        # 第五步：执行爬取
        print(f"\n🚀 第二步：执行爬取任务")
        articles = scraper.scrape_with_choice(pages, include_content)

        if articles:
            # 第六步：保存结果
            print(f"\n💾 第三步：保存结果")
            filename = scraper.save_results(articles, strategy)

            print(f"\n✅ 爬取完成！")
            print(f"📊 共获取 {len(articles)} 篇文章")
            print(f"📁 数据文件: {filename}")

            if include_content:
                print(f"💡 可以使用此文件进行AI智能总结")

        else:
            print("❌ 没有获取到文章数据")

    except KeyboardInterrupt:
        print("\n❌ 用户中断操作")
    except Exception as e:
        print(f"❌ 操作过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
