from BaseLocal import BaseLocalEmbeddings
from typing import List
import torch
from transformers import AutoModel, AutoTokenizer
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()


class BgeEmbedding(BaseLocalEmbeddings):
    """
    class for Bge embeddings
    """

    # path:str = TIANJI_PATH / "embedding/BAAI/bge-small-zh"
    def __init__(self, path: str = "BAAI/bge-small-zh") -> None:
        super().__init__(path)
        self._model, self._tokenizer, self._device = self.load_model()

    def get_embedding(self, text: str) -> List[float]:
        encoded_input = self._tokenizer(
            text, padding=True, truncation=False, return_tensors="pt"
        ).to(self._device)
        return self._model(**encoded_input)[0][:, 0][0]

    def load_model(self):
        if torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
        model = AutoModel.from_pretrained(self.path, trust_remote_code=True).to(device)
        tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-large-zh-v1.5")
        return model, tokenizer, device


if __name__ == "__main__":
    Bge = BgeEmbedding()
    embedding_result = Bge.get_embedding("你好")
    print(
        f"Result of Bge Embedding: \n"
        f"\t Type of output: {type(embedding_result)}\n"
        f"\t Shape of output: {len(embedding_result)}"
    )
