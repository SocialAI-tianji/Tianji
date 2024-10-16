from zhipuai import ZhipuAI
import os
import asyncio


# singleton 模式的 llm 实体
class ZhipuApi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ZhipuApi, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, client=None):
        if self.__initialized:
            return
        self.__initialized = True
        self.client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])

    async def _aask(
        self, prompt, stream=False, model="glm-4-0520", top_p=0.7, temperature=0.95
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


if __name__ == "__main__":
    llm_api = ZhipuApi()
    result = asyncio.run(llm_api._aask("你好啊"))
    print("result", result)
