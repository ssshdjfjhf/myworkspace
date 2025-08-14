#!/bin/bash
# AI文章智能总结系统启动脚本

echo "🚀 启动AI文章智能总结系统..."

# 检查虚拟环境是否存在
if [ ! -d "ai_env" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv ai_env
    echo "✅ 虚拟环境创建完成"
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source ai_env/bin/activate

# 检查依赖是否安装
echo "📋 检查依赖包..."
pip list | grep requests > /dev/null
if [ $? -ne 0 ]; then
    echo "📦 安装依赖包..."
    pip install requests beautifulsoup4
    echo "✅ 依赖包安装完成"
fi

# 进入AI总结目录
cd "AI文章智能总结"

echo ""
echo "🎯 选择操作："
echo "1. 测试API连接"
echo "2. 运行文章总结"
echo "3. 退出"
echo ""

read -p "请输入选择 (1-3): " choice

case $choice in
    1)
        echo "🧪 开始API测试..."
        python test_api.py
        ;;
    2)
        echo "📝 开始文章总结..."
        python ai_article_summarizer.py
        ;;
    3)
        echo "👋 退出系统"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "✅ 操作完成！"
echo "💡 提示：要退出虚拟环境，请运行 'deactivate' 命令"
