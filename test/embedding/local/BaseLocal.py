from typing import List


class BaseLocalEmbeddings:
    """
    Base class for local embeddings
    """

    def __init__(self, path: str) -> None:
        self.path = path

    def get_embedding(self, text: str, model: str) -> List[float]:
        raise NotImplementedError
