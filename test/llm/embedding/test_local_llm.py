from typing import List
import torch
from transformers import AutoModel, AutoTokenizer
from dotenv import load_dotenv

load_dotenv()


class EmbeddingLocalModel:
    """
    class for different embeddings
    """

    def __init__(self, model_type: str, path: str) -> None:
        super().__init__()
        self.path = path
        self._model, self._tokenizer, self._device = self.load_model(model_type)

    def get_embedding(self, text: str) -> List[float]:
        if hasattr(self, "_tokenizer"):
            encoded_input = self._tokenizer(
                text, padding=True, truncation=False, return_tensors="pt"
            ).to(self._device)
            return self._model(**encoded_input)[0][:, 0][0]
        else:
            return self._model.encode([text])[0]

    def load_model(self, model_type: str):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = AutoModel.from_pretrained(self.path, trust_remote_code=True).to(device)
        tokenizer = (
            AutoTokenizer.from_pretrained("BAAI/bge-large-zh-v1.5")
            if model_type == "Bge"
            else None
        )
        return model, tokenizer, device


if __name__ == "__main__":
    jina_embedding = EmbeddingLocalModel("Jina", "jinaai/jina-embeddings-v2-base-zh")
    embedding_result = jina_embedding.get_embedding("你好")
    print(
        f"Result of Jina Embedding: \n"
        f"\t Type of output: {type(embedding_result)}\n"
        f"\t Shape of output: {len(embedding_result)}"
    )

    bge_embedding = EmbeddingLocalModel("Bge", "BAAI/bge-small-zh")
    embedding_result = bge_embedding.get_embedding("你好")
    print(
        f"Result of Bge Embedding: \n"
        f"\t Type of output: {type(embedding_result)}\n"
        f"\t Shape of output: {len(embedding_result)}"
    )
