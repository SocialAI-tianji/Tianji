"""
使用说明:
    该脚本用于加载基础RAG并提供基于上下文的回答功能。用户可以通过输入问题与模型进行交互，模型将根据提供的上下文生成详细的答案。

    使用方法:
    1. 运行该脚本以启动Gradio界面。
    2. 在输入框中输入您的问题。
    3. 点击“Chat”按钮提交问题。
    4. 模型将返回基于上下文的答案，并在聊天记录中显示。

    参数:
    - question: 用户输入的问题，类型为字符串。
    - chat_history: 聊天记录，类型为列表，默认为空列表。
"""

import gradio as gr
from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from tianji.knowledges.RQA.model import Zhipu_LLM
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from tianji.knowledges.RQA.config import RQA_ST_Liyi_Chroma_Config


def load_chain():
    """
    加载QA链，包括嵌入模型、向量数据库和LLM模型，并生成QA链。

    返回:
    - qa_chain: 返回生成的QA链对象。
    """
    # 加载嵌入模型
    embeddings = HuggingFaceEmbeddings(
        model_name=RQA_ST_Liyi_Chroma_Config.HF_SENTENCE_TRANSFORMER_WEIGHT
    )

    # 加载向量数据库
    persist_directory = RQA_ST_Liyi_Chroma_Config.PERSIST_DIRECTORY
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )

    # 加载LLM模型
    llm = Zhipu_LLM()

    # 定义QA链的提示模板
    template = """使用以下上下文中文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答案。尽量使答案调理清楚，内容详实。总是在回答的最后说”谢谢你的提问！“。
    {context}
    问题: {question}
    详细真实的答案:"""

    qa_chain_prompt = PromptTemplate(
        input_variables=["context", "question"], template=template
    )

    # 创建QA链
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": qa_chain_prompt},
    )

    return qa_chain


class ModelCenter:
    """
    模型中心，目前支持智浦AI
    """

    def __init__(self):
        """
        初始化模型中心，加载QA链。
        """
        self.chain = load_chain()

    def qa_chain_self_answer(self, question: str, chat_history: list = []):
        """
        根据用户输入的问题生成答案，并更新聊天记录。

        参数:
        - question: 用户输入的问题，类型为字符串。
        - chat_history: 聊天记录，类型为列表，默认为空列表。

        返回:
        - 答案和更新后的聊天记录。
        """
        if question is None or len(question) < 1:
            return "", chat_history
        try:
            chat_history.append((question, self.chain({"query": question})["result"]))
            return "", chat_history
        except Exception as e:
            return str(e), chat_history


# 初始化模型中心
model_center = ModelCenter()

# 创建Gradio界面
block = gr.Blocks()
with block as demo:
    with gr.Row(equal_height=True):
        with gr.Column(scale=15):
            gr.Markdown(
                """<h1><center>InternLM</center></h1>
                <center>人情世故</center>
                """
            )

    with gr.Row():
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(height=450, show_copy_button=True)
            msg = gr.Textbox(label="Prompt/问题")

            with gr.Row():
                chat_button = gr.Button("Chat")
            with gr.Row():
                clear_button = gr.ClearButton(
                    components=[chatbot], value="Clear console"
                )

        # 绑定按钮点击事件
        chat_button.click(
            model_center.qa_chain_self_answer,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot],
        )

    gr.Markdown(
        """提醒：<br>
    1. 初始化数据库时间可能较长，请耐心等待。
    2. 使用中如果出现异常，将会在文本输入框进行展示，请不要惊慌。 <br>
    """
    )

demo.launch()
