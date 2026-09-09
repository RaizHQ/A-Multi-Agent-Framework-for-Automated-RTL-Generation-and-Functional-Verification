from key_manager import get_llm
from langchain.agents import create_agent
from tools import calculate_golden_fir_response
import re

def generate_tb(rtl_code: str, spec_message: str) -> dict:
    # 1. Initialize the LLM
    llm = get_llm(temperature=0.1)
    
    # 2. Define the system prompt directly as a string
    system_prompt = (
        "You are an expert FPGA Verification Engineer. Write a self-checking Verilog testbench. \n"
        "1. Use the calculate_golden_fir_response tool to generate expected outputs for a 10-sample step input.\n"
        "2. Hardcode these input stimulus and expected integer outputs into the testbench.\n"
        "3. If all outputs match, $display(\"SIMULATION PASSED\"); otherwise $display(\"SIMULATION FAILED\"); and $stop.\n"
        "4. The top module MUST be named 'tb_fir'. Wrap code in ```verilog ... ``` tags."
    )
    
    # 3. Create the agent using the new factory function
    agent = create_agent(
        model=llm, 
        tools=[calculate_golden_fir_response], 
        system_prompt=system_prompt
    )
    
    # 4. Construct the user message
    user_content = f"Specifications:\n{spec_message}\n\nRTL Code:\n{rtl_code}"
    
    # 5. Invoke the agent using the new standard "messages" list format
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_content}
        ]
    })
    
    # 6. Extract the final output text (safely handling lists/dicts like the earlier fix)
    output_content = response["messages"][-1].content
    if isinstance(output_content, list):
        output_text = "".join([block.get("text", "") if isinstance(block, dict) else str(block) for block in output_content])
    else:
        output_text = str(output_content)

    # 7. Extract the Verilog code
    match = re.search(r'```verilog\n(.*?)\n```', output_text, re.DOTALL)
    if match:
        return {"success": True, "code": match.group(1)}
    return {"success": False, "message": "Failed to extract Testbench code. Agent responded with:\n" + output_text}