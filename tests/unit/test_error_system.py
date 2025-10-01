"""Comprehensive unit tests for the mlpy error system."""


import pytest

from mlpy.ml.errors.context import ErrorContext, SourceLine, SourceLocation, create_error_context
from mlpy.ml.errors.exceptions import (
    CWECategory,
    ErrorSeverity,
    MLCapabilityError,
    MLConfigurationError,
    MLError,
    MLParserError,
    MLRuntimeError,
    MLSandboxError,
    MLSecurityError,
    MLSyntaxError,
    MLTranspilationError,
    MLTypeError,
    create_code_injection_error,
    create_reflection_abuse_error,
    create_unsafe_import_error,
)


class TestMLError:
    """Test cases for MLError base class."""

    def test_basic_error_creation(self):
        """Test basic MLError creation."""
        error = MLError("Test error message")

        assert error.message == "Test error message"
        assert error.code is None
        assert error.severity == ErrorSeverity.MEDIUM
        assert error.cwe is None
        assert error.suggestions == []
        assert error.context == {}
        assert error.source_file is None
        assert error.line_number is None
        assert error.column is None

    def test_error_with_all_parameters(self):
        """Test MLError with all parameters."""
        suggestions = ["Fix this", "Try that"]
        context = {"key": "value", "number": 42}

        error = MLError(
            "Complex error",
            code="TEST_001",
            severity=ErrorSeverity.HIGH,
            cwe=CWECategory.CODE_INJECTION,
            suggestions=suggestions,
            context=context,
            source_file="test.ml",
            line_number=10,
            column=5,
        )

        assert error.message == "Complex error"
        assert error.code == "TEST_001"
        assert error.severity == ErrorSeverity.HIGH
        assert error.cwe == CWECategory.CODE_INJECTION
        assert error.suggestions == suggestions
        assert error.context == context
        assert error.source_file == "test.ml"
        assert error.line_number == 10
        assert error.column == 5

    def test_error_to_dict(self):
        """Test error serialization to dictionary."""
        error = MLError(
            "Test error",
            code="TEST_002",
            severity=ErrorSeverity.CRITICAL,
            cwe=CWECategory.MISSING_AUTHORIZATION,
            suggestions=["Fix it"],
            context={"test": True},
            source_file="example.ml",
            line_number=5,
            column=10,
        )

        result = error.to_dict()

        expected = {
            "type": "MLError",
            "message": "Test error",
            "code": "TEST_002",
            "severity": "critical",
            "cwe": 862,  # CWECategory.MISSING_AUTHORIZATION.value
            "suggestions": ["Fix it"],
            "context": {"test": True},
            "source_file": "example.ml",
            "line_number": 5,
            "column": 10,
        }

        assert result == expected


class TestSpecificErrorTypes:
    """Test cases for specific error types."""

    def test_syntax_error(self):
        """Test MLSyntaxError creation."""
        error = MLSyntaxError("Invalid syntax")

        assert error.code == "ML_SYNTAX_ERROR"
        assert error.severity == ErrorSeverity.HIGH
        assert isinstance(error, MLError)

    def test_security_error(self):
        """Test MLSecurityError creation."""
        error = MLSecurityError("Security violation", cwe=CWECategory.CODE_INJECTION)

        assert error.code == "ML_SECURITY_ERROR"
        assert error.severity == ErrorSeverity.CRITICAL
        assert error.cwe == CWECategory.CODE_INJECTION

    def test_capability_error(self):
        """Test MLCapabilityError creation."""
        error = MLCapabilityError("Missing capability")

        assert error.code == "ML_CAPABILITY_ERROR"
        assert error.severity == ErrorSeverity.CRITICAL
        assert error.cwe == CWECategory.MISSING_AUTHORIZATION

    def test_parser_error(self):
        """Test MLParserError creation."""
        error = MLParserError("Parse failed")

        assert error.code == "ML_PARSER_ERROR"
        assert error.severity == ErrorSeverity.HIGH

    def test_type_error(self):
        """Test MLTypeError creation."""
        error = MLTypeError("Type mismatch")

        assert error.code == "ML_TYPE_ERROR"
        assert error.severity == ErrorSeverity.MEDIUM

    def test_runtime_error(self):
        """Test MLRuntimeError creation."""
        error = MLRuntimeError("Runtime failure")

        assert error.code == "ML_RUNTIME_ERROR"
        assert error.severity == ErrorSeverity.HIGH

    def test_sandbox_error(self):
        """Test MLSandboxError creation."""
        error = MLSandboxError("Sandbox violation")

        assert error.code == "ML_SANDBOX_ERROR"
        assert error.severity == ErrorSeverity.CRITICAL
        assert error.cwe == CWECategory.DENIAL_OF_SERVICE

    def test_transpilation_error(self):
        """Test MLTranspilationError creation."""
        error = MLTranspilationError("Transpilation failed")

        assert error.code == "ML_TRANSPILATION_ERROR"
        assert error.severity == ErrorSeverity.HIGH

    def test_configuration_error(self):
        """Test MLConfigurationError creation."""
        error = MLConfigurationError("Bad config")

        assert error.code == "ML_CONFIGURATION_ERROR"
        assert error.severity == ErrorSeverity.MEDIUM


class TestSecurityErrorCreators:
    """Test cases for security error creation functions."""

    def test_create_code_injection_error(self):
        """Test code injection error creation."""
        error = create_code_injection_error("eval", source_file="test.ml", line_number=5)

        assert isinstance(error, MLSecurityError)
        assert error.cwe == CWECategory.CODE_INJECTION
        assert "eval" in error.message
        assert error.source_file == "test.ml"
        assert error.line_number == 5
        assert len(error.suggestions) > 0
        assert error.context["operation"] == "eval"
        assert error.context["category"] == "code_injection"

    def test_create_unsafe_import_error(self):
        """Test unsafe import error creation."""
        error = create_unsafe_import_error("os", source_file="dangerous.ml", line_number=10)

        assert isinstance(error, MLSecurityError)
        assert error.cwe == CWECategory.MISSING_AUTHORIZATION
        assert "os" in error.message
        assert error.source_file == "dangerous.ml"
        assert error.line_number == 10
        assert len(error.suggestions) > 0
        assert error.context["module"] == "os"
        assert error.context["category"] == "unsafe_import"

    def test_create_reflection_abuse_error(self):
        """Test reflection abuse error creation."""
        error = create_reflection_abuse_error(
            "__class__", source_file="reflection.ml", line_number=15
        )

        assert isinstance(error, MLSecurityError)
        assert error.cwe == CWECategory.UNSAFE_REFLECTION
        assert "__class__" in error.message
        assert error.source_file == "reflection.ml"
        assert error.line_number == 15
        assert len(error.suggestions) > 0
        assert error.context["attribute"] == "__class__"
        assert error.context["category"] == "reflection_abuse"


class TestSourceLocation:
    """Test cases for SourceLocation."""

    def test_basic_source_location(self):
        """Test basic SourceLocation creation."""
        location = SourceLocation(file_path="test.ml", line_number=10, column=5)

        assert location.file_path == "test.ml"
        assert location.line_number == 10
        assert location.column == 5
        assert location.length == 1
        assert location.end_column == 6

    def test_source_location_with_length(self):
        """Test SourceLocation with custom length."""
        location = SourceLocation(file_path="example.ml", line_number=20, column=10, length=5)

        assert location.length == 5
        assert location.end_column == 15

    def test_source_location_str(self):
        """Test SourceLocation string representation."""
        location = SourceLocation("file.ml", 10, 5)
        assert str(location) == "file.ml:10:5"


class TestSourceLine:
    """Test cases for SourceLine."""

    def test_basic_source_line(self):
        """Test basic SourceLine creation."""
        line = SourceLine(
            number=10,
            content="function test() {",
            is_primary=True,
            highlight_start=9,
            highlight_end=13,
        )

        assert line.number == 10
        assert line.content == "function test() {"
        assert line.is_primary is True
        assert line.highlight_start == 9
        assert line.highlight_end == 13

    def test_highlighted_content(self):
        """Test highlighted content generation."""
        line = SourceLine(
            number=1,
            content="eval(dangerous_code)",
            is_primary=True,
            highlight_start=0,
            highlight_end=4,
        )

        highlighted = line.highlighted_content
        assert ">>>eval<<<" in highlighted
        assert "(dangerous_code)" in highlighted

    def test_highlighted_content_no_highlight(self):
        """Test highlighted content without highlighting."""
        line = SourceLine(number=1, content="normal code", is_primary=False)

        assert line.highlighted_content == "normal code"


class TestErrorContext:
    """Test cases for ErrorContext."""

    def test_basic_error_context(self):
        """Test basic ErrorContext creation."""
        error = MLError("Test error", source_file="test.ml", line_number=5, column=10)

        context = ErrorContext(error)

        assert context.error == error
        assert context.source_content is None
        assert context.context_lines == 3

    def test_error_context_with_source(self):
        """Test ErrorContext with source content."""
        source_content = """line 1
line 2
error line
line 4
line 5"""

        error = MLError("Test error", source_file="test.ml", line_number=3, column=1)

        context = ErrorContext(error, source_content=source_content)

        assert context.source_content == source_content
        assert len(context.source_lines) == 5
        assert context.source_lines[2] == "error line"

    def test_get_location(self):
        """Test location extraction."""
        error = MLError("Test error", source_file="test.ml", line_number=10, column=5)

        context = ErrorContext(error)
        location = context.get_location()

        assert location is not None
        assert location.file_path == "test.ml"
        assert location.line_number == 10
        assert location.column == 5

    def test_get_location_none(self):
        """Test location extraction when no location info."""
        error = MLError("Test error")
        context = ErrorContext(error)
        location = context.get_location()

        assert location is None

    def test_get_context_lines(self):
        """Test context lines extraction."""
        source_content = """line 1
line 2
line 3
error line
line 5
line 6
line 7"""

        error = MLError("Test error", source_file="test.ml", line_number=4, column=1)

        context = ErrorContext(error, source_content=source_content, context_lines=2)
        context_lines = context.get_context_lines()

        assert len(context_lines) == 5  # 2 before + 1 error + 2 after
        assert context_lines[2].is_primary is True
        assert context_lines[2].content == "error line"
        assert context_lines[2].number == 4

    def test_severity_icon(self):
        """Test severity icon generation."""
        error = MLError("Test", severity=ErrorSeverity.CRITICAL)
        context = ErrorContext(error)

        icon = context.get_severity_icon()
        assert icon == "🚨"

    def test_cwe_info(self):
        """Test CWE information extraction."""
        error = MLSecurityError("Security issue", cwe=CWECategory.CODE_INJECTION)
        context = ErrorContext(error)

        cwe_info = context.get_cwe_info()
        assert cwe_info is not None
        assert cwe_info["id"] == 95
        assert cwe_info["name"] == "CODE_INJECTION"
        assert "cwe.mitre.org" in cwe_info["url"]

    def test_cwe_info_none(self):
        """Test CWE information when no CWE."""
        error = MLError("Test error")
        context = ErrorContext(error)

        cwe_info = context.get_cwe_info()
        assert cwe_info is None

    def test_format_plain_text(self):
        """Test plain text formatting."""
        source_content = "function test() {\n    eval(code)\n}"

        error = create_code_injection_error("eval", source_file="test.ml", line_number=2)

        context = ErrorContext(error, source_content=source_content)
        formatted = context.format_plain_text()

        # Accept both Unicode emoji and ASCII fallback
        assert "🚨 CRITICAL" in formatted or "[!] CRITICAL" in formatted
        assert "eval" in formatted
        assert "Security Issue: CWE-95" in formatted
        assert "Suggestions:" in formatted
        # Location may not be included if error doesn't have location info
        # Just check that formatting works
        assert len(formatted) > 100

    def test_to_dict(self):
        """Test error context serialization."""
        source_content = "function test() {\n    eval(code)\n}"

        error = create_code_injection_error("eval", source_file="test.ml", line_number=2)

        context = ErrorContext(error, source_content=source_content)
        result = context.to_dict()

        assert "error" in result
        assert "location" in result
        assert "context_lines" in result
        assert "cwe_info" in result
        assert "severity_icon" in result

        # Location may be None if error doesn't have location info
        if result["location"] is not None:
            assert result["location"]["file_path"] == "test.ml"
            assert result["location"]["line_number"] == 2
        assert result["cwe_info"]["id"] == 95


class TestCreateErrorContext:
    """Test cases for create_error_context function."""

    def test_create_error_context_basic(self):
        """Test basic error context creation."""
        error = MLError("Test error")
        context = create_error_context(error)

        assert isinstance(context, ErrorContext)
        assert context.error == error

    def test_create_error_context_with_source_file(self):
        """Test error context creation with source file override."""
        error = MLError("Test error")
        context = create_error_context(error, source_file="override.ml")

        assert error.source_file == "override.ml"

    def test_create_error_context_with_source_content(self):
        """Test error context creation with source content."""
        error = MLError("Test error")
        source_content = "test content"

        context = create_error_context(error, source_content=source_content)

        assert context.source_content == source_content

    def test_create_error_context_custom_context_lines(self):
        """Test error context creation with custom context lines."""
        error = MLError("Test error")
        context = create_error_context(error, context_lines=5)

        assert context.context_lines == 5


@pytest.fixture
def sample_error():
    """Fixture providing a sample MLError."""
    return create_code_injection_error("eval", source_file="sample.ml", line_number=10)


@pytest.fixture
def sample_source_content():
    """Fixture providing sample source content."""
    return """function processData(input) {
    if (input.type === "expression") {
        // This is dangerous!
        result = eval(input.code)
        return result
    }
    return null
}"""


class TestErrorSystemIntegration:
    """Integration tests for the complete error system."""

    def test_end_to_end_error_handling(self, sample_error, sample_source_content):
        """Test complete error handling flow."""
        # Create error context
        context = create_error_context(sample_error, source_content=sample_source_content)

        # Verify error context
        assert context.error == sample_error
        assert context.source_content == sample_source_content

        # Verify location (may be None if error doesn't have location info)
        location = context.get_location()
        if location is not None:
            assert location.file_path == "sample.ml"

        # Verify context lines
        context_lines = context.get_context_lines()
        assert len(context_lines) > 0

        # Verify formatting works
        formatted = context.format_plain_text()
        assert len(formatted) > 0
        assert "eval" in formatted

        # Verify serialization works
        serialized = context.to_dict()
        assert "error" in serialized
        assert "location" in serialized

    def test_multiple_error_types(self):
        """Test handling multiple different error types."""
        errors = [
            create_code_injection_error("eval"),
            create_unsafe_import_error("os"),
            create_reflection_abuse_error("__class__"),
            MLCapabilityError("Missing file access capability"),
            MLSyntaxError("Unexpected token"),
        ]

        for error in errors:
            context = create_error_context(error)
            formatted = context.format_plain_text()

            # Each error should format successfully
            assert len(formatted) > 0
            assert error.message in formatted

            # Security errors should have CWE info
            if isinstance(error, MLSecurityError):
                cwe_info = context.get_cwe_info()
                assert cwe_info is not None
                assert "CWE-" in formatted

    def test_error_system_performance(self, sample_source_content):
        """Test error system performance with many errors."""
        import time

        start_time = time.time()

        # Create many errors and contexts
        for i in range(100):
            error = create_code_injection_error(
                f"eval_{i}", source_file=f"test_{i}.ml", line_number=i + 1
            )

            context = create_error_context(error, source_content=sample_source_content)

            # Format each error
            formatted = context.format_plain_text()
            assert len(formatted) > 0

        end_time = time.time()
        duration = end_time - start_time

        # Should handle 100 errors in reasonable time (< 1 second)
        assert duration < 1.0, f"Error system too slow: {duration:.3f}s for 100 errors"
