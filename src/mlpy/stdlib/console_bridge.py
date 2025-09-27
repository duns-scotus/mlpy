"""ML Console Standard Library Module."""

import sys
from typing import Any


class Console:
    """ML console object providing logging and output functionality."""

    @staticmethod
    def log(*args: Any) -> None:
        """Log messages to stdout."""
        print(*args)

    @staticmethod
    def error(*args: Any) -> None:
        """Log error messages to stderr."""
        print(*args, file=sys.stderr)

    @staticmethod
    def warn(*args: Any) -> None:
        """Log warning messages to stderr."""
        print("WARNING:", *args, file=sys.stderr)

    @staticmethod
    def info(*args: Any) -> None:
        """Log info messages to stdout."""
        print("INFO:", *args)

    @staticmethod
    def debug(*args: Any) -> None:
        """Log debug messages to stdout."""
        print("DEBUG:", *args)


# Global console instance for ML programs
console = Console()
