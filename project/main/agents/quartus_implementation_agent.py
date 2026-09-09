# project\main\agents\quartus_implementation_agent.py
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

# Import standard File Tools
from main.tools.file_tools import read_file, write_file

# Reuse CLI Tools created for the simulation agent
from main.tools.simulation_tools import (
    check_tool_installed,
    execute_cli_command,
    ensure_directory
)

# Import New Quartus Parsing Tools
from main.tools.quartus_tools import (
    extract_quartus_resources,
    extract_quartus_timing
)

PROMPT_PATH = BASE_DIR / "data" / "md" / "agent_prompts" / "quartus_implementation_agent_prompt.md"

def create_quartus_agent():
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Prompt file not found at {PROMPT_PATH}")
    
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 1. Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.0, # Deterministic logic required for constraints validation
        max_retries=2,
    )

    # 2. Define tools - Combining OS-level CLI control with Quartus-specific parsers
    tools = [
        read_file, 
        write_file, 
        check_tool_installed,
        execute_cli_command,
        ensure_directory,
        extract_quartus_resources,
        extract_quartus_timing,
        PythonREPLTool() # Kept as fallback for dynamic constraint math (e.g., calculating clock periods)
    ]

    # 3. Create the agent using the modern LangChain API
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt 
    )

    return agent

if __name__ == "__main__":
    agent = create_quartus_agent()
    
    trigger_message = (
        "Begin the Quartus implementation process. "
        "First, verify if 'quartus_sh' is installed using check_tool_installed. "
        "Read the validated spec and architecture JSONs to get the exact FPGA part number. "
        "Create the Quartus project and TCL scripts using write_file. "
        "Execute the compilation flow using execute_cli_command. "
        "Extract DSP/LUT utilization and Fmax/Slack using the Quartus extraction tools. "
        "Compare against requirements and write the final quartus results JSON."
    )
    
    print("Starting Quartus Implementation Agent...\n")
    
    # 4. Execute the agent
    response = agent.invoke({
        "messages": [HumanMessage(content=trigger_message)]
    })
    
    print("\n=== FINAL OUTPUT ===")
    
    # Extract the final message from the sequence
    final_message = response["messages"][-1].content
    print(final_message)