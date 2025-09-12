"""Test configuration for AI Shell."""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_config_dir():
    """Create a temporary directory for test configuration."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_config_file(temp_config_dir):
    """Create a mock configuration file."""
    config_content = """
llm:
  provider: gemini
  gemini:
    api_key: test_key
    model: gemini-1.5-flash
  local:
    host: localhost
    port: 11434
    model: llama3

logging:
  level: INFO
  file: test.log
  format: '%(asctime)s - %(levelname)s - %(message)s'

training:
  dataset_file: test_dataset.jsonl
  auto_log: true

security:
  require_confirmation: false
  dangerous_commands:
    - rm -rf
    - format
"""
    config_path = Path(temp_config_dir) / "config.yaml"
    with open(config_path, "w") as f:
        f.write(config_content)
    return str(config_path)
