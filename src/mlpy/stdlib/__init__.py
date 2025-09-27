"""ML Standard Library - Auto-imported functionality for ML programs."""

# Core console functionality
from .console_bridge import console


# Built-in functions that should be available in ML programs
def getCurrentTime():
    """Get current timestamp as string."""
    import datetime

    return datetime.datetime.now().isoformat()


def processData(data):
    """Process input data (placeholder implementation)."""
    return f"processed_{data}"


# Export all standard library symbols
__all__ = ["console", "getCurrentTime", "processData"]
