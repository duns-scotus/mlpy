"""Rich error formatting with syntax highlighting and beautiful console output."""

from typing import Any

from rich import box
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from mlpy.ml.errors.context import ErrorContext, SourceLine
from mlpy.ml.errors.exceptions import ErrorSeverity, MLError


class MLErrorFormatter:
    """Rich formatter for MLError instances with beautiful console output."""

    def __init__(self, console: Console | None = None) -> None:
        """Initialize error formatter.

        Args:
            console: Rich console instance (creates default if None)
        """
        self.console = console or Console()

    def format_error(self, error_context: ErrorContext) -> Panel:
        """Format an error context as a Rich panel.

        Args:
            error_context: ErrorContext to format

        Returns:
            Rich Panel with formatted error
        """
        error = error_context.error

        # Create main content
        content_parts = []

        # Error message with icon
        message_text = Text()
        message_text.append(f"{error_context.get_severity_icon()} ", style="bold")
        message_text.append(error.message, style=self._get_severity_style(error.severity))
        content_parts.append(message_text)
        content_parts.append("")

        # Location information
        location = error_context.get_location()
        if location:
            location_text = Text()
            location_text.append("[LOCATION] Location: ", style="bold blue")
            location_text.append(str(location), style="cyan")
            content_parts.append(location_text)
            content_parts.append("")

        # CWE information
        cwe_info = error_context.get_cwe_info()
        if cwe_info:
            cwe_text = Text()
            cwe_text.append("[SECURITY] Security Issue: ", style="bold red")
            cwe_text.append(f"CWE-{cwe_info['id']}", style="red bold")
            cwe_text.append(f" ({cwe_info['name']})", style="red")
            content_parts.append(cwe_text)

            url_text = Text()
            url_text.append("[LINK] Reference: ", style="bold blue")
            url_text.append(cwe_info["url"], style="blue underline")
            content_parts.append(url_text)
            content_parts.append("")

        # Source code context
        context_lines = error_context.get_context_lines()
        if context_lines:
            content_parts.append(self._format_source_context(context_lines, error))
            content_parts.append("")

        # Suggestions
        if error.suggestions:
            content_parts.append(self._format_suggestions(error.suggestions))
            content_parts.append("")

        # Additional context
        if error.context:
            content_parts.append(self._format_additional_context(error.context))

        # Create panel
        panel_title = self._format_panel_title(error)
        panel_style = self._get_panel_style(error.severity)

        # Convert content parts to renderable format
        renderable_content = []
        for part in content_parts:
            if hasattr(part, "__rich__") or hasattr(part, "__rich_console__"):
                renderable_content.append(part)
            else:
                renderable_content.append(str(part))

        from rich.console import Group

        content_group = Group(*renderable_content)

        return Panel(
            content_group,
            title=panel_title,
            border_style=panel_style,
            box=box.ROUNDED,
            padding=(1, 2),
        )

    def _format_panel_title(self, error: MLError) -> Text:
        """Format panel title with error type and code."""
        title = Text()
        title.append(error.__class__.__name__, style="bold white")
        if error.code:
            title.append(f" [{error.code}]", style="dim white")
        return title

    def _format_source_context(self, context_lines: list[SourceLine], error: MLError) -> Table:
        """Format source code context as a Rich table."""
        table = Table(
            show_header=False,
            show_edge=False,
            pad_edge=False,
            box=None,
            padding=(0, 1, 0, 0),
        )
        table.add_column("marker", width=3, style="bold")
        table.add_column("line_num", width=4, style="dim")
        table.add_column("separator", width=1, style="dim")
        table.add_column("code", overflow="fold")

        for source_line in context_lines:
            marker = ">>>" if source_line.is_primary else "   "
            marker_style = "bold red" if source_line.is_primary else "dim"

            line_num = str(source_line.number)
            line_style = "bold" if source_line.is_primary else "dim"

            # Syntax highlighting for the code
            code_content = source_line.content
            if source_line.is_primary and source_line.highlight_start is not None:
                # Highlight the problematic part
                start = source_line.highlight_start
                end = source_line.highlight_end or start + 1

                code_text = Text()
                code_text.append(code_content[:start])
                code_text.append(code_content[start:end], style="bold red on yellow")
                code_text.append(code_content[end:])
                code_display = code_text
            else:
                # Basic syntax highlighting for ML code
                try:
                    code_display = Syntax(
                        code_content,
                        "python",  # Use Python syntax for now
                        theme="monokai",
                        line_numbers=False,
                        background_color="default",
                    )
                except Exception:
                    code_display = Text(code_content)

            table.add_row(
                Text(marker, style=marker_style),
                Text(line_num, style=line_style),
                Text("|", style="dim"),
                code_display,
            )

            # Add pointer line for primary error line
            if source_line.is_primary and source_line.highlight_start is not None:
                pointer = " " * source_line.highlight_start + "^"
                if (
                    source_line.highlight_end
                    and source_line.highlight_end > source_line.highlight_start + 1
                ):
                    pointer += "~" * (source_line.highlight_end - source_line.highlight_start - 1)

                table.add_row(
                    "",
                    "",
                    "",
                    Text(pointer, style="bold red"),
                )

        return Padding(table, (0, 2))

    def _format_suggestions(self, suggestions: list[str]) -> Panel:
        """Format suggestions as a Rich panel."""
        suggestion_text = Text()
        suggestion_text.append("[SUGGESTIONS] Suggestions:\n\n", style="bold yellow")

        for i, suggestion in enumerate(suggestions, 1):
            suggestion_text.append(f"  {i}. ", style="bold yellow")
            suggestion_text.append(f"{suggestion}\n", style="white")

        return Panel(
            suggestion_text,
            title="How to Fix",
            border_style="yellow",
            box=box.ROUNDED,
            padding=(0, 1),
        )

    def _format_additional_context(self, context: dict[str, Any]) -> Panel:
        """Format additional context as a Rich panel."""
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("key", style="bold cyan")
        table.add_column("separator", width=2)
        table.add_column("value", style="white")

        for key, value in context.items():
            table.add_row(
                key.replace("_", " ").title(),
                ":",
                str(value),
            )

        return Panel(
            table,
            title="Additional Context",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(0, 1),
        )

    def _get_severity_style(self, severity: ErrorSeverity) -> str:
        """Get Rich style for error severity."""
        styles = {
            ErrorSeverity.CRITICAL: "bold red",
            ErrorSeverity.HIGH: "red",
            ErrorSeverity.MEDIUM: "yellow",
            ErrorSeverity.LOW: "blue",
            ErrorSeverity.INFO: "green",
        }
        return styles.get(severity, "white")

    def _get_panel_style(self, severity: ErrorSeverity) -> str:
        """Get Rich panel border style for error severity."""
        styles = {
            ErrorSeverity.CRITICAL: "bold red",
            ErrorSeverity.HIGH: "red",
            ErrorSeverity.MEDIUM: "yellow",
            ErrorSeverity.LOW: "blue",
            ErrorSeverity.INFO: "green",
        }
        return styles.get(severity, "white")

    def print_error(self, error_context: ErrorContext) -> None:
        """Print formatted error to console.

        Args:
            error_context: ErrorContext to print
        """
        formatted_error = self.format_error(error_context)
        self.console.print(formatted_error)

    def format_multiple_errors(self, error_contexts: list[ErrorContext]) -> Panel:
        """Format multiple errors in a single panel.

        Args:
            error_contexts: List of ErrorContext instances

        Returns:
            Rich Panel with all formatted errors
        """
        if not error_contexts:
            return Panel("No errors to display", style="green")

        if len(error_contexts) == 1:
            return self.format_error(error_contexts[0])

        # Group by severity
        by_severity = {}
        for ctx in error_contexts:
            severity = ctx.error.severity
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(ctx)

        # Create summary
        summary_table = Table(show_header=True, box=box.SIMPLE)
        summary_table.add_column("Severity", style="bold")
        summary_table.add_column("Count", justify="right", style="bold")
        summary_table.add_column("Icon", justify="center")

        total_errors = len(error_contexts)
        for severity in ErrorSeverity:
            count = len(by_severity.get(severity, []))
            if count > 0:
                icon = error_contexts[0].get_severity_icon() if error_contexts else ""
                # Get the right icon for each severity
                for ctx in error_contexts:
                    if ctx.error.severity == severity:
                        icon = ctx.get_severity_icon()
                        break

                summary_table.add_row(
                    severity.value.title(),
                    str(count),
                    icon,
                )

        content_parts = [
            Text(f"Found {total_errors} error(s):", style="bold white"),
            Text(""),
            summary_table,
            Text(""),
        ]

        # Add individual errors
        for ctx in error_contexts:
            content_parts.append(self.format_error(ctx))
            content_parts.append(Text(""))

        # Convert content parts to renderable format
        renderable_content = []
        for part in content_parts:
            if hasattr(part, "__rich__") or hasattr(part, "__rich_console__"):
                renderable_content.append(part)
            else:
                renderable_content.append(str(part))

        from rich.console import Group

        content_group = Group(*renderable_content)

        return Panel(
            content_group,
            title="Error Report",
            border_style="red",
            box=box.ROUNDED,
            padding=(1, 2),
        )

    def print_multiple_errors(self, error_contexts: list[ErrorContext]) -> None:
        """Print multiple formatted errors to console.

        Args:
            error_contexts: List of ErrorContext instances
        """
        formatted_errors = self.format_multiple_errors(error_contexts)
        self.console.print(formatted_errors)


# Global formatter instance
error_formatter = MLErrorFormatter()


def format_error(error_context: ErrorContext) -> Panel:
    """Format an error context using the global formatter.

    Args:
        error_context: ErrorContext to format

    Returns:
        Rich Panel with formatted error
    """
    return error_formatter.format_error(error_context)


def print_error(error_context: ErrorContext) -> None:
    """Print a formatted error using the global formatter.

    Args:
        error_context: ErrorContext to print
    """
    error_formatter.print_error(error_context)


def print_multiple_errors(error_contexts: list[ErrorContext]) -> None:
    """Print multiple formatted errors using the global formatter.

    Args:
        error_contexts: List of ErrorContext instances
    """
    error_formatter.print_multiple_errors(error_contexts)
