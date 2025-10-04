"""ML Console Standard Library Module."""

import sys
from typing import Any
from mlpy.stdlib.decorators import ml_module, ml_function


@ml_module(
    name="console",
    description="Console output and logging functionality",
    capabilities=["console.write", "console.error"],
    version="1.0.0"
)
class Console:
    """ML console object providing logging and output functionality."""

    @ml_function(
        description="Log messages to stdout",
        capabilities=["console.write"]
    )
    def log(self, *args: Any) -> None:
        """Log messages to stdout."""
        print(*args)

    @ml_function(
        description="Log error messages to stderr",
        capabilities=["console.error"]
    )
    def error(self, *args: Any) -> None:
        """Log error messages to stderr."""
        print(*args, file=sys.stderr)

    @ml_function(
        description="Log warning messages to stderr",
        capabilities=["console.error"]
    )
    def warn(self, *args: Any) -> None:
        """Log warning messages to stderr."""
        print("WARNING:", *args, file=sys.stderr)

    @ml_function(
        description="Log info messages to stdout",
        capabilities=["console.write"]
    )
    def info(self, *args: Any) -> None:
        """Log info messages to stdout."""
        print("INFO:", *args)

    @ml_function(
        description="Log debug messages to stdout",
        capabilities=["console.write"]
    )
    def debug(self, *args: Any) -> None:
        """Log debug messages to stdout."""
        print("DEBUG:", *args)


# Global console instance for ML programs
console = Console()
