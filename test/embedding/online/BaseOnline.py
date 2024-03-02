from typing import List

class BaseOnlineEmbeddings:
    """
    Base class for online embeddings
    """
    def __init__(self) -> None:
        pass
        
    def get_embedding(self, text: str, model: str) -> List[float]:
        raise NotImplementedError
    
    
