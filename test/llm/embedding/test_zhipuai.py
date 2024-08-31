# 参考文档
# https://open.bigmodel.cn/
# https://open.bigmodel.cn/dev/api#sdk
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

from zhipuai import ZhipuAI


class ZhipuEmbedding:
    """
    class for Zhipu embeddings
    """

    def __init__(self) -> None:
        super().__init__()
        self.client = ZhipuAI(api_key=os.getenv("ZHIPUAI_API_KEY"))

    def get_embedding(
        self,
        text: str,
        model: str = "embedding-3",
    ) -> List[float]:
        response = self.client.embeddings.create(
            model=model,
            input=text,
        )
        return response.data[0].embedding


if __name__ == "__main__":
    Zhipu = ZhipuEmbedding()
    embedding_result = Zhipu.get_embedding("你好")
    print(
        f"Result of Zhipu Embedding: \n"
        f"\t Type of output: {type(embedding_result)}\n"
        f"\t Shape of output: {len(embedding_result)}"
    )
