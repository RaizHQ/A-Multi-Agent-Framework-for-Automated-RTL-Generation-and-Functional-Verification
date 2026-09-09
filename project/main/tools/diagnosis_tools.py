# project\main\tools\diagnosis_tools.py
import json
import re
import os
from pathlib import Path
from langchain_core.tools import tool

# Resolves to the 'project' root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

@tool
def list_workspace_files(directory: str = "data/json") -> str:
    """
    Lists all files in a specific directory (relative to project root).
    Useful for discovering what manifests, logs, or results exist before reading them.
    """
    full_path = BASE_DIR / directory
    try:
        if not full_path.exists():
            return json.dumps({"error": f"Directory does not exist: {directory}"})
            
        files = [str(p.relative_to(BASE_DIR)) for p in full_path.rglob('*') if p.is_file()]
        return json.dumps({"directory": directory, "files": files})
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def search_log_errors(log_file_path: str, context_lines: int = 3) -> str:
    """
    Scans a large log file for error keywords (Error, Fatal, Warning, Mismatch, Fail) 
    and returns the matched lines with surrounding context.
    """
    full_path = BASE_DIR / log_file_path
    if not full_path.exists():
        return json.dumps({"error": f"Log file not found: {log_file_path}"})
        
    try:
        with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
            
        error_patterns = re.compile(r'(error|fatal|mismatch|fail|violation)', re.IGNORECASE)
        extracted = []
        
        for i, line in enumerate(lines):
            if error_patterns.search(line):
                # Grab surrounding context
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                
                snippet = "".join(lines[start:end])
                extracted.append({
                    "line_number": i + 1,
                    "snippet": snippet.strip()
                })
                
        return json.dumps({
            "log_file": log_file_path,
            "errors_found": len(extracted),
            "snippets": extracted[:10] # Cap at 10 to avoid token bloat
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def manage_retry_state(target_agent: str, max_retries: int = 3) -> str:
    """
    Tracks how many times a specific agent has been called to prevent infinite repair loops.
    Reads/Updates 'data/json/retry_state.json'.
    Returns whether the retry limit has been exceeded.
    """
    state_file = BASE_DIR / "data" / "json" / "retry_state.json"
    
    try:
        # Load existing state or initialize
        if state_file.exists():
            with open(state_file, 'r') as f:
                state = json.load(f)
        else:
            state = {}
            
        # Increment counter for the target agent
        current_count = state.get(target_agent, 0) + 1
        state[target_agent] = current_count
        
        # Save updated state
        state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
            
        limit_exceeded = current_count > max_retries
        
        return json.dumps({
            "target_agent": target_agent,
            "current_attempts": current_count,
            "max_retries_allowed": max_retries,
            "limit_exceeded": limit_exceeded,
            "instruction": "Route to 'manual' (BLOCKED) if limit_exceeded is true."
        })
    except Exception as e:
        return json.dumps({"error": str(e)})