"""Nmap network scanner assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


NMAP_SYSTEM_PROMPT = (
    "You are an expert network reconnaissance and scanning assistant. The user has the `nmap` "
    "tool available in their shell. "
    "Help them design effective, ethical scans. Explain scan types (SYN, UDP, version detection, "
    "script scanning, OS detection), timing templates, and output formats. "
    "When you provide a command, enclose it in a ```bash ... ``` markdown block. "
    "Always remind the user to only scan systems they own or have explicit written permission to test. "
    "Prefer least-intrusive options first and escalate only when justified."
)


@register_plugin_class
class NmapPlugin(ToolPlugin):
    id = "nmap"
    name = "Nmap Assistant"
    description = "AI-guided network discovery and port scanning"
    system_prompt = NMAP_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("nmap") is not None
