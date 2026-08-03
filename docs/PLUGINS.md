# Plugin System

AI Shell Suite supports **tool plugins** that provide specialized interactive assistants.

## Built-in Plugins

| ID           | Name                  | Requires                          |
|--------------|-----------------------|-----------------------------------|
| `metasploit` | Metasploit Assistant  | `msfconsole`                      |
| `wapiti`     | Wapiti Assistant      | `wapiti`                          |
| `nmap`       | Nmap Assistant        | `nmap`                            |
| `docker`     | Docker Assistant      | `docker`                          |
| `podman`     | Podman Assistant      | `podman`                          |
| `kubectl`    | Kubectl Assistant     | `kubectl`                         |
| `helm`       | Helm Assistant        | `helm`                            |
| `git`        | Git Assistant         | `git`                             |
| `ansible`    | Ansible Assistant     | `ansible` / `ansible-playbook`    |
| `terraform`  | Terraform Assistant  | `terraform` or `tofu`             |
| `aws`        | AWS Assistant         | `aws`                             |
| `trivy`      | Trivy Assistant       | `trivy`                           |
| `systemd`    | Systemd Assistant     | `systemctl`                       |
| `network`    | Network Assistant     | `ip` / `ss` / `ifconfig`          |

## Using a Plugin

```bash
ai-shell --mode kubectl
ai-shell -m git -p local
ais -m terraform
ais -m ansible --dry-run
```

Or run `ai-shell` and pick from the interactive menu (plugins appear after the core modes). Unavailable tools are marked “(not installed)”.

## Creating a New Plugin

1. Create a file under `ai_shell/plugins/`, e.g. `mytool.py`:

```python
from .base import ToolPlugin, register_plugin_class

MYTOOL_SYSTEM_PROMPT = (
    "You are an expert assistant for mytool. "
    "When you provide a command, enclose it in a ```bash ... ``` block."
)

@register_plugin_class
class MyToolPlugin(ToolPlugin):
    id = "mytool"
    name = "MyTool Assistant"
    description = "Short description shown in the menu"
    system_prompt = MYTOOL_SYSTEM_PROMPT
    start_command = ["bash"]          # or ["mytool"] for a direct shell
    requires_pty = True
    color_key = "info"

    def check_available(self) -> bool:
        import shutil
        return shutil.which("mytool") is not None
```

2. Restart `ai-shell`. The plugin is auto-discovered and appears in the menu.

## API Overview

| Symbol                    | Purpose                                      |
|---------------------------|----------------------------------------------|
| `ToolPlugin`              | Abstract base class                          |
| `@register_plugin_class`  | Decorator – registers on import              |
| `list_plugins()`          | All registered plugin instances              |
| `list_plugin_info()`      | Lightweight metadata for menus               |
| `get_plugin(id)`          | Lookup by id                                 |
| `discover_plugins()`      | Scans the package (called automatically)     |

Plugins may override:

- `check_available()` – detect whether the binary is installed
- `on_start()` / `on_stop()` – lifecycle hooks
- `preprocess_command(cmd)` – transform LLM suggestions before execution
