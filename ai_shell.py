

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

        # Handles cases like ```bash\nls -l\n```

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


    Args:

        prompt: The user's natural language input.

        api_key: The Google AI API key.


    Returns:

        The corresponding shell command as a string, or None if an error occurs.

    """

    if not genai:

        print(f"\n{colors.ERROR}Error:{colors.RESET} The 'google-generativeai' package is not installed. Please install it with 'pip install google-generativeai'.")

        return None

        

    try:

        genai.configure(api_key=api_key)

        

        model = genai.GenerativeModel('gemini-1.5-flash')

        

        meta_prompt = build_meta_prompt(prompt)

        

        response = model.generate_content(

            meta_prompt,

            generation_config=genai.types.GenerationConfig(

                temperature=0.0,

                max_output_tokens=100

            )

        )

        

        command = clean_llm_response(response.text)

        return command if command else None


    except Exception as e:

        print(f"\n{colors.ERROR}Error calling Gemini API:{colors.RESET} {e}")

        return None


def translate_with_local_llm(prompt: str, api_url: str) -> str | None:

    """

    Translates a prompt using a local LLM API (e.g., Ollama).


    Args:

        prompt: The user's natural language input.

        api_url: The URL of the local LLM's API endpoint.


    Returns:

        The corresponding shell command as a string, or None if an error occurs.

    """

    meta_prompt = build_meta_prompt(prompt)

    

    payload = {

        "model": "llama3", 

        "prompt": meta_prompt,

        "stream": False,

        "options": {

            "temperature": 0.0

        }

    }

    

    try:

        response = requests.post(api_url, json=payload, timeout=30)

        response.raise_for_status() 

        

        data = response.json()

        

        command_text = data.get('response', '')

        command = clean_llm_response(command_text)


        return command if command else None

        

    except requests.exceptions.RequestException as e:

        print(f"\n{colors.ERROR}Error calling local LLM API:{colors.RESET} {e}")

        print(f"{colors.INFO}Info:{colors.RESET} Please ensure your local LLM server is running and the URL '{api_url}' is correct.")

        return None

    except json.JSONDecodeError:

        print(f"\n{colors.ERROR}Error:{colors.RESET} Failed to decode JSON response from the local LLM API.")

        return None


# --- Command Execution ---


def execute_command(command: str, stream: bool = True):

    """

    Executes a shell command safely after user confirmation and prints its output.

    

    Args:

        command: The shell command string to execute.

        stream: Whether to print output in real-time.

    """

    if not command:

        print(f"\n{colors.WARNING}Sorry, I couldn't translate that into a command. Please try being more specific.{colors.RESET}")

        return


    print(f"\nI am about to execute this command: {colors.COMMAND}{command}{colors.RESET}")

    

    if command.strip().startswith("sudo"):

        print(f"{colors.WARNING}This command requires administrator privileges. You may be prompted for your password.{colors.RESET}")


    try:

        confirm = input("Do you want to proceed? [y/n] ").lower().strip()

        if confirm != 'y':

            print("Execution cancelled.")

            return


        print(f"\n{colors.INFO}--- Command Output ---{colors.RESET}")


        needs_shell = '|' in command or '>' in command or '<' in command or '&' in command

        

        if not needs_shell and platform.system() == "Windows":

            first_arg = shlex.split(command)[0] if command else ''

            if first_arg in ['dir', 'copy', 'del', 'move', 'rename', 'echo']:

                needs_shell = True


        process_args = command if needs_shell else shlex.split(command)

        

        if stream:

            process = subprocess.Popen(

                process_args,

                stdout=subprocess.PIPE,

                stderr=subprocess.STDOUT,

                text=True,

                shell=needs_shell,

                bufsize=1,

                universal_newlines=True

            )

            if process.stdout:

                for line in iter(process.stdout.readline, ''):

                    print(line, end='', flush=True)

                process.stdout.close()

            return_code = process.wait()

            if return_code != 0:

                 print(f"\n{colors.ERROR}Command finished with exit code: {return_code}{colors.RESET}")

        else:

            result = subprocess.run(

                process_args, capture_output=True, text=True, check=False, shell=needs_shell

            )

            if result.returncode == 0:

                print(result.stdout if result.stdout else "[No output]")

            else:

                print(f"{colors.ERROR}Error (Exit Code: {result.returncode}):{colors.RESET}")

                print(result.stderr if result.stderr else "[No error message]")


        print(f"\n{colors.INFO}----------------------{colors.RESET}")


    except FileNotFoundError:

        print(f"\n{colors.ERROR}Error:{colors.RESET} Command not found: '{shlex.split(command)[0]}'")

    except Exception as e:

        print(f"\n{colors.ERROR}An unexpected error occurred:{colors.RESET} {e}")


# --- Local LLM Setup ---


def check_and_setup_ollama() -> bool:

    """

    Checks if Ollama is installed and guides the user through setup if it's not.

    

    Returns:

        True if Ollama is ready, False otherwise.

    """

    try:

        subprocess.run(["ollama", "--version"], capture_output=True, check=True)

        print(f"{colors.SUCCESS}Ollama is already installed.{colors.RESET}")

    except (subprocess.CalledProcessError, FileNotFoundError):

        print(f"{colors.WARNING}Ollama is not installed or not in your PATH.{colors.RESET}")

        os_type = platform.system()


        if os_type == "Linux":

            install_cmd = "curl -fsSL https://ollama.com/install.sh | sh"

            print("You can install it by running the following command:")

            print(f"  {colors.COMMAND}{install_cmd}{colors.RESET}")

            if input("Do you want me to run this command for you? [y/n] ").lower().strip() == 'y':

                execute_command(install_cmd)

                print(f"{colors.INFO}Please restart your terminal after the installation for the changes to take effect.{colors.RESET}")

                return False # User needs to restart

        elif os_type == "Darwin": # macOS

            print(f"You can install it using Homebrew with the command:")

            print(f"  {colors.COMMAND}brew install ollama{colors.RESET}")

        elif os_type == "Windows":

            print(f"Please download and install Ollama from the official website:")

            print(f"  {colors.INFO}https://ollama.com/download{colors.RESET}")

        

        return False # Installation is required


    # If installed, check for a model and pull one if needed

    try:

        print("Checking for available models...")

        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)

        if "llama3" not in result.stdout:

            print(f"{colors.WARNING}'llama3' model not found. I will download it for you now (this may take a while).{colors.RESET}")

            execute_command("ollama pull llama3")

        else:

            print(f"{colors.SUCCESS}'llama3' model is available.{colors.RESET}")


    except (subprocess.CalledProcessError, FileNotFoundError):

        print(f"{colors.ERROR}Failed to check for Ollama models.{colors.RESET}")

        return False


    return True


# --- Main Application Logic ---


def main():

    """The main function to configure and run the application loop."""

    

    print(f"\n{colors.SUCCESS}Welcome to the Natural Language Shell!{colors.RESET}")


    # --- Interactive Setup ---

    provider = ""

    while provider not in ['gemini', 'local']:

        choice = input(f"Choose an LLM provider:\n{colors.INFO}1. Gemini{colors.RESET}\n{colors.INFO}2. Local LLM{colors.RESET}\nEnter choice (1 or 2): ").strip()

        if choice == '1':

            provider = 'gemini'

        elif choice == '2':

            provider = 'local'

        else:

            print(f"{colors.WARNING}Invalid choice. Please enter 1 or 2.{colors.RESET}")


    gemini_api_key = None

    local_llm_url = None


    if provider == 'gemini':

        gemini_api_key = os.environ.get("API_KEY")

        if not gemini_api_key:

            print(f"\n{colors.WARNING}Warning:{colors.RESET} 'API_KEY' environment variable not found.")

            try:

                gemini_api_key = getpass.getpass("Please enter your Gemini API Key: ").strip()

                if not gemini_api_key:

                    print(f"{colors.ERROR}No API key provided. Exiting.{colors.RESET}")

                    return

            except (KeyboardInterrupt, EOFError):

                 print("\nAPI key entry cancelled. Exiting.")

                 return

    else:  # local provider

        if not check_and_setup_ollama():

            print("Local LLM setup is required before you can proceed. Please follow the instructions above.")

            return

        

        print(f"\n{colors.INFO}Enter the details for your local LLM (e.g., Ollama).{colors.RESET}")

        ip = input("Enter the IP address [default: localhost]: ").strip() or "localhost"

        port = input("Enter the port number [default: 11434]: ").strip() or "11434"

        local_llm_url = f"http://{ip}:{port}/api/generate"

    

    print("-" * 30)

    print(f"Using provider: {colors.INFO}{provider.capitalize()}{colors.RESET}")

    print("Ask me to do things like 'what is my local ip?' or 'show me disk space'.")

    print("Type 'exit' or 'quit' to close.")


    # --- Main Loop ---

    while True:

        try:

            user_prompt = input(f"\n{colors.PROMPT}>{colors.RESET} ")

            if user_prompt.lower() in ["exit", "quit"]:

                print("Exiting...")

                break

            if not user_prompt:

                continue


            print(f"{colors.INFO}Translating prompt...{colors.RESET}")

            command_to_run = None

            if provider == 'gemini':

                command_to_run = translate_with_gemini(user_prompt, gemini_api_key)

            else: # local provider

                command_to_run = translate_with_local_llm(user_prompt, local_llm_url)

            

            execute_command(command_to_run)


        except (KeyboardInterrupt, EOFError):

            print("\nExiting...")

            break


if __name__ == "__main__":

    main()

