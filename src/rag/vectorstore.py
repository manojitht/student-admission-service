from langchain_chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from src.config import settings

def get_vectorstore():
    embedding_function = OpenAIEmbeddings(
        model=settings.openai_embed_model,
        api_key=settings.OPENAI_API_KEY
    )
    
    vectorstore = Chroma(
        persist_directory=settings.CHROMA_DB_DIR,
        embedding_function=embedding_function,
        collection_name="bank_docs",
    )
    return vectorstore

