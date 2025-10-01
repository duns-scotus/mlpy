"""
Comprehensive test suite for capabilities/context.py

Tests capability context management including:
- CapabilityContext creation and identity
- Thread-safe capability storage
- Context hierarchy and inheritance
- Capability lookup with parent traversal
- Token validation and cleanup
- Context manager protocol
"""

import threading
import time
from datetime import datetime, timedelta

import pytest

from mlpy.runtime.capabilities.context import CapabilityContext
from mlpy.runtime.capabilities.exceptions import (
    CapabilityContextError,
    CapabilityNotFoundError,
)
from mlpy.runtime.capabilities.tokens import CapabilityConstraint, CapabilityToken


class TestCapabilityContext:
    """Test CapabilityContext class."""

    def test_context_creation_defaults(self):
        """Test context creation with defaults."""
        context = CapabilityContext()
        assert context.context_id is not None
        assert len(context.context_id) > 0
        assert context.name == ""
        assert context.parent_context is None
        assert len(context.child_contexts) == 0
        assert context.thread_id is not None

    def test_context_with_name(self):
        """Test context with custom name."""
        context = CapabilityContext(name="test_context")
        assert context.name == "test_context"

    def test_context_with_parent(self):
        """Test context with parent."""
        parent = CapabilityContext(name="parent")
        child = CapabilityContext(name="child", parent_context=parent)
        assert child.parent_context == parent
        assert child in parent.child_contexts

    def test_context_id_is_unique(self):
        """Test each context gets unique ID."""
        context1 = CapabilityContext()
        context2 = CapabilityContext()
        assert context1.context_id != context2.context_id

    def test_add_capability(self):
        """Test adding capability token."""
        context = CapabilityContext()
        token = CapabilityToken(capability_type="file_system")
        context.add_capability(token)
        assert context.has_capability("file_system")

    def test_add_invalid_capability_raises_error(self):
        """Test adding invalid token raises error."""
        context = CapabilityContext()
        # Create expired token
        expires = datetime.now() - timedelta(hours=1)
        constraint = CapabilityConstraint(expires_at=expires)
        token = CapabilityToken(capability_type="test", constraints=constraint)

        with pytest.raises(CapabilityContextError):
            context.add_capability(token)

    def test_remove_capability(self):
        """Test removing capability."""
        context = CapabilityContext()
        token = CapabilityToken(capability_type="file_system")
        context.add_capability(token)

        result = context.remove_capability("file_system")
        assert result is True
        assert not context.has_capability("file_system")

    def test_remove_nonexistent_capability(self):
        """Test removing non-existent capability."""
        context = CapabilityContext()
        result = context.remove_capability("nonexistent")
        assert result is False

    def test_has_capability_local(self):
        """Test has_capability for local token."""
        context = CapabilityContext()
        token = CapabilityToken(capability_type="file_system")
        context.add_capability(token)
        assert context.has_capability("file_system") is True

    def test_has_capability_missing(self):
        """Test has_capability for missing capability."""
        context = CapabilityContext()
        assert context.has_capability("nonexistent") is False

    def test_has_capability_in_parent(self):
        """Test has_capability finds capability in parent."""
        parent = CapabilityContext(name="parent")
        child = CapabilityContext(name="child", parent_context=parent)

        token = CapabilityToken(capability_type="file_system")
        parent.add_capability(token)

        assert child.has_capability("file_system", check_parents=True) is True

    def test_has_capability_no_parent_check(self):
        """Test has_capability without parent check."""
        parent = CapabilityContext(name="parent")
        child = CapabilityContext(name="child", parent_context=parent)

        token = CapabilityToken(capability_type="file_system")
        parent.add_capability(token)

        assert child.has_capability("file_system", check_parents=False) is False

    def test_get_capability(self):
        """Test getting capability token."""
        context = CapabilityContext()
        token = CapabilityToken(capability_type="file_system")
        context.add_capability(token)

        retrieved = context.get_capability("file_system")
        assert retrieved == token

    def test_get_capability_from_parent(self):
        """Test getting capability from parent."""
        parent = CapabilityContext(name="parent")
        child = CapabilityContext(name="child", parent_context=parent)

        token = CapabilityToken(capability_type="file_system")
        parent.add_capability(token)

        retrieved = child.get_capability("file_system", check_parents=True)
        assert retrieved == token

    def test_get_capability_not_found_raises_error(self):
        """Test get_capability raises error when not found."""
        context = CapabilityContext()
        with pytest.raises(CapabilityNotFoundError):
            context.get_capability("nonexistent")

    def test_can_access_resource(self):
        """Test can_access_resource."""
        context = CapabilityContext()
        constraint = CapabilityConstraint(
            resource_patterns=["*.txt"], allowed_operations={"read"}
        )
        token = CapabilityToken(capability_type="file_system", constraints=constraint)
        context.add_capability(token)

        assert context.can_access_resource("file_system", "file.txt", "read") is True

    def test_can_access_resource_denied(self):
        """Test can_access_resource denied."""
        context = CapabilityContext()
        constraint = CapabilityConstraint(resource_patterns=["*.txt"])
        token = CapabilityToken(capability_type="file_system", constraints=constraint)
        context.add_capability(token)

        assert context.can_access_resource("file_system", "file.py", "read") is False

    def test_use_capability(self):
        """Test using capability."""
        context = CapabilityContext()
        token = CapabilityToken(capability_type="file_system")
        context.add_capability(token)

        context.use_capability("file_system", "file.txt", "read")
        # Should increment usage count
        assert token.usage_count == 1

    def test_get_all_capabilities_local(self):
        """Test getting all local capabilities."""
        context = CapabilityContext()
        token1 = CapabilityToken(capability_type="file_system")
        token2 = CapabilityToken(capability_type="network")
        context.add_capability(token1)
        context.add_capability(token2)

        all_caps = context.get_all_capabilities(include_parents=False)
        assert len(all_caps) == 2
        assert "file_system" in all_caps
        assert "network" in all_caps

    def test_get_all_capabilities_with_parents(self):
        """Test getting all capabilities including parents."""
        parent = CapabilityContext(name="parent")
        child = CapabilityContext(name="child", parent_context=parent)

        parent_token = CapabilityToken(capability_type="file_system")
        child_token = CapabilityToken(capability_type="network")
        parent.add_capability(parent_token)
        child.add_capability(child_token)

        all_caps = child.get_all_capabilities(include_parents=True)
        assert len(all_caps) >= 2
        assert "file_system" in all_caps
        assert "network" in all_caps

    def test_cleanup_expired_tokens(self):
        """Test cleanup of expired tokens."""
        context = CapabilityContext()

        # Add expired token
        expires = datetime.now() - timedelta(hours=1)
        constraint = CapabilityConstraint(expires_at=expires)
        expired_token = CapabilityToken(capability_type="expired", constraints=constraint)
        # Bypass validation by adding directly
        context._tokens["expired"] = expired_token

        # Add valid token
        valid_token = CapabilityToken(capability_type="valid")
        context.add_capability(valid_token)

        removed_count = context.cleanup_expired_tokens()
        assert removed_count == 1
        assert not context.has_capability("expired")
        assert context.has_capability("valid")

    def test_create_child_context(self):
        """Test creating child context."""
        parent = CapabilityContext(name="parent")
        child = parent.create_child_context("child")

        assert child.parent_context == parent
        assert child in parent.child_contexts
        assert child.name == "child"

    def test_get_context_hierarchy(self):
        """Test getting context hierarchy."""
        root = CapabilityContext(name="root")
        level1 = CapabilityContext(name="level1", parent_context=root)
        level2 = CapabilityContext(name="level2", parent_context=level1)

        hierarchy = level2.get_context_hierarchy()
        assert "root" in hierarchy
        assert "level1" in hierarchy
        assert "level2" in hierarchy

    def test_to_dict_serialization(self):
        """Test to_dict serialization."""
        context = CapabilityContext(name="test")
        token = CapabilityToken(capability_type="file_system")
        context.add_capability(token)

        data = context.to_dict()
        assert data["context_id"] == context.context_id
        assert data["name"] == "test"
        assert "capabilities" in data
        assert len(data["capabilities"]) > 0

    def test_context_manager_enter(self):
        """Test context manager __enter__."""
        context = CapabilityContext()
        with context as ctx:
            assert ctx == context

    def test_context_manager_exit(self):
        """Test context manager __exit__."""
        # Just ensure no errors
        context = CapabilityContext()
        with context:
            pass

    def test_repr(self):
        """Test string representation."""
        context = CapabilityContext(name="test")
        repr_str = repr(context)
        assert "CapabilityContext" in repr_str
        assert "test" in repr_str

    def test_thread_safety(self):
        """Test thread-safe access."""
        context = CapabilityContext()
        results = []

        def add_tokens():
            for i in range(10):
                token = CapabilityToken(capability_type=f"type_{i}")
                context.add_capability(token)
                results.append(i)

        threads = [threading.Thread(target=add_tokens) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Should have successfully added tokens from both threads
        assert len(results) > 0

    def test_has_capability_removes_invalid(self):
        """Test has_capability removes invalid tokens."""
        context = CapabilityContext()

        # Add expired token directly
        expires = datetime.now() - timedelta(hours=1)
        constraint = CapabilityConstraint(expires_at=expires)
        expired_token = CapabilityToken(capability_type="expired", constraints=constraint)
        context._tokens["expired"] = expired_token

        # has_capability should detect and remove invalid token
        result = context.has_capability("expired")
        assert result is False
        assert "expired" not in context._tokens

    def test_multi_level_hierarchy(self):
        """Test multi-level context hierarchy."""
        root = CapabilityContext(name="root")
        level1 = CapabilityContext(name="level1", parent_context=root)
        level2 = CapabilityContext(name="level2", parent_context=level1)

        root_token = CapabilityToken(capability_type="root_cap")
        root.add_capability(root_token)

        # level2 should find capability in root
        assert level2.has_capability("root_cap", check_parents=True) is True

    def test_child_overrides_parent_capability(self):
        """Test child capability overrides parent."""
        parent = CapabilityContext(name="parent")
        child = CapabilityContext(name="child", parent_context=parent)

        parent_token = CapabilityToken(capability_type="test")
        child_token = CapabilityToken(capability_type="test")
        parent.add_capability(parent_token)
        child.add_capability(child_token)

        # Child should return its own token, not parent's
        retrieved = child.get_capability("test", check_parents=False)
        assert retrieved == child_token
