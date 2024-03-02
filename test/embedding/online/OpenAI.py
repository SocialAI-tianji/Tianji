from BaseOnline import BaseOnlineEmbeddings
from typing import List
import os
# os.environ["OPENAI_BASE_URL"]=""
# os.environ["OPENAI_API_KEY"]=""

class OpenAIEmbedding(BaseOnlineEmbeddings):
    """
    class for OpenAI embeddings
    """
    def __init__(self) -> None:
        super().__init__()
        from openai import OpenAI
        self.client = OpenAI()
        self.client.base_url = os.getenv("OPENAI_BASE_URL")
        self.client.api_key = os.getenv("OPENAI_API_KEY")
    
    def get_embedding(self, text: str, model: str = "text-embedding-3-small") -> List[float]:
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model=model).data[0].embedding

if __name__ == "__main__":
    OpenAI = OpenAIEmbedding()
    embedding_result = OpenAI.get_embedding("你好")
    print(f"Result of OpenAI Embedding: \n"
      f"\t Type of output: {type(embedding_result)}\n"
      f"\t Shape of output: {len(embedding_result)}")