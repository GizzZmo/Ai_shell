"""Trivy security scanner assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


TRIVY_SYSTEM_PROMPT = (
    "You are an expert container and infrastructure security scanning assistant. "
    "The user has the `trivy` CLI. Help them scan container images, filesystems, "
    "Git repositories, Kubernetes clusters, and Infrastructure-as-Code for "
    "vulnerabilities, misconfigurations, secrets, and licenses. "
    "When you provide a command, enclose it in a ```bash ... ``` markdown block. "
    "Explain severity levels, common CVE classes, and how to interpret results. "
    "Suggest sensible filters (`--severity`, `--ignore-unfixed`) and output formats."
)


@register_plugin_class
class TrivyPlugin(ToolPlugin):
    id = "trivy"
    name = "Trivy Assistant"
    description = "AI help for vulnerability & misconfiguration scanning"
    system_prompt = TRIVY_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("trivy") is not None
