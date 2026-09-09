# project\main\tools\quartus_tools.py
import json
import re
from pathlib import Path
from langchain_core.tools import tool

# Resolves to the 'project' root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

@tool
def extract_quartus_resources(summary_file_path: str) -> str:
    """
    Reads a Quartus .map.summary or .fit.summary file and extracts resource utilization.
    Returns JSON containing DSP, ALM/LUT, Register, and BRAM usage.
    """
    full_path = BASE_DIR / summary_file_path
    if not full_path.exists():
        return json.dumps({"error": f"Summary file not found: {summary_file_path}"})
        
    try:
        with open(full_path, 'r') as f:
            content = f.read()

        # Regex patterns for various Quartus Prime Standard/Pro resource lines
        metrics = {
            "dsps": re.search(r'(?:Total DSP Blocks|DSP Blocks|DSP blocks).*?:\s*([\d,]+)', content),
            "alms_luts": re.search(r'(?:Logic utilization \(in ALMs\)|Total logic elements|ALMs).*?:\s*([\d,]+)', content),
            "registers": re.search(r'(?:Total registers|Dedicated logic registers).*?:\s*([\d,]+)', content),
            "bram_bits": re.search(r'(?:Total block memory bits).*?:\s*([\d,]+)', content)
        }

        results = {}
        for key, match in metrics.items():
            if match:
                # Remove commas and convert to int
                results[key] = int(match.group(1).replace(',', ''))
            else:
                results[key] = None

        return json.dumps({
            "file_parsed": summary_file_path,
            "resources": results
        })
    except Exception as e:
        return json.dumps({"error": f"Failed to parse resources: {str(e)}"})

@tool
def extract_quartus_timing(sta_rpt_file_path: str) -> str:
    """
    Extracts worst-case Setup Slack, Hold Slack, and Fmax from a Quartus Timing Analyzer (.sta.rpt) report.
    Returns JSON with timing metrics.
    """
    full_path = BASE_DIR / sta_rpt_file_path
    if not full_path.exists():
        return json.dumps({"error": f"Timing report not found: {sta_rpt_file_path}"})
        
    try:
        with open(full_path, 'r') as f:
            # We don't read the whole file into memory if it's huge, but .sta.rpt summaries are usually manageable
            # For safety, we'll read line by line and look for the Setup/Hold Summary tables
            setup_slack = None
            hold_slack = None
            fmax = None
            
            content = f.read()
            
            # Common Quartus STA report patterns
            setup_match = re.search(r'Setup\s+:\s+([-\d\.]+)', content)
            hold_match = re.search(r'Hold\s+:\s+([-\d\.]+)', content)
            fmax_match = re.search(r'Fmax\s+:\s+([\d\.]+)\s+MHz', content)

            if setup_match: setup_slack = float(setup_match.group(1))
            if hold_match: hold_slack = float(hold_match.group(1))
            if fmax_match: fmax = float(fmax_match.group(1))

        return json.dumps({
            "file_parsed": sta_rpt_file_path,
            "timing": {
                "worst_case_setup_slack_ns": setup_slack,
                "worst_case_hold_slack_ns": hold_slack,
                "fmax_mhz": fmax
            }
        })
    except Exception as e:
        return json.dumps({"error": f"Failed to parse timing: {str(e)}"})