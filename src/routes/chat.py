from fastapi import APIRouter, HTTPException
from src.schemas.query import QueryRequest, QueryResponse
from src.rag.chain import get_rag_chain

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    try:
        chain = get_rag_chain()
        response = chain.invoke({"query": request.question})
        
        answer = response["result"]
        # Extract unique sources
        sources = list(set([doc.metadata.get("source", "unknown") for doc in response["source_documents"]]))
        
        return QueryResponse(answer=answer, sources=sources)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

