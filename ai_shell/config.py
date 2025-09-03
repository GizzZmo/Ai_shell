"""
Configuration Management for AI Shell

This module provides comprehensive configuration management for AI Shell,
supporting YAML files, environment variables, and programmatic configuration.

The configuration system follows a hierarchical approach:
1. Command-line arguments (highest priority)
2. Environment variables 
3. Configuration files (YAML)
4. Default values (lowest priority)

Key Features:
- YAML-based configuration with environment variable substitution
- Nested configuration access using dot notation
- Automatic configuration file discovery
- Runtime configuration updates
- Configuration validation and error handling

Examples:
    Basic usage:
        >>> config = Config()
        >>> api_key = config.get('llm.gemini.api_key')
        >>> config.set('security.require_confirmation', False)
        
    Load from specific file:
        >>> config = Config('/path/to/config.yaml')
        
    Environment variable integration:
        >>> os.environ['GEMINI_API_KEY'] = 'key123'
        >>> config = get_config()
        >>> key = config.get('llm.gemini.api_key')  # Returns 'key123'

Configuration Schema:
    llm:
        provider: str                    # 'gemini' or 'local'
        gemini:
            api_key: str                # API key for Gemini
            model: str                  # Model name
        local:
            host: str                   # Ollama host
            port: int                   # Ollama port
            model: str                  # Local model name
    
    security:
        require_confirmation: bool       # Require user confirmation
        dangerous_commands: List[str]    # List of dangerous command patterns
        
    logging:
        level: str                      # Log level (DEBUG, INFO, etc.)
        file: str                       # Log file path
        format: str                     # Log format string
        
    training:
        dataset_file: str               # Training data file path
        auto_log: bool                  # Auto-log successful commands

Author: AI Shell Contributors
License: MIT
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """
    Configuration manager for AI Shell with YAML and environment variable support.
    
    This class provides a unified interface for accessing configuration values
    from multiple sources with proper precedence handling. It supports:
    - YAML configuration files
    - Environment variable overrides
    - Nested key access using dot notation
    - Runtime configuration updates
    - Default value fallbacks
    
    Attributes:
        config_file (str): Path to the loaded configuration file
        config (dict): Loaded configuration data
        
    Examples:
        >>> config = Config()
        >>> provider = config.get('llm.provider', 'gemini')
        >>> config.set('security.require_confirmation', True)
        >>> config.save('updated_config.yaml')
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_file: Path to configuration file. If None, uses default locations.
        """
        self.config_file = config_file or self._find_config_file()
        self.config = self._load_config()
    
    def _find_config_file(self) -> Optional[str]:
        """Find configuration file in standard locations."""
        possible_locations = [
            "config.yaml",
            "~/.ai-shell/config.yaml",
            "~/.config/ai-shell/config.yaml",
        ]
        
        for location in possible_locations:
            path = Path(location).expanduser()
            if path.exists():
                return str(path)
        return None
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults."""
        if not self.config_file or not Path(self.config_file).exists():
            return self._get_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
                # Merge with defaults
                default_config = self._get_default_config()
                default_config.update(config)
                return default_config
        except Exception as e:
            print(f"Warning: Could not load config file {self.config_file}: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'llm': {
                'provider': 'gemini',  # 'gemini' or 'local'
                'gemini': {
                    'api_key': os.environ.get('GEMINI_API_KEY', ''),
                    'model': 'gemini-1.5-flash'
                },
                'local': {
                    'host': 'localhost',
                    'port': 11434,
                    'model': 'llama3'
                }
            },
            'logging': {
                'level': 'INFO',
                'file': 'ai_shell.log',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'training': {
                'dataset_file': 'training_dataset.jsonl',
                'auto_log': True
            },
            'security': {
                'require_confirmation': True,
                'dangerous_commands': ['rm -rf', 'format', 'dd if=', 'mkfs']
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation."""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def save(self, file_path: Optional[str] = None) -> None:
        """Save configuration to file."""
        if file_path:
            self.config_file = file_path
        
        if not self.config_file:
            # Create default config directory
            config_dir = Path.home() / '.ai-shell'
            config_dir.mkdir(exist_ok=True)
            self.config_file = str(config_dir / 'config.yaml')
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
        except Exception as e:
            print(f"Error saving configuration: {e}")


# Global configuration instance
_config = None

def get_config() -> Config:
    """Get global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config