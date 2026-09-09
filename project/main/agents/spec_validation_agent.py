# project\main\agents\spec_validation_agent.py
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

# Import New Validation Tools
from main.tools.dsp_validation_tools import (
    validate_frequencies,
    calculate_accumulator_width
)

PROMPT_PATH = BASE_DIR / "data" / "md" / "agent_prompts" / "spec_validation_agent_prompt.md"

def create_spec_validation_agent():
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Prompt file not found at {PROMPT_PATH}")
    
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 1. Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.0, # Zero temperature is critical for specification validation
        max_retries=2,
    )

    # 2. Define tools - Merging our validation tools with File IO & REPL
    tools = [
        read_file, 
        write_file, 
        validate_frequencies,
        calculate_accumulator_width,
        PythonREPLTool() # Kept as a fallback for any complex dynamic checks
    ]

    # 3. Create the agent using the modern LangChain API
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt 
    )

    return agent

if __name__ == "__main__":
    agent = create_spec_validation_agent()
    
    trigger_message = (
        "Begin the specification validation process. Read data/json/requirements.json, "
        "check for the existence of the optional toolchain/fpga capability files, "
        "validate all frequency and resource parameters, systematically resolve all 'Automatic' defaults, "
        "and generate the final validated_spec.json, default_decisions.json, "
        "requirements_issues.json, and the agent result JSON."
    )
    
    print("Starting Spec Validation Agent...\n")
    
    # 4. Execute the agent
    response = agent.invoke({
        "messages": [HumanMessage(content=trigger_message)]
    })
    
    print("\n=== FINAL OUTPUT ===")
    
    # Extract the final message from the sequence
    final_message = response["messages"][-1].content
    print(final_message)