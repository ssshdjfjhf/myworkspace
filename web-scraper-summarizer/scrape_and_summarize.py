#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页爬取和AI总结一体化工具
一键完成网页内容爬取和智能总结
"""

import argparse
import sys
import os
import tempfile
from web_scraper import WebScraper
from ai_summarizer import AISummarizer
from friday_config import FRIDAY_CONFIG, setup_friday_env

def main():
    parser = argparse.ArgumentParser(description='网页爬取和AI总结一体化工具')
    parser.add_argument('url', help='要爬取和总结的网页URL')

    # 爬虫参数
    parser.add_argument('-t', '--timeout', type=int, default=10, help='请求超时时间（秒）')

    # 总结参数
    parser.add_argument('--summary-type', choices=['comprehensive', 'brief', 'technical', 'academic'],
                       default='comprehensive', help='总结类型')
    parser.add_argument('--model', help='使用的AI模型名称')
    parser.add_argument('--api-type', choices=['friday', 'openai', 'local'], default='friday', help='API类型')
    parser.add_argument('--api-key', help='API密钥（Friday使用AppId）')
    parser.add_argument('--base-url', help='API基础URL')

    # 输出参数
    parser.add_argument('-o', '--output', help='输出文件前缀')
    parser.add_argument('--keep-scraped', action='store_true', help='保留爬取的原始内容文件')

    args = parser.parse_args()

    # 如果使用Friday API且没有指定api_key，使用配置文件中的AppId
    if args.api_type == "friday" and not args.api_key:
        args.api_key = FRIDAY_CONFIG['app_id']
        if not args.base_url:
            args.base_url = FRIDAY_CONFIG['base_url']
        if not args.model:
            args.model = FRIDAY_CONFIG['default_model']

    print("🚀 开始网页爬取和AI总结流程...")
    print(f"🌐 目标URL: {args.url}")
    print(f"🤖 使用API: {args.api_type}")
    if args.api_type == "friday":
        print(f"📱 App ID: {args.api_key}")
        print(f"🎯 模型: {args.model or FRIDAY_CONFIG['default_model']}")
    print("-" * 60)

    # 第一步：爬取网页内容
    print("📥 第一步：爬取网页内容")

    # 验证URL格式
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url

    scraper = WebScraper()

    # 爬取内容
    html_content = scraper.fetch_content(args.url, args.timeout)
    if not html_content:
        print("❌ 网页爬取失败，程序退出")
        sys.exit(1)

    # 提取文本内容
    content_data = scraper.extract_text_content(html_content, args.url)
    if not content_data:
        print("❌ 内容提取失败，程序退出")
        sys.exit(1)

    print(f"✅ 爬取成功！")
    print(f"📄 标题: {content_data['title']}")
    print(f"📊 内容长度: {content_data['length']} 字符")

    # 保存爬取内容（临时文件或永久文件）
    if args.keep_scraped:
        scraped_filename = f"{args.output}_scraped.json" if args.output else None
        scraped_file = scraper.save_content(content_data, scraped_filename)
    else:
        # 使用临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            import json
            json.dump(content_data, f, ensure_ascii=False, indent=2)
            scraped_file = f.name

    print("-" * 60)

    # 第二步：AI总结
    print("🤖 第二步：AI智能总结")

    # 初始化总结器
    summarizer = AISummarizer(
        api_type=args.api_type,
        api_key=args.api_key,
        base_url=args.base_url
    )

    # 进行总结
    summary_data = summarizer.summarize(content_data, args.summary_type, args.model)
    if not summary_data:
        print("❌ AI总结失败，程序退出")
        # 清理临时文件
        if not args.keep_scraped and os.path.exists(scraped_file):
            os.unlink(scraped_file)
        sys.exit(1)

    print("✅ 总结完成！")

    # 显示总结结果
    print("\n" + "="*60)
    print("📋 AI总结结果")
    print("="*60)
    print(summary_data['summary'])
    print("="*60)

    print(f"\n📈 内容压缩: {content_data['length']} → {summary_data['summary_length']} 字符")
    print(f"🤖 使用模型: {summary_data['model_used']}")
    print(f"📝 总结类型: {args.summary_type}")

    # 保存总结结果
    summary_filename = f"{args.output}_summary.json" if args.output else None
    saved_file = summarizer.save_summary(summary_data, summary_filename)

    # 清理临时文件
    if not args.keep_scraped and os.path.exists(scraped_file):
        os.unlink(scraped_file)

    print(f"\n🎉 全部完成！")
    if args.keep_scraped:
        print(f"📁 原始内容: {scraped_file}")
    print(f"📁 总结结果: {saved_file}")

    # 显示使用建议
    print(f"\n💡 使用建议:")
    print(f"   - 如需不同类型的总结，可使用: --summary-type brief|technical|academic")
    print(f"   - 如需使用其他模型，可使用: --model gpt-4")
    print(f"   - 如需保留原始内容，可使用: --keep-scraped")

if __name__ == "__main__":
    main()
