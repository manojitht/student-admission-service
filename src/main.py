from fastapi import FastAPI
from src.routes import chat, ingest
import uvicorn

app = FastAPI(title="Bank RAG Service", version="1.0.0")

# Include Routers
app.include_router(ingest.router, prefix="/api/v1", tags=["Ingestion"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="localhost", port=8000, reload=True)
