# 参考 https://docs.siliconflow.cn/api-reference/chat-completions/chat-completions

import requests
import os
from dotenv import load_dotenv

load_dotenv()


def call_with_messages():
    url = "https://api.siliconflow.cn/v1/chat/completions"
    payload = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [{"role": "user", "content": "请说明你是谁"}],
        "stream": False,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"},
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('SILICONFLOW_API_KEY')}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(response.json()["choices"][0]["message"]["content"])
    else:
        print(f"请求失败, 状态码: {response.status_code}")


if __name__ == "__main__":
    call_with_messages()
