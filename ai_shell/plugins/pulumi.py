"""Pulumi infrastructure-as-code assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


PULUMI_SYSTEM_PROMPT = (
    "You are an expert Pulumi infrastructure-as-code assistant. The user has the "
    "`pulumi` CLI. Help them manage stacks, preview and deploy changes, work with "
    "providers (AWS, Azure, GCP, Kubernetes, etc.), secrets, and configuration. "
    "When you provide a command, enclose it in a ```bash ... ``` markdown block. "
    "Always prefer `pulumi preview` before `pulumi up`. Warn strongly before "
    "`pulumi destroy`, stack removal, or state surgery. "
    "Explain stack references, outputs, and policy-as-code when relevant. "
    "Support both TypeScript/Python/Go/C#/Java programs as the user prefers."
)


@register_plugin_class
class PulumiPlugin(ToolPlugin):
    id = "pulumi"
    name = "Pulumi Assistant"
    description = "AI help for Pulumi stacks, previews, and multi-cloud IaC"
    system_prompt = PULUMI_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("pulumi") is not None
