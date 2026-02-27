import streamlit as st
import requests
import json

st.title("我的 AI 助手 ")

# 1. 准备秘钥
import os  # 新增这一行，用来读取系统环境

# 把你原来的 10-15 行替换成下面这段
if "API_KEY" in st.secrets:
    API_KEY = st.secrets["API_KEY"]
elif os.getenv("API_KEY"): # 兼容另一种常见的云端写法
    API_KEY = os.getenv("API_KEY")
else:
    API_KEY = "sk-xxxxxxxxxxxx" # 实在不行，这里先填入你真实的Key测试一下
    st.warning("提醒：正在使用本地硬编码Key运行")
URL = "https://api.deepseek.com/chat/completions"

# 2. 建立大脑记忆区 (专属储物柜)
# 如果柜子是空的，我们就放进去一张“系统人设卡片”
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一个资深的工程与AI跨界导师。擅长解答力学与数字孪生问题。"}
    ]

# 3. 把历史记忆展示在网页上 (UI 升级为真正的聊天气泡)
for msg in st.session_state.messages:
    if msg["role"] != "system": # 系统底层的设定不用展示给用户看
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# 4. 接收你的新问题 (换成了更帅的悬浮聊天输入框)
user_input = st.chat_input("继续向我提问吧...")

if user_input:
    # 先把你的问题显示在屏幕上
    with st.chat_message("user"):
        st.write(user_input)
    
    # 极度关键：把你的问题锁进“记忆储物柜”
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 带着整个储物柜里所有的历史记忆，去请求 DeepSeek
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "deepseek-chat",
        "messages": st.session_state.messages # 这里直接把整个记忆列表端过去！
    }
    
    # 展示 AI 的思考过程和回答
    with st.chat_message("assistant"):
        with st.spinner("AI 大脑高速运转中..."):
            response = requests.post(URL, headers=headers, data=json.dumps(data))
            
            if response.status_code == 200:
                result = response.json()
                ai_reply = result["choices"][0]["message"]["content"]
                st.write(ai_reply)
                
                # 同样关键：把 AI 刚说的话，也记在小本本上存进柜子
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            else:
                st.error("网络开小差了，错误代码：" + str(response.status_code))

