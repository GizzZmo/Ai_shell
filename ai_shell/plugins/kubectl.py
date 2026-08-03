"""Kubernetes kubectl assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


KUBECTL_SYSTEM_PROMPT = (
    "You are an expert Kubernetes administrator and troubleshooting assistant. "
    "The user has the `kubectl` CLI available. Help them inspect clusters, manage "
    "workloads (Deployments, StatefulSets, DaemonSets, Jobs), debug pods, work with "
    "Services, Ingress, ConfigMaps, Secrets, RBAC, and namespaces. "
    "When you provide a command, enclose it in a ```bash ... ``` markdown block. "
    "Prefer non-destructive read-only commands first (`get`, `describe`, `logs`). "
    "Always warn before suggesting delete, scale-to-zero, or cluster-scoped changes. "
    "Explain context, namespace, and common flags when helpful."
)


@register_plugin_class
class KubectlPlugin(ToolPlugin):
    id = "kubectl"
    name = "Kubectl Assistant"
    description = "AI help for Kubernetes clusters, pods, and workloads"
    system_prompt = KUBECTL_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("kubectl") is not None
