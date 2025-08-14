#!/bin/bash

# Git学习练习脚本
# 这个脚本会创建一个完整的Git练习环境

echo "🚀 欢迎来到Git学习练习！"
echo "这个脚本会为你创建一个完整的Git练习环境"
echo ""

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装，请先安装Git"
    echo "macOS: brew install git"
    echo "Ubuntu: sudo apt install git"
    echo "Windows: 下载Git for Windows"
    exit 1
fi

echo "✅ Git已安装，版本：$(git --version)"
echo ""

# 检查Git配置
if ! git config --global user.name &> /dev/null || ! git config --global user.email &> /dev/null; then
    echo "⚠️  Git用户信息未配置，请先配置："
    echo "git config --global user.name \"你的姓名\""
    echo "git config --global user.email \"你的邮箱\""
    echo ""
    read -p "是否现在配置？(y/n): " configure_now
    if [[ $configure_now == "y" || $configure_now == "Y" ]]; then
        read -p "请输入你的姓名: " user_name
        read -p "请输入你的邮箱: " user_email
        git config --global user.name "$user_name"
        git config --global user.email "$user_email"
        echo "✅ Git配置完成"
    else
        echo "请手动配置后再运行此脚本"
        exit 1
    fi
fi

echo "📋 当前Git配置："
echo "用户名: $(git config --global user.name)"
echo "邮箱: $(git config --global user.email)"
echo ""

# 创建练习目录
PRACTICE_DIR="git-practice-workspace"
if [ -d "$PRACTICE_DIR" ]; then
    echo "⚠️  练习目录已存在，是否删除重新创建？"
    read -p "(y/n): " recreate
    if [[ $recreate == "y" || $recreate == "Y" ]]; then
        rm -rf "$PRACTICE_DIR"
        echo "🗑️  已删除旧的练习目录"
    else
        echo "使用现有目录"
    fi
fi

if [ ! -d "$PRACTICE_DIR" ]; then
    mkdir "$PRACTICE_DIR"
    echo "📁 创建练习目录: $PRACTICE_DIR"
fi

cd "$PRACTICE_DIR"

# 创建练习项目1：基础操作练习
echo "📝 创建练习项目1：基础操作练习"
mkdir -p basic-practice
cd basic-practice

# 初始化Git仓库
git init
echo "✅ 初始化Git仓库"

# 创建README文件
cat > README.md << 'EOF'
# Git基础操作练习项目

这是一个用于学习Git基础操作的练习项目。

## 学习目标
- 掌握Git基本命令
- 理解工作区、暂存区、版本库概念
- 学会查看提交历史和状态

## 练习内容
1. 文件添加和提交
2. 查看状态和差异
3. 提交历史查看
EOF

# 创建一些示例文件
echo "console.log('Hello, Git!');" > hello.js
echo "body { font-family: Arial, sans-serif; }" > style.css

cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Git练习项目</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>欢迎来到Git学习</h1>
    <p>这是一个练习项目</p>
    <script src="hello.js"></script>
</body>
</html>
EOF

# 创建.gitignore文件
cat > .gitignore << 'EOF'
# 日志文件
*.log

# 临时文件
*.tmp
*.temp

# 系统文件
.DS_Store
Thumbs.db

# IDE文件
.vscode/
.idea/
EOF

echo "📄 创建示例文件完成"

# 第一次提交
git add README.md
git commit -m "feat: 添加项目README文档"

git add .gitignore
git commit -m "feat: 添加.gitignore文件"

git add .
git commit -m "feat: 添加HTML、CSS、JavaScript文件"

echo "✅ 完成初始提交"

# 创建一些临时文件（用于演示.gitignore）
echo "这是一个日志文件" > app.log
echo "这是一个临时文件" > temp.tmp

cd ..

# 创建练习项目2：分支操作练习
echo ""
echo "🌿 创建练习项目2：分支操作练习"
mkdir -p branch-practice
cd branch-practice

git init

# 创建主分支内容
cat > README.md << 'EOF'
# Git分支操作练习

这个项目用于练习Git分支操作。

## 分支策略
- main: 主分支
- feature/*: 功能分支
- hotfix/*: 热修复分支

## 练习内容
1. 创建和切换分支
2. 分支合并
3. 冲突解决
EOF

cat > app.py << 'EOF'
#!/usr/bin/env python3
"""
简单的Python应用
用于Git分支练习
"""

def main():
    print("欢迎使用Git分支练习应用")
    print("版本: 1.0.0")

if __name__ == "__main__":
    main()
EOF

git add .
git commit -m "feat: 初始化分支练习项目"

# 创建feature分支
git checkout -b feature/add-calculator

cat > calculator.py << 'EOF'
#!/usr/bin/env python3
"""
简单计算器模块
"""

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Error: Division by zero"

if __name__ == "__main__":
    print("计算器模块测试")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"5 - 2 = {subtract(5, 2)}")
    print(f"4 * 3 = {multiply(4, 3)}")
    print(f"8 / 2 = {divide(8, 2)}")
EOF

# 修改主应用文件
cat > app.py << 'EOF'
#!/usr/bin/env python3
"""
简单的Python应用
用于Git分支练习
"""

from calculator import add, subtract, multiply, divide

def main():
    print("欢迎使用Git分支练习应用")
    print("版本: 1.1.0 - 添加计算器功能")

    # 简单的计算器演示
    print("\n计算器演示:")
    print(f"10 + 5 = {add(10, 5)}")
    print(f"10 - 5 = {subtract(10, 5)}")
    print(f"10 * 5 = {multiply(10, 5)}")
    print(f"10 / 5 = {divide(10, 5)}")

if __name__ == "__main__":
    main()
EOF

git add .
git commit -m "feat: 添加计算器功能"

# 切换回主分支
git checkout main

# 创建另一个feature分支（用于演示冲突）
git checkout -b feature/add-greeting

cat > greeting.py << 'EOF'
#!/usr/bin/env python3
"""
问候语模块
"""

def say_hello(name="World"):
    return f"Hello, {name}!"

def say_goodbye(name="World"):
    return f"Goodbye, {name}!"

if __name__ == "__main__":
    print(say_hello("Git学习者"))
    print(say_goodbye("Git学习者"))
EOF

# 修改主应用文件（这里会产生冲突）
cat > app.py << 'EOF'
#!/usr/bin/env python3
"""
简单的Python应用
用于Git分支练习
"""

from greeting import say_hello, say_goodbye

def main():
    print("欢迎使用Git分支练习应用")
    print("版本: 1.1.0 - 添加问候功能")

    # 问候语演示
    print("\n问候语演示:")
    print(say_hello("Git学习者"))
    print(say_goodbye("Git学习者"))

if __name__ == "__main__":
    main()
EOF

git add .
git commit -m "feat: 添加问候语功能"

# 切换回主分支
git checkout main

echo "✅ 分支练习环境创建完成"

cd ..

# 创建练习项目3：远程仓库练习（模拟）
echo ""
echo "🌐 创建练习项目3：远程仓库模拟练习"
mkdir -p remote-practice
cd remote-practice

# 创建"远程"仓库（实际是本地的bare仓库）
git init --bare ../remote-repo.git
echo "📦 创建模拟远程仓库"

# 克隆"远程"仓库
git clone ../remote-repo.git .

# 创建初始内容
cat > README.md << 'EOF'
# Git远程仓库练习

这个项目用于练习Git远程仓库操作。

## 练习内容
1. 克隆远程仓库
2. 推送和拉取
3. 远程分支管理
4. 团队协作模拟

## 远程仓库操作
- git clone: 克隆仓库
- git push: 推送到远程
- git pull: 从远程拉取
- git fetch: 获取远程更新
EOF

cat > team-info.md << 'EOF'
# 团队信息

## 成员列表
- 开发者A: 负责前端开发
- 开发者B: 负责后端开发
- 开发者C: 负责测试

## 协作规范
1. 每个功能使用独立分支开发
2. 代码review后才能合并到主分支
3. 保持提交信息清晰明确
EOF

git add .
git commit -m "feat: 初始化远程仓库练习项目"
git push origin main

echo "✅ 远程仓库练习环境创建完成"

cd ..

# 创建练习指导文件
echo ""
echo "📚 创建练习指导文件"

cat > 练习指导.md << 'EOF'
# Git练习指导

欢迎来到Git练习环境！这里为你准备了三个练习项目。

## 📁 练习项目说明

### 1. basic-practice - 基础操作练习
**位置**: `basic-practice/`
**目标**: 掌握Git基础命令

**练习步骤**:
```bash
cd basic-practice

# 查看仓库状态
git status

# 查看提交历史
git log --oneline

# 修改文件并查看差异
echo "console.log('学习Git真有趣!');" >> hello.js
git diff

# 添加并提交修改
git add hello.js
git commit -m "update: 添加新的日志输出"

# 查看文件历史
git log --oneline hello.js
```

### 2. branch-practice - 分支操作练习
**位置**: `branch-practice/`
**目标**: 掌握分支创建、切换、合并

**练习步骤**:
```bash
cd branch-practice

# 查看所有分支
git branch -a

# 合并calculator功能分支
git merge feature/add-calculator

# 尝试合并greeting分支（会产生冲突）
git merge feature/add-greeting

# 解决冲突后提交
# 编辑app.py文件，解决冲突
git add app.py
git commit -m "merge: 解决功能分支冲突"

# 删除已合并的分支
git branch -d feature/add-calculator
git branch -d feature/add-greeting
```

### 3. remote-practice - 远程仓库练习
**位置**: `remote-practice/`
**目标**: 掌握远程仓库操作

**练习步骤**:
```bash
cd remote-practice

# 查看远程仓库信息
git remote -v

# 创建新分支并推送
git checkout -b feature/add-docs
echo "# 项目文档" > docs.md
git add docs.md
git commit -m "feat: 添加项目文档"
git push origin feature/add-docs

# 模拟其他开发者的修改
cd ../
git clone remote-repo.git developer-b
cd developer-b
echo "开发者B的修改" >> team-info.md
git add team-info.md
git commit -m "update: 开发者B添加信息"
git push origin main

# 回到原项目，拉取更新
cd ../remote-practice
git pull origin main
```

## 🎯 练习检查清单

完成练习后，你应该能够：

### 基础操作
- [ ] 查看仓库状态 (`git status`)
- [ ] 添加文件到暂存区 (`git add`)
- [ ] 提交修改 (`git commit`)
- [ ] 查看提交历史 (`git log`)
- [ ] 查看文件差异 (`git diff`)

### 分支操作
- [ ] 查看分支列表 (`git branch`)
- [ ] 创建新分支 (`git checkout -b`)
- [ ] 切换分支 (`git checkout`)
- [ ] 合并分支 (`git merge`)
- [ ] 解决合并冲突
- [ ] 删除分支 (`git branch -d`)

### 远程操作
- [ ] 查看远程仓库 (`git remote -v`)
- [ ] 推送到远程 (`git push`)
- [ ] 从远程拉取 (`git pull`)
- [ ] 克隆仓库 (`git clone`)

## 💡 练习提示

1. **不要害怕出错**: Git几乎所有操作都可以撤销
2. **多使用git status**: 随时了解仓库状态
3. **善用git log**: 查看提交历史帮助理解项目演进
4. **练习冲突解决**: 这是团队协作的重要技能
5. **保持提交信息清晰**: 好的提交信息是团队协作的基础

## 🆘 遇到问题？

如果遇到问题，可以：
1. 使用 `git help <命令>` 查看帮助
2. 查看 `Git常用命令速查表.md`
3. 重新阅读 `Git基础教程.md`
4. 参考 `Git实战练习.md` 中的详细步骤

## 🎉 完成练习后

恭喜你完成了Git基础练习！现在你可以：
1. 在实际项目中应用这些技能
2. 学习更高级的Git功能
3. 探索GitHub、GitLab等代码托管平台
4. 学习团队协作工作流

继续加油，Git会成为你开发路上的得力助手！🚀
EOF

# 创建快速开始脚本
cat > 快速开始.sh << 'EOF'
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
EOF

chmod +x 快速开始.sh

echo ""
echo "🎉 Git练习环境创建完成！"
echo ""
echo "📁 创建的内容："
echo "├── basic-practice/          # 基础操作练习"
echo "├── branch-practice/         # 分支操作练习"
echo "├── remote-practice/         # 远程仓库练习"
echo "├── remote-repo.git/         # 模拟远程仓库"
echo "├── 练习指导.md              # 详细练习指导"
echo "└── 快速开始.sh              # 快速开始脚本"
echo ""
echo "🚀 开始练习："
echo "1. 阅读练习指导: cat 练习指导.md"
echo "2. 快速开始: ./快速开始.sh"
echo "3. 或直接进入练习目录开始练习"
echo ""
echo "💡 提示: 建议先阅读 Git基础教程.md 和 Git实战练习.md"
echo "📋 需要时查看 Git常用命令速查表.md"
echo ""
echo "祝你学习愉快！🎊"
