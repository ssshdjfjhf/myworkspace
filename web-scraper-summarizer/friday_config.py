#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美团Friday大模型配置文件
"""

# Friday API配置
FRIDAY_CONFIG = {
    "app_id": "21910615279495929878",
    "base_url": "https://aigc.sankuai.com/v1/openai/native",
    "default_model": "LongCat-8B-128K-Chat",
    "available_models": [
        "LongCat-8B-128K-Chat",
        "LongCat-Flash-Chat-Preview",
        "LongCat-Large-Thinking",
        "LongCat-MoE-3B-32K-Chat"
        # 可以根据实际可用模型添加更多
    ]
}

# 设置环境变量的便捷函数
def setup_friday_env():
    """
    设置Friday相关的环境变量
    """
    import os
    os.environ['FRIDAY_APP_ID'] = FRIDAY_CONFIG['app_id']
    os.environ['FRIDAY_BASE_URL'] = FRIDAY_CONFIG['base_url']
    os.environ['FRIDAY_DEFAULT_MODEL'] = FRIDAY_CONFIG['default_model']
    print("✅ Friday环境变量已设置")

if __name__ == "__main__":
    setup_friday_env()
    print(f"🤖 Friday配置信息:")
    print(f"   App ID: {FRIDAY_CONFIG['app_id']}")
    print(f"   Base URL: {FRIDAY_CONFIG['base_url']}")
    print(f"   默认模型: {FRIDAY_CONFIG['default_model']}")
    print(f"   可用模型: {', '.join(FRIDAY_CONFIG['available_models'])}")
