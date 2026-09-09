# project/main/main.py
import sys

from controllers.execute_prompt_generator import execute_prompt_generator

if __name__ == "__main__":
    print("Starting FIR Generator Pipeline...")
    execute_prompt_generator()
    print("Pipeline Finished.")