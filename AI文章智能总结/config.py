#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI文章智能总结系统配置文件
"""

# 美团Friday API配置
FRIDAY_CONFIG = {
    "app_id": "21910615279495929878",  # 你的AppID
    "base_url": "https://aigc.sankuai.com/v1/openai/native/chat/completions",
    "model": "LongCat-Large-32K-Chat",
    "temperature": 0.7,
    "max_tokens": 1000,
    "timeout": 30
}

# 爬虫数据文件路径配置
DATA_CONFIG = {
    "input_file": "../爬取AI咨询/ai_articles_20250814_201716.json",  # 输入文件路径
    "output_dir": "./",  # 输出目录
}

# 处理配置
PROCESS_CONFIG = {
    "batch_size": 3,  # 批处理大小（建议3-5）
    "delay": 3.0,     # 批次间延迟（秒）
    "base_delay": 0.5,  # 基础延迟（秒）
    "max_retries": 3   # 最大重试次数
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "file": "ai_summarizer.log"
}

# 提示词模板配置
PROMPT_CONFIG = {
    "system_prompt": """你是一个专业的AI技术分析师，擅长对AI工具和项目进行深度分析和总结。""",

    "analysis_sections": [
        "🎯 核心功能",
        "🔧 主要特点",
        "🏷️ 应用场景",
        "💡 创新点",
        "📊 实用性评估"
    ],

    "guidelines": [
        "专业准确，突出技术特点",
        "简洁明了，每部分控制在50字以内",
        "客观中性，避免过度营销语言",
        "突出实用价值和应用前景"
    ]
}
