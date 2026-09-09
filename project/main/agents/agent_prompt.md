Similarly, i need to make the agent code for: diagnosis_router_agent

where:

project\main\agents\diagnosis_router_agent.py
project\data\md\agent_prompts\diagnosis_router_agent_prompt.md

i have the python file for langchain agent in above location. its prompt is saved in a .md file. the prompt specifies to take some input files from the  file paths mentioned in the prompt. so i need to input those files to the agent and generate the outputs in the defined location in prompt.

 Assess what are the tools this agent need to use to implement the prompt. 
 list those tools.
 If it require additional tools like scipy, cli access for installed apps, etc, then generate codes for those tools.  

 tools will be saved in the location: 

 project\main\tools\ 

 after identifying and writing codes for the tools, update the agent code.



==========================================================================================

quartus_implementation_agent_prompt.md:

# AGENT: Failure Diagnosis and Repair Router

You are the senior hardware verification/debug orchestrator.

INPUT:
- all JSON manifests/results under data/json/
- simulation logs/results
- Quartus reports/results
- RTL source
- verification source
- original requirements

TASK:
Determine the most likely root cause, confidence, affected artifact and next
agent. Never make a design requirement disappear to obtain PASS.

ROUTING:
- requirement contradiction/filter-edge issue -> specification validator
- tap/beta/coefficient/Q/accumulator issue -> FIR/DSP agent
- resource/timing/architecture issue -> architecture agent
- syntax/signedness/RTL behavior -> RTL generator
- reference model/testbench/scoreboard issue -> verification agent
- missing simulator/environment/command issue -> execution agent
- Quartus project/device/constraint/timing issue -> Quartus agent
- ambiguous or unsafe automatic decision -> BLOCKED/manual review

Use bounded retries. Preserve previous artifacts; never overwrite evidence.
OUTPUT:
- data/json/diagnosis.json
- data/json/repair_plan.json
- data/json/agent_results/diagnosis.json

Return JSON only with:
{
  "status": "REPAIR_REQUIRED|BLOCKED|PASS",
  "root_cause": "...",
  "confidence": "high|medium|low",
  "next_agent": "spec_validation|fir_design|architecture|rtl|verification|simulation|quartus|manual",
  "repair_instructions": ["..."],
  "files_to_review": ["..."],
  "reason": "..."
}



====================================================================================================


## Tools:
project\main\tools\file_tools.py:

from pathlib import Path
from langchain_core.tools import tool

# Resolves to the 'project' root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

@tool
def read_file(file_path: str) -> str:
    """Reads a file from the given path (relative to the project root) and returns its content."""
    full_path = BASE_DIR / file_path
    try:
        with open(full_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"

@tool
def write_file(file_path: str, content: str) -> str:
    """Writes content to the specified file path (relative to the project root). Creates directories if needed."""
    full_path = BASE_DIR / file_path
    try:
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing to {file_path}: {str(e)}"