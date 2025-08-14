#!/bin/bash

# AI工具集爬虫启动脚本

echo "=== AI工具集网站爬虫 ==="
echo ""

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

echo ""
echo "请选择要运行的爬虫版本："
echo "1. 简化版爬虫 (simple_scraper.py) - 推荐"
echo "2. 完整版爬虫 (ai_news_scraper.py) - 功能全面"
echo "3. 增强版爬虫 (enhanced_scraper.py) - 改进版"
echo ""

read -p "请输入选择 (1-3): " choice

case $choice in
    1)
        echo "运行简化版爬虫..."
        python simple_scraper.py
        ;;
    2)
        echo "运行完整版爬虫..."
        python ai_news_scraper.py
        ;;
    3)
        echo "运行增强版爬虫..."
        python enhanced_scraper.py
        ;;
    *)
        echo "无效选择，运行简化版爬虫..."
        python simple_scraper.py
        ;;
esac

echo ""
echo "爬取完成！生成的文件："
ls -la *.json *.csv 2>/dev/null || echo "没有找到输出文件"

echo ""
echo "如需查看日志文件："
ls -la *.log 2>/dev/null || echo "没有日志文件"
