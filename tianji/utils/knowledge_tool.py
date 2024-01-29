from __future__ import annotations

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.embeddings.base import Embeddings
from langchain.pydantic_v1 import BaseModel, root_validator
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()


# OpenAI
def get_docs_list_query_openai(
    query_str,
    loader_file_path="knowledges/knowledges.txt",
    persist_directory="",
    k_num=5,
):
    embeddings = OpenAIEmbeddings()
    loader_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), loader_file_path
    )
    if os.path.exists(persist_directory):
        db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
    else:
        loader = TextLoader(file_path=loader_file_path, encoding="utf-8")
        # print("loader_file_path", loader)
        # print(os.path.exists(loader_file_path))
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        db = Chroma.from_documents(
            docs,
            embeddings,
            collection_name="langchain",
            persist_directory=persist_directory,
        )
    docs = db.similarity_search(query_str, k=k_num)
    knowledge = ""
    for i in docs:
        knowledge = knowledge + i.page_content + "\n"
    return knowledge


class ZhipuAIEmbeddings(BaseModel, Embeddings):
    """`Zhipuai Embeddings` embedding models."""

    zhipuai_api_key: Optional[str] = None
    """Zhipuai application apikey"""

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """
        Validate whether zhipuai_api_key in the environment variables or
        configuration file are available or not.

        Args:

            values: a dictionary containing configuration information, must include the
            fields of zhipuai_api_key
        Returns:

            a dictionary containing configuration information. If zhipuai_api_key
            are not provided in the environment variables or configuration
            file, the original values will be returned; otherwise, values containing
            zhipuai_api_key will be returned.
        Raises:

            ValueError: zhipuai package not found, please install it with `pip install
            zhipuai`
        """
        # values["zhipuai_api_key"] = get_from_dict_or_env(
        #     values,
        #     "zhipuai_api_key",
        #     "ZHIPUAI_API_KEY",
        # )

        try:
            import zhipuai

            # zhipuai.api_key = values["zhipuai_api_key"]
            values["client"] = zhipuai.ZhipuAI()

        except ImportError:
            raise ValueError(
                "Zhipuai package not found, please install it with "
                "`pip install zhipuai`"
            )
        return values

    def _embed(self, texts: str) -> List[float]:
        # send request
        try:
            resp = self.client.embeddings.create(
                model="embedding-2",  # 填写需要调用的模型名称
                input=texts,
            )
        except Exception as e:
            raise ValueError(f"Error raised by inference endpoint: {e}")

        # if resp["code"] != 200:
        #     raise ValueError(
        #         "Error raised by inference API HTTP code: %s, %s"
        #         % (resp["code"], resp["msg"])
        #     )
        embeddings = resp.data[0].embedding

        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """
        Embedding a text.

        Args:

            Text (str): A text to be embedded.

        Return:

            List [float]: An embedding list of input text, which is a list of floating-point values.
        """
        resp = self.embed_documents([text])
        return resp[0]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a list of text documents.

        Args:
            texts (List[str]): A list of text documents to embed.

        Returns:
            List[List[float]]: A list of embeddings for each document in the input list.
                            Each embedding is represented as a list of float values.
        """
        return [self._embed(text) for text in texts]

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """Asynchronous Embed search docs."""
        raise NotImplementedError(
            "Please use `embed_documents`. Official does not support asynchronous requests"
        )

    async def aembed_query(self, text: str) -> List[float]:
        """Asynchronous Embed query text."""
        raise NotImplementedError(
            "Please use `aembed_query`. Official does not support asynchronous requests"
        )


def get_docs_list_query_zhipuai(
    query_str,
    loader_file_path="knowledges/knowledges.txt",
    persist_directory="",
    k_num=5,
):
    embeddings = ZhipuAIEmbeddings()
    loader_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), loader_file_path
    )
    if os.path.exists(persist_directory):
        db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
    else:
        loader = TextLoader(file_path=loader_file_path, encoding="utf-8")
        # print("loader_file_path", loader)
        # print(os.path.exists(loader_file_path))
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        db = Chroma.from_documents(
            docs,
            embeddings,
            collection_name="langchain",
            persist_directory=persist_directory,
        )
    docs = db.similarity_search(query_str, k=k_num)
    knowledge = ""
    for i in docs:
        knowledge = knowledge + i.page_content + "\n"
    return knowledge
