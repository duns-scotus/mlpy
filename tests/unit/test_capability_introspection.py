"""Unit tests for capability introspection functions.

Tests the three capability introspection builtin functions:
- hasCapability(name)
- getCapabilities()
- getCapabilityInfo(name)
"""

import pytest
from datetime import datetime, timedelta

from mlpy.stdlib.builtin import builtin
from mlpy.runtime.capabilities import CapabilityContext, CapabilityToken
from mlpy.runtime.capabilities.tokens import CapabilityConstraint
from mlpy.runtime.whitelist_validator import set_capability_context


class TestHasCapability:
    """Tests for hasCapability() builtin function."""

    def test_returns_true_when_capability_available(self):
        """Test hasCapability returns true for granted capabilities."""
        with CapabilityContext() as ctx:
            ctx.add_capability(CapabilityToken(capability_type='file.read'))
            set_capability_context(ctx)

            assert builtin.hasCapability('file.read') == True

            set_capability_context(None)

    def test_returns_false_when_capability_not_available(self):
        """Test hasCapability returns false for non-granted capabilities."""
        with CapabilityContext() as ctx:
            ctx.add_capability(CapabilityToken(capability_type='file.read'))
            set_capability_context(ctx)

            assert builtin.hasCapability('file.write') == False
            assert builtin.hasCapability('network.http') == False

            set_capability_context(None)

    def test_returns_false_when_no_context(self):
        """Test hasCapability returns false when no capability context exists."""
        set_capability_context(None)
        assert builtin.hasCapability('file.read') == False
        assert builtin.hasCapability('network.http') == False

    def test_checks_parent_context_capabilities(self):
        """Test hasCapability checks parent contexts for inherited capabilities."""
        with CapabilityContext(name='parent') as parent_ctx:
            parent_ctx.add_capability(CapabilityToken(capability_type='file.read'))

            # Create child context
            child_ctx = parent_ctx.create_child_context(name='child')
            child_ctx.add_capability(CapabilityToken(capability_type='file.write'))

            set_capability_context(child_ctx)

            # Should have both child and parent capabilities
            assert builtin.hasCapability('file.write') == True  # From child
            assert builtin.hasCapability('file.read') == True   # From parent

            set_capability_context(None)

    def test_returns_false_for_expired_capability(self):
        """Test hasCapability returns false for expired capabilities."""
        # Create constraint that will be valid initially but can be checked for expiration
        future_time = datetime.now() + timedelta(seconds=1)
        constraint = CapabilityConstraint(
            expires_at=future_time
        )

        with CapabilityContext() as ctx:
            token = CapabilityToken(
                capability_type='file.read',
                constraints=constraint
            )
            ctx.add_capability(token)
            set_capability_context(ctx)

            # Token is valid initially
            assert builtin.hasCapability('file.read') == True

            # Manually set expiration to the past to simulate expiration
            token.constraints.expires_at = datetime.now() - timedelta(hours=1)

            # Expired capability should now return False
            assert builtin.hasCapability('file.read') == False

            set_capability_context(None)

    def test_multiple_capabilities(self):
        """Test checking multiple capabilities."""
        with CapabilityContext() as ctx:
            ctx.add_capability(CapabilityToken(capability_type='file.read'))
            ctx.add_capability(CapabilityToken(capability_type='file.write'))
            ctx.add_capability(CapabilityToken(capability_type='network.http'))
            set_capability_context(ctx)

            assert builtin.hasCapability('file.read') == True
            assert builtin.hasCapability('file.write') == True
            assert builtin.hasCapability('network.http') == True
            assert builtin.hasCapability('gui.create') == False

            set_capability_context(None)


class TestGetCapabilities:
    """Tests for getCapabilities() builtin function."""

    def test_returns_all_capabilities(self):
        """Test getCapabilities returns complete list of capabilities."""
        with CapabilityContext() as ctx:
            ctx.add_capability(CapabilityToken(capability_type='file.read'))
            ctx.add_capability(CapabilityToken(capability_type='file.write'))
            ctx.add_capability(CapabilityToken(capability_type='network.http'))
            set_capability_context(ctx)

            caps = builtin.getCapabilities()
            assert sorted(caps) == ['file.read', 'file.write', 'network.http']

            set_capability_context(None)

    def test_returns_empty_list_when_no_context(self):
        """Test getCapabilities returns empty list when no context."""
        set_capability_context(None)
        caps = builtin.getCapabilities()
        assert caps == []

    def test_returns_empty_list_when_no_capabilities(self):
        """Test getCapabilities returns empty list for context with no capabilities."""
        with CapabilityContext() as ctx:
            set_capability_context(ctx)

            caps = builtin.getCapabilities()
            assert caps == []

            set_capability_context(None)

    def test_includes_parent_context_capabilities(self):
        """Test getCapabilities includes inherited capabilities from parent."""
        with CapabilityContext(name='parent') as parent_ctx:
            parent_ctx.add_capability(CapabilityToken(capability_type='file.read'))
            parent_ctx.add_capability(CapabilityToken(capability_type='file.write'))

            # Create child context with additional capability
            child_ctx = parent_ctx.create_child_context(name='child')
            child_ctx.add_capability(CapabilityToken(capability_type='network.http'))

            set_capability_context(child_ctx)

            caps = builtin.getCapabilities()
            # Should include both parent and child capabilities
            assert sorted(caps) == ['file.read', 'file.write', 'network.http']

            set_capability_context(None)

    def test_returns_sorted_list(self):
        """Test getCapabilities returns sorted list."""
        with CapabilityContext() as ctx:
            # Add in random order
            ctx.add_capability(CapabilityToken(capability_type='zebra'))
            ctx.add_capability(CapabilityToken(capability_type='alpha'))
            ctx.add_capability(CapabilityToken(capability_type='beta'))
            set_capability_context(ctx)

            caps = builtin.getCapabilities()
            assert caps == ['alpha', 'beta', 'zebra']  # Should be sorted

            set_capability_context(None)

    def test_excludes_expired_capabilities(self):
        """Test getCapabilities excludes expired capabilities."""
        # Create constraint that will be valid initially
        future_time = datetime.now() + timedelta(seconds=1)
        expiring_constraint = CapabilityConstraint(
            expires_at=future_time
        )

        with CapabilityContext() as ctx:
            ctx.add_capability(CapabilityToken(capability_type='file.read'))
            write_token = CapabilityToken(
                capability_type='file.write',
                constraints=expiring_constraint
            )
            ctx.add_capability(write_token)
            set_capability_context(ctx)

            # Both capabilities should be valid initially
            caps = builtin.getCapabilities()
            assert sorted(caps) == ['file.read', 'file.write']

            # Manually expire the write token
            write_token.constraints.expires_at = datetime.now() - timedelta(hours=1)

            # Now should only include valid capability
            caps = builtin.getCapabilities()
            assert caps == ['file.read']

            set_capability_context(None)


class TestGetCapabilityInfo:
    """Tests for getCapabilityInfo() builtin function."""

    def test_returns_basic_info_for_simple_capability(self):
        """Test getCapabilityInfo returns basic info for capability without constraints."""
        with CapabilityContext() as ctx:
            token = CapabilityToken(capability_type='file.read')
            ctx.add_capability(token)
            set_capability_context(ctx)

            info = builtin.getCapabilityInfo('file.read')
            assert info is not None
            assert info['type'] == 'file.read'
            assert info['available'] == True
            assert info['usage_count'] == 0
            assert info['patterns'] is None
            assert info['operations'] is None
            assert info['max_usage'] is None
            assert info['expires_at'] is None

            set_capability_context(None)

    def test_returns_none_when_capability_not_available(self):
        """Test getCapabilityInfo returns None for non-existent capability."""
        with CapabilityContext() as ctx:
            ctx.add_capability(CapabilityToken(capability_type='file.read'))
            set_capability_context(ctx)

            info = builtin.getCapabilityInfo('file.write')
            assert info is None

            set_capability_context(None)

    def test_returns_none_when_no_context(self):
        """Test getCapabilityInfo returns None when no context."""
        set_capability_context(None)
        info = builtin.getCapabilityInfo('file.read')
        assert info is None

    def test_returns_detailed_info_with_constraints(self):
        """Test getCapabilityInfo returns complete constraint information."""
        constraint = CapabilityConstraint(
            resource_patterns=['*.txt', 'data/*.json'],
            allowed_operations={'read', 'write'},
            max_usage_count=100
        )

        with CapabilityContext() as ctx:
            token = CapabilityToken(
                capability_type='file.read',
                constraints=constraint
            )
            ctx.add_capability(token)
            set_capability_context(ctx)

            info = builtin.getCapabilityInfo('file.read')
            assert info is not None
            assert info['type'] == 'file.read'
            assert info['available'] == True
            assert info['patterns'] == ['*.txt', 'data/*.json']
            assert sorted(info['operations']) == ['read', 'write']
            assert info['max_usage'] == 100
            assert info['usage_count'] == 0

            set_capability_context(None)

    def test_returns_expiration_info(self):
        """Test getCapabilityInfo includes expiration timestamp."""
        future_time = datetime.now() + timedelta(hours=24)
        constraint = CapabilityConstraint(expires_at=future_time)

        with CapabilityContext() as ctx:
            token = CapabilityToken(
                capability_type='file.read',
                constraints=constraint
            )
            ctx.add_capability(token)
            set_capability_context(ctx)

            info = builtin.getCapabilityInfo('file.read')
            assert info is not None
            assert info['expires_at'] is not None
            assert info['expires_at'] == future_time.isoformat()

            set_capability_context(None)

    def test_tracks_usage_count(self):
        """Test getCapabilityInfo reflects capability usage."""
        with CapabilityContext() as ctx:
            token = CapabilityToken(capability_type='file.read')
            ctx.add_capability(token)
            set_capability_context(ctx)

            # Use the capability
            token.use_token('test.txt', 'read')
            token.use_token('data.txt', 'read')

            info = builtin.getCapabilityInfo('file.read')
            assert info is not None
            assert info['usage_count'] == 2

            set_capability_context(None)

    def test_shows_unavailable_for_expired_capability(self):
        """Test getCapabilityInfo shows available=false for expired capability."""
        # Create constraint that will be valid initially
        future_time = datetime.now() + timedelta(seconds=1)
        expiring_constraint = CapabilityConstraint(
            expires_at=future_time
        )

        with CapabilityContext() as ctx:
            token = CapabilityToken(
                capability_type='file.read',
                constraints=expiring_constraint
            )
            ctx.add_capability(token)
            set_capability_context(ctx)

            # Token should be valid initially
            info = builtin.getCapabilityInfo('file.read')
            assert info is not None
            assert info['available'] == True

            # Manually expire the token
            token.constraints.expires_at = datetime.now() - timedelta(hours=1)

            # Now should show as unavailable
            info = builtin.getCapabilityInfo('file.read')
            assert info is not None
            assert info['available'] == False  # Expired

            set_capability_context(None)

    def test_handles_empty_constraint_lists(self):
        """Test getCapabilityInfo handles constraints with empty lists."""
        constraint = CapabilityConstraint(
            resource_patterns=[],
            allowed_operations=set()
        )

        with CapabilityContext() as ctx:
            token = CapabilityToken(
                capability_type='file.read',
                constraints=constraint
            )
            ctx.add_capability(token)
            set_capability_context(ctx)

            info = builtin.getCapabilityInfo('file.read')
            assert info is not None
            # Empty lists should be returned as None for ML compatibility
            assert info['patterns'] is None
            assert info['operations'] is None

            set_capability_context(None)


class TestIntegrationScenarios:
    """Integration tests for combined usage of capability introspection functions."""

    def test_defensive_programming_pattern(self):
        """Test defensive programming pattern: check before use."""
        with CapabilityContext() as ctx:
            ctx.add_capability(CapabilityToken(capability_type='file.read'))
            set_capability_context(ctx)

            # Defensive check
            if builtin.hasCapability('file.read'):
                # Would proceed with file operation
                assert True
            else:
                # Would handle missing capability
                assert False, "Should have file.read capability"

            # Check for unavailable capability
            if builtin.hasCapability('network.http'):
                assert False, "Should not have network.http"
            else:
                # Graceful degradation
                assert True

            set_capability_context(None)

    def test_capability_listing_pattern(self):
        """Test capability listing for debug/logging."""
        with CapabilityContext() as ctx:
            ctx.add_capability(CapabilityToken(capability_type='file.read'))
            ctx.add_capability(CapabilityToken(capability_type='file.write'))
            ctx.add_capability(CapabilityToken(capability_type='network.http'))
            set_capability_context(ctx)

            caps = builtin.getCapabilities()
            assert len(caps) == 3
            assert 'file.read' in caps
            assert 'file.write' in caps
            assert 'network.http' in caps

            # Simulate logging/debug output
            for cap in caps:
                assert builtin.hasCapability(cap) == True

            set_capability_context(None)

    def test_resource_constraint_checking_pattern(self):
        """Test checking resource constraints before operations."""
        constraint = CapabilityConstraint(
            resource_patterns=['*.txt'],
            max_usage_count=5
        )

        with CapabilityContext() as ctx:
            token = CapabilityToken(
                capability_type='file.read',
                constraints=constraint
            )
            ctx.add_capability(token)
            set_capability_context(ctx)

            # Check if capability exists
            assert builtin.hasCapability('file.read') == True

            # Get detailed info to check constraints
            info = builtin.getCapabilityInfo('file.read')
            assert info is not None
            assert info['patterns'] == ['*.txt']
            assert info['max_usage'] == 5

            # Simulate checking if operation is allowed
            # (In real code, would check if file matches pattern)
            if info['patterns'] is not None:
                assert '*.txt' in info['patterns']

            # Check usage limits
            if info['max_usage'] is not None:
                remaining = info['max_usage'] - info['usage_count']
                assert remaining == 5  # Not used yet

            set_capability_context(None)

    def test_no_context_safety(self):
        """Test all functions handle missing context safely."""
        set_capability_context(None)

        # All functions should handle None context gracefully
        assert builtin.hasCapability('file.read') == False
        assert builtin.getCapabilities() == []
        assert builtin.getCapabilityInfo('file.read') is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
