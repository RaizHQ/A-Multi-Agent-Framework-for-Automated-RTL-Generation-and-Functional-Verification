import os
import json
import subprocess
import sys

def execute_prompt_generator():
    # 1. Setup absolute paths based on the current file's location
    # controllers_dir = project/main/controllers
    controllers_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to requirements.json: project/data/json/requirements.json
    json_path = os.path.join(controllers_dir, '..', '..', 'data', 'json', 'requirements.json')
    json_path = os.path.normpath(json_path)

    # Path to prompt_generators folder: project/main/prompt_generators
    generators_dir = os.path.join(controllers_dir, '..', 'prompt_generators')
    generators_dir = os.path.normpath(generators_dir)

    # 2. Read the JSON file
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        sys.exit(1)

    # 3. Extract the 'experience' value (default to basic if missing)
    experience = data.get("experience", "basic").strip().lower()

    # 4. Map the experience value to the correct script file
    # Note: Maps both 'advance' and 'advanced' to advance.py to prevent typos
    script_mapping = {
        'basic': 'basic.py',
        'advance': 'advance.py',
        'advanced': 'advance.py',
        'expert': 'expert.py'
    }

    script_filename = script_mapping.get(experience)

    if not script_filename:
        print(f"Error: Unknown experience level '{experience}' in JSON.")
        sys.exit(1)

    # 5. Build the full path to the chosen generator script
    target_script_path = os.path.join(generators_dir, script_filename)

    if not os.path.exists(target_script_path):
        print(f"Error: The target script was not found at {target_script_path}")
        sys.exit(1)

    # 6. Execute the chosen script
    print(f"Mode Controller: Detected experience level '{experience}'.")
    print(f"Mode Controller: Executing {script_filename}...\n" + "-"*40)
    
    try:
        # sys.executable ensures it uses the same Python environment currently running
        result = subprocess.run([sys.executable, target_script_path], check=True)
        print("-" * 40 + "\nMode Controller: Execution completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: The script {script_filename} failed with exit code {e.returncode}.")
        sys.exit(e.returncode)

if __name__ == "__main__":
    execute_prompt_generator()