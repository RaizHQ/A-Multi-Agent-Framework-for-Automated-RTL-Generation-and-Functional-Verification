from pathlib import Path
from langchain_core.tools import tool

# Resolves to the 'project' root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

@tool
def read_file(file_path: str) -> str:
    """Reads a file from the given path (relative to the project root) and returns its content."""
    full_path = BASE_DIR / file_path
    try:
        with open(full_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"

@tool
def write_file(file_path: str, content: str) -> str:
    """Writes content to the specified file path (relative to the project root). Creates directories if needed."""
    full_path = BASE_DIR / file_path
    try:
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing to {file_path}: {str(e)}"