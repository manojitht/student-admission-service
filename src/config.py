import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Required Secrets
    OPENAI_API_KEY: str
    
    # Paths
    CHROMA_DB_DIR: str = "data/chroma"
    UPLOAD_DIR: str = "data/uploads"
    AUDIT_LOG_PATH: str = "logs/audit.jsonl"
    POLICY_PATH: str = "data/policies/policy_scholarship_and_program.txt"
    
    # Models (Matches the lowercase names in your .env / error log)
    openai_model: str = "gpt-4o-mini"
    openai_embed_model: str = "text-embedding-3-large"
    
    # RAG Parameters
    chunk_size: int = 600
    chunk_overlap: int = 150
    TOP_K: int = 3
    
    # System
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        # CRITICAL FIX: This tells Pydantic to ignore any unknown variables 
        # in the .env file instead of crashing.
        extra = "ignore" 

settings = Settings()

# Ensure directories exist
os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)