import os
from dotenv import load_dotenv
import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tianji.knowledges.langchain_onlinellm.models import ZhipuLLM, ZhipuAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from tianji import TIANJI_PATH

# Initialize HuggingFace Embeddings
model_kwargs = {"device": "cpu"}
hf_embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-zh-v1.5",
    cache_folder=os.path.join(TIANJI_PATH, "temp"),
    model_kwargs=model_kwargs,
)

load_dotenv()

llm = ZhipuLLM()

# 加载、分块和索引 web 上的内容
docs_loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",),
)
docs = docs_loader.load()

# 如果改变 chunk_size ,需要删除之前已建立好的 chroma 存储文件夹
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# use zhipuai
# vectorstore = Chroma.from_documents(documents=splits, embedding=ZhipuAIEmbeddings(), persist_directory=os.path.join(TIANJI_PATH, "temp","test_RAG"))
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=hf_embeddings,
    persist_directory=os.path.join(TIANJI_PATH, "temp", "test_RAG"),
)

# 使用博客的相关片段进行检索和生成
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")
print(prompt)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    result = rag_chain.invoke("TALM是什么?")
    print(result)

    vectorstore.delete_collection()
