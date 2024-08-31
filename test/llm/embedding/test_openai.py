from typing import List
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# os.environ["OPENAI_API_BASE"]=""
# os.environ["OPENAI_API_KEY"]=""


class OpenAIEmbedding:
    """
    class for OpenAI embeddings
    """

    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI()
        self.client.base_url = os.getenv("OPENAI_API_BASE")
        self.client.api_key = os.getenv("OPENAI_API_KEY")

    def get_embedding(
        self, text: str, model: str = "text-embedding-3-small"
    ) -> List[float]:
        text = text.replace("\n", " ")
        return (
            self.client.embeddings.create(input=[text], model=model).data[0].embedding
        )


if __name__ == "__main__":
    OpenAI = OpenAIEmbedding()
    embedding_result = OpenAI.get_embedding("你好")
    print(
        f"Result of OpenAI Embedding: \n"
        f"\t Type of output: {type(embedding_result)}\n"
        f"\t Shape of output: {len(embedding_result)}"
    )
