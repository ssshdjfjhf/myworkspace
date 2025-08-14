#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI内容总结工具
支持多种大模型API进行内容总结
"""

import json
import argparse
import sys
import os
from datetime import datetime
import requests
import openai
from typing import Dict, Any, Optional
try:
    from friday_config import FRIDAY_CONFIG
except ImportError:
    FRIDAY_CONFIG = None

class AISummarizer:
    def __init__(self, api_type="friday", api_key=None, base_url=None):
        """
        初始化AI总结器

        Args:
            api_type: API类型 ("friday", "openai", "local")
            api_key: API密钥（Friday使用AppId）
            base_url: API基础URL
        """
        self.api_type = api_type

        if api_type == "friday":
            self.api_key = api_key or os.getenv('FRIDAY_APP_ID') or (FRIDAY_CONFIG['app_id'] if FRIDAY_CONFIG else None)
            self.base_url = base_url or 'https://aigc.sankuai.com/v1/openai/native'
        else:
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            self.base_url = base_url or os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')

        if api_type == "openai" and self.api_key:
            openai.api_key = self.api_key
            if base_url:
                openai.api_base = base_url

    def load_content(self, file_path):
        """
        从文件加载爬取的内容
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 加载文件失败: {e}")
            return None

    def create_summary_prompt(self, content_data, summary_type="comprehensive"):
        """
        创建总结提示词
        """
        title = content_data.get('title', '未知标题')
        content = content_data.get('content', '')
        url = content_data.get('url', '')

        prompts = {
            "comprehensive": f"""请对以下网页内容进行全面总结：

标题：{title}
来源：{url}

内容：
{content}

请提供：
1. 主要内容概述（3-5句话）
2. 关键要点（列表形式）
3. 重要信息提取
4. 如果是技术文章，请提取技术要点
5. 总结性评价

请用中文回答，保持客观和准确。""",

            "brief": f"""请简要总结以下网页内容：

标题：{title}
内容：{content}

请用2-3句话概括主要内容，用中文回答。""",

            "technical": f"""请从技术角度分析以下内容：

标题：{title}
内容：{content}

请提供：
1. 技术要点总结
2. 关键技术概念
3. 实用价值评估
4. 相关技术建议

请用中文回答。""",

            "academic": f"""请从学术角度分析以下内容：

标题：{title}
内容：{content}

请提供：
1. 核心观点总结
2. 论证逻辑分析
3. 重要结论提取
4. 学术价值评估

请用中文回答。"""
        }

        return prompts.get(summary_type, prompts["comprehensive"])

    def summarize_with_openai(self, prompt, model="gpt-3.5-turbo"):
        """
        使用OpenAI API进行总结
        """
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一个专业的内容总结助手，擅长提取关键信息并进行结构化总结。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ OpenAI API调用失败: {e}")
            return None

    def summarize_with_friday(self, prompt, model="LongCat-8B-128K-Chat"):
        """
        使用美团Friday大模型API进行总结
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
            }

            data = {
                "model": model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False  # 不使用流式输出，便于处理结果
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"❌ Friday API请求失败: {response.status_code}")
                print(f"响应内容: {response.text}")
                return None

        except Exception as e:
            print(f"❌ Friday API调用失败: {e}")
            return None

    def summarize_with_local_api(self, prompt, model="chatglm"):
        """
        使用本地部署的大模型API进行总结
        """
        try:
            headers = {
                'Content-Type': 'application/json',
            }

            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "你是一个专业的内容总结助手。"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000,
                "temperature": 0.3
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"❌ API请求失败: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ 本地API调用失败: {e}")
            return None

    def summarize(self, content_data, summary_type="comprehensive", model=None):
        """
        对内容进行总结
        """
        prompt = self.create_summary_prompt(content_data, summary_type)

        print(f"🤖 正在使用 {self.api_type} 进行内容总结...")
        print(f"📝 总结类型: {summary_type}")

        if self.api_type == "friday":
            model = model or "LongCat-8B-128K-Chat"
            summary = self.summarize_with_friday(prompt, model)
        elif self.api_type == "openai":
            model = model or "gpt-3.5-turbo"
            summary = self.summarize_with_openai(prompt, model)
        elif self.api_type == "local":
            model = model or "chatglm"
            summary = self.summarize_with_local_api(prompt, model)
        else:
            print(f"❌ 不支持的API类型: {self.api_type}")
            return None

        if summary:
            return {
                'original_title': content_data.get('title', ''),
                'original_url': content_data.get('url', ''),
                'summary_type': summary_type,
                'model_used': model,
                'summary': summary,
                'original_length': content_data.get('length', 0),
                'summary_length': len(summary),
                'timestamp': datetime.now().isoformat()
            }

        return None

    def save_summary(self, summary_data, filename=None):
        """
        保存总结结果
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"summary_{timestamp}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, ensure_ascii=False, indent=2)
            print(f"💾 总结已保存到: {filename}")
            return filename
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='AI内容总结工具')
    parser.add_argument('input_file', help='输入的内容文件（JSON格式）')
    parser.add_argument('-t', '--type', choices=['comprehensive', 'brief', 'technical', 'academic'],
                       default='comprehensive', help='总结类型')
    parser.add_argument('-m', '--model', help='使用的模型名称')
    parser.add_argument('-o', '--output', help='输出文件名')
    parser.add_argument('--api-type', choices=['friday', 'openai', 'local'], default='friday', help='API类型')
    parser.add_argument('--api-key', help='API密钥（Friday使用AppId）')
    parser.add_argument('--base-url', help='API基础URL')

    args = parser.parse_args()

    # 初始化总结器
    summarizer = AISummarizer(
        api_type=args.api_type,
        api_key=args.api_key,
        base_url=args.base_url
    )

    # 加载内容
    content_data = summarizer.load_content(args.input_file)
    if not content_data:
        sys.exit(1)

    print(f"📄 原文标题: {content_data.get('title', '未知')}")
    print(f"📊 原文长度: {content_data.get('length', 0)} 字符")

    # 进行总结
    summary_data = summarizer.summarize(content_data, args.type, args.model)
    if not summary_data:
        sys.exit(1)

    # 显示总结结果
    print("\n" + "="*60)
    print("📋 AI总结结果")
    print("="*60)
    print(summary_data['summary'])
    print("="*60)

    print(f"\n📈 压缩比: {content_data.get('length', 0)} → {summary_data['summary_length']} 字符")
    print(f"🤖 使用模型: {summary_data['model_used']}")

    # 保存总结
    saved_file = summarizer.save_summary(summary_data, args.output)
    print(f"\n✅ 总结完成！结果已保存到: {saved_file}")

if __name__ == "__main__":
    main()
