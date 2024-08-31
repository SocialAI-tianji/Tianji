import os
import json
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from zhipuai import ZhipuAI

_ = load_dotenv(find_dotenv())

client = ZhipuAI(api_key=os.getenv("ZHIPUAI_API_KEY"))

with open("test/gpt_prompt/prompt.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    system_prompt = data["test_system"]
    user_prompt = data["test1"]


def get_completion(prompt, model="glm-4-flash", messages=[]):
    """
    prompt: 对应的提示词
    model: 调用的模型，默认为 glm-4-flash
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages + [{"role": "user", "content": prompt}],
    )
    return response.choices[0].message["content"]


with st.sidebar:
    st.markdown("## 人情世故-天机")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, step=0.01)

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by SociaAI")

if "messages" not in st.session_state:  # 设置system prompt
    st.session_state["messages"] = [{"role": "system", "content": system_prompt}]

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    st.chat_message(msg["role"]).write(msg["content"])

if text := st.chat_input():
    prompt = user_prompt.format(text=text)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(text)
    response = get_completion(
        prompt,
        model="glm-4-flash",
        messages=st.session_state["messages"],
    )
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
