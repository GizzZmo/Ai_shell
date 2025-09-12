"""Tests for AI Shell executor module."""

import tempfile
import json
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

from ai_shell.executor import SecurityChecker, TrainingDataLogger, CommandExecutor


class TestSecurityChecker:
    """Test cases for SecurityChecker class."""

    def test_security_checker_initialization(self):
        """Test SecurityChecker initialization."""
        checker = SecurityChecker()
        assert checker is not None
        assert hasattr(checker, "dangerous_commands")

    def test_dangerous_command_detection(self):
        """Test detection of dangerous commands."""
        checker = SecurityChecker()

        # Test dangerous commands
        assert checker.is_dangerous_command("rm -rf /")
        assert checker.is_dangerous_command("format C:")
        assert checker.is_dangerous_command("dd if=/dev/zero of=/dev/sda")
        assert checker.is_dangerous_command("sudo rm -rf")

        # Test safe commands
        assert not checker.is_dangerous_command("ls -la")
        assert not checker.is_dangerous_command("cat file.txt")
        assert not checker.is_dangerous_command("mkdir new_folder")

    def test_command_validation(self):
        """Test command validation logic."""
        checker = SecurityChecker()

        # Test safe command
        is_safe, message = checker.validate_command("ls -la")
        assert is_safe
        assert message is None

        # Test dangerous command
        is_safe, message = checker.validate_command("rm -rf /")
        assert not is_safe
        assert "dangerous" in message.lower()

    def test_custom_dangerous_commands(self):
        """Test custom dangerous commands configuration."""
        with patch("ai_shell.executor.get_config") as mock_config:
            mock_config.return_value.get.return_value = ["custom_dangerous_cmd"]
            checker = SecurityChecker()
            assert checker.is_dangerous_command("custom_dangerous_cmd")


class TestTrainingDataLogger:
    """Test cases for TrainingDataLogger class."""

    def test_training_logger_initialization(self):
        """Test TrainingDataLogger initialization."""
        logger = TrainingDataLogger()
        assert logger is not None

    def test_log_training_pair(self, tmp_path):
        """Test logging training data pairs."""
        # Create temporary dataset file
        dataset_file = tmp_path / "test_dataset.jsonl"

        with patch("ai_shell.executor.get_config") as mock_config:
            mock_config.return_value.get.side_effect = lambda key, default=None: {
                "training.dataset_file": str(dataset_file),
                "training.auto_log": True,
            }.get(key, default)

            logger = TrainingDataLogger()
            logger.log_training_pair("list files", "ls -la", "positive")

            # Verify data was logged
            assert dataset_file.exists()
            with open(dataset_file, "r") as f:
                data = json.loads(f.read())
                assert data["prompt"] == "list files"
                assert data["completion"] == "ls -la"
                assert data["feedback"] == "positive"

    def test_auto_log_disabled(self, tmp_path):
        """Test that logging is skipped when auto_log is disabled."""
        dataset_file = tmp_path / "test_dataset.jsonl"

        with patch("ai_shell.executor.get_config") as mock_config:
            mock_config.return_value.get.side_effect = lambda key, default=None: {
                "training.dataset_file": str(dataset_file),
                "training.auto_log": False,
            }.get(key, default)

            logger = TrainingDataLogger()
            logger.log_training_pair("test", "test", "positive")

            # Verify no data was logged
            assert not dataset_file.exists()


class TestCommandExecutor:
    """Test cases for CommandExecutor class."""

    def test_executor_initialization(self):
        """Test CommandExecutor initialization."""
        executor = CommandExecutor()
        assert executor is not None
        assert hasattr(executor, "security_checker")
        assert hasattr(executor, "training_logger")

    @patch("ai_shell.executor.subprocess.Popen")
    @patch("builtins.input")
    def test_safe_command_execution(self, mock_input, mock_popen):
        """Test execution of safe commands."""
        # Mock user input for confirmation and feedback
        mock_input.side_effect = ["y", "y"]  # confirm execution, positive feedback
        
        # Mock subprocess
        mock_process = MagicMock()
        mock_process.stdout.readline.side_effect = ["test output\n", ""]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        executor = CommandExecutor()
        result = executor.execute_command("ls -la", "list files")

        assert result is True
        mock_popen.assert_called_once()

    @patch("builtins.input", return_value="n")
    def test_dangerous_command_rejection(self, mock_input):
        """Test rejection of dangerous commands."""
        executor = CommandExecutor()
        result = executor.execute_command("rm -rf /", "delete everything")

        assert result is False

    @patch("ai_shell.executor.subprocess.Popen")
    @patch("builtins.input")
    def test_command_execution_failure(self, mock_input, mock_popen):
        """Test handling of command execution failures."""
        # Mock user input for confirmation and feedback
        mock_input.side_effect = ["y", "n"]  # confirm execution, negative feedback
        
        # Mock subprocess with failure
        mock_process = MagicMock()
        mock_process.stdout.readline.side_effect = ["error output\n", ""]
        mock_process.wait.return_value = 1
        mock_popen.return_value = mock_process

        executor = CommandExecutor()
        result = executor.execute_command("nonexistent_command", "run fake command")

        assert result is False

    @patch("ai_shell.executor.get_config")
    @patch("ai_shell.executor.subprocess.Popen")
    @patch("builtins.input")
    def test_no_confirmation_mode(self, mock_input, mock_popen, mock_config):
        """Test execution without confirmation when configured."""
        mock_config.return_value.get.side_effect = lambda key, default=None: {
            "security.require_confirmation": False
        }.get(key, default)

        # Mock successful execution  
        mock_process = MagicMock()
        mock_process.stdout.readline.side_effect = ["output\n", ""]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process
        
        # Mock feedback input (this will still be called for feedback)
        mock_input.return_value = "y"

        executor = CommandExecutor()
        result = executor.execute_command("ls", "list files")

        assert result is True
        # Should only be called once for feedback, not for confirmation
        assert mock_input.call_count == 1

    def test_get_executor_singleton(self):
        """Test that get_executor returns singleton instance."""
        from ai_shell.executor import get_executor

        executor1 = get_executor()
        executor2 = get_executor()

        assert executor1 is executor2