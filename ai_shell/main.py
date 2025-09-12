"""
AI Shell - Main Application Entry Point

This module serves as the primary entry point for the AI Shell application,
providing command-line interface, mode management, and core application logic.

The application supports three main operating modes:
1. Command Translator: Direct natural language to shell command translation
2. AI Assistant: Conversational mode with context awareness
3. Metasploit Assistant: Specialized penetration testing support

Key Features:
- Multi-provider LLM support (Gemini, Ollama)
- Interactive PTY sessions for tool integration
- Real-time command output streaming
- Security validation and user confirmation
- Training data collection and feedback loops

Examples:
    Basic usage:
        $ ai-shell

    Direct mode selection:
        $ ai-shell --mode translator
        $ ai-shell --mode assistant --provider local

    Custom configuration:
        $ ai-shell --config myconfig.yaml --no-confirmation

Author: AI Shell Contributors
License: MIT
"""

import argparse
import asyncio
import getpass
import logging
import os
import pty
import select
import subprocess
import sys
from typing import Optional

from . import __version__
from .config import get_config
from .llm import (
    get_llm_provider,
    GeminiProvider,
    LocalLLMProvider,
    ASSISTANT_SYSTEM_PROMPT,
    METASPLOIT_SYSTEM_PROMPT,
    WAPITI_SYSTEM_PROMPT,
    extract_command_from_response,
)
from .executor import get_executor
from .ui import (
    colors,
    print_banner,
    print_mode_selection,
    print_provider_selection,
    print_local_model_selection,
    format_error,
    format_warning,
    format_info,
    format_success,
)


def setup_logging():
    """
    Configure logging for the AI Shell application.

    Sets up logging based on configuration file settings, including:
    - Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - Log file location
    - Log format string
    - Multiple handlers (file and console)

    The configuration is loaded from the global config and supports
    environment variable overrides.

    Raises:
        PermissionError: If log file cannot be created/written
        ValueError: If log level is invalid
    """
    config = get_config()
    log_level = config.get("logging.level", "INFO")
    log_file = config.get("logging.file", "ai_shell.log")
    log_format = config.get(
        "logging.format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
    )


def parse_arguments():
    """
    Parse and validate command-line arguments.

    Creates an argument parser with all supported command-line options
    including mode selection, provider configuration, logging options,
    and security settings.

    Returns:
        argparse.Namespace: Parsed command-line arguments with the following attributes:
            - mode (str): Operating mode ('translator', 'assistant', 'metasploit', 'wapiti')
            - provider (str): LLM provider ('gemini', 'local')
            - config (str): Path to configuration file
            - api_key (str): API key for cloud providers
            - no_confirmation (bool): Skip command confirmation
            - log_level (str): Override log level
            - version (bool): Show version information

    Examples:
        >>> args = parse_arguments()
        >>> print(args.mode)
        'translator'
        >>> print(args.provider)
        'gemini'
    """
    parser = argparse.ArgumentParser(
        description="AI Shell - An intelligent command-line assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ai-shell                          # Interactive mode selection
  ai-shell --mode translator       # Direct translator mode
  ai-shell --mode assistant        # AI assistant mode
  ai-shell --provider local        # Use local LLM
  ai-shell --config myconfig.yaml  # Use custom config file
        """,
    )

    parser.add_argument(
        "--version", action="version", version=f"AI Shell {__version__}"
    )

    parser.add_argument(
        "--mode",
        choices=["translator", "assistant", "metasploit", "wapiti"],
        help="Operating mode (default: interactive selection)",
    )

    parser.add_argument(
        "--provider",
        choices=["gemini", "local"],
        help="LLM provider (default: from config or interactive selection)",
    )

    parser.add_argument("--config", metavar="FILE", help="Configuration file path")

    parser.add_argument(
        "--api-key",
        metavar="KEY",
        help="Gemini API key (overrides config and environment)",
    )

    parser.add_argument(
        "--no-confirmation",
        action="store_true",
        help="Skip command confirmation prompts",
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level",
    )

    return parser.parse_args()


def interactive_mode_selection() -> str:
    """Interactive mode selection."""
    print_mode_selection()

    while True:
        try:
            choice = input("Enter choice (1, 2, 3, or 4): ").strip()
            mode_map = {
                "1": "translator",
                "2": "assistant",
                "3": "metasploit",
                "4": "wapiti",
            }
            if choice in mode_map:
                return mode_map[choice]
            print(format_warning("Invalid choice. Please enter 1, 2, 3, or 4."))
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            sys.exit(0)


def interactive_provider_selection() -> str:
    """Interactive provider selection."""
    print_provider_selection()

    while True:
        try:
            choice = input("Enter choice (1 or 2): ").strip()
            if choice == "1":
                return "gemini"
            elif choice == "2":
                return "local"
            print(format_warning("Invalid choice. Please enter 1 or 2."))
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            sys.exit(0)


def setup_gemini_provider(api_key: Optional[str] = None) -> bool:
    """Setup Gemini provider configuration."""
    config = get_config()

    if not api_key:
        api_key = config.get("llm.gemini.api_key") or os.environ.get("GEMINI_API_KEY")

    if not api_key:
        try:
            api_key = getpass.getpass("Please enter your Gemini API Key: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nNo API key provided. Exiting.")
            return False

    if not api_key:
        print(format_error("No API key provided"))
        return False

    config.set("llm.gemini.api_key", api_key)
    return True


def setup_local_provider() -> bool:
    """Setup local LLM provider configuration."""
    config = get_config()

    # Available models
    local_models = {
        "1": {"name": "llama3", "size_gb": 5.4},
        "2": {"name": "codellama", "size_gb": 4.0},
        "3": {"name": "mistral", "size_gb": 4.1},
    }

    print_local_model_selection(local_models)

    while True:
        try:
            choice = input(f"Enter choice ({', '.join(local_models.keys())}): ").strip()
            if choice in local_models:
                break
            print(
                format_warning(
                    f"Invalid choice. Please enter {', '.join(local_models.keys())}."
                )
            )
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            return False

    selected_model = local_models[choice]

    # Check and setup Ollama
    if not check_and_setup_ollama(selected_model["name"], selected_model["size_gb"]):
        return False

    # Get connection details
    try:
        host = input("Enter Ollama IP address [localhost]: ").strip() or "localhost"
        port = input("Enter Ollama port [11434]: ").strip() or "11434"
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        return False

    config.set("llm.local.host", host)
    config.set("llm.local.port", int(port))
    config.set("llm.local.model", selected_model["name"])

    return True


def check_and_setup_ollama(model_name: str, model_size_gb: float) -> bool:
    """Check and setup Ollama with the specified model."""
    try:
        # Check if Ollama is installed
        subprocess.run(
            ["ollama", "--version"], capture_output=True, check=True, text=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(format_error("Ollama is not installed or not in your PATH"))
        print("Please install Ollama from https://ollama.ai/")
        return False

    try:
        # Check if model is available
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, check=True
        )
        if model_name not in result.stdout:
            print(format_info(f"'{model_name}' model not found. Pulling now..."))
            subprocess.run(["ollama", "pull", model_name], check=True)
            print(format_success(f"Successfully downloaded '{model_name}'"))
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(format_error("Could not connect to Ollama server"))
        return False

    return True


def translator_loop():
    """Main loop for the direct command translator."""
    print("\n--- Command Translator Mode ---")
    print("Enter a prompt, and I'll give you a shell command.")
    print("Type 'exit' or 'quit' to close.")

    llm_provider = get_llm_provider()
    executor = get_executor()

    while True:
        try:
            user_prompt = input(f"\n{colors.PROMPT}>{colors.RESET} ")
            if user_prompt.lower() in ["exit", "quit"]:
                break
            if not user_prompt:
                continue

            print(format_info("Translating prompt..."))
            command_to_run, _ = llm_provider.generate_response(
                user_prompt, "translator"
            )

            if command_to_run:
                executor.execute_command(command_to_run, user_prompt)
            else:
                print(format_warning("Could not generate command"))

        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break


def assistant_loop():
    """Main loop for the conversational AI assistant."""
    print("\n--- AI Assistant Mode ---")
    print(
        "Ask me anything, or describe a task. I can explain concepts or provide commands."
    )
    print("Type 'exit' or 'quit' to close.")

    llm_provider = get_llm_provider()
    executor = get_executor()
    chat_session = None

    while True:
        try:
            user_prompt = input(f"\n{colors.PROMPT}You: {colors.RESET}")
            if user_prompt.lower() in ["exit", "quit"]:
                break
            if not user_prompt:
                continue

            print(format_info("Assistant is thinking..."))
            assistant_response, chat_session = llm_provider.generate_response(
                user_prompt, "assistant", ASSISTANT_SYSTEM_PROMPT, chat_session
            )

            if assistant_response:
                print(
                    f"\n{colors.ASSISTANT}Assistant:{colors.RESET}\n{assistant_response}"
                )

                # Check for executable command
                command_to_run = extract_command_from_response(assistant_response)
                if command_to_run:
                    executor.execute_command(command_to_run, user_prompt)
            else:
                print(format_warning("Assistant did not provide a response"))

        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break


async def metasploit_loop():
    """Main loop for Metasploit assistant."""
    await pty_loop_base(
        tool_name="metasploit",
        tool_color=colors.METASPLOIT,
        system_prompt=METASPLOIT_SYSTEM_PROMPT,
        start_command=["msfconsole", "-q"],
    )


async def wapiti_loop():
    """Main loop for Wapiti assistant."""
    # Check if wapiti is available
    try:
        subprocess.run(["wapiti", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(format_error("'wapiti' not found or not working"))
        print("Please ensure Wapiti is installed and in your PATH")
        print("(e.g., 'sudo apt install wapiti' or 'pip install wapiti3')")
        return

    await pty_loop_base(
        tool_name="wapiti",
        tool_color=colors.WAPITI,
        system_prompt=WAPITI_SYSTEM_PROMPT,
        start_command=["bash"],
    )


async def pty_loop_base(
    tool_name: str, tool_color: str, system_prompt: str, start_command: list
):
    """Generic base function for running a tool in a pseudoterminal with AI assistance."""
    print(f"\n--- {tool_name.capitalize()} Assistant Mode ---")
    print(f"Starting a shell for {tool_name} tasks.")
    print(
        f"To ask the AI for commands, start your prompt with '{colors.PROMPT}?{colors.RESET}'"
    )
    print(f"Example: {colors.PROMPT}? scan example.com for xss{colors.RESET}")
    print(f"To exit, type '{colors.COMMAND}exit{colors.RESET}' at the shell prompt.")

    pid, master_fd = pty.fork()

    if pid == 0:  # Child process
        try:
            os.execvp(start_command[0], start_command)
        except FileNotFoundError:
            print(format_error(f"'{start_command[0]}' not found"))
            print("Please ensure it is installed and in your PATH")
            os._exit(1)
    else:  # Parent process
        loop = asyncio.get_event_loop()
        llm_provider = get_llm_provider()
        chat_session = None

        os.set_blocking(master_fd, False)
        os.set_blocking(0, False)

        def handle_user_input():
            try:
                user_data = os.read(0, 1024)
                if user_data:
                    user_input = user_data.decode().strip()
                    if user_input.startswith("?"):
                        handle_ai_interaction(user_input[1:].strip())
                    else:
                        os.write(master_fd, user_data)
            except (BlockingIOError, InterruptedError):
                pass

        def handle_tool_output():
            try:
                tool_data = os.read(master_fd, 1024)
                if tool_data:
                    print(
                        f"{tool_color}{tool_data.decode()}{colors.RESET}",
                        end="",
                        flush=True,
                    )
                else:
                    loop.stop()
            except (BlockingIOError, InterruptedError):
                pass

        def handle_ai_interaction(user_prompt):
            nonlocal chat_session
            print(format_info("\nAssistant is thinking..."))

            assistant_response, chat_session = llm_provider.generate_response(
                user_prompt, tool_name, system_prompt, chat_session
            )

            if assistant_response:
                print(
                    f"\n{colors.ASSISTANT}Assistant:{colors.RESET}\n{assistant_response}"
                )
                command_to_run = extract_command_from_response(assistant_response)
                if command_to_run:
                    print(
                        f"\nI am about to run this command in the shell: {colors.COMMAND}{command_to_run}{colors.RESET}"
                    )
                    loop.remove_reader(0)
                    os.set_blocking(0, True)
                    try:
                        confirm = (
                            input("Do you want to proceed? [y/n] ").lower().strip()
                        )
                        if confirm == "y":
                            os.write(master_fd, (command_to_run + "\n").encode())
                        else:
                            print("Execution cancelled.")
                    finally:
                        os.set_blocking(0, False)
                        loop.add_reader(0, handle_user_input)
            else:
                print(format_warning("\nThe assistant did not provide a response"))

        loop.add_reader(0, handle_user_input)
        loop.add_reader(master_fd, handle_tool_output)

        try:
            await asyncio.Event().wait()
        finally:
            loop.remove_reader(0)
            loop.remove_reader(master_fd)
            os.set_blocking(0, True)
            print(f"\n{tool_name.capitalize()} session ended.")


def main():
    """
    Main entry point for the AI Shell application.

    Orchestrates the complete application workflow including:
    1. Command-line argument parsing and validation
    2. Logging setup and configuration loading
    3. LLM provider initialization
    4. Mode selection and execution
    5. Error handling and graceful shutdown

    The function handles different operating modes:
    - translator: Direct command translation
    - assistant: Conversational AI assistance
    - metasploit: Security testing with msfconsole integration
    - wapiti: Web application security scanning

    Returns:
        int: Exit code (0 for success, non-zero for errors)

    Raises:
        KeyboardInterrupt: User interrupted the application
        SystemExit: Application terminated due to critical error

    Examples:
        Run from command line:
            $ ai-shell
            $ ai-shell --mode translator --provider local
    """
    args = parse_arguments()

    # Setup logging
    setup_logging()

    # Load configuration
    config = get_config()

    # Apply command line overrides
    if args.api_key:
        config.set("llm.gemini.api_key", args.api_key)

    if args.no_confirmation:
        config.set("security.require_confirmation", False)

    if args.log_level:
        config.set("logging.level", args.log_level)

    # Display banner
    print_banner()

    # Determine mode
    mode = args.mode
    if not mode:
        mode = interactive_mode_selection()

    # Determine provider
    provider = args.provider or config.get("llm.provider")
    if not provider:
        provider = interactive_provider_selection()

    config.set("llm.provider", provider)

    # Setup provider
    if provider == "gemini":
        if not setup_gemini_provider(args.api_key):
            sys.exit(1)
    elif provider == "local":
        if not setup_local_provider():
            sys.exit(1)

    # Display configuration
    print("-" * 50)
    print(f"Mode: {format_info(mode.capitalize())}")
    print(f"Provider: {format_info(provider.capitalize())}")
    if provider == "local":
        print(f"Model: {format_info(config.get('llm.local.model'))}")

    # Run the selected mode
    try:
        if mode == "translator":
            translator_loop()
        elif mode == "assistant":
            assistant_loop()
        elif mode == "metasploit":
            asyncio.run(metasploit_loop())
        elif mode == "wapiti":
            asyncio.run(wapiti_loop())
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")

    print("\nGoodbye!")


if __name__ == "__main__":
    main()
