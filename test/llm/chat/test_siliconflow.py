# 参考 https://docs.siliconflow.cn/api-reference/chat-completions/chat-completions

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def call_with_messages():
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.siliconflow.cn/v1"
    )
    
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[{"role": "user", "content": "请说明你是谁"}],
        max_tokens=2048,
        temperature=0.7,
        top_p=0.7,
        frequency_penalty=0.5,
        n=1,
        response_format={"type": "text"},
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    call_with_messages()
