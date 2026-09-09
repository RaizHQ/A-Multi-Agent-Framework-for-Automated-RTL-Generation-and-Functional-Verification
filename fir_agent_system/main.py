import os
from agent_spec import analyze_spec
from agent_rtl import generate_rtl
from agent_tb import generate_tb
from agent_validation import validate_design
from key_manager import safe_execute # Import the error handler

#Simple 8-tap Moving Average Low-pass FIR filter

def main():
    if not os.path.exists("requirements.md"):
        print("[!] Error: requirements.md not found in the root directory.")
        return

    with open("requirements.md", "r") as f:
        requirements = f.read()

    print("\n=== 1. Invoking Specification Analyzer Agent ===")
    spec_result = safe_execute(analyze_spec, requirements)
    if not isinstance(spec_result, dict) or not spec_result.get("feasible", False):
        print("[!] Error: User requirements are unfeasible or API failed.")
        print(spec_result.get("message", "Unknown error.") if isinstance(spec_result, dict) else "Unknown error.")
        return
    print("[+] Specifications Feasible. Extracted parameters successfully.\n")
    
    print("=== 2. Invoking RTL Agent ===")
    rtl_result = safe_execute(generate_rtl, spec_result["message"])
    if not isinstance(rtl_result, dict) or not rtl_result.get("success", False):
        print("[!] Error in RTL Generation:")
        print(rtl_result.get("message", "Unknown error.") if isinstance(rtl_result, dict) else "Unknown error.")
        return
    
    with open("fir_filter.v", "w") as f:
        f.write(rtl_result["code"])
    print("[+] RTL generated and saved to fir_filter.v\n")
    
    print("=== 3. Invoking Testbench Generator Agent ===")
    tb_result = safe_execute(generate_tb, rtl_result["code"], spec_result["message"])
    if not isinstance(tb_result, dict) or not tb_result.get("success", False):
        print("[!] Error in Testbench Generation:")
        print(tb_result.get("message", "Unknown error.") if isinstance(tb_result, dict) else "Unknown error.")
        return
    
    with open("tb_fir.v", "w") as f:
        f.write(tb_result["code"])
    print("[+] Self-checking Testbench generated and saved to tb_fir.v\n")
    
    print("=== 4. Invoking Validation Agent (Quartus/ModelSim Headless) ===")
    val_result = safe_execute(validate_design, rtl_result["code"], tb_result["code"])
    
    print("\n---------------------------------------------------------")
    if not isinstance(val_result, dict) or not val_result.get("success", False):
        print("[X] VALIDATION FAILED")
        print(val_result.get("message", "Unknown error.") if isinstance(val_result, dict) else "Unknown error.")
    else:
        print("[✓] VALIDATION SUCCESSFUL - Output meets user requirements")
        print(val_result.get("message", ""))
    print("---------------------------------------------------------")

if __name__ == "__main__":
    main()