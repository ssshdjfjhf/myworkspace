#!/bin/bash

# 命令行学习练习脚本
# 这个脚本会创建一些练习文件和文件夹，让你练习基础命令

echo "🎉 欢迎来到命令行学习练习！"
echo "这个脚本会为你创建一些练习材料"
echo ""

# 创建练习目录结构
echo "📁 正在创建练习目录..."
mkdir -p practice-area/documents
mkdir -p practice-area/images
mkdir -p practice-area/backup

# 创建一些练习文件
echo "📄 正在创建练习文件..."
echo "这是我的第一个文本文件！" > practice-area/documents/first.txt
echo "学习命令行真有趣" > practice-area/documents/learning.txt
echo "记住要多练习哦" > practice-area/documents/tips.txt

# 创建一个简单的数据文件
echo "苹果" > practice-area/documents/fruits.txt
echo "香蕉" >> practice-area/documents/fruits.txt
echo "橙子" >> practice-area/documents/fruits.txt

echo "✅ 练习环境创建完成！"
echo ""
echo "现在你可以尝试以下练习："
echo "1. cd practice-area          # 进入练习区域"
echo "2. ls                        # 查看文件夹内容"
echo "3. cd documents              # 进入documents文件夹"
echo "4. ls                        # 查看文件"
echo "5. cat first.txt             # 查看文件内容"
echo "6. cp first.txt ../backup/   # 复制文件到backup文件夹"
echo "7. cd ../backup              # 进入backup文件夹"
echo "8. ls                        # 确认文件已复制"
echo ""
echo "记住：如果不确定当前位置，随时可以用 pwd 命令查看！"
