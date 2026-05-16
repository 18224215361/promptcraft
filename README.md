# PromptCraft - AI 提示词工坊

输入你的需求，AI 帮你生成高质量的优化提示词。

## 功能

- **6 种优化风格**：营销文案、社交媒体、学术写作、图片生成、代码辅助、通用优化
- **提示词优化**：根据需求和风格，生成结构清晰、可直接使用的 AI 提示词
- **示例输出**：根据优化后的提示词，生成示例内容

## 技术栈

- **后端**：Flask + Anthropic Claude API
- **前端**：原生 HTML/CSS/JavaScript
- **部署**：Render

## 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# 3. 启动
python app.py
```

访问 http://localhost:5000

## 部署

项目已配置为支持 Render 一键部署。在 Render 中创建 Web Service 并连接 GitHub 仓库，设置 `ANTHROPIC_API_KEY` 环境变量即可。
