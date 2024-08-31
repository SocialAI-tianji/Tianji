# 参考文档
# https://platform.deepseek.com/sign_in
# https://chat.deepseek.com/sign_in
# https://platform.deepseek.com/docs

import os
from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_API_BASE")

# 检查API密钥和基础URL是否为空
if not api_key or not base_url:
    raise ValueError("API Key或Base URL为空，请检查.env文件中的设置。")

print(f"API Key: {api_key}, Base URL: {base_url}")
client = OpenAI(api_key=api_key, base_url=base_url)
print(client.models.list())

# 获取模型列表
for model in client.models.list().data:
    print(model)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个助手"},
        {"role": "user", "content": "你好"},
    ],
)

print(response.choices[0].message.content)
