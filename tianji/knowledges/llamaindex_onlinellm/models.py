from typing import List, Any
import os
import requests
from zhipuai import ZhipuAI
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core.bridge.pydantic import PrivateAttr
from llama_index.core.embeddings import BaseEmbedding
import json

class ZhipuLLM(CustomLLM):
    """智谱AI的自定义聊天模型。"""

    client: Any = None
    context_window: int = 10000
    num_output: int = 8000
    model_name: str = "glm-4-flash"

    def __init__(self):
        super().__init__()
        print("正在初始化模型...")
        self.client = ZhipuAI(api_key=os.environ.get("ZHIPUAI_API_KEY"))
        print("模型初始化完成")

    @property
    def metadata(self) -> LLMMetadata:
        """获取LLM元数据。"""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        """运行LLM并返回完成响应。"""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        return CompletionResponse(text=response.choices[0].message.content)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        """流式运行LLM并返回完成响应生成器。"""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )

        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield CompletionResponse(
                    text=chunk.choices[0].delta.content,
                    delta=chunk.choices[0].delta.content,
                )

    @classmethod
    def class_name(cls) -> str:
        return "zhipu_llm"


class SiliconFlowLLM(CustomLLM):
    """SiliconFlow的自定义聊天模型。"""

    client: Any = None
    context_window: int = 10000
    num_output: int = 8000
    model_name: str = "Qwen/Qwen2.5-7B-Instruct"
    base_url: str = "https://api.siliconflow.cn/v1"
    token: str = None

    def __init__(self):
        super().__init__()
        self.token = os.environ.get("SILICONFLOW_API_KEY")

    @property
    def metadata(self) -> LLMMetadata:
        """获取LLM元数据。"""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        """运行LLM并返回完成响应。"""
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"},
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return CompletionResponse(text=response.json()["choices"][0]["message"]["content"])
        else:
            raise ValueError(f"请求失败, 状态码: {response.status_code}")

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        """流式运行LLM并返回完成响应生成器。"""
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,  
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"},
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers, stream=True)
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    try:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            data_str = line_str.replace('data: ', '')
                            if data_str.strip() == '[DONE]':  # 检查是否为结束标记
                                break
                            if data_str.strip():  # 确保不是空字符串
                                data = json.loads(data_str)
                                if data["choices"][0]["delta"].get("content"):
                                    yield CompletionResponse(
                                        text=data["choices"][0]["delta"]["content"],
                                        delta=data["choices"][0]["delta"]["content"]
                                    )
                    except json.JSONDecodeError:
                        print(f"无效的JSON数据: {line_str}")
                        continue
                    except Exception as e:
                        raise ValueError(f"处理响应时出错: {str(e)}")
        else:
            raise ValueError(f"请求失败, 状态码: {response.status_code}")

    @classmethod
    def class_name(cls) -> str:
        return "siliconflow_llm"

from typing import Any, List
from zhipuai import ZhipuAI

from llama_index.core.bridge.pydantic import PrivateAttr
from llama_index.core.embeddings import BaseEmbedding


class ZhipuEmbeddings(BaseEmbedding):
    """智谱AI的嵌入模型。"""

    _client: ZhipuAI = PrivateAttr()
    _model: str = PrivateAttr()
    embed_dim: int = 2048

    def __init__(
        self,
        model: str = "embedding-3",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._client = ZhipuAI(api_key=os.getenv("ZHIPUAI_API_KEY"))
        self._model = model

    @classmethod
    def class_name(cls) -> str:
        return "zhipu_embedding"

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    def _get_query_embedding(self, query: str) -> List[float]:
        response = self._client.embeddings.create(
            model=self._model,
            input=query,
        )
        return response.data[0].embedding

    def _get_text_embedding(self, text: str) -> List[float]:
        response = self._client.embeddings.create(
            model=self._model,
            input=text,
        )
        return response.data[0].embedding

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """获取文本嵌入。"""
        embeddings_list: List[List[float]] = []
        for text in texts:
            response = self._client.embeddings.create(
                model=self._model,
                input=text,
            )
            embeddings_list.append(response.data[0].embedding)
        return embeddings_list


class SiliconFlowEmbeddings(BaseEmbedding):
    """SiliconFlow的嵌入模型。"""

    _model: str = PrivateAttr()
    embed_dim: int = 1024

    def __init__(
        self,
        model: str = "BAAI/bge-m3",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._model = model

    @classmethod
    def class_name(cls) -> str:
        return "siliconflow_embedding"

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    def _get_query_embedding(self, query: str) -> List[float]:
        return self._get_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        return self._get_embedding(text)

    def _get_embedding(self, text: str) -> List[float]:
        url = "https://api.siliconflow.cn/v1/embeddings"
        payload = {
            "model": self._model,
            "input": text,
            "encoding_format": "float",
        }
        headers = {
            "Authorization": f"Bearer {os.getenv('SILICONFLOW_API_KEY')}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()["data"][0]["embedding"]
        else:
            raise ValueError(f"请求失败, 状态码: {response.status_code}")

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """获取文本嵌入。"""
        embeddings_list: List[List[float]] = []
        for text in texts:
            embeddings_list.append(self._get_embedding(text))
        return embeddings_list