from dotenv import load_dotenv

load_dotenv()

import asyncio
import os
import erniebot
from zhipuai import ZhipuAI
from metagpt.logs import logger
from openai import OpenAI

class BaiduApi:
    def __init__(self):
        pass

    async def _aask(self, prompt, stream=False, model="ernie-4.0", top_p=0.95, temperature=1.0):
        messages = [{"role": "user", "content": prompt}]
        response = erniebot.ChatCompletion.create(
            model=model, messages=messages, top_p=top_p, temperature=temperature, stream=stream
        )
        return response.result


class ZhipuApi:
    def __init__(self, glm=None):
        if glm is None:
            raise RuntimeError("ZhipuApi is Error!")
        self.glm = glm

    async def _aask(self, prompt, stream=False, model="glm-3-turbo", top_p=0.95, temperature=1.0):
        messages = [{"role": "user", "content": prompt}]
        response = self.glm.chat.completions.create(
            model=model, messages=messages, top_p=top_p, temperature=temperature, stream=stream
        )
        return response.choices[0].message.content
    
class DeepSeekApi:
    def __init__(self, ds=None):
        if ds is None:
            raise RuntimeError("DeepSeekApi is Error!")
        self.ds = ds

    async def _aask(self, prompt, stream=False, model="deepseek-chat", top_p=0.95, temperature=1.0):
        messages = [{"role": "user", "content": prompt, "temperature": temperature}]
        response = self.ds.chat.completions.create(
            model=model, messages=messages, stream=stream
        )
        return response.choices[0].message.content


class LLMApi:
    def __init__(self):
        self.llm_api = None
        # select api
        if os.environ["DEEPSEEK_API_KEY"] is not None:
            ds = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
            self.llm_api = DeepSeekApi(ds=ds)
        elif os.environ["ZHIPUAI_API_KEY"] is not None:
            glm = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])
            self.llm_api = ZhipuApi(glm=glm)
        elif os.environ["BAIDU_API_KEY"] is not None:
            erniebot.api_type = "aistudio"
            erniebot.access_token = os.environ["BAIDU_API_KEY"]
            self.llm_api = BaiduApi()
        else:
            raise RuntimeError("No api_key found!")

    # 这里的 model 的 default value 逻辑不对，应该是根据 api_type 来决定，不一定必须是 zhipuai
    async def _aask(self, prompt, stream=False, top_p=0.95, temperature=1.0):
        logger.info(f"call llm_api, response is below")
        rsp = await self.llm_api._aask(prompt, stream=stream, top_p=top_p, temperature=temperature)
        return rsp


if __name__ == "__main__":
    # models = erniebot.Model.list()
    # print("可用模型",models)

    llm_api = LLMApi()
    # result = asyncio.run(baidu_api._aask("你好啊"))
    result = asyncio.run(llm_api._aask("你好啊"))
    print("result", result)
