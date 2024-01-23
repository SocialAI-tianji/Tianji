import erniebot 
import asyncio
import os
erniebot.api_type = "aistudio"
from dotenv import load_dotenv
load_dotenv()
erniebot.access_token = os.environ["BAIDU_API_KEY"]


class BaiduApi():
    def __init__(self):
        pass
    
    async def _aask(self, prompt, stream=False, model="ernie-4.0", top_p=0.95):
        messages = [{'role': 'user', 'content': prompt}]
        response = erniebot.ChatCompletion.create(
            model=model,
            messages=messages,
            top_p=top_p,
            stream=stream
        )
        return response.result

if __name__ == "__main__":
    models = erniebot.Model.list()
    print("可用模型",models)
    
    baidu_api = BaiduApi()
    result = asyncio.run(baidu_api._aask("你好啊"))
    print("result",result)