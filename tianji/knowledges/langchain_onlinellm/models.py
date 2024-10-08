from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain.embeddings.base import Embeddings
from typing import Any, Dict, List, Optional
import os
from zhipuai import ZhipuAI
from langchain.pydantic_v1 import BaseModel, root_validator


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
            raise ValueError(f"Error raised by inference endpoint: {e}")
        embeddings = resp.data[0].embedding
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        resp = self.embed_documents([text])
        return resp[0]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(text) for text in texts]
