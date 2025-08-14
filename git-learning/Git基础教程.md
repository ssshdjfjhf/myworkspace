# 🚀 Git基础教程 - 从零开始

欢迎来到Git的世界！这里是你学习版本控制的起点。

## 什么是Git？

Git是一个**分布式版本控制系统**，简单来说就是：
- 📝 **记录文件变化**：像给你的代码拍照，记录每次修改
- 🔄 **版本管理**：可以随时回到之前的任何版本
- 👥 **团队协作**：多人可以同时修改同一个项目
- 🌿 **分支管理**：可以创建不同的开发分支

## 为什么要学Git？

- ✅ **不怕丢失代码**：所有历史版本都保存着
- ✅ **方便团队合作**：多人开发不会冲突
- ✅ **实验新功能**：可以创建分支尝试，不影响主代码
- ✅ **找回删除的文件**：误删了也能恢复
- ✅ **工作必备技能**：几乎所有公司都在用

## 基础概念

### 仓库（Repository）
- 就是一个项目文件夹，Git会跟踪这个文件夹里的所有变化
- 分为**本地仓库**（你电脑上的）和**远程仓库**（GitHub、GitLab等）

### 工作区、暂存区、版本库
```
工作区 → 暂存区 → 版本库
 ↓        ↓        ↓
修改文件  git add  git commit
```

### 分支（Branch）
- 想象成平行宇宙，你可以在不同分支上做不同的实验
- `master/main`：主分支，通常是稳定版本
- `feature`：功能分支，开发新功能用

## 最基础的Git命令

### 1. 配置Git（第一次使用必须做）
```bash
# 设置你的姓名和邮箱
git config --global user.name "你的姓名"
git config --global user.email "你的邮箱@example.com"

# 查看配置
git config --list
```

### 2. 创建仓库
```bash
# 方法1：在现有文件夹中初始化Git
cd 你的项目文件夹
git init

# 方法2：克隆远程仓库
git clone https://github.com/用户名/仓库名.git
```

### 3. 基本工作流程
```bash
# 查看文件状态
git status

# 添加文件到暂存区
git add 文件名              # 添加单个文件
git add .                   # 添加所有文件
git add *.txt               # 添加所有txt文件

# 提交到版本库
git commit -m "提交说明"

# 查看提交历史
git log
git log --oneline           # 简洁版本
```

### 4. 查看和比较
```bash
# 查看文件差异
git diff                    # 工作区与暂存区的差异
git diff --cached           # 暂存区与版本库的差异
git diff HEAD               # 工作区与版本库的差异

# 查看文件状态
git status
```

### 5. 撤销操作
```bash
# 撤销工作区的修改
git checkout -- 文件名

# 撤销暂存区的文件（取消add）
git reset HEAD 文件名

# 撤销最近一次提交
git reset --soft HEAD~1     # 保留修改
git reset --hard HEAD~1     # 丢弃修改（危险！）
```

## 分支操作

### 基本分支命令
```bash
# 查看分支
git branch                  # 查看本地分支
git branch -a               # 查看所有分支

# 创建分支
git branch 分支名

# 切换分支
git checkout 分支名
git switch 分支名            # 新版本推荐

# 创建并切换分支
git checkout -b 分支名
git switch -c 分支名         # 新版本推荐

# 合并分支
git merge 分支名

# 删除分支
git branch -d 分支名         # 安全删除
git branch -D 分支名         # 强制删除
```

## 远程仓库操作

### 基本远程操作
```bash
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin https://github.com/用户名/仓库名.git

# 推送到远程仓库
git push origin 分支名
git push -u origin master    # 第一次推送，设置上游分支

# 从远程仓库拉取
git pull origin 分支名
git pull                     # 拉取当前分支

# 获取远程仓库信息（不合并）
git fetch
```

## 实用技巧

### 1. .gitignore文件
创建`.gitignore`文件，告诉Git哪些文件不需要跟踪：
```
# 忽略所有.log文件
*.log

# 忽略node_modules文件夹
node_modules/

# 忽略系统文件
.DS_Store
Thumbs.db

# 忽略IDE配置文件
.vscode/
.idea/
```

### 2. 常用别名设置
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
```

### 3. 查看漂亮的提交历史
```bash
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
```

## 常见问题解决

### 1. 提交信息写错了
```bash
git commit --amend -m "正确的提交信息"
```

### 2. 忘记添加文件到上次提交
```bash
git add 忘记的文件
git commit --amend --no-edit
```

### 3. 合并冲突
当出现冲突时：
1. 打开冲突文件，找到`<<<<<<<`、`=======`、`>>>>>>>`标记
2. 手动编辑，保留需要的内容
3. 删除冲突标记
4. `git add 文件名`
5. `git commit`

### 4. 误删文件恢复
```bash
git checkout HEAD -- 文件名
```

## 最佳实践

### 1. 提交信息规范
```bash
# 好的提交信息
git commit -m "feat: 添加用户登录功能"
git commit -m "fix: 修复密码验证bug"
git commit -m "docs: 更新README文档"

# 不好的提交信息
git commit -m "修改"
git commit -m "bug"
git commit -m "更新代码"
```

### 2. 提交频率
- ✅ **小步快跑**：功能完成一小部分就提交
- ✅ **逻辑清晰**：每次提交只做一件事
- ❌ **避免大提交**：不要积累太多修改才提交

### 3. 分支策略
- `main/master`：稳定的生产版本
- `develop`：开发分支
- `feature/功能名`：新功能开发
- `hotfix/bug名`：紧急bug修复

## 学习建议

### 第一周目标
- [ ] 配置Git环境
- [ ] 学会基本的add、commit、push
- [ ] 理解工作区、暂存区、版本库概念
- [ ] 能够查看提交历史

### 第二周目标
- [ ] 掌握分支的创建和切换
- [ ] 学会合并分支
- [ ] 理解远程仓库操作
- [ ] 能够解决简单的合并冲突

### 第三周目标
- [ ] 熟练使用各种撤销操作
- [ ] 掌握.gitignore的使用
- [ ] 学会查看文件差异
- [ ] 能够进行团队协作

## 下一步学习

掌握基础后，你可以学习：
- **GitHub/GitLab使用**：代码托管平台
- **Git Flow工作流**：团队协作规范
- **高级Git命令**：rebase、cherry-pick等
- **Git钩子**：自动化工作流

## 记住

- 🎯 **多练习**：Git需要大量实践才能熟练
- 🔍 **不怕出错**：Git几乎所有操作都可以撤销
- 📚 **善用帮助**：`git help 命令名` 查看详细帮助
- 👥 **多交流**：和同事、朋友一起学习Git

开始你的Git学习之旅吧！记住，每个程序员都是从这里开始的。🚀
