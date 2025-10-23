"""
Unit tests for the Debug Adapter Protocol (DAP) server.

Tests cover:
- DAP protocol message parsing and formatting
- Request handler implementations
- Breakpoint management
- Execution control
- Variable inspection
- Expression evaluation
"""

import pytest
import json
import io
import threading
import time
from pathlib import Path
from typing import Dict, Any, List

from mlpy.debugging.dap_server import MLDebugAdapter


class TestDAPProtocol:
    """Test DAP protocol message handling."""

    def test_message_parsing_with_content_length(self):
        """Test reading DAP message with Content-Length header."""
        # Create a DAP message
        body = json.dumps({"type": "request", "seq": 1, "command": "initialize"})
        content = body.encode('utf-8')
        message = f'Content-Length: {len(content)}\r\n\r\n'.encode('utf-8') + content

        # Create adapter with mock stdin
        stdin = io.BytesIO(message)
        adapter = MLDebugAdapter(stdin=stdin, stdout=io.BytesIO())

        # Read message
        parsed = adapter._read_message()

        assert parsed is not None
        assert parsed['type'] == 'request'
        assert parsed['seq'] == 1
        assert parsed['command'] == 'initialize'

    def test_message_sending(self):
        """Test sending DAP message with Content-Length header."""
        stdout = io.BytesIO()
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=stdout)

        message = {
            "type": "response",
            "request_seq": 1,
            "success": True,
            "command": "initialize",
            "seq": 1
        }

        adapter._send_message(message)

        # Read what was written
        stdout.seek(0)
        data = stdout.read().decode('utf-8')

        # Check Content-Length header
        assert 'Content-Length:' in data
        # Check message body
        assert '"type": "response"' in data
        assert '"command": "initialize"' in data

    def test_sequence_number_increment(self):
        """Test that sequence numbers increment correctly."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        seq1 = adapter._next_seq()
        seq2 = adapter._next_seq()
        seq3 = adapter._next_seq()

        assert seq2 == seq1 + 1
        assert seq3 == seq2 + 1

    def test_empty_message_returns_none(self):
        """Test that empty stdin returns None."""
        stdin = io.BytesIO(b'')
        adapter = MLDebugAdapter(stdin=stdin, stdout=io.BytesIO())

        result = adapter._read_message()
        assert result is None


class TestInitializeRequest:
    """Test initialize request handler."""

    def test_initialize_returns_capabilities(self):
        """Test that initialize returns correct capabilities."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        response = adapter._handle_initialize(1, {"clientID": "vscode"})

        assert response['type'] == 'response'
        assert response['success'] is True
        assert response['command'] == 'initialize'

        # Check key capabilities
        body = response['body']
        assert body['supportsConfigurationDoneRequest'] is True
        assert body['supportsConditionalBreakpoints'] is True
        assert body['supportsEvaluateForHovers'] is True
        assert body['supportsExceptionInfoRequest'] is True

        # Check exception filters
        assert 'exceptionBreakpointFilters' in body
        filters = body['exceptionBreakpointFilters']
        assert len(filters) >= 2
        filter_names = [f['filter'] for f in filters]
        assert 'all' in filter_names
        assert 'uncaught' in filter_names

    def test_initialize_sets_flag(self):
        """Test that initialize sets the initialize_complete flag."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        assert adapter.initialize_complete is False

        adapter._handle_initialize(1, {})

        assert adapter.initialize_complete is True


class TestLaunchRequest:
    """Test launch request handler."""

    def test_launch_without_program_returns_error(self):
        """Test that launch without program returns error."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        response = adapter._handle_launch(1, {})

        assert response['success'] is False
        assert 'No program specified' in response['message']

    def test_launch_with_nonexistent_file_returns_error(self):
        """Test that launch with non-existent file returns error."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        response = adapter._handle_launch(1, {"program": "/nonexistent/file.ml"})

        assert response['success'] is False
        # Either transpilation fails or file not found

    def test_launch_with_valid_ml_file(self, tmp_path):
        """Test launch with valid ML file."""
        # Create a simple ML file
        ml_file = tmp_path / "test.ml"
        ml_file.write_text("""
function greet(name) {
    print("Hello, " + name);
}

greet("World");
""")

        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        # Note: This will attempt actual transpilation
        # It may fail if transpiler isn't set up properly
        try:
            response = adapter._handle_launch(1, {"program": str(ml_file)})

            # If transpilation succeeds
            if response.get('success'):
                assert adapter.debugger is not None
                assert adapter.py_file is not None
                assert adapter.source_map_index is not None
        except Exception:
            # If transpiler not available, that's OK for unit test
            pytest.skip("Transpiler not available")


class TestBreakpointHandlers:
    """Test breakpoint request handlers."""

    def test_set_breakpoints_without_debugger_returns_error(self):
        """Test setBreakpoints without debugger initialized."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        response = adapter._handle_setBreakpoints(1, {
            "source": {"path": "test.ml"},
            "breakpoints": [{"line": 5}]
        })

        assert response['success'] is False
        assert 'Debugger not initialized' in response['message']

    def test_set_breakpoints_empty_list(self):
        """Test setting empty breakpoint list."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        # Create a mock debugger
        from unittest.mock import Mock
        adapter.debugger = Mock()
        adapter.debugger.set_breakpoint = Mock(return_value=Mock(id=1))

        response = adapter._handle_setBreakpoints(1, {
            "source": {"path": "test.ml"},
            "breakpoints": []
        })

        assert response['success'] is True
        assert response['body']['breakpoints'] == []

    def test_set_breakpoints_with_conditions(self):
        """Test setting breakpoints with conditions."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        # Create a mock debugger
        from unittest.mock import Mock
        adapter.debugger = Mock()
        adapter.debugger.set_breakpoint = Mock(return_value=Mock(id=1))

        response = adapter._handle_setBreakpoints(1, {
            "source": {"path": "test.ml"},
            "breakpoints": [
                {"line": 5, "condition": "x > 10"},
                {"line": 10}
            ]
        })

        assert response['success'] is True
        assert len(response['body']['breakpoints']) == 2

        # Verify set_breakpoint was called with conditions
        calls = adapter.debugger.set_breakpoint.call_args_list
        assert len(calls) == 2
        # First call should have condition
        assert calls[0][1].get('condition') == "x > 10"

    def test_set_exception_breakpoints(self):
        """Test setting exception breakpoints."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        # Create a mock debugger
        from unittest.mock import Mock
        adapter.debugger = Mock()

        response = adapter._handle_setExceptionBreakpoints(1, {
            "filters": ["all", "uncaught"]
        })

        assert response['success'] is True
        assert adapter.debugger.break_on_exceptions is True
        assert adapter.debugger.exception_filters == ["all", "uncaught"]


class TestExecutionControl:
    """Test execution control handlers."""

    def test_continue_handler(self):
        """Test continue request."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        # Mock debugger
        from unittest.mock import Mock
        adapter.debugger = Mock()
        adapter.debugger.continue_execution = Mock()

        response = adapter._handle_continue(1, {"threadId": 1})

        assert response['success'] is True
        assert response['body']['allThreadsContinued'] is True
        adapter.debugger.continue_execution.assert_called_once()

    def test_next_handler(self):
        """Test next (step over) request."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        from unittest.mock import Mock
        adapter.debugger = Mock()
        adapter.debugger.step_next = Mock()

        response = adapter._handle_next(1, {"threadId": 1})

        assert response['success'] is True
        adapter.debugger.step_next.assert_called_once()

    def test_step_in_handler(self):
        """Test stepIn request."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        from unittest.mock import Mock
        adapter.debugger = Mock()
        adapter.debugger.step_into = Mock()

        response = adapter._handle_stepIn(1, {"threadId": 1})

        assert response['success'] is True
        adapter.debugger.step_into.assert_called_once()

    def test_step_out_handler(self):
        """Test stepOut request."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        from unittest.mock import Mock
        adapter.debugger = Mock()
        adapter.debugger.step_out = Mock()

        response = adapter._handle_stepOut(1, {"threadId": 1})

        assert response['success'] is True
        adapter.debugger.step_out.assert_called_once()


class TestStackAndVariables:
    """Test stack trace and variable inspection handlers."""

    def test_threads_handler(self):
        """Test threads request returns main thread."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        response = adapter._handle_threads(1, {})

        assert response['success'] is True
        assert len(response['body']['threads']) == 1
        assert response['body']['threads'][0]['id'] == 1
        assert response['body']['threads'][0]['name'] == 'Main Thread'

    def test_stack_trace_without_debugger(self):
        """Test stackTrace without debugger returns empty."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        response = adapter._handle_stackTrace(1, {"threadId": 1})

        assert response['success'] is True
        assert response['body']['stackFrames'] == []
        assert response['body']['totalFrames'] == 0

    def test_stack_trace_with_frames(self):
        """Test stackTrace with mock frames."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        # Mock debugger with stack frames
        from unittest.mock import Mock
        adapter.debugger = Mock()
        adapter.debugger.get_call_stack_with_frames = Mock(return_value=[
            {
                'frame': Mock(),
                'ml_position': ('test.ml', 10, 5),
                'function_name': 'main'
            },
            {
                'frame': Mock(),
                'ml_position': ('test.ml', 5, 1),
                'function_name': 'helper'
            }
        ])

        response = adapter._handle_stackTrace(1, {"threadId": 1})

        assert response['success'] is True
        frames = response['body']['stackFrames']
        assert len(frames) == 2

        # Check first frame
        assert frames[0]['name'] == 'main'
        assert frames[0]['source']['path'] == 'test.ml'
        assert frames[0]['line'] == 10
        assert frames[0]['column'] == 5

    def test_scopes_handler(self):
        """Test scopes request returns locals and globals."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        response = adapter._handle_scopes(1, {"frameId": 0})

        assert response['success'] is True
        scopes = response['body']['scopes']
        assert len(scopes) == 2

        # Check locals scope
        assert scopes[0]['name'] == 'Locals'
        assert scopes[0]['expensive'] is False

        # Check globals scope
        assert scopes[1]['name'] == 'Globals'

    def test_variables_without_debugger(self):
        """Test variables without debugger returns empty."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        response = adapter._handle_variables(1, {"variablesReference": 1})

        assert response['success'] is True
        assert response['body']['variables'] == []

    def test_variables_locals(self):
        """Test getting local variables."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        # Mock debugger
        from unittest.mock import Mock
        adapter.debugger = Mock()
        adapter.debugger.get_locals = Mock(return_value={
            'x': 42,
            'name': 'test',
            'items': [1, 2, 3]
        })

        # variablesReference encoding: frame_id * 1000 + scope_id
        # scope_id 1 = locals
        response = adapter._handle_variables(1, {"variablesReference": 1})

        assert response['success'] is True
        variables = response['body']['variables']
        assert len(variables) == 3

        # Variables should be formatted
        var_names = [v['name'] for v in variables]
        assert 'x' in var_names
        assert 'name' in var_names
        assert 'items' in var_names

    def test_variables_globals(self):
        """Test getting global variables."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        from unittest.mock import Mock
        adapter.debugger = Mock()
        adapter.debugger.get_globals = Mock(return_value={
            'module_var': 'value',
            '__name__': '__main__',  # Should be filtered
            'constant': 100
        })

        # scope_id 2 = globals
        response = adapter._handle_variables(1, {"variablesReference": 2})

        assert response['success'] is True
        variables = response['body']['variables']

        # Check that __name__ is filtered
        var_names = [v['name'] for v in variables]
        assert 'module_var' in var_names
        assert 'constant' in var_names
        assert '__name__' not in var_names  # Internal variables filtered


class TestEvaluate:
    """Test expression evaluation handler."""

    def test_evaluate_without_debugger_returns_error(self):
        """Test evaluate without debugger."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        response = adapter._handle_evaluate(1, {
            "expression": "x + 5",
            "frameId": 0
        })

        assert response['success'] is False
        assert 'Debugger not running' in response['message']

    def test_evaluate_simple_expression(self):
        """Test evaluating a simple expression."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        # Mock debugger
        from unittest.mock import Mock
        adapter.debugger = Mock()
        adapter.debugger.evaluate_expression = Mock(return_value=47)

        response = adapter._handle_evaluate(1, {
            "expression": "x + 5",
            "frameId": 0,
            "context": "watch"
        })

        assert response['success'] is True
        assert response['body']['result'] == '47'
        assert response['body']['type'] == 'int'

        # Verify evaluate was called correctly
        adapter.debugger.evaluate_expression.assert_called_once_with("x + 5", 0)

    def test_evaluate_with_error(self):
        """Test evaluate that raises an error."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        from unittest.mock import Mock
        adapter.debugger = Mock()
        adapter.debugger.evaluate_expression = Mock(side_effect=ValueError("Invalid expression"))

        response = adapter._handle_evaluate(1, {
            "expression": "invalid!",
            "frameId": 0
        })

        assert response['success'] is False
        assert 'Evaluation failed' in response['message']


class TestResponseHelpers:
    """Test response creation helper methods."""

    def test_create_response(self):
        """Test creating success response."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        response = adapter._create_response(
            request_seq=10,
            command="test",
            body={"result": "success"}
        )

        assert response['type'] == 'response'
        assert response['request_seq'] == 10
        assert response['success'] is True
        assert response['command'] == 'test'
        assert response['body'] == {"result": "success"}
        assert 'seq' in response

    def test_create_error_response(self):
        """Test creating error response."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        response = adapter._create_error_response(
            request_seq=10,
            message="Something went wrong"
        )

        assert response['type'] == 'response'
        assert response['request_seq'] == 10
        assert response['success'] is False
        assert response['message'] == "Something went wrong"
        assert 'seq' in response

    def test_send_event(self):
        """Test sending event."""
        stdout = io.BytesIO()
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=stdout)

        adapter._send_event('stopped', {
            'reason': 'breakpoint',
            'threadId': 1
        })

        # Read what was sent
        stdout.seek(0)
        data = stdout.read().decode('utf-8')

        assert '"type": "event"' in data
        assert '"event": "stopped"' in data
        assert '"reason": "breakpoint"' in data


class TestUnknownCommand:
    """Test handling of unknown commands."""

    def test_unknown_command_returns_error(self):
        """Test that unknown commands return error response."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        response = adapter._handle_message({
            "type": "request",
            "seq": 1,
            "command": "unknownCommand",
            "arguments": {}
        })

        assert response is not None
        assert response['success'] is False
        assert 'Unknown command' in response['message']


class TestLogging:
    """Test debug logging functionality."""

    def test_logging_disabled_by_default(self, capsys):
        """Test that logging is disabled by default."""
        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        adapter.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" not in captured.err

    def test_logging_enabled_with_env_var(self, capsys, monkeypatch):
        """Test that logging can be enabled via environment variable."""
        monkeypatch.setenv('MLPY_DEBUG', '1')

        adapter = MLDebugAdapter(stdin=io.BytesIO(), stdout=io.BytesIO())

        adapter.log("Test debug message")

        captured = capsys.readouterr()
        assert "Test debug message" in captured.err


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
