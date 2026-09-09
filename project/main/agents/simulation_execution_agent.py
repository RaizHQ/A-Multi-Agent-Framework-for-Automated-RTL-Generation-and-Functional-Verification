# project\main\agents\simulation_execution_agent.py
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

# Import New Simulation Tools
from main.tools.simulation_tools import (
    check_tool_installed,
    execute_cli_command,
    ensure_directory
)

PROMPT_PATH = BASE_DIR / "data" / "md" / "agent_prompts" / "simulation_execution_agent_prompt.md"

def create_simulation_execution_agent():
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Prompt file not found at {PROMPT_PATH}")
    
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 1. Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.0, # Must be 0 for deterministic execution flows
        max_retries=2,
    )

    # 2. Define tools - CLI execution and system checks are the core of this agent
    tools = [
        read_file, 
        write_file, 
        check_tool_installed,
        execute_cli_command,
        ensure_directory,
        PythonREPLTool() # Kept strictly for lightweight internal log parsing if the agent requires it
    ]

    # 3. Create the agent using the modern LangChain API
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt 
    )

    return agent

if __name__ == "__main__":
    agent = create_simulation_execution_agent()
    
    trigger_message = (
        "Begin the simulation execution process. "
        "First, use check_tool_installed to find an available HDL simulator (like iverilog). "
        "Create the isolated simulation directories using ensure_directory. "
        "Compile and execute the RTL testbenches using execute_cli_command. "
        "Capture the exit codes, stdout/stderr, generate the simulation logs, "
        "and return the final simulation execution agent result JSON."
    )
    
    print("Starting Simulation Execution Agent...\n")
    
    # 4. Execute the agent
    response = agent.invoke({
        "messages": [HumanMessage(content=trigger_message)]
    })
    
    print("\n=== FINAL OUTPUT ===")
    
    # Extract the final message from the sequence
    final_message = response["messages"][-1].content
    print(final_message)