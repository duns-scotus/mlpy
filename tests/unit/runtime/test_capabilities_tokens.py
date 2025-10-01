"""
Comprehensive test suite for capabilities/tokens.py

Tests capability token system including:
- CapabilityConstraint for resource and operation constraints
- CapabilityToken with UUID-based identity
- Token validation and integrity checking
- Resource pattern matching
- Operation permissions
- Usage tracking and limits
- Expiration handling
- Serialization (to_dict/from_dict)
"""

import uuid
from datetime import datetime, timedelta

import pytest

from mlpy.runtime.capabilities.exceptions import (
    CapabilityExpiredError,
    CapabilityValidationError,
)
from mlpy.runtime.capabilities.tokens import CapabilityConstraint, CapabilityToken


class TestCapabilityConstraint:
    """Test CapabilityConstraint class."""

    def test_constraint_creation_defaults(self):
        """Test constraint creation with defaults."""
        constraint = CapabilityConstraint()
        assert constraint.resource_patterns == []
        assert constraint.allowed_operations == set()
        assert constraint.max_usage_count is None
        assert constraint.expires_at is None
        assert constraint.max_file_size is None
        assert constraint.max_memory is None
        assert constraint.max_cpu_time is None
        assert constraint.allowed_hosts == []
        assert constraint.allowed_ports == []

    def test_constraint_with_resource_patterns(self):
        """Test constraint with resource patterns."""
        constraint = CapabilityConstraint(resource_patterns=["*.txt", "data/*"])
        assert len(constraint.resource_patterns) == 2
        assert "*.txt" in constraint.resource_patterns

    def test_constraint_with_allowed_operations(self):
        """Test constraint with allowed operations."""
        constraint = CapabilityConstraint(allowed_operations={"read", "write"})
        assert "read" in constraint.allowed_operations
        assert "write" in constraint.allowed_operations

    def test_constraint_with_usage_limit(self):
        """Test constraint with usage limit."""
        constraint = CapabilityConstraint(max_usage_count=10)
        assert constraint.max_usage_count == 10

    def test_constraint_with_expiration(self):
        """Test constraint with expiration time."""
        expires = datetime.now() + timedelta(hours=1)
        constraint = CapabilityConstraint(expires_at=expires)
        assert constraint.expires_at == expires

    def test_constraint_with_resource_limits(self):
        """Test constraint with resource limits."""
        constraint = CapabilityConstraint(
            max_file_size=1024 * 1024,  # 1MB
            max_memory=1024 * 1024 * 100,  # 100MB
            max_cpu_time=60.0,  # 60 seconds
        )
        assert constraint.max_file_size == 1024 * 1024
        assert constraint.max_memory == 1024 * 1024 * 100
        assert constraint.max_cpu_time == 60.0

    def test_constraint_with_network_restrictions(self):
        """Test constraint with network restrictions."""
        constraint = CapabilityConstraint(
            allowed_hosts=["example.com", "api.example.com"], allowed_ports=[80, 443]
        )
        assert "example.com" in constraint.allowed_hosts
        assert 443 in constraint.allowed_ports

    def test_matches_resource_no_restrictions(self):
        """Test matches_resource with no restrictions."""
        constraint = CapabilityConstraint()
        assert constraint.matches_resource("/any/path/file.txt") is True

    def test_matches_resource_with_wildcard(self):
        """Test matches_resource with wildcard patterns."""
        constraint = CapabilityConstraint(resource_patterns=["*.txt"])
        assert constraint.matches_resource("file.txt") is True
        assert constraint.matches_resource("file.py") is False

    def test_matches_resource_with_path_pattern(self):
        """Test matches_resource with path patterns."""
        constraint = CapabilityConstraint(resource_patterns=["data/*"])
        assert constraint.matches_resource("data/file.txt") is True
        assert constraint.matches_resource("other/file.txt") is False

    def test_matches_resource_multiple_patterns(self):
        """Test matches_resource with multiple patterns."""
        constraint = CapabilityConstraint(resource_patterns=["*.txt", "*.md", "data/*"])
        assert constraint.matches_resource("readme.md") is True
        assert constraint.matches_resource("file.txt") is True
        assert constraint.matches_resource("data/config.json") is True
        assert constraint.matches_resource("script.py") is False

    def test_allows_operation_no_restrictions(self):
        """Test allows_operation with no restrictions."""
        constraint = CapabilityConstraint()
        assert constraint.allows_operation("read") is True
        assert constraint.allows_operation("write") is True

    def test_allows_operation_with_restrictions(self):
        """Test allows_operation with restrictions."""
        constraint = CapabilityConstraint(allowed_operations={"read"})
        assert constraint.allows_operation("read") is True
        assert constraint.allows_operation("write") is False

    def test_allows_operation_multiple(self):
        """Test allows_operation with multiple operations."""
        constraint = CapabilityConstraint(allowed_operations={"read", "write", "execute"})
        assert constraint.allows_operation("read") is True
        assert constraint.allows_operation("write") is True
        assert constraint.allows_operation("execute") is True
        assert constraint.allows_operation("delete") is False

    def test_is_expired_no_expiration(self):
        """Test is_expired with no expiration set."""
        constraint = CapabilityConstraint()
        assert constraint.is_expired() is False

    def test_is_expired_future_expiration(self):
        """Test is_expired with future expiration."""
        expires = datetime.now() + timedelta(hours=1)
        constraint = CapabilityConstraint(expires_at=expires)
        assert constraint.is_expired() is False

    def test_is_expired_past_expiration(self):
        """Test is_expired with past expiration."""
        expires = datetime.now() - timedelta(hours=1)
        constraint = CapabilityConstraint(expires_at=expires)
        assert constraint.is_expired() is True


class TestCapabilityToken:
    """Test CapabilityToken class."""

    def test_token_creation_defaults(self):
        """Test token creation with defaults."""
        token = CapabilityToken()
        assert token.token_id is not None
        assert len(token.token_id) > 0
        assert token.capability_type == ""
        assert isinstance(token.constraints, CapabilityConstraint)
        assert token.usage_count == 0
        assert token.last_used_at is None
        assert token.created_by == "system"

    def test_token_with_custom_id(self):
        """Test token with custom ID."""
        custom_id = str(uuid.uuid4())
        token = CapabilityToken(token_id=custom_id)
        assert token.token_id == custom_id

    def test_token_with_capability_type(self):
        """Test token with capability type."""
        token = CapabilityToken(capability_type="file_system")
        assert token.capability_type == "file_system"

    def test_token_with_constraints(self):
        """Test token with custom constraints."""
        constraint = CapabilityConstraint(allowed_operations={"read"})
        token = CapabilityToken(constraints=constraint)
        assert token.constraints == constraint

    def test_token_with_creator(self):
        """Test token with creator information."""
        token = CapabilityToken(created_by="user123", description="Test capability")
        assert token.created_by == "user123"
        assert token.description == "Test capability"

    def test_token_id_is_unique(self):
        """Test that each token gets unique ID."""
        token1 = CapabilityToken()
        token2 = CapabilityToken()
        assert token1.token_id != token2.token_id

    def test_post_init_calculates_checksum(self):
        """Test that __post_init__ calculates checksum."""
        token = CapabilityToken()
        assert token._checksum is not None
        assert len(token._checksum) > 0

    def test_calculate_checksum_is_deterministic(self):
        """Test that checksum calculation is deterministic."""
        token_id = str(uuid.uuid4())
        created_at = datetime.now()

        token1 = CapabilityToken(token_id=token_id, created_at=created_at)
        checksum1 = token1._checksum

        token2 = CapabilityToken(token_id=token_id, created_at=created_at)
        checksum2 = token2._checksum

        assert checksum1 == checksum2

    def test_validate_integrity_valid_token(self):
        """Test validate_integrity for valid token."""
        token = CapabilityToken()
        assert token.validate_integrity() is True

    def test_validate_integrity_tampered_token(self):
        """Test validate_integrity for tampered token."""
        token = CapabilityToken()
        original_checksum = token._checksum
        token.capability_type = "modified"
        # Checksum should no longer match
        assert token.validate_integrity() is False
        # Restore for cleanup
        token._checksum = original_checksum

    def test_is_valid_fresh_token(self):
        """Test is_valid for fresh token."""
        token = CapabilityToken(capability_type="test")
        assert token.is_valid() is True

    def test_is_valid_expired_token(self):
        """Test is_valid for expired token."""
        expires = datetime.now() - timedelta(hours=1)
        constraint = CapabilityConstraint(expires_at=expires)
        token = CapabilityToken(constraints=constraint)
        assert token.is_valid() is False

    def test_is_valid_usage_limit_exceeded(self):
        """Test is_valid for token with exceeded usage limit."""
        constraint = CapabilityConstraint(max_usage_count=2)
        token = CapabilityToken(constraints=constraint, usage_count=3)
        assert token.is_valid() is False

    def test_is_valid_tampered_token(self):
        """Test is_valid for tampered token."""
        token = CapabilityToken()
        token.capability_type = "modified"
        assert token.is_valid() is False

    def test_can_access_resource_allowed(self):
        """Test can_access_resource for allowed access."""
        constraint = CapabilityConstraint(
            resource_patterns=["*.txt"], allowed_operations={"read"}
        )
        token = CapabilityToken(constraints=constraint)
        assert token.can_access_resource("file.txt", "read") is True

    def test_can_access_resource_wrong_pattern(self):
        """Test can_access_resource for wrong resource pattern."""
        constraint = CapabilityConstraint(resource_patterns=["*.txt"])
        token = CapabilityToken(constraints=constraint)
        assert token.can_access_resource("file.py", "read") is False

    def test_can_access_resource_wrong_operation(self):
        """Test can_access_resource for wrong operation."""
        constraint = CapabilityConstraint(allowed_operations={"read"})
        token = CapabilityToken(constraints=constraint)
        assert token.can_access_resource("file.txt", "write") is False

    def test_can_access_resource_expired_token(self):
        """Test can_access_resource for expired token."""
        expires = datetime.now() - timedelta(hours=1)
        constraint = CapabilityConstraint(expires_at=expires)
        token = CapabilityToken(constraints=constraint)
        assert token.can_access_resource("file.txt", "read") is False

    def test_use_token_successful(self):
        """Test use_token for successful usage."""
        constraint = CapabilityConstraint(resource_patterns=["*.txt"])
        token = CapabilityToken(constraints=constraint)
        initial_count = token.usage_count

        token.use_token("file.txt", "read")

        assert token.usage_count == initial_count + 1
        assert token.last_used_at is not None

    def test_use_token_increments_usage_count(self):
        """Test use_token increments usage count."""
        token = CapabilityToken()
        token.use_token("file.txt", "read")
        token.use_token("file.txt", "read")
        assert token.usage_count == 2

    def test_use_token_updates_last_used(self):
        """Test use_token updates last_used_at."""
        token = CapabilityToken()
        before = datetime.now()
        token.use_token("file.txt", "read")
        assert token.last_used_at >= before

    def test_use_token_expired_raises_error(self):
        """Test use_token raises error for expired token."""
        expires = datetime.now() - timedelta(hours=1)
        constraint = CapabilityConstraint(expires_at=expires)
        token = CapabilityToken(constraints=constraint)

        with pytest.raises(CapabilityExpiredError):
            token.use_token("file.txt", "read")

    def test_use_token_usage_limit_exceeded_raises_error(self):
        """Test use_token raises error when usage limit exceeded."""
        constraint = CapabilityConstraint(max_usage_count=1)
        token = CapabilityToken(constraints=constraint, usage_count=1)

        with pytest.raises(CapabilityValidationError):
            token.use_token("file.txt", "read")

    def test_use_token_invalid_resource_raises_error(self):
        """Test use_token raises error for invalid resource."""
        constraint = CapabilityConstraint(resource_patterns=["*.txt"])
        token = CapabilityToken(constraints=constraint)

        with pytest.raises(CapabilityValidationError):
            token.use_token("file.py", "read")

    def test_use_token_invalid_operation_raises_error(self):
        """Test use_token raises error for invalid operation."""
        constraint = CapabilityConstraint(allowed_operations={"read"})
        token = CapabilityToken(constraints=constraint)

        with pytest.raises(CapabilityValidationError):
            token.use_token("file.txt", "write")

    def test_to_dict_serialization(self):
        """Test to_dict serialization."""
        token = CapabilityToken(
            capability_type="test", created_by="user1", description="Test token"
        )
        data = token.to_dict()

        assert data["token_id"] == token.token_id
        assert data["capability_type"] == "test"
        assert data["created_by"] == "user1"
        assert data["description"] == "Test token"
        assert "constraints" in data
        assert "usage_count" in data

    def test_to_dict_includes_constraints(self):
        """Test to_dict includes constraint data."""
        constraint = CapabilityConstraint(
            resource_patterns=["*.txt"], allowed_operations={"read"}
        )
        token = CapabilityToken(constraints=constraint)
        data = token.to_dict()

        assert "constraints" in data
        assert data["constraints"]["resource_patterns"] == ["*.txt"]
        assert data["constraints"]["allowed_operations"] == ["read"]

    def test_from_dict_deserialization(self):
        """Test from_dict deserialization."""
        original = CapabilityToken(capability_type="test", created_by="user1")
        data = original.to_dict()
        restored = CapabilityToken.from_dict(data)

        assert restored.token_id == original.token_id
        assert restored.capability_type == original.capability_type
        assert restored.created_by == original.created_by

    def test_from_dict_restores_constraints(self):
        """Test from_dict restores constraints."""
        constraint = CapabilityConstraint(
            resource_patterns=["*.txt"], allowed_operations={"read"}
        )
        original = CapabilityToken(constraints=constraint)
        data = original.to_dict()
        restored = CapabilityToken.from_dict(data)

        assert len(restored.constraints.resource_patterns) == 1
        assert "*.txt" in restored.constraints.resource_patterns
        assert "read" in restored.constraints.allowed_operations

    def test_from_dict_restores_usage_tracking(self):
        """Test from_dict restores usage tracking."""
        original = CapabilityToken()
        original.use_token("file.txt", "read")
        data = original.to_dict()
        restored = CapabilityToken.from_dict(data)

        assert restored.usage_count == original.usage_count
        assert restored.last_used_at is not None

    def test_round_trip_serialization(self):
        """Test round-trip serialization preserves token."""
        expires = datetime.now() + timedelta(hours=1)
        constraint = CapabilityConstraint(
            resource_patterns=["*.txt", "data/*"],
            allowed_operations={"read", "write"},
            max_usage_count=10,
            expires_at=expires,
        )
        original = CapabilityToken(
            capability_type="file_system", constraints=constraint, created_by="test_user"
        )

        # Serialize and deserialize
        data = original.to_dict()
        restored = CapabilityToken.from_dict(data)

        # Verify key properties preserved
        assert restored.token_id == original.token_id
        assert restored.capability_type == original.capability_type
        assert len(restored.constraints.resource_patterns) == 2
        assert len(restored.constraints.allowed_operations) == 2

    def test_token_with_all_constraints(self):
        """Test token with all constraint types."""
        expires = datetime.now() + timedelta(hours=1)
        constraint = CapabilityConstraint(
            resource_patterns=["*.txt"],
            allowed_operations={"read", "write"},
            max_usage_count=100,
            expires_at=expires,
            max_file_size=1024 * 1024,
            max_memory=1024 * 1024 * 10,
            max_cpu_time=30.0,
            allowed_hosts=["example.com"],
            allowed_ports=[80, 443],
        )
        token = CapabilityToken(constraints=constraint)

        assert token.is_valid() is True
        assert token.can_access_resource("file.txt", "read") is True

    def test_multiple_tokens_independent(self):
        """Test that multiple tokens are independent."""
        token1 = CapabilityToken(capability_type="type1")
        token2 = CapabilityToken(capability_type="type2")

        token1.use_token("file.txt", "read")

        assert token1.usage_count == 1
        assert token2.usage_count == 0
        assert token1.token_id != token2.token_id
