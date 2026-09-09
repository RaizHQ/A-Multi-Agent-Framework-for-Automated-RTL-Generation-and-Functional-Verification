# LangChain Environment Setup Guide

This guide provides step-by-step instructions to create a Python virtual environment named `env_langchain` and integrate LangChain with **OpenAI**, **Anthropic**, and **Google Gemini**.

---

## 1. Create and Activate the Virtual Environment

Open your terminal or terminal application and run the command matching your operating system:

### macOS / Linux (Bash/Zsh)
```bash
python3 -m venv env_langchain
source env_langchain/bin/activate
```

### Windows (Command Prompt - CMD)
```cmd
python -m venv env_langchain
env_langchain\Scripts\activate.bat
```

### Windows (PowerShell)
```powershell
# Optional: Run this if PowerShell blocks script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Activate the environment
.\env_langchain\Scripts\Activate.ps1
```
pip install -r requirements.txt
---

## 2. Install LangChain & Provider Libraries

Ensure your environment is active (you should see `(env_langchain)` at the start of your terminal prompt), then run:

```bash
pip install -U langchain langchain-openai langchain-anthropic langchain-google-genai
```

---

## 3. Set Up API Keys

Configure your API keys as environment variables. Replace the placeholders with your actual keys.

### macOS / Linux
```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export GEMINI_API_KEY="your-gemini-key"
```

### Windows (Command Prompt - CMD)
```cmd
set OPENAI_API_KEY=your-openai-key
set ANTHROPIC_API_KEY=your-anthropic-key
set GEMINI_API_KEY=your-gemini-key
```

### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY="your-openai-key"
$env:ANTHROPIC_API_KEY="your-anthropic-key"
$env:GEMINI_API_KEY="your-gemini-key"
```

---

## 4. Implementation Code

Create a file named `app.py` and paste the following Python code to verify the integrations:

```python
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Initialize models with recommended defaults
openai_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
anthropic_model = ChatAnthropic(model="claude-3-5-haiku-latest", temperature=0.7)
gemini_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# 2. Build a reusable chat prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

# 3. Create execution chains
openai_chain = prompt | openai_model
anthropic_chain = prompt | anthropic_model
gemini_chain = prompt | gemini_model

# 4. Helper function to safely execute and log responses
def test_model(name, chain, user_input):
    print(f"\n--- Testing {name} ---")
    try:
        response = chain.invoke({"input": user_input})
        print(response.content)
    except Exception as e:
        print(f"Error testing {name}: {e}")

if __name__ == "__main__":
    user_query = "Give me a one-sentence fun fact about space."
    
    # Run tests across all providers
    test_model("OpenAI (GPT-4o-mini)", openai_chain, user_query)
    test_model("Anthropic (Claude 3.5 Haiku)", anthropic_chain, user_query)
    test_model("Google Gemini (Gemini 2.5 Flash)", gemini_chain, user_query)
```

---

## 5. Run the Script

Execute the test pipeline with the following command:

```bash
python app.py
```
