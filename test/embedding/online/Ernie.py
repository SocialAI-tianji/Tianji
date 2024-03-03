from BaseOnline import BaseOnlineEmbeddings
from typing import List
import os
import erniebot
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# os.environ["BAIDU_API_KEY"]=""


class ErnieEmbedding(BaseOnlineEmbeddings):
    """
    class for Ernie embeddings
    """

    def __init__(self) -> None:
        super().__init__()
        erniebot.api_type = "aistudio"
        erniebot.access_token = os.getenv("BAIDU_API_KEY")
        self.client = erniebot.Embedding()

    def get_embedding(
        self, text: str, model: str = "ernie-text-embedding"
    ) -> List[float]:
        response = self.client.create(model=model, input=[text])
        return response.get_result()[0]


if __name__ == "__main__":
    Ernie = ErnieEmbedding()
    embedding_result = Ernie.get_embedding("你好")
    print(
        f"Result of Ernie Embedding: \n"
        f"\t Type of output: {type(embedding_result)}\n"
        f"\t Shape of output: {len(embedding_result)}"
    )
