import os
import subprocess
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()



# Initialize the Gemini Model
chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
rtl_agent = create_agent(model=chat_model, tools=[])
tb_agent = create_agent(model=chat_model, tools=[])

# ---------------------------------------------------------
# 1. RTL AGENT: Generate the Hardware Module
# ---------------------------------------------------------
rtl_prompt = """
Write a simple Verilog module for a 2-input AND gate. 
Module name: and_gate
Inputs: a, b
Output: y
Output ONLY raw Verilog code. Do not include markdown formatting, backticks, or explanations.
"""

print("-> 1. RTL Agent generating design...")
rtl_response = rtl_agent.invoke({"messages": [HumanMessage(content=rtl_prompt)]})
verilog_code = rtl_response["messages"][-1].content.strip()

with open("design.v", "w") as f:
    f.write(verilog_code)
print("   [+] Saved design.v")

# ---------------------------------------------------------
# 2. TESTBENCH AGENT: Generate the Verification Environment
# ---------------------------------------------------------
tb_prompt = f"""
You are a hardware verification engineer. Write a self-checking Verilog testbench for the following module:

{verilog_code}

Strict Requirements:
1. The testbench module MUST be named `tb_design`.
2. Iterate through all possible input combinations.
3. If any output is incorrect, execute $display("TEST FAILED");
4. If all tests pass, execute $display("TEST PASSED"); at the end.
5. You MUST include $finish; at the very end of the test sequence to stop the headless simulator.
6. Output ONLY raw Verilog code. Do not include markdown formatting, backticks, or explanations.
7. Do NOT use SystemVerilog features.
8. Do not use inline loop declarations like for (int i = 0; ... ). You must declare integer i; at the top of the module or initial block before any procedural assignments.
9. Do not declare reg variables inside a for loop.
"""

print("-> 2. Testbench Agent generating self-checking testbench...")
tb_response = tb_agent.invoke({"messages": [HumanMessage(content=tb_prompt)]})
testbench_code = tb_response["messages"][-1].content.strip()

with open("tb_design.v", "w") as f:
    f.write(testbench_code)
print("   [+] Saved tb_design.v")

# ---------------------------------------------------------
# 3. VERIFICATION AGENT: Execute ModelSim Headlessly
# ---------------------------------------------------------
print("-> 3. Running ModelSim Compilation & Simulation...")

# Create work library (ignoring errors if it already exists)
subprocess.run(["vlib", "work"], capture_output=True)

# Compile both generated files
comp = subprocess.run(["vlog", "design.v", "tb_design.v"], capture_output=True, text=True)

if comp.returncode != 0:
    print("\n❌ COMPILE ERROR:")
    print(comp.stdout)
else:
    # Run simulation
    sim = subprocess.run(["vsim", "-c", "-do", "run -all; quit -f", "tb_design"], 
                         capture_output=True, text=True, timeout=10)
    
    if "TEST PASSED" in sim.stdout:
        print("\n✅ CLOSED-LOOP SUCCESS: RTL and Testbench autonomously generated and verified!")
    elif "TEST FAILED" in sim.stdout:
        print("\n⚠️ LOGIC ERROR: Simulation ran, but the testbench reported a failure.")
        print(sim.stdout)
    else:
        print("\n❌ SIMULATION TIMED OUT OR CRASHED.")
        print(sim.stdout)