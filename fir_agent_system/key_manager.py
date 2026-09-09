import os
import time
import itertools
import threading
from dotenv import load_dotenv
from pydantic import SecretStr

# --- Dynamic Imports (Gracefully handles missing packages) ---
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

try:
    from langchain_deepseek import ChatDeepSeek
except ImportError:
    ChatDeepSeek = None

try:
    from langchain_mistralai import ChatMistralAI
except ImportError:
    ChatMistralAI = None


# Load .env variables
load_dotenv()

def _mask_key(key: str) -> str:
    """Masks key for safe printing in terminal (e.g., sk-a...ef56)."""
    if len(key) <= 8:
        return "****"
    return f"{key[:4]}...{key[-4:]}"

def _test_key(model) -> bool:
    """Performs a quick 1-token check to verify if the key works."""
    try:
        model.invoke("hi")
        return True
    except Exception as e:
        return False

def _build_model(provider: str, api_key: str, temperature: float = 0.1):
    """Instantiates the specific provider LLM model."""
    if provider == "GEMINI":
        if not ChatGoogleGenerativeAI: return None
        return ChatGoogleGenerativeAI(
            model="gemini-3.7-flash", 
            temperature=temperature, 
            api_key=SecretStr(api_key)
        )
    elif provider == "ANTHROPIC":
        if not ChatAnthropic: return None
        return ChatAnthropic(
            model_name="claude-3-5-sonnet-20241022",
            temperature=temperature, 
            api_key=SecretStr(api_key),
            timeout=None,
            stop=None
        )
    
    elif provider == "GROQ":
        if not ChatGroq: return None
        return ChatGroq(
            model="llama-3.3-70b-versatile", 
            temperature=temperature, 
            api_key=SecretStr(api_key)
        )
    elif provider == "DEEPSEEK":
        if not ChatDeepSeek: return None
        return ChatDeepSeek(
            model="deepseek-v4-pro", 
            temperature=temperature, 
            api_key=SecretStr(api_key)
        )
    elif provider == "MISTRAL":
        if not ChatMistralAI: return None
        return ChatMistralAI(
            model_name="codestral-latest",
            temperature=temperature, 
            api_key=SecretStr(api_key)
        )
    return None

# --- Startup Initialization & Key Validation ---
valid_models = []

print("\n--- Initializing Key Manager & Validating Keys ---")

for env_var, value in os.environ.items():
    if not value or not value.strip():
        continue
        
    provider = None
    if env_var.startswith("GEMINI_KEY"): provider = "GEMINI"
    elif env_var.startswith("ANTHROPIC_KEY"): provider = "ANTHROPIC"
    elif env_var.startswith("GROQ_KEY"): provider = "GROQ"
    elif env_var.startswith("DEEPSEEK_KEY"): provider = "DEEPSEEK"
    elif env_var.startswith("MISTRAL_KEY"): provider = "MISTRAL"
        
    if provider:
        masked = _mask_key(value.strip())
        print(f"Testing {env_var} ({provider} - {masked})...", end=" ", flush=True)
        
        model_instance = _build_model(provider, value.strip())
        if model_instance is None:
            print(f"[!] SKIPPED - langchain-{provider.lower()} package not installed")
        elif _test_key(model_instance):
            valid_models.append(model_instance)
            print("[✓] VALID")
        else:
            print("[X] INVALID - Skipping")
            
        # DELAY ADDED HERE: Wait 3 seconds between testing each key to prevent startup rate-limiting
        time.sleep(3) 

if not valid_models:
    raise RuntimeError("[!] No valid API keys found in your .env file. Please check your credentials.")

print(f"--- Key Manager Ready: {len(valid_models)} working key(s) in active rotation ---\n")

# --- Thread-Safe Round Robin ---
_cycle = itertools.cycle(valid_models)
_lock = threading.Lock()

def get_llm(temperature: float = 0.1):
    """Returns the next validated model in the round-robin sequence."""
    with _lock:
        model = next(_cycle)
        model.temperature = temperature
        return model

# --- Graceful Error Handler & Auto-Retry ---
def safe_execute(func, *args, max_retries=3, **kwargs):
    """
    Wraps any agent execution to catch API errors, suppress ugly tracebacks,
    and automatically retry with the next key in the rotation.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            # Attempt to execute the agent function
            return func(*args, **kwargs)
        except Exception as e:
            attempt += 1
            error_msg = str(e)
            
            # Cleanly print the error without tracebacks
            print(f"\n[!] API Error Encountered (Attempt {attempt}/{max_retries}):")
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print(" -> Rate Limit Exceeded (429).")
            else:
                print(f" -> {error_msg.splitlines()[0]}") # Only prints the top line of the error
                
            if attempt < max_retries:
                print(f" -> Retrying in 5 seconds with the NEXT available API key in rotation...\n")
                time.sleep(5)
            else:
                print(" -> Max retries reached. Moving to the next step or aborting.")
                return {"success": False, "message": "Failed due to repeated API errors.", "feasible": False}