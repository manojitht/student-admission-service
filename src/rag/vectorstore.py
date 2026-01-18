from langchain_chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from src.config import settings

def get_vectorstore():
    embedding_function = OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY
    )
    
    vectorstore = Chroma(
        persist_directory=settings.CHROMA_DB_DIR,
        embedding_function=embedding_function,
        collection_name="bank_docs",
        collection_metadata={"hnsw:space": "cosine"}
    )
    return vectorstore

