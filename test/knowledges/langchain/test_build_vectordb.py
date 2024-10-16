from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_core.embeddings import Embeddings
import os
from tianji import TIANJI_PATH  # 引入 TIANJI_PATH

load_dotenv()

model_name = "BAAI/bge-base-zh-v1.5"
model_kwargs = {"device": "cuda"}
encode_kwargs = {"normalize_embeddings": True}
embedding_func = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    cache_folder=os.path.join(TIANJI_PATH, "temp"),
    query_instruction="为这个句子生成表示以用于检索相关文章：",
)


def get_chunks_from_db(
    query_str: str, persist_directory: str, embedding_func: Embeddings, k_num: int
) -> str:
    db = Chroma(embedding_function=embedding_func, persist_directory=persist_directory)
    docs = db.similarity_search(query_str, k=k_num)
    return "\n".join([i.page_content for i in docs])


def create_vectordb(
    folder_path: str,
    persist_directory: str,
    embedding_func: Embeddings,
    chunk_size: int,
    force: bool = False,
):
    if force and os.path.exists(persist_directory):
        print(f"强制模式启用，删除现有的向量数据库：{persist_directory}")
        os.remove(os.path.join(persist_directory, "chroma.sqlite3"))
    elif not force and os.path.exists(persist_directory):
        print(f"向量数据库已存在于 {persist_directory}，直接使用现有数据库。")
        return
    loader = DirectoryLoader(folder_path, glob="*.txt", loader_cls=TextLoader)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=150
    )
    split_docs = text_splitter.split_documents(loader.load())
    vector_db = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_func,
        persist_directory=persist_directory,
    )
    vector_db.persist()


if __name__ == "__main__":
    persist_directory = os.path.join(
        TIANJI_PATH, "temp", "chromadb_spring"
    )  # 复用 persist_directory

    # build_db_from_folder
    folder_path = "./db_files"
    chunk_size = 1024
    force_rebuild = True  # 设置为 True 强制重新生成向量数据库
    create_vectordb(
        folder_path, persist_directory, embedding_func, chunk_size, force=force_rebuild
    )

    # test_get_chunks_from_db
    query_str = "春节,南方吃什么"
    k_num = 5
    result = get_chunks_from_db(query_str, persist_directory, embedding_func, k_num)
    print(f"Top {k_num} chunks from db for query '{query_str}':\n{result}")
