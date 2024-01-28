from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
import os
from zhipuai import ZhipuAI
from dotenv import load_dotenv
load_dotenv()

# OpenAI 
def get_docs_list_query_openai(query_str,loader_file_path="knowledges/knowledges.txt",persist_directory = "",k_num=5):
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
        db = Chroma.from_documents(docs, embeddings,collection_name="langchain", persist_directory=persist_directory)
    docs = db.similarity_search(query_str, k=k_num)
    knowledge = ""
    for i in docs:
        knowledge = knowledge+i.page_content+"\n"
    return knowledge

# ZhipuAI
class ZhipuAIEmbeddings:
    def __init__(self, api_key=None):
        self.client = ZhipuAI(api_key=api_key)

    def __call__(self, texts):
        response = self.client.embeddings.create(
            model="embedding-2",
            input=texts,
        )
        return response['embeddings']
    
def get_docs_list_query_zhipu(query_str,loader_file_path="knowledges/knowledges.txt",persist_directory = "",k_num=5):
    embeddings = ZhipuAIEmbeddings()
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
        db = Chroma.from_documents(docs, embeddings,collection_name="langchain", persist_directory=persist_directory)
    docs = db.similarity_search(query_str, k=k_num)
    knowledge = ""
    for i in docs:
        knowledge = knowledge+i.page_content+"\n"
    return knowledge