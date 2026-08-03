"""Podman container engine assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


PODMAN_SYSTEM_PROMPT = (
    "You are an expert Podman and rootless container assistant. The user has the "
    "`podman` CLI (and optionally `podman-compose` / `buildah`). Help them manage "
    "images, containers, pods, volumes, networks, and generate systemd units. "
    "When you provide a command, enclose it in a ```bash ... ``` markdown block. "
    "Highlight differences from Docker where relevant (rootless, pods, "
    "quadlets). Prefer non-destructive commands and warn before prune or force-remove."
)


@register_plugin_class
class PodmanPlugin(ToolPlugin):
    id = "podman"
    name = "Podman Assistant"
    description = "AI help for Podman containers, pods and rootless workflows"
    system_prompt = PODMAN_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("podman") is not None
