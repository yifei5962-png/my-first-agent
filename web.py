import streamlit as st
import requests

# --- 核心配置：这是你实验室电脑的公网接头地址 ---
# 确保后缀和你 n8n Webhook 节点里设置的 Path 一致
N8N_WEBHOOK_URL = "https://521a1ace.r2.cpolar.top/webhook/zdu-paper-query"

st.set_page_config(page_title="郑大土木学术 AI", page_icon="🏗️")
st.title("🏗️ 郑大土木学术 AI 助手")

# 侧边栏：展示你的开发者身份
with st.sidebar:
    st.header("系统说明")
    st.info("本助手已接入 Pinecone 论文数据库，由 n8n 驱动。")
    st.write("开发者：郑大土木研究生")
    st.write("---")
    if st.button("清空对话记忆"):
        st.session_state.messages = []
        st.rerun()

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 渲染对话
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 接收用户输入
user_input = st.chat_input("输入专业问题，我将检索论文库为您解答...")

if user_input:
    # 1. 展示用户消息
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. 向 n8n 发起请求
    with st.chat_message("assistant"):
        with st.spinner("正在检索论文库并深度思考..."):
            # 这里的 "chatInput" 必须和你 n8n 节点里引用的变量名完全对应
            payload = {"chatInput": user_input}
            
            try:
                response = requests.post(N8N_WEBHOOK_URL, json=payload)
                
                if response.status_code == 200:
                    res_data = response.json()
                    # 获取 n8n 返回的 AI 答案
                    # 注意：如果你的 n8n 返回字段不是 output，请修改这里
                    ans = res_data.get("output", "查询成功，但未获得有效回答。")
                    st.write(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                else:
                    st.error(f"n8n 响应异常，错误码：{response.status_code}")
            except Exception as e:
                st.error("连接失败！请确认实验室电脑上的 cpolar 窗口是否保持开启。")
