"""Tests for debug REPL interactive commands.

This module tests the DebuggerREPL class which provides a command-line
interface for interactive debugging of ML programs.
"""

import pytest
from io import StringIO
from unittest.mock import Mock, MagicMock, patch
import sys

from mlpy.debugging.repl import DebuggerREPL
from mlpy.debugging.debugger import PendingBreakpoint


@pytest.fixture
def mock_debugger():
    """Create a mock MLDebugger instance."""
    debugger = Mock()
    debugger.ml_file = "test.ml"
    debugger.breakpoints = {}
    debugger.pending_breakpoints = {}
    debugger.watches = {}
    debugger.current_frame = None
    debugger.current_frame_index = 0
    debugger.source_map_index = Mock()

    # Mock methods
    debugger.continue_execution = Mock()
    debugger.step_next = Mock()
    debugger.step_into = Mock()
    debugger.step_out = Mock()
    debugger.set_breakpoint = Mock()
    debugger.delete_breakpoint = Mock(return_value=True)
    debugger.enable_breakpoint = Mock(return_value=True)
    debugger.disable_breakpoint = Mock(return_value=True)
    debugger.get_variable = Mock(return_value=42)
    debugger.show_source_context = Mock(return_value="Source code context")
    debugger.add_watch = Mock(return_value=1)
    debugger.remove_watch = Mock(return_value=True)
    debugger.get_all_breakpoints = Mock(return_value={})
    debugger.get_watch_values = Mock(return_value={})
    debugger.get_all_locals = Mock(return_value={})
    debugger.get_all_globals = Mock(return_value={})
    debugger.enable_exception_breakpoints = Mock()
    debugger.disable_exception_breakpoints = Mock()
    debugger.get_exception_info = Mock(return_value=None)
    debugger.navigate_up_stack = Mock(return_value=True)
    debugger.navigate_down_stack = Mock(return_value=True)
    debugger.get_call_stack = Mock(return_value=[])
    debugger.get_current_stack_frame = Mock(return_value=None)
    debugger.load_source_map_for_file = Mock(return_value=True)
    debugger.stop = Mock()

    return debugger


@pytest.fixture
def repl(mock_debugger):
    """Create a DebuggerREPL instance with mocked debugger."""
    return DebuggerREPL(mock_debugger)


class TestInitialization:
    """Test REPL initialization."""

    def test_initialization(self, mock_debugger):
        """Test REPL is properly initialized."""
        repl = DebuggerREPL(mock_debugger)

        assert repl.debugger == mock_debugger
        assert repl.should_continue is False
        assert repl.formatter is not None
        assert repl.prompt == "[mldb] "
        assert "ML Debugger" in repl.intro


class TestExecutionControlCommands:
    """Test execution control commands (continue, next, step, return)."""

    def test_continue_command(self, repl, mock_debugger):
        """Test continue command calls debugger.continue_execution()."""
        result = repl.do_continue("")

        mock_debugger.continue_execution.assert_called_once()
        assert repl.should_continue is True
        assert result is True  # Should exit cmdloop

    def test_continue_alias_c(self, repl, mock_debugger):
        """Test 'c' alias for continue."""
        result = repl.do_c("")

        mock_debugger.continue_execution.assert_called_once()
        assert result is True

    def test_continue_alias_cont(self, repl, mock_debugger):
        """Test 'cont' alias for continue."""
        result = repl.do_cont("")

        mock_debugger.continue_execution.assert_called_once()
        assert result is True

    def test_next_command(self, repl, mock_debugger):
        """Test next command calls debugger.step_next()."""
        result = repl.do_next("")

        mock_debugger.step_next.assert_called_once()
        assert repl.should_continue is True
        assert result is True

    def test_next_alias_n(self, repl, mock_debugger):
        """Test 'n' alias for next."""
        result = repl.do_n("")

        mock_debugger.step_next.assert_called_once()
        assert result is True

    def test_step_command(self, repl, mock_debugger):
        """Test step command calls debugger.step_into()."""
        result = repl.do_step("")

        mock_debugger.step_into.assert_called_once()
        assert repl.should_continue is True
        assert result is True

    def test_step_alias_s(self, repl, mock_debugger):
        """Test 's' alias for step."""
        result = repl.do_s("")

        mock_debugger.step_into.assert_called_once()
        assert result is True

    def test_return_command(self, repl, mock_debugger):
        """Test return command calls debugger.step_out()."""
        result = repl.do_return("")

        mock_debugger.step_out.assert_called_once()
        assert repl.should_continue is True
        assert result is True

    def test_return_alias_r(self, repl, mock_debugger):
        """Test 'r' alias for return."""
        result = repl.do_r("")

        mock_debugger.step_out.assert_called_once()
        assert result is True


class TestBreakpointCommands:
    """Test breakpoint management commands."""

    def test_break_with_line_number(self, repl, mock_debugger, capsys):
        """Test setting breakpoint with line number."""
        mock_bp = Mock()
        mock_bp.id = 1
        mock_debugger.set_breakpoint.return_value = mock_bp

        repl.do_break("42")

        mock_debugger.set_breakpoint.assert_called_once_with("test.ml", 42)
        captured = capsys.readouterr()
        assert "Breakpoint 1 set at test.ml:42" in captured.out

    def test_break_with_file_and_line(self, repl, mock_debugger, capsys):
        """Test setting breakpoint with file:line format."""
        mock_bp = Mock()
        mock_bp.id = 2
        mock_debugger.set_breakpoint.return_value = mock_bp

        repl.do_break("example.ml:100")

        mock_debugger.set_breakpoint.assert_called_once_with("example.ml", 100)
        captured = capsys.readouterr()
        assert "Breakpoint 2 set at example.ml:100" in captured.out

    def test_break_pending_breakpoint(self, repl, mock_debugger, capsys):
        """Test setting pending breakpoint (file not loaded)."""
        pending_bp = PendingBreakpoint(id=3, ml_file="pending.ml", ml_line=50)
        mock_debugger.set_breakpoint.return_value = pending_bp

        repl.do_break("pending.ml:50")

        captured = capsys.readouterr()
        assert "PENDING" in captured.out
        assert "file not loaded" in captured.out

    def test_break_invalid_location(self, repl, mock_debugger, capsys):
        """Test setting breakpoint at invalid location."""
        mock_debugger.set_breakpoint.return_value = None

        repl.do_break("999")

        captured = capsys.readouterr()
        assert "Cannot set breakpoint" in captured.out
        assert "invalid location" in captured.out

    def test_break_no_argument(self, repl, capsys):
        """Test break command with no argument shows usage."""
        repl.do_break("")

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_break_invalid_line_number(self, repl, mock_debugger, capsys):
        """Test break command with non-numeric line number."""
        repl.do_break("abc")

        captured = capsys.readouterr()
        assert "Invalid line number" in captured.out
        mock_debugger.set_breakpoint.assert_not_called()

    def test_break_alias_b(self, repl, mock_debugger):
        """Test 'b' alias for break."""
        mock_bp = Mock()
        mock_bp.id = 1
        mock_debugger.set_breakpoint.return_value = mock_bp

        repl.do_b("42")

        mock_debugger.set_breakpoint.assert_called_once_with("test.ml", 42)

    def test_delete_breakpoint(self, repl, mock_debugger, capsys):
        """Test deleting a breakpoint."""
        repl.do_delete("1")

        mock_debugger.delete_breakpoint.assert_called_once_with(1)
        captured = capsys.readouterr()
        assert "Breakpoint 1 deleted" in captured.out

    def test_delete_nonexistent_breakpoint(self, repl, mock_debugger, capsys):
        """Test deleting non-existent breakpoint."""
        mock_debugger.delete_breakpoint.return_value = False

        repl.do_delete("999")

        captured = capsys.readouterr()
        assert "No breakpoint with ID 999" in captured.out

    def test_delete_no_argument(self, repl, capsys):
        """Test delete command with no argument."""
        repl.do_delete("")

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_delete_invalid_id(self, repl, mock_debugger, capsys):
        """Test delete command with non-numeric ID."""
        repl.do_delete("abc")

        captured = capsys.readouterr()
        assert "Invalid breakpoint ID" in captured.out
        mock_debugger.delete_breakpoint.assert_not_called()

    def test_delete_alias_d(self, repl, mock_debugger):
        """Test 'd' alias for delete."""
        repl.do_d("1")

        mock_debugger.delete_breakpoint.assert_called_once_with(1)

    def test_enable_breakpoint(self, repl, mock_debugger, capsys):
        """Test enabling a breakpoint."""
        repl.do_enable("1")

        mock_debugger.enable_breakpoint.assert_called_once_with(1)
        captured = capsys.readouterr()
        assert "Breakpoint 1 enabled" in captured.out

    def test_enable_nonexistent_breakpoint(self, repl, mock_debugger, capsys):
        """Test enabling non-existent breakpoint."""
        mock_debugger.enable_breakpoint.return_value = False

        repl.do_enable("999")

        captured = capsys.readouterr()
        assert "No breakpoint with ID 999" in captured.out

    def test_enable_no_argument(self, repl, capsys):
        """Test enable command with no argument."""
        repl.do_enable("")

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_enable_invalid_id(self, repl, mock_debugger, capsys):
        """Test enable command with non-numeric ID."""
        repl.do_enable("abc")

        captured = capsys.readouterr()
        assert "Invalid breakpoint ID" in captured.out
        mock_debugger.enable_breakpoint.assert_not_called()

    def test_disable_breakpoint(self, repl, mock_debugger, capsys):
        """Test disabling a breakpoint."""
        repl.do_disable("1")

        mock_debugger.disable_breakpoint.assert_called_once_with(1)
        captured = capsys.readouterr()
        assert "Breakpoint 1 disabled" in captured.out

    def test_disable_nonexistent_breakpoint(self, repl, mock_debugger, capsys):
        """Test disabling non-existent breakpoint."""
        mock_debugger.disable_breakpoint.return_value = False

        repl.do_disable("999")

        captured = capsys.readouterr()
        assert "No breakpoint with ID 999" in captured.out

    def test_disable_no_argument(self, repl, capsys):
        """Test disable command with no argument."""
        repl.do_disable("")

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_disable_invalid_id(self, repl, mock_debugger, capsys):
        """Test disable command with non-numeric ID."""
        repl.do_disable("abc")

        captured = capsys.readouterr()
        assert "Invalid breakpoint ID" in captured.out
        mock_debugger.disable_breakpoint.assert_not_called()


class TestConditionCommand:
    """Test conditional breakpoint commands."""

    def test_condition_set_on_active_breakpoint(self, repl, mock_debugger, capsys):
        """Test setting condition on active breakpoint."""
        mock_bp = Mock()
        mock_bp.condition = None
        mock_debugger.breakpoints = {1: mock_bp}

        repl.do_condition("1 x > 10")

        assert mock_bp.condition == "x > 10"
        captured = capsys.readouterr()
        assert "condition set to: x > 10" in captured.out

    def test_condition_remove_from_active_breakpoint(self, repl, mock_debugger, capsys):
        """Test removing condition from active breakpoint."""
        mock_bp = Mock()
        mock_bp.condition = "x > 10"
        mock_debugger.breakpoints = {1: mock_bp}

        repl.do_condition("1")

        assert mock_bp.condition is None
        captured = capsys.readouterr()
        assert "unconditional" in captured.out

    def test_condition_set_on_pending_breakpoint(self, repl, mock_debugger, capsys):
        """Test setting condition on pending breakpoint."""
        pending_bp = PendingBreakpoint(id=2, ml_file="test.ml", ml_line=50)
        mock_debugger.pending_breakpoints = {2: pending_bp}

        repl.do_condition("2 count == 5")

        assert pending_bp.condition == "count == 5"
        captured = capsys.readouterr()
        assert "condition set to: count == 5" in captured.out

    def test_condition_remove_from_pending_breakpoint(self, repl, mock_debugger, capsys):
        """Test removing condition from pending breakpoint."""
        pending_bp = PendingBreakpoint(id=2, ml_file="test.ml", ml_line=50)
        pending_bp.condition = "x > 0"
        mock_debugger.pending_breakpoints = {2: pending_bp}

        repl.do_condition("2")

        assert pending_bp.condition is None
        captured = capsys.readouterr()
        assert "unconditional" in captured.out

    def test_condition_nonexistent_breakpoint(self, repl, mock_debugger, capsys):
        """Test setting condition on non-existent breakpoint."""
        repl.do_condition("999 x > 10")

        captured = capsys.readouterr()
        assert "No breakpoint with ID 999" in captured.out

    def test_condition_no_argument(self, repl, capsys):
        """Test condition command with no argument."""
        repl.do_condition("")

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_condition_invalid_id(self, repl, capsys):
        """Test condition command with non-numeric ID."""
        repl.do_condition("abc x > 10")

        captured = capsys.readouterr()
        assert "Invalid breakpoint ID" in captured.out

    def test_condition_alias_cond(self, repl, mock_debugger):
        """Test 'cond' alias for condition."""
        mock_bp = Mock()
        mock_bp.condition = None
        mock_debugger.breakpoints = {1: mock_bp}

        repl.do_cond("1 x > 10")

        assert mock_bp.condition == "x > 10"


class TestInspectionCommands:
    """Test variable inspection commands."""

    def test_print_variable(self, repl, mock_debugger, capsys):
        """Test printing a variable."""
        mock_debugger.get_variable.return_value = 42

        repl.do_print("x")

        mock_debugger.get_variable.assert_called_once_with("x")
        captured = capsys.readouterr()
        assert "42" in captured.out or "x" in captured.out

    def test_print_undefined_variable(self, repl, mock_debugger, capsys):
        """Test printing undefined variable."""
        mock_debugger.get_variable.return_value = None

        repl.do_print("undefined_var")

        captured = capsys.readouterr()
        assert "undefined" in captured.out

    def test_print_no_argument(self, repl, capsys):
        """Test print command with no argument."""
        repl.do_print("")

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_print_alias_p(self, repl, mock_debugger):
        """Test 'p' alias for print."""
        repl.do_p("x")

        mock_debugger.get_variable.assert_called_once_with("x")

    def test_list_source_default(self, repl, mock_debugger, capsys):
        """Test list command with default context lines."""
        repl.do_list("")

        mock_debugger.show_source_context.assert_called_once_with(2, 2)
        captured = capsys.readouterr()
        assert "Source code context" in captured.out

    def test_list_source_custom_lines(self, repl, mock_debugger, capsys):
        """Test list command with custom context lines."""
        repl.do_list("5")

        mock_debugger.show_source_context.assert_called_once_with(5, 5)

    def test_list_invalid_line_count(self, repl, mock_debugger, capsys):
        """Test list command with non-numeric line count."""
        repl.do_list("abc")

        captured = capsys.readouterr()
        assert "Invalid line count" in captured.out
        mock_debugger.show_source_context.assert_not_called()

    def test_list_alias_l(self, repl, mock_debugger):
        """Test 'l' alias for list."""
        repl.do_l("")

        mock_debugger.show_source_context.assert_called_once_with(2, 2)

    def test_watch_add(self, repl, mock_debugger, capsys):
        """Test adding watch expression."""
        repl.do_watch("x > 10")

        mock_debugger.add_watch.assert_called_once_with("x > 10")
        captured = capsys.readouterr()
        assert "Watch 1 set" in captured.out

    def test_watch_no_argument(self, repl, capsys):
        """Test watch command with no argument."""
        repl.do_watch("")

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_unwatch(self, repl, mock_debugger, capsys):
        """Test removing watch expression."""
        repl.do_unwatch("1")

        mock_debugger.remove_watch.assert_called_once_with(1)
        captured = capsys.readouterr()
        assert "Watch 1 removed" in captured.out

    def test_unwatch_nonexistent(self, repl, mock_debugger, capsys):
        """Test removing non-existent watch expression."""
        mock_debugger.remove_watch.return_value = False

        repl.do_unwatch("999")

        captured = capsys.readouterr()
        assert "No watch with ID 999" in captured.out

    def test_unwatch_no_argument(self, repl, capsys):
        """Test unwatch command with no argument."""
        repl.do_unwatch("")

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_unwatch_invalid_id(self, repl, mock_debugger, capsys):
        """Test unwatch command with non-numeric ID."""
        repl.do_unwatch("abc")

        captured = capsys.readouterr()
        assert "Invalid watch ID" in captured.out
        mock_debugger.remove_watch.assert_not_called()


class TestInfoCommands:
    """Test info commands."""

    def test_info_breakpoints_empty(self, repl, mock_debugger, capsys):
        """Test info breakpoints with no breakpoints."""
        repl.do_info("breakpoints")

        captured = capsys.readouterr()
        assert "No breakpoints set" in captured.out

    def test_info_breakpoints_with_active(self, repl, mock_debugger, capsys):
        """Test info breakpoints with active breakpoints."""
        mock_bp = Mock()
        mock_bp.hit_count = 3
        mock_debugger.breakpoints = {1: mock_bp}
        mock_debugger.get_all_breakpoints.return_value = {
            1: ("test.ml", 42, "active", None, True)
        }

        repl.do_info("breakpoints")

        captured = capsys.readouterr()
        assert "Breakpoints:" in captured.out
        assert "test.ml:42" in captured.out
        assert "ACTIVE" in captured.out

    def test_info_breakpoints_with_pending(self, repl, mock_debugger, capsys):
        """Test info breakpoints with pending breakpoints."""
        mock_debugger.get_all_breakpoints.return_value = {
            2: ("pending.ml", 50, "pending", None, True)
        }

        repl.do_info("breakpoints")

        captured = capsys.readouterr()
        assert "pending.ml:50" in captured.out
        assert "PENDING" in captured.out

    def test_info_watches_empty(self, repl, mock_debugger, capsys):
        """Test info watches with no watches."""
        repl.do_info("watches")

        captured = capsys.readouterr()
        assert "No watches set" in captured.out

    def test_info_watches_with_values(self, repl, mock_debugger, capsys):
        """Test info watches with watch expressions."""
        mock_debugger.watches = {1: "x > 10"}
        mock_debugger.get_watch_values.return_value = {
            1: ("x > 10", True, True)
        }

        repl.do_info("watches")

        captured = capsys.readouterr()
        assert "Watch expressions:" in captured.out

    def test_info_locals_empty(self, repl, mock_debugger, capsys):
        """Test info locals with no local variables."""
        repl.do_info("locals")

        captured = capsys.readouterr()
        assert "No local variables" in captured.out

    def test_info_locals_with_variables(self, repl, mock_debugger, capsys):
        """Test info locals with local variables."""
        mock_debugger.get_all_locals.return_value = {
            "x": 42,
            "name": "test"
        }

        repl.do_info("locals")

        captured = capsys.readouterr()
        assert "Local variables:" in captured.out

    def test_info_globals_empty(self, repl, mock_debugger, capsys):
        """Test info globals with no global variables."""
        repl.do_info("globals")

        captured = capsys.readouterr()
        assert "No global variables" in captured.out

    def test_info_globals_with_variables(self, repl, mock_debugger, capsys):
        """Test info globals with global variables."""
        mock_debugger.get_all_globals.return_value = {
            "PI": 3.14159,
            "VERSION": "2.0"
        }

        repl.do_info("globals")

        captured = capsys.readouterr()
        assert "Global variables:" in captured.out

    def test_info_args_no_frame(self, repl, mock_debugger, capsys):
        """Test info args when not in function."""
        repl.do_info("args")

        captured = capsys.readouterr()
        assert "Not in a function" in captured.out

    def test_info_args_with_frame(self, repl, mock_debugger, capsys):
        """Test info args when in function."""
        mock_debugger.current_frame = Mock()

        repl.do_info("args")

        captured = capsys.readouterr()
        assert "Function arguments:" in captured.out

    def test_info_no_argument(self, repl, capsys):
        """Test info command with no argument."""
        repl.do_info("")

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_info_unknown_command(self, repl, capsys):
        """Test info command with unknown subcommand."""
        repl.do_info("unknown")

        captured = capsys.readouterr()
        assert "Unknown info command" in captured.out

    def test_info_alias_i(self, repl, mock_debugger):
        """Test 'i' alias for info."""
        repl.do_i("breakpoints")

        mock_debugger.get_all_breakpoints.assert_called_once()


class TestExceptionCommands:
    """Test exception handling commands."""

    def test_catch_all_exceptions(self, repl, mock_debugger, capsys):
        """Test enabling breaking on all exceptions."""
        repl.do_catch("")

        mock_debugger.enable_exception_breakpoints.assert_called_once()
        captured = capsys.readouterr()
        assert "all exceptions" in captured.out

    def test_catch_specific_exception(self, repl, mock_debugger, capsys):
        """Test enabling breaking on specific exception type."""
        repl.do_catch("ValueError")

        mock_debugger.enable_exception_breakpoints.assert_called_once_with("ValueError")
        captured = capsys.readouterr()
        assert "ValueError" in captured.out

    def test_catch_off(self, repl, mock_debugger, capsys):
        """Test disabling exception breakpoints."""
        repl.do_catch("off")

        mock_debugger.disable_exception_breakpoints.assert_called_once()
        captured = capsys.readouterr()
        assert "disabled" in captured.out

    def test_catch_alias_except(self, repl, mock_debugger):
        """Test 'except' alias for catch."""
        repl.do_except("")

        mock_debugger.enable_exception_breakpoints.assert_called_once()

    def test_exception_info_available(self, repl, mock_debugger, capsys):
        """Test displaying exception information."""
        mock_debugger.get_exception_info.return_value = {
            "type": "ValueError",
            "message": "Invalid value"
        }

        repl.do_exception("")

        captured = capsys.readouterr()
        assert "ValueError" in captured.out
        assert "Invalid value" in captured.out

    def test_exception_info_not_available(self, repl, mock_debugger, capsys):
        """Test exception command when no exception available."""
        repl.do_exception("")

        captured = capsys.readouterr()
        assert "No exception information" in captured.out

    def test_exception_alias_exc(self, repl, mock_debugger):
        """Test 'exc' alias for exception."""
        repl.do_exc("")

        mock_debugger.get_exception_info.assert_called_once()


class TestStackNavigationCommands:
    """Test call stack navigation commands."""

    def test_up_single_frame(self, repl, mock_debugger, capsys):
        """Test navigating up one stack frame."""
        with patch.object(repl, '_show_stack_context'):
            repl.do_up("")

            mock_debugger.navigate_up_stack.assert_called_once()

    def test_up_multiple_frames(self, repl, mock_debugger, capsys):
        """Test navigating up multiple stack frames."""
        with patch.object(repl, '_show_stack_context'):
            repl.do_up("3")

            assert mock_debugger.navigate_up_stack.call_count == 3

    def test_up_at_top(self, repl, mock_debugger, capsys):
        """Test navigating up when already at top of stack."""
        mock_debugger.navigate_up_stack.return_value = False

        with patch.object(repl, '_show_stack_context'):
            repl.do_up("")

            captured = capsys.readouterr()
            assert "top of stack" in captured.out

    def test_up_invalid_count(self, repl, mock_debugger, capsys):
        """Test up command with non-numeric count."""
        repl.do_up("abc")

        captured = capsys.readouterr()
        assert "Invalid number" in captured.out
        mock_debugger.navigate_up_stack.assert_not_called()

    def test_down_single_frame(self, repl, mock_debugger, capsys):
        """Test navigating down one stack frame."""
        with patch.object(repl, '_show_stack_context'):
            repl.do_down("")

            mock_debugger.navigate_down_stack.assert_called_once()

    def test_down_multiple_frames(self, repl, mock_debugger, capsys):
        """Test navigating down multiple stack frames."""
        with patch.object(repl, '_show_stack_context'):
            repl.do_down("2")

            assert mock_debugger.navigate_down_stack.call_count == 2

    def test_down_at_bottom(self, repl, mock_debugger, capsys):
        """Test navigating down when already at bottom of stack."""
        mock_debugger.navigate_down_stack.return_value = False

        with patch.object(repl, '_show_stack_context'):
            repl.do_down("")

            captured = capsys.readouterr()
            assert "bottom of stack" in captured.out

    def test_down_invalid_count(self, repl, mock_debugger, capsys):
        """Test down command with non-numeric count."""
        repl.do_down("abc")

        captured = capsys.readouterr()
        assert "Invalid number" in captured.out
        mock_debugger.navigate_down_stack.assert_not_called()

    def test_where_empty_stack(self, repl, mock_debugger, capsys):
        """Test where command with empty stack."""
        repl.do_where("")

        captured = capsys.readouterr()
        assert "No stack information" in captured.out

    def test_where_with_stack(self, repl, mock_debugger, capsys):
        """Test where command with call stack."""
        mock_debugger.get_call_stack.return_value = [
            ("test.ml", 42, "main"),
            ("utils.ml", 10, "helper")
        ]
        mock_debugger.current_frame_index = 0

        repl.do_where("")

        captured = capsys.readouterr()
        assert "Call stack:" in captured.out
        assert "main" in captured.out
        assert "test.ml:42" in captured.out

    def test_where_alias_bt(self, repl, mock_debugger):
        """Test 'bt' alias for where."""
        repl.do_bt("")

        mock_debugger.get_call_stack.assert_called_once()

    def test_where_alias_backtrace(self, repl, mock_debugger):
        """Test 'backtrace' alias for where."""
        repl.do_backtrace("")

        mock_debugger.get_call_stack.assert_called_once()


class TestLoadMapCommand:
    """Test source map loading command."""

    def test_loadmap_success(self, repl, mock_debugger, capsys):
        """Test successful source map loading."""
        repl.do_loadmap("utils.ml")

        mock_debugger.load_source_map_for_file.assert_called_once_with("utils.ml")
        captured = capsys.readouterr()
        assert "Source map loaded" in captured.out

    def test_loadmap_failure(self, repl, mock_debugger, capsys):
        """Test failed source map loading."""
        mock_debugger.load_source_map_for_file.return_value = False

        repl.do_loadmap("missing.ml")

        captured = capsys.readouterr()
        assert "Failed to load" in captured.out

    def test_loadmap_no_argument(self, repl, capsys):
        """Test loadmap command with no argument."""
        repl.do_loadmap("")

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_loadmap_alias_load(self, repl, mock_debugger):
        """Test 'load' alias for loadmap."""
        repl.do_load("test.ml")

        mock_debugger.load_source_map_for_file.assert_called_once_with("test.ml")


class TestUtilityCommands:
    """Test utility commands."""

    @patch('os.system')
    def test_clear_command_windows(self, mock_system, repl):
        """Test clear command on Windows."""
        with patch('os.name', 'nt'):
            repl.do_clear("")

            mock_system.assert_called_once_with("cls")

    @patch('os.system')
    def test_clear_command_unix(self, mock_system, repl):
        """Test clear command on Unix."""
        with patch('os.name', 'posix'):
            repl.do_clear("")

            mock_system.assert_called_once_with("clear")

    def test_quit_command(self, repl, mock_debugger):
        """Test quit command exits debugger."""
        with pytest.raises(SystemExit):
            repl.do_quit("")

        mock_debugger.stop.assert_called_once()

    def test_quit_alias_q(self, repl, mock_debugger):
        """Test 'q' alias for quit."""
        with pytest.raises(SystemExit):
            repl.do_q("")

        mock_debugger.stop.assert_called_once()

    def test_quit_alias_exit(self, repl, mock_debugger):
        """Test 'exit' alias for quit."""
        with pytest.raises(SystemExit):
            repl.do_exit("")

        mock_debugger.stop.assert_called_once()

    def test_help_command_no_argument(self, repl, capsys):
        """Test help command with no argument shows all commands."""
        repl.do_help("")

        captured = capsys.readouterr()
        assert "Available commands:" in captured.out
        assert "continue" in captured.out
        assert "break" in captured.out
        assert "print" in captured.out

    def test_help_command_specific(self, repl, capsys):
        """Test help command for specific command."""
        with patch.object(repl, 'do_help', wraps=repl.do_help):
            repl.do_help("continue")

    def test_emptyline(self, repl):
        """Test empty line does nothing."""
        result = repl.emptyline()

        assert result is None

    def test_default_unknown_command(self, repl, capsys):
        """Test default handler for unknown commands."""
        repl.default("unknown_command")

        captured = capsys.readouterr()
        assert "Unknown command" in captured.out
        assert "help" in captured.out
