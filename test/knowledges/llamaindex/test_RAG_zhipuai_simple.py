"""
使用说明：
本脚本实现了一个基于LlamaIndex和智谱AI的简单RAG（检索增强生成）系统。

主要功能：
1. 从指定网页加载内容
2. 使用智谱AI的LLM和嵌入模型
3. 创建向量索引
4. 实现基于检索的问答

注意：使用前需要安装额外的库：
pip install llama-index llama-index-readers-web
"""

import os
import time
from tianji.knowledges.llamaindex_onlinellm.models import ZhipuLLM, ZhipuEmbeddings
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.readers.web import SimpleWebPageReader
from dotenv import load_dotenv

load_dotenv()


def test_retrieval_chat_zhipuai():
    # 初始化嵌入模型和语言模型
    embed_model = ZhipuEmbeddings()
    llm = ZhipuLLM()

    # 从网络获取文档
    urls = [
        r"https://baike.baidu.com/item/%E6%98%A5%E8%8A%82/136876",
        r"https://baike.baidu.com/item/%E5%85%83%E6%97%A6/137017",
    ]
    documents = SimpleWebPageReader().load_data(urls)

    # 创建索引，设定上下文长度
    Settings.chunk_size = 2048
    Settings.chunk_overlap = 200
    parser = SimpleNodeParser.from_defaults()
    nodes = parser.get_nodes_from_documents(documents)

    # 记录索引创建时间
    start_time = time.time()
    index = VectorStoreIndex(nodes, embed_model=embed_model)
    end_time = time.time()
    print(f"索引创建耗时: {end_time - start_time:.2f} 秒")

    # 创建检索器
    retriever = index.as_retriever(similarity_top_k=2)

    # 创建聊天引擎
    chat_engine = SimpleChatEngine.from_defaults(
        llm=llm,
        retriever=retriever,
        system_prompt="你是一个智能助手，使用检索到的信息来回答问题。如果无法找到相关信息，请诚实地说不知道。",
    )

    # 进行检索对话
    questions = ["春节有哪些传统习俗？", "中国的传统节日有哪些？", "如何制作饺子？"]

    for question in questions:
        print(f"问题: {question}")
        response = chat_engine.chat(question)
        print(f"回答: {response.response}\n")


if __name__ == "__main__":
    test_retrieval_chat_zhipuai()
