<<<<<<< HEAD
# English-interview-practice
=======
# AI Interview Assistant

一个利用AI帮助用户准备面试的应用程序。

## 功能特点

- 简历上传与分析
- 基于简历和职位描述生成个性化面试问题
- 实时面试练习
- 面试回答分析与反馈

## 技术栈

### 前端
- React
- Material-UI
- React Router

### 后端
- Flask
- Google Gemini API
- PyPDF2, python-docx (文档解析)

## 项目结构

```
.
├── backend/            # Flask后端
│   ├── app.py          # 主应用入口
│   ├── uploads/        # 上传文件存储目录
│   └── test_gemini.py  # Gemini API测试脚本
├── frontend/           # React前端
│   ├── src/            # 源代码
│   │   ├── components/ # React组件
│   │   └── App.js      # 主应用组件
├── .gitignore          # Git忽略文件
└── README.md           # 项目说明文档
```

## 安装与运行

### 后端设置

1. 安装Python依赖：
```bash
cd backend
pip install -r requirements.txt
```

2. 创建`.env`文件并添加Google API密钥：
```
# 拷贝示例文件
cp .env.example .env

# 编辑.env文件，替换为你的API密钥
GOOGLE_API_KEY=your_actual_api_key_here
```

3. 运行后端服务：
```bash
python app.py
```

### 前端设置

1. 安装Node.js依赖：
```bash
cd frontend
npm install
```

2. 运行前端开发服务器：
```bash
npm start
```

## 使用说明

1. 上传简历（支持PDF, DOCX, JSON格式）
2. 提供职位描述
3. 系统分析简历与职位匹配度
4. 开始面试练习
5. 获取面试反馈与建议

## API密钥安全说明

本项目使用Google Gemini API，需要API密钥才能运行。为保护你的API密钥安全：

1. **永远不要**将含有真实API密钥的`.env`文件提交到Git仓库
2. 该文件已在`.gitignore`中被排除
3. 仓库中只包含`.env.example`示例文件，不含真实密钥
4. 在本地开发时，复制`.env.example`为`.env`并添加你的API密钥

```bash
# 检查.env文件是否被正确忽略
git check-ignore -v backend/.env
```

## 许可证

MIT 
>>>>>>> 0cef5a9 (Initial commit: AI Interview Assistant project)
