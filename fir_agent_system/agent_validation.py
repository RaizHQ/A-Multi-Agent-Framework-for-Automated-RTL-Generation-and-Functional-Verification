from key_manager import get_llm
from langchain.agents import create_agent
from tools import run_quartus_modelsim_headless

def validate_design(rtl_code: str, tb_code: str) -> dict:
    llm = get_llm(temperature=0.1)
    
    system_prompt = (
        "You are an FPGA Validation Agent. Use the run_quartus_modelsim_headless tool to compile and simulate the provided RTL and TB files. \n"
        "1. Analyze the simulation log.\n"
        "2. If the log contains 'SIMULATION PASSED', declare the verification successful.\n"
        "3. If it contains 'SIMULATION FAILED' or compilation errors, identify the specific Verilog bug."
    )
    
    agent = create_agent(
        model=llm,
        tools=[run_quartus_modelsim_headless],
        system_prompt=system_prompt
    )
    
    user_content = f"RTL Code:\n{rtl_code}\n\nTestbench Code:\n{tb_code}"
    
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_content}
        ]
    })
    
    output_content = response["messages"][-1].content
    if isinstance(output_content, list):
        output_text = "".join([block.get("text", "") if isinstance(block, dict) else str(block) for block in output_content])
    else:
        output_text = str(output_content)
    
    success = "PASSED" in output_text.upper() or "SUCCESSFUL" in output_text.upper()
    return {"success": success, "message": output_text}