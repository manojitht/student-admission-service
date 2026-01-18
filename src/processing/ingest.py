import os
import time
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.rag.vectorstore import get_vectorstore
from src.config import settings
from src.core.logger import logger  # Import our central logger

def ingest_document(file_path: str):
    try:
        start_time = time.time()
        filename = os.path.basename(file_path)
        
        # 1. Load Document
        logger.info(f"[{filename}] Starting loader...")
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
            
        documents = loader.load()
        logger.info(f"[{filename}] Loaded {len(documents)} pages/documents.")
        
        # 2. Split Text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"[{filename}] Split into {len(chunks)} chunks.")
        
        if not chunks:
            logger.warning(f"[{filename}] No chunks created. File might be empty.")
            return 0
        
        # 3. Embed & Store (The heavy lifting)
        # ChromaDB handles embedding internally when we call add_documents
        logger.info(f"[{filename}] Generating embeddings and storing in ChromaDB...")
        vectorstore = get_vectorstore()
        
        # Add metadata to track the source filename easily later
        for chunk in chunks:
            chunk.metadata["source"] = filename
            
        vectorstore.add_documents(chunks)
        
        elapsed = time.time() - start_time
        logger.info(f"[{filename}] Ingestion complete in {elapsed:.2f}s.")
        
        return len(chunks)

    except Exception as e:
        logger.error(f"[{filename}] Error during processing: {str(e)}")
        raise e
    
