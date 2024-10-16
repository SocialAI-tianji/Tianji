import os
import gradio as gr
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from tianji.knowledges.langchain_onlinellm.models import ZhipuAIEmbeddings, ZhipuLLM
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    TextLoader,
    DirectoryLoader,
    WebBaseLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from tianji import TIANJI_PATH

# 加载环境变量
load_dotenv()


def create_embeddings(embedding_choice: str, cache_folder: str):
    """
    根据选择创建嵌入模型
    :param embedding_choice: 嵌入模型选择 ('huggingface' 或 'zhipuai')
    :param cache_folder: 缓存文件夹路径
    :return: 嵌入模型实例
    """
    if embedding_choice == "huggingface":
        return HuggingFaceEmbeddings(
            model_name="BAAI/bge-base-zh-v1.5",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
            cache_folder=cache_folder,
        )
    return ZhipuAIEmbeddings()


def create_vectordb(
    data_type: str,
    data_path: str,
    persist_directory: str,
    embedding_func,
    chunk_size: int,
    force: bool = True,
):
    """
    创建或加载向量数据库
    :param data_type: 数据类型 ('folder' 或 'web')
    :param data_path: 数据路径
    :param persist_directory: 持久化目录
    :param embedding_func: 嵌入函数
    :param chunk_size: 文本块大小
    :param force: 是否强制重建数据库
    :return: Chroma 向量数据库实例
    """
    if os.path.exists(persist_directory) and not force:
        print(f"使用现有的向量数据库: {persist_directory}")
        return Chroma(
            persist_directory=persist_directory, embedding_function=embedding_func
        )

    if force and os.path.exists(persist_directory):
        print(f"强制重建向量数据库: {persist_directory}")
        if os.path.isdir(persist_directory):
            import shutil

            shutil.rmtree(persist_directory)
        else:
            os.remove(persist_directory)

    if data_type == "folder":
        loader = DirectoryLoader(data_path, glob="*.txt", loader_cls=TextLoader)
    elif data_type == "web":
        loader = WebBaseLoader(
            web_paths=(data_path,),
        )
    else:
        raise gr.Error("不支持的数据类型。请选择 'folder' 或 'web'。")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=200
    )
    split_docs = text_splitter.split_documents(loader.load())
    if len(split_docs) == 0:
        raise gr.Error("当前知识数据无效,处理数据后为空")

    vector_db = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_func,
        persist_directory=persist_directory,
    )
    return vector_db


def initialize_chain(
    embedding_choice: str,
    chunk_size: int,
    cache_folder: str,
    persist_directory: str,
    data_type: str,
    data_path: str,
):
    """
    初始化检索增强生成（RAG）链
    :param embedding_choice: 嵌入模型选择
    :param chunk_size: 文本块大小
    :param cache_folder: 缓存文件夹路径
    :param persist_directory: 持久化目录
    :param data_type: 数据类型
    :param data_path: 数据路径
    :return: RAG 链
    """
    embeddings = create_embeddings(embedding_choice, cache_folder)
    vectordb = create_vectordb(
        data_type, data_path, persist_directory, embeddings, chunk_size
    )
    retriever = vectordb.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")
    prompt.messages[
        0
    ].prompt.template = """
    您是一名用于问答任务的助手。使用检索到的上下文来回答问题。如果您不知道答案，就直接说不知道。\
    1.根据我的提问,总结检索到的上下文中与提问最接近的部分,将相关部分浓缩为一段话返回;
    2.根据语料结合我的问题,给出建议和解释。\
    \n问题：{question} \n上下文：{context} \n答案：
    """
    llm = ZhipuLLM()  # 使用ZhipuLLM作为默认LLM
    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )


def format_docs(docs):
    """格式化文档"""
    return "\n\n".join(doc.page_content for doc in docs)


def handle_question(chain, question: str, chat_history):
    """
    处理用户问题
    :param chain: RAG 链
    :param question: 用户问题
    :param chat_history: 聊天历史
    :return: 更新后的问题和聊天历史
    """
    if not question:
        return "", chat_history
    try:
        result = chain.invoke(question)
        chat_history.append((question, result))
        return "", chat_history
    except Exception as e:
        return str(e), chat_history


def update_settings(
    embedding_choice: str,
    chunk_size: int,
    cache_folder: str,
    persist_directory: str,
    data_type: str,
    data_path: str,
):
    """
    更新设置并初始化模型
    :return: 初始化的链和状态消息
    """
    chain = initialize_chain(
        embedding_choice,
        chunk_size,
        cache_folder,
        persist_directory,
        data_type,
        data_path,
    )
    return chain, "什么是春节?"


def update_data_path(data_type: str):
    """
    根据数据类型更新数据路径
    :param data_type: 数据类型
    :return: 更新后的数据路径
    """
    if data_type == "web":
        return (
            "https://r.jina.ai/https://baike.baidu.com/item/%E6%98%A5%E8%8A%82/136876"
        )
    return os.path.join(TIANJI_PATH, "test", "knowledges", "langchain", "db_files")


def update_chat_history(msg: str, chat_history):
    """更新聊天历史"""
    return str(msg), chat_history


# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown(
        """提醒：<br>
        1. 初始化数据库可能需要一些时间，请耐心等待。<br>
        2. 如果使用过程中出现异常，将在文本输入框中显示，请不要惊慌。<br>
        """
    )
    with gr.Row():
        embedding_choice = gr.Radio(
            ["huggingface", "zhipuai"], label="选择嵌入模型", value="zhipuai"
        )
        chunk_size = gr.Slider(256, 2048, step=256, label="选择文本块大小", value=512)
        cache_folder = gr.Textbox(
            label="缓存文件夹路径", value=os.path.join(TIANJI_PATH, "temp")
        )
        persist_directory = gr.Textbox(
            label="持久化数据库路径", value=os.path.join(TIANJI_PATH, "temp", "chromadb_spring")
        )
        data_type = gr.Radio(["folder", "web"], label="数据类型", value="folder")
        data_path = gr.Textbox(
            label="数据路径",
            value=os.path.join(
                TIANJI_PATH, "test", "knowledges", "langchain", "db_files"
            ),
        )
        update_button = gr.Button("初始化数据库")

    chatbot = gr.Chatbot(height=450, show_copy_button=True)
    msg = gr.Textbox(label="问题/提示")

    with gr.Row():
        chat_button = gr.Button("聊天")
        clear_button = gr.ClearButton(components=[chatbot], value="清除聊天记录")

    data_type.change(update_data_path, inputs=[data_type], outputs=[data_path])

    model_chain = gr.State()

    update_button.click(
        update_settings,
        inputs=[
            embedding_choice,
            chunk_size,
            cache_folder,
            persist_directory,
            data_type,
            data_path,
        ],
        outputs=[model_chain, msg],
    )

    chat_button.click(
        handle_question,
        inputs=[model_chain, msg, chatbot],
        outputs=[msg, chatbot],
    ).then(update_chat_history, inputs=[msg, chatbot], outputs=[msg, chatbot])

# 启动Gradio应用
if __name__ == "__main__":
    demo.launch()
