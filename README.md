# AI Tools Plugin for Claude Code

AI 开发工具集 - Prompt Engineering、RAG 系统、Agent 开发

## 状态

✅ **当前版本：v0.2.0**

AI 开发工具集，包含网页处理、Prompt Engineering、RAG 系统等实用 skills。

## 规划功能

### 📄 网页处理
- **webpage-to-markdown**: 网页内容提取并转换为 Markdown
  - 支持 JavaScript 渲染的页面
  - 保留格式、图片、链接
  - 基于 Playwright 浏览器自动化

### 🎨 Prompt Engineering
- Prompt 模板库
- Prompt 优化建议
- Chain-of-Thought 提示词生成
- Few-shot Learning 示例构建

### 🔍 RAG 系统
- 文档切分策略分析
- Embedding 模型选择建议
- 向量数据库配置优化
- 检索策略设计

### 🤖 Agent 开发
- Multi-Agent 架构设计
- Tool/Function Calling 最佳实践
- Agent 记忆系统设计
- Agent 评估框架

### 💡 LLM 应用开发
- LLM API 调用优化
- 成本控制策略
- 输出质量评估
- 错误处理模式

## Skills 列表

### webpage-to-markdown

提取网页内容并转换为 Markdown 格式，支持 JavaScript 渲染的复杂页面。

**安装依赖**：
```bash
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

**使用示例**：
```bash
# 基本用法
python3 skills/webpage-to-markdown/scripts/fetch_as_markdown.py https://example.com

# 保存到文件
python3 skills/webpage-to-markdown/scripts/fetch_as_markdown.py \
  https://example.com -o output.md

# 详细输出
python3 skills/webpage-to-markdown/scripts/fetch_as_markdown.py \
  https://example.com -o output.md --verbose
```

**功能特性**：
- ✅ 处理 JavaScript 渲染的页面
- ✅ 保留文章结构（标题、列表、表格）
- ✅ 保留图片和链接
- ✅ 支持中文内容
- ✅ 自定义超时和等待策略

## 安装

### 通过 Marketplace

```bash
# 添加 marketplace
/plugin marketplace add stevelin001/gl-claude-marketplace

# 安装 plugin
/plugin install ai-tools
```

### 直接安装

```bash
/plugin install stevelin001/gl-ai-tools-plugin
```

## 贡献

如果你有好的 AI 开发工具想法，欢迎提交 Issue 或 PR！

## 版本历史

### v0.2.0 (2026-01-03)
- ✨ 新增 webpage-to-markdown skill
  - 网页内容提取并转换为 Markdown
  - 支持 JavaScript 渲染页面
  - 基于 Playwright + markdownify
- 📁 创建 skills/ 目录结构
- 📝 更新文档和使用说明

### v0.1.0 (2025-11-06)
- 🎯 初始占位版本
- 📋 规划功能列表

## 许可证

MIT License

## 作者

林形省 (stevelin001)
- Email: xingshenglin@gmail.com
- GitHub: https://github.com/stevelin001
