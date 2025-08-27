import os
import platform
import shlex
import subprocess
import requests
import json
import getpass
import time

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import torch
    from transformers import pipeline
except ImportError:
    torch = None
    pipeline = None

# --- ANSI Color Codes for better terminal UI ---
class colors:
    RESET = '\033[0m'
    WARNING = '\033[1;33m'
    INFO = '\033[1;34m'
    SUCCESS = '\033[1;32m'
    ERROR = '\033[1;31m'
    COMMAND = '\033[1;35m'
    PROMPT = '\033[1;36m'

# --- LLM Integration ---

def build_meta_prompt(prompt: str) -> str:
    """
    Creates a standardized meta-prompt to instruct the LLM.
    
    Args:
        prompt: The user's natural language input.

    Returns:
        A detailed instruction string for the LLM.
    """
    os_type = platform.system()
    return (
        "You are an expert natural language to shell command translator. "
        "Your task is to take a user's prompt and their operating system, and return ONLY the single, most appropriate shell command. "
        "For tasks requiring administrator privileges (like installing software), prefix the command with 'sudo'. "
        "Do not provide any explanation, preamble, or markdown formatting like ```bash ... ```. Just the raw command."
        f"\n\nUser's Operating System: {os_type}"
        f"\nUser's Prompt: \"{prompt}\""
        "\n\nCommand:"
    )

def clean_llm_response(text: str) -> str:
    """
    Cleans up common formatting issues from LLM responses.
    
    Args:
        text: The raw text response from the LLM.
        
    Returns:
        A cleaned, command-only string.
    """
    command = text.strip()
    # Remove markdown code blocks
    if command.startswith("```") and command.endswith("```"):
        command_lines = command.splitlines()
        if len(command_lines) > 1:
            command = ' '.join(command_lines[1:-1]) if len(command_lines) > 2 else command_lines[1]
        else:
             command = command.strip("`")

    # Remove backticks
    if command.startswith("`") and command.endswith("`"):
        command = command.strip("`")
    
    return command

def translate_with_gemini(prompt: str, api_key: str) -> str | None:
    """
    Translates a prompt into a shell command using Google's Gemini model.
    """
    if not genai:
        print(f"\n{colors.ERROR}Error:{colors.RESET} The 'google-generativeai' package is not installed.")
        return None
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        meta_prompt = build_meta_prompt(prompt)
        response = model.generate_content(
            meta_prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.0, max_output_tokens=100)
        )
        command = clean_llm_response(response.text)
        return command if command else None
    except Exception as e:
        print(f"\n{colors.ERROR}Error calling Gemini API:{colors.RESET} {e}")
        return None

def translate_with_local_llm(prompt: str, api_url: str, model_name: str) -> str | None:
    """
    Translates a prompt using a local LLM API (e.g., Ollama).
    """
    meta_prompt = build_meta_prompt(prompt)
    payload = {
        "model": model_name, 
        "prompt": meta_prompt,
        "stream": False,
        "options": {"temperature": 0.0}
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status() 
        data = response.json()
        command_text = data.get('response', '')
        command = clean_llm_response(command_text)
        return command if command else None
    except requests.exceptions.RequestException as e:
        print(f"\n{colors.ERROR}Error calling local LLM API:{colors.RESET} {e}")
        return None
    except json.JSONDecodeError:
        print(f"\n{colors.ERROR}Error:{colors.RESET} Failed to decode JSON response.")
        return None

def translate_with_transformer(prompt: str, pipe) -> str | None:
    """
    Translates a prompt using a local Hugging Face transformer model.
    """
    if not pipe:
        print(f"\n{colors.ERROR}Error:{colors.RESET} Transformer pipeline is not available.")
        return None
    try:
        meta_prompt = build_meta_prompt(prompt)
        sequences = pipe(
            meta_prompt,
            max_new_tokens=50,
            do_sample=False,
            num_return_sequences=1,
        )
        # The output is a list of dictionaries, we need to extract the generated text
        if sequences and isinstance(sequences, list) and 'generated_text' in sequences[0]:
             # The generated text includes the prompt, so we remove it
            full_text = sequences[0]['generated_text']
            command_text = full_text.replace(meta_prompt, '')
            command = clean_llm_response(command_text)
            return command if command else None
        return None
    except Exception as e:
        print(f"\n{colors.ERROR}Error during translation with transformer:{colors.RESET} {e}")
        return None


# --- Data Collection for Fine-Tuning ---

def log_training_pair(prompt: str, command: str):
    """Appends a prompt-completion pair to the training dataset."""
    dataset_file = "training_dataset.jsonl"
    data = {"prompt": prompt, "completion": command}
    try:
        with open(dataset_file, "a") as f:
            f.write(json.dumps(data) + "\n")
        print(f"{colors.INFO}Feedback logged to {dataset_file}{colors.RESET}")
    except IOError as e:
        print(f"{colors.ERROR}Could not write to dataset file: {e}{colors.RESET}")

# --- Command Execution ---

def execute_command(command: str, user_prompt: str) -> int:
    """
    Executes a shell command and uses user feedback to log training data.
    Returns the exit code of the command.
    """
    if not command:
        print(f"\n{colors.WARNING}Sorry, I couldn't translate that. Please try being more specific.{colors.RESET}")
        return 1 # Return a non-zero exit code for failure

    print(f"\nI am about to execute this command: {colors.COMMAND}{command}{colors.RESET}")
    
    if command.strip().startswith("sudo"):
        print(f"{colors.WARNING}This command requires administrator privileges.{colors.RESET}")

    try:
        # No confirmation needed for setup commands like install/pull
        if "install ollama" not in user_prompt and "pull" not in user_prompt and "pip install" not in command:
            confirm = input("Do you want to proceed? [y/n] ").lower().strip()
            if confirm != 'y':
                print("Execution cancelled.")
                return 1

        print(f"\n{colors.INFO}--- Command Output ---{colors.RESET}")
        needs_shell = '|' in command or '>' in command or '<' in command or '&' in command
        process_args = command if needs_shell else shlex.split(command)
        
        process = subprocess.Popen(
            process_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, shell=needs_shell, bufsize=1, universal_newlines=True
        )
        
        if process.stdout:
            for line in iter(process.stdout.readline, ''):
                print(line, end='', flush=True)
            process.stdout.close()
        
        return_code = process.wait()
        print(f"\n{colors.INFO}----------------------{colors.RESET}")

        if return_code == 0:
             if "install ollama" not in user_prompt and "pull" not in user_prompt and "pip install" not in command:
                feedback = input("Was this command correct and useful? [y/n] ").lower().strip()
                if feedback == 'y':
                    log_training_pair(user_prompt, command)
        else:
            print(f"\n{colors.ERROR}Command finished with exit code: {return_code}{colors.RESET}")
            if "install ollama" not in user_prompt and "pull" not in user_prompt and "pip install" not in command:
                print(f"{colors.WARNING}If you know the correct command, please enter it to improve the AI.{colors.RESET}")
                correction = input("Correct command (or press Enter to skip): ").strip()
                if correction:
                    log_training_pair(user_prompt, correction)
        
        return return_code

    except FileNotFoundError:
        print(f"\n{colors.ERROR}Error:{colors.RESET} Command not found: '{shlex.split(command)[0]}'")
        return 1
    except Exception as e:
        print(f"\n{colors.ERROR}An unexpected error occurred:{colors.RESET} {e}")
        return 1

# --- Local LLM Setup ---

def check_and_setup_ollama(model_name: str) -> bool:
    """
    Checks if Ollama is installed and if the specified model is available.
    """
    try:
        subprocess.run(["ollama", "--version"], capture_output=True, check=True)
        print(f"{colors.SUCCESS}Ollama is already installed.{colors.RESET}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{colors.WARNING}Ollama is not installed or not in your PATH.{colors.RESET}")
        os_type = platform.system()
        if os_type == "Linux":
            install_cmd = "curl -fsSL https://ollama.com/install.sh | sh"
            print(f"You can install it by running: {colors.COMMAND}{install_cmd}{colors.RESET}")
            if input("Run this command for you? [y/n] ").lower().strip() == 'y':
                if execute_command(install_cmd, "install ollama") == 0:
                     print(f"{colors.INFO}Please restart your terminal after installation.{colors.RESET}")
                else:
                     print(f"{colors.ERROR}Ollama installation failed.{colors.RESET}")
                return False
        return False

    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        if model_name not in result.stdout:
            print(f"{colors.WARNING}'{model_name}' model not found. I will download it now (this may take a while).{colors.RESET}")
            if execute_command(f"ollama pull {model_name}", f"pull {model_name} model") != 0:
                print(f"\n{colors.ERROR}Failed to pull '{model_name}'. Please check the model name and your internet connection.{colors.RESET}")
                print(f"{colors.INFO}You can find available models at https://ollama.com/library{colors.RESET}")
                return False
        else:
            print(f"{colors.SUCCESS}'{model_name}' model is available.{colors.RESET}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    return True

def check_and_setup_transformer() -> bool:
    """Checks if transformers and torch are installed and guides the user if not."""
    if torch and pipeline:
        print(f"{colors.SUCCESS}Transformers library is already installed.{colors.RESET}")
        return True
    
    print(f"{colors.WARNING}The 'transformers' and 'torch' libraries are required for this option.{colors.RESET}")
    if input("Do you want to install them now? [y/n] ").lower().strip() == 'y':
        install_command = "pip install transformers torch --break-system-packages"
        print(f"Running command: {colors.COMMAND}{install_command}{colors.RESET}")
        if execute_command(install_command, "install transformers") == 0:
            print(f"{colors.SUCCESS}Installation successful. Please restart the script.{colors.RESET}")
        else:
            print(f"{colors.ERROR}Installation failed. Please install 'transformers' and 'torch' manually.{colors.RESET}")
    return False

# --- Main Application Logic ---

def main():
    """The main function to configure and run the application loop."""
    print(f"\n{colors.SUCCESS}Welcome to the Natural Language Shell!{colors.RESET}")

    provider = ""
    while provider not in ['gemini', 'local', 'transformer']:
        choice = input(f"Choose an LLM provider:\n{colors.INFO}1. Gemini{colors.RESET}\n{colors.INFO}2. Ollama (Local Server){colors.RESET}\n{colors.INFO}3. Transformer (Local Model){colors.RESET}\nEnter choice (1, 2, or 3): ").strip()
        if choice == '1': provider = 'gemini'
        elif choice == '2': provider = 'local'
        elif choice == '3': provider = 'transformer'

    gemini_api_key, local_llm_url, local_model_name, transformer_pipe = None, None, "whiterabbitneo", None

    if provider == 'gemini':
        gemini_api_key = os.environ.get("API_KEY") or getpass.getpass("Please enter your Gemini API Key: ").strip()
        if not gemini_api_key:
            print(f"{colors.ERROR}No API key provided. Exiting.{colors.RESET}"); return
    elif provider == 'local':
        custom_model = input(f"Enter Ollama model name [{local_model_name}]: ").strip()
        if custom_model: 
            local_model_name = custom_model
        
        if not check_and_setup_ollama(local_model_name): return

        ip = input("Enter IP address [localhost]: ").strip() or "localhost"
        port = input("Enter port [11434]: ").strip() or "11434"
        local_llm_url = f"http://{ip}:{port}/api/generate"
    elif provider == 'transformer':
        if not check_and_setup_transformer(): return
        model_name = "distilgpt2" # A smaller model for quicker setup
        print(f"{colors.INFO}Loading transformer model '{model_name}'... (this might take a moment the first time){colors.RESET}")
        try:
            transformer_pipe = pipeline('text-generation', model=model_name)
            print(f"{colors.SUCCESS}Model loaded successfully.{colors.RESET}")
        except Exception as e:
            print(f"{colors.ERROR}Failed to load transformer model: {e}{colors.RESET}")
            return

    print("-" * 30)
    print(f"Using provider: {colors.INFO}{provider.capitalize()}{colors.RESET}")
    if provider != 'gemini':
        model_to_display = local_model_name if provider == 'local' else 'distilgpt2'
        print(f"Using model: {colors.INFO}{model_to_display}{colors.RESET}")
    print(f"{colors.SUCCESS}Now collecting feedback to build a fine-tuning dataset!{colors.RESET}")
    print("Type 'exit' or 'quit' to close.")

    while True:
        try:
            user_prompt = input(f"\n{colors.PROMPT}>{colors.RESET} ")
            if user_prompt.lower() in ["exit", "quit"]: break
            if not user_prompt: continue

            print(f"{colors.INFO}Translating prompt...{colors.RESET}")
            command_to_run = None
            if provider == 'gemini':
                command_to_run = translate_with_gemini(user_prompt, gemini_api_key)
            elif provider == 'local':
                command_to_run = translate_with_local_llm(user_prompt, local_llm_url, local_model_name)
            elif provider == 'transformer':
                command_to_run = translate_with_transformer(user_prompt, transformer_pipe)

            if command_to_run:
                execute_command(command_to_run, user_prompt)

        except (KeyboardInterrupt, EOFError):
            break
    print("\nExiting...")

if __name__ == "__main__":
    main()
