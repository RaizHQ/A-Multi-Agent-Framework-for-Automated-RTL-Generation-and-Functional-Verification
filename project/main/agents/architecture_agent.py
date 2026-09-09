# project\main\agents\architecture_agent.py
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

# Import New Architecture Tools
from main.tools.architecture_tools import (
    analyze_clock_domain,
    estimate_hardware_resources
)

PROMPT_PATH = BASE_DIR / "data" / "md" / "agent_prompts" / "architecture_agent_prompt.md"

def create_architecture_agent():
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

    # 2. Define tools - Merging our hardware estimation tools with standard File IO & REPL
    tools = [
        read_file, 
        write_file, 
        analyze_clock_domain,
        estimate_hardware_resources,
        PythonREPLTool() # Kept as a fallback for any dynamic constraints math
    ]

    # 3. Create the agent using the modern LangChain API
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt 
    )

    return agent

if __name__ == "__main__":
    agent = create_architecture_agent()
    
    trigger_message = (
        "Begin the architecture planning process. Read the required JSON inputs, "
        "analyze the clock constraints, select the optimal DSP architecture, "
        "estimate the resource utilization, write the timing and interface specs, "
        "and return the final architecture agent result JSON."
    )
    
    print("Starting Architecture Agent...\n")
    
    # 4. Execute the agent directly using messages
    response = agent.invoke({
        "messages": [HumanMessage(content=trigger_message)]
    })
    
    print("\n=== FINAL OUTPUT ===")
    
    # Extract the final message from the sequence
    final_message = response["messages"][-1].content
    print(final_message)