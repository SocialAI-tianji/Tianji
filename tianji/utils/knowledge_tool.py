from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
import os
from dotenv import load_dotenv
load_dotenv()

def getDocumentsListByQuery(query_str,loader_file_path="knowledges/knowledges.txt",persist_directory = "/home/aistudio/chroma_db_1229",k_num=5):
    embeddings = OpenAIEmbeddings()
    loader_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),loader_file_path)
    if os.path.exists(persist_directory):
        db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
    else:
        loader = TextLoader(file_path=loader_file_path, encoding="utf-8")
        print("loader_file_path",loader)
        print(os.path.exists(loader_file_path))
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        # db = Chroma.from_documents(documents=docs, embedding_function=embeddings, persist_directory=persist_directory)
        db = Chroma.from_documents(docs, embeddings,collection_name="langchain", persist_directory="/home/aistudio/chroma_db_1229")
    docs = db.similarity_search(query_str, k=k_num)
    print(docs)
    knowledge = ""
    for i in docs:
        knowledge = knowledge+i.page_content+"\n"
    return knowledge
# doclist = getDocumentsListByQuery(query_str="元旦祝福")
# 打印Documents结果
#
# for i in doclist:
#     knowledges = knowledges+i.page_content+"\n"
# print(knowledges)