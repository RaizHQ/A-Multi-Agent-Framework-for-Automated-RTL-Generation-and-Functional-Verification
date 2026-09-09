# project\main\agents\diagnosis_router_agent.py
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

# Import New Diagnosis Tools
from main.tools.diagnosis_tools import (
    list_workspace_files,
    search_log_errors,
    manage_retry_state
)

PROMPT_PATH = BASE_DIR / "data" / "md" / "agent_prompts" / "diagnosis_router_agent_prompt.md"

def create_diagnosis_router_agent():
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Prompt file not found at {PROMPT_PATH}")
    
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 1. Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.0, # Deterministic, analytical reasoning required
        max_retries=2,
    )

    # 2. Define tools - Focused on log parsing, state management, and file I/O
    tools = [
        read_file, 
        write_file, 
        list_workspace_files,
        search_log_errors,
        manage_retry_state,
        PythonREPLTool() # Kept in case the agent needs to perform complex diffs between JSON files
    ]

    # 3. Create the agent using the modern LangChain API
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt 
    )

    return agent

if __name__ == "__main__":
    agent = create_diagnosis_router_agent()
    
    trigger_message = (
        "Begin the diagnosis and routing process. "
        "Use list_workspace_files to check simulation and quartus directories. "
        "Use search_log_errors on any logs (like compile.log, simulation.log, or .rpt files) to find the failure. "
        "Determine the root cause. If repairs are needed, use manage_retry_state to ensure we haven't looped too many times. "
        "Write diagnosis.json, repair_plan.json, and the final agent result JSON containing the routing instructions."
    )
    
    print("Starting Diagnosis & Router Agent...\n")
    
    # 4. Execute the agent
    response = agent.invoke({
        "messages": [HumanMessage(content=trigger_message)]
    })
    
    print("\n=== FINAL OUTPUT ===")
    
    # Extract the final message from the sequence
    final_message = response["messages"][-1].content
    print(final_message)