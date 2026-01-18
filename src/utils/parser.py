import json
import re

def parse_agent_response(full_text: str):
    """
    Parses the single JSON output from the LLM.
    """
    try:
        # 1. Clean Markdown code blocks if present
        json_str = re.sub(r'```json', '', full_text)
        json_str = re.sub(r'```', '', json_str).strip()
        
        # 2. Parse JSON
        data = json.loads(json_str)
        return data
        
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        # Return a safe fallback structure if LLM fails
        return {
            "decision": "ERROR",
            "reasoning_summary": ["Failed to parse agent response."],
            "missing_info": "Raw output was invalid JSON.",
            "key_facts": [],
            "checks": []
        }
    
