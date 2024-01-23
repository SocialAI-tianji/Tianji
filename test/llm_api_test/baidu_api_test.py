import os
from dotenv import load_dotenv
import erniebot

load_dotenv()

# 当你看不懂代码的时候看看其它代码然后看看文档。
erniebot.api_type = "aistudio"


def call_with_messages(message):
    # 每次用复制这些
    erniebot.access_token = os.environ["BAIDU_API_KEY"]
    ############
    stream = False

    messages = [{"role": "user", "content": message}]
    response = erniebot.ChatCompletion.create(
        model="ernie-4.0", messages=messages, top_p=0.95, stream=stream  # 改
    )
    if stream:
        result = ""
        for resp in response:
            result += resp.get_result()
    else:
        result = response.get_result()

    print(result)


if __name__ == "__main__":
    call_with_messages("你好")
