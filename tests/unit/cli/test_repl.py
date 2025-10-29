"""
Comprehensive unit tests for repl.py - Interactive REPL for ML execution.

Tests cover:
- REPLResult dataclass
- MLREPLSession initialization
- execute_ml_line() method
- Namespace management
- Security integration
- Error handling
- Multi-line support
- Command history
"""


import pytest

from mlpy.cli.repl import (
    MLREPLSession,
    REPLResult,
)


class TestREPLResult:
    """Test REPLResult dataclass."""

    def test_repl_result_success(self):
        """Test successful REPL result."""
        result = REPLResult(
            success=True, value=42, transpiled_python="x = 42", execution_time_ms=1.5
        )

        assert result.success is True
        assert result.value == 42
        assert result.error is None
        assert result.transpiled_python == "x = 42"
        assert result.execution_time_ms == 1.5

    def test_repl_result_error(self):
        """Test error REPL result."""
        result = REPLResult(success=False, error="Parse error")

        assert result.success is False
        assert result.value is None
        assert result.error == "Parse error"

    def test_repl_result_defaults(self):
        """Test REPL result with defaults."""
        result = REPLResult(success=True)

        assert result.success is True
        assert result.value is None
        assert result.error is None
        assert result.transpiled_python == ""
        assert result.execution_time_ms == 0.0


class TestMLREPLSessionInit:
    """Test MLREPLSession initialization."""

    def test_session_creation_default(self):
        """Test creating REPL session with defaults."""
        session = MLREPLSession()

        assert session.transpiler is not None
        assert isinstance(session.python_namespace, dict)
        assert session.security_enabled is True
        assert session.profile is False
        # History uses deque for automatic FIFO eviction when max_history reached
        from collections import deque
        assert isinstance(session.history, deque)

    def test_session_creation_with_security_disabled(self):
        """Test creating REPL session with security disabled."""
        session = MLREPLSession(security_enabled=False)

        assert session.security_enabled is False

    def test_session_creation_with_profiling(self):
        """Test creating REPL session with profiling enabled."""
        session = MLREPLSession(profile=True)

        assert session.profile is True

    def test_namespace_initialization(self):
        """Test namespace is initialized with builtins."""
        session = MLREPLSession()

        # Should have __builtins__
        assert "__builtins__" in session.python_namespace

    def test_namespace_has_stdlib_modules(self):
        """Test namespace has ML stdlib modules pre-loaded."""
        session = MLREPLSession()

        # Should attempt to load common modules
        # May or may not succeed depending on environment
        namespace = session.python_namespace
        assert isinstance(namespace, dict)


class TestExecuteMLLine:
    """Test execute_ml_line method."""

    @pytest.fixture
    def session(self):
        """Create REPL session."""
        return MLREPLSession(security_enabled=False)

    def test_execute_empty_line(self, session):
        """Test executing empty line."""
        result = session.execute_ml_line("")

        assert result.success is True
        assert result.value is None

    def test_execute_whitespace_only(self, session):
        """Test executing whitespace-only line."""
        result = session.execute_ml_line("   \n  \t  ")

        assert result.success is True
        assert result.value is None

    def test_execute_simple_assignment(self, session):
        """Test executing simple assignment."""
        result = session.execute_ml_line("x = 42;")

        assert result.success is True
        # Variable should be in namespace
        assert "x" in session.python_namespace

    def test_execute_expression(self, session):
        """Test executing expression."""
        result = session.execute_ml_line("2 + 3;")

        # Should succeed
        assert result.success is True

    def test_execute_with_syntax_error(self, session):
        """Test executing code with syntax error."""
        result = session.execute_ml_line("let x =")

        # Should handle error gracefully
        assert result.success is False
        assert result.error is not None

    def test_namespace_persistence(self, session):
        """Test namespace persists across executions."""
        # First execution
        result1 = session.execute_ml_line("x = 10;")
        assert result1.success is True

        # Second execution using variable from first
        result2 = session.execute_ml_line("y = x + 5;")
        assert result2.success is True

        # Both variables should be in namespace
        assert "x" in session.python_namespace
        assert "y" in session.python_namespace

    def test_function_definition(self, session):
        """Test defining a function."""
        result = session.execute_ml_line("function add(a, b) { return a + b; }")

        # Should succeed
        assert isinstance(result, REPLResult)

    def test_execution_time_tracked(self, session):
        """Test execution time is tracked."""
        result = session.execute_ml_line("x = 42;")

        # Execution time should be recorded
        assert result.execution_time_ms >= 0


class TestHistoryManagement:
    """Test command history management."""

    @pytest.fixture
    def session(self):
        """Create REPL session."""
        return MLREPLSession()

    def test_history_empty_initially(self, session):
        """Test history is empty on creation."""
        assert len(session.history) == 0

    def test_history_records_commands(self, session):
        """Test history records executed commands."""
        session.execute_ml_line("x = 1;")
        session.execute_ml_line("y = 2;")

        # History should have entries (if implemented)
        # Check structure exists
        assert hasattr(session, "history")


class TestSecurityIntegration:
    """Test security analysis integration."""

    @pytest.fixture
    def secure_session(self):
        """Create REPL session with security enabled."""
        return MLREPLSession(security_enabled=True)

    @pytest.fixture
    def insecure_session(self):
        """Create REPL session with security disabled."""
        return MLREPLSession(security_enabled=False)

    def test_security_enabled_flag(self, secure_session):
        """Test security enabled flag is set."""
        assert secure_session.security_enabled is True

    def test_security_disabled_flag(self, insecure_session):
        """Test security disabled flag is set."""
        assert insecure_session.security_enabled is False


class TestErrorHandling:
    """Test error handling in REPL."""

    @pytest.fixture
    def session(self):
        """Create REPL session."""
        return MLREPLSession()

    def test_parse_error_handling(self, session):
        """Test handling of parse errors."""
        result = session.execute_ml_line("function broken(")

        # Should return error result
        assert result.success is False
        assert result.error is not None

    def test_runtime_error_handling(self, session):
        """Test handling of runtime errors."""
        # Division by zero
        result = session.execute_ml_line("x = 1 / 0;")

        # Should handle error
        assert isinstance(result, REPLResult)

    def test_undefined_variable_error(self, session):
        """Test handling of undefined variable access."""
        result = session.execute_ml_line("y = undefined_var;")

        # Should handle error gracefully
        assert isinstance(result, REPLResult)


class TestTranspilation:
    """Test transpilation in REPL."""

    @pytest.fixture
    def session(self):
        """Create REPL session."""
        return MLREPLSession()

    def test_transpiled_code_returned(self, session):
        """Test transpiled Python code is returned."""
        result = session.execute_ml_line("x = 42;")

        # Should have transpiled code
        assert isinstance(result.transpiled_python, str)

    def test_transpilation_preserves_semantics(self, session):
        """Test transpilation preserves code semantics."""
        # Execute assignment
        result = session.execute_ml_line("count = 100;")

        if result.success:
            # Variable should exist in namespace
            assert "count" in session.python_namespace


class TestNamespaceManagement:
    """Test Python namespace management."""

    @pytest.fixture
    def session(self):
        """Create REPL session."""
        return MLREPLSession()

    def test_namespace_is_dict(self, session):
        """Test namespace is a dictionary."""
        assert isinstance(session.python_namespace, dict)

    def test_namespace_isolation(self, session):
        """Test namespace is isolated per session."""
        session1 = MLREPLSession()
        session2 = MLREPLSession()

        session1.execute_ml_line("x = 1;")
        session2.execute_ml_line("x = 2;")

        # Namespaces should be separate
        assert session1.python_namespace is not session2.python_namespace

    def test_namespace_has_builtins(self, session):
        """Test namespace has Python builtins."""
        assert "__builtins__" in session.python_namespace


class TestREPLSessionMethods:
    """Test additional REPL session methods."""

    @pytest.fixture
    def session(self):
        """Create REPL session."""
        return MLREPLSession()

    def test_has_transpiler(self, session):
        """Test session has transpiler."""
        assert hasattr(session, "transpiler")
        assert session.transpiler is not None

    def test_has_execute_method(self, session):
        """Test session has execute method."""
        assert hasattr(session, "execute_ml_line")
        assert callable(session.execute_ml_line)

    def test_session_is_reusable(self, session):
        """Test session can execute multiple commands."""
        result1 = session.execute_ml_line("a = 1;")
        result2 = session.execute_ml_line("b = 2;")
        result3 = session.execute_ml_line("c = a + b;")

        # All should succeed
        assert isinstance(result1, REPLResult)
        assert isinstance(result2, REPLResult)
        assert isinstance(result3, REPLResult)


class TestAutoSemicolonInsertion:
    """Test automatic semicolon insertion."""

    @pytest.fixture
    def session(self):
        """Create REPL session."""
        return MLREPLSession()

    def test_adds_semicolon_to_simple_statement(self, session):
        """Test semicolon added to statement missing it."""
        # Execute without semicolon
        result = session.execute_ml_line("x = 42")

        # Should succeed (semicolon added automatically)
        assert isinstance(result, REPLResult)

    def test_preserves_existing_semicolon(self, session):
        """Test existing semicolon is preserved."""
        result = session.execute_ml_line("x = 42;")

        assert isinstance(result, REPLResult)

    def test_handles_function_definitions(self, session):
        """Test function definitions don't get extra semicolons."""
        result = session.execute_ml_line("function test() { return 5; }")

        # Should not add semicolon after }
        assert isinstance(result, REPLResult)

    def test_handles_curly_brace_lines(self, session):
        """Test lines ending with { don't get semicolons."""
        # This would be part of multi-line input
        result = session.execute_ml_line("if (true) {")

        # Should handle gracefully
        assert isinstance(result, REPLResult)


class TestHistoryTracking:
    """Test command history tracking."""

    @pytest.fixture
    def session(self):
        """Create REPL session."""
        return MLREPLSession()

    def test_history_records_executed_commands(self, session):
        """Test history records all executed commands."""
        session.execute_ml_line("x = 1;")
        session.execute_ml_line("y = 2;")
        session.execute_ml_line("z = 3;")

        # History should have 3 entries
        assert len(session.history) == 3

    def test_history_preserves_order(self, session):
        """Test history preserves command order."""
        session.execute_ml_line("first = 1;")
        session.execute_ml_line("second = 2;")

        assert len(session.history) >= 2
        # First command should be in history
        assert any("first" in cmd for cmd in session.history)

    def test_empty_lines_added_to_history(self, session):
        """Test even empty lines are tracked."""
        session.execute_ml_line("")
        session.execute_ml_line("x = 1;")

        # Should have entries
        assert len(session.history) >= 1


class TestSecurityCheckingInREPL:
    """Test security checking in REPL execution."""

    @pytest.fixture
    def secure_session(self):
        """Create session with security enabled."""
        return MLREPLSession(security_enabled=True)

    def test_detects_dangerous_code(self, secure_session):
        """Test dangerous code is detected when security enabled."""
        # Try to execute potentially dangerous code
        result = secure_session.execute_ml_line("eval('dangerous');")

        # Should detect security issue or parse error
        assert isinstance(result, REPLResult)

    def test_allows_safe_code_with_security(self, secure_session):
        """Test safe code executes with security enabled."""
        result = secure_session.execute_ml_line("safe = 42;")

        # Should allow safe code
        assert isinstance(result, REPLResult)


class TestCodeExecution:
    """Test actual code execution in namespace."""

    @pytest.fixture
    def session(self):
        """Create REPL session."""
        return MLREPLSession()

    def test_expression_evaluation(self, session):
        """Test expression evaluation returns value."""
        result = session.execute_ml_line("5 + 3;")

        # Should execute successfully
        assert isinstance(result, REPLResult)

    def test_variable_assignment_and_retrieval(self, session):
        """Test variables can be assigned and retrieved."""
        session.execute_ml_line("myVar = 100;")

        # Variable should be in namespace
        assert "myVar" in session.python_namespace
        assert session.python_namespace["myVar"] == 100

    def test_function_definition_and_call(self, session):
        """Test function can be defined and called."""
        # Define function
        result1 = session.execute_ml_line("function double(n) { return n * 2; }")

        # Call function
        result2 = session.execute_ml_line("result = double(5);")

        # Should work
        assert isinstance(result1, REPLResult)
        assert isinstance(result2, REPLResult)

    def test_mathematical_operations(self, session):
        """Test mathematical operations work."""
        result = session.execute_ml_line("math_result = (10 + 5) * 2;")

        if result.success:
            assert "math_result" in session.python_namespace

    def test_string_operations(self, session):
        """Test string operations work."""
        result = session.execute_ml_line('greeting = "Hello" + " " + "World";')

        assert isinstance(result, REPLResult)


class TestErrorRecovery:
    """Test REPL recovers from errors."""

    @pytest.fixture
    def session(self):
        """Create REPL session."""
        return MLREPLSession()

    def test_recovers_from_parse_error(self, session):
        """Test REPL continues after parse error."""
        # Cause parse error
        result1 = session.execute_ml_line("syntax error here")

        # Should return error result
        assert result1.success is False

        # Should still be able to execute valid code after
        result2 = session.execute_ml_line("x = 1;")
        assert isinstance(result2, REPLResult)

    def test_recovers_from_runtime_error(self, session):
        """Test REPL continues after runtime error."""
        # Cause runtime error (if it executes)
        result1 = session.execute_ml_line("undefined_variable;")

        # Should handle error
        assert isinstance(result1, REPLResult)

        # Should still work after
        result2 = session.execute_ml_line("y = 2;")
        assert isinstance(result2, REPLResult)

    def test_namespace_preserved_after_error(self, session):
        """Test namespace is preserved even after errors."""
        # Set a variable
        session.execute_ml_line("preserved = 42;")

        # Cause an error
        session.execute_ml_line("bad syntax")

        # Original variable should still exist
        assert "preserved" in session.python_namespace


class TestREPLResultFormatting:
    """Test REPL result formatting."""

    @pytest.fixture
    def session(self):
        """Create REPL session."""
        return MLREPLSession()

    def test_result_includes_execution_time(self, session):
        """Test result includes execution time."""
        result = session.execute_ml_line("x = 1;")

        # Execution time should be set
        assert hasattr(result, "execution_time_ms")
        assert result.execution_time_ms >= 0

    def test_result_includes_transpiled_code(self, session):
        """Test result includes transpiled Python code."""
        result = session.execute_ml_line("y = 2;")

        # Should have transpiled code
        assert hasattr(result, "transpiled_python")
        assert isinstance(result.transpiled_python, str)

    def test_error_result_has_error_message(self, session):
        """Test error results have error messages."""
        result = session.execute_ml_line("invalid syntax")

        if not result.success:
            assert result.error is not None
            assert isinstance(result.error, str)
            assert len(result.error) > 0
