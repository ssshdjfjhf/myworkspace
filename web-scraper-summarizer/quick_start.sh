#!/bin/bash

# 网页爬取和AI总结工具 - 快速启动脚本

echo "🚀 网页爬取和AI总结工具 - 快速启动"
echo "=================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

echo "✅ Python环境检查通过"

# 检查pip
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到pip，请先安装pip"
    exit 1
fi

# 使用pip3如果存在，否则使用pip
PIP_CMD="pip"
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
fi

echo "✅ pip环境检查通过"

# 检查并创建虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ 虚拟环境创建失败"
        exit 1
    fi
fi

# 激活虚拟环境并安装依赖
echo "📦 正在安装Python依赖..."
source venv/bin/activate && pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败，请检查网络连接或权限"
    exit 1
fi

echo ""
echo "🎉 安装完成！现在你可以使用以下命令："
echo ""
echo "📖 查看详细使用说明："
echo "   cat 使用说明.md"
echo ""
echo "🌐 爬取并总结网页（已预配置美团Friday）："
echo "   source venv/bin/activate && python3 scrape_and_summarize.py \"网页URL\""
echo ""
echo "🤖 查看Friday配置信息："
echo "   python3 friday_config.py"
echo ""
echo "💡 示例命令："
echo "   python3 scrape_and_summarize.py \"https://example.com\" --summary-type brief"
echo ""

# 检查是否提供了URL参数
if [ $# -eq 1 ]; then
    echo "🚀 检测到URL参数，正在运行..."
    source venv/bin/activate && python3 scrape_and_summarize.py "$1"
else
    echo "💭 提示：你可以直接运行 './quick_start.sh \"网页URL\"' 来快速开始"
fi
