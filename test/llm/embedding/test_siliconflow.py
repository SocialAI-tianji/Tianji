import os
import requests
from dotenv import load_dotenv

load_dotenv()


class SiliconFlowAPI:
    def __init__(self):
        self.base_url = "https://api.siliconflow.cn/v1"
        self.token = os.getenv("OPENAI_API_KEY")

    def get_embedding(self, model, input_text, encoding_format="float"):
        from openai import OpenAI
        client = OpenAI(
            api_key=self.token,
            base_url=self.base_url
        )
        response = client.embeddings.create(
            model=model,
            input=input_text,
            encoding_format=encoding_format
        )
        return response.data[0].embedding

    def rerank(
        self,
        model,
        query,
        documents,
        top_n=4,
        return_documents=True,
        max_chunks_per_doc=123,
        overlap_tokens=79,
    ):
        url = f"{self.base_url}/rerank"
        payload = {
            "model": model,
            "query": query,
            "documents": documents,
            "top_n": top_n,
            "return_documents": return_documents,
            "max_chunks_per_doc": max_chunks_per_doc,
            "overlap_tokens": overlap_tokens,
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers)
        return response


if __name__ == "__main__":
    api = SiliconFlowAPI()
    embedding_result = api.get_embedding("BAAI/bge-m3", "试试看效果")
    print(
        f"Result of SiliconFlow Embedding: \n"
        f"\t Type of output: {type(embedding_result)}\n"
        f"\t Shape of output: {len(embedding_result)}"
    )

    rerank_result = api.rerank(
        "BAAI/bge-reranker-v2-m3", "Apple", ["苹果", "香蕉", "水果", "蔬菜"]
    )
    import json

    rerank_result_json = json.loads(rerank_result.text)
    for result in rerank_result_json["results"]:
        print(
            f"文本: {result['document']['text']}, 相关性分数: {result['relevance_score']}, 索引: {result['index']}"
        )
