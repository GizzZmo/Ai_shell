"""Git version control assistant plugin."""

from __future__ import annotations

from .base import ToolPlugin, register_plugin_class


GIT_SYSTEM_PROMPT = (
    "You are an expert Git and version-control assistant. The user has the `git` CLI. "
    "Help them with everyday workflows (status, add, commit, branch, merge, rebase, "
    "stash, cherry-pick, bisect) and more advanced topics (reflog, worktrees, submodules, "
    "hooks, interactive rebase). "
    "When you provide a command, enclose it in a ```bash ... ``` markdown block. "
    "Prefer safe, reversible operations. Always warn before force-push, hard reset, "
    "or history-rewriting commands. Suggest clear, conventional commit messages when asked."
)


@register_plugin_class
class GitPlugin(ToolPlugin):
    id = "git"
    name = "Git Assistant"
    description = "AI help for Git workflows, branching, and history"
    system_prompt = GIT_SYSTEM_PROMPT
    start_command = ["bash"]
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("git") is not None
