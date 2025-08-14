#!/bin/bash

# 命令行进阶学习练习脚本
# 这个脚本会创建完整的进阶练习环境

echo "🚀 欢迎来到命令行进阶学习！"
echo "正在为你创建完整的练习环境..."
echo ""

# 创建主练习目录
echo "📁 创建练习目录结构..."
mkdir -p practice-area-advanced/{data,logs,backup,organized,scripts}

# 创建文本处理练习数据
echo "📄 创建文本处理练习数据..."

# 学生名单
cat > practice-area-advanced/data/students.txt << 'EOF'
张小明
李小红
王小强
赵小美
陈小华
刘小东
杨小丽
周小军
吴小燕
郑小峰
孙小梅
马小龙
朱小芳
胡小伟
高小娟
林小涛
何小敏
宋小刚
唐小雪
韩小磊
EOF

# 数字文件
cat > practice-area-advanced/data/numbers.txt << 'EOF'
45
12
78
23
56
89
34
67
91
15
EOF

# 颜色文件（包含重复）
cat > practice-area-advanced/data/colors.txt << 'EOF'
红色
蓝色
绿色
红色
黄色
蓝色
紫色
橙色
绿色
黑色
白色
红色
EOF

# 作文文件
cat > practice-area-advanced/data/essay.txt << 'EOF'
命令行是程序员必备的技能之一。通过学习命令行，我们可以更高效地操作计算机。
文本处理是命令行的重要应用场景。grep命令可以帮助我们快速搜索文件内容。
管道操作让我们能够组合多个命令，实现复杂的数据处理流程。
系统监控帮助我们了解计算机的运行状态，及时发现和解决问题。
脚本编程让我们能够自动化重复性任务，大大提高工作效率。
学习命令行需要多练习，熟能生巧。每个命令都要亲自尝试，才能真正掌握。
EOF

# 创建日志文件
echo "📋 创建系统日志文件..."
cat > practice-area-advanced/logs/app.log << 'EOF'
2024-01-15 09:00:01 INFO Application started
2024-01-15 09:00:05 INFO User login: admin
2024-01-15 09:01:23 WARNING Low disk space
2024-01-15 09:02:45 ERROR Database connection failed
2024-01-15 09:03:12 INFO Database connection restored
2024-01-15 09:05:33 INFO User login: user123
2024-01-15 09:07:21 ERROR File not found: config.xml
2024-01-15 09:08:45 WARNING Memory usage high
2024-01-15 09:10:12 INFO Backup completed
2024-01-15 09:12:34 ERROR Network timeout
2024-01-15 09:15:21 INFO User logout: admin
2024-01-15 09:16:45 WARNING Disk cleanup needed
2024-01-15 09:18:23 INFO System maintenance started
2024-01-15 09:20:12 ERROR Permission denied
2024-01-15 09:22:34 INFO System maintenance completed
EOF

# 创建示例脚本
echo "🔧 创建示例脚本..."

# Hello World脚本
cat > practice-area-advanced/scripts/hello.sh << 'EOF'
#!/bin/bash
echo "Hello, World!"
echo "当前时间：$(date)"
echo "当前用户：$(whoami)"
EOF

# 简单的计算器脚本
cat > practice-area-advanced/scripts/calculator.sh << 'EOF'
#!/bin/bash
echo "简单计算器"
read -p "请输入第一个数字: " num1
read -p "请输入第二个数字: " num2

echo "加法: $num1 + $num2 = $((num1 + num2))"
echo "减法: $num1 - $num2 = $((num1 - num2))"
echo "乘法: $num1 × $num2 = $((num1 * num2))"
if [ $num2 -ne 0 ]; then
    echo "除法: $num1 ÷ $num2 = $((num1 / num2))"
else
    echo "除法: 不能除以零"
fi
EOF

# 给脚本执行权限
chmod +x practice-area-advanced/scripts/*.sh

# 创建一些测试文件用于文件整理练习
echo "📎 创建测试文件..."
touch practice-area-advanced/test1.txt
touch practice-area-advanced/test2.md
touch practice-area-advanced/image1.jpg
touch practice-area-advanced/image2.png
touch practice-area-advanced/script1.sh

echo "✅ 进阶练习环境创建完成！"
echo ""
echo "🎯 现在你可以开始进阶练习了："
echo ""
echo "第一阶段 - 文本处理："
echo "  cd practice-area-advanced/data"
echo "  grep '张' students.txt"
echo "  head -5 students.txt"
echo "  wc -l students.txt"
echo ""
echo "第二阶段 - 管道和重定向："
echo "  cd practice-area-advanced"
echo "  ls | grep '.txt'"
echo "  cat data/students.txt | grep '小' | wc -l"
echo "  ls > 文件列表.txt"
echo ""
echo "第三阶段 - 系统监控："
echo "  ps aux | head -10"
echo "  df -h"
echo "  free -h"
echo ""
echo "第四阶段 - 文本编辑："
echo "  nano data/students.txt"
echo "  # 添加新学生然后保存"
echo ""
echo "第五阶段 - 脚本编程："
echo "  cd scripts"
echo "  ./hello.sh"
echo "  ./calculator.sh"
echo ""
echo "💡 提示：每个阶段都有对应的详细教程文件，记得先阅读教程！"
echo "📚 教程文件："
echo "  - 01-文本处理练习.md"
echo "  - 02-管道重定向练习.md"
echo "  - 03-系统监控练习.md"
echo "  - 04-文本编辑器练习.md"
echo "  - 05-脚本编程练习.md"
echo ""
echo "🎉 祝你学习愉快！记住：多练习是掌握命令行的关键！"
