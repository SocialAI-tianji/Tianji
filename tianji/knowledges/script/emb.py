from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma 

from . import RQA_ST_Liyi_Chroma_Config

if __name__ == "__main__":
    persist_directory = RQA_ST_Liyi_Chroma_Config.PERSIST_DIRECTORY
    data_directory = RQA_ST_Liyi_Chroma_Config.ORIGIN_DATA
    loader = DirectoryLoader(data_directory, glob="*.txt", loader_cls=TextLoader)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=150)
    split_docs = text_splitter.split_documents(loader.load())
    
    
    embeddings = HuggingFaceEmbeddings(model_name="/root/weights/model/sentence-transformer")
    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=persist_directory 
    )
    vectordb.persist()