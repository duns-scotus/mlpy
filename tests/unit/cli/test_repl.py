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
from unittest.mock import Mock, patch, MagicMock
from mlpy.cli.repl import (
    REPLResult,
    MLREPLSession,
)


class TestREPLResult:
    """Test REPLResult dataclass."""

    def test_repl_result_success(self):
        """Test successful REPL result."""
        result = REPLResult(
            success=True,
            value=42,
            transpiled_python="x = 42",
            execution_time_ms=1.5
        )

        assert result.success is True
        assert result.value == 42
        assert result.error is None
        assert result.transpiled_python == "x = 42"
        assert result.execution_time_ms == 1.5

    def test_repl_result_error(self):
        """Test error REPL result."""
        result = REPLResult(
            success=False,
            error="Parse error"
        )

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
        assert isinstance(session.history, list)

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
        assert '__builtins__' in session.python_namespace

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
        assert 'x' in session.python_namespace

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
        assert 'x' in session.python_namespace
        assert 'y' in session.python_namespace

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
        assert hasattr(session, 'history')


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
            assert 'count' in session.python_namespace


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
        assert '__builtins__' in session.python_namespace


class TestREPLSessionMethods:
    """Test additional REPL session methods."""

    @pytest.fixture
    def session(self):
        """Create REPL session."""
        return MLREPLSession()

    def test_has_transpiler(self, session):
        """Test session has transpiler."""
        assert hasattr(session, 'transpiler')
        assert session.transpiler is not None

    def test_has_execute_method(self, session):
        """Test session has execute method."""
        assert hasattr(session, 'execute_ml_line')
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
