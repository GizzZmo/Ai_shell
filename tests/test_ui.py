"""Tests for AI Shell UI module."""

import io
import sys
from unittest.mock import patch

from ai_shell.ui import (
    colors,
    format_error,
    format_warning,
    format_info,
    format_success,
    format_command_output,
    print_banner,
    print_mode_selection,
    print_provider_selection,
    print_local_model_selection,
)


class TestColorFormatting:
    """Test cases for color formatting functions."""

    def test_format_error(self):
        """Test error message formatting."""
        message = "Test error"
        formatted = format_error(message)
        assert colors.ERROR in formatted
        assert colors.RESET in formatted
        assert message in formatted

    def test_format_warning(self):
        """Test warning message formatting."""
        message = "Test warning"
        formatted = format_warning(message)
        assert colors.WARNING in formatted
        assert colors.RESET in formatted
        assert message in formatted

    def test_format_info(self):
        """Test info message formatting."""
        message = "Test info"
        formatted = format_info(message)
        assert colors.INFO in formatted
        assert colors.RESET in formatted
        assert message in formatted

    def test_format_success(self):
        """Test success message formatting."""
        message = "Test success"
        formatted = format_success(message)
        assert colors.SUCCESS in formatted
        assert colors.RESET in formatted
        assert message in formatted

    def test_format_command_output(self):
        """Test command output formatting."""
        output = "command output"
        formatted = format_command_output(output)
        assert colors.COMMAND in formatted
        assert colors.RESET in formatted
        assert output in formatted


class TestPrintFunctions:
    """Test cases for print functions."""

    def test_print_banner(self):
        """Test banner printing."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_banner()
            output = mock_stdout.getvalue()
            assert "AI-Powered Shell Assistant" in output
            assert "v0.1.0" in output

    def test_print_mode_selection(self):
        """Test mode selection menu printing."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_mode_selection()
            output = mock_stdout.getvalue()
            assert "Choose an operating mode" in output
            assert "Command Translator" in output
            assert "AI Assistant" in output
            assert "Metasploit Assistant" in output
            assert "Wapiti Assistant" in output

    def test_print_provider_selection(self):
        """Test provider selection menu printing."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_provider_selection()
            output = mock_stdout.getvalue()
            assert "Choose an LLM provider" in output
            assert "Gemini" in output
            assert "Local LLM" in output

    def test_print_local_model_selection(self):
        """Test local model selection menu printing."""
        test_models = {
            "1": {"name": "Test Model 1", "size_gb": "4"},
            "2": {"name": "Test Model 2", "size_gb": "8"},
        }

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_local_model_selection(test_models)
            output = mock_stdout.getvalue()
            assert "choose a local LLM" in output
            assert "Test Model 1" in output
            assert "Test Model 2" in output
            assert "4 GB" in output
            assert "8 GB" in output


class TestColorConstants:
    """Test cases for color constants."""

    def test_colors_dictionary(self):
        """Test that colors object contains required attributes."""
        required_colors = [
            "INFO",
            "SUCCESS", 
            "WARNING",
            "ERROR",
            "RESET",
        ]

        for color in required_colors:
            assert hasattr(colors, color)
            assert isinstance(getattr(colors, color), str)

    def test_color_codes_are_strings(self):
        """Test that all color codes are strings."""
        color_attrs = [attr for attr in dir(colors) if not attr.startswith('_')]
        for color_name in color_attrs:
            color_code = getattr(colors, color_name)
            assert isinstance(color_code, str)
            assert len(color_code) > 0


class TestColoramaCompatibility:
    """Test cases for colorama compatibility."""

    def test_colorama_fallback(self):
        """Test that UI functions work without colorama."""
        # Test that functions don't crash when colorama is not available
        # This would be tested by temporarily mocking COLORAMA_AVAILABLE = False
        with patch("ai_shell.ui.COLORAMA_AVAILABLE", False):
            # Re-import to get fallback behavior
            import importlib
            import ai_shell.ui

            importlib.reload(ai_shell.ui)

            # Test basic functionality still works
            message = ai_shell.ui.format_error("test")
            assert "test" in message

    def test_format_functions_with_empty_input(self):
        """Test format functions with empty input."""
        assert format_error("") != ""
        assert format_warning("") != ""
        assert format_info("") != ""
        assert format_success("") != ""

    def test_format_functions_with_special_characters(self):
        """Test format functions with special characters."""
        special_text = "Test with 🎉 emojis and\nnewlines\ttabs"

        # Should not crash and should preserve the input
        assert special_text in format_error(special_text)
        assert special_text in format_warning(special_text)
        assert special_text in format_info(special_text)
        assert special_text in format_success(special_text)