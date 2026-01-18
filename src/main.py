from fastapi import FastAPI
from src.routes import chat, ingest

app = FastAPI(
    title="Enterprise RAG Service",
    description="Two separate APIs: One for data ingestion, one for querying."
)

app.include_router(ingest.router, prefix="/api/v1/documents", tags=["Ingestion"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Query"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="localhost", port=8000, reload=True)

