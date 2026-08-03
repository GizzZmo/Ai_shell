"""Network diagnostics assistant plugin (ss, ip, tcpdump, dig, ...)."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


NETWORK_SYSTEM_PROMPT = (
    "You are an expert network diagnostics and troubleshooting assistant. "
    "The user has common Linux networking tools available (`ip`, `ss`, `ping`, "
    "`traceroute`/`mtr`, `dig`/`nslookup`, `tcpdump`, `curl`, `nmap` if present). "
    "Help them inspect interfaces, routes, sockets, DNS, connectivity, and capture "
    "traffic. When you provide a command, enclose it in a ```bash ... ``` markdown block. "
    "Prefer least-intrusive checks first. Warn before long-running packet captures "
    "or scans of external networks. Explain output when it is dense or cryptic."
)


@register_plugin_class
class NetworkPlugin(ToolPlugin):
    id = "network"
    name = "Network Assistant"
    description = "AI help for ip, ss, dig, tcpdump and connectivity debugging"
    system_prompt = NETWORK_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        # Consider available if at least one core networking binary exists
        return any(shutil.which(b) for b in ("ip", "ss", "ifconfig"))
