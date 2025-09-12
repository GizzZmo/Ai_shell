"""UI utilities and color management for AI Shell."""

try:
    from colorama import init, Fore, Style

    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


class Colors:
    """ANSI color codes for terminal output."""

    if COLORAMA_AVAILABLE:
        RESET = Style.RESET_ALL
        WARNING = Fore.YELLOW + Style.BRIGHT
        INFO = Fore.BLUE + Style.BRIGHT
        SUCCESS = Fore.GREEN + Style.BRIGHT
        ERROR = Fore.RED + Style.BRIGHT
        COMMAND = Fore.MAGENTA + Style.BRIGHT
        PROMPT = Fore.CYAN + Style.BRIGHT
        ASSISTANT = Fore.GREEN + Style.BRIGHT
        METASPLOIT = Fore.RED + Style.BRIGHT
        WAPITI = Fore.YELLOW + Style.BRIGHT
    else:
        # Fallback to basic ANSI codes
        RESET = "\033[0m"
        WARNING = "\033[1;33m"
        INFO = "\033[1;34m"
        SUCCESS = "\033[1;32m"
        ERROR = "\033[1;31m"
        COMMAND = "\033[1;35m"
        PROMPT = "\033[1;36m"
        ASSISTANT = "\033[1;32m"
        METASPLOIT = "\033[1;31m"
        WAPITI = "\033[1;38;5;208m"


colors = Colors()


def print_banner():
    """Print the application banner."""
    banner = f"""
{colors.SUCCESS}╔══════════════════════════════════════════════════════════════╗
║                    AI-Powered Shell Assistant                ║
║              Your Command-Line Copilot v0.1.0               ║
╚══════════════════════════════════════════════════════════════╝{colors.RESET}
"""
    print(banner)


def print_mode_selection():
    """Print mode selection menu."""
    print("Choose an operating mode:")
    print(f"{colors.INFO}1. Command Translator{colors.RESET} (Prompt → Command)")
    print(f"{colors.INFO}2. AI Assistant{colors.RESET} (Conversational shell help)")
    print(
        f"{colors.INFO}3. Metasploit Assistant{colors.RESET} (AI-driven penetration testing)"
    )
    print(
        f"{colors.INFO}4. Wapiti Assistant{colors.RESET} (AI-driven web app scanning)"
    )


def print_provider_selection():
    """Print LLM provider selection menu."""
    print("\nChoose an LLM provider:")
    print(f"{colors.INFO}1. Gemini{colors.RESET} (Google's cloud API)")
    print(f"{colors.INFO}2. Local LLM{colors.RESET} (Ollama)")


def print_local_model_selection(models):
    """Print local model selection menu."""
    print("\nPlease choose a local LLM to run:")
    for key, info in models.items():
        print(
            f"{colors.INFO}{key}. {info['name']}{colors.RESET} (~{info['size_gb']} GB RAM)"
        )


def format_command_output(text: str) -> str:
    """Format command output with appropriate colors."""
    return f"{colors.COMMAND}{text}{colors.RESET}"


def format_error(text: str) -> str:
    """Format error message with appropriate colors."""
    return f"{colors.ERROR}Error: {text}{colors.RESET}"


def format_warning(text: str) -> str:
    """Format warning message with appropriate colors."""
    return f"{colors.WARNING}Warning: {text}{colors.RESET}"


def format_info(text: str) -> str:
    """Format info message with appropriate colors."""
    return f"{colors.INFO}{text}{colors.RESET}"


def format_success(text: str) -> str:
    """Format success message with appropriate colors."""
    return f"{colors.SUCCESS}{text}{colors.RESET}"
