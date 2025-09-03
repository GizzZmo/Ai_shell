"""Configuration management for AI Shell."""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """Configuration manager for AI Shell."""
    
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