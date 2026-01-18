import uuid
import time
from fastapi import APIRouter, HTTPException
from src.schemas.query import QueryRequest, QueryResponse
from src.rag.retriever import retrieve_documents
from src.rag.generator import generate_decision
from src.core.logger import log_audit_event, logger
from src.utils.parser import parse_agent_response

router = APIRouter()

@router.post("/evaluate", response_model=QueryResponse)
async def evaluate_student(request: QueryRequest):
    try:
        trace_id = str(uuid.uuid4())
        logger.info(f"Processing Request {trace_id}: {request.question}")
        
        # --- STEP 1: RETRIEVE ---
        evidence_list = retrieve_documents(request.question)
        
        # Convert evidence list to a single string for the Prompt
        # Format: "[Source: file.pdf] \n Content: ... \n\n"
        context_str = "\n\n".join(
            [f"[Source: {doc['source_id']}]\n{doc['content']}" for doc in evidence_list]
        )
        
        # --- STEP 2: GENERATE ---
        raw_llm_output = generate_decision(context_text=context_str, question=request.question)
        
        # --- STEP 3: PARSE & LOG ---
        agent_data = parse_agent_response(raw_llm_output)
        
        agent_data["trace_id"] = trace_id
        agent_data["actor"] = "api_user"
        agent_data["processing_time"] = time.time()
        
        log_audit_event(agent_data)
        
        # Extract unique sources from our evidence list
        unique_sources = list(set([doc["source_id"] for doc in evidence_list]))
        
        return QueryResponse(
            decision=agent_data.get("decision", "UNKNOWN"),
            reasoning_summary=agent_data.get("reasoning_summary", []),
            missing_info=agent_data.get("missing_info", "None"),
            sources=unique_sources
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
