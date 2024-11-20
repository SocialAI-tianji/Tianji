# 参考 https://ai.baidu.com/ai-doc/AISTUDIO/rm344erns 兼容 OpenAI 接口
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv(
    "OPENAI_API_BASE"
)  # 或指定 OPENAI_API_BASE=https://aistudio.baidu.com/llm/lmapi/v3
base_url = "https://aistudio.baidu.com/llm/lmapi/v3"
client = OpenAI(api_key=api_key, base_url=base_url)
for model in client.models.list().data:
    print(model)

"""
Model(id='bge-large-zh', created=None, object='model', owned_by=None)
Model(id='embedding-v1', created=None, object='model', owned_by=None)
Model(id='ernie-3.5-8k', created=None, object='model', owned_by=None)
Model(id='ernie-4.0-8k', created=None, object='model', owned_by=None)
Model(id='ernie-4.0-turbo-8k', created=None, object='model', owned_by=None)
Model(id='ernie-char-8k', created=None, object='model', owned_by=None)
Model(id='ernie-lite-8k', created=None, object='model', owned_by=None)
Model(id='ernie-speed-128k', created=None, object='model', owned_by=None)
Model(id='ernie-speed-8k', created=None, object='model', owned_by=None)
Model(id='ernie-tiny-8k', created=None, object='model', owned_by=None)
Model(id='Stable-Diffusion-XL', created=None, object='model', owned_by=None)
"""


def call_with_messages(message):
    response = client.chat.completions.create(
        model="ernie-3.5-8k",
        messages=[
            {"role": "user", "content": message},
        ],
        max_tokens=150,
        temperature=0.7,
    )
    print(response.choices[0].message)  # 打印生成的文本


if __name__ == "__main__":
    call_with_messages("你好，请介绍下你自己")
