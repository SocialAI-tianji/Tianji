from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from tianji.knowledges.RQA.model import Zhipu_LLM
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from tianji.knowledges.RQA.config import RQA_ST_Liyi_Chroma_Config


def load_chain():
    embeddings = HuggingFaceEmbeddings(
        model_name=RQA_ST_Liyi_Chroma_Config.HF_SENTENCE_TRANSFORMER_WEIGHT
    )

    persist_directory = RQA_ST_Liyi_Chroma_Config.PERSIST_DIRECTORY
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )

    llm = Zhipu_LLM()

    template = """使用以下上下文中文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
    案。尽量使答案调理清楚，内容详实。总是在回答的最后说”谢谢你的提问！“。
    {context}
    问题: {question}
    详细真实的答案:"""

    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"], template=template
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )

    return qa_chain


class Model_center:
    def __init__(self):
        self.chain = load_chain()

    def qa_chain_self_answer(self, question: str, chat_history: list = []):
        if question is None or len(question) < 1:
            return "", chat_history
        try:
            chat_history.append((question, self.chain({"query": question})["result"]))
            return "", chat_history
        except Exception as e:
            return e, chat_history


import gradio as gr

model_center = Model_center()
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
                db_wo_his_btn = gr.Button("Chat")
            with gr.Row():
                clear = gr.ClearButton(components=[chatbot], value="Clear console")

        db_wo_his_btn.click(
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
gr.close_all()
demo.launch()
