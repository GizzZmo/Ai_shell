"""systemd / journalctl system service assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


SYSTEMD_SYSTEM_PROMPT = (
    "You are an expert Linux system administration assistant focused on systemd. "
    "The user has `systemctl` and `journalctl` available. Help them manage services, "
    "units, timers, sockets, targets, and inspect logs. "
    "When you provide a command, enclose it in a ```bash ... ``` markdown block. "
    "Prefer status/inspect commands first. Warn before `stop`, `disable`, "
    "`mask`, or reboot-related operations on critical services. "
    "Explain unit files, drop-ins, and common failure patterns when helpful."
)


@register_plugin_class
class SystemdPlugin(ToolPlugin):
    id = "systemd"
    name = "Systemd Assistant"
    description = "AI help for systemctl, journalctl and service management"
    system_prompt = SYSTEMD_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("systemctl") is not None
