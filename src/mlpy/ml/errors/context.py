"""Rich error context with source line display and suggestions."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .exceptions import ErrorSeverity, MLError


@dataclass
class SourceLocation:
    """Represents a location in source code."""

    file_path: str
    line_number: int
    column: int
    length: int = 1

    @property
    def end_column(self) -> int:
        """Calculate end column position."""
        return self.column + self.length

    def __str__(self) -> str:
        """String representation of source location."""
        return f"{self.file_path}:{self.line_number}:{self.column}"


@dataclass
class SourceLine:
    """Represents a line of source code with highlighting."""

    number: int
    content: str
    is_primary: bool = False
    highlight_start: int | None = None
    highlight_end: int | None = None

    @property
    def highlighted_content(self) -> str:
        """Get content with highlighting markers."""
        if not self.is_primary or self.highlight_start is None:
            return self.content

        start = max(0, self.highlight_start)
        end = min(len(self.content), self.highlight_end or len(self.content))

        return self.content[:start] + ">>>" + self.content[start:end] + "<<<" + self.content[end:]


class ErrorContext:
    """Rich error context with source code display and suggestions."""

    def __init__(
        self,
        error: MLError,
        source_content: str | None = None,
        context_lines: int = 3,
    ) -> None:
        """Initialize error context.

        Args:
            error: The MLError to provide context for
            source_content: Complete source file content
            context_lines: Number of lines to show before/after error
        """
        self.error = error
        self.source_content = source_content
        self.context_lines = context_lines
        self._source_lines: list[str] | None = None

    @property
    def source_lines(self) -> list[str]:
        """Get source lines, loading from file if needed."""
        if self._source_lines is None:
            if self.source_content:
                self._source_lines = self.source_content.splitlines()
            elif self.error.source_file:
                try:
                    path = Path(self.error.source_file)
                    if path.exists():
                        self._source_lines = path.read_text(encoding="utf-8").splitlines()
                    else:
                        self._source_lines = []
                except Exception:
                    self._source_lines = []
            else:
                self._source_lines = []
        return self._source_lines

    def get_location(self) -> SourceLocation | None:
        """Get source location if available."""
        if (
            self.error.source_file
            and self.error.line_number is not None
            and self.error.column is not None
        ):
            return SourceLocation(
                file_path=self.error.source_file,
                line_number=self.error.line_number,
                column=self.error.column,
            )
        return None

    def get_context_lines(self) -> list[SourceLine]:
        """Get source lines with context around the error."""
        if not self.error.line_number or not self.source_lines:
            return []

        error_line = self.error.line_number - 1  # Convert to 0-based
        start_line = max(0, error_line - self.context_lines)
        end_line = min(len(self.source_lines), error_line + self.context_lines + 1)

        context_lines = []
        for i in range(start_line, end_line):
            is_primary = i == error_line
            highlight_start = None
            highlight_end = None

            if is_primary and self.error.column is not None:
                highlight_start = self.error.column - 1  # Convert to 0-based
                # Try to detect the problematic token
                line_content = self.source_lines[i]
                highlight_end = self._find_token_end(line_content, highlight_start)

            context_lines.append(
                SourceLine(
                    number=i + 1,  # Convert back to 1-based for display
                    content=self.source_lines[i],
                    is_primary=is_primary,
                    highlight_start=highlight_start,
                    highlight_end=highlight_end,
                )
            )

        return context_lines

    def _find_token_end(self, line: str, start: int) -> int:
        """Find the end of the token starting at the given position."""
        if start >= len(line):
            return start

        # If we're on a word character, find the end of the word
        if line[start].isalnum() or line[start] == "_":
            end = start
            while end < len(line) and (line[end].isalnum() or line[end] == "_"):
                end += 1
            return end

        # For operators or punctuation, highlight just the character
        # but check for multi-character operators
        two_char_ops = ["==", "!=", "<=", ">=", "->", "=>", "&&", "||", "++", "--"]
        three_char_ops = ["===", "!==", ">>>", "<<<"]

        # Check three-character operators first
        if start + 2 < len(line):
            three_char = line[start : start + 3]
            if three_char in three_char_ops:
                return start + 3

        # Check two-character operators
        if start + 1 < len(line):
            two_char = line[start : start + 2]
            if two_char in two_char_ops:
                return start + 2

        # Single character
        return start + 1

    def get_severity_icon(self) -> str:
        """Get icon for error severity."""
        icons = {
            ErrorSeverity.CRITICAL: "[!]",
            ErrorSeverity.HIGH: "[X]",
            ErrorSeverity.MEDIUM: "[!]",
            ErrorSeverity.LOW: "[i]",
            ErrorSeverity.INFO: "[*]",
        }
        return icons.get(self.error.severity, "[?]")

    def get_cwe_info(self) -> dict[str, Any] | None:
        """Get CWE information if available."""
        if not self.error.cwe:
            return None

        return {
            "id": self.error.cwe.value,
            "name": self.error.cwe.name,
            "url": f"https://cwe.mitre.org/data/definitions/{self.error.cwe.value}.html",
        }

    def format_plain_text(self) -> str:
        """Format error context as plain text."""
        lines = []

        # Header with severity and location
        header = f"{self.get_severity_icon()} {self.error.severity.value.upper()}"
        if self.error.code:
            header += f" [{self.error.code}]"

        location = self.get_location()
        if location:
            header += f" at {location}"

        lines.append(header)
        lines.append("=" * len(header))
        lines.append("")

        # Error message
        lines.append(self.error.message)
        lines.append("")

        # CWE information
        cwe_info = self.get_cwe_info()
        if cwe_info:
            lines.append(f"Security Issue: CWE-{cwe_info['id']} ({cwe_info['name']})")
            lines.append(f"Reference: {cwe_info['url']}")
            lines.append("")

        # Source code context
        context_lines = self.get_context_lines()
        if context_lines:
            lines.append("Source Context:")
            lines.append("-" * 15)

            for source_line in context_lines:
                prefix = ">>>" if source_line.is_primary else "   "
                line_num = f"{source_line.number:3d}"
                content = source_line.highlighted_content

                lines.append(f"{prefix} {line_num} | {content}")

                # Add pointer for primary line
                if source_line.is_primary and source_line.highlight_start is not None:
                    pointer_line = "       | " + " " * source_line.highlight_start + "^"
                    if (
                        source_line.highlight_end
                        and source_line.highlight_end > source_line.highlight_start + 1
                    ):
                        pointer_line += "~" * (
                            source_line.highlight_end - source_line.highlight_start - 1
                        )
                    lines.append(pointer_line)

            lines.append("")

        # Suggestions
        if self.error.suggestions:
            lines.append("Suggestions:")
            for i, suggestion in enumerate(self.error.suggestions, 1):
                lines.append(f"  {i}. {suggestion}")
            lines.append("")

        # Additional context
        if self.error.context:
            lines.append("Additional Context:")
            for key, value in self.error.context.items():
                lines.append(f"  {key}: {value}")

        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        """Convert error context to dictionary for serialization."""
        location = self.get_location()
        context_lines = self.get_context_lines()

        return {
            "error": self.error.to_dict(),
            "location": (
                {
                    "file_path": location.file_path,
                    "line_number": location.line_number,
                    "column": location.column,
                }
                if location
                else None
            ),
            "context_lines": [
                {
                    "number": line.number,
                    "content": line.content,
                    "is_primary": line.is_primary,
                    "highlighted": line.highlighted_content,
                }
                for line in context_lines
            ],
            "cwe_info": self.get_cwe_info(),
            "severity_icon": self.get_severity_icon(),
        }


def create_error_context(
    error: MLError,
    source_file: str | None = None,
    source_content: str | None = None,
    context_lines: int = 3,
) -> ErrorContext:
    """Create an ErrorContext with optional source file loading.

    Args:
        error: The MLError to create context for
        source_file: Path to source file (overrides error.source_file)
        source_content: Direct source content (overrides file loading)
        context_lines: Number of context lines to show

    Returns:
        ErrorContext with rich error information
    """
    if source_file:
        error.source_file = source_file

    return ErrorContext(
        error=error,
        source_content=source_content,
        context_lines=context_lines,
    )
