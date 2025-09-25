"""Rich error context with source line display and suggestions."""

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .exceptions import ErrorSeverity, MLError


class TerminalColors:
    """Terminal color codes with support detection."""

    # ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"

    # Bright colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    @classmethod
    def supports_color(cls) -> bool:
        """Check if terminal supports color output."""
        # Check if we're in a TTY and have color support
        if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
            return False

        # Check environment variables
        if os.environ.get("NO_COLOR"):
            return False

        if os.environ.get("FORCE_COLOR"):
            return True

        # Check TERM variable
        term = os.environ.get("TERM", "").lower()
        return "color" in term or term in ("xterm", "xterm-256color", "screen", "tmux")

    @classmethod
    def colorize(cls, text: str, color: str, bold: bool = False) -> str:
        """Apply color to text if terminal supports it."""
        if not cls.supports_color():
            return text

        prefix = cls.BOLD + color if bold else color
        return f"{prefix}{text}{cls.RESET}"

    @classmethod
    def get_severity_color(cls, severity: ErrorSeverity) -> str:
        """Get color code for error severity."""
        color_map = {
            ErrorSeverity.CRITICAL: cls.BRIGHT_RED,
            ErrorSeverity.HIGH: cls.RED,
            ErrorSeverity.MEDIUM: cls.YELLOW,
            ErrorSeverity.LOW: cls.BLUE,
            ErrorSeverity.INFO: cls.CYAN,
        }
        return color_map.get(severity, cls.WHITE)


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

    def get_severity_icon(self, use_unicode: bool = True) -> str:
        """Get icon for error severity with Unicode/ASCII fallback.

        Args:
            use_unicode: If True, use emoji/Unicode icons; if False, use ASCII
        """
        if use_unicode:
            icons = {
                ErrorSeverity.CRITICAL: "🚨",
                ErrorSeverity.HIGH: "❌",
                ErrorSeverity.MEDIUM: "⚠️",
                ErrorSeverity.LOW: "ℹ️",
                ErrorSeverity.INFO: "💡",
            }
        else:
            icons = {
                ErrorSeverity.CRITICAL: "[!]",
                ErrorSeverity.HIGH: "[X]",
                ErrorSeverity.MEDIUM: "[!]",
                ErrorSeverity.LOW: "[i]",
                ErrorSeverity.INFO: "[*]",
            }
        return icons.get(self.error.severity, "[?]" if not use_unicode else "❓")

    def get_cwe_info(self) -> dict[str, Any] | None:
        """Get CWE information if available."""
        if not self.error.cwe:
            return None

        return {
            "id": self.error.cwe.value,
            "name": self.error.cwe.name,
            "url": f"https://cwe.mitre.org/data/definitions/{self.error.cwe.value}.html",
        }

    def format_rich_text(self, use_colors: bool = True, use_unicode: bool = True) -> str:
        """Format error context with rich terminal formatting.

        Args:
            use_colors: Enable terminal color output
            use_unicode: Use Unicode/emoji icons
        """
        lines = []
        colors = TerminalColors()
        use_colors = use_colors and colors.supports_color()

        # Get severity color
        severity_color = colors.get_severity_color(self.error.severity)

        # Header with icon and severity
        icon = self.get_severity_icon(use_unicode)
        severity_text = self.error.severity.value.upper()

        if use_colors:
            header = f"{colors.colorize(icon, severity_color, bold=True)} {colors.colorize(severity_text, severity_color, bold=True)}"
        else:
            header = f"{icon} {severity_text}"

        # Add error code if available
        if self.error.code:
            code_text = f"[{self.error.code}]"
            header += " " + (colors.colorize(code_text, colors.DIM) if use_colors else code_text)

        # Add location if available
        location = self.get_location()
        if location:
            loc_text = f" at {location}"
            header += colors.colorize(loc_text, colors.GRAY) if use_colors else loc_text

        lines.append(header)

        # Separator line
        separator = "─" * 50 if use_unicode else "=" * 50
        lines.append(colors.colorize(separator, colors.GRAY) if use_colors else separator)
        lines.append("")

        # Error message (main content)
        message = self.error.message
        if use_colors:
            message = colors.colorize(message, colors.WHITE, bold=True)
        lines.append(message)
        lines.append("")

        # CWE information for security errors
        cwe_info = self.get_cwe_info()
        if cwe_info:
            security_icon = "🔒" if use_unicode else "[SEC]"
            sec_header = f"{security_icon} Security Issue: CWE-{cwe_info['id']}"

            if use_colors:
                sec_header = colors.colorize(sec_header, colors.BRIGHT_RED, bold=True)

            lines.append(sec_header)

            cwe_desc = f"   {cwe_info['name']}"
            if use_colors:
                cwe_desc = colors.colorize(cwe_desc, colors.RED)
            lines.append(cwe_desc)

            ref_text = f"   Reference: {cwe_info['url']}"
            if use_colors:
                ref_text = colors.colorize(ref_text, colors.BLUE, bold=False)
            lines.append(ref_text)
            lines.append("")

        # Source code context with enhanced highlighting
        context_lines = self.get_context_lines()
        if context_lines:
            src_header = f"{'📍' if use_unicode else '>>>'} Source Context:"
            if use_colors:
                src_header = colors.colorize(src_header, colors.CYAN, bold=True)

            lines.append(src_header)
            lines.append("")

            for source_line in context_lines:
                # Line number with proper padding
                line_num = f"{source_line.number:4d}"

                if source_line.is_primary:
                    # Primary error line - highlighted
                    prefix = "►" if use_unicode else ">"
                    content = self._format_source_line_content(source_line, use_colors, use_unicode)

                    if use_colors:
                        line_display = f"{colors.colorize(prefix, colors.BRIGHT_RED, bold=True)} {colors.colorize(line_num, colors.BRIGHT_RED)} │ {content}"
                    else:
                        line_display = f"{prefix} {line_num} | {content}"

                    lines.append(line_display)

                    # Add enhanced error pointer
                    if source_line.highlight_start is not None:
                        self._add_error_pointer(lines, source_line, use_colors, use_unicode, colors)

                else:
                    # Context line - dimmed
                    prefix = " "
                    content = source_line.content

                    if use_colors:
                        line_display = f"{prefix} {colors.colorize(line_num, colors.GRAY)} │ {colors.colorize(content, colors.GRAY)}"
                    else:
                        line_display = f"  {line_num} | {content}"

                    lines.append(line_display)

            lines.append("")

        # Suggestions section
        if self.error.suggestions:
            sugg_header = f"{'💡' if use_unicode else '[?]'} Suggestions:"
            if use_colors:
                sugg_header = colors.colorize(sugg_header, colors.BRIGHT_YELLOW, bold=True)

            lines.append(sugg_header)
            for i, suggestion in enumerate(self.error.suggestions, 1):
                bullet = f"{i}." if len(self.error.suggestions) > 1 else "•"
                sugg_line = f"   {bullet} {suggestion}"

                if use_colors:
                    sugg_line = colors.colorize(sugg_line, colors.YELLOW)

                lines.append(sugg_line)
            lines.append("")

        # Additional context information
        if self.error.context:
            ctx_header = f"{'🔍' if use_unicode else '[*]'} Additional Context:"
            if use_colors:
                ctx_header = colors.colorize(ctx_header, colors.BRIGHT_BLUE, bold=True)

            lines.append(ctx_header)
            for key, value in self.error.context.items():
                ctx_line = f"   {key}: {value}"
                if use_colors:
                    ctx_line = colors.colorize(ctx_line, colors.BLUE)
                lines.append(ctx_line)

        return "\n".join(lines)

    def format_plain_text(self) -> str:
        """Format error context as plain text (legacy method)."""
        return self.format_rich_text(use_colors=False, use_unicode=False)

    def _format_source_line_content(
        self, source_line: SourceLine, use_colors: bool, use_unicode: bool
    ) -> str:
        """Format source line content with enhanced highlighting."""
        content = source_line.content
        if not source_line.is_primary or source_line.highlight_start is None:
            return content

        colors = TerminalColors()
        start = max(0, source_line.highlight_start)
        end = min(len(content), source_line.highlight_end or len(content))

        if use_colors:
            # Split content into parts for highlighting
            before = content[:start]
            highlighted = content[start:end]
            after = content[end:]

            # Apply bright red background to highlighted section
            if highlighted:
                highlighted = colors.colorize(highlighted, colors.BRIGHT_RED, bold=True)

            return before + highlighted + after
        else:
            # Use bracket highlighting for plain text
            return content[:start] + f"[{content[start:end]}]" + content[end:]

    def _add_error_pointer(
        self,
        lines: list[str],
        source_line: SourceLine,
        use_colors: bool,
        use_unicode: bool,
        colors: TerminalColors,
    ) -> None:
        """Add enhanced error pointer below source line."""
        if source_line.highlight_start is None:
            return

        # Create pointer line with proper indentation
        indent = "       │ "  # Match line number format
        spaces = " " * source_line.highlight_start

        # Choose pointer characters
        if use_unicode:
            pointer_char = "▲"
            extend_char = "─"
        else:
            pointer_char = "^"
            extend_char = "~"

        # Build pointer
        pointer = pointer_char
        if (
            source_line.highlight_end
            and source_line.highlight_end > source_line.highlight_start + 1
        ):
            length = source_line.highlight_end - source_line.highlight_start - 1
            pointer += extend_char * length

        pointer_line = indent + spaces + pointer

        if use_colors:
            pointer_line = colors.colorize(pointer_line, colors.BRIGHT_RED, bold=True)

        lines.append(pointer_line)

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
