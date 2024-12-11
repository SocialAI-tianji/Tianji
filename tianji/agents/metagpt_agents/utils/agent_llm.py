from zhipuai import ZhipuAI
from openai import OpenAI
import os
import asyncio

class ZhipuApi:
    """
    此处演示如何注册一个自定义llm
    """
    def __init__(self, client=None):
        self.client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])

    async def _aask(
        self, prompt, stream=False, model="glm-4-flash", top_p=0.7, temperature=0.95
    ):
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            top_p=top_p,
            temperature=temperature,
            stream=stream,
        )
        return response.choices[0].message.content


class OpenaiApi:
    def __init__(self, client=None):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"],base_url=os.environ["OPENAI_API_BASE"])

    async def _aask(
        self, prompt, stream=False, model=os.environ["OPENAI_API_MODEL"], top_p=0.7, temperature=0.95
    ):
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=4096,
            top_p=top_p,
            temperature=temperature,
            stream=stream,
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    zhipu_api = ZhipuApi()
    openai_api = OpenaiApi()
    zhipu_result = asyncio.run(zhipu_api._aask("你是谁"))
    openai_result = asyncio.run(openai_api._aask("你是谁"))
    print("Zhipu result", zhipu_result)
    print("OpenAI result", openai_result)
