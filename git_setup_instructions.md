# 在GitHub上创建仓库并推送代码

## 步骤1：在GitHub上创建新仓库

1. 访问 [GitHub](https://github.com) 并登录你的账户
2. 点击右上角的 "+" 图标，然后选择 "New repository"
3. 填写仓库名称，例如："ai-interview-assistant"
4. 添加描述（可选）："AI驱动的面试准备与练习系统"
5. 选择公开或私有（根据需要）
6. **不要**初始化仓库，保持所有选项不勾选
7. 点击 "Create repository"

## 步骤2：将本地仓库连接到GitHub

在终端中执行以下命令（将URL替换为你的GitHub仓库URL）：

```bash
git remote add origin https://github.com/你的用户名/ai-interview-assistant.git
git branch -M main
git push -u origin main
```

如果你使用的是SSH认证方式：

```bash
git remote add origin git@github.com:你的用户名/ai-interview-assistant.git
git branch -M main
git push -u origin main
```

## 密钥设置（如果使用SSH）

如果你还没有设置SSH密钥，可以按照以下步骤：

1. 生成SSH密钥：
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

2. 复制SSH公钥：
```bash
cat ~/.ssh/id_ed25519.pub
```

3. 在GitHub上添加SSH密钥：
   - 访问 GitHub 设置页面的 "SSH and GPG keys" 部分
   - 点击 "New SSH key"
   - 粘贴你的公钥并添加标题
   - 点击 "Add SSH key"

完成上述步骤后，你的代码将被成功推送到GitHub仓库。 