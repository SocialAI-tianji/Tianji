from BaseLocal import BaseLocalEmbeddings
from typing import List
import os
#os.environ["HF_TOKEN"]=""

class JinaEmbedding(BaseLocalEmbeddings):
    """
    class for Jina embeddings
    """
    #path:str = TIANJI_PATH / "embedding/jinaai/jina-embeddings-v2-base-zh"
    def __init__(self, path:str='jinaai/jina-embeddings-v2-base-zh') -> None:
        super().__init__(path)
        self._model = self.load_model()
        
    def get_embedding(self, text: str)-> List[float]:
        return self._model.encode([text])[0]
    
    def load_model(self):
        import torch
        from transformers import AutoModel
        if torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
        model = AutoModel.from_pretrained(self.path, trust_remote_code=True).to(device)
        return model

if __name__ == "__main__":
    Jina = JinaEmbedding()
    embedding_result = Jina.get_embedding("你好")
    print(f"Result of Jina Embedding: \n"
      f"\t Type of output: {type(embedding_result)}\n"
      f"\t Shape of output: {len(embedding_result)}")
