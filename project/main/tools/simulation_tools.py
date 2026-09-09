# project\main\tools\simulation_tools.py
import json
import subprocess
import shutil
from pathlib import Path
from langchain_core.tools import tool

# Resolves to the 'project' root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

@tool
def check_tool_installed(tool_name: str) -> str:
    """
    Checks if a CLI tool (e.g., 'iverilog', 'python', 'verilator') is installed on the host OS.
    Returns the absolute path and version if found.
    """
    try:
        tool_path = shutil.which(tool_name)
        if not tool_path:
            return json.dumps({
                "tool": tool_name,
                "installed": False,
                "path": None,
                "version": None
            })
            
        # Attempt to get the version string (most tools support --version or -V)
        version_output = "Unknown"
        for flag in ["--version", "-V", "-v"]:
            try:
                result = subprocess.run(
                    [tool_path, flag], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                if result.returncode == 0:
                    output = (result.stdout or result.stderr).strip()
                    if output:
                        # Grab just the first line to avoid massive dumps
                        version_output = output.split('\n')[0]
                        break
            except Exception:
                continue

        return json.dumps({
            "tool": tool_name,
            "installed": True,
            "path": tool_path,
            "version": version_output
        })
    except Exception as e:
        return json.dumps({"error": f"Failed to check tool {tool_name}: {str(e)}"})

@tool
def execute_cli_command(command: str, relative_cwd: str = ".", timeout_sec: int = 60) -> str:
    """
    Executes a shell command in a specified working directory relative to the project root.
    Enforces a strict timeout and captures stdout, stderr, and the exit code.
    Args:
        command: The shell command to run (e.g., 'iverilog -o sim.vvp src/*.v').
        relative_cwd: The directory to run the command in, relative to project root. Default is root.
        timeout_sec: Maximum execution time in seconds.
    """
    work_dir = BASE_DIR / relative_cwd
    
    if not work_dir.exists():
        return json.dumps({"error": f"Working directory does not exist: {relative_cwd}"})

    try:
        result = subprocess.run(
            command,
            cwd=str(work_dir),
            shell=True,          # Required to support globs like src/*.v and output redirection
            capture_output=True,
            text=True,
            timeout=timeout_sec
        )
        
        return json.dumps({
            "command_executed": command,
            "working_directory": relative_cwd,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "timed_out": False
        })
    except subprocess.TimeoutExpired as e:
        return json.dumps({
            "command_executed": command,
            "working_directory": relative_cwd,
            "exit_code": -1,
            "stdout": e.stdout.decode('utf-8') if e.stdout else "",
            "stderr": e.stderr.decode('utf-8') if e.stderr else "",
            "timed_out": True,
            "error_msg": f"Command exceeded {timeout_sec} seconds and was killed."
        })
    except Exception as e:
        return json.dumps({"error": f"Failed to execute command: {str(e)}"})

@tool
def ensure_directory(dir_path: str) -> str:
    """
    Creates a directory (and all necessary parent directories) relative to the project root.
    """
    full_path = BASE_DIR / dir_path
    try:
        full_path.mkdir(parents=True, exist_ok=True)
        return json.dumps({
            "directory": dir_path,
            "status": "created_or_exists"
        })
    except Exception as e:
        return json.dumps({"error": f"Failed to create directory {dir_path}: {str(e)}"})