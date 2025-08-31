import os
import platform
import shlex
import subprocess
import requests
import json
import getpass
import time
import re
import pty
import asyncio
import select

try:
    import google.generativeai as genai
except ImportError:
    # Set a flag or a dummy class if the import fails
    genai = None

# --- ANSI Color Codes for better terminal UI ---
class colors:
    RESET = '\033[0m'
    WARNING = '\033[1;33m'
    INFO = '\033[1;34m'
    SUCCESS = '\033[1;32m'
    ERROR = '\033[1;31m'
    COMMAND = '\033[1;35m'
    PROMPT = '\033[1;36m'
    ASSISTANT = '\033[1;32m'
    METASPLOIT = '\033[1;31m' # For Metasploit-specific output
    WAPITI = '\033[1;38;5;208m' # For Wapiti-specific output (Orange)

# --- LLM Integration & System Prompts ---

# System prompt for the general AI assistant
ASSISTANT_SYSTEM_PROMPT = (
    "You are an expert AI shell assistant. Your goal is to help the user accomplish their tasks by "
    "providing explanations, suggestions, and shell commands. The user is interacting with you through a special shell. "
    "When you provide a shell command that the user can execute, you MUST enclose it in a ```bash ... ``` markdown block. "
    "Be conversational and helpful. Break down complex tasks into steps. You can suggest tools and workflows. "
    f"The user's operating system is: {platform.system()}."
)

# System prompt specifically for the Metasploit assistant
METASPLOIT_SYSTEM_PROMPT = (
    "You are a world-class cybersecurity expert and penetration testing assistant. The user is currently inside the Metasploit Framework console (`msfconsole`). "
    "Your primary goal is to help the user conduct their penetration test effectively and safely. "
    "Provide guidance, explain concepts, and suggest the exact `msfconsole` commands to achieve their goals. "
    "When you provide a command for the user to execute, you MUST enclose it in a ```bash ... ``` markdown block. "
    "Example commands include `search cve:2021 type:exploit`, `use exploit/windows/smb/ms17_010_eternalblue`, `set RHOSTS 10.10.1.5`, `run`, etc. "
    "Always prioritize ethical considerations and user safety. Be conversational and act as a senior penetration tester mentoring a junior."
)

# New system prompt specifically for the Wapiti assistant
WAPITI_SYSTEM_PROMPT = (
    "You are a world-class web application security expert. The user is in a shell environment with the `wapiti` tool available. "
    "Your primary goal is to help the user scan web applications for vulnerabilities effectively. "
    "Provide guidance, explain web vulnerabilities (like XSS, SQLi, LFI), and suggest the exact `wapiti` commands to perform scans. "
    "When you provide a command for the user to execute, you MUST enclose it in a ```bash ... ``` markdown block. "
    "Example commands include `wapiti -u http://example.com`, `wapiti -u http://test.com -m xss,sqli --scope domain`, `wapiti -u http://vulnerable.site -x http://vulnerable.site/logout`. "
    "Always remind the user to only scan applications they have explicit permission to test. Be conversational and act as a senior security analyst."
)


def build_translator_meta_prompt(prompt: str) -> str:
    """
    Creates a standardized meta-prompt to instruct the LLM for translator mode.
    """
    os_type = platform.system()
    return (
        "You are an expert natural language to shell command translator. "
        "Your task is to take a user's prompt and their operating system, and return ONLY the single, most appropriate shell command. "
        "For tasks requiring administrator privileges (like installing software), prefix the command with 'sudo'. "
        "Do not provide any explanation, preamble, or markdown formatting. Just the raw command."
        f"\n\nUser's Operating System: {os_type}"
        f"\nUser's Prompt: \"{prompt}\""
        "\n\nCommand:"
    )

def clean_llm_response(text: str) -> str:
    """
    Cleans up common formatting issues from LLM responses for translator mode.
    """
    command = text.strip()
    # Remove markdown code blocks
    if command.startswith("```") and command.endswith("```"):
        command_lines = command.splitlines()
        if len(command_lines) > 1:
            # Handle cases like ```bash\ncommand\n```
            command = ' '.join(line for line in command_lines[1:-1] if line.strip())
        else:
             command = command.strip("`")
    # Remove backticks
    if command.startswith("`") and command.endswith("`"):
        command = command.strip("`")
    return command

def extract_command_from_response(text: str) -> str | None:
    """
    Extracts a shell command from a markdown code block in the assistant's response.
    """
    # Pattern to find ```bash ... ``` blocks
    match = re.search(r"```bash\n(.*?)\n```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def get_gemini_response(prompt: str, api_key: str, mode: str, system_prompt: str = ASSISTANT_SYSTEM_PROMPT, chat_session=None) -> tuple[str | None, any]:
    """
    Gets a response from Google's Gemini model. Returns the response text and the updated chat session.
    """
    if not genai:
        print(f"\n{colors.ERROR}Error:{colors.RESET} The 'google-generativeai' package is not installed.")
        return None, chat_session
    try:
        genai.configure(api_key=api_key)
        if mode == 'translator':
            model = genai.GenerativeModel('gemini-1.5-flash')
            meta_prompt = build_translator_meta_prompt(prompt)
            response = model.generate_content(
                meta_prompt,
                generation_config=genai.types.GenerationConfig(temperature=0.0, max_output_tokens=100)
            )
            return clean_llm_response(response.text), chat_session
        else: # assistant, metasploit, or wapiti
            if chat_session is None:
                model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
                chat_session = model.start_chat(history=[])
            response = chat_session.send_message(prompt)
            return response.text, chat_session
    except Exception as e:
        print(f"\n{colors.ERROR}Error calling Gemini API:{colors.RESET} {e}")
        return None, chat_session

def get_local_llm_response(prompt: str, api_url: str, model_name: str, mode: str, system_prompt: str = ASSISTANT_SYSTEM_PROMPT, history: list | None = None) -> str | None:
    """
    Gets a response from a local LLM API.
    """
    if history is None:
        history = []
        
    if mode == 'translator':
        meta_prompt = build_translator_meta_prompt(prompt)
        payload = {"model": model_name, "prompt": meta_prompt, "stream": False, "options": {"temperature": 0.0}}
    else: # assistant, metasploit, or wapiti
        full_prompt = f"<|system|>\n{system_prompt}\n"
        for turn in history:
            full_prompt += f"<|user|>\n{turn['user']}\n<|assistant|>\n{turn['assistant']}\n"
        full_prompt += f"<|user|>\n{prompt}\n<|assistant|>"
        payload = {"model": model_name, "prompt": full_prompt, "stream": False, "options": {"temperature": 0.2}}

    try:
        response = requests.post(api_url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        if 'error' in data:
            print(f"\n{colors.ERROR}Ollama server error:{colors.RESET} {data['error']}")
            return None
        response_text = data.get('response', '')
        return clean_llm_response(response_text) if mode == 'translator' else response_text
    except requests.exceptions.RequestException as e:
        print(f"\n{colors.ERROR}Error calling local LLM API:{colors.RESET} {e}")
        return None
    except json.JSONDecodeError:
        print(f"\n{colors.ERROR}Error:{colors.RESET} Failed to decode JSON response.")
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
def execute_command(command: str, user_prompt: str):
    """
    Executes a general shell command and uses user feedback to log training data.
    """
    if not command:
        print(f"\n{colors.WARNING}No command to execute.{colors.RESET}")
        return

    print(f"\nI am about to execute this command: {colors.COMMAND}{command}{colors.RESET}")
    if command.strip().startswith("sudo"):
        print(f"{colors.WARNING}This command requires administrator privileges.{colors.RESET}")

    try:
        confirm = input("Do you want to proceed? [y/n] ").lower().strip()
        if confirm != 'y':
            print("Execution cancelled.")
            return

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
            feedback = input("Was this command correct and useful? [y/n] ").lower().strip()
            if feedback == 'y':
                log_training_pair(user_prompt, command)
        else:
            print(f"\n{colors.ERROR}Command finished with exit code: {return_code}{colors.RESET}")
            print(f"{colors.WARNING}If you know the correct command, please enter it to improve the AI.{colors.RESET}")
            correction = input("Correct command (or press Enter to skip): ").strip()
            if correction:
                log_training_pair(user_prompt, correction)

    except FileNotFoundError:
        print(f"\n{colors.ERROR}Error:{colors.RESET} Command not found: '{shlex.split(command)[0]}'")
    except Exception as e:
        print(f"\n{colors.ERROR}An unexpected error occurred:{colors.RESET} {e}")

# --- Local LLM Setup ---
def get_available_memory() -> float:
    if platform.system() == "Linux":
        try:
            with open('/proc/meminfo', 'r') as mem:
                for line in mem:
                    if 'MemAvailable' in line:
                        return int(line.split()[1]) / (1024 * 1024)
        except FileNotFoundError: return 0.0
    return 4.0

def check_ollama_server_health(ip: str, port: str) -> bool:
    try:
        response = requests.get(f"http://{ip}:{port}", timeout=5)
        return response.status_code == 200 and "Ollama is running" in response.text
    except requests.exceptions.RequestException:
        return False

def check_and_setup_ollama(model_name: str, model_size_gb: float) -> bool:
    if model_size_gb > 0:
        available_memory = get_available_memory()
        if available_memory > 0 and available_memory < model_size_gb:
            print(f"\n{colors.ERROR}Error:{colors.RESET} Not enough memory for '{model_name}'.")
            print(f"Requires ~{model_size_gb:.1f} GB, have ~{available_memory:.1f} GB.")
            return False
    try:
        subprocess.run(["ollama", "--version"], capture_output=True, check=True, text=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{colors.WARNING}Ollama is not installed or not in your PATH.{colors.RESET}")
        return False
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        if model_name not in result.stdout:
            print(f"{colors.WARNING}'{model_name}' model not found. Pulling now...{colors.RESET}")
            subprocess.run(["ollama", "pull", model_name], check=True)
            print(f"\n{colors.SUCCESS}Successfully downloaded '{model_name}'.{colors.RESET}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"\n{colors.ERROR}Error:{colors.RESET} Could not connect to Ollama server.")
        return False
    return True

# --- Application Loops ---
def translator_loop(provider, config):
    """Main loop for the direct command translator."""
    print("\n--- Command Translator Mode ---")
    print("Enter a prompt, and I'll give you a shell command.")
    print("Type 'exit' or 'quit' to close.")
    
    while True:
        user_prompt = input(f"\n{colors.PROMPT}>{colors.RESET} ")
        if user_prompt.lower() in ["exit", "quit"]: break
        if not user_prompt: continue

        print(f"{colors.INFO}Translating prompt...{colors.RESET}")
        command_to_run = None
        if provider == 'gemini':
            command_to_run, _ = get_gemini_response(user_prompt, config['api_key'], 'translator')
        else: # local
            if check_ollama_server_health(config['ip'], config['port']):
                command_to_run = get_local_llm_response(user_prompt, config['url'], config['model'], 'translator')
            else:
                print(f"\n{colors.ERROR}Ollama server is not responding.{colors.RESET}")

        if command_to_run:
            execute_command(command_to_run, user_prompt)

def assistant_loop(provider, config):
    """Main loop for the conversational AI assistant."""
    print("\n--- AI Assistant Mode ---")
    print("Ask me anything, or describe a task. I can explain concepts or provide commands.")
    print("Type 'exit' or 'quit' to close.")

    gemini_chat_session = None
    local_history = []

    while True:
        user_prompt = input(f"\n{colors.PROMPT}You: {colors.RESET}")
        if user_prompt.lower() in ["exit", "quit"]: break
        if not user_prompt: continue
        
        print(f"{colors.INFO}Assistant is thinking...{colors.RESET}")
        assistant_response = None
        if provider == 'gemini':
            assistant_response, gemini_chat_session = get_gemini_response(user_prompt, config['api_key'], 'assistant', chat_session=gemini_chat_session)
        else: # local
            assistant_response = get_local_llm_response(user_prompt, config['url'], config['model'], 'assistant', history=local_history)
            if assistant_response:
                local_history.append({"user": user_prompt, "assistant": assistant_response})
        
        if assistant_response:
            print(f"\n{colors.ASSISTANT}Assistant:{colors.RESET}\n{assistant_response}")
            command_to_run = extract_command_from_response(assistant_response)
            if command_to_run:
                execute_command(command_to_run, user_prompt)

async def pty_loop_base(provider, config, tool_name: str, tool_color: str, system_prompt: str, start_command: list):
    """
    A generic base function for running a tool in a pseudoterminal with AI assistance.
    """
    print(f"\n--- {tool_name.capitalize()} Assistant Mode ---")
    print(f"Starting a shell for {tool_name} tasks.")
    print(f"To ask the AI for commands, start your prompt with a '{colors.PROMPT}?{colors.RESET}'. Example: {colors.PROMPT}? scan example.com for xss{colors.RESET}")
    print(f"To exit, type '{colors.COMMAND}exit{colors.RESET}' at the shell prompt.")

    pid, master_fd = pty.fork()

    if pid == 0:  # Child process
        try:
            os.execvp(start_command[0], start_command)
        except FileNotFoundError:
            print(f"{colors.ERROR}Error: '{start_command[0]}' not found.{colors.RESET}")
            print(f"Please ensure it is installed and in your PATH.")
            os._exit(1)
    else:  # Parent process
        loop = asyncio.get_event_loop()
        gemini_chat_session = None
        local_history = []

        os.set_blocking(master_fd, False)
        os.set_blocking(0, False)

        def handle_user_input():
            try:
                user_data = os.read(0, 1024)
                if user_data:
                    user_input = user_data.decode().strip()
                    if user_input.startswith('?'):
                        handle_ai_interaction(user_input[1:].strip())
                    else:
                        os.write(master_fd, user_data)
            except (BlockingIOError, InterruptedError):
                pass

        def handle_tool_output():
            try:
                tool_data = os.read(master_fd, 1024)
                if tool_data:
                    print(f"{tool_color}{tool_data.decode()}{colors.RESET}", end='', flush=True)
                else:
                    loop.stop()
            except (BlockingIOError, InterruptedError):
                pass
        
        def handle_ai_interaction(user_prompt):
            nonlocal gemini_chat_session, local_history
            print(f"\n{colors.INFO}Assistant is thinking...{colors.RESET}")
            assistant_response = None
            if provider == 'gemini':
                assistant_response, gemini_chat_session = get_gemini_response(
                    user_prompt, config['api_key'], tool_name, system_prompt, gemini_chat_session
                )
            else: # local
                assistant_response = get_local_llm_response(
                    user_prompt, config['url'], config['model'], tool_name, system_prompt, local_history
                )
                if assistant_response:
                    local_history.append({"user": user_prompt, "assistant": assistant_response})
            
            if assistant_response:
                print(f"\n{colors.ASSISTANT}Assistant:{colors.RESET}\n{assistant_response}")
                command_to_run = extract_command_from_response(assistant_response)
                if command_to_run:
                    print(f"\nI am about to run this command in the shell: {colors.COMMAND}{command_to_run}{colors.RESET}")
                    loop.remove_reader(0)
                    os.set_blocking(0, True)
                    try:
                        confirm = input("Do you want to proceed? [y/n] ").lower().strip()
                        if confirm == 'y':
                            os.write(master_fd, (command_to_run + '\n').encode())
                        else:
                            print("Execution cancelled.")
                    finally:
                        os.set_blocking(0, False)
                        loop.add_reader(0, handle_user_input)
            else:
                print(f"\n{colors.WARNING}The assistant did not provide a response.{colors.RESET}")

        loop.add_reader(0, handle_user_input)
        loop.add_reader(master_fd, handle_tool_output)

        try:
            await asyncio.Event().wait()
        finally:
            loop.remove_reader(0)
            loop.remove_reader(master_fd)
            os.set_blocking(0, True)
            print(f"\n{tool_name.capitalize()} session ended.")


async def metasploit_loop(provider, config):
    """Wrapper for the Metasploit Assistant."""
    await pty_loop_base(
        provider, config,
        tool_name='metasploit',
        tool_color=colors.METASPLOIT,
        system_prompt=METASPLOIT_SYSTEM_PROMPT,
        start_command=['msfconsole', '-q']
    )

async def wapiti_loop(provider, config):
    """Wrapper for the Wapiti Assistant."""
    # Check if wapiti is installed
    try:
        subprocess.run(['wapiti', '--version'], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"{colors.ERROR}Error: 'wapiti' not found or not working.{colors.RESET}")
        print("Please ensure Wapiti is installed and in your PATH. (e.g., 'sudo apt install wapiti' or 'pip install wapiti3')")
        return

    await pty_loop_base(
        provider, config,
        tool_name='wapiti',
        tool_color=colors.WAPITI,
        system_prompt=WAPITI_SYSTEM_PROMPT,
        start_command=['bash']  # Start a bash shell for flexibility
    )


# --- Main Application Logic ---
def main():
    """The main function to configure and run the application."""
    print(f"\n{colors.SUCCESS}Welcome to the AI-Powered Shell!{colors.RESET}")

    mode = ""
    while mode not in ['translator', 'assistant', 'metasploit', 'wapiti']:
        choice = input(
            f"Choose an operating mode:\n"
            f"{colors.INFO}1. Command Translator{colors.RESET} (Prompt -> Command)\n"
            f"{colors.INFO}2. AI Assistant{colors.RESET} (Conversational shell help)\n"
            f"{colors.INFO}3. Metasploit Assistant{colors.RESET} (AI-driven penetration testing)\n"
            f"{colors.INFO}4. Wapiti Assistant{colors.RESET} (AI-driven web app scanning)\n"
            "Enter choice (1, 2, 3, or 4): "
        ).strip()
        if choice == '1': mode = 'translator'
        elif choice == '2': mode = 'assistant'
        elif choice == '3': mode = 'metasploit'
        elif choice == '4': mode = 'wapiti'


    provider = ""
    while provider not in ['gemini', 'local']:
        choice = input(f"\nChoose an LLM provider:\n{colors.INFO}1. Gemini{colors.RESET}\n{colors.INFO}2. Local LLM (Ollama){colors.RESET}\nEnter choice (1 or 2): ").strip()
        if choice == '1': provider = 'gemini'
        elif choice == '2': provider = 'local'

    config = {}
    if provider == 'gemini':
        api_key = os.environ.get("API_KEY") or getpass.getpass("Please enter your Gemini API Key: ").strip()
        if not api_key:
            print(f"{colors.ERROR}No API key provided. Exiting.{colors.RESET}"); return
        config['api_key'] = api_key
    else: # local
        local_models = {
            "1": {"name": "llama3", "size_gb": 5.4},
            "2": {"name": "codellama", "size_gb": 4.0},
            "3": {"name": "mistral", "size_gb": 4.1},
        }
        model_choice = ""
        while model_choice not in local_models:
            print(f"\nPlease choose a local LLM to run:")
            for key, info in local_models.items():
                print(f"{colors.INFO}{key}. {info['name']} (~{info['size_gb']} GB RAM){colors.RESET}")
            model_choice = input(f"Enter choice ({', '.join(local_models.keys())}): ").strip()
        
        selected_model = local_models[model_choice]
        if not check_and_setup_ollama(selected_model['name'], selected_model['size_gb']): return
        
        config['model'] = selected_model['name']
        config['ip'] = input(f"Enter Ollama IP address [localhost]: ").strip() or "localhost"
        config['port'] = input(f"Enter Ollama port [11434]: ").strip() or "11434"
        config['url'] = f"http://{config['ip']}:{config['port']}/api/generate"

    print("-" * 30)
    print(f"Mode: {colors.INFO}{mode.capitalize()}{colors.RESET}")
    print(f"Provider: {colors.INFO}{provider.capitalize()}{colors.RESET}")
    if provider == 'local':
        print(f"Model: {colors.INFO}{config['model']}{colors.RESET}")
    
    try:
        if mode == 'translator':
            translator_loop(provider, config)
        elif mode == 'assistant':
            assistant_loop(provider, config)
        elif mode == 'metasploit':
            asyncio.run(metasploit_loop(provider, config))
        elif mode == 'wapiti':
            asyncio.run(wapiti_loop(provider, config))
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
    
    print("\nGoodbye!")

if __name__ == "__main__":
    main()

