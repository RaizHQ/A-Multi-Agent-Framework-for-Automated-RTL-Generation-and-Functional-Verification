from key_manager import get_llm
from langchain_core.prompts import ChatPromptTemplate
import re

def generate_rtl(spec_message: str) -> dict:
    llm = get_llm(temperature=0.1)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert FPGA Verilog Designer. Given the filter specs, generate standard Verilog-2001 RTL code for the FIR filter. Ensure you wrap ONLY the code in ```verilog ... ``` tags. Include clock, active-low reset, and enable signals. Optimize for logic (e.g., use shifts instead of multipliers for moving average)."),
        ("user", "Specifications:\n{spec}")
    ])
    chain = prompt | llm
    
    # Get the raw response
    response_content = chain.invoke({"spec": spec_message}).content
    
    # Extract string safely if it returns a list
    if isinstance(response_content, list):
        text_response = "".join([block.get("text", "") if isinstance(block, dict) else str(block) for block in response_content])
    else:
        text_response = str(response_content)
    
    # Now it is safe to use text_response in re.search and string concatenation
    match = re.search(r'```verilog\n(.*?)\n```', text_response, re.DOTALL)
    if match:
        return {"success": True, "code": match.group(1)}
        
    return {"success": False, "message": "Failed to extract RTL code from response: " + text_response}