"""
使用说明：
本脚本实现了一个基于LlamaIndex和智谱AI的高级RAG（检索增强生成）系统。

主要功能：
1. 从指定目录加载文档或从网页加载内容
2. 使用智谱AI的LLM和嵌入模型
3. 创建和持久化FAISS向量索引
4. 实现文档检索和重排序
5. 执行查询并返回结果

参数说明：
- chunk_size: 文档分块大小，默认为1024
- similarity_top_k: 检索时返回的最相似节点数，默认为2
- doc_data_dir: 文档目录路径，当mode为"local"时使用
- url: 网页URL，当mode为"web"时使用
- faiss_index_path: FAISS索引持久化路径
- force: 是否强制重新创建索引，默认为False
- mode: 读取模式，可选 "local" 或 "web"

注意：使用前需要安装额外的库：
pip install llama-index-vector-stores-faiss
pip install llama-index-readers-web

更多关于FAISS向量存储的信息，请参考：
https://docs.llamaindex.ai/en/stable/examples/vector_stores/FaissIndexDemo/
"""

import os
from dotenv import load_dotenv, find_dotenv
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core import QueryBundle
from tianji.knowledges.llamaindex_onlinellm.models import ZhipuLLM, ZhipuEmbeddings
from llama_index.vector_stores.faiss import FaissVectorStore
from tianji import TIANJI_PATH
from huggingface_hub import snapshot_download
import shutil
from llama_index.core.settings import Settings
import faiss


def download_reranker_model():
    local_reranker_path = os.path.join(TIANJI_PATH, "temp", "bge-reranker-base")
    if not os.path.exists(local_reranker_path):
        print("本地未找到reranker模型，正在从Hugging Face下载...")
        try:
            snapshot_download(
                repo_id="BAAI/bge-reranker-base",
                local_dir=local_reranker_path,
                ignore_patterns=["*.md", "*.txt"],
                local_dir_use_symlinks=False,
            )
            print(f"reranker模型已成功下载到 {local_reranker_path}")
        except Exception as e:
            print(f"下载reranker模型时出错: {str(e)}")
            print("将使用默认的在线模型")
            local_reranker_path = "BAAI/bge-reranker-base"
    else:
        print(f"找到本地reranker模型: {local_reranker_path}")
    return local_reranker_path


def setup_index(documents, chunk_size, llm, embed_model, faiss_index_path, force=False):
    Settings.chunk_size = chunk_size
    Settings.llm = llm
    Settings.embed_model = embed_model

    # 检查是否需要强制重建索引
    if force and os.path.exists(faiss_index_path):
        print("强制重建索引，删除现有的持久化数据...")
        shutil.rmtree(faiss_index_path)

    if not os.path.exists(faiss_index_path):
        print("创建新的FAISS索引...")
        d = embed_model.embed_dim  # 获取嵌入维度
        faiss_index = faiss.IndexFlatL2(d)
        vector_store = FaissVectorStore(faiss_index=faiss_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )
        # 保存索引到磁盘
        index.storage_context.persist(persist_dir=faiss_index_path)
    else:
        print("从磁盘加载现有索引...")
        vector_store = FaissVectorStore.from_persist_dir(faiss_index_path)
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store, persist_dir=faiss_index_path
        )
        index = load_index_from_storage(storage_context=storage_context)

    return index


def perform_query(query, retriever, reranker, query_engine):
    nodes = retriever.retrieve(query)
    reranked_nodes = reranker.postprocess_nodes(
        nodes, query_bundle=QueryBundle(query_str=query)
    )

    print(f"初始检索: {len(nodes)} 个节点")
    print(f"重新排序后: {len(reranked_nodes)} 个节点")

    for node in nodes:
        print(node)

    for node in reranked_nodes:
        print(node)

    response = query_engine.query(str_or_query_bundle=query)
    return response


def main(mode, data_source, chunk_size, similarity_top_k, faiss_index_path, force):
    load_dotenv(find_dotenv())

    # 根据模式加载文档
    if mode == "local":
        documents = SimpleDirectoryReader(
            data_source, required_exts=[".txt"]
        ).load_data()
    elif mode == "web":
        documents = SimpleWebPageReader().load_data(urls=[data_source])
    else:
        raise ValueError("无效的模式。请选择 'local' 或 'web'")

    # 初始化模型
    llm = ZhipuLLM()
    embed_model = ZhipuEmbeddings()

    # 设置索引
    index = setup_index(
        documents, chunk_size, llm, embed_model, faiss_index_path, force
    )

    # 设置检索器
    retriever = VectorIndexRetriever(index=index, similarity_top_k=similarity_top_k)

    # 设置重排序器
    local_reranker_path = download_reranker_model()
    reranker = SentenceTransformerRerank(top_n=1, model=local_reranker_path)

    # 设置查询引擎
    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        node_postprocessors=[reranker],
    )

    query = "chatgpt诞生在那一年?全年营收多少"
    response = perform_query(query, retriever, reranker, query_engine)
    print(response)


if __name__ == "__main__":
    # 设置参数
    chunk_size = 1800  # 设置每个文档的块大小
    similarity_top_k = 6  # 设置检索时返回的最相似节点数量
    faiss_index_path = os.path.join(
        TIANJI_PATH, "temp", "llamaindex_rag_faiss_cache"
    )  # 设置FAISS索引的持久化存储路径
    force = True  # 设置为True以强制重新创建索引，即使索引已存在
    mode = "web"  # 设置数据源模式，可以是 "web"（从网络加载）或 "local"（从本地加载）

    if mode == "web":
        data_source = "https://baike.baidu.com/item/OpenAI/19758408"
    else:
        data_source = "./data/"  # 指定本地文档目录

    main(mode, data_source, chunk_size, similarity_top_k, faiss_index_path, force)
