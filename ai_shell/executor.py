"""Command execution and security utilities for AI Shell."""

import shlex
import subprocess
import json
import time
from typing import Optional, Tuple

from .config import get_config
from .ui import colors, format_error, format_warning, format_info, format_success


class SecurityChecker:
    """Security checker for command validation."""

    def __init__(self):
        self.config = get_config()
        self.dangerous_commands = self.config.get(
            "security.dangerous_commands",
            [
                "rm -rf",
                "format",
                "dd if=",
                "mkfs",
                "fdisk",
                "parted",
                "wipefs",
                "shred",
                "chmod 777",
                "chown -R root",
            ],
        )

    def is_dangerous_command(self, command: str) -> bool:
        """Check if a command is potentially dangerous."""
        command_lower = command.lower().strip()
        return any(dangerous in command_lower for dangerous in self.dangerous_commands)

    def validate_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """Validate a command for security issues.

        Returns:
            Tuple of (is_valid, warning_message)
        """
        if not command or not command.strip():
            return False, "Empty command"

        if self.is_dangerous_command(command):
            return False, "This command is potentially dangerous and has been blocked"

        # Check for suspicious patterns
        suspicious_patterns = [
            "&&",
            "||",
            ";",  # Command chaining
            ">",
            ">>",
            "<",  # Redirection
            "|",  # Pipes
            "$(",  # Command substitution
            "`",  # Backticks
        ]

        has_suspicious = any(pattern in command for pattern in suspicious_patterns)
        if has_suspicious:
            return (
                True,
                "This command contains advanced shell features - please review carefully",
            )

        return True, None


class TrainingDataLogger:
    """Logger for training data collection."""

    def __init__(self):
        self.config = get_config()
        self.dataset_file = self.config.get(
            "training.dataset_file", "training_dataset.jsonl"
        )
        self.auto_log = self.config.get("training.auto_log", True)

    def log_training_pair(
        self, prompt: str, command: str, feedback: str = "positive"
    ) -> None:
        """Log a prompt-completion pair to the training dataset."""
        if not self.auto_log:
            return

        data = {
            "prompt": prompt,
            "completion": command,
            "feedback": feedback,
            "timestamp": time.time(),
        }

        try:
            with open(self.dataset_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(data) + "\n")
            print(format_info(f"Feedback logged to {self.dataset_file}"))
        except IOError as e:
            print(format_error(f"Could not write to dataset file: {e}"))


class CommandExecutor:
    """Command execution with security and logging."""

    def __init__(self):
        self.security_checker = SecurityChecker()
        self.training_logger = TrainingDataLogger()
        self.config = get_config()

    def execute_command(self, command: str, user_prompt: str) -> bool:
        """Execute a command with security checks and user confirmation.

        Returns:
            True if command executed successfully, False otherwise
        """
        if not command:
            print(format_warning("No command to execute"))
            return False

        # Security validation
        is_valid, warning = self.security_checker.validate_command(command)
        if not is_valid:
            print(format_error(warning))
            return False

        if warning:
            print(format_warning(warning))

        # Display command and ask for confirmation
        print(
            f"\nI am about to execute this command: {colors.COMMAND}{command}{colors.RESET}"
        )

        if command.strip().startswith("sudo"):
            print(format_warning("This command requires administrator privileges"))

        # Get user confirmation if required
        if self.config.get("security.require_confirmation", True):
            try:
                confirm = input("Do you want to proceed? [y/n] ").lower().strip()
                if confirm != "y":
                    print("Execution cancelled.")
                    return False
            except (KeyboardInterrupt, EOFError):
                print("\nExecution cancelled.")
                return False

        # Execute the command
        return self._run_command(command, user_prompt)

    def _run_command(self, command: str, user_prompt: str) -> bool:
        """Run the command and handle output."""
        try:
            print(f"\n{format_info('--- Command Output ---')}")

            # Determine if we need shell=True
            needs_shell = any(char in command for char in ["|", ">", "<", "&", ";"])
            process_args = command if needs_shell else shlex.split(command)

            # Start process
            process = subprocess.Popen(
                process_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=needs_shell,
                bufsize=1,
                universal_newlines=True,
            )

            # Stream output
            if process.stdout:
                for line in iter(process.stdout.readline, ""):
                    print(line, end="", flush=True)
                process.stdout.close()

            return_code = process.wait()
            print(f"\n{format_info('----------------------')}")

            # Handle feedback and logging
            if return_code == 0:
                print(format_success("Command executed successfully"))
                self._handle_successful_execution(user_prompt, command)
                return True
            else:
                print(format_error(f"Command finished with exit code: {return_code}"))
                self._handle_failed_execution(user_prompt, command)
                return False

        except FileNotFoundError:
            command_name = shlex.split(command)[0] if command else "unknown"
            print(format_error(f"Command not found: '{command_name}'"))
            return False
        except Exception as e:
            print(format_error(f"An unexpected error occurred: {e}"))
            return False

    def _handle_successful_execution(self, user_prompt: str, command: str):
        """Handle successful command execution feedback."""
        try:
            feedback = (
                input("Was this command correct and useful? [y/n] ").lower().strip()
            )
            if feedback == "y":
                self.training_logger.log_training_pair(user_prompt, command, "positive")
            elif feedback == "n":
                self.training_logger.log_training_pair(user_prompt, command, "negative")
        except (KeyboardInterrupt, EOFError):
            pass

    def _handle_failed_execution(self, user_prompt: str, command: str):
        """Handle failed command execution feedback."""
        try:
            print(
                format_warning(
                    "If you know the correct command, please enter it to improve the AI"
                )
            )
            correction = input("Correct command (or press Enter to skip): ").strip()
            if correction:
                # Validate the correction
                is_valid, warning = self.security_checker.validate_command(correction)
                if is_valid:
                    self.training_logger.log_training_pair(
                        user_prompt, correction, "correction"
                    )
                else:
                    print(format_error(f"Correction rejected: {warning}"))
        except (KeyboardInterrupt, EOFError):
            pass


# Global executor instance
_executor = None


def get_executor() -> CommandExecutor:
    """Get global command executor instance."""
    global _executor
    if _executor is None:
        _executor = CommandExecutor()
    return _executor
