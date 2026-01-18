from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    decision: str
    reasoning_summary: List[str]
    missing_info: Optional[str] = None
    sources: List[str]

