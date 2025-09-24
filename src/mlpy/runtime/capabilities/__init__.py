"""Capability-based security system for mlpy v2.0.

This module implements a production-ready capability system that provides:
- Fine-grained access control through capability tokens
- Thread-safe context management with inheritance
- Performance-optimized capability validation
- Integration with ML language constructs

The capability system is designed with a zero-trust security model where
all system access must go through capability validation.
"""

from .context import CapabilityContext
from .decorators import requires_capability, with_capability
from .exceptions import (
    CapabilityError,
    CapabilityExpiredError,
    CapabilityNotFoundError,
    CapabilityValidationError,
    InsufficientCapabilityError,
)
from .manager import CapabilityManager, get_capability_manager
from .tokens import CapabilityToken, create_capability_token

__all__ = [
    # Core classes
    "CapabilityToken",
    "CapabilityManager",
    "CapabilityContext",
    # Factory functions
    "create_capability_token",
    "get_capability_manager",
    # Decorators
    "requires_capability",
    "with_capability",
    # Exceptions
    "CapabilityError",
    "CapabilityNotFoundError",
    "CapabilityExpiredError",
    "CapabilityValidationError",
    "InsufficientCapabilityError",
]
