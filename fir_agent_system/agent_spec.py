from key_manager import get_llm
from langchain_core.prompts import ChatPromptTemplate

def analyze_spec(requirements: str) -> dict:
    llm = get_llm(temperature=0.1)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert FPGA DSP Specification Analyzer. Analyze the user requirements. If feasible, start your response exactly with 'STATUS: FEASIBLE' and list the structured specs (Taps, Bit-widths, Architecture). If impossible to build, start with 'STATUS: UNFEASIBLE' and provide the reason."),
        ("user", "{requirements}")
    ])
    chain = prompt | llm
    
    # Get the raw response content
    response_content = chain.invoke({"requirements": requirements}).content
    
    # FIX: Safely extract string if LangChain returns a list of dictionaries
    if isinstance(response_content, list):
        # Join text from all blocks in the list
        text_response = "".join([block.get("text", "") if isinstance(block, dict) else str(block) for block in response_content])
    else:
        text_response = str(response_content)
        
    # Now it is safe to use .upper()
    is_feasible = "STATUS: FEASIBLE" in text_response.upper()
    
    return {"feasible": is_feasible, "message": text_response}