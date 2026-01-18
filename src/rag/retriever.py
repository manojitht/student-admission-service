from typing import List, Dict, Any
from src.config import settings
from src.rag.vectorstore import get_vectorstore

def retrieve_documents(question: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Manually searches ChromaDB and returns a clean list of evidence.
    """
    store = get_vectorstore()
    
    # Perform Similarity Search
    # Note: We use Cosine Distance by default in Chroma, lower score is better? 
    # Actually, usually cosine similarity (1.0 is best). 
    # LangChain's default Chroma wrapper usually returns Distance.
    results = store.similarity_search_with_score(question, k=top_k)

    evidence = []
    for doc, score in results:
        md = doc.metadata or {}
        evidence.append({
            "source_id": md.get("source", "unknown"),
            "content": doc.page_content,
            "score": float(score)
        })
        
    return evidence