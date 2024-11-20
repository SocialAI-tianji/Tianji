from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ["SHUSHENG_API_KEY"],
    base_url=os.environ[
        "SHUSHENG_BASE_URL"
    ],  # "https://internlm-chat.intern-ai.org.cn/puyu/api/v1/"
)

response = client.chat.completions.create(
    model="internlm2.5-latest",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "你是谁"},
    ],
)
print(response.choices[0].message)
