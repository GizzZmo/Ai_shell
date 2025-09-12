"""LLM integration and prompt management for AI Shell."""

import re
import platform
import requests
import json
from typing import Optional, Tuple, Dict, Any

try:
    import google.generativeai as genai

    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    GENAI_AVAILABLE = False

from .config import get_config
from .ui import format_error


# System prompts for different modes
ASSISTANT_SYSTEM_PROMPT = (
    "You are an expert AI shell assistant. Your goal is to help the user accomplish their tasks by "
    "providing explanations, suggestions, and shell commands. The user is interacting with you through a special shell. "
    "When you provide a shell command that the user can execute, you MUST enclose it in a ```bash ... ``` markdown block. "
    "Be conversational and helpful. Break down complex tasks into steps. You can suggest tools and workflows. "
    f"The user's operating system is: {platform.system()}."
)

METASPLOIT_SYSTEM_PROMPT = (
    "You are a world-class cybersecurity expert and penetration testing assistant. The user is currently inside the Metasploit Framework console (`msfconsole`). "
    "Your primary goal is to help the user conduct their penetration test effectively and safely. "
    "Provide guidance, explain concepts, and suggest the exact `msfconsole` commands to achieve their goals. "
    "When you provide a command for the user to execute, you MUST enclose it in a ```bash ... ``` markdown block. "
    "Example commands include `search cve:2021 type:exploit`, `use exploit/windows/smb/ms17_010_eternalblue`, `set RHOSTS 10.10.1.5`, `run`, etc. "
    "Always prioritize ethical considerations and user safety. Be conversational and act as a senior penetration tester mentoring a junior."
)

WAPITI_SYSTEM_PROMPT = (
    "You are a world-class web application security expert. The user is in a shell environment with the `wapiti` tool available. "
    "Your primary goal is to help the user scan web applications for vulnerabilities effectively. "
    "Provide guidance, explain web vulnerabilities (like XSS, SQLi, LFI), and suggest the exact `wapiti` commands to perform scans. "
    "When you provide a command for the user to execute, you MUST enclose it in a ```bash ... ``` markdown block. "
    "Example commands include `wapiti -u http://example.com`, `wapiti -u http://test.com -m xss,sqli --scope domain`, `wapiti -u http://vulnerable.site -x http://vulnerable.site/logout`. "
    "Always remind the user to only scan applications they have explicit permission to test. Be conversational and act as a senior security analyst."
)


class LLMProvider:
    """Base class for LLM providers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def generate_response(
        self,
        prompt: str,
        mode: str,
        system_prompt: str = ASSISTANT_SYSTEM_PROMPT,
        chat_session: Any = None,
    ) -> Tuple[Optional[str], Any]:
        """Generate a response from the LLM."""
        raise NotImplementedError


class GeminiProvider(LLMProvider):
    """Google Gemini LLM provider."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        if not GENAI_AVAILABLE:
            raise ImportError("google-generativeai package is not installed")

        api_key = config.get("api_key", "")
        if not api_key:
            raise ValueError("Gemini API key is required")

        genai.configure(api_key=api_key)
        self.model_name = config.get("model", "gemini-1.5-flash")

    def generate_response(
        self,
        prompt: str,
        mode: str,
        system_prompt: str = ASSISTANT_SYSTEM_PROMPT,
        chat_session: Any = None,
    ) -> Tuple[Optional[str], Any]:
        """Generate a response from Gemini."""
        try:
            if mode == "translator":
                model = genai.GenerativeModel(self.model_name)
                meta_prompt = build_translator_meta_prompt(prompt)
                response = model.generate_content(
                    meta_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.0, max_output_tokens=100
                    ),
                )
                return clean_llm_response(response.text), chat_session
            else:  # assistant, metasploit, or wapiti
                if chat_session is None:
                    model = genai.GenerativeModel(
                        self.model_name, system_instruction=system_prompt
                    )
                    chat_session = model.start_chat(history=[])
                response = chat_session.send_message(prompt)
                return response.text, chat_session
        except Exception as e:
            print(format_error(f"Gemini API error: {e}"))
            return None, chat_session


class LocalLLMProvider(LLMProvider):
    """Local LLM provider using Ollama."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 11434)
        self.model = config.get("model", "llama3")
        self.api_url = f"http://{self.host}:{self.port}/api/generate"
        self.history = []

    def generate_response(
        self,
        prompt: str,
        mode: str,
        system_prompt: str = ASSISTANT_SYSTEM_PROMPT,
        chat_session: Any = None,
    ) -> Tuple[Optional[str], Any]:
        """Generate a response from local LLM."""
        try:
            if mode == "translator":
                meta_prompt = build_translator_meta_prompt(prompt)
                payload = {
                    "model": self.model,
                    "prompt": meta_prompt,
                    "stream": False,
                    "options": {"temperature": 0.0},
                }
            else:  # assistant, metasploit, or wapiti
                full_prompt = f"<|system|>\n{system_prompt}\n"
                for turn in self.history:
                    full_prompt += f"<|user|>\n{turn['user']}\n<|assistant|>\n{turn['assistant']}\n"
                full_prompt += f"<|user|>\n{prompt}\n<|assistant|>"
                payload = {
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {"temperature": 0.2},
                }

            response = requests.post(self.api_url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                print(format_error(f"Ollama server error: {data['error']}"))
                return None, chat_session

            response_text = data.get("response", "")
            if mode != "translator":
                self.history.append({"user": prompt, "assistant": response_text})

            return (
                clean_llm_response(response_text)
                if mode == "translator"
                else response_text
            ), chat_session

        except requests.exceptions.RequestException as e:
            print(format_error(f"Local LLM API error: {e}"))
            return None, chat_session
        except json.JSONDecodeError:
            print(format_error("Failed to decode JSON response from local LLM"))
            return None, chat_session


def build_translator_meta_prompt(prompt: str) -> str:
    """Create a standardized meta-prompt for translator mode."""
    os_type = platform.system()
    return (
        "You are an expert natural language to shell command translator. "
        "Your task is to take a user's prompt and their operating system, and return ONLY the single, most appropriate shell command. "
        "For tasks requiring administrator privileges (like installing software), prefix the command with 'sudo'. "
        "Do not provide any explanation, preamble, or markdown formatting. Just the raw command."
        f"\n\nUser's Operating System: {os_type}"
        f'\nUser\'s Prompt: "{prompt}"'
        "\n\nCommand:"
    )


def clean_llm_response(text: str) -> str:
    """Clean up common formatting issues from LLM responses for translator mode."""
    command = text.strip()
    # Remove markdown code blocks
    if command.startswith("```") and command.endswith("```"):
        command_lines = command.splitlines()
        if len(command_lines) > 1:
            # Handle cases like ```bash\ncommand\n```
            command = " ".join(line for line in command_lines[1:-1] if line.strip())
        else:
            command = command.strip("`")
    # Remove backticks
    if command.startswith("`") and command.endswith("`"):
        command = command.strip("`")
    return command


def extract_command_from_response(text: str) -> Optional[str]:
    """Extract a shell command from a markdown code block in the assistant's response."""
    # Pattern to find ```bash ... ``` blocks
    match = re.search(r"```bash\n(.*?)\n```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def get_llm_provider() -> LLMProvider:
    """Get the configured LLM provider."""
    config = get_config()
    provider_type = config.get("llm.provider", "gemini")

    if provider_type == "gemini":
        gemini_config = config.get("llm.gemini", {})
        return GeminiProvider(gemini_config)
    elif provider_type == "local":
        local_config = config.get("llm.local", {})
        return LocalLLMProvider(local_config)
    else:
        raise ValueError(f"Unknown LLM provider: {provider_type}")
