# 📖 校园百事通 - RAG 智能问答助手

## 项目简介
基于 RAG（检索增强生成）技术的校园智能问答系统，可回答校园生活相关问题，支持多轮对话记忆。

## 功能特点
- 🔍 智能检索校园知识库
- 💬 多轮对话记忆
- 📊 工具调用（查询校历、计算绩点）
- 🌐 Web 界面（Streamlit）

## 技术栈
- Python 3.11
- LangChain
- DeepSeek API
- Chroma 向量数据库
- Streamlit

## 快速开始
```bash
pip install -r requirements.txt
streamlit run src/app.py