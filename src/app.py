import streamlit as st
from agent import chat_with_memory
import sys
import os

# 添加当前目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 页面配置
st.set_page_config(
    page_title="校园百事通",
    page_icon="📖",
    layout="wide"
)

# 标题
st.title("📖 校园百事通助手")
st.markdown("---")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 输入框
if prompt := st.chat_input("问点校园问题..."):
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 调用智能体
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = chat_with_memory(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})