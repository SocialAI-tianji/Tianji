import os
from tianji import TIANJI_PATH
from tianji.knowledges.langchain_onlinellm.models import ZhipuAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()


def test_embedding_similarity_zhipuai():
    # Initialize the embedding model
    embedding_model = ZhipuAIEmbeddings()

    # Define two similar sentences
    sentence1 = "春节是中国的传统节日。"
    sentence2 = "中国人每年都庆祝春节。"

    # Get embeddings for the sentences
    embedding1 = embedding_model.embed_query(sentence1)
    embedding2 = embedding_model.embed_query(sentence2)
    embedding_documents = embedding_model.embed_documents([sentence1, sentence2])
    # 打印嵌入向量及其形状
    print(f"Embedding 1 shape: {len(embedding1)}")
    print(f"Embedding 2 shape: {len(embedding2)}")
    print(f"Embedding documents shape: {len(embedding_documents[0])}")

    # Calculate cosine similarity between the two embeddings
    similarity = cosine_similarity([embedding1], [embedding2])[0][0]

    print(f"ZhipuAI Embeddings - Similarity between the sentences: {similarity}")


def test_embedding_similarity_huggingface():
    from langchain_community.embeddings import HuggingFaceBgeEmbeddings

    model_name = "BAAI/bge-base-zh-v1.5"
    model_kwargs = {"device": "cuda"}
    encode_kwargs = {
        "normalize_embeddings": True
    }  # set True to compute cosine similarity
    model = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
        cache_folder=os.path.join(TIANJI_PATH, "temp"),
        query_instruction="为这个句子生成表示以用于检索相关文章：",
    )
    model.query_instruction = "为这个句子生成表示以用于检索相关文章："

    # Define two similar sentences
    sentence1 = "春节是中国的传统节日。"
    sentence2 = "中国人每年都庆祝春节。"

    # Get embeddings for the sentences
    embedding1 = model.embed_query(sentence1)
    embedding2 = model.embed_query(sentence2)

    # Calculate cosine similarity between the two embeddings
    similarity = cosine_similarity([embedding1], [embedding2])[0][0]

    print(f"HuggingFace Embeddings - Similarity between the sentences: {similarity}")


if __name__ == "__main__":
    test_embedding_similarity_zhipuai()
    # test_embedding_similarity_huggingface()
