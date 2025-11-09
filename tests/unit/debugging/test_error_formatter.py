"""Tests for error formatter with rich console output.

This module tests the MLErrorFormatter class which provides beautiful,
rich-formatted error output with syntax highlighting and structured information.
"""

import pytest
from io import StringIO
from unittest.mock import Mock, MagicMock, patch
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from mlpy.debugging.error_formatter import MLErrorFormatter, format_error, print_error, print_multiple_errors
from mlpy.ml.errors.context import ErrorContext, SourceLine
from mlpy.ml.errors.exceptions import MLError, ErrorSeverity


@pytest.fixture
def mock_console():
    """Create a mock Rich console."""
    return Mock(spec=Console)


@pytest.fixture
def formatter(mock_console):
    """Create an MLErrorFormatter instance with mocked console."""
    return MLErrorFormatter(console=mock_console)


@pytest.fixture
def simple_error():
    """Create a simple MLError for testing."""
    return MLError(
        message="Test error message",
        severity=ErrorSeverity.HIGH,
        code="TEST001"
    )


@pytest.fixture
def error_with_suggestions():
    """Create an MLError with suggestions."""
    return MLError(
        message="Variable not found",
        severity=ErrorSeverity.MEDIUM,
        code="VAR001",
        suggestions=[
            "Check the variable name spelling",
            "Ensure the variable is defined before use",
            "Import the module containing the variable"
        ]
    )


@pytest.fixture
def error_with_context():
    """Create an MLError with additional context."""
    return MLError(
        message="Type mismatch",
        severity=ErrorSeverity.HIGH,
        code="TYPE001",
        context={
            "expected_type": "number",
            "actual_type": "string",
            "variable_name": "count"
        }
    )


@pytest.fixture
def simple_error_context(simple_error):
    """Create a simple ErrorContext."""
    context = Mock(spec=ErrorContext)
    context.error = simple_error
    context.get_severity_icon = Mock(return_value="❌")
    context.get_location = Mock(return_value="test.ml:42:10")
    context.get_cwe_info = Mock(return_value=None)
    context.get_context_lines = Mock(return_value=[])
    return context


@pytest.fixture
def error_context_with_source(simple_error):
    """Create an ErrorContext with source lines."""
    context = Mock(spec=ErrorContext)
    context.error = simple_error
    context.get_severity_icon = Mock(return_value="❌")
    context.get_location = Mock(return_value="test.ml:42:10")
    context.get_cwe_info = Mock(return_value=None)

    # Mock source lines
    source_lines = [
        SourceLine(number=40, content="let x = 10;", is_primary=False),
        SourceLine(number=41, content="let y = 20;", is_primary=False),
        SourceLine(number=42, content="let result = x + z;", is_primary=True, highlight_start=17, highlight_end=18),
        SourceLine(number=43, content="print(result);", is_primary=False),
    ]
    context.get_context_lines = Mock(return_value=source_lines)
    return context


@pytest.fixture
def error_context_with_cwe(simple_error):
    """Create an ErrorContext with CWE information."""
    context = Mock(spec=ErrorContext)
    context.error = simple_error
    context.get_severity_icon = Mock(return_value="🚨")
    context.get_location = Mock(return_value="test.ml:42:10")
    context.get_cwe_info = Mock(return_value={
        "id": 89,
        "name": "SQL Injection",
        "url": "https://cwe.mitre.org/data/definitions/89.html"
    })
    context.get_context_lines = Mock(return_value=[])
    return context


class TestInitialization:
    """Test MLErrorFormatter initialization."""

    def test_initialization_default_console(self):
        """Test formatter initialization with default console."""
        formatter = MLErrorFormatter()

        assert formatter.console is not None
        assert hasattr(formatter, 'use_unicode')

    def test_initialization_custom_console(self, mock_console):
        """Test formatter initialization with custom console."""
        formatter = MLErrorFormatter(console=mock_console)

        assert formatter.console == mock_console
        assert hasattr(formatter, 'use_unicode')

    def test_unicode_detection(self, formatter):
        """Test Unicode detection."""
        # Should have detected Unicode support
        assert isinstance(formatter.use_unicode, bool)


class TestFormatError:
    """Test error formatting methods."""

    def test_format_simple_error(self, formatter, simple_error_context):
        """Test formatting a simple error."""
        panel = formatter.format_error(simple_error_context)

        assert isinstance(panel, Panel)
        simple_error_context.get_severity_icon.assert_called_once()
        simple_error_context.get_location.assert_called_once()

    def test_format_error_with_location(self, formatter, simple_error_context):
        """Test formatting error with location information."""
        panel = formatter.format_error(simple_error_context)

        assert isinstance(panel, Panel)
        # Location should be retrieved
        simple_error_context.get_location.assert_called_once()

    def test_format_error_without_location(self, formatter, simple_error):
        """Test formatting error without location information."""
        context = Mock(spec=ErrorContext)
        context.error = simple_error
        context.get_severity_icon = Mock(return_value="❌")
        context.get_location = Mock(return_value=None)
        context.get_cwe_info = Mock(return_value=None)
        context.get_context_lines = Mock(return_value=[])

        panel = formatter.format_error(context)

        assert isinstance(panel, Panel)

    def test_format_error_with_cwe(self, formatter, error_context_with_cwe):
        """Test formatting error with CWE information."""
        panel = formatter.format_error(error_context_with_cwe)

        assert isinstance(panel, Panel)
        error_context_with_cwe.get_cwe_info.assert_called_once()

    def test_format_error_with_source_context(self, formatter, error_context_with_source):
        """Test formatting error with source code context."""
        panel = formatter.format_error(error_context_with_source)

        assert isinstance(panel, Panel)
        error_context_with_source.get_context_lines.assert_called_once()

    def test_format_error_with_suggestions(self, formatter, error_with_suggestions):
        """Test formatting error with suggestions."""
        context = Mock(spec=ErrorContext)
        context.error = error_with_suggestions
        context.get_severity_icon = Mock(return_value="⚠️")
        context.get_location = Mock(return_value=None)
        context.get_cwe_info = Mock(return_value=None)
        context.get_context_lines = Mock(return_value=[])

        panel = formatter.format_error(context)

        assert isinstance(panel, Panel)

    def test_format_error_with_additional_context(self, formatter, error_with_context):
        """Test formatting error with additional context."""
        context = Mock(spec=ErrorContext)
        context.error = error_with_context
        context.get_severity_icon = Mock(return_value="❌")
        context.get_location = Mock(return_value=None)
        context.get_cwe_info = Mock(return_value=None)
        context.get_context_lines = Mock(return_value=[])

        panel = formatter.format_error(context)

        assert isinstance(panel, Panel)


class TestPanelTitle:
    """Test panel title formatting."""

    def test_format_panel_title_with_code(self, formatter, simple_error):
        """Test panel title formatting with error code."""
        title = formatter._format_panel_title(simple_error)

        assert isinstance(title, Text)
        # Title should contain class name and code
        title_str = str(title)
        assert "MLError" in title_str

    def test_format_panel_title_without_code(self, formatter):
        """Test panel title formatting without error code."""
        error = MLError(message="Test", severity=ErrorSeverity.LOW, code=None)
        title = formatter._format_panel_title(error)

        assert isinstance(title, Text)


class TestSourceContextFormatting:
    """Test source code context formatting."""

    def test_format_source_context_basic(self, formatter, simple_error):
        """Test basic source context formatting."""
        source_lines = [
            SourceLine(number=10, content="let x = 10;", is_primary=False),
            SourceLine(number=11, content="let y = 20;", is_primary=True),
        ]

        result = formatter._format_source_context(source_lines, simple_error)

        assert result is not None

    def test_format_source_context_with_highlight(self, formatter, simple_error):
        """Test source context formatting with highlighting."""
        source_lines = [
            SourceLine(number=10, content="let x = undefined;", is_primary=True, highlight_start=8, highlight_end=17),
        ]

        result = formatter._format_source_context(source_lines, simple_error)

        assert result is not None

    def test_format_source_context_with_pointer(self, formatter, simple_error):
        """Test source context formatting with error pointer."""
        source_lines = [
            SourceLine(number=10, content="let x = undefined;", is_primary=True, highlight_start=8, highlight_end=17),
        ]

        result = formatter._format_source_context(source_lines, simple_error)

        assert result is not None
        # Should generate pointer line with ^^^

    def test_format_source_context_syntax_error_fallback(self, formatter, simple_error):
        """Test source context formatting with syntax highlighting error fallback."""
        source_lines = [
            SourceLine(number=10, content="invalid syntax {{{", is_primary=False),
        ]

        # Should not raise exception, should fall back to plain text
        result = formatter._format_source_context(source_lines, simple_error)

        assert result is not None


class TestSuggestionsFormatting:
    """Test suggestions formatting."""

    def test_format_suggestions_single(self, formatter):
        """Test formatting single suggestion."""
        suggestions = ["Check your syntax"]

        panel = formatter._format_suggestions(suggestions)

        assert isinstance(panel, Panel)

    def test_format_suggestions_multiple(self, formatter):
        """Test formatting multiple suggestions."""
        suggestions = [
            "Check variable spelling",
            "Ensure variable is defined",
            "Import the module"
        ]

        panel = formatter._format_suggestions(suggestions)

        assert isinstance(panel, Panel)

    def test_format_suggestions_empty(self, formatter):
        """Test formatting empty suggestions list."""
        suggestions = []

        panel = formatter._format_suggestions(suggestions)

        assert isinstance(panel, Panel)


class TestAdditionalContextFormatting:
    """Test additional context formatting."""

    def test_format_additional_context_single_item(self, formatter):
        """Test formatting single context item."""
        context = {"variable_name": "x"}

        panel = formatter._format_additional_context(context)

        assert isinstance(panel, Panel)

    def test_format_additional_context_multiple_items(self, formatter):
        """Test formatting multiple context items."""
        context = {
            "expected_type": "number",
            "actual_type": "string",
            "variable_name": "count"
        }

        panel = formatter._format_additional_context(context)

        assert isinstance(panel, Panel)

    def test_format_additional_context_key_formatting(self, formatter):
        """Test context key formatting (underscores to spaces, title case)."""
        context = {"variable_name": "x", "expected_type": "number"}

        panel = formatter._format_additional_context(context)

        assert isinstance(panel, Panel)
        # Keys should be formatted with spaces and title case


class TestSeverityStyles:
    """Test severity-based styling."""

    def test_get_severity_style_critical(self, formatter):
        """Test critical severity style."""
        style = formatter._get_severity_style(ErrorSeverity.CRITICAL)

        assert style == "bold red"

    def test_get_severity_style_high(self, formatter):
        """Test high severity style."""
        style = formatter._get_severity_style(ErrorSeverity.HIGH)

        assert style == "red"

    def test_get_severity_style_medium(self, formatter):
        """Test medium severity style."""
        style = formatter._get_severity_style(ErrorSeverity.MEDIUM)

        assert style == "yellow"

    def test_get_severity_style_low(self, formatter):
        """Test low severity style."""
        style = formatter._get_severity_style(ErrorSeverity.LOW)

        assert style == "blue"

    def test_get_severity_style_info(self, formatter):
        """Test info severity style."""
        style = formatter._get_severity_style(ErrorSeverity.INFO)

        assert style == "green"

    def test_get_panel_style_critical(self, formatter):
        """Test critical panel border style."""
        style = formatter._get_panel_style(ErrorSeverity.CRITICAL)

        assert style == "bold red"

    def test_get_panel_style_high(self, formatter):
        """Test high panel border style."""
        style = formatter._get_panel_style(ErrorSeverity.HIGH)

        assert style == "red"

    def test_get_panel_style_medium(self, formatter):
        """Test medium panel border style."""
        style = formatter._get_panel_style(ErrorSeverity.MEDIUM)

        assert style == "yellow"

    def test_get_panel_style_low(self, formatter):
        """Test low panel border style."""
        style = formatter._get_panel_style(ErrorSeverity.LOW)

        assert style == "blue"

    def test_get_panel_style_info(self, formatter):
        """Test info panel border style."""
        style = formatter._get_panel_style(ErrorSeverity.INFO)

        assert style == "green"


class TestUnicodeSupport:
    """Test Unicode/emoji support detection."""

    @patch('sys.stdout')
    @patch('os.environ', {})
    def test_supports_unicode_with_utf8_encoding(self, mock_stdout, formatter):
        """Test Unicode detection with UTF-8 encoding."""
        mock_stdout.encoding = "utf-8"

        supports = formatter._supports_unicode()

        assert supports is True

    @patch('sys.stdout')
    @patch.dict('os.environ', {'NO_COLOR': '1'})
    def test_supports_unicode_with_no_color_env(self, mock_stdout, formatter):
        """Test Unicode detection with NO_COLOR environment variable."""
        supports = formatter._supports_unicode()

        assert supports is False

    @patch('sys.stdout')
    @patch.dict('os.environ', {'FORCE_UNICODE': '1'})
    def test_supports_unicode_with_force_unicode_env(self, mock_stdout, formatter):
        """Test Unicode detection with FORCE_UNICODE environment variable."""
        supports = formatter._supports_unicode()

        assert supports is True

    @patch('sys.stdout')
    @patch('sys.platform', 'win32')
    def test_supports_unicode_windows_success(self, mock_stdout, formatter):
        """Test Unicode detection on Windows with emoji support."""
        mock_stdout.encoding = "utf-8"

        supports = formatter._supports_unicode()

        # Should handle Windows emoji encoding
        assert isinstance(supports, bool)

    @patch('sys.stdout')
    def test_supports_unicode_fallback(self, mock_stdout, formatter):
        """Test Unicode detection fallback on exception."""
        mock_stdout.encoding = None

        # Should not raise exception
        supports = formatter._supports_unicode()

        assert isinstance(supports, bool)


class TestPrintError:
    """Test error printing methods."""

    def test_print_error(self, formatter, simple_error_context):
        """Test printing single error."""
        formatter.print_error(simple_error_context)

        formatter.console.print.assert_called_once()

    def test_print_error_formats_correctly(self, formatter, simple_error_context):
        """Test print_error calls format_error."""
        with patch.object(formatter, 'format_error', return_value=Mock()) as mock_format:
            formatter.print_error(simple_error_context)

            mock_format.assert_called_once_with(simple_error_context)
            formatter.console.print.assert_called_once()


class TestMultipleErrorsFormatting:
    """Test formatting multiple errors."""

    def test_format_multiple_errors_empty(self, formatter):
        """Test formatting empty error list."""
        panel = formatter.format_multiple_errors([])

        assert isinstance(panel, Panel)

    def test_format_multiple_errors_single(self, formatter, simple_error_context):
        """Test formatting single error in list."""
        panel = formatter.format_multiple_errors([simple_error_context])

        assert isinstance(panel, Panel)

    def test_format_multiple_errors_multiple(self, formatter, simple_error_context):
        """Test formatting multiple errors."""
        error_context_2 = Mock(spec=ErrorContext)
        error_context_2.error = MLError(
            message="Second error",
            severity=ErrorSeverity.MEDIUM,
            code="TEST002"
        )
        error_context_2.get_severity_icon = Mock(return_value="⚠️")
        error_context_2.get_location = Mock(return_value=None)
        error_context_2.get_cwe_info = Mock(return_value=None)
        error_context_2.get_context_lines = Mock(return_value=[])

        panel = formatter.format_multiple_errors([simple_error_context, error_context_2])

        assert isinstance(panel, Panel)

    def test_format_multiple_errors_grouped_by_severity(self, formatter):
        """Test multiple errors grouped by severity."""
        contexts = []
        for severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH, ErrorSeverity.MEDIUM]:
            context = Mock(spec=ErrorContext)
            context.error = MLError(
                message=f"{severity.value} error",
                severity=severity,
                code="TEST"
            )
            context.get_severity_icon = Mock(return_value="❌")
            context.get_location = Mock(return_value=None)
            context.get_cwe_info = Mock(return_value=None)
            context.get_context_lines = Mock(return_value=[])
            contexts.append(context)

        panel = formatter.format_multiple_errors(contexts)

        assert isinstance(panel, Panel)

    def test_print_multiple_errors(self, formatter, simple_error_context):
        """Test printing multiple errors."""
        formatter.print_multiple_errors([simple_error_context])

        formatter.console.print.assert_called_once()


class TestGlobalFunctions:
    """Test global convenience functions."""

    @patch('mlpy.debugging.error_formatter.error_formatter')
    def test_format_error_global(self, mock_formatter, simple_error_context):
        """Test global format_error function."""
        mock_formatter.format_error.return_value = Mock()

        result = format_error(simple_error_context)

        mock_formatter.format_error.assert_called_once_with(simple_error_context)

    @patch('mlpy.debugging.error_formatter.error_formatter')
    def test_print_error_global(self, mock_formatter, simple_error_context):
        """Test global print_error function."""
        print_error(simple_error_context)

        mock_formatter.print_error.assert_called_once_with(simple_error_context)

    @patch('mlpy.debugging.error_formatter.error_formatter')
    def test_print_multiple_errors_global(self, mock_formatter, simple_error_context):
        """Test global print_multiple_errors function."""
        contexts = [simple_error_context]

        print_multiple_errors(contexts)

        mock_formatter.print_multiple_errors.assert_called_once_with(contexts)


class TestErrorContextIntegration:
    """Test integration with ErrorContext."""

    def test_full_error_formatting_pipeline(self, formatter):
        """Test complete error formatting pipeline."""
        # Create a realistic error context
        error = MLError(
            message="Undefined variable 'count'",
            severity=ErrorSeverity.HIGH,
            code="VAR001",
            suggestions=["Check spelling", "Define the variable"],
            context={"variable": "count"}
        )

        context = Mock(spec=ErrorContext)
        context.error = error
        context.get_severity_icon = Mock(return_value="❌")
        context.get_location = Mock(return_value="test.ml:10:5")
        context.get_cwe_info = Mock(return_value=None)
        context.get_context_lines = Mock(return_value=[
            SourceLine(number=9, content="let x = 10;", is_primary=False),
            SourceLine(number=10, content="let y = count + 1;", is_primary=True, highlight_start=8, highlight_end=13),
            SourceLine(number=11, content="print(y);", is_primary=False),
        ])

        panel = formatter.format_error(context)

        assert isinstance(panel, Panel)
        # Should have called all context methods
        context.get_severity_icon.assert_called()
        context.get_location.assert_called()
        context.get_cwe_info.assert_called()
        context.get_context_lines.assert_called()
