"""Tests for AI Shell configuration module."""

import pytest
import yaml
from pathlib import Path
from ai_shell.config import Config


def test_config_initialization():
    """Test basic configuration initialization."""
    config = Config()
    assert config.config is not None
    assert isinstance(config.config, dict)


def test_config_get_default_values():
    """Test getting default configuration values."""
    config = Config()
    
    # Test default values
    assert config.get('llm.provider') == 'gemini'
    assert config.get('logging.level') == 'INFO'
    assert config.get('security.require_confirmation') is True
    assert config.get('nonexistent.key', 'default') == 'default'


def test_config_set_values():
    """Test setting configuration values."""
    config = Config()
    
    config.set('test.key', 'test_value')
    assert config.get('test.key') == 'test_value'
    
    config.set('nested.deep.key', 42)
    assert config.get('nested.deep.key') == 42


def test_config_load_from_file(mock_config_file):
    """Test loading configuration from file."""
    config = Config(mock_config_file)
    
    assert config.get('llm.provider') == 'gemini'
    assert config.get('llm.gemini.api_key') == 'test_key'
    assert config.get('security.require_confirmation') is False


def test_config_save_to_file(temp_config_dir):
    """Test saving configuration to file."""
    config = Config()
    config.set('test.key', 'test_value')
    
    config_file = Path(temp_config_dir) / "test_config.yaml"
    config.save(str(config_file))
    
    # Verify file was created and contains expected data
    assert config_file.exists()
    
    with open(config_file, 'r') as f:
        saved_config = yaml.safe_load(f)
    
    assert saved_config['test']['key'] == 'test_value'


def test_config_dangerous_commands():
    """Test default dangerous commands list."""
    config = Config()
    dangerous_commands = config.get('security.dangerous_commands', [])
    
    assert 'rm -rf' in dangerous_commands
    assert 'format' in dangerous_commands
    assert isinstance(dangerous_commands, list)


def test_config_nested_access():
    """Test deeply nested configuration access."""
    config = Config()
    
    # Test non-existent nested key
    assert config.get('a.b.c.d.e', 'default') == 'default'
    
    # Set nested value
    config.set('a.b.c.d.e', 'nested_value')
    assert config.get('a.b.c.d.e') == 'nested_value'