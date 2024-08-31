from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")  # 请在此处填写您的API密钥

# embedding
response = client.embeddings.create(
    model="text-embedding-ada-002",  # 填写需要调用的模型名称
    input="你好",
)

# chat
response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "我是人工智能助手"},
        {"role": "user", "content": "你叫什么名字"},
        {"role": "assistant", "content": "我叫OpenAI助手"},
        {"role": "user", "content": "你都可以做些什么事"},
    ],
)
print(response.choices[0].message)
