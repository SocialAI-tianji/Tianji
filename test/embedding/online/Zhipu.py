from BaseOnline import BaseOnlineEmbeddings
from typing import List
import os
from zhipuai import ZhipuAI
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# os.environ["ZHIPUAI_API_KEY"]=""


class ZhipuEmbedding(BaseOnlineEmbeddings):
    """
    class for Zhipu embeddings
    """

    def __init__(self) -> None:
        super().__init__()
        self.client = ZhipuAI(api_key=os.getenv("ZHIPUAI_API_KEY"))

    def get_embedding(
        self,
        text: str,
        model: str = "embedding-2",
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
