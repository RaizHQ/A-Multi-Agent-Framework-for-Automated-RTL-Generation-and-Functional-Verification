# A-Multi-Agent-Framework-for-Automated-RTL-Generation-and-Functional-Verification
An autonomous, multi-agent AI framework that translates natural language prompts into fully verified Verilog RTL. Built with Python and LangChain, it utilizes a self-correcting feedback loop to automate hardware generation, headless simulation, and error debugging for FPGAs.


This project introduces a closed-loop, multi-agent AI system designed to absorb repetitive bottlenecks in modern VLSI design workflows. By leveraging specialized LLM agents, the framework translates human-readable requirements into syntactically valid and functionally verified hardware description logic without manual intervention.  

Autonomous Workflow: Orchestrates Specification, RTL, Testbench, and Verification agents to design and test an 8-tap FIR filter entirely from natural language prompts.  

Self-Correcting Feedback: Intercepts compilation errors and simulation mismatches via headless execution, dynamically routing diagnostic data back to the agents to fix bugs autonomously.  

Tech Stack: Python, LangChain, LLM APIs (Gemini, DeepSeek), and Altera Quartus II ModelSim.  

Hardware Target: Developed and verified for the ALTERA Cyclone II EP2C5T144 FPGA, establishing a scalable foundation for future Digital Signal Processors and RISC-V architectures
