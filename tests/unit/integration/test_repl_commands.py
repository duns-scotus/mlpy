"""Tests for integration REPL commands."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import asyncio

from mlpy.integration.repl_commands import (
    handle_async_command,
    handle_callback_command,
    handle_benchmark_command,
    dispatch_integration_command,
    print_integration_help,
)


class TestAsyncCommand:
    """Test the .async REPL command."""

    def test_async_command_with_no_code(self, capsys):
        """Test async command displays usage when no code provided."""
        session = Mock()
        handle_async_command(session, "")

        captured = capsys.readouterr()
        assert "Usage: .async" in captured.out
        assert "Example:" in captured.out

    @patch('mlpy.integration.async_executor.async_ml_execute')
    @patch('asyncio.run')
    def test_async_command_successful_execution(self, mock_run, mock_execute, capsys):
        """Test async command with successful execution."""
        session = Mock()

        # Mock successful result
        result = Mock()
        result.success = True
        result.value = 42
        result.transpile_time = 0.01
        mock_run.return_value = result

        handle_async_command(session, "x = 40 + 2;")

        captured = capsys.readouterr()
        assert "Executing async..." in captured.out
        assert "=> 42" in captured.out
        assert "Execution time:" in captured.out

    @patch('mlpy.integration.async_executor.async_ml_execute')
    @patch('asyncio.run')
    def test_async_command_with_error(self, mock_run, mock_execute, capsys):
        """Test async command with execution error."""
        session = Mock()

        # Mock error result
        result = Mock()
        result.success = False
        result.error = "Parse error"
        mock_run.return_value = result

        handle_async_command(session, "invalid syntax")

        captured = capsys.readouterr()
        assert "Error: Parse error" in captured.out

    @patch('mlpy.integration.async_executor.async_ml_execute')
    @patch('asyncio.run')
    def test_async_command_timeout(self, mock_run, mock_execute, capsys):
        """Test async command timeout handling."""
        session = Mock()
        mock_run.side_effect = asyncio.TimeoutError()

        handle_async_command(session, "long_running_task();")

        captured = capsys.readouterr()
        assert "timed out" in captured.out

    @patch('mlpy.integration.async_executor.async_ml_execute')
    @patch('asyncio.run')
    def test_async_command_exception(self, mock_run, mock_execute, capsys):
        """Test async command with general exception."""
        session = Mock()
        mock_run.side_effect = RuntimeError("Unexpected error")

        handle_async_command(session, "code;")

        captured = capsys.readouterr()
        assert "Error: Unexpected error" in captured.out


class TestCallbackCommand:
    """Test the .callback REPL command."""

    def test_callback_command_no_function_name(self, capsys):
        """Test callback command displays usage when no function name provided."""
        session = Mock()
        handle_callback_command(session, "")

        captured = capsys.readouterr()
        assert "Usage: .callback" in captured.out
        assert "Example:" in captured.out

    def test_callback_command_function_not_found(self, capsys):
        """Test callback command when function doesn't exist."""
        session = Mock()
        session.python_namespace = {}

        handle_callback_command(session, "nonexistent_function")

        captured = capsys.readouterr()
        assert "Error: Function 'nonexistent_function' not found" in captured.out

    @patch('mlpy.integration.ml_callback.ml_callback')
    def test_callback_command_successful(self, mock_ml_callback, capsys):
        """Test callback command with successful creation."""
        session = Mock()
        session.python_namespace = {"double": lambda x: x * 2}

        # Mock the callback creation
        callback_fn = lambda x: x * 2
        mock_ml_callback.return_value = callback_fn

        handle_callback_command(session, "double")

        captured = capsys.readouterr()
        assert "Callback" in captured.out
        assert "created successfully" in captured.out

    @patch('mlpy.integration.ml_callback.ml_callback')
    def test_callback_command_creation_error(self, mock_ml_callback, capsys):
        """Test callback command with creation error."""
        session = Mock()
        session.python_namespace = {"func": Mock()}

        # Mock callback creation failure
        mock_ml_callback.side_effect = Exception("Creation failed")

        handle_callback_command(session, "func")

        captured = capsys.readouterr()
        assert "Error creating callback" in captured.out


class TestBenchmarkCommand:
    """Test the .benchmark REPL command."""

    def test_benchmark_command_no_code(self, capsys):
        """Test benchmark command displays usage when no code provided."""
        session = Mock()
        handle_benchmark_command(session, "")

        captured = capsys.readouterr()
        assert "Usage: .benchmark" in captured.out

    @patch('mlpy.integration.testing.performance.PerformanceTester')
    @patch('asyncio.run')
    def test_benchmark_command_with_iterations(self, mock_run, mock_tester_class, capsys):
        """Test benchmark command with custom iterations."""
        session = Mock()

        # Mock the benchmark results
        mock_results = {
            'mean': 0.0015,  # 1.5ms
            'median': 0.0015,
            'std_dev': 0.0001,
            'min': 0.0014,
            'max': 0.0016
        }
        mock_run.return_value = mock_results

        handle_benchmark_command(session, "x = 1 + 1;", "10")

        captured = capsys.readouterr()
        assert "Running benchmark" in captured.out
        assert "Mean:" in captured.out

    @patch('mlpy.integration.testing.performance.PerformanceTester')
    @patch('asyncio.run')
    def test_benchmark_command_default_iterations(self, mock_run, mock_tester_class, capsys):
        """Test benchmark command with default iterations."""
        session = Mock()

        mock_results = {
            'mean': 0.002,
            'median': 0.002,
            'std_dev': 0.0001,
            'min': 0.0019,
            'max': 0.0021
        }
        mock_run.return_value = mock_results

        handle_benchmark_command(session, "calc();", "")

        captured = capsys.readouterr()
        assert "100 iterations" in captured.out

    @patch('mlpy.integration.testing.performance.PerformanceTester')
    @patch('asyncio.run')
    def test_benchmark_command_execution_error(self, mock_run, mock_tester_class, capsys):
        """Test benchmark command with execution error."""
        session = Mock()
        mock_run.side_effect = Exception("Execution failed")

        handle_benchmark_command(session, "invalid;", "5")

        captured = capsys.readouterr()
        assert "Error" in captured.out


class TestREPLCommandIntegration:
    """Test integration of REPL commands with session."""

    def test_all_commands_handle_empty_session(self):
        """Test all commands handle empty/minimal session gracefully."""
        session = Mock()
        session.python_namespace = {}

        # Should not crash
        handle_async_command(session, "")
        handle_callback_command(session, "")
        handle_benchmark_command(session, "")

    def test_commands_preserve_session_state(self):
        """Test commands don't corrupt session state."""
        session = Mock()
        original_namespace = {"x": 42}
        session.python_namespace = original_namespace.copy()

        # Run commands
        handle_async_command(session, "")
        handle_callback_command(session, "")

        # Namespace should still have original values
        assert "x" in session.python_namespace

    def test_benchmark_command_invalid_iterations_negative(self, capsys):
        """Test benchmark command with negative iterations."""
        session = Mock()
        handle_benchmark_command(session, "x = 1;", "-5")

        captured = capsys.readouterr()
        assert "must be >= 1" in captured.out

    def test_benchmark_command_invalid_iterations_zero(self, capsys):
        """Test benchmark command with zero iterations."""
        session = Mock()
        handle_benchmark_command(session, "x = 1;", "0")

        captured = capsys.readouterr()
        assert "must be >= 1" in captured.out

    def test_benchmark_command_invalid_iterations_string(self, capsys):
        """Test benchmark command with non-numeric iterations."""
        session = Mock()
        handle_benchmark_command(session, "x = 1;", "abc")

        captured = capsys.readouterr()
        assert "Invalid iterations value" in captured.out

    @patch('mlpy.integration.testing.performance.PerformanceTester')
    @patch('asyncio.run')
    def test_benchmark_command_timeout(self, mock_run, mock_tester_class, capsys):
        """Test benchmark command timeout handling."""
        session = Mock()
        mock_run.side_effect = asyncio.TimeoutError()

        handle_benchmark_command(session, "long_task();", "10")

        captured = capsys.readouterr()
        assert "timed out" in captured.out


class TestCommandDispatcher:
    """Test the command dispatcher."""

    def test_dispatch_non_dot_command_returns_false(self):
        """Test dispatcher returns False for non-dot commands."""
        session = Mock()
        result = dispatch_integration_command(session, "regular code")
        assert result is False

    def test_dispatch_empty_dot_command_returns_false(self):
        """Test dispatcher returns False for empty dot command."""
        session = Mock()
        result = dispatch_integration_command(session, ".")
        assert result is False

    @patch('mlpy.integration.repl_commands.INTEGRATION_COMMANDS')
    def test_dispatch_async_command(self, mock_commands):
        """Test dispatcher handles .async command."""
        session = Mock()
        mock_handler = Mock()
        mock_commands.__getitem__.return_value = mock_handler
        mock_commands.__contains__.return_value = True

        result = dispatch_integration_command(session, ".async x = 1;")
        assert result is True
        mock_handler.assert_called_once_with(session, "x = 1;")

    @patch('mlpy.integration.repl_commands.INTEGRATION_COMMANDS')
    def test_dispatch_callback_command(self, mock_commands):
        """Test dispatcher handles .callback command."""
        session = Mock()
        session.python_namespace = {"myFunc": Mock()}
        mock_handler = Mock()
        mock_commands.__getitem__.return_value = mock_handler
        mock_commands.__contains__.return_value = True

        result = dispatch_integration_command(session, ".callback myFunc")
        assert result is True
        mock_handler.assert_called_once_with(session, "myFunc")

    @patch('mlpy.integration.repl_commands.INTEGRATION_COMMANDS')
    def test_dispatch_benchmark_command_with_iterations(self, mock_commands):
        """Test dispatcher handles .benchmark command with iterations."""
        session = Mock()
        mock_handler = Mock()
        mock_commands.__getitem__.return_value = mock_handler

        result = dispatch_integration_command(session, ".benchmark code(); 50")
        assert result is True
        mock_handler.assert_called_once_with(session, "code()", "50")

    @patch('mlpy.integration.repl_commands.INTEGRATION_COMMANDS')
    def test_dispatch_benchmark_command_no_semicolon(self, mock_commands):
        """Test dispatcher handles .benchmark command without semicolon."""
        session = Mock()
        mock_handler = Mock()
        mock_commands.__getitem__.return_value = mock_handler
        mock_commands.__contains__.return_value = True

        result = dispatch_integration_command(session, ".benchmark code()")
        assert result is True
        # Dispatcher calls handler with just the code when no semicolon present
        mock_handler.assert_called_once_with(session, "code()")

    def test_dispatch_unknown_command_returns_false(self):
        """Test dispatcher returns False for unknown command."""
        session = Mock()
        result = dispatch_integration_command(session, ".unknown arg")
        assert result is False

    @patch('mlpy.integration.repl_commands.INTEGRATION_COMMANDS')
    def test_dispatch_case_insensitive(self, mock_commands):
        """Test dispatcher is case insensitive."""
        session = Mock()
        mock_handler = Mock()
        mock_commands.__getitem__.return_value = mock_handler
        mock_commands.__contains__.return_value = True

        result = dispatch_integration_command(session, ".ASYNC code;")
        assert result is True

    def test_print_integration_help(self, capsys):
        """Test help printing function."""
        print_integration_help()

        captured = capsys.readouterr()
        assert "Integration Toolkit Commands" in captured.out
        assert ".async" in captured.out
        assert ".callback" in captured.out
        assert ".benchmark" in captured.out
