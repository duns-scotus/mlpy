"""Capability context management for thread-safe capability inheritance."""

import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Optional

from .exceptions import CapabilityContextError, CapabilityNotFoundError
from .tokens import CapabilityToken


@dataclass
class CapabilityContext:
    """Thread-safe capability context with inheritance support."""

    # Core identity
    context_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""

    # Capability storage
    _tokens: dict[str, CapabilityToken] = field(default_factory=dict, init=False)

    # Context hierarchy
    parent_context: Optional["CapabilityContext"] = None
    child_contexts: list["CapabilityContext"] = field(default_factory=list, init=False)

    # Thread safety
    _lock: threading.RLock = field(default_factory=threading.RLock, init=False)

    # Metadata
    created_at: float = field(default_factory=time.time)
    thread_id: int | None = field(
        default_factory=lambda: threading.current_thread().ident, init=False
    )

    def __post_init__(self) -> None:
        """Initialize context after creation."""
        self.thread_id = threading.current_thread().ident

        # Add to parent's children if parent exists
        if self.parent_context:
            with self.parent_context._lock:
                self.parent_context.child_contexts.append(self)

    def add_capability(self, token: CapabilityToken) -> None:
        """Add a capability token to this context."""
        with self._lock:
            if not token.is_valid():
                raise CapabilityContextError(
                    f"Cannot add invalid token: {token.token_id}", self.context_id
                )

            self._tokens[token.capability_type] = token

    def remove_capability(self, capability_type: str) -> bool:
        """Remove a capability from this context."""
        with self._lock:
            return self._tokens.pop(capability_type, None) is not None

    def has_capability(self, capability_type: str, check_parents: bool = True) -> bool:
        """Check if context has a specific capability type."""
        with self._lock:
            # Check local capabilities
            if capability_type in self._tokens:
                token = self._tokens[capability_type]
                if token.is_valid():
                    return True
                else:
                    # Remove invalid token
                    del self._tokens[capability_type]

            # Check parent contexts if requested
            if check_parents and self.parent_context:
                return self.parent_context.has_capability(capability_type, check_parents=True)

            return False

    def get_capability(self, capability_type: str, check_parents: bool = True) -> CapabilityToken:
        """Get a capability token by type."""
        with self._lock:
            # Check local capabilities first
            if capability_type in self._tokens:
                token = self._tokens[capability_type]
                if token.is_valid():
                    return token
                else:
                    # Remove invalid token
                    del self._tokens[capability_type]

            # Check parent contexts
            if check_parents and self.parent_context:
                return self.parent_context.get_capability(capability_type, check_parents=True)

            raise CapabilityNotFoundError(capability_type)

    def get_capability_token(self, capability_type: str) -> CapabilityToken | None:
        """Get a capability token by type, returning None if not found."""
        try:
            return self.get_capability(capability_type)
        except CapabilityNotFoundError:
            return None

    def get_capability_token_unchecked(self, capability_type: str, check_parents: bool = True) -> CapabilityToken | None:
        """Get a capability token without validation or removal.

        This method returns the token even if it's expired or invalid.
        Useful for introspection and debugging.

        Args:
            capability_type: Type of capability to retrieve
            check_parents: Whether to check parent contexts

        Returns:
            The token if found, None otherwise
        """
        with self._lock:
            # Check local capabilities first
            if capability_type in self._tokens:
                return self._tokens[capability_type]

            # Check parent contexts
            if check_parents and self.parent_context:
                return self.parent_context.get_capability_token_unchecked(capability_type, check_parents=True)

            return None

    def can_access_resource(self, capability_type: str, resource_path: str, operation: str) -> bool:
        """Check if context allows access to a specific resource."""
        try:
            token = self.get_capability(capability_type)
            return token.can_access_resource(resource_path, operation)
        except CapabilityNotFoundError:
            return False

    def use_capability(self, capability_type: str, resource_path: str, operation: str) -> None:
        """Use a capability for resource access."""
        token = self.get_capability(capability_type)
        token.use_token(resource_path, operation)

    def get_all_capabilities(self, include_parents: bool = True) -> dict[str, CapabilityToken]:
        """Get all available capabilities in this context."""
        with self._lock:
            capabilities = {}

            # Add parent capabilities first (so local ones override)
            if include_parents and self.parent_context:
                capabilities.update(self.parent_context.get_all_capabilities(include_parents=True))

            # Collect invalid tokens to remove (can't modify dict during iteration)
            invalid_tokens = []

            # Add local capabilities (these take precedence)
            for cap_type, token in self._tokens.items():
                if token.is_valid():
                    capabilities[cap_type] = token
                else:
                    # Mark for cleanup
                    invalid_tokens.append(cap_type)

            # Clean up invalid tokens after iteration
            for cap_type in invalid_tokens:
                del self._tokens[cap_type]

            return capabilities

    def cleanup_expired_tokens(self) -> int:
        """Remove expired tokens and return count of removed tokens."""
        with self._lock:
            expired_tokens = [
                cap_type for cap_type, token in self._tokens.items() if not token.is_valid()
            ]

            for cap_type in expired_tokens:
                del self._tokens[cap_type]

            return len(expired_tokens)

    def create_child_context(self, name: str = "") -> "CapabilityContext":
        """Create a child context that inherits from this context."""
        return CapabilityContext(name=name, parent_context=self)

    def get_context_hierarchy(self) -> list[str]:
        """Get the full context hierarchy as a list of context names."""
        hierarchy = []
        current: CapabilityContext | None = self

        while current:
            hierarchy.append(current.name or current.context_id[:8])
            current = current.parent_context

        return list(reversed(hierarchy))

    def to_dict(self) -> dict[str, Any]:
        """Convert context to dictionary for debugging/serialization."""
        with self._lock:
            return {
                "context_id": self.context_id,
                "name": self.name,
                "thread_id": self.thread_id,
                "capabilities": {
                    cap_type: token.to_dict()
                    for cap_type, token in self._tokens.items()
                    if token.is_valid()
                },
                "parent_context_id": (
                    self.parent_context.context_id if self.parent_context else None
                ),
                "child_context_count": len(self.child_contexts),
                "hierarchy": self.get_context_hierarchy(),
            }

    def __enter__(self) -> "CapabilityContext":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit - cleanup expired tokens."""
        self.cleanup_expired_tokens()

        # Remove from parent's children
        if self.parent_context:
            with self.parent_context._lock:
                try:
                    self.parent_context.child_contexts.remove(self)
                except ValueError:
                    pass  # Already removed

    def __repr__(self) -> str:
        """String representation of context."""
        with self._lock:
            valid_caps = len([t for t in self._tokens.values() if t.is_valid()])
            hierarchy = " -> ".join(self.get_context_hierarchy())

            return (
                f"CapabilityContext("
                f"id={self.context_id[:8]}, "
                f"name='{self.name}', "
                f"capabilities={valid_caps}, "
                f"hierarchy='{hierarchy}'"
                f")"
            )


# Thread-local storage for current capability context
_thread_local = threading.local()


def get_current_context() -> CapabilityContext | None:
    """Get the current capability context for this thread."""
    return getattr(_thread_local, "capability_context", None)


def set_current_context(context: CapabilityContext | None) -> None:
    """Set the current capability context for this thread."""
    _thread_local.capability_context = context


@contextmanager
def capability_context(context: CapabilityContext) -> Any:
    """Context manager for temporarily setting a capability context."""
    previous_context = get_current_context()
    set_current_context(context)

    try:
        yield context
    finally:
        set_current_context(previous_context)


@contextmanager
def isolated_capability_context(name: str = "isolated") -> Any:
    """Create an isolated capability context with no parent inheritance."""
    context = CapabilityContext(name=name)

    with capability_context(context):
        yield context
