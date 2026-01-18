import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.rag.vectorstore import get_vectorstore

def ingest_document(file_path: str):
    # 1. Load Document based on extension
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)
        
    documents = loader.load()
    
    # 2. Split Text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    
    # 3. Add to ChromaDB
    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)
    
    return len(chunks)

