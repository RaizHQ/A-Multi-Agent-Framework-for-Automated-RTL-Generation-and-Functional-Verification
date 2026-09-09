# project\main\tools\dsp_tools.py
import json
import numpy as np
from scipy import signal
from langchain_core.tools import tool

@tool
def design_fir_taps(num_taps: int, cutoff_freqs: list[float], filter_type: str, fs: float, window: str = "hamming") -> str:
    """
    Designs an FIR filter and returns floating point coefficients.
    Args:
        num_taps: Number of filter taps (must be odd/even appropriately).
        cutoff_freqs: List of cutoff frequencies in Hz.
        filter_type: 'lowpass', 'highpass', 'bandpass', or 'bandstop'.
        fs: Sampling frequency in Hz.
        window: Window type (e.g., 'hamming', 'hann', 'blackman', or a tuple like '("kaiser", 5.0)').
    Returns:
        JSON string containing the array of floating-point taps.
    """
    try:
        # Safely evaluate tuple strings for parametric windows like kaiser
        if "kaiser" in window:
            window = eval(window)
            
        taps = signal.firwin(
            numtaps=num_taps,
            cutoff=cutoff_freqs,
            window=window,
            pass_zero=filter_type in ['lowpass', 'bandstop'],
            fs=fs
        )

        taps_array = np.asarray(taps)
        return json.dumps(taps_array.tolist())
    
    except Exception as e:
        return f"Error designing filter: {str(e)}"

@tool
def quantize_coefficients(taps_json: str, total_bits: int, fractional_bits: int) -> str:
    """
    Quantizes floating-point FIR coefficients to fixed-point representations.
    Args:
        taps_json: JSON string of floating-point taps array.
        total_bits: Total bit width of the coefficient.
        fractional_bits: Number of fractional bits (Q notation).
    Returns:
        JSON string of detailed dictionary containing floating, fixed_int, scale, and quant_error for each tap.
    """
    try:
        taps = np.array(json.loads(taps_json))
        scale_factor = 2 ** fractional_bits
        
        # Calculate max min bounds based on signed representation
        max_val = (2 ** (total_bits - 1)) - 1
        min_val = -(2 ** (total_bits - 1))
        
        quantized_data = []
        for i, tap in enumerate(taps):
            # Scale and round
            scaled = np.round(tap * scale_factor)
            # Clip to bit width
            clipped = np.clip(scaled, min_val, max_val)
            
            quantized_tap = int(clipped)
            reconstructed = quantized_tap / scale_factor
            error = float(tap - reconstructed)
            
            quantized_data.append({
                "tap_index": i,
                "float_val": float(tap),
                "fixed_int": quantized_tap,
                "scale_factor": scale_factor,
                "bit_width": total_bits,
                "q_format": f"Q{total_bits - fractional_bits - 1}.{fractional_bits}",
                "quant_error": error
            })
            
        return json.dumps(quantized_data)
    except Exception as e:
        return f"Error quantizing coefficients: {str(e)}"

@tool
def calculate_frequency_response(taps_json: str, fs: float) -> str:
    """
    Calculates the frequency response of the given filter taps.
    Args:
        taps_json: JSON string of filter taps (either float or reconstructed fixed-point).
        fs: Sampling frequency in Hz.
    Returns:
        JSON string containing arrays for 'frequencies' (Hz) and 'magnitude_db'.
    """
    try:
        taps = np.array(json.loads(taps_json))
        w, h = signal.freqz(taps, worN=1024, fs=fs)
        
        # Avoid log of zero
        magnitude = np.abs(h)
        magnitude = np.maximum(magnitude, 1e-12)
        magnitude_db = 20 * np.log10(magnitude)
        
        response = {
            "frequencies": np.asarray(w).tolist(),
            "magnitude_db": np.asarray(magnitude_db).tolist()
        }
        return json.dumps(response)
    except Exception as e:
        return f"Error calculating frequency response: {str(e)}"