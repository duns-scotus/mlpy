"""Tests for capability token system."""

import pytest
from datetime import datetime, timedelta
from src.mlpy.runtime.capabilities.tokens import (
    CapabilityToken, CapabilityConstraint, create_capability_token,
    create_file_capability, create_network_capability
)
from src.mlpy.runtime.capabilities.exceptions import (
    CapabilityValidationError, CapabilityExpiredError
)


class TestCapabilityConstraint:
    """Test capability constraint functionality."""

    def test_resource_pattern_matching(self):
        """Test resource pattern matching."""
        constraint = CapabilityConstraint(resource_patterns=["*.txt", "data/*.json"])

        assert constraint.matches_resource("file.txt")
        assert constraint.matches_resource("data/config.json")
        assert not constraint.matches_resource("file.py")
        assert not constraint.matches_resource("config.json")

    def test_operation_permission(self):
        """Test operation permission checking."""
        constraint = CapabilityConstraint(allowed_operations={"read", "write"})

        assert constraint.allows_operation("read")
        assert constraint.allows_operation("write")
        assert not constraint.allows_operation("execute")

    def test_expiration_check(self):
        """Test expiration checking."""
        # Non-expiring constraint
        constraint1 = CapabilityConstraint()
        assert not constraint1.is_expired()

        # Expired constraint
        constraint2 = CapabilityConstraint(
            expires_at=datetime.now() - timedelta(hours=1)
        )
        assert constraint2.is_expired()

        # Non-expired constraint
        constraint3 = CapabilityConstraint(
            expires_at=datetime.now() + timedelta(hours=1)
        )
        assert not constraint3.is_expired()


class TestCapabilityToken:
    """Test capability token functionality."""

    def test_token_creation(self):
        """Test basic token creation."""
        token = CapabilityToken(capability_type="file")

        assert token.token_id is not None
        assert token.capability_type == "file"
        assert token.usage_count == 0
        assert token.validate_integrity()

    def test_token_validation(self):
        """Test token validation."""
        # Valid token
        token = CapabilityToken(capability_type="file")
        assert token.is_valid()

        # Invalid usage count
        token.usage_count = 1000
        token.constraints.max_usage_count = 5
        assert not token.is_valid()

    def test_resource_access_validation(self):
        """Test resource access validation."""
        constraint = CapabilityConstraint(
            resource_patterns=["*.txt"],
            allowed_operations={"read"}
        )
        token = CapabilityToken(
            capability_type="file",
            constraints=constraint
        )

        assert token.can_access_resource("test.txt", "read")
        assert not token.can_access_resource("test.txt", "write")
        assert not token.can_access_resource("test.py", "read")

    def test_token_usage(self):
        """Test token usage tracking."""
        token = CapabilityToken(capability_type="file")

        assert token.usage_count == 0
        assert token.last_used_at is None

        # Use token
        token.use_token("test.txt", "read")

        assert token.usage_count == 1
        assert token.last_used_at is not None

    def test_token_usage_limits(self):
        """Test token usage limits."""
        constraint = CapabilityConstraint(max_usage_count=2)
        token = CapabilityToken(
            capability_type="file",
            constraints=constraint
        )

        # First usage should work
        token.use_token("test.txt", "read")
        assert token.usage_count == 1

        # Second usage should work
        token.use_token("test.txt", "read")
        assert token.usage_count == 2

        # Third usage should fail
        with pytest.raises(CapabilityValidationError):
            token.use_token("test.txt", "read")

    def test_token_expiration(self):
        """Test token expiration."""
        constraint = CapabilityConstraint(
            expires_at=datetime.now() - timedelta(seconds=1)
        )
        token = CapabilityToken(
            capability_type="file",
            constraints=constraint
        )

        with pytest.raises(CapabilityExpiredError):
            token.use_token("test.txt", "read")

    def test_token_serialization(self):
        """Test token serialization and deserialization."""
        original_token = CapabilityToken(
            capability_type="file",
            description="Test token"
        )

        # Serialize to dict
        token_dict = original_token.to_dict()

        # Deserialize from dict
        restored_token = CapabilityToken.from_dict(token_dict)

        assert restored_token.token_id == original_token.token_id
        assert restored_token.capability_type == original_token.capability_type
        assert restored_token.description == original_token.description
        assert restored_token.validate_integrity()

    def test_token_integrity_validation(self):
        """Test token integrity validation."""
        token = CapabilityToken(capability_type="file")

        # Valid token
        assert token.validate_integrity()

        # Tamper with token
        token.capability_type = "network"

        # Should detect tampering
        assert not token.validate_integrity()


class TestCapabilityTokenFactory:
    """Test capability token factory functions."""

    def test_create_capability_token(self):
        """Test generic capability token creation."""
        token = create_capability_token(
            capability_type="test",
            resource_patterns=["*.txt"],
            allowed_operations={"read"},
            description="Test token"
        )

        assert token.capability_type == "test"
        assert token.constraints.resource_patterns == ["*.txt"]
        assert token.constraints.allowed_operations == {"read"}
        assert token.description == "Test token"

    def test_create_file_capability(self):
        """Test file capability creation."""
        token = create_file_capability(
            patterns=["*.txt", "data/*.json"],
            operations={"read", "write"},
            max_file_size=1024 * 1024
        )

        assert token.capability_type == "file"
        assert token.constraints.resource_patterns == ["*.txt", "data/*.json"]
        assert token.constraints.allowed_operations == {"read", "write"}
        assert token.constraints.max_file_size == 1024 * 1024

    def test_create_network_capability(self):
        """Test network capability creation."""
        token = create_network_capability(
            hosts=["example.com", "api.test.com"],
            ports=[80, 443],
            operations={"http", "https"}
        )

        assert token.capability_type == "network"
        assert token.constraints.allowed_operations == {"http", "https"}
        assert token.constraints.allowed_hosts == ["example.com", "api.test.com"]
        assert token.constraints.allowed_ports == [80, 443]

    def test_token_with_expiration(self):
        """Test token creation with expiration."""
        token = create_capability_token(
            capability_type="test",
            expires_in=timedelta(hours=1)
        )

        assert not token.constraints.is_expired()
        assert token.constraints.expires_at is not None

        # Check expiration is in the future
        assert token.constraints.expires_at > datetime.now()


if __name__ == "__main__":
    pytest.main([__file__])