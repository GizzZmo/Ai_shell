"""
AI Shell Suite – Plugin system.

Importing this package triggers auto-discovery of all tool plugins.
"""

from .base import (
    PluginInfo,
    ToolPlugin,
    clear_registry,
    discover_plugins,
    get_plugin,
    list_plugin_info,
    list_plugins,
    register_plugin,
    register_plugin_class,
)

# Trigger discovery of built-in plugins (metasploit, wapiti, nmap, docker, ...)
discover_plugins()

__all__ = [
    "ToolPlugin",
    "PluginInfo",
    "register_plugin",
    "register_plugin_class",
    "get_plugin",
    "list_plugins",
    "list_plugin_info",
    "discover_plugins",
    "clear_registry",
]
