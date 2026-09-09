import json
import os
import re
from typing import Any, cast
import numpy as np
from scipy import signal

# Determine the absolute path to the directory where this Python script lives (project/main/prompt_generators)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the JSON file: go up two levels ('..', '..'), then into 'data/json'
json_file_path = os.path.join(script_dir, '..', '..', 'data', 'json', 'requirements.json')

# Normalize the path (resolves the '..' to a clean path string)
json_file_path = os.path.normpath(json_file_path)

# 1. Read JSON data from requirements.json
try:
    with open(json_file_path, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: 'requirements.json' not found at:\n{json_file_path}")
    exit(1)
except json.JSONDecodeError:
    print("Error: 'requirements.json' contains invalid JSON.")
    exit(1)

# 2. Define a list of ALL possible keys
all_keys = [
    # Basic
    "projectName", "experience", "hdl", "description", "filterType", 
    "samplingFrequency", "samplingUnit", "cutoff", "lowerFrequency", 
    "upperFrequency", "passband", "stopband", "ripple", "attenuation", 
    "tapMode", "tapValue", "designMethod", "kaiserBeta", "linearPhase",
    "manufacturer", "fpgaPart", "board", "tool", "clock", "sampleRate", 
    "source", "adcResolution", "throughput", "testbench", "verification", 
    "simTool", "verify", "output", "notes",
    # Advanced
    "inputWidth", "inputFormat", "inputQ", "coeffWidth", "coeffQ", 
    "accWidth", "outputWidth", "rounding", "overflow",
    "architecture", "processing", "symmetric", "optimization", "latency", 
    "timingThroughput", "pipelining", "clockDomains", "firClock",
    "interface", "inputHandshake", "outputHandshake", "resetType", 
    "resetPolarity", "clockEnable",
    # Expert Constraints
    "maxDSP", "maxLUT", "maxBRAM", "maxFF", "maxPower", "constraints"
]

# 3. Fill missing or empty keys with "N/A" so the formatter doesn't crash
safe_data = {}
for key in all_keys:
    val = data.get(key)
    if val in [None, "", []]:
        safe_data[key] = "N/A"
    else:
        safe_data[key] = val

if safe_data.get("clockDomains") != "Separate clocks" and safe_data.get("firClock") == "N/A":
    safe_data["firClock"] = "Same as System Clock"

# 4. Format lists into readable strings
if isinstance(safe_data['verify'], list): safe_data['verify'] = ", ".join(safe_data['verify'])
if isinstance(safe_data['output'], list): safe_data['output'] = ", ".join(safe_data['output'])

# 5. --- Calculate AND Quantize FIR Coefficients using SciPy ---
def parse_float(val, default=None):
    try: return float(val)
    except (ValueError, TypeError): return default

def calculate_and_quantize_coefficients(data_dict):
    try:
        # 1. Extract parameters
        fs = parse_float(data_dict.get('samplingFrequency'))
        num_taps = int(parse_float(data_dict.get('tapValue'), 31))

        filter_type = (
            str(data_dict.get('filterType', 'lowpass'))
            .lower()
            .replace("-", "")
            .replace(" ", "")
        )

        # Determine cutoff frequencies
        if filter_type in ['lowpass', 'highpass']:
            cutoffs = parse_float(data_dict.get('cutoff'))

        elif filter_type in ['bandpass', 'bandstop']:
            cutoffs = [
                parse_float(data_dict.get('lowerFrequency')),
                parse_float(data_dict.get('upperFrequency'))
            ]

        else:
            raise ValueError(
                f"Unsupported filter type: {filter_type}"
            )

        pass_zero = (
            False
            if filter_type in ['highpass', 'bandpass']
            else True
        )

        # ==================================================
        # 2. DESIGN FIR FILTER USING SELECTED METHOD
        # ==================================================

        design_method = str(
            data_dict.get('designMethod', 'Kaiser Window')
        ).lower().strip()

        design_method = (
            design_method
            .replace('-', '')
            .replace('_', '')
            .replace(' ', '')
        )


        kaiser_beta = parse_float(data_dict.get('kaiserBeta'))
        if kaiser_beta is None:
            kaiser_beta = 5.0

        if design_method in ['kaiser', 'kaiserwindow', 'automatic']:

            coeffs_float = signal.firwin(
                num_taps,
                cutoffs,
                pass_zero=pass_zero,
                window=cast(Any, ('kaiser', kaiser_beta)),
                fs=fs
            )

        elif design_method in ['hamming', 'hammingwindow']:

            coeffs_float = signal.firwin(
                num_taps,
                cutoffs,
                pass_zero=pass_zero,
                window='hamming',
                fs=fs
            )

        elif design_method in ['hann', 'hannwindow', 'hanning']:

            coeffs_float = signal.firwin(
                num_taps,
                cutoffs,
                pass_zero=pass_zero,
                window='hann',
                fs=fs
            )

        elif design_method in ['blackman', 'blackmanwindow']:

            coeffs_float = signal.firwin(
                num_taps,
                cutoffs,
                pass_zero=pass_zero,
                window='blackman',
                fs=fs
            )

        elif design_method in ['bartlett', 'bartlettwindow']:

            coeffs_float = signal.firwin(
                num_taps,
                cutoffs,
                pass_zero=pass_zero,
                window='bartlett',
                fs=fs
            )

        elif design_method in [
            'boxcar',
            'rectangular',
            'rectangularwindow'
        ]:

            coeffs_float = signal.firwin(
                num_taps,
                cutoffs,
                pass_zero=pass_zero,
                window='boxcar',
                fs=fs
            )

        else:
            raise ValueError(
                f"Unsupported FIR design method: "
                f"{data_dict.get('designMethod')}"
            )

        # ==================================================
        # 3. FIXED-POINT QUANTIZATION
        # ==================================================

        c_width_str = str(
            data_dict.get('coeffWidth', '16')
        )

        match = re.search(r'(\d+)', c_width_str)

        bit_width = int(match.group(1)) if match else 16

        scale_factor = (1 << (bit_width - 1)) - 1

        coeffs_fixed = np.round(
            coeffs_float * scale_factor
        ).astype(int)

        # ==================================================
        # 4. FORMAT COEFFICIENTS FOR PROMPT
        # ==================================================

        float_str = ",\n".join(
            [f"    {c:.10f}" for c in coeffs_float]
        )

        fixed_str = ",\n".join(
            [f"    {c}" for c in coeffs_fixed]
        )

        return {
            "float": f"[\n{float_str}\n]",
            "fixed": f"[\n{fixed_str}\n]",
            "bit_width": bit_width,
            "scale_factor": scale_factor
        }

    except Exception as e:

        err = f"Error: {str(e)}"

        return {
            "float": err,
            "fixed": err,
            "bit_width": "N/A",
            "scale_factor": "N/A"
        }
    
# Execute and inject dictionaries into safe_data
coeff_results = calculate_and_quantize_coefficients(data)
safe_data['calculated_coeffs_float'] = coeff_results['float']
safe_data['calculated_coeffs_fixed'] = coeff_results['fixed']
safe_data['coeff_bit_width'] = coeff_results['bit_width']
safe_data['coeff_scale_factor'] = coeff_results['scale_factor']


# 6. Read the Expert prompt template from rtl_expert_prompt.md
md_template_path = os.path.join(script_dir, '..', '..', 'data', 'md', 'templates', 'rtl_expert_prompt.md')
md_template_path = os.path.normpath(md_template_path)

try:
    with open(md_template_path, 'r', encoding='utf-8') as md_file:
        prompt_template = md_file.read()
except FileNotFoundError:
    print(f"Error: Prompt template 'rtl_expert_prompt.md' not found at:\n{md_template_path}")
    exit(1)

# 7. Format the template with the safe JSON data
final_prompt = prompt_template.format(**safe_data)

# 8. Write the generated prompt to rtl_prompt.md
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', '..', 'data', 'md', 'agent_prompts')
output_dir = os.path.normpath(output_dir)
os.makedirs(output_dir, exist_ok=True)
output_filename = os.path.join(output_dir, 'rtl_agent_prompt.md')

with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(final_prompt)
    
print(f"Successfully generated the prompt with Fixed-Point SciPy coefficients and saved it to {output_filename}")