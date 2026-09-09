# project\main\tools\dsp_validation_tools.py
import math
import json
from langchain_core.tools import tool

@tool
def validate_frequencies(fs: float, filter_type: str, freqs_json: str) -> str:
    """
    Validates DSP frequencies against the Nyquist limit and checks transition band logic.
    Args:
        fs: Sampling frequency in Hz.
        filter_type: 'lowpass', 'highpass', 'bandpass', or 'bandstop'.
        freqs_json: JSON string of provided frequencies (e.g., {"passband": 1000, "stopband": 1200}).
    Returns:
        JSON string containing Nyquist violations, transition bandwidth, and logical ordering errors.
    """
    try:
        freqs = json.loads(freqs_json)
        nyquist = fs / 2.0
        issues = []
        
        # Check Nyquist
        for name, val in freqs.items():
            if val is not None and val >= nyquist:
                issues.append(f"Nyquist violation: {name} ({val} Hz) is >= fs/2 ({nyquist} Hz)")

        # Check Ordering / Transition width
        f_pass = freqs.get("passband")
        f_stop = freqs.get("stopband")
        
        if f_pass is not None and f_stop is not None:
            if filter_type == "lowpass" and f_pass >= f_stop:
                issues.append("Lowpass error: passband must be less than stopband.")
            elif filter_type == "highpass" and f_stop >= f_pass:
                issues.append("Highpass error: stopband must be less than passband.")
                
            transition_width = abs(f_stop - f_pass)
        else:
            transition_width = "Unknown - missing passband or stopband"

        return json.dumps({
            "is_valid": len(issues) == 0,
            "nyquist_limit": nyquist,
            "transition_width_hz": transition_width,
            "issues": issues
        })
    except Exception as e:
        return json.dumps({"error": f"Failed to validate frequencies: {str(e)}"})

@tool
def calculate_accumulator_width(input_width: int, coeff_width: int, num_taps: int) -> str:
    """
    Calculates the worst-case accumulator bit-width required to prevent overflow.
    Args:
        input_width: Bit width of the input signal.
        coeff_width: Bit width of the quantized coefficients.
        num_taps: Number of filter taps.
    Returns:
        JSON string containing the minimum safe accumulator width.
    """
    try:
        # Worst case bit growth: input_width + coeff_width + ceil(log2(num_taps))
        growth = math.ceil(math.log2(num_taps))
        acc_width = input_width + coeff_width + growth
        
        return json.dumps({
            "acc_width_required": acc_width,
            "formula_used": f"{input_width} (input) + {coeff_width} (coeff) + {growth} (log2({num_taps}) taps growth)"
        })
    except Exception as e:
        return json.dumps({"error": f"Failed to calculate accumulator width: {str(e)}"})