"""Tests for AI Shell audit logging functionality."""

import tempfile
import json
import time
import os
from pathlib import Path
from unittest.mock import patch

from ai_shell.audit import AuditLogger, get_audit_logger


class TestAuditLogger:
    """Test cases for AuditLogger class."""

    def test_audit_logger_initialization(self):
        """Test AuditLogger initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_file = Path(temp_dir) / "test_audit.jsonl"
            
            with patch("ai_shell.audit.get_config") as mock_config:
                mock_config.return_value.get.side_effect = lambda key, default: {
                    "logging.audit_file": str(audit_file),
                    "logging.audit_enabled": True,
                }.get(key, default)
                
                logger = AuditLogger()
                assert logger.enabled is True
                assert logger.audit_file == str(audit_file)

    def test_log_command_attempt(self):
        """Test logging command attempts."""
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_file = Path(temp_dir) / "test_audit.jsonl"
            
            with patch("ai_shell.audit.get_config") as mock_config:
                mock_config.return_value.get.side_effect = lambda key, default: {
                    "logging.audit_file": str(audit_file),
                    "logging.audit_enabled": True,
                }.get(key, default)
                
                logger = AuditLogger()
                logger.log_command_attempt("ls -la", "list files", "allowed")
                
                # Verify log entry
                assert audit_file.exists()
                with open(audit_file, 'r') as f:
                    entry = json.loads(f.read().strip())
                    assert entry["event_type"] == "command_attempt"
                    assert entry["command"] == "ls -la"
                    assert entry["user_prompt"] == "list files"
                    assert entry["security_status"] == "allowed"

    def test_log_command_execution(self):
        """Test logging command execution results."""
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_file = Path(temp_dir) / "test_audit.jsonl"
            
            with patch("ai_shell.audit.get_config") as mock_config:
                mock_config.return_value.get.side_effect = lambda key, default: {
                    "logging.audit_file": str(audit_file),
                    "logging.audit_enabled": True,
                }.get(key, default)
                
                logger = AuditLogger()
                logger.log_command_execution("ls -la", "list files", 0, 0.5, True)
                
                # Verify log entry
                assert audit_file.exists()
                with open(audit_file, 'r') as f:
                    entry = json.loads(f.read().strip())
                    assert entry["event_type"] == "command_execution"
                    assert entry["command"] == "ls -la"
                    assert entry["exit_code"] == 0
                    assert entry["success"] is True
                    assert entry["execution_time_seconds"] == 0.5
                    assert entry["user_confirmed"] is True

    def test_log_security_event(self):
        """Test logging security events."""
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_file = Path(temp_dir) / "test_audit.jsonl"
            
            with patch("ai_shell.audit.get_config") as mock_config:
                mock_config.return_value.get.side_effect = lambda key, default: {
                    "logging.audit_file": str(audit_file),
                    "logging.audit_enabled": True,
                }.get(key, default)
                
                logger = AuditLogger()
                logger.log_security_event(
                    "blocked_command", 
                    "rm -rf /", 
                    {"reason": "dangerous command"}
                )
                
                # Verify log entry
                assert audit_file.exists()
                with open(audit_file, 'r') as f:
                    entry = json.loads(f.read().strip())
                    assert entry["event_type"] == "security_event"
                    assert entry["security_event_type"] == "blocked_command"
                    assert entry["command"] == "rm -rf /"
                    assert entry["details"]["reason"] == "dangerous command"

    def test_disabled_logging(self):
        """Test that logging is disabled when configured."""
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_file = Path(temp_dir) / "test_audit.jsonl"
            
            with patch("ai_shell.audit.get_config") as mock_config:
                mock_config.return_value.get.side_effect = lambda key, default: {
                    "logging.audit_file": str(audit_file),
                    "logging.audit_enabled": False,
                }.get(key, default)
                
                logger = AuditLogger()
                logger.log_command_attempt("ls -la", "list files", "allowed")
                
                # Verify no log file created
                assert not audit_file.exists()

    def test_get_recent_commands(self):
        """Test retrieving recent commands."""
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_file = Path(temp_dir) / "test_audit.jsonl"
            
            with patch("ai_shell.audit.get_config") as mock_config:
                mock_config.return_value.get.side_effect = lambda key, default: {
                    "logging.audit_file": str(audit_file),
                    "logging.audit_enabled": True,
                }.get(key, default)
                
                logger = AuditLogger()
                
                # Log multiple commands
                logger.log_command_execution("ls", "list", 0, 0.1, True)
                logger.log_command_execution("pwd", "current dir", 0, 0.1, True)
                logger.log_command_execution("whoami", "user", 0, 0.1, True)
                
                # Get recent commands
                commands = logger.get_recent_commands(2)
                assert len(commands) == 2
                assert commands[0]["command"] == "whoami"  # Most recent first
                assert commands[1]["command"] == "pwd"

    def test_get_security_events(self):
        """Test retrieving security events."""
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_file = Path(temp_dir) / "test_audit.jsonl"
            
            with patch("ai_shell.audit.get_config") as mock_config:
                mock_config.return_value.get.side_effect = lambda key, default: {
                    "logging.audit_file": str(audit_file),
                    "logging.audit_enabled": True,
                }.get(key, default)
                
                logger = AuditLogger()
                
                # Log security events
                logger.log_security_event("blocked_command", "rm -rf /", {})
                logger.log_security_event("suspicious_pattern", "ls; rm -rf", {})
                
                # Get security events
                events = logger.get_security_events(24)
                assert len(events) == 2
                assert all(event["event_type"] == "security_event" for event in events)

    def test_generate_audit_report(self):
        """Test generating audit reports."""
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_file = Path(temp_dir) / "test_audit.jsonl"
            
            with patch("ai_shell.audit.get_config") as mock_config:
                mock_config.return_value.get.side_effect = lambda key, default: {
                    "logging.audit_file": str(audit_file),
                    "logging.audit_enabled": True,
                }.get(key, default)
                
                logger = AuditLogger()
                
                # Log various events
                logger.log_command_execution("ls", "list", 0, 0.1, True)
                logger.log_command_execution("pwd", "dir", 1, 0.1, True)  # Failed
                logger.log_security_event("blocked_command", "rm -rf /", {})
                
                # Generate report
                report = logger.generate_audit_report()
                
                assert report["total_commands"] == 2
                assert report["successful_commands"] == 1
                assert report["failed_commands"] == 1
                assert report["security_events"] == 1
                assert "ls" in report["top_commands"]
                assert "pwd" in report["top_commands"]

    def test_audit_file_directory_creation(self):
        """Test that audit file directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_file = Path(temp_dir) / "nested" / "dir" / "test_audit.jsonl"
            
            with patch("ai_shell.audit.get_config") as mock_config:
                mock_config.return_value.get.side_effect = lambda key, default: {
                    "logging.audit_file": str(audit_file),
                    "logging.audit_enabled": True,
                }.get(key, default)
                
                logger = AuditLogger()
                logger.log_command_attempt("test", "test", "allowed")
                
                # Verify directory and file created
                assert audit_file.parent.exists()
                assert audit_file.exists()

    def test_get_audit_logger_singleton(self):
        """Test that get_audit_logger returns singleton instance."""
        logger1 = get_audit_logger()
        logger2 = get_audit_logger()
        assert logger1 is logger2

    def test_json_serialization_safety(self):
        """Test that audit logging handles complex data safely."""
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_file = Path(temp_dir) / "test_audit.jsonl"
            
            with patch("ai_shell.audit.get_config") as mock_config:
                mock_config.return_value.get.side_effect = lambda key, default: {
                    "logging.audit_file": str(audit_file),
                    "logging.audit_enabled": True,
                }.get(key, default)
                
                logger = AuditLogger()
                
                # Log event with complex details
                complex_details = {
                    "nested": {"data": True},
                    "list": [1, 2, 3],
                    "special_chars": "unicode: 🔒",
                }
                
                logger.log_security_event(
                    "test_event", 
                    "test command", 
                    complex_details
                )
                
                # Verify it can be read back
                with open(audit_file, 'r') as f:
                    entry = json.loads(f.read().strip())
                    assert entry["details"]["nested"]["data"] is True
                    assert entry["details"]["list"] == [1, 2, 3]
                    assert "🔒" in entry["details"]["special_chars"]