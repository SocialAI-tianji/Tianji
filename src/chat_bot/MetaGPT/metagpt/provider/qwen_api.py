#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/12/27 21:45
@Author  : baldwang
@File    : anthropic_api.py
"""

from typing import Optional
from metagpt.logs import logger
from metagpt.provider.base_gpt_api import BaseGPTAPI


from metagpt.config import CONFIG
import random
from http import HTTPStatus
import dashscope


def call_with_messages(message):
    messages = [
        {'role': 'user', 'content': message}]
    response = dashscope.Generation.call(
        'qwen-72b-chat',
        messages=messages,
        api_key = CONFIG.spark_api_key,
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        return (response.output.choices[0].message.content)
    else:
        return  ('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    call_with_messages()



class QwenAPI(BaseGPTAPI):

    def __init__(self):
        logger.warning('当前方法无法支持异步运行。当你使用acompletion时，并不能并行访问。')

    def ask(self, msg: str) -> str:
        message = [self._default_system_msg(), self._user_msg(msg)]
        rsp = self.completion(message)
        return rsp

    async def aask(self, msg: str, system_msgs: Optional[list[str]] = None) -> str:
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
        w = call_with_messages(messages[1]["content"])
        return w

    def completion(self, messages: list[dict]):
        w = call_with_messages(messages)
        return w


def call_with_messages(message):
    messages = [
        {'role': 'user', 'content': message}]
    response = dashscope.Generation.call(
        'qwen-72b-chat',
        messages=messages,
        api_key = "sk-dade718043f54560a3465edfa13a47c6",
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        return (response.output.choices[0].message.content)
    else:
        return  ('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))