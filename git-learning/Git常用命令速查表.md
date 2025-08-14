# 📋 Git常用命令速查表

这是一个Git命令的快速参考指南，按功能分类整理，方便你快速查找需要的命令。

## 🔧 配置相关

### 初始配置
```bash
# 设置用户名和邮箱
git config --global user.name "你的姓名"
git config --global user.email "你的邮箱"

# 查看配置
git config --list
git config user.name
git config user.email

# 设置默认编辑器
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "vim"          # Vim

# 设置命令别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
```

## 📁 仓库操作

### 创建仓库
```bash
# 在当前目录初始化仓库
git init

# 克隆远程仓库
git clone <url>
git clone <url> <目录名>

# 克隆指定分支
git clone -b <分支名> <url>
```

## 📝 基本操作

### 文件状态
```bash
# 查看工作区状态
git status
git status -s                    # 简洁格式

# 查看文件差异
git diff                         # 工作区 vs 暂存区
git diff --cached               # 暂存区 vs 版本库
git diff HEAD                   # 工作区 vs 版本库
git diff <文件名>               # 查看特定文件差异
```

### 添加和提交
```bash
# 添加文件到暂存区
git add <文件名>
git add .                       # 添加所有文件
git add *.txt                   # 添加所有txt文件
git add -A                      # 添加所有修改（包括删除）

# 提交到版本库
git commit -m "提交信息"
git commit -am "提交信息"       # 添加并提交已跟踪文件
git commit --amend -m "新信息"  # 修改最后一次提交信息
```

### 查看历史
```bash
# 查看提交历史
git log
git log --oneline               # 简洁格式
git log --graph                 # 图形化显示
git log --stat                  # 显示文件变更统计
git log -p                      # 显示详细差异
git log -n 5                    # 显示最近5次提交

# 查看特定文件的历史
git log <文件名>
git log --follow <文件名>       # 跟踪文件重命名

# 查看提交详情
git show <提交ID>
git show HEAD                   # 查看最新提交
```

## 🌿 分支操作

### 分支管理
```bash
# 查看分支
git branch                      # 查看本地分支
git branch -r                   # 查看远程分支
git branch -a                   # 查看所有分支

# 创建分支
git branch <分支名>
git checkout -b <分支名>        # 创建并切换
git switch -c <分支名>          # 新语法

# 切换分支
git checkout <分支名>
git switch <分支名>             # 新语法

# 重命名分支
git branch -m <旧名> <新名>

# 删除分支
git branch -d <分支名>          # 安全删除
git branch -D <分支名>          # 强制删除
```

### 合并分支
```bash
# 合并分支
git merge <分支名>

# 取消合并
git merge --abort

# 变基合并
git rebase <分支名>
git rebase --continue           # 解决冲突后继续
git rebase --abort              # 取消变基
```

## 🔄 撤销操作

### 撤销修改
```bash
# 撤销工作区修改
git checkout -- <文件名>
git restore <文件名>            # 新语法

# 撤销暂存区修改
git reset HEAD <文件名>
git restore --staged <文件名>   # 新语法

# 撤销提交
git reset --soft HEAD~1         # 保留修改在暂存区
git reset --mixed HEAD~1        # 保留修改在工作区（默认）
git reset --hard HEAD~1         # 完全删除修改（危险！）

# 撤销特定提交
git revert <提交ID>             # 创建新提交来撤销
```

### 文件操作
```bash
# 删除文件
git rm <文件名>                 # 删除文件并暂存
git rm --cached <文件名>        # 从Git中删除但保留本地文件

# 移动/重命名文件
git mv <旧名> <新名>

# 恢复删除的文件
git checkout HEAD -- <文件名>
```

## 🌐 远程仓库

### 远程仓库管理
```bash
# 查看远程仓库
git remote
git remote -v                   # 显示详细信息

# 添加远程仓库
git remote add <名称> <url>
git remote add origin <url>

# 修改远程仓库URL
git remote set-url origin <新url>

# 删除远程仓库
git remote remove <名称>
```

### 同步操作
```bash
# 获取远程更新
git fetch                       # 获取所有远程分支
git fetch origin               # 获取origin的更新
git fetch origin <分支名>      # 获取特定分支

# 拉取并合并
git pull                       # 拉取当前分支
git pull origin <分支名>       # 拉取特定分支

# 推送到远程
git push                       # 推送当前分支
git push origin <分支名>       # 推送到特定分支
git push -u origin <分支名>    # 推送并设置上游分支
git push --all                 # 推送所有分支
git push --tags                # 推送所有标签
```

## 🏷️ 标签操作

```bash
# 创建标签
git tag <标签名>               # 轻量标签
git tag -a <标签名> -m "说明"  # 注释标签

# 查看标签
git tag                        # 列出所有标签
git tag -l "v1.*"             # 列出匹配的标签
git show <标签名>             # 查看标签详情

# 推送标签
git push origin <标签名>      # 推送特定标签
git push origin --tags        # 推送所有标签

# 删除标签
git tag -d <标签名>           # 删除本地标签
git push origin :refs/tags/<标签名>  # 删除远程标签
```

## 🔍 搜索和查找

```bash
# 在提交历史中搜索
git log --grep="关键词"        # 搜索提交信息
git log -S "代码内容"          # 搜索代码变更

# 在文件中搜索
git grep "关键词"              # 在工作区搜索
git grep "关键词" <提交ID>     # 在特定提交中搜索

# 查找文件
git ls-files                   # 列出所有跟踪的文件
git ls-files --others         # 列出未跟踪的文件
```

## 🗂️ 暂存操作

```bash
# 暂存当前修改
git stash
git stash save "暂存说明"

# 查看暂存列表
git stash list

# 应用暂存
git stash apply                # 应用最新暂存
git stash apply stash@{0}      # 应用特定暂存
git stash pop                  # 应用并删除最新暂存

# 删除暂存
git stash drop stash@{0}       # 删除特定暂存
git stash clear                # 删除所有暂存
```

## 🔧 高级操作

### 交互式操作
```bash
# 交互式添加
git add -i
git add -p                     # 部分添加文件

# 交互式变基
git rebase -i HEAD~3           # 修改最近3次提交

# 选择性合并
git cherry-pick <提交ID>       # 合并特定提交
```

### 文件忽略
```bash
# .gitignore 常用规则
*.log                          # 忽略所有.log文件
/temp                          # 忽略根目录下的temp文件夹
temp/                          # 忽略所有temp文件夹
!important.log                 # 不忽略important.log

# 忽略已跟踪的文件
git rm --cached <文件名>
git update-index --skip-worktree <文件名>
```

## 📊 统计和分析

```bash
# 提交统计
git shortlog -sn               # 按作者统计提交数
git log --author="作者名"      # 查看特定作者的提交

# 文件变更统计
git diff --stat                # 查看变更统计
git log --stat                 # 查看历史变更统计

# 代码行数统计
git ls-files | xargs wc -l     # 统计所有文件行数
```

## 🚨 紧急情况处理

### 常见问题解决
```bash
# 合并冲突
git status                     # 查看冲突文件
# 手动编辑冲突文件
git add <冲突文件>
git commit

# 误删分支恢复
git reflog                     # 查看操作历史
git checkout -b <分支名> <提交ID>

# 找回丢失的提交
git reflog
git cherry-pick <提交ID>

# 清理仓库
git clean -f                   # 删除未跟踪文件
git clean -fd                  # 删除未跟踪文件和目录
git clean -n                   # 预览要删除的文件
```

## 🎯 实用技巧

### 命令组合
```bash
# 查看漂亮的提交历史
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit

# 查看每个人的代码贡献
git log --pretty=format:"%an %s" | sort | uniq -c | sort -rn

# 查看文件的每一行是谁修改的
git blame <文件名>

# 查看两个分支的差异
git diff <分支1>..<分支2>
```

### 配置优化
```bash
# 设置更好的日志格式
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# 设置自动颜色
git config --global color.ui auto

# 设置推送默认行为
git config --global push.default simple
```

## 📚 学习资源

### 帮助命令
```bash
git help <命令>                # 查看命令详细帮助
git <命令> --help              # 同上
man git-<命令>                 # 查看手册页
```

### 在线资源
- [Git官方文档](https://git-scm.com/doc)
- [Pro Git书籍](https://git-scm.com/book)
- [Git可视化学习](https://learngitbranching.js.org/)
- [GitHub Git手册](https://guides.github.com/)

## 💡 记忆技巧

### 常用命令记忆
- `add` → 添加到暂存区
- `commit` → 提交到版本库
- `push` → 推送到远程
- `pull` → 从远程拉取
- `branch` → 分支操作
- `merge` → 合并分支
- `checkout` → 切换分支/恢复文件
- `status` → 查看状态
- `log` → 查看历史

### 工作流程记忆
```
修改文件 → git add → git commit → git push
   ↓         ↓         ↓          ↓
 工作区   → 暂存区  → 版本库   → 远程仓库
```

---

**💡 提示**：将这个速查表保存为书签，在使用Git时随时查阅。随着经验的积累，你会发现自己越来越少需要查阅，这些命令会成为你的肌肉记忆！
