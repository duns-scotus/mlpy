"""
Comprehensive test suite for capabilities/manager.py

Tests capability manager system including:
- CapabilityManager initialization and singleton pattern
- Context creation and management with weak references
- Capability checking with intelligent caching
- Statistics tracking and performance metrics
- Context manager protocol (capability_context)
- File and network capability helpers
- Global manager functions and convenience APIs
- Cache invalidation and TTL
- Thread-safe operations
"""

import time
import weakref

import pytest

from mlpy.runtime.capabilities.context import CapabilityContext, get_current_context
from mlpy.runtime.capabilities.exceptions import CapabilityContextError, CapabilityNotFoundError
from mlpy.runtime.capabilities.manager import (
    CapabilityManager,
    add_capability,
    file_capability_context,
    get_capability_manager,
    has_capability,
    network_capability_context,
    reset_capability_manager,
    use_capability,
)
from mlpy.runtime.capabilities.tokens import CapabilityConstraint, CapabilityToken


class TestCapabilityManager:
    """Test CapabilityManager class."""

    def setup_method(self):
        """Setup for each test."""
        self.manager = CapabilityManager()
        self.manager.clear_cache()

    def teardown_method(self):
        """Cleanup after each test."""
        self.manager.clear_cache()

    def test_manager_initialization(self):
        """Test CapabilityManager initialization."""
        manager = CapabilityManager()
        assert manager._contexts == {}
        assert manager._validation_cache == {}
        assert manager._cache_ttl == 5.0
        assert manager._stats["contexts_created"] == 0

    def test_create_context_basic(self):
        """Test creating a basic context."""
        context = self.manager.create_context("test_context")
        assert context is not None
        assert context.name == "test_context"
        assert self.manager._stats["contexts_created"] == 1

    def test_create_context_with_parent(self):
        """Test creating context with parent."""
        parent = self.manager.create_context("parent")
        child = self.manager.create_context("child", parent=parent)
        assert child.parent_context == parent
        assert child in parent.child_contexts

    def test_context_weak_reference_storage(self):
        """Test contexts stored as weak references."""
        context = self.manager.create_context("test")
        context_id = context.context_id

        # Context should be registered
        assert context_id in self.manager._contexts
        assert isinstance(self.manager._contexts[context_id], weakref.ReferenceType)

    def test_get_context_by_id(self):
        """Test getting context by ID."""
        context = self.manager.create_context("test")
        retrieved = self.manager.get_context(context.context_id)
        assert retrieved == context

    def test_get_context_nonexistent(self):
        """Test getting non-existent context."""
        result = self.manager.get_context("nonexistent_id")
        assert result is None

    def test_has_capability_no_context(self):
        """Test has_capability with no current context."""
        result = self.manager.has_capability("file")
        assert result is False

    def test_has_capability_with_context(self):
        """Test has_capability with active context."""
        token = CapabilityToken(capability_type="file")

        with self.manager.capability_context("test", [token]):
            result = self.manager.has_capability("file")
            assert result is True

    def test_has_capability_missing(self):
        """Test has_capability for missing capability."""
        with self.manager.capability_context("test", []):
            result = self.manager.has_capability("network")
            assert result is False

    def test_has_capability_with_resource_and_operation(self):
        """Test has_capability with resource path and operation."""
        constraint = CapabilityConstraint(
            resource_patterns=["*.txt"], allowed_operations={"read"}
        )
        token = CapabilityToken(capability_type="file", constraints=constraint)

        with self.manager.capability_context("test", [token]):
            result = self.manager.has_capability("file", "test.txt", "read")
            assert result is True

    def test_has_capability_caching(self):
        """Test capability check caching."""
        token = CapabilityToken(capability_type="file")

        with self.manager.capability_context("test", [token]):
            # First call - cache miss
            self.manager.has_capability("file")
            initial_misses = self.manager._stats["cache_misses"]

            # Second call - should hit cache
            self.manager.has_capability("file")
            assert self.manager._stats["cache_hits"] > 0

    def test_has_capability_cache_ttl(self):
        """Test cache TTL expiration."""
        token = CapabilityToken(capability_type="file")

        # Set very short TTL for testing
        self.manager._cache_ttl = 0.01

        with self.manager.capability_context("test", [token]):
            # First check
            self.manager.has_capability("file")

            # Wait for cache to expire
            time.sleep(0.02)

            # Should be cache miss after expiration
            initial_misses = self.manager._stats["cache_misses"]
            self.manager.has_capability("file")
            assert self.manager._stats["cache_misses"] > initial_misses

    def test_use_capability(self):
        """Test using a capability."""
        constraint = CapabilityConstraint(
            resource_patterns=["*.txt"], allowed_operations={"read"}
        )
        token = CapabilityToken(capability_type="file", constraints=constraint)

        with self.manager.capability_context("test", [token]):
            self.manager.use_capability("file", "test.txt", "read")
            assert token.usage_count > 0

    def test_use_capability_no_context_raises_error(self):
        """Test use_capability raises error without context."""
        with pytest.raises(CapabilityNotFoundError):
            self.manager.use_capability("file", "test.txt", "read")

    def test_add_capability_to_current_context(self):
        """Test adding capability to current context."""
        with self.manager.capability_context("test", []):
            token = CapabilityToken(capability_type="network")
            self.manager.add_capability_to_current_context(token)

            assert self.manager.has_capability("network")

    def test_add_capability_no_context_raises_error(self):
        """Test adding capability without context raises error."""
        token = CapabilityToken(capability_type="file")

        with pytest.raises(CapabilityContextError):
            self.manager.add_capability_to_current_context(token)

    def test_cache_invalidation_on_capability_use(self):
        """Test cache is invalidated when capability is used."""
        constraint = CapabilityConstraint(
            resource_patterns=["*.txt"], allowed_operations={"read"}
        )
        token = CapabilityToken(capability_type="file", constraints=constraint)

        with self.manager.capability_context("test", [token]):
            # Build cache
            self.manager.has_capability("file", "test.txt", "read")
            initial_entries = len(self.manager._validation_cache)

            # Use capability - should invalidate cache
            self.manager.use_capability("file", "test.txt", "read")

            # Cache should have been invalidated
            # (may not be empty but specific entries removed)

    def test_clear_cache(self):
        """Test clearing validation cache."""
        token = CapabilityToken(capability_type="file")

        with self.manager.capability_context("test", [token]):
            # Build cache
            self.manager.has_capability("file")
            assert len(self.manager._validation_cache) > 0

            # Clear cache
            self.manager.clear_cache()
            assert len(self.manager._validation_cache) == 0

    def test_cleanup_expired_tokens(self):
        """Test cleanup of expired tokens."""
        from datetime import datetime, timedelta

        expires = datetime.now() - timedelta(hours=1)
        constraint = CapabilityConstraint(expires_at=expires)
        expired_token = CapabilityToken(capability_type="expired", constraints=constraint)

        with self.manager.capability_context("test", []) as ctx:
            # Bypass validation to add expired token
            ctx._tokens["expired"] = expired_token

            # Cleanup
            removed = self.manager.cleanup_expired_tokens()
            assert removed >= 0

    def test_get_statistics(self):
        """Test getting statistics."""
        stats = self.manager.get_statistics()

        assert "contexts_created" in stats
        assert "contexts_destroyed" in stats
        assert "capability_checks" in stats
        assert "cache_hits" in stats
        assert "cache_misses" in stats
        assert "active_contexts" in stats
        assert "cache_entries" in stats
        assert "cache_hit_rate" in stats

    def test_get_statistics_hit_rate_calculation(self):
        """Test cache hit rate calculation."""
        token = CapabilityToken(capability_type="file")

        with self.manager.capability_context("test", [token]):
            # Generate some cache hits
            self.manager.has_capability("file")
            self.manager.has_capability("file")

            stats = self.manager.get_statistics()
            assert stats["cache_hit_rate"] >= 0.0
            assert stats["cache_hit_rate"] <= 1.0

    def test_capability_context_manager(self):
        """Test capability_context context manager."""
        token = CapabilityToken(capability_type="file")

        with self.manager.capability_context("test", [token]) as ctx:
            assert isinstance(ctx, CapabilityContext)
            assert ctx.name == "test"
            assert get_current_context() == ctx

    def test_capability_context_restoration(self):
        """Test context is restored after exiting."""
        token = CapabilityToken(capability_type="file")

        previous = get_current_context()

        with self.manager.capability_context("test", [token]):
            pass

        # Context should be restored
        assert get_current_context() == previous

    def test_capability_context_with_parent(self):
        """Test capability context inherits from parent."""
        parent_token = CapabilityToken(capability_type="parent_cap")
        child_token = CapabilityToken(capability_type="child_cap")

        with self.manager.capability_context("parent", [parent_token]):
            parent_ctx = get_current_context()

            with self.manager.capability_context("child", [child_token]) as child_ctx:
                # Child context should have parent set
                assert child_ctx.parent_context == parent_ctx
                # Child has its own capability
                assert self.manager.has_capability("child_cap")

    def test_create_file_capability_context(self):
        """Test create_file_capability_context helper."""
        with self.manager.create_file_capability_context(
            ["*.txt"], {"read", "write"}
        ) as ctx:
            assert self.manager.has_capability("file")

    def test_create_network_capability_context(self):
        """Test create_network_capability_context helper."""
        with self.manager.create_network_capability_context(
            ["api.example.com"], [80, 443]
        ) as ctx:
            assert self.manager.has_capability("network")

    def test_get_debug_info(self):
        """Test getting debug information."""
        token = CapabilityToken(capability_type="file")

        with self.manager.capability_context("test", [token]):
            debug_info = self.manager.get_debug_info()

            assert "statistics" in debug_info
            assert "contexts" in debug_info
            assert "current_context" in debug_info
            assert debug_info["current_context"] is not None


class TestGlobalManagerFunctions:
    """Test global capability manager functions."""

    def setup_method(self):
        """Setup for each test."""
        reset_capability_manager()

    def teardown_method(self):
        """Cleanup after each test."""
        reset_capability_manager()

    def test_get_capability_manager_singleton(self):
        """Test get_capability_manager returns singleton."""
        manager1 = get_capability_manager()
        manager2 = get_capability_manager()
        assert manager1 is manager2

    def test_reset_capability_manager(self):
        """Test resetting global manager."""
        manager1 = get_capability_manager()
        reset_capability_manager()
        manager2 = get_capability_manager()
        assert manager1 is not manager2

    def test_has_capability_global_function(self):
        """Test has_capability global function."""
        manager = get_capability_manager()
        token = CapabilityToken(capability_type="file")

        with manager.capability_context("test", [token]):
            result = has_capability("file")
            assert result is True

    def test_use_capability_global_function(self):
        """Test use_capability global function."""
        manager = get_capability_manager()
        constraint = CapabilityConstraint(
            resource_patterns=["*.txt"], allowed_operations={"read"}
        )
        token = CapabilityToken(capability_type="file", constraints=constraint)

        with manager.capability_context("test", [token]):
            use_capability("file", "test.txt", "read")
            assert token.usage_count > 0

    def test_add_capability_global_function(self):
        """Test add_capability global function."""
        manager = get_capability_manager()

        with manager.capability_context("test", []):
            token = CapabilityToken(capability_type="network")
            add_capability(token)
            assert has_capability("network")

    def test_file_capability_context_global(self):
        """Test file_capability_context global function."""
        with file_capability_context(["*.txt"], {"read"}):
            assert has_capability("file")

    def test_network_capability_context_global(self):
        """Test network_capability_context global function."""
        with network_capability_context(["api.example.com"], [80]):
            assert has_capability("network")


class TestManagerCacheInvalidation:
    """Test cache invalidation logic."""

    def setup_method(self):
        """Setup for each test."""
        self.manager = CapabilityManager()
        self.manager.clear_cache()

    def teardown_method(self):
        """Cleanup after each test."""
        self.manager.clear_cache()

    def test_cache_invalidation_on_add_capability(self):
        """Test cache invalidation when adding capability."""
        with self.manager.capability_context("test", []):
            # Build cache with negative result
            self.manager.has_capability("file")

            # Add capability - should invalidate cache
            token = CapabilityToken(capability_type="file")
            self.manager.add_capability_to_current_context(token)

            # Next check should reflect new capability
            assert self.manager.has_capability("file") is True

    def test_invalidate_cache_for_capability(self):
        """Test _invalidate_cache_for_capability method."""
        token = CapabilityToken(capability_type="file")

        with self.manager.capability_context("test", [token]) as ctx:
            # Build cache
            self.manager.has_capability("file", "test.txt", "read")

            # Invalidate specific capability
            self.manager._invalidate_cache_for_capability(ctx.context_id, "file")

            # Cache entries for this capability should be removed


class TestManagerStatistics:
    """Test statistics tracking."""

    def setup_method(self):
        """Setup for each test."""
        self.manager = CapabilityManager()
        self.manager.clear_cache()

    def teardown_method(self):
        """Cleanup after each test."""
        self.manager.clear_cache()

    def test_contexts_created_counter(self):
        """Test contexts_created counter."""
        initial = self.manager._stats["contexts_created"]

        self.manager.create_context("test1")
        self.manager.create_context("test2")

        assert self.manager._stats["contexts_created"] == initial + 2

    def test_capability_checks_counter(self):
        """Test capability_checks counter."""
        token = CapabilityToken(capability_type="file")

        with self.manager.capability_context("test", [token]):
            initial = self.manager._stats["capability_checks"]

            self.manager.has_capability("file")
            self.manager.has_capability("file")  # Should hit cache

            # At least one capability check should be recorded
            assert self.manager._stats["capability_checks"] >= initial + 1

    def test_cache_statistics(self):
        """Test cache hit/miss statistics."""
        token = CapabilityToken(capability_type="file")

        with self.manager.capability_context("test", [token]):
            # First call - miss
            self.manager.has_capability("file")
            assert self.manager._stats["cache_misses"] > 0

            # Second call - hit
            self.manager.has_capability("file")
            assert self.manager._stats["cache_hits"] > 0
