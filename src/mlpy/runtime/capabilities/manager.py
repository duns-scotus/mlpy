"""Capability manager for global capability system coordination."""

import threading
import time
import weakref
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from .context import CapabilityContext, get_current_context, set_current_context
from .exceptions import CapabilityContextError, CapabilityNotFoundError
from .tokens import CapabilityToken


class CapabilityManager:
    """Global capability system manager with performance optimization."""

    def __init__(self) -> None:
        """Initialize the capability manager."""
        self._contexts: dict[str, weakref.ReferenceType] = {}
        self._context_cache: dict[str, CapabilityContext] = {}
        self._global_lock = threading.RLock()

        # Performance optimization
        self._validation_cache: dict[str, tuple] = {}  # (result, timestamp)
        self._cache_ttl = 5.0  # 5 second cache TTL
        self._cache_lock = threading.RLock()

        # Statistics
        self._stats = {
            "contexts_created": 0,
            "contexts_destroyed": 0,
            "capability_checks": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }

    def create_context(
        self, name: str = "", parent: CapabilityContext | None = None
    ) -> CapabilityContext:
        """Create a new capability context."""
        with self._global_lock:
            context = CapabilityContext(name=name, parent_context=parent)

            # Register context with weak reference
            self._contexts[context.context_id] = weakref.ref(context, self._cleanup_context)

            # Update statistics
            self._stats["contexts_created"] += 1

            return context

    def get_context(self, context_id: str) -> CapabilityContext | None:
        """Get a context by ID."""
        with self._global_lock:
            ref = self._contexts.get(context_id)
            if ref:
                context = ref()
                if context:
                    return context
                else:
                    # Context was garbage collected
                    del self._contexts[context_id]

            return None

    def _cleanup_context(self, ref: weakref.ReferenceType) -> None:
        """Cleanup callback for garbage collected contexts."""
        with self._global_lock:
            # Find and remove the context reference
            to_remove = []
            for context_id, context_ref in self._contexts.items():
                if context_ref is ref:
                    to_remove.append(context_id)

            for context_id in to_remove:
                del self._contexts[context_id]

            self._stats["contexts_destroyed"] += 1

    def has_capability(
        self, capability_type: str, resource_path: str = "", operation: str = ""
    ) -> bool:
        """Check if current context has capability for resource access."""
        context = get_current_context()
        if not context:
            return False

        # Build cache key
        cache_key = f"{context.context_id}:{capability_type}:{resource_path}:{operation}"

        # Check cache first
        with self._cache_lock:
            if cache_key in self._validation_cache:
                result, timestamp = self._validation_cache[cache_key]
                if time.time() - timestamp < self._cache_ttl:
                    self._stats["cache_hits"] += 1
                    return result

            self._stats["cache_misses"] += 1

        # Perform actual capability check
        try:
            if resource_path and operation:
                result = context.can_access_resource(capability_type, resource_path, operation)
            else:
                result = context.has_capability(capability_type)

            # Cache the result
            with self._cache_lock:
                self._validation_cache[cache_key] = (result, time.time())

            self._stats["capability_checks"] += 1
            return result

        except CapabilityNotFoundError:
            # Cache negative result
            with self._cache_lock:
                self._validation_cache[cache_key] = (False, time.time())

            return False

    def use_capability(self, capability_type: str, resource_path: str, operation: str) -> None:
        """Use a capability for resource access."""
        context = get_current_context()
        if not context:
            raise CapabilityNotFoundError(capability_type)

        context.use_capability(capability_type, resource_path, operation)

        # Invalidate cache for this capability type
        self._invalidate_cache_for_capability(context.context_id, capability_type)

    def add_capability_to_current_context(self, token: CapabilityToken) -> None:
        """Add a capability token to the current context."""
        context = get_current_context()
        if not context:
            raise CapabilityContextError("No current capability context")

        context.add_capability(token)

        # Invalidate cache for this capability type
        self._invalidate_cache_for_capability(context.context_id, token.capability_type)

    def _invalidate_cache_for_capability(self, context_id: str, capability_type: str) -> None:
        """Invalidate cache entries for a specific capability type."""
        with self._cache_lock:
            keys_to_remove = [
                key
                for key in self._validation_cache.keys()
                if key.startswith(f"{context_id}:{capability_type}:")
            ]

            for key in keys_to_remove:
                del self._validation_cache[key]

    def clear_cache(self) -> None:
        """Clear the validation cache."""
        with self._cache_lock:
            self._validation_cache.clear()

    def cleanup_expired_tokens(self) -> int:
        """Clean up expired tokens from all contexts."""
        total_removed = 0

        with self._global_lock:
            for context_ref in list(self._contexts.values()):
                context = context_ref()
                if context:
                    total_removed += context.cleanup_expired_tokens()

        # Clear cache after cleanup
        self.clear_cache()

        return total_removed

    def get_statistics(self) -> dict[str, Any]:
        """Get capability system statistics."""
        with self._global_lock, self._cache_lock:
            return {
                **self._stats,
                "active_contexts": len(self._contexts),
                "cache_entries": len(self._validation_cache),
                "cache_hit_rate": (
                    self._stats["cache_hits"]
                    / (self._stats["cache_hits"] + self._stats["cache_misses"])
                    if (self._stats["cache_hits"] + self._stats["cache_misses"]) > 0
                    else 0.0
                ),
            }

    @contextmanager
    def capability_context(
        self, name: str = "", capabilities: list[CapabilityToken] | None = None
    ) -> Generator[CapabilityContext, None, None]:
        """Create a managed capability context."""
        # Get current context as parent
        parent_context = get_current_context()

        # Create new context
        context = self.create_context(name=name, parent=parent_context)

        # Add provided capabilities
        if capabilities:
            for token in capabilities:
                context.add_capability(token)

        # Set as current context
        previous_context = get_current_context()
        set_current_context(context)

        try:
            yield context
        finally:
            # Restore previous context
            set_current_context(previous_context)

            # Cleanup expired tokens
            context.cleanup_expired_tokens()

    def create_file_capability_context(
        self, patterns: list[str], operations: set[str] | None = None
    ) -> Generator[CapabilityContext, None, None]:
        """Create a context with file access capabilities."""
        from .tokens import create_file_capability

        token = create_file_capability(
            patterns=patterns, operations=operations or {"read", "write"}
        )

        return self.capability_context(
            name=f"file_access_{len(patterns)}_patterns", capabilities=[token]
        )

    def create_network_capability_context(
        self, hosts: list[str], ports: list[int] | None = None
    ) -> Generator[CapabilityContext, None, None]:
        """Create a context with network access capabilities."""
        from .tokens import create_network_capability

        token = create_network_capability(hosts=hosts, ports=ports or [80, 443])

        return self.capability_context(
            name=f"network_access_{len(hosts)}_hosts", capabilities=[token]
        )

    def get_debug_info(self) -> dict[str, Any]:
        """Get detailed debug information about the capability system."""
        with self._global_lock:
            contexts_info = []

            for context_id, context_ref in self._contexts.items():
                context = context_ref()
                if context:
                    contexts_info.append(context.to_dict())

            return {
                "statistics": self.get_statistics(),
                "contexts": contexts_info,
                "current_context": (
                    get_current_context().to_dict() if get_current_context() else None
                ),
            }


# Global capability manager instance
_global_manager: CapabilityManager | None = None
_manager_lock = threading.Lock()


def get_capability_manager() -> CapabilityManager:
    """Get the global capability manager instance."""
    global _global_manager

    if _global_manager is None:
        with _manager_lock:
            if _global_manager is None:
                _global_manager = CapabilityManager()

    return _global_manager


def reset_capability_manager() -> None:
    """Reset the global capability manager (for testing)."""
    global _global_manager
    with _manager_lock:
        _global_manager = None


# Convenience functions using global manager
def has_capability(capability_type: str, resource_path: str = "", operation: str = "") -> bool:
    """Check if current context has capability."""
    return get_capability_manager().has_capability(capability_type, resource_path, operation)


def use_capability(capability_type: str, resource_path: str, operation: str) -> None:
    """Use a capability for resource access."""
    return get_capability_manager().use_capability(capability_type, resource_path, operation)


def add_capability(token: CapabilityToken) -> None:
    """Add capability to current context."""
    return get_capability_manager().add_capability_to_current_context(token)


# Context managers using global manager
def file_capability_context(
    patterns: list[str], operations: set[str] | None = None
) -> Generator[CapabilityContext, None, None]:
    """Create file access capability context."""
    return get_capability_manager().create_file_capability_context(patterns, operations)


def network_capability_context(
    hosts: list[str], ports: list[int] | None = None
) -> Generator[CapabilityContext, None, None]:
    """Create network access capability context."""
    return get_capability_manager().create_network_capability_context(hosts, ports)
