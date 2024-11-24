from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain.embeddings.base import Embeddings
from typing import Any, Dict, List, Optional
import os
import requests
from zhipuai import ZhipuAI
from langchain.pydantic_v1 import BaseModel, root_validator
import loguru

class ZhipuLLM(LLM):
    """A custom chat model for ZhipuAI."""

    client: Any = None

    def __init__(self):
        super().__init__()
        print("Initializing model...")
        self.client = ZhipuAI(api_key=os.environ.get("ZHIPUAI_API_KEY"))
        print("Model initialization complete")

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Run the LLM on the given input."""

        response = self.client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {"model_name": "ZhipuAI"}

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model."""
        return "ZhipuAI"


class SiliconFlowLLM(LLM):
    """A custom chat model for SiliconFlow."""

    model_name: str = "Qwen/Qwen2.5-7B-Instruct"
    base_url: str = "https://api.siliconflow.cn/v1"
    token: Optional[str] = None

    def __init__(self):
        super().__init__()
        print("Initializing model...")
        self.token = os.getenv("SILICONFLOW_API_KEY")
        if not self.token:
            raise ValueError("SILICONFLOW_API_KEY not found in environment variables")
        print("Model initialization complete")

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Run the LLM on the given input."""
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model_name,
            "messages": [{"role": "system", "content": "你是 SocialAI 组织开发的人情世故大师，叫做天机，你将解答用户有关人情世故的问题。"},{"role": "user", "content": prompt}],
            "stream": False,
            "max_tokens": 4096,
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
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise ValueError(f"请求失败, 状态码: {response.status_code}")

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {"model_name": self.model_name}

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model."""
        return "SiliconFlow"

# 以下为embedding模型

class ZhipuAIEmbeddings(BaseModel, Embeddings):
    """`Zhipuai Embeddings` embedding models."""

    zhipuai_api_key: Optional[str] = None

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        values["zhupuai_api_key"] = values.get("zhupuai_api_key") or os.getenv(
            "ZHIPUAI_API_KEY"
        )
        try:
            import zhipuai

            zhipuai.api_key = values["zhupuai_api_key"]
            values["client"] = zhipuai.ZhipuAI()
        except ImportError:
            raise ValueError(
                "Zhipuai package not found, please install it with `pip install zhipuai`"
            )
        return values
    def _embed(self, texts: str) -> List[float]:
        try:
            resp = self.client.embeddings.create(
                model="embedding-3",
                input=texts,
            )
        except Exception as e:
            loguru.logger.error(f"Error raised by inference endpoint: {e}")
            raise ValueError(f"Error raised by inference endpoint: {e}")
        embeddings = resp.data[0].embedding
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        try:
            resp = self.embed_documents([text])
            return resp[0]
        except Exception as e:
            loguru.logger.error(f"Error raised by inference endpoint: {e}")
            raise ValueError(f"Error raised by inference endpoint: {e}")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        try:
            return [self._embed(text) for text in texts]
        except Exception as e:
            loguru.logger.error(f"Error raised by inference endpoint: {e}")
            raise ValueError(f"Error raised by inference endpoint: {e}")


class SiliconFlowEmbeddings(BaseModel, Embeddings):
    """`SiliconFlow Embeddings` embedding models."""

    siliconflow_api_key: Optional[str] = None
    model_name: str = "BAAI/bge-m3"

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        values["siliconflow_api_key"] = values.get("siliconflow_api_key") or os.getenv(
            "SILICONFLOW_API_KEY"
        )
        if not values["siliconflow_api_key"]:
            raise ValueError("SiliconFlow API key not found")
        return values

    def _embed(self, texts: str) -> List[float]:
        url = "https://api.siliconflow.cn/v1/embeddings"
        payload = {
            "model": self.model_name,
            "input": texts,
            "encoding_format": "float",
        }
        headers = {
            "Authorization": f"Bearer {self.siliconflow_api_key}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()["data"][0]["embedding"]
            else:
                raise ValueError(f"请求失败, 状态码: {response.status_code}")
        except Exception as e:
            raise ValueError(f"Error raised by inference endpoint: {e}")

    def embed_query(self, text: str) -> List[float]:
        resp = self.embed_documents([text])
        return resp[0]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(text) for text in texts]
