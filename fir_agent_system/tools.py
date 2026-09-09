import subprocess
import os
import tempfile
import sys
import numpy as np
from scipy.signal import lfilter
from langchain_core.tools import tool

@tool
def calculate_golden_fir_response(inputs: str, taps: str) -> str:
    """Calculates the golden response of an FIR filter using SciPy and NumPy.
    inputs: comma separated string of integer input samples.
    taps: comma separated string of filter coefficients.
    Returns comma separated string of expected integer outputs.
    """
    try:
        x = np.array([float(i.strip()) for i in inputs.split(',')])
        b = np.array([float(t.strip()) for t in taps.split(',')])
        y = lfilter(b, [1.0], x)
        return ','.join([str(int(val)) for val in y])
    except Exception as e:
        return f"Error computing golden response: {str(e)}"

@tool
def run_quartus_modelsim_headless(rtl_code: str, tb_code: str) -> str:
    """Runs ModelSim headless simulation (bundled with Quartus II 13.0) 
    and live streams stdout directly to your terminal.
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            rtl_path = os.path.join(temp_dir, "fir_filter.v")
            tb_path = os.path.join(temp_dir, "tb_fir.v")
            
            with open(rtl_path, "w") as f:
                f.write(rtl_code)
            with open(tb_path, "w") as f:
                f.write(tb_code)
            
            full_log = []

            def stream_command(cmd):
                print(f"\n[MODELSIM CLI] Executing: {' '.join(cmd)}")
                process = subprocess.Popen(
                    cmd,
                    cwd=temp_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                output_lines = []
                # Read output line by line as it streams in real time
                stdout = process.stdout
                if stdout is None:
                    process.wait()
                    return process.returncode, ""
                for line in stdout:
                    print(f"   {line}", end="", flush=True)  # Live print to your terminal
                    output_lines.append(line)
                    
                process.wait()
                return process.returncode, "".join(output_lines)

            # 1. Initialize Work library
            ret_code, out = stream_command(["vlib", "work"])
            full_log.append(out)
            if ret_code != 0:
                return f"vlib initialization error:\n{''.join(full_log)}"

            # 2. Compile RTL and Testbench
            ret_code, out = stream_command(["vlog", "fir_filter.v", "tb_fir.v"])
            full_log.append(out)
            if ret_code != 0:
                return f"Compilation Error:\n{''.join(full_log)}"

            # 3. Simulate headlessly
            sim_cmd = ["vsim", "-c", "-do", "run -all; quit", "tb_fir"]
            ret_code, out = stream_command(sim_cmd)
            full_log.append(out)
            
            return f"Simulation Output:\n{''.join(full_log)}"

    except FileNotFoundError:
        return "Error: ModelSim commands not found in system PATH. Please add Quartus II / ModelSim binaries to system PATH."
    except Exception as e:
        return f"Simulation Execution Error: {str(e)}"