"""Terraform infrastructure-as-code assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


TERRAFORM_SYSTEM_PROMPT = (
    "You are an expert Terraform / OpenTofu infrastructure-as-code assistant. "
    "The user has the `terraform` (or `tofu`) CLI. Help them write HCL, manage "
    "providers, modules, state, workspaces, and run plan/apply/destroy safely. "
    "When you provide a command, enclose it in a ```bash ... ``` markdown block. "
    "Always prefer `terraform plan` before `apply`. Warn strongly before "
    "`destroy`, state surgery (`state rm`, `state mv`), or force-unlock. "
    "Explain backends, remote state, and lock files when relevant."
)


@register_plugin_class
class TerraformPlugin(ToolPlugin):
    id = "terraform"
    name = "Terraform Assistant"
    description = "AI help for Terraform/OpenTofu plans, state and modules"
    system_prompt = TERRAFORM_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("terraform") is not None or shutil.which("tofu") is not None
