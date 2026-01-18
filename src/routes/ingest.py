import shutil
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from src.config import settings
from src.processing.ingest import ingest_document

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    
    try:
        # Save file locally
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Trigger ingestion
        num_chunks = ingest_document(file_path)
        
        return {"message": "File processed successfully", "chunks_created": num_chunks}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

