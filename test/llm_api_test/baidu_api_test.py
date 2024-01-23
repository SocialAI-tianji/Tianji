import os
from typing import Optional
from dotenv import load_dotenv
load_dotenv()
from metagpt.logs import logger
from metagpt.provider.base_gpt_api import BaseGPTAPI
import erniebot
import random
from http import HTTPStatus
# 当你看不懂代码的时候看看其它代码然后看看文档。
erniebot.api_type = "aistudio"

def call_with_messages(message):
    # 每次用复制这些
    erniebot.access_token = os.environ["BAIDU_API_KEY"]
    ############
    stream = False
    
    messages =[{'role': 'user', 'content': message}]
    response = erniebot.ChatCompletion.create(
        model="ernie-4.0",
        messages=messages,
        top_p=0.95,  # 改 
        stream=stream
    )
    if stream:
        result = ""
        for resp in response:
            result += resp.get_result()
    else:
        result = response.get_result()

    print(result)


if __name__ == '__main__':
    call_with_messages("你好")