# 参考文档
# https://platform.deepseek.com/sign_in
# https://chat.deepseek.com/sign_in
# https://platform.deepseek.com/docs

from openai import OpenAI

client = OpenAI(api_key="<deepseek api key>", base_url="https://api.deepseek.com/v1")

# 获取模型列表
for model in client.models.list().data:
    print(model)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个助手"},
        {"role": "user", "content": "你好"},
    ]
)

print(response.choices[0].message.content)
