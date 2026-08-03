"""Ansible automation assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


ANSIBLE_SYSTEM_PROMPT = (
    "You are an expert Ansible automation and configuration-management assistant. "
    "The user has Ansible tools available (`ansible`, `ansible-playbook`, `ansible-galaxy`, "
    "`ansible-inventory`, `ansible-vault`). Help them write and run playbooks, manage "
    "inventories, roles, collections, and vault secrets. "
    "When you provide a command, enclose it in a ```bash ... ``` markdown block. "
    "Prefer idempotent, check-mode (`--check`) runs before applying changes. "
    "Warn before any destructive or production-impacting playbook runs. "
    "Explain modules, handlers, tags, and variable precedence when helpful."
)


@register_plugin_class
class AnsiblePlugin(ToolPlugin):
    id = "ansible"
    name = "Ansible Assistant"
    description = "AI help for playbooks, roles, inventory and automation"
    system_prompt = ANSIBLE_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("ansible") is not None or shutil.which("ansible-playbook") is not None
