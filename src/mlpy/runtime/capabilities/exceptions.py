"""Exception classes for the capability system."""

from typing import Any


class CapabilityError(Exception):
    """Base exception for all capability-related errors."""

    def __init__(self, message: str, context: dict[str, Any] | None = None):
        super().__init__(message)
        self.context = context or {}


class CapabilityNotFoundError(CapabilityError):
    """Raised when a required capability is not found in the current context."""

    def __init__(self, capability_type: str, pattern: str | None = None):
        message = f"Required capability '{capability_type}' not found"
        if pattern:
            message += f" for pattern '{pattern}'"

        super().__init__(
            message,
            context={
                "capability_type": capability_type,
                "pattern": pattern,
                "error_code": "CAPABILITY_NOT_FOUND",
            },
        )


class CapabilityExpiredError(CapabilityError):
    """Raised when attempting to use an expired capability token."""

    def __init__(self, capability_type: str, expired_at: str):
        super().__init__(
            f"Capability '{capability_type}' expired at {expired_at}",
            context={
                "capability_type": capability_type,
                "expired_at": expired_at,
                "error_code": "CAPABILITY_EXPIRED",
            },
        )


class CapabilityValidationError(CapabilityError):
    """Raised when capability token validation fails."""

    def __init__(self, reason: str, token_id: str | None = None):
        super().__init__(
            f"Capability validation failed: {reason}",
            context={
                "reason": reason,
                "token_id": token_id,
                "error_code": "CAPABILITY_VALIDATION_FAILED",
            },
        )


class InsufficientCapabilityError(CapabilityError):
    """Raised when current capability doesn't have sufficient permissions."""

    def __init__(self, required_permission: str, current_permission: str):
        super().__init__(
            f"Insufficient capability: required '{required_permission}', "
            f"have '{current_permission}'",
            context={
                "required_permission": required_permission,
                "current_permission": current_permission,
                "error_code": "INSUFFICIENT_CAPABILITY",
            },
        )


class CapabilityContextError(CapabilityError):
    """Raised when there are issues with capability context management."""

    def __init__(self, message: str, context_id: str | None = None):
        super().__init__(
            f"Capability context error: {message}",
            context={"context_id": context_id, "error_code": "CAPABILITY_CONTEXT_ERROR"},
        )
