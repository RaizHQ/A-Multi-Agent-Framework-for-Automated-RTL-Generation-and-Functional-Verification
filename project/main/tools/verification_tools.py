# project\main\tools\verification_tools.py
import json
import numpy as np
from pathlib import Path
from langchain_core.tools import tool

# Resolves to the 'project' root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

@tool
def list_directory(dir_path: str) -> str:
    """
    Lists all files in a given directory relative to the project root.
    Use this to resolve wildcard paths like 'rtl/src/*' or 'data/coeff/*'.
    """
    full_path = BASE_DIR / dir_path
    try:
        if not full_path.exists():
            return f"Directory does not exist: {dir_path}"
        if not full_path.is_dir():
            return f"Path is a file, not a directory: {dir_path}"
            
        files = [str(p.relative_to(BASE_DIR)) for p in full_path.rglob('*') if p.is_file()]
        return json.dumps(files)
    except Exception as e:
        return f"Error listing directory {dir_path}: {str(e)}"

@tool
def generate_stimulus_vectors(stimulus_type: str, num_samples: int, bit_width: int, seed: int = 42) -> str:
    """
    Generates deterministic test stimulus arrays for verification reference models.
    Args:
        stimulus_type: 'impulse', 'step', 'random', or 'sine'.
        num_samples: Number of samples to generate.
        bit_width: The total bit width for the signed integer input.
        seed: Random seed for deterministic reproducibility.
    Returns:
        JSON string of the integer stimulus array.
    """
    try:
        np.random.seed(seed)
        max_val = (2 ** (bit_width - 1)) - 1
        min_val = -(2 ** (bit_width - 1))
        
        if stimulus_type == "impulse":
            vectors = np.zeros(num_samples, dtype=int)
            vectors[0] = max_val
        elif stimulus_type == "step":
            vectors = np.full(num_samples, max_val, dtype=int)
        elif stimulus_type == "random":
            vectors = np.random.randint(min_val, max_val + 1, size=num_samples, dtype=int)
        elif stimulus_type == "sine":
            t = np.linspace(0, 2*np.pi, num_samples)
            # 0.9 scale to prevent overflow
            vectors = np.round(np.sin(t) * (max_val * 0.9)).astype(int)
        else:
            return json.dumps({"error": f"Unknown stimulus_type: {stimulus_type}"})
            
        return json.dumps(vectors.tolist())
    except Exception as e:
        return json.dumps({"error": f"Failed to generate vectors: {str(e)}"})

@tool
def calculate_scoreboard_tolerances(fractional_bits: int, num_taps: int) -> str:
    """
    Calculates the expected worst-case quantization error bounds for the scoreboard to use
    when comparing fixed-point DUT outputs vs floating-point reference outputs.
    """
    try:
        # LSB value
        lsb = 2 ** -fractional_bits
        # Worst case accumulation of quantization errors assuming rounding to nearest
        # Each multiplication introduces up to 0.5 LSB error
        max_theoretical_error = (0.5 * lsb) * num_taps
        
        return json.dumps({
            "lsb_value": lsb,
            "max_theoretical_abs_error": max_theoretical_error,
            "recommended_scoreboard_tolerance": max_theoretical_error * 1.5 # Safety margin
        })
    except Exception as e:
        return json.dumps({"error": str(e)})