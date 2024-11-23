import os
from tianji import TIANJI_PATH
from tianji.knowledges.langchain_onlinellm.models import SiliconFlowEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

def test_embedding_similarity_siliconflow():
    # Initialize the embedding model
    embedding_model = SiliconFlowEmbeddings()

    # Define two similar sentences
    sentence1 = "春节是中国的传统节日。"
    sentence2 = "中国人每年都庆祝春节。"

    # Get embeddings for the sentences
    embedding1 = embedding_model.embed_query(sentence1)
    embedding2 = embedding_model.embed_query(sentence2)
    embedding_documents = embedding_model.embed_documents([sentence1, sentence2])
    print(f"Embedding 1 shape: {len(embedding1)}")
    print(f"Embedding 2 shape: {len(embedding2)}")
    print(f"Embedding documents shape: {len(embedding_documents[0])}")
    # Calculate cosine similarity between the two embeddings
    similarity = cosine_similarity([embedding1], [embedding2])[0][0]

    print(f"SiliconFlow Embeddings - Similarity between the sentences: {similarity}")

if __name__ == "__main__":
    test_embedding_similarity_siliconflow()