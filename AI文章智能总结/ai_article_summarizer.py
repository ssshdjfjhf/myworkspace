#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI文章智能总结系统
集成美团Friday大模型，对爬取的AI文章进行智能总结和关键信息提取
"""

import requests
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
import os
import sys

# 添加爬虫模块路径
sys.path.append('../爬取AI咨询')

class FridayAIClient:
    """美团Friday大模型客户端"""

    def __init__(self, app_id: str):
        self.app_id = app_id
        self.base_url = "https://aigc.sankuai.com/v1/openai/native/chat/completions"
        self.headers = {
            'Authorization': f'Bearer {app_id}',
            'Content-Type': 'application/json'
        }

        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ai_summarizer.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def create_summary_prompt(self, article_data: Dict) -> str:
        """创建文章总结的提示词"""
        # 优先使用完整文章内容，如果没有则使用描述
        content_text = article_data.get('content', '') or article_data.get('description', '')

        prompt = f"""请对以下AI工具/项目文章进行专业分析和总结，提取关键信息：

文章标题：{article_data.get('title', '')}
文章分类：{article_data.get('category', '')}
发布时间：{article_data.get('publish_time', '')}
文章链接：{article_data.get('url', '')}

文章内容：
{content_text[:2000]}{'...[内容已截断]' if len(content_text) > 2000 else ''}

请按照以下格式进行总结分析：

## 🎯 核心功能
[用1-2句话概括这个AI工具/项目的核心功能和价值]

## 🔧 主要特点
[列出3-5个主要特点或亮点，每个特点用一行简洁描述]

## 🏷️ 应用场景
[描述适用的具体应用场景和目标用户群体]

## 💡 创新点
[指出相比同类产品的创新之处或独特优势]

## 📊 实用性评估
[从技术成熟度、易用性、实用价值等角度给出简要评估]

请确保总结内容：
1. 专业准确，突出技术特点
2. 简洁明了，每部分控制在50字以内
3. 客观中性，避免过度营销语言
4. 突出实用价值和应用前景

如果原始描述信息不足，请基于标题和分类进行合理推测，并标注"[基于标题推测]"。"""

        return prompt

    def call_friday_api(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """调用Friday API获取总结"""
        payload = {
            "model": "LongCat-Large-32K-Chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,  # 设置为False以获取完整响应
            "temperature": 0.7,
            "max_tokens": 1000
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        content = result['choices'][0]['message']['content']
                        return content.strip()
                    else:
                        self.logger.warning(f"API响应格式异常: {result}")
                        return None
                else:
                    self.logger.warning(f"API调用失败 (状态码: {response.status_code}): {response.text}")

            except requests.RequestException as e:
                self.logger.warning(f"API调用异常 (尝试 {attempt + 1}/{max_retries}): {e}")

            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避

        self.logger.error("API调用最终失败")
        return None

    def summarize_article(self, article_data: Dict) -> Dict:
        """对单篇文章进行总结"""
        self.logger.info(f"正在总结文章: {article_data.get('title', 'Unknown')}")

        # 创建提示词
        prompt = self.create_summary_prompt(article_data)

        # 调用API
        summary = self.call_friday_api(prompt)

        # 构建结果
        result = article_data.copy()
        result['ai_summary'] = summary or "总结生成失败"
        result['summary_generated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return result

class ArticleSummarizer:
    """文章总结器主类"""

    def __init__(self, app_id: str):
        self.friday_client = FridayAIClient(app_id)
        self.logger = logging.getLogger(__name__)

    def load_articles_from_json(self, json_file: str) -> List[Dict]:
        """从JSON文件加载文章数据"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            self.logger.info(f"成功加载 {len(articles)} 篇文章")
            return articles
        except Exception as e:
            self.logger.error(f"加载文章数据失败: {e}")
            return []

    def summarize_articles(self, articles: List[Dict], batch_size: int = 5, delay: float = 2.0) -> List[Dict]:
        """批量总结文章"""
        summarized_articles = []
        total = len(articles)

        self.logger.info(f"开始总结 {total} 篇文章...")

        for i, article in enumerate(articles, 1):
            try:
                self.logger.info(f"处理进度: {i}/{total}")

                # 总结文章
                summarized_article = self.friday_client.summarize_article(article)
                summarized_articles.append(summarized_article)

                # 批次延迟
                if i % batch_size == 0 and i < total:
                    self.logger.info(f"批次处理完成，等待 {delay} 秒...")
                    time.sleep(delay)
                else:
                    time.sleep(0.5)  # 基础延迟

            except Exception as e:
                self.logger.error(f"处理文章失败 ({i}/{total}): {e}")
                # 添加失败的文章（不含总结）
                failed_article = article.copy()
                failed_article['ai_summary'] = f"总结生成失败: {str(e)}"
                failed_article['summary_generated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                summarized_articles.append(failed_article)

        self.logger.info(f"总结完成！成功处理 {len(summarized_articles)} 篇文章")
        return summarized_articles

    def save_summarized_articles(self, articles: List[Dict], output_file: Optional[str] = None):
        """保存总结后的文章"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'summarized_articles_{timestamp}.json'

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            self.logger.info(f"总结结果已保存到: {output_file}")
        except Exception as e:
            self.logger.error(f"保存文件失败: {e}")

    def generate_summary_report(self, articles: List[Dict], report_file: Optional[str] = None):
        """生成总结报告"""
        if not report_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = f'summary_report_{timestamp}.md'

        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("# AI文章智能总结报告\n\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"文章总数: {len(articles)}\n\n")

                # 统计信息
                categories = {}
                success_count = 0

                for article in articles:
                    category = article.get('category', '未分类')
                    categories[category] = categories.get(category, 0) + 1

                    if article.get('ai_summary') and not article['ai_summary'].startswith('总结生成失败'):
                        success_count += 1

                f.write(f"成功总结: {success_count} 篇\n")
                f.write(f"失败数量: {len(articles) - success_count} 篇\n\n")

                f.write("## 分类统计\n\n")
                for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"- {category}: {count} 篇\n")

                f.write("\n## 文章总结详情\n\n")

                for i, article in enumerate(articles, 1):
                    f.write(f"### {i}. {article.get('title', 'Unknown Title')}\n\n")
                    f.write(f"**分类**: {article.get('category', '未分类')}\n")
                    f.write(f"**时间**: {article.get('publish_time', '未知')}\n")
                    f.write(f"**链接**: {article.get('url', '')}\n\n")

                    if article.get('ai_summary'):
                        f.write("**AI智能总结**:\n\n")
                        f.write(f"{article['ai_summary']}\n\n")
                    else:
                        f.write("**原始描述**:\n\n")
                        f.write(f"{article.get('description', '无描述')}\n\n")

                    f.write("---\n\n")

            self.logger.info(f"总结报告已生成: {report_file}")

        except Exception as e:
            self.logger.error(f"生成报告失败: {e}")

    def run(self, input_file: str, batch_size: int = 5, delay: float = 2.0):
        """运行总结流程"""
        # 加载文章数据
        articles = self.load_articles_from_json(input_file)
        if not articles:
            self.logger.error("没有找到文章数据")
            return

        # 总结文章
        summarized_articles = self.summarize_articles(articles, batch_size, delay)

        # 保存结果
        self.save_summarized_articles(summarized_articles)

        # 生成报告
        self.generate_summary_report(summarized_articles)

        return summarized_articles

def main():
    """主函数"""
    # 配置参数
    APP_ID = "21910615279495929878"  # 你的AppID
    INPUT_FILE = "爬取AI咨询/ai_articles_20250814_201716.json"  # 输入文件路径
    
    BATCH_SIZE = 3  # 批处理大小
    DELAY = 3.0  # 批次间延迟（秒）

    try:
        # 检查输入文件是否存在
        if not os.path.exists(INPUT_FILE):
            print(f"❌ 输入文件不存在: {INPUT_FILE}")
            print("请先运行爬虫获取文章数据，或修改INPUT_FILE路径")
            return

        # 创建总结器
        summarizer = ArticleSummarizer(APP_ID)

        # 运行总结
        print("🚀 开始AI文章智能总结...")
        summarized_articles = summarizer.run(INPUT_FILE, BATCH_SIZE, DELAY)

        if summarized_articles:
            print(f"✅ 总结完成！共处理 {len(summarized_articles)} 篇文章")
            print("📁 结果文件已保存到当前目录")
        else:
            print("❌ 总结失败")

    except KeyboardInterrupt:
        print("\n❌ 用户中断处理")
    except Exception as e:
        print(f"❌ 处理过程中出现错误: {e}")
        logging.exception("详细错误信息:")

if __name__ == "__main__":
    main()
