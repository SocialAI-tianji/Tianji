# 参考 https://ai.baidu.com/ai-doc/AISTUDIO/rm344erns 兼容 OpenAI 接口
from typing import List
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ErnieEmbedding:
    """
    class for Ernie embeddings
    """

    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI()
        self.client.base_url = os.getenv("OPENAI_API_BASE")
        self.client.api_key = os.getenv("OPENAI_API_KEY")

    def get_embedding(self, text: str, model: str = "embedding-v1") -> List[float]:
        text = text.replace("\n", " ")
        return (
            self.client.embeddings.create(input=[text], model=model).data[0].embedding
        )


if __name__ == "__main__":
    Ernie = ErnieEmbedding()
    embedding_result = Ernie.get_embedding("你好")
    print(
        f"Result of Ernie Embedding: \n"
        f"\t Type of output: {type(embedding_result)}\n"
        f"\t Shape of output: {len(embedding_result)}"
    )
