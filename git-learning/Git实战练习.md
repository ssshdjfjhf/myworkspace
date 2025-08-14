# 🏃‍♂️ Git实战练习 - 动手学Git

理论学完了，现在让我们通过实际操作来掌握Git！

## 🎯 练习目标

通过一系列实战练习，让你：
- 熟练掌握Git基本操作
- 理解Git工作流程
- 学会处理常见问题
- 建立良好的Git使用习惯

## 📋 练习前准备

### 检查Git安装
```bash
git --version
```
如果没有安装，请先安装Git。

### 配置Git（如果还没配置）
```bash
git config --global user.name "你的姓名"
git config --global user.email "你的邮箱"
```

## 🚀 练习1：创建第一个Git仓库

### 步骤1：创建项目文件夹
```bash
cd ~/Documents
mkdir my-first-git-project
cd my-first-git-project
```

### 步骤2：初始化Git仓库
```bash
git init
```

### 步骤3：创建第一个文件
```bash
echo "# 我的第一个Git项目" > README.md
echo "这是一个学习Git的练习项目" >> README.md
```

### 步骤4：查看状态并提交
```bash
# 查看状态
git status

# 添加文件到暂存区
git add README.md

# 再次查看状态
git status

# 提交到版本库
git commit -m "feat: 添加README文件"

# 查看提交历史
git log
```

### ✅ 练习1检查点
- [ ] 成功创建Git仓库
- [ ] 理解了工作区、暂存区、版本库的概念
- [ ] 完成了第一次提交

## 🔄 练习2：文件修改和版本管理

### 步骤1：修改文件
```bash
echo "" >> README.md
echo "## 项目功能" >> README.md
echo "- 学习Git基础操作" >> README.md
echo "- 掌握版本控制" >> README.md
```

### 步骤2：查看差异
```bash
# 查看修改了什么
git diff

# 查看文件状态
git status
```

### 步骤3：提交修改
```bash
git add README.md
git commit -m "docs: 添加项目功能说明"
```

### 步骤4：创建更多文件
```bash
# 创建一个简单的HTML文件
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>我的Git练习项目</title>
</head>
<body>
    <h1>欢迎来到我的Git练习项目</h1>
    <p>这是我学习Git时创建的第一个网页。</p>
</body>
</html>
EOF

# 创建一个CSS文件
cat > style.css << 'EOF'
body {
    font-family: Arial, sans-serif;
    margin: 40px;
    background-color: #f5f5f5;
}

h1 {
    color: #333;
    text-align: center;
}

p {
    color: #666;
    line-height: 1.6;
}
EOF
```

### 步骤5：批量添加和提交
```bash
# 查看状态
git status

# 添加所有文件
git add .

# 提交
git commit -m "feat: 添加HTML和CSS文件"

# 查看提交历史
git log --oneline
```

### ✅ 练习2检查点
- [ ] 学会查看文件差异
- [ ] 掌握了批量添加文件
- [ ] 理解了提交历史的查看

## 🌿 练习3：分支操作

### 步骤1：创建并切换到新分支
```bash
# 创建并切换到feature分支
git checkout -b feature/add-javascript

# 查看当前分支
git branch
```

### 步骤2：在新分支上开发
```bash
# 创建JavaScript文件
cat > script.js << 'EOF'
// 简单的JavaScript功能
function showWelcomeMessage() {
    alert('欢迎来到我的Git练习项目！');
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    console.log('页面加载完成');
});
EOF

# 修改HTML文件，添加JavaScript引用
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>我的Git练习项目</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>欢迎来到我的Git练习项目</h1>
    <p>这是我学习Git时创建的第一个网页。</p>
    <button onclick="showWelcomeMessage()">点击我</button>
    <script src="script.js"></script>
</body>
</html>
EOF
```

### 步骤3：提交新功能
```bash
git add .
git commit -m "feat: 添加JavaScript交互功能"
```

### 步骤4：切换回主分支并合并
```bash
# 切换回主分支
git checkout master

# 查看文件（注意JavaScript功能不在这里）
ls
cat index.html

# 合并feature分支
git merge feature/add-javascript

# 查看合并后的文件
cat index.html

# 查看提交历史
git log --oneline --graph
```

### 步骤5：删除已合并的分支
```bash
git branch -d feature/add-javascript
git branch
```

### ✅ 练习3检查点
- [ ] 学会创建和切换分支
- [ ] 理解了分支的独立性
- [ ] 掌握了分支合并操作

## 🔧 练习4：处理冲突

### 步骤1：创建两个冲突的分支
```bash
# 创建分支A
git checkout -b feature/update-title-a
echo "# Git学习项目 - 版本A" > README.md
git add README.md
git commit -m "update: 修改标题为版本A"

# 切换回主分支
git checkout master

# 创建分支B
git checkout -b feature/update-title-b
echo "# Git实战练习项目 - 版本B" > README.md
git add README.md
git commit -m "update: 修改标题为版本B"
```

### 步骤2：先合并一个分支
```bash
git checkout master
git merge feature/update-title-a
```

### 步骤3：尝试合并第二个分支（会产生冲突）
```bash
git merge feature/update-title-b
```

### 步骤4：解决冲突
```bash
# 查看冲突状态
git status

# 查看冲突文件
cat README.md

# 手动编辑解决冲突（选择一个版本或合并两个版本）
echo "# Git学习与实战练习项目" > README.md
echo "这是一个学习Git的练习项目，包含基础操作和实战练习。" >> README.md

# 标记冲突已解决
git add README.md

# 完成合并
git commit -m "merge: 解决标题冲突，合并两个版本"
```

### 步骤5：清理分支
```bash
git branch -d feature/update-title-a
git branch -d feature/update-title-b
```

### ✅ 练习4检查点
- [ ] 理解了什么是合并冲突
- [ ] 学会手动解决冲突
- [ ] 掌握了冲突解决的完整流程

## 📝 练习5：.gitignore的使用

### 步骤1：创建一些不需要跟踪的文件
```bash
# 创建日志文件
echo "2024-01-01 应用启动" > app.log
echo "2024-01-01 用户登录" >> app.log

# 创建临时文件
echo "临时数据" > temp.tmp

# 创建配置文件（包含敏感信息）
echo "database_password=secret123" > config.env

# 查看状态
git status
```

### 步骤2：创建.gitignore文件
```bash
cat > .gitignore << 'EOF'
# 日志文件
*.log

# 临时文件
*.tmp

# 环境配置文件
*.env

# 系统文件
.DS_Store
Thumbs.db

# IDE文件
.vscode/
.idea/
EOF
```

### 步骤3：验证.gitignore效果
```bash
# 查看状态（注意哪些文件被忽略了）
git status

# 添加.gitignore文件
git add .gitignore
git commit -m "feat: 添加.gitignore文件"
```

### ✅ 练习5检查点
- [ ] 理解了.gitignore的作用
- [ ] 学会配置忽略规则
- [ ] 知道哪些文件应该被忽略

## 🔄 练习6：撤销操作

### 步骤1：练习撤销工作区修改
```bash
# 修改文件
echo "这是一个错误的修改" >> README.md

# 查看修改
git diff

# 撤销修改
git checkout -- README.md

# 验证撤销结果
git diff
```

### 步骤2：练习撤销暂存区操作
```bash
# 修改文件并添加到暂存区
echo "另一个修改" >> README.md
git add README.md

# 查看状态
git status

# 撤销暂存区操作
git reset HEAD README.md

# 查看状态
git status

# 撤销工作区修改
git checkout -- README.md
```

### 步骤3：练习修改最后一次提交
```bash
# 创建一个新文件但忘记添加到提交中
echo "忘记的文件内容" > forgotten.txt
git add forgotten.txt
git commit -m "feat: 添加新功能"

# 发现忘记修改README
echo "" >> README.md
echo "## 新增功能" >> README.md
echo "- 添加了新的功能模块" >> README.md

# 将忘记的修改添加到上一次提交
git add README.md
git commit --amend -m "feat: 添加新功能和说明文档"

# 查看提交历史
git log --oneline
```

### ✅ 练习6检查点
- [ ] 学会撤销工作区修改
- [ ] 掌握撤销暂存区操作
- [ ] 理解如何修改最后一次提交

## 🌐 练习7：远程仓库操作（可选）

如果你有GitHub账号，可以进行这个练习：

### 步骤1：在GitHub创建仓库
1. 登录GitHub
2. 点击"New repository"
3. 输入仓库名：`my-first-git-project`
4. 不要初始化README（我们已经有了）
5. 点击"Create repository"

### 步骤2：连接远程仓库
```bash
# 添加远程仓库（替换为你的GitHub用户名）
git remote add origin https://github.com/你的用户名/my-first-git-project.git

# 查看远程仓库
git remote -v
```

### 步骤3：推送到远程仓库
```bash
# 推送主分支
git push -u origin master

# 查看GitHub上的仓库
```

### 步骤4：模拟团队协作
```bash
# 在GitHub上直接编辑README.md文件，添加一行内容

# 拉取远程更新
git pull origin master

# 查看更新内容
cat README.md
```

### ✅ 练习7检查点
- [ ] 学会连接远程仓库
- [ ] 掌握推送和拉取操作
- [ ] 理解远程协作流程

## 🎉 综合练习：完整项目流程

现在让我们模拟一个完整的项目开发流程：

### 场景：开发一个简单的待办事项应用

```bash
# 1. 创建新功能分支
git checkout -b feature/todo-app

# 2. 创建HTML结构
cat > todo.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>待办事项应用</title>
    <link rel="stylesheet" href="todo.css">
</head>
<body>
    <div class="container">
        <h1>我的待办事项</h1>
        <input type="text" id="todoInput" placeholder="输入新的待办事项">
        <button onclick="addTodo()">添加</button>
        <ul id="todoList"></ul>
    </div>
    <script src="todo.js"></script>
</body>
</html>
EOF

# 3. 创建CSS样式
cat > todo.css << 'EOF'
.container {
    max-width: 600px;
    margin: 50px auto;
    padding: 20px;
    font-family: Arial, sans-serif;
}

h1 {
    text-align: center;
    color: #333;
}

input[type="text"] {
    width: 70%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    padding: 10px;
    margin: 5px 0;
    background-color: #f8f9fa;
    border-radius: 4px;
}
EOF

# 4. 创建JavaScript功能
cat > todo.js << 'EOF'
let todos = [];

function addTodo() {
    const input = document.getElementById('todoInput');
    const todoText = input.value.trim();

    if (todoText) {
        todos.push(todoText);
        input.value = '';
        renderTodos();
    }
}

function renderTodos() {
    const todoList = document.getElementById('todoList');
    todoList.innerHTML = '';

    todos.forEach((todo, index) => {
        const li = document.createElement('li');
        li.textContent = todo;
        todoList.appendChild(li);
    });
}

// 回车键添加待办事项
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('todoInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTodo();
        }
    });
});
EOF

# 5. 提交新功能
git add .
git commit -m "feat: 添加待办事项应用"

# 6. 切换回主分支并合并
git checkout master
git merge feature/todo-app

# 7. 删除功能分支
git branch -d feature/todo-app

# 8. 查看最终结果
git log --oneline --graph
ls -la
```

## 🏆 练习完成检查清单

完成所有练习后，你应该能够：

### 基础操作
- [ ] 初始化Git仓库
- [ ] 添加和提交文件
- [ ] 查看提交历史和状态
- [ ] 查看文件差异

### 分支管理
- [ ] 创建和切换分支
- [ ] 合并分支
- [ ] 删除分支
- [ ] 解决合并冲突

### 高级操作
- [ ] 使用.gitignore忽略文件
- [ ] 撤销各种操作
- [ ] 修改提交信息
- [ ] 连接和使用远程仓库

### 实战技能
- [ ] 完整的项目开发流程
- [ ] 良好的提交信息习惯
- [ ] 合理的分支策略
- [ ] 问题排查和解决

## 🎯 下一步学习建议

完成这些练习后，你可以：

1. **深入学习Git高级功能**
   - `git rebase`：重写提交历史
   - `git cherry-pick`：选择性合并提交
   - `git stash`：临时保存修改

2. **学习团队协作工具**
   - GitHub/GitLab的使用
   - Pull Request/Merge Request流程
   - Code Review最佳实践

3. **掌握Git工作流**
   - Git Flow工作流
   - GitHub Flow工作流
   - GitLab Flow工作流

4. **自动化和集成**
   - Git Hooks的使用
   - CI/CD集成
   - 自动化测试

## 💡 学习心得记录

在这里记录你的学习心得：

```
我的Git学习心得：
1. 最难理解的概念：
2. 最有用的命令：
3. 遇到的问题和解决方法：
4. 下一步学习计划：
```

恭喜你完成了Git实战练习！现在你已经具备了使用Git进行版本控制的基本技能。记住，熟练使用Git需要大量的实践，继续在实际项目中应用这些技能吧！🚀
