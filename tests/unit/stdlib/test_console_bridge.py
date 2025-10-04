"""Unit tests for console_bridge module migration."""

import pytest
import sys
from io import StringIO
from mlpy.stdlib.console_bridge import Console, console
from mlpy.stdlib.decorators import get_module_metadata, _MODULE_REGISTRY


class TestConsoleModuleRegistration:
    """Test that Console module is properly registered with decorators."""

    def test_console_module_registered(self):
        """Test that console module is in global registry."""
        assert "console" in _MODULE_REGISTRY
        assert _MODULE_REGISTRY["console"] == Console

    def test_console_module_metadata(self):
        """Test console module metadata is correct."""
        metadata = get_module_metadata("console")
        assert metadata is not None
        assert metadata.name == "console"
        assert metadata.description == "Console output and logging functionality"
        assert "console.write" in metadata.capabilities
        assert "console.error" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_console_has_function_metadata(self):
        """Test that all console functions have metadata."""
        metadata = get_module_metadata("console")

        # Check all 5 methods are registered
        assert len(metadata.functions) == 5
        assert "log" in metadata.functions
        assert "error" in metadata.functions
        assert "warn" in metadata.functions
        assert "info" in metadata.functions
        assert "debug" in metadata.functions

    def test_console_function_capabilities(self):
        """Test that console functions have correct capabilities."""
        metadata = get_module_metadata("console")

        # log, info, debug require console.write
        assert metadata.functions["log"].capabilities == ["console.write"]
        assert metadata.functions["info"].capabilities == ["console.write"]
        assert metadata.functions["debug"].capabilities == ["console.write"]

        # error, warn require console.error
        assert metadata.functions["error"].capabilities == ["console.error"]
        assert metadata.functions["warn"].capabilities == ["console.error"]


class TestConsoleFunctionality:
    """Test that console functions still work after migration."""

    def test_console_log(self, capsys):
        """Test console.log() outputs to stdout."""
        console.log("Hello", "World")
        captured = capsys.readouterr()
        assert captured.out == "Hello World\n"
        assert captured.err == ""

    def test_console_info(self, capsys):
        """Test console.info() outputs with INFO prefix."""
        console.info("Information")
        captured = capsys.readouterr()
        assert captured.out == "INFO: Information\n"
        assert captured.err == ""

    def test_console_debug(self, capsys):
        """Test console.debug() outputs with DEBUG prefix."""
        console.debug("Debug message")
        captured = capsys.readouterr()
        assert captured.out == "DEBUG: Debug message\n"
        assert captured.err == ""

    def test_console_error(self, capsys):
        """Test console.error() outputs to stderr."""
        console.error("Error message")
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == "Error message\n"

    def test_console_warn(self, capsys):
        """Test console.warn() outputs with WARNING prefix to stderr."""
        console.warn("Warning message")
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == "WARNING: Warning message\n"

    def test_console_multiple_arguments(self, capsys):
        """Test console functions handle multiple arguments."""
        console.log("a", "b", "c", 123)
        captured = capsys.readouterr()
        assert captured.out == "a b c 123\n"


class TestConsoleInstance:
    """Test global console instance."""

    def test_console_is_instance_of_console_class(self):
        """Test that console is an instance of Console."""
        assert isinstance(console, Console)

    def test_console_has_decorated_methods(self):
        """Test that console instance has all decorated methods."""
        assert hasattr(console, "log")
        assert hasattr(console, "error")
        assert hasattr(console, "warn")
        assert hasattr(console, "info")
        assert hasattr(console, "debug")

        # Check they have metadata
        assert hasattr(console.log, "_ml_function_metadata")
        assert hasattr(console.error, "_ml_function_metadata")
        assert hasattr(console.warn, "_ml_function_metadata")
        assert hasattr(console.info, "_ml_function_metadata")
        assert hasattr(console.debug, "_ml_function_metadata")
