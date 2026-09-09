# project\main\tools\rtl_tools.py
import json
import hashlib
from pathlib import Path
from langchain_core.tools import tool

# Resolves to the 'project' root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

@tool
def verify_coefficient_symmetry(taps_json: str) -> str:
    """
    Mathematically verifies if an array of filter coefficients is symmetric.
    Args:
        taps_json: JSON string of the filter coefficients (list of numbers or list of dictionaries).
    Returns:
        JSON string containing the symmetry status ('symmetric', 'anti-symmetric', or 'none').
    """
    try:
        taps = json.loads(taps_json)
        
        # Extract values depending on whether it's a raw list or the agent's detailed dictionary list
        if len(taps) > 0 and isinstance(taps[0], dict):
            if "fixed_int" in taps[0]:
                vals = [t["fixed_int"] for t in taps]
            elif "float_val" in taps[0]:
                vals = [t["float_val"] for t in taps]
            else:
                return json.dumps({"error": "Coefficient dictionaries missing fixed_int or float_val fields."})
        else:
            vals = taps

        num_taps = len(vals)
        if num_taps == 0:
            return json.dumps({"error": "Empty coefficient array"})

        is_symmetric = True
        is_antisymmetric = True

        for i in range(num_taps // 2):
            if vals[i] != vals[num_taps - 1 - i]:
                is_symmetric = False
            if vals[i] != -vals[num_taps - 1 - i]:
                is_antisymmetric = False

        status = "none"
        if is_symmetric:
            status = "symmetric"
        elif is_antisymmetric:
            status = "anti-symmetric"

        return json.dumps({
            "num_taps": num_taps,
            "symmetry_type": status,
            "is_symmetric": is_symmetric or is_antisymmetric
        })
    except Exception as e:
        return json.dumps({"error": f"Failed to verify symmetry: {str(e)}"})

@tool
def calculate_file_hash(file_path: str) -> str:
    """
    Calculates the SHA-256 hash of a file. Required for the RTL manifest.
    Args:
        file_path: Path to the file relative to the project root.
    Returns:
        JSON string containing the file path and its SHA-256 hash.
    """
    full_path = BASE_DIR / file_path
    try:
        if not full_path.exists():
            return json.dumps({"error": f"File not found: {file_path}"})
        
        sha256_hash = hashlib.sha256()
        with open(full_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return json.dumps({
            "file_path": file_path,
            "sha256": sha256_hash.hexdigest()
        })
    except Exception as e:
        return json.dumps({"error": str(e)})