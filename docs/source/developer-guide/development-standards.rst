====================
Development Standards
====================

This document establishes comprehensive development standards for mlpy contributors. These standards ensure code quality, security, performance, and maintainability across the entire codebase.

Code Quality Standards
======================

Python Code Standards
---------------------

**PEP 8 Compliance with Extensions**:

.. code-block:: python

    # Maximum line length: 100 characters (extended from PEP 8's 79)
    def long_function_name_that_demonstrates_line_length_guidelines(
        parameter_one: str,
        parameter_two: int,
        parameter_three: Optional[dict] = None
    ) -> ComplexReturnType:
        """Function demonstrating proper formatting standards."""
        pass

    # Type hints are mandatory for all public APIs
    def process_ml_code(
        source_code: str,
        source_file: str | None = None,
        strict_security: bool = True
    ) -> TranspilationResult:
        """Process ML source code with security validation."""
        pass

    # Use dataclasses for structured data
    @dataclass
    class SecurityIssue:
        severity: str
        category: str
        message: str
        line: int | None = None
        column: int | None = None
        context: dict[str, Any] = field(default_factory=dict)

**Import Organization**:

.. code-block:: python

    # 1. Standard library imports
    import ast
    import re
    from dataclasses import dataclass, field
    from typing import Any, Optional

    # 2. Third-party imports
    import lark
    import pytest

    # 3. Local application imports
    from mlpy.ml.grammar.ast_nodes import ASTNode, Expression
    from mlpy.ml.errors.exceptions import MLSecurityError
    from mlpy.runtime.capabilities.manager import CapabilityContext

**Naming Conventions**:

.. code-block:: python

    # Classes: PascalCase
    class SecurityAnalyzer:
        pass

    # Functions and variables: snake_case
    def analyze_security_patterns():
        pattern_count = 0
        return pattern_count

    # Constants: UPPER_SNAKE_CASE
    MAX_SECURITY_ISSUES = 100
    DEFAULT_TIMEOUT_SECONDS = 30.0

    # Private members: leading underscore
    class Parser:
        def __init__(self):
            self._internal_state = {}
            self.__very_private = None

Documentation Standards
======================

**Docstring Format** (Google Style):

.. code-block:: python

    def transpile_ml_code(
        source_code: str,
        source_file: str | None = None,
        strict_security: bool = True,
        generate_source_maps: bool = False
    ) -> TranspilationResult:
        """Transpile ML source code to Python with security validation.

        This function performs complete ML-to-Python transpilation including
        parsing, security analysis, and code generation. All operations are
        performed with capability-based security validation.

        Args:
            source_code: ML source code to transpile
            source_file: Optional source file path for error reporting
            strict_security: Enable strict security analysis mode
            generate_source_maps: Generate source maps for debugging

        Returns:
            TranspilationResult containing generated Python code, source maps,
            and security analysis results.

        Raises:
            MLSyntaxError: If source code contains syntax errors
            MLSecurityError: If security analysis detects threats
            TranspilationError: If code generation fails

        Example:
            >>> result = transpile_ml_code('function hello() { return "world" }')
            >>> print(result.python_code)
            def hello():
                return "world"

        Security:
            This function validates all code for security threats before
            generation. Set strict_security=False only for trusted code.

        Performance:
            Typical transpilation completes in <10ms. Large files may require
            additional processing time for security analysis.
        """
        pass

**Module Documentation**:

.. code-block:: python

    """ML Language Security Analysis Module.

    This module provides comprehensive security analysis for ML language constructs,
    detecting potential vulnerabilities through static analysis of AST structures.

    The security analyzer implements multiple detection strategies:
    - Pattern-based threat detection
    - Data flow analysis for taint propagation
    - Capability-based access validation
    - CWE-mapped vulnerability classification

    Example:
        from mlpy.ml.analysis.security_analyzer import SecurityAnalyzer

        analyzer = SecurityAnalyzer("source.ml")
        issues = analyzer.analyze(ast_node)

    Performance:
        The analyzer is optimized for sub-millisecond analysis of typical programs
        using parallel processing and intelligent caching strategies.

    Security:
        All security analysis is performed in isolated contexts to prevent
        analysis-time attacks or information leakage.
    """

Security Standards
=================

**Security-First Development Principles**:

1. **Fail Secure**: All error conditions default to secure behavior
2. **Least Privilege**: Functions request minimal capabilities required
3. **Input Validation**: All external input is validated before processing
4. **Output Sanitization**: All output is sanitized for the target context
5. **Audit Trail**: Security-relevant operations are logged comprehensively

**Capability-Based Security Implementation**:

.. code-block:: python

    from mlpy.runtime.capabilities.decorators import require_capability

    @require_capability("file:read:source")
    def read_source_file(file_path: str) -> str:
        """Read source file with capability validation.

        Security:
            Requires file:read:source capability for access.
            Path traversal attacks are prevented by validation.
        """
        # Validate file path to prevent directory traversal
        if not self.is_safe_file_path(file_path):
            raise SecurityError("Unsafe file path detected")

        # Read file with error handling
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except OSError as e:
            raise FileAccessError(f"Cannot read file: {e}")

    def is_safe_file_path(self, path: str) -> bool:
        """Validate file path for security."""
        # Check for directory traversal attempts
        if ".." in path or path.startswith("/"):
            return False

        # Check against allowed file extensions
        allowed_extensions = {'.ml', '.py', '.md', '.txt'}
        if not any(path.endswith(ext) for ext in allowed_extensions):
            return False

        return True

**Input Validation Patterns**:

.. code-block:: python

    def validate_ml_identifier(identifier: str) -> bool:
        """Validate ML language identifier for security."""
        if not isinstance(identifier, str):
            return False

        if len(identifier) == 0 or len(identifier) > 255:
            return False

        # Must start with letter or underscore
        if not (identifier[0].isalpha() or identifier[0] == '_'):
            return False

        # Must contain only alphanumeric and underscore
        if not all(c.isalnum() or c == '_' for c in identifier):
            return False

        # Check against reserved keywords
        if identifier in ML_RESERVED_KEYWORDS:
            return False

        return True

    def sanitize_error_message(message: str) -> str:
        """Sanitize error message to prevent information leakage."""
        # Remove file system paths
        message = re.sub(r'/[^\s]+', '<path>', message)

        # Remove sensitive patterns
        sensitive_patterns = [
            r'password[=:]\w+',
            r'token[=:]\w+',
            r'key[=:]\w+'
        ]

        for pattern in sensitive_patterns:
            message = re.sub(pattern, '<redacted>', message, flags=re.IGNORECASE)

        return message

Performance Standards
====================

**Performance Targets**:

.. code-block:: python

    # Performance requirements for core operations
    PERFORMANCE_TARGETS = {
        'lexical_analysis': 0.1,      # milliseconds
        'syntax_parsing': 0.5,        # milliseconds
        'security_analysis': 1.0,     # milliseconds
        'code_generation': 1.0,       # milliseconds
        'full_transpilation': 10.0,   # milliseconds
        'capability_check': 0.01,     # milliseconds
    }

**Performance Monitoring**:

.. code-block:: python

    from functools import wraps
    import time
    from mlpy.runtime.profiling.monitor import performance_monitor

    def performance_critical(target_ms: float):
        """Decorator for performance-critical functions."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()

                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    elapsed_ms = (time.perf_counter() - start_time) * 1000

                    if elapsed_ms > target_ms:
                        performance_monitor.record_slowdown(
                            function=func.__name__,
                            target_ms=target_ms,
                            actual_ms=elapsed_ms
                        )
            return wrapper
        return decorator

    @performance_critical(1.0)  # Target: 1ms
    def analyze_security(ast_node: ASTNode) -> list[SecurityIssue]:
        """Analyze AST for security issues."""
        pass

**Memory Management**:

.. code-block:: python

    import weakref
    from typing import Protocol

    class ResourceManager(Protocol):
        """Protocol for managed resources."""
        def cleanup(self) -> None: ...

    class ManagedResource:
        """Base class for resources requiring cleanup."""
        _instances = weakref.WeakSet()

        def __init__(self):
            self._instances.add(self)
            self._cleanup_callbacks: list[callable] = []

        def add_cleanup_callback(self, callback: callable) -> None:
            """Add callback for resource cleanup."""
            self._cleanup_callbacks.append(callback)

        def cleanup(self) -> None:
            """Clean up managed resources."""
            for callback in self._cleanup_callbacks:
                try:
                    callback()
                except Exception as e:
                    logger.warning(f"Cleanup callback failed: {e}")

        @classmethod
        def cleanup_all(cls) -> None:
            """Clean up all managed instances."""
            for instance in list(cls._instances):
                instance.cleanup()

Testing Standards
================

**Test Structure and Organization**:

.. code-block:: python

    # tests/test_security_analyzer.py
    """Comprehensive tests for security analysis functionality."""

    import pytest
    from unittest.mock import Mock, patch

    from mlpy.ml.analysis.security_analyzer import SecurityAnalyzer
    from mlpy.ml.grammar.ast_nodes import FunctionCall, StringLiteral
    from mlpy.ml.errors.exceptions import MLSecurityError


    class TestSecurityAnalyzer:
        """Test suite for SecurityAnalyzer class."""

        def setup_method(self):
            """Set up test fixtures."""
            self.analyzer = SecurityAnalyzer("test.ml")
            self.mock_ast = self.create_test_ast()

        def teardown_method(self):
            """Clean up after tests."""
            self.analyzer.cleanup()

        @pytest.mark.security
        def test_detects_code_injection_eval(self):
            """Test detection of eval() code injection vulnerability."""
            # Arrange
            eval_call = FunctionCall(
                function="eval",
                arguments=[StringLiteral("user_input")],
                line=1,
                column=1
            )

            # Act
            self.analyzer.visit_function_call(eval_call)
            issues = self.analyzer.issues

            # Assert
            assert len(issues) == 1
            assert issues[0].severity == "critical"
            assert issues[0].category == "code_injection"
            assert "eval" in issues[0].message.lower()

        @pytest.mark.performance
        def test_analysis_performance_target(self, benchmark):
            """Test that security analysis meets performance targets."""
            # Arrange
            large_ast = self.create_large_test_ast(nodes=1000)

            # Act & Assert
            result = benchmark(self.analyzer.analyze, large_ast)
            assert result is not None
            # benchmark automatically validates against performance targets

        @pytest.mark.parametrize("function_name,expected_severity", [
            ("eval", "critical"),
            ("exec", "critical"),
            ("getattr", "high"),
            ("open", "medium"),
        ])
        def test_dangerous_function_detection(self, function_name, expected_severity):
            """Test detection of various dangerous functions."""
            # Arrange
            func_call = FunctionCall(
                function=function_name,
                arguments=[StringLiteral("test")],
                line=1,
                column=1
            )

            # Act
            self.analyzer.visit_function_call(func_call)

            # Assert
            issues = [i for i in self.analyzer.issues if i.category == "code_injection"]
            assert len(issues) == 1
            assert issues[0].severity == expected_severity

        @pytest.fixture
        def mock_capability_context(self):
            """Provide mock capability context for testing."""
            with patch('mlpy.runtime.capabilities.get_current_context') as mock:
                mock.return_value.check.return_value = True
                yield mock.return_value

**Test Categories and Markers**:

.. code-block:: python

    # pytest.ini configuration
    [tool:pytest]
    markers =
        security: Security-related tests
        performance: Performance validation tests
        integration: Integration tests with external systems
        slow: Tests that take longer than 1 second
        capability: Capability system tests
        sandbox: Sandbox execution tests

**Coverage Requirements**:

.. code-block:: python

    # pyproject.toml
    [tool.coverage.run]
    source = ["src/mlpy"]
    omit = [
        "*/tests/*",
        "*/test_*.py",
        "*/__pycache__/*"
    ]

    [tool.coverage.report]
    exclude_lines = [
        "pragma: no cover",
        "def __repr__",
        "raise AssertionError",
        "raise NotImplementedError",
        "if __name__ == .__main__.:",
        "@abstract"
    ]

    # Minimum coverage requirements
    fail_under = 95  # Core components must have 95%+ coverage
    show_missing = true
    precision = 2

Error Handling Standards
=======================

**Exception Hierarchy**:

.. code-block:: python

    # Base exceptions
    class MLError(Exception):
        """Base exception for all ML-related errors."""
        pass

    class MLSyntaxError(MLError):
        """Syntax errors in ML code."""
        pass

    class MLSecurityError(MLError):
        """Security-related errors."""
        def __init__(self, message: str, cwe: str = None, **context):
            super().__init__(message)
            self.cwe = cwe
            self.context = context

    class MLRuntimeError(MLError):
        """Runtime execution errors."""
        pass

    # Specific error types
    class CapabilityError(MLSecurityError):
        """Insufficient capabilities for operation."""
        pass

    class ValidationError(MLError):
        """Input validation failures."""
        pass

**Error Context and Reporting**:

.. code-block:: python

    from dataclasses import dataclass
    from typing import Optional, Any

    @dataclass
    class ErrorContext:
        """Rich error context for debugging."""
        error: Exception
        source_file: Optional[str] = None
        line_number: Optional[int] = None
        column_number: Optional[int] = None
        source_context: Optional[str] = None
        stack_trace: Optional[str] = None
        suggestions: list[str] = field(default_factory=list)
        related_errors: list['ErrorContext'] = field(default_factory=list)

    def create_error_context(
        error: Exception,
        source_file: str = None,
        line: int = None,
        column: int = None
    ) -> ErrorContext:
        """Create comprehensive error context."""

        # Extract source context if available
        source_context = None
        if source_file and line:
            source_context = extract_source_context(source_file, line)

        # Generate helpful suggestions
        suggestions = generate_error_suggestions(error, source_context)

        return ErrorContext(
            error=error,
            source_file=source_file,
            line_number=line,
            column_number=column,
            source_context=source_context,
            stack_trace=format_stack_trace(error),
            suggestions=suggestions
        )

Git and Version Control Standards
=================================

**Commit Message Format**:

.. code-block:: text

    <type>(<scope>): <description>

    [optional body]

    [optional footer]

**Types**:
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (no functionality change)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Test additions or modifications
- **security**: Security improvements
- **chore**: Build process or auxiliary tool changes

**Examples**:

.. code-block:: text

    feat(security): add SQL injection detection to security analyzer

    Implement comprehensive SQL injection pattern detection including:
    - String concatenation analysis
    - Template literal validation
    - Dynamic query construction detection

    Closes #123

    ---

    fix(parser): resolve parsing error with nested expressions

    Fixed issue where deeply nested expressions caused stack overflow
    in the AST transformer. Added iterative processing for deep nesting.

    Performance impact: Minimal (<1% overhead)
    Security impact: None

    ---

    security(capabilities): strengthen capability validation

    Enhanced capability validation to prevent privilege escalation:
    - Added capability inheritance validation
    - Implemented token expiration checking
    - Added audit logging for capability grants

    BREAKING CHANGE: Capability tokens now require explicit expiration

**Branch Naming**:

.. code-block:: text

    # Feature branches
    feature/sql-injection-detection
    feature/async-await-support

    # Bug fix branches
    fix/parser-stack-overflow
    fix/memory-leak-in-analyzer

    # Security branches
    security/capability-validation-hardening
    security/input-sanitization-improvement

    # Documentation branches
    docs/developer-guide-update
    docs/api-reference-completion

Code Review Standards
====================

**Review Checklist**:

1. **Functionality**
   - [ ] Code works as intended
   - [ ] Edge cases are handled
   - [ ] Error conditions are managed properly

2. **Security**
   - [ ] Input validation is comprehensive
   - [ ] Capabilities are properly checked
   - [ ] No information leakage in error messages
   - [ ] No hardcoded credentials or secrets

3. **Performance**
   - [ ] Meets performance targets
   - [ ] No unnecessary memory allocations
   - [ ] Efficient algorithms used
   - [ ] Proper resource cleanup

4. **Code Quality**
   - [ ] Follows coding standards
   - [ ] Proper documentation
   - [ ] Appropriate test coverage
   - [ ] Clear and maintainable structure

5. **Testing**
   - [ ] Unit tests cover new functionality
   - [ ] Integration tests validate behavior
   - [ ] Security tests verify threat prevention
   - [ ] Performance tests validate targets

**Review Process**:

.. code-block:: text

    1. Automated checks must pass before human review
       - Linting (ruff, black)
       - Type checking (mypy)
       - Security scanning
       - Test execution
       - Performance benchmarks

    2. Human review requirements:
       - At least one approving review from code owner
       - Security review for security-sensitive changes
       - Performance review for performance-critical changes

    3. Final validation:
       - All conversations resolved
       - CI/CD pipeline passes completely
       - Documentation updated if needed

These development standards ensure that mlpy maintains high quality, security, and performance characteristics while remaining maintainable and accessible to contributors.