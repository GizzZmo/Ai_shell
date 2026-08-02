"""
Plugin system base classes and registry for AI Shell Suite.

Tool plugins provide specialized interactive assistants (Metasploit, Wapiti,
nmap, docker, kubectl, etc.). New tools can be added by:

1. Subclassing ``ToolPlugin``
2. Implementing the required attributes/methods
3. Placing the module under ``ai_shell/plugins/`` (auto-discovered)
   or registering manually via ``register_plugin()``.
"""

from __future__ import annotations

import importlib
import logging
import pkgutil
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type

logger = logging.getLogger(__name__)


@dataclass
class PluginInfo:
    """Lightweight metadata used for menus and discovery."""

    id: str
    name: str
    description: str
    available: bool = True
    requires_pty: bool = True
    color_key: str = "info"  # maps to ui.colors or rich style


class ToolPlugin(ABC):
    """
    Abstract base class for interactive tool plugins.

    Subclasses must define class attributes and may override methods.
    """

    # --- Required class attributes ---
    id: str = ""                     # unique short id, e.g. "metasploit"
    name: str = ""                   # human name shown in menus
    description: str = ""            # one-line description
    system_prompt: str = ""          # LLM system prompt for this tool
    start_command: List[str] = field(default_factory=lambda: ["bash"])  # command to exec in PTY
    requires_pty: bool = True
    color_key: str = "info"          # key used by ui for coloring output

    def __init__(self):
        if not self.id or not self.name:
            raise ValueError(f"{self.__class__.__name__} must define 'id' and 'name'")

    # --- Optional overrides ---

    def check_available(self) -> bool:
        """
        Return True if the underlying tool is installed and usable.
        Default implementation tries to run the first element of start_command --version / --help.
        """
        import shutil
        import subprocess

        if not self.start_command:
            return False
        binary = self.start_command[0]
        if shutil.which(binary) is None:
            return False
        # Light check – many tools support --version
        try:
            subprocess.run(
                [binary, "--version"],
                capture_output=True,
                timeout=5,
                check=False,
            )
            return True
        except Exception:
            # Still consider it available if the binary exists
            return True

    def get_info(self) -> PluginInfo:
        return PluginInfo(
            id=self.id,
            name=self.name,
            description=self.description,
            available=self.check_available(),
            requires_pty=self.requires_pty,
            color_key=self.color_key,
        )

    def on_start(self) -> None:
        """Hook called just before the PTY session starts."""
        pass

    def on_stop(self) -> None:
        """Hook called after the PTY session ends."""
        pass

    def preprocess_command(self, command: str) -> str:
        """Optional: transform an LLM-suggested command before sending to the tool."""
        return command


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_REGISTRY: Dict[str, ToolPlugin] = {}


def register_plugin(plugin: ToolPlugin) -> None:
    """Register a plugin instance (or replace an existing one with the same id)."""
    if not plugin.id:
        raise ValueError("Plugin must have a non-empty id")
    _REGISTRY[plugin.id] = plugin
    logger.debug("Registered plugin: %s (%s)", plugin.id, plugin.name)


def register_plugin_class(cls: Type[ToolPlugin]) -> Type[ToolPlugin]:
    """Decorator to register a plugin class (instantiates it immediately)."""
    instance = cls()
    register_plugin(instance)
    return cls


def get_plugin(plugin_id: str) -> Optional[ToolPlugin]:
    return _REGISTRY.get(plugin_id)


def list_plugins(available_only: bool = False) -> List[ToolPlugin]:
    plugins = list(_REGISTRY.values())
    if available_only:
        plugins = [p for p in plugins if p.check_available()]
    return sorted(plugins, key=lambda p: p.name.lower())


def list_plugin_info(available_only: bool = False) -> List[PluginInfo]:
    return [p.get_info() for p in list_plugins(available_only=available_only)]


def discover_plugins() -> None:
    """
    Auto-discover and import all modules under ai_shell.plugins
    (except base and __init__). Modules should register themselves
    via the @register_plugin_class decorator or by calling register_plugin().
    """
    try:
        import ai_shell.plugins as plugins_pkg
    except ImportError:
        logger.warning("Could not import ai_shell.plugins package")
        return

    package_path = plugins_pkg.__path__
    prefix = plugins_pkg.__name__ + "."

    for finder, name, ispkg in pkgutil.iter_modules(package_path, prefix):
        if name.endswith(".base") or name.endswith(".__init__"):
            continue
        try:
            importlib.import_module(name)
            logger.debug("Loaded plugin module: %s", name)
        except Exception as e:
            logger.warning("Failed to load plugin module %s: %s", name, e)


def clear_registry() -> None:
    """Clear all registered plugins (mainly for tests)."""
    _REGISTRY.clear()
