#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能AI文章总结系统
在AI总结时实时获取网页内容，而不是预先爬取
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
import os
import sys

# 添加爬虫模块路径
sys.path.append('../爬取AI咨询')

class SmartWebReader:
    """智能网页读取器"""

    def __init__(self):
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
                logging.FileHandler('smart_summarizer.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_page_content(self, url: str, max_retries: int = 3) -> Optional[str]:
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
                    time.sleep(2 ** attempt)
                else:
                    self.logger.error(f"获取页面最终失败: {url}")
                    return None

    def extract_article_content(self, html_content: str, url: str) -> str:
        """从HTML中提取文章内容"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # 针对AI工具集网站优化的内容选择器
        content_selectors = [
            '.entry-content',           # WordPress标准内容区域
            '.post-content',            # 文章内容区域
            '.article-content',         # 文章内容
            '.content',                 # 通用内容区域
            'article .content',         # 文章标签内的内容
            '.main-content',            # 主要内容区域
            '.post-body',               # 文章主体
            '.single-content',          # 单页内容
            '[class*="content"]',       # 包含content的类名
            'main article',             # 主要文章区域
            '.wp-content'               # WordPress内容
        ]

        content = ''
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # 移除不需要的元素
                for unwanted in content_elem(["script", "style", "nav", "footer", "header", ".sidebar", ".related", ".comments", ".navigation"]):
                    unwanted.decompose()

                # 提取文本内容
                content = content_elem.get_text(separator='\n', strip=True)

                # 清理多余的空行
                content = '\n'.join(line.strip() for line in content.split('\n') if line.strip())

                if len(content) > 200:  # 确保内容有足够长度
                    break

        # 如果没有找到合适的内容，尝试从整个页面提取
        if not content or len(content) < 100:
            # 移除不需要的标签
            for unwanted in soup(["script", "style", "nav", "footer", "header", ".sidebar", ".menu", ".navigation"]):
                unwanted.decompose()

            # 尝试从body或main标签提取
            body_content = soup.find('body') or soup.find('main')
            if body_content:
                content = body_content.get_text(separator='\n', strip=True)
                content = '\n'.join(line.strip() for line in content.split('\n') if line.strip())

        # 限制内容长度，避免过长
        if len(content) > 4000:
            content = content[:4000] + "...[内容已截断]"

        return content if content else "无法获取文章详细内容"

    def read_article_realtime(self, article_url: str) -> str:
        """实时读取文章内容"""
        self.logger.info(f"实时读取文章: {article_url}")

        html_content = self.get_page_content(article_url)
        if not html_content:
            return "无法获取文章内容"

        content = self.extract_article_content(html_content, article_url)
        self.logger.info(f"成功提取内容，长度: {len(content)} 字符")

        return content

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
        self.logger = logging.getLogger(__name__)

    def create_summary_prompt(self, article_data: Dict, realtime_content: str) -> str:
        """创建文章总结的提示词"""
        prompt = f"""请对以下AI工具/项目文章进行专业分析和总结，提取关键信息：

基本信息：
- 文章标题：{article_data.get('title', '')}
- 文章分类：{article_data.get('category', '')}
- 发布时间：{article_data.get('publish_time', '')}
- 文章链接：{article_data.get('url', '')}
- 简要描述：{article_data.get('description', '')}

实时获取的完整文章内容：
{realtime_content}

请基于以上信息，按照以下格式进行专业分析和总结：

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
5. 基于实时获取的完整内容进行分析

如果实时内容获取失败，请基于基本信息进行合理推测，并标注"[基于基本信息推测]"。"""

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
            "stream": False,
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
                time.sleep(2 ** attempt)

        self.logger.error("API调用最终失败")
        return None

class SmartArticleSummarizer:
    """智能文章总结器主类"""

    def __init__(self, app_id: str):
        self.web_reader = SmartWebReader()
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

    def summarize_article_smart(self, article_data: Dict) -> Dict:
        """智能总结单篇文章（实时获取内容）"""
        self.logger.info(f"开始智能总结文章: {article_data.get('title', 'Unknown')}")

        # 实时获取文章内容
        article_url = article_data.get('url', '')
        if article_url:
            realtime_content = self.web_reader.read_article_realtime(article_url)
        else:
            realtime_content = "无法获取文章链接"

        # 创建提示词
        prompt = self.friday_client.create_summary_prompt(article_data, realtime_content)

        # 调用AI进行总结
        summary = self.friday_client.call_friday_api(prompt)

        # 构建结果
        result = article_data.copy()
        result['ai_summary'] = summary or "总结生成失败"
        result['realtime_content_length'] = len(realtime_content)
        result['content_source'] = "realtime" if realtime_content != "无法获取文章内容" else "failed"
        result['summary_generated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return result

    def summarize_articles_smart(self, articles: List[Dict], batch_size: int = 3, delay: float = 3.0) -> List[Dict]:
        """智能批量总结文章"""
        summarized_articles = []
        total = len(articles)

        self.logger.info(f"开始智能总结 {total} 篇文章...")
        print(f"🚀 开始智能总结 {total} 篇文章...")
        print("📖 每篇文章都会实时获取最新内容进行分析")

        for i, article in enumerate(articles, 1):
            try:
                print(f"\n📄 处理进度: {i}/{total} - {article.get('title', 'Unknown')[:50]}...")

                # 智能总结文章
                summarized_article = self.summarize_article_smart(article)
                summarized_articles.append(summarized_article)

                # 显示处理结果
                content_length = summarized_article.get('realtime_content_length', 0)
                content_source = summarized_article.get('content_source', 'unknown')

                if content_source == "realtime":
                    print(f"   ✅ 成功获取实时内容 ({content_length} 字符)")
                else:
                    print(f"   ⚠️ 内容获取失败，使用基本信息")

                # 批次延迟
                if i % batch_size == 0 and i < total:
                    print(f"   ⏳ 批次处理完成，等待 {delay} 秒...")
                    time.sleep(delay)
                else:
                    time.sleep(1)  # 基础延迟

            except Exception as e:
                self.logger.error(f"处理文章失败 ({i}/{total}): {e}")
                # 添加失败的文章
                failed_article = article.copy()
                failed_article['ai_summary'] = f"总结生成失败: {str(e)}"
                failed_article['realtime_content_length'] = 0
                failed_article['content_source'] = "error"
                failed_article['summary_generated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                summarized_articles.append(failed_article)
                print(f"   ❌ 处理失败: {str(e)}")

        self.logger.info(f"智能总结完成！成功处理 {len(summarized_articles)} 篇文章")
        return summarized_articles

    def save_smart_results(self, articles: List[Dict], output_file: Optional[str] = None):
        """保存智能总结结果"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'smart_summarized_articles_{timestamp}.json'

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            self.logger.info(f"智能总结结果已保存到: {output_file}")
        except Exception as e:
            self.logger.error(f"保存文件失败: {e}")

    def generate_smart_report(self, articles: List[Dict], report_file: Optional[str] = None):
        """生成智能总结报告"""
        if not report_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = f'smart_summary_report_{timestamp}.md'

        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("# AI文章智能总结报告（实时内容版）\n\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"文章总数: {len(articles)}\n\n")

                # 统计信息
                categories = {}
                success_count = 0
                realtime_success = 0

                for article in articles:
                    category = article.get('category', '未分类')
                    categories[category] = categories.get(category, 0) + 1

                    if article.get('ai_summary') and not article['ai_summary'].startswith('总结生成失败'):
                        success_count += 1

                    if article.get('content_source') == 'realtime':
                        realtime_success += 1

                f.write(f"成功总结: {success_count} 篇\n")
                f.write(f"实时内容获取成功: {realtime_success} 篇\n")
                f.write(f"失败数量: {len(articles) - success_count} 篇\n\n")

                f.write("## 分类统计\n\n")
                for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"- {category}: {count} 篇\n")

                f.write("\n## 文章智能总结详情\n\n")

                for i, article in enumerate(articles, 1):
                    f.write(f"### {i}. {article.get('title', 'Unknown Title')}\n\n")
                    f.write(f"**分类**: {article.get('category', '未分类')}\n")
                    f.write(f"**时间**: {article.get('publish_time', '未知')}\n")
                    f.write(f"**链接**: {article.get('url', '')}\n")
                    f.write(f"**内容来源**: {'实时获取' if article.get('content_source') == 'realtime' else '基本信息'}\n")
                    f.write(f"**内容长度**: {article.get('realtime_content_length', 0)} 字符\n\n")

                    if article.get('ai_summary'):
                        f.write("**AI智能总结**:\n\n")
                        f.write(f"{article['ai_summary']}\n\n")
                    else:
                        f.write("**原始描述**:\n\n")
                        f.write(f"{article.get('description', '无描述')}\n\n")

                    f.write("---\n\n")

            self.logger.info(f"智能总结报告已生成: {report_file}")

        except Exception as e:
            self.logger.error(f"生成报告失败: {e}")

    def run_smart_summary(self, input_file: str, batch_size: int = 3, delay: float = 3.0):
        """运行智能总结流程"""
        # 加载文章数据
        articles = self.load_articles_from_json(input_file)
        if not articles:
            self.logger.error("没有找到文章数据")
            return []

        print(f"📚 加载了 {len(articles)} 篇文章")
        print("🔄 将为每篇文章实时获取最新内容进行AI总结")

        # 智能总结文章
        summarized_articles = self.summarize_articles_smart(articles, batch_size, delay)

        # 保存结果
        self.save_smart_results(summarized_articles)

        # 生成报告
        self.generate_smart_report(summarized_articles)

        return summarized_articles

def main():
    """主函数"""
    # 配置参数
    APP_ID = "21910615279495929878"  # 你的AppID
    INPUT_FILE = "../爬取AI咨询/basic_articles_20250814_212345.json"  # 基本信息文件路径
    BATCH_SIZE = 2  # 批处理大小（实时获取内容较慢，建议减小）
    DELAY = 4.0     # 批次间延迟（秒）

    try:
        # 检查输入文件是否存在
        if not os.path.exists(INPUT_FILE):
            print(f"❌ 输入文件不存在: {INPUT_FILE}")
            print("💡 请先使用交互式爬虫获取基本文章信息")
            print("   选择 '3. ⚡ 仅获取基本信息' 选项")
            return

        # 创建智能总结器
        summarizer = SmartArticleSummarizer(APP_ID)

        # 运行智能总结
        print("🧠 启动智能AI文章总结系统...")
        print("📖 特点：实时获取网页内容，确保分析最新信息")

        summarized_articles = summarizer.run_smart_summary(INPUT_FILE, BATCH_SIZE, DELAY)

        if summarized_articles:
            print(f"\n✅ 智能总结完成！共处理 {len(summarized_articles)} 篇文章")
            print("📁 结果文件已保存到当前目录")

            # 统计成功率
            realtime_success = sum(1 for a in summarized_articles if a.get('content_source') == 'realtime')
            print(f"📊 实时内容获取成功率: {realtime_success}/{len(summarized_articles)} ({realtime_success/len(summarized_articles)*100:.1f}%)")
        else:
            print("❌ 智能总结失败")

    except KeyboardInterrupt:
        print("\n❌ 用户中断处理")
    except Exception as e:
        print(f"❌ 处理过程中出现错误: {e}")
        logging.exception("详细错误信息:")

if __name__ == "__main__":
    main()
