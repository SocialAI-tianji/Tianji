#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/12/27 21:45
@Author  : baldwang
@File    : anthropic_api.py
"""
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



class BdAPI(BaseGPTAPI):

    def __init__(self):
        logger.warning('当前方法无法支持异步运行。当你使用acompletion时，并不能并行访问。')

    def ask(self, msg: str) -> str:
        message = [self._default_system_msg(), self._user_msg(msg)]
        rsp = self.completion(message)
        return rsp

    async def aask(self, msg: str, system_msgs: Optional[list[str]] = None) -> str:
        print("Baidu aask")
        logger.warning('Baidu aask Baidu aask Baidu aask')
        if system_msgs:
            message = self._system_msgs(system_msgs) + [self._user_msg(msg)]
        else:
            message = [self._default_system_msg(), self._user_msg(msg)]
        rsp = await self.acompletion(message)
        logger.debug(message)
        return rsp

    def get_choice_text(self, rsp: dict) -> str:
        return rsp["payload"]["choices"]["text"][-1]["content"]

    async def acompletion_text(self, messages: list[dict], stream=False) -> str:
        # 不支持
        logger.error('该功能禁用。')
        w = call_with_messages(messages)
        print("dict",messages)
        return w

    async def acompletion(self, messages: list[dict]):
        # 不支持异步
        # print("dict",messages[1])
        # print(messages[1]["content"])
        w = call_with_messages(messages)
        return w

    def completion(self, messages: list[dict]):
        w = call_with_messages(messages)
        return w


