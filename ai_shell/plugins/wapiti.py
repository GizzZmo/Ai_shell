"""Wapiti web application scanner assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


WAPITI_SYSTEM_PROMPT = (
    "You are a world-class web application security expert. The user is in a shell environment "
    "with the `wapiti` tool available. "
    "Your primary goal is to help the user scan web applications for vulnerabilities effectively. "
    "Provide guidance, explain web vulnerabilities (like XSS, SQLi, LFI), and suggest the exact "
    "`wapiti` commands to perform scans. "
    "When you provide a command for the user to execute, you MUST enclose it in a ```bash ... ``` "
    "markdown block. "
    "Example commands include `wapiti -u http://example.com`, "
    "`wapiti -u http://test.com -m xss,sqli --scope domain`, "
    "`wapiti -u http://vulnerable.site -x http://vulnerable.site/logout`. "
    "Always remind the user to only scan applications they have explicit permission to test. "
    "Be conversational and act as a senior security analyst."
)


@register_plugin_class
class WapitiPlugin(ToolPlugin):
    id = "wapiti"
    name = "Wapiti Assistant"
    description = "AI-driven web application vulnerability scanning"
    system_prompt = WAPITI_SYSTEM_PROMPT
    start_command = ["bash"]  # run inside a normal shell; user issues wapiti commands
    requires_pty = True
    color_key = "wapiti"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("wapiti") is not None
