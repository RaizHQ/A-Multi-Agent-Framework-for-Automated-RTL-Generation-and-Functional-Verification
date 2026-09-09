import sys
import json
from pathlib import Path

# Ensure the 'main' directory is in the Python path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_experimental.tools import PythonREPLTool

# IMPORT THE CORRECT MODERN AGENT BUILDER
from langchain.agents import create_agent

# Import File Tools
from main.tools.file_tools import read_file, write_file

# Import New DSP Tools
from main.tools.dsp_tools import (
    design_fir_taps, 
    quantize_coefficients, 
    calculate_frequency_response
)

PROMPT_PATH = BASE_DIR / "data" / "md" / "agent_prompts" / "fir_design_agent_prompt.md"

def create_fir_design_agent():
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Prompt file not found at {PROMPT_PATH}")
    
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 1. Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.0, 
        max_retries=2,
    )

    # 2. Define tools - Merging DSP tools with standard File IO & REPL
    tools = [
        read_file, 
        write_file, 
        design_fir_taps, 
        quantize_coefficients, 
        calculate_frequency_response,
        PythonREPLTool() # Kept as a fallback
    ]

    # 3. Create the agent using the modern LangChain API
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt 
    )

    return agent

if __name__ == "__main__":
    agent = create_fir_design_agent()
    
    trigger_message = (
        "Begin the FIR design process. Read the required input JSON files, "
        "compute the taps, perform fixed-point quantization, check the frequency response, "
        "write all specified output JSON files, and return the final agent result JSON."
    )
    
    print("Starting FIR Design Agent...\n")
    
    # 4. Execute the agent
    response = agent.invoke({
        "messages": [HumanMessage(content=trigger_message)]
    })
    
    print("\n=== FINAL OUTPUT ===")
    
    # Extract the final message from the sequence
    final_message = response["messages"][-1].content
    print(final_message)