# project\main\agents\verification_agent.py
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

# Import New Verification Tools
from main.tools.verification_tools import (
    list_directory,
    generate_stimulus_vectors,
    calculate_scoreboard_tolerances
)

PROMPT_PATH = BASE_DIR / "data" / "md" / "agent_prompts" / "verification_agent_prompt.md"

def create_verification_agent():
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

    # 2. Define tools - Merging standard IO, directory inspection, and DSP verification math
    tools = [
        read_file, 
        write_file, 
        list_directory,
        generate_stimulus_vectors,
        calculate_scoreboard_tolerances,
        PythonREPLTool() # Essential for the agent to test its own Python reference model before saving
    ]

    # 3. Create the agent using the modern LangChain API
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt 
    )

    return agent

if __name__ == "__main__":
    agent = create_verification_agent()
    
    trigger_message = (
        "Begin the verification environment generation process. "
        "Use the list_directory tool to discover RTL sources and coefficient files. "
        "Read the necessary JSON specs, generate the Python reference model, the HDL testbench, "
        "and the simulation manifest. Write all required files and return the final verification JSON."
    )
    
    print("Starting Verification Agent...\n")
    
    # 4. Execute the agent
    response = agent.invoke({
        "messages": [HumanMessage(content=trigger_message)]
    })
    
    print("\n=== FINAL OUTPUT ===")
    
    # Extract the final message from the sequence
    final_message = response["messages"][-1].content
    print(final_message)