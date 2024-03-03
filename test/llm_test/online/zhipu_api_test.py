# 参考文档
# https://open.bigmodel.cn/
# https://open.bigmodel.cn/dev/api#sdk

from dotenv import load_dotenv

load_dotenv()

from zhipuai import ZhipuAI

client = ZhipuAI()  # 也可在此显式指定 api_key

# embedding
response = client.embeddings.create(
    model="embedding-2",  # 填写需要调用的模型名称
    input="你好",
)

# chat
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "我是人工智能助手"},
        {"role": "user", "content": "你叫什么名字"},
        {"role": "assistant", "content": "我叫chatGLM"},
        {"role": "user", "content": "你都可以做些什么事"},
    ],
)
print(response.choices[0].message)
