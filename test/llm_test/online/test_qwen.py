# 参考文档
# https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-qianwen-7b-14b-72b-api-detailes

from dotenv import load_dotenv

load_dotenv()

import random
from http import HTTPStatus
import dashscope


def call_with_messages():
    messages = [{"role": "user", "content": "用萝卜、土豆、茄子做饭，给我个菜谱"}]
    response = dashscope.Generation.call(
        model="qwen-72b-chat",
        messages=messages,
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        result_format="message",  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print(
            "Request id: %s, Status code: %s, error code: %s, error message: %s"
            % (
                response.request_id,
                response.status_code,
                response.code,
                response.message,
            )
        )


if __name__ == "__main__":
    call_with_messages()
