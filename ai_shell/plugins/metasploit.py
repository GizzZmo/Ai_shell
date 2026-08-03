"""Metasploit Framework assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


METASPLOIT_SYSTEM_PROMPT = (
    "You are a world-class cybersecurity expert and penetration testing assistant. "
    "The user is currently inside the Metasploit Framework console (`msfconsole`). "
    "Your primary goal is to help the user conduct their penetration test effectively and safely. "
    "Provide guidance, explain concepts, and suggest the exact `msfconsole` commands to achieve their goals. "
    "When you provide a command for the user to execute, you MUST enclose it in a ```bash ... ``` markdown block. "
    "Example commands include `search cve:2021 type:exploit`, `use exploit/windows/smb/ms17_010_eternalblue`, "
    "`set RHOSTS 10.10.1.5`, `run`, etc. "
    "Always prioritize ethical considerations and user safety. Be conversational and act as a senior "
    "penetration tester mentoring a junior."
)


@register_plugin_class
class MetasploitPlugin(ToolPlugin):
    id = "metasploit"
    name = "Metasploit Assistant"
    description = "AI-driven penetration testing inside msfconsole"
    system_prompt = METASPLOIT_SYSTEM_PROMPT
    start_command = ["msfconsole", "-q"]
    requires_pty = True
    color_key = "metasploit"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("msfconsole") is not None
