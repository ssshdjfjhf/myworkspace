#!/bin/bash

# AI工具集爬虫启动脚本

echo "🚀 启动AI工具集爬虫..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt > /dev/null 2>&1

# 运行爬虫
echo "🕷️ 开始爬取..."
python ai_news_scraper.py

echo "✅ 爬取完成！"
echo "📁 查看生成的文件："
ls -la *.json *.csv 2>/dev/null | head -5
