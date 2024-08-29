# 参考 https://github.com/PaddlePaddle/ERNIE-SDK/blob/develop/erniebot/README.md
import os
from dotenv import load_dotenv
import erniebot

load_dotenv()

# 列出支持的模型
models = erniebot.Model.list()
print(models)

# 设置鉴权参数
erniebot.api_type = "aistudio"
erniebot.access_token = os.environ["BAIDU_API_KEY"]


def call_with_messages(message):
    stream = False

    messages = [{"role": "user", "content": message}]
    response = erniebot.ChatCompletion.create(
        model="ernie-4.0-turbo-8k ", messages=messages, top_p=0.95, stream=stream
    )
    if stream:
        result = ""
        for resp in response:
            result += resp.get_result()
    else:
        result = response.get_result()

    print(result)


if __name__ == "__main__":
    call_with_messages("你好，请介绍下你自己")
