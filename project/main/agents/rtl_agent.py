# project\main\agents\rtl_agent.py
import sys
from pathlib import Path

# Ensure the 'main' directory is in the Python path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_agent

# Import File Tools
from main.tools.file_tools import read_file, write_file

# Import New RTL Tools
from main.tools.rtl_tools import (
    verify_coefficient_symmetry,
    calculate_file_hash
)

PROMPT_PATH = BASE_DIR / "data" / "md" / "agent_prompts" / "rtl_agent_prompt.md"

def create_rtl_agent():
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Prompt file not found at {PROMPT_PATH}")
    
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 1. Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.0, # Zero temperature to ensure deterministic Verilog generation
        max_retries=2,
    )

    # 2. Define tools - Merging our RTL tools with standard File IO & REPL
    tools = [
        read_file, 
        write_file, 
        verify_coefficient_symmetry,
        calculate_file_hash,
        PythonREPLTool() # Kept as a fallback for complex string manipulation if needed
    ]

    # 3. Create the agent using the modern LangChain API
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt 
    )

    return agent

if __name__ == "__main__":
    agent = create_rtl_agent()
    
    trigger_message = (
        "Begin the Verilog FIR RTL generation process. Read all upstream JSON configurations, "
        "verify the coefficient symmetry, generate the synthesizable Verilog modules, "
        "calculate the coefficient artifact hash for the manifest, write all required output files, "
        "and return the final RTL agent result JSON."
    )
    
    print("Starting RTL Generation Agent...\n")
    
    # 4. Execute the agent directly using messages
    response = agent.invoke({
        "messages": [HumanMessage(content=trigger_message)]
    })
    
    print("\n=== FINAL OUTPUT ===")
    
    # Extract the final message from the sequence
    final_message = response["messages"][-1].content
    print(final_message)