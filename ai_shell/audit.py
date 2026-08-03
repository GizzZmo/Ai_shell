"""Command audit logging for AI Shell."""

import json
import time
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from .config import get_config
from .ui import format_info, format_error


class AuditLogger:
    """
    Command audit logger for security and compliance tracking.
    
    Logs all executed commands with metadata including:
    - Command executed
    - User prompt that generated the command
    - Execution timestamp
    - Success/failure status
    - User confirmation details
    - Security warnings
    """

    def __init__(self):
        self.config = get_config()
        self.audit_file = self.config.get("logging.audit_file", "ai_shell_audit.jsonl")
        self.enabled = self.config.get("logging.audit_enabled", True)
        
        # Ensure audit log directory exists
        audit_path = Path(self.audit_file)
        audit_path.parent.mkdir(parents=True, exist_ok=True)

    def log_command_attempt(
        self,
        command: str,
        user_prompt: str,
        security_status: str = "allowed",
        warning_message: Optional[str] = None,
    ) -> None:
        """Log a command execution attempt."""
        if not self.enabled:
            return

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "unix_timestamp": time.time(),
            "event_type": "command_attempt",
            "command": command,
            "user_prompt": user_prompt,
            "security_status": security_status,  # allowed, blocked, warning
            "warning_message": warning_message,
            "user": os.getenv("USER", "unknown"),
            "working_directory": os.getcwd(),
        }

        self._write_log_entry(log_entry)

    def log_command_execution(
        self,
        command: str,
        user_prompt: str,
        exit_code: int,
        execution_time: float,
        user_confirmed: bool = True,
    ) -> None:
        """Log command execution results."""
        if not self.enabled:
            return

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "unix_timestamp": time.time(),
            "event_type": "command_execution",
            "command": command,
            "user_prompt": user_prompt,
            "exit_code": exit_code,
            "success": exit_code == 0,
            "execution_time_seconds": execution_time,
            "user_confirmed": user_confirmed,
            "user": os.getenv("USER", "unknown"),
            "working_directory": os.getcwd(),
        }

        self._write_log_entry(log_entry)

    def log_security_event(
        self,
        event_type: str,
        command: str,
        details: Dict[str, Any],
    ) -> None:
        """Log security-related events."""
        if not self.enabled:
            return

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "unix_timestamp": time.time(),
            "event_type": "security_event",
            "security_event_type": event_type,  # blocked_command, suspicious_pattern, etc.
            "command": command,
            "details": details,
            "user": os.getenv("USER", "unknown"),
            "working_directory": os.getcwd(),
        }

        self._write_log_entry(log_entry)

    def _write_log_entry(self, entry: Dict[str, Any]) -> None:
        """Write log entry to audit file."""
        try:
            with open(self.audit_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except IOError as e:
            print(format_error(f"Failed to write audit log: {e}"))

    def get_recent_commands(self, limit: int = 10) -> list:
        """Get recent command executions from audit log."""
        if not os.path.exists(self.audit_file):
            return []

        commands = []
        try:
            with open(self.audit_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if entry.get("event_type") == "command_execution":
                            commands.append(entry)
                    except json.JSONDecodeError:
                        continue

            # Return most recent commands first
            return commands[-limit:][::-1]

        except IOError:
            return []

    def get_security_events(self, hours: int = 24) -> list:
        """Get security events from the last N hours."""
        if not os.path.exists(self.audit_file):
            return []

        cutoff_time = time.time() - (hours * 3600)
        events = []

        try:
            with open(self.audit_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if (
                            entry.get("event_type") == "security_event"
                            and entry.get("unix_timestamp", 0) > cutoff_time
                        ):
                            events.append(entry)
                    except json.JSONDecodeError:
                        continue

            return events

        except IOError:
            return []

    def generate_audit_report(self) -> Dict[str, Any]:
        """Generate an audit report summary."""
        if not os.path.exists(self.audit_file):
            return {"error": "No audit log found"}

        report = {
            "total_commands": 0,
            "successful_commands": 0,
            "failed_commands": 0,
            "blocked_commands": 0,
            "security_events": 0,
            "unique_users": set(),
            "most_recent_activity": None,
            "top_commands": {},
        }

        try:
            with open(self.audit_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        
                        if entry.get("user"):
                            report["unique_users"].add(entry["user"])
                        
                        if entry.get("timestamp"):
                            report["most_recent_activity"] = entry["timestamp"]

                        if entry.get("event_type") == "command_execution":
                            report["total_commands"] += 1
                            if entry.get("success"):
                                report["successful_commands"] += 1
                            else:
                                report["failed_commands"] += 1
                                
                            # Track command frequency
                            cmd = entry.get("command", "").split()[0] if entry.get("command") else "unknown"
                            report["top_commands"][cmd] = report["top_commands"].get(cmd, 0) + 1

                        elif entry.get("event_type") == "security_event":
                            report["security_events"] += 1
                            
                        elif entry.get("security_status") == "blocked":
                            report["blocked_commands"] += 1

                    except json.JSONDecodeError:
                        continue

            # Convert set to list for JSON serialization
            report["unique_users"] = list(report["unique_users"])
            
            # Sort top commands by frequency
            report["top_commands"] = dict(
                sorted(report["top_commands"].items(), key=lambda x: x[1], reverse=True)[:10]
            )

            return report

        except IOError as e:
            return {"error": f"Failed to read audit log: {e}"}


# Global audit logger instance
_audit_logger = None


def get_audit_logger() -> AuditLogger:
    """Get global audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger