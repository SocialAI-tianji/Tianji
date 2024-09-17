from typing import List, Union
import torch
from transformers import AutoModel, AutoTokenizer
import torch.nn.functional as F
from tianji import TIANJI_PATH
import os


class EmbeddingLocalModel:
    """
    用于不同嵌入模型的类
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self._model, self._tokenizer, self._device = self.load_model()

    def get_embedding(self, text: Union[str, List[str]]) -> torch.Tensor:
        if isinstance(text, str):
            text = [text]

        encoded_input = self._tokenizer(
            text, padding=True, truncation=True, return_tensors="pt"
        ).to(self._device)

        with torch.no_grad():
            model_output = self._model(**encoded_input)
            sentence_embeddings = model_output[0][:, 0]

        # 归一化嵌入
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

        return sentence_embeddings

    def load_model(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        cache_dir = os.path.join(TIANJI_PATH, "temp")
        model = AutoModel.from_pretrained(
            pretrained_model_name_or_path=self.name, cache_dir=cache_dir
        ).to(device)
        tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=self.name, cache_dir=cache_dir
        )
        model.eval()
        return model, tokenizer, device


if __name__ == "__main__":
    # 测试 Jina 嵌入
    jina_embedding = EmbeddingLocalModel("jinaai/jina-embeddings-v2-base-zh")
    embedding_result = jina_embedding.get_embedding("你好")
    print(
        f"Jina 嵌入结果: \n"
        f"\t 输出类型: {type(embedding_result)}\n"
        f"\t 输出形状: {embedding_result.shape}"
    )

    # 测试 BGE 嵌入
    bge_embedding = EmbeddingLocalModel("BAAI/bge-large-zh-v1.5")
    sentences = ["样例数据-1", "样例数据-2"]
    embedding_result = bge_embedding.get_embedding(sentences)
    print(
        f"BGE 嵌入结果: \n"
        f"\t 输出类型: {type(embedding_result)}\n"
        f"\t 输出形状: {embedding_result.shape}"
    )
    print("句子嵌入:", embedding_result)
