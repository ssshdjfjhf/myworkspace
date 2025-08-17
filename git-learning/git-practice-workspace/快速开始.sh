#!/bin/bash

echo "🚀 Git练习快速开始"
echo ""
echo "选择你要进行的练习："
echo "1. 基础操作练习 (basic-practice)"
echo "2. 分支操作练习 (branch-practice)"
echo "3. 远程仓库练习 (remote-practice)"
echo "4. 查看练习指导"
echo ""

read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo "进入基础操作练习..."
        cd basic-practice
        echo "当前目录: $(pwd)"
        echo "建议命令: git status, git log --oneline"
        ;;
    2)
        echo "进入分支操作练习..."
        cd branch-practice
        echo "当前目录: $(pwd)"
        echo "建议命令: git branch -a, git log --oneline --graph"
        ;;
    3)
        echo "进入远程仓库练习..."
        cd remote-practice
        echo "当前目录: $(pwd)"
        echo "建议命令: git remote -v, git log --oneline"
        ;;
    4)
        echo "查看练习指导..."
        cat 练习指导.md
        ;;
    *)
        echo "无效选项，请重新运行脚本"
        ;;
esac
