# project\main\tools\architecture_tools.py
import json
import math
from langchain_core.tools import tool

@tool
def analyze_clock_domain(sys_clk_hz: float, sample_rate_hz: float, num_taps: int) -> str:
    """
    Analyzes the clock domain to determine available clock cycles per sample and feasible folding factors.
    Args:
        sys_clk_hz: System clock frequency in Hz.
        sample_rate_hz: Incoming data sample rate in Hz.
        num_taps: Total number of FIR filter taps.
    Returns:
        JSON string containing cycle analysis and architecture feasibility.
    """
    try:
        if sample_rate_hz <= 0:
            return json.dumps({"error": "Sample rate must be greater than 0"})
            
        cycles_per_sample = math.floor(sys_clk_hz / sample_rate_hz)
        
        # Determine if a single DSP can handle all taps sequentially
        can_fully_fold = cycles_per_sample >= num_taps
        max_taps_per_dsp = max(0, cycles_per_sample - 2) # Account for state machine/pipeline overhead
        
        return json.dumps({
            "sys_clk_hz": sys_clk_hz,
            "sample_rate_hz": sample_rate_hz,
            "cycles_per_sample": cycles_per_sample,
            "can_process_fully_sequential": can_fully_fold,
            "max_taps_per_dsp": max_taps_per_dsp,
            "recommended_baseline": "sequential_folded" if can_fully_fold else "parallel"
        })
    except Exception as e:
        return json.dumps({"error": f"Failed to analyze clock domain: {str(e)}"})

@tool
def estimate_hardware_resources(num_taps: int, architecture: str, is_symmetric: bool, folding_factor: int = 1) -> str:
    """
    Estimates FPGA resource usage (DSPs, FFs, BRAMs) based on the chosen FIR architecture.
    Args:
        num_taps: Total number of taps.
        architecture: 'parallel_direct', 'parallel_transposed', or 'sequential_folded'.
        is_symmetric: True if coefficient symmetry is exploited to halve multipliers.
        folding_factor: Number of MAC operations time-multiplexed onto a single DSP (for sequential).
    Returns:
        JSON string containing hardware resource estimates.
    """
    try:
        effective_taps = math.ceil(num_taps / 2) if is_symmetric else num_taps
        
        dsps = 0
        brams = 0
        ffs_baseline = 0
        
        if architecture in ['parallel_direct', 'parallel_transposed']:
            dsps = effective_taps
            ffs_baseline = num_taps * 16 # Rough heuristic for delay line registers
        elif architecture == 'sequential_folded':
            if folding_factor < 1:
                return json.dumps({"error": "Folding factor must be >= 1"})
            dsps = math.ceil(effective_taps / folding_factor)
            brams = 1 if num_taps > 32 else 0 # Use BRAM for tap/coeff storage if large
            ffs_baseline = 150 # Baseline for state machine, counters, and accumulator
        else:
            return json.dumps({"error": "Unknown architecture. Use parallel_direct, parallel_transposed, or sequential_folded"})
            
        return json.dumps({
            "architecture_evaluated": architecture,
            "is_symmetric": is_symmetric,
            "estimated_dsps": dsps,
            "estimated_brams": brams,
            "estimated_ffs": ffs_baseline,
            "assumption": "Estimates assume standard data widths (<18x25). Extreme bit-widths will require cascading DSPs."
        })
    except Exception as e:
        return json.dumps({"error": str(e)})