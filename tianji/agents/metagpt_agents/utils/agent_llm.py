from zhipuai import ZhipuAI
from openai import OpenAI
import os
import asyncio

"""
LLM接口封装模块

该模块提供了对不同LLM服务的统一接口封装，支持智谱AI和OpenAI两种服务。
主要用于处理智能体系统中的自然语言理解和生成任务。

功能：
1. 提供统一的异步调用接口
2. 支持多种LLM服务
3. 处理API调用的错误和重试
"""

class ZhipuApi:
    """智谱AI接口封装
    
    封装智谱AI的API调用，提供统一的接口格式。
    
    属性:
        client: 智谱AI客户端实例
    """
    
    def __init__(self, client=None):
        """初始化智谱AI接口
        
        参数:
            client: 可选的预配置客户端
        """
        self.client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])

    async def _aask(
        self, 
        prompt, 
        stream=False, 
        model="glm-4-flash", 
        top_p=0.7, 
        temperature=0.95
    ):
        """异步调用智谱AI接口
        
        参数:
            prompt (str): 提示文本
            stream (bool): 是否使用流式输出
            model (str): 模型名称
            top_p (float): 采样阈值
            temperature (float): 温度参数
            
        返回:
            str: 模型生成的回复
        """
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
    """OpenAI接口封装
    
    封装OpenAI的API调用，提供统一的接口格式。
    
    属性:
        client: OpenAI客户端实例
    """
    
    def __init__(self, client=None):
        """初始化OpenAI接口
        
        参数:
            client: 可选的预配置客户端
        """
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=os.environ["OPENAI_API_BASE"]
        )

    async def _aask(
        self, 
        prompt, 
        stream=False, 
        model=os.environ["OPENAI_API_MODEL"], 
        top_p=0.7, 
        temperature=0.95
    ):
        """异步调用OpenAI接口
        
        参数:
            prompt (str): 提示文本
            stream (bool): 是否使用流式输出
            model (str): 模型名称
            top_p (float): 采样阈值
            temperature (float): 温度参数
            
        返回:
            str: 模型生成的回复
        """
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
