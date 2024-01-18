import streamlit as st
import uuid

# 初始化session_state变量
if 'user_id' not in st.session_state:
    # 为新用户会话生成一个唯一的UUID
    st.session_state['user_id'] = str(uuid.uuid4())

# 显示用户的UUID（仅供演示）
st.write(f"您的会话ID是: {st.session_state['user_id']}")

# 以下是应用的主要逻辑
# ...
# 你可以根据 st.session_state['user_id'] 来跟踪不同会话的状态
# ...
