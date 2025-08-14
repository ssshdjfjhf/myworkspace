#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美团Friday API测试脚本
用于验证API连接和基本功能
"""

import requests
import json
from config import FRIDAY_CONFIG

def test_friday_api():
    """测试Friday API连接"""
    print("🧪 测试美团Friday API连接...")

    # 测试用的简单提示
    test_prompt = "请简单介绍一下人工智能的定义，用50字以内回答。"

    payload = {
        "model": FRIDAY_CONFIG["model"],
        "messages": [
            {
                "role": "user",
                "content": test_prompt
            }
        ],
        "stream": False,
        "temperature": 0.7,
        "max_tokens": 100
    }

    headers = {
        'Authorization': f'Bearer {FRIDAY_CONFIG["app_id"]}',
        'Content-Type': 'application/json'
    }

    try:
        print(f"📡 发送测试请求到: {FRIDAY_CONFIG['base_url']}")
        print(f"🔑 使用AppID: {FRIDAY_CONFIG['app_id']}")

        response = requests.post(
            FRIDAY_CONFIG["base_url"],
            headers=headers,
            json=payload,
            timeout=30
        )

        print(f"📊 响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ API连接成功！")
            print("\n📝 测试响应:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"\n🤖 AI回答: {content}")
                return True
            else:
                print("⚠️ 响应格式异常")
                return False
        else:
            print(f"❌ API调用失败")
            print(f"错误信息: {response.text}")
            return False

    except requests.RequestException as e:
        print(f"❌ 网络请求异常: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_article_summary():
    """测试文章总结功能"""
    print("\n🧪 测试文章总结功能...")

    # 模拟文章数据
    test_article = {
        "title": "ChatGPT - OpenAI推出的对话式AI助手",
        "category": "AI工具",
        "publish_time": "1天前",
        "description": "ChatGPT是OpenAI开发的大型语言模型，能够进行自然对话，回答问题，协助写作等多种任务。",
        "url": "https://example.com/chatgpt"
    }

    prompt = f"""请对以下AI工具/项目文章进行专业分析和总结，提取关键信息：

文章标题：{test_article.get('title', '')}
文章分类：{test_article.get('category', '')}
发布时间：{test_article.get('publish_time', '')}
原始描述：{test_article.get('description', '')}

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

请确保总结内容简洁明了，每部分控制在50字以内。"""

    payload = {
        "model": FRIDAY_CONFIG["model"],
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "temperature": 0.7,
        "max_tokens": 800
    }

    headers = {
        'Authorization': f'Bearer {FRIDAY_CONFIG["app_id"]}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(
            FRIDAY_CONFIG["base_url"],
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print("✅ 文章总结测试成功！")
                print("\n📄 测试文章:")
                print(f"标题: {test_article['title']}")
                print(f"分类: {test_article['category']}")
                print(f"描述: {test_article['description']}")
                print("\n🤖 AI总结结果:")
                print(content)
                return True
            else:
                print("⚠️ 响应格式异常")
                return False
        else:
            print(f"❌ 文章总结测试失败: {response.text}")
            return False

    except Exception as e:
        print(f"❌ 文章总结测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🚀 美团Friday API 功能测试")
    print("=" * 60)

    # 基础连接测试
    basic_test = test_friday_api()

    if basic_test:
        # 文章总结功能测试
        summary_test = test_article_summary()

        print("\n" + "=" * 60)
        print("📊 测试结果总结")
        print("=" * 60)
        print(f"✅ 基础API连接: {'通过' if basic_test else '失败'}")
        print(f"✅ 文章总结功能: {'通过' if summary_test else '失败'}")

        if basic_test and summary_test:
            print("\n🎉 所有测试通过！可以开始使用AI文章总结系统。")
        else:
            print("\n⚠️ 部分测试失败，请检查配置和网络连接。")
    else:
        print("\n❌ 基础API连接失败，请检查AppID和网络连接。")

if __name__ == "__main__":
    main()
