import json
import logging
import os
from datetime import datetime

# 1. Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# 2. Basic Console Logging (Standard Output)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("admission-agent")

def log_audit_event(audit_data: dict):
    """
    Writes the structured agent decision to the audit log.
    Overwrites timestamp with server time for accuracy.
    """
    try:
        # Add server-side timestamp
        audit_data["server_timestamp"] = datetime.now().isoformat()
        
        # Append to JSONL file
        with open("logs/audit.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_data) + "\n")
            
    except Exception as e:
        # If file write fails, print to console so you see it during the demo
        print(f"FAILED TO WRITE AUDIT LOG: {e}")

