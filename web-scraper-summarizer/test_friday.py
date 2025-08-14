#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Friday API测试脚本
用于验证美团Friday大模型API是否正常工作
"""

import requests
import json
from friday_config import FRIDAY_CONFIG

def test_friday_api():
    """
    测试Friday API连接和响应
    """
    print("🧪 开始测试Friday API...")
    print(f"📱 App ID: {FRIDAY_CONFIG['app_id']}")
    print(f"🌐 Base URL: {FRIDAY_CONFIG['base_url']}")
    print(f"🤖 模型: {FRIDAY_CONFIG['default_model']}")
    print("-" * 50)

    # 准备请求
    headers = {
        'Authorization': f'Bearer {FRIDAY_CONFIG["app_id"]}',
        'Content-Type': 'application/json',
    }

    data = {
        "model": FRIDAY_CONFIG['default_model'],
        "messages": [
            {
                "role": "user",
                "content": "请简单介绍一下你自己，并说明你的主要功能。"
            }
        ],
        "stream": False
    }

    try:
        print("📡 发送测试请求...")
        response = requests.post(
            f"{FRIDAY_CONFIG['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        print(f"📊 响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ API调用成功！")
            print("\n🤖 Friday回复:")
            print("-" * 30)
            print(result['choices'][0]['message']['content'])
            print("-" * 30)

            # 显示一些统计信息
            if 'usage' in result:
                usage = result['usage']
                print(f"\n📈 Token使用情况:")
                print(f"   输入Token: {usage.get('prompt_tokens', 'N/A')}")
                print(f"   输出Token: {usage.get('completion_tokens', 'N/A')}")
                print(f"   总Token: {usage.get('total_tokens', 'N/A')}")

            return True

        else:
            print(f"❌ API调用失败")
            print(f"错误信息: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
        return False
    except json.JSONDecodeError:
        print("❌ 响应格式错误，无法解析JSON")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def test_summarization():
    """
    测试总结功能
    """
    print("\n" + "="*50)
    print("🧪 测试总结功能...")

    # 模拟一个简单的内容总结任务
    test_content = """
    人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，
    它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
    人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大。
    可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。
    """

    headers = {
        'Authorization': f'Bearer {FRIDAY_CONFIG["app_id"]}',
        'Content-Type': 'application/json',
    }

    data = {
        "model": FRIDAY_CONFIG['default_model'],
        "messages": [
            {
                "role": "user",
                "content": f"请对以下内容进行简要总结：\n\n{test_content}"
            }
        ],
        "stream": False
    }

    try:
        response = requests.post(
            f"{FRIDAY_CONFIG['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ 总结功能测试成功！")
            print("\n📝 总结结果:")
            print("-" * 30)
            print(result['choices'][0]['message']['content'])
            print("-" * 30)
            return True
        else:
            print(f"❌ 总结功能测试失败: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ 总结功能测试异常: {e}")
        return False

def main():
    print("🚀 Friday API 完整测试")
    print("="*50)

    # 测试基本API连接
    basic_test = test_friday_api()

    if basic_test:
        # 测试总结功能
        summary_test = test_summarization()

        print("\n" + "="*50)
        print("📋 测试结果总结:")
        print(f"   基本API测试: {'✅ 通过' if basic_test else '❌ 失败'}")
        print(f"   总结功能测试: {'✅ 通过' if summary_test else '❌ 失败'}")

        if basic_test and summary_test:
            print("\n🎉 所有测试通过！Friday API工作正常")
            print("💡 现在可以使用网页爬取和总结工具了")
        else:
            print("\n⚠️  部分测试失败，请检查配置")
    else:
        print("\n❌ 基本API测试失败，请检查App ID和网络连接")

if __name__ == "__main__":
    main()
