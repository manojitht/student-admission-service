import shutil
import os
import time
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from src.config import settings
from src.processing.ingest import ingest_document
from src.core.logger import logger

router = APIRouter()

@router.post("/ingest", summary="Upload and ingest multiple documents")
async def ingest_documents(files: List[UploadFile] = File(...)):
    """
    Ingests a list of files (PDF, TXT) into the Vector DB.
    """
    start_time = time.time()
    
    logger.info(f"Received batch ingestion request for {len(files)} files.")

    results = {
        "succeeded": [],
        "failed": [],
        "total_chunks": 0
    }

    for file in files:
        try:
            # 1. Define save path
            file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
            
            # 2. Save file locally
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # 3. Call the processing logic (Granular logs happen inside here)
            # This is where the splitting and embedding happens
            num_chunks = ingest_document(file_path)
            
            results["succeeded"].append(file.filename)
            results["total_chunks"] += num_chunks
            
        except Exception as e:
            # This catches any errors from the processing step
            logger.error(f"Failed to ingest {file.filename}: {str(e)}")
            results["failed"].append({"filename": file.filename, "error": str(e)})

    process_time = time.time() - start_time
    
    logger.info(f"Batch complete. Added {results['total_chunks']} chunks in {process_time:.2f}s.")
    
    return {
        "message": "Batch ingestion complete",
        "processed_files": len(results["succeeded"]),
        "total_chunks_added": results["total_chunks"],
        "details": results,
        "time_taken": f"{process_time:.2f}s"
    }

