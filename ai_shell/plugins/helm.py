"""Helm Kubernetes package manager assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


HELM_SYSTEM_PROMPT = (
    "You are an expert Helm and Kubernetes packaging assistant. The user has the "
    "`helm` CLI. Help them search, install, upgrade, rollback, and manage charts "
    "and releases. Explain values files, chart dependencies, hooks, and "
    "release history. "
    "When you provide a command, enclose it in a ```bash ... ``` markdown block. "
    "Prefer `helm template` / `helm lint` / dry-run installs before applying. "
    "Warn before uninstall or upgrade that could disrupt production workloads."
)


@register_plugin_class
class HelmPlugin(ToolPlugin):
    id = "helm"
    name = "Helm Assistant"
    description = "AI help for Helm charts, releases and Kubernetes packaging"
    system_prompt = HELM_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("helm") is not None
