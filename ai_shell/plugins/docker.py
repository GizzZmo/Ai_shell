"""Docker assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


DOCKER_SYSTEM_PROMPT = (
    "You are an expert Docker and containerization assistant. The user has the `docker` CLI "
    "available. Help them manage images, containers, networks, volumes, and Compose workflows. "
    "Provide clear, safe commands. When you suggest a command, enclose it in a ```bash ... ``` "
    "markdown block. Prefer non-destructive options and always warn before suggesting "
    "`docker system prune`, forced removals, or operations that delete data. "
    "Explain concepts briefly when helpful (layers, volumes vs bind mounts, networks, etc.)."
)


@register_plugin_class
class DockerPlugin(ToolPlugin):
    id = "docker"
    name = "Docker Assistant"
    description = "AI help for Docker images, containers, Compose & troubleshooting"
    system_prompt = DOCKER_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("docker") is not None
