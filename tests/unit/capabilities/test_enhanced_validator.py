"""Tests for enhanced capability validator."""

import pytest
import re
import time
from unittest.mock import Mock, MagicMock

from mlpy.runtime.capabilities.enhanced_validator import (
    EnhancedCapabilityValidator,
    ValidationResult,
    ValidationContext,
    SecurityViolation,
    ValidationPolicy,
)
from mlpy.runtime.capabilities.context import CapabilityContext


class TestValidationEnums:
    """Test validation result enum."""

    def test_validation_result_values(self):
        """Test ValidationResult enum values."""
        assert ValidationResult.ALLOWED.value == "allowed"
        assert ValidationResult.DENIED.value == "denied"
        assert ValidationResult.REQUIRES_ELEVATION.value == "requires_elevation"
        assert ValidationResult.SUSPICIOUS.value == "suspicious"
        assert ValidationResult.BLOCKED.value == "blocked"


class TestValidationContext:
    """Test ValidationContext dataclass."""

    def test_validation_context_creation(self):
        """Test creating validation context."""
        ctx = ValidationContext(
            operation="read",
            resource_path="/tmp/test.txt",
            capability_type="file",
            user_context="test_user"
        )

        assert ctx.operation == "read"
        assert ctx.resource_path == "/tmp/test.txt"
        assert ctx.capability_type == "file"
        assert ctx.user_context == "test_user"
        assert isinstance(ctx.timestamp, float)
        assert isinstance(ctx.metadata, dict)


class TestSecurityViolation:
    """Test SecurityViolation dataclass."""

    def test_security_violation_creation(self):
        """Test creating security violation."""
        violation = SecurityViolation(
            severity="high",
            message="Access denied",
            location="/etc/shadow",
            recommendation="Remove sensitive file access"
        )

        assert violation.severity == "high"
        assert violation.message == "Access denied"
        assert violation.location == "/etc/shadow"
        assert violation.recommendation == "Remove sensitive file access"
        assert violation.blocked is True


class TestValidationPolicy:
    """Test ValidationPolicy dataclass."""

    def test_validation_policy_creation(self):
        """Test creating validation policy."""
        policy = ValidationPolicy(
            name="test_policy",
            capability_types={"file", "file_read"},
            allowed_patterns=[re.compile(r"^/tmp/.*")],
            blocked_patterns=[re.compile(r"^/etc/.*")],
            max_usage_count=100,
            monitoring_level="normal"
        )

        assert policy.name == "test_policy"
        assert "file" in policy.capability_types
        assert policy.max_usage_count == 100
        assert policy.monitoring_level == "normal"


class TestEnhancedCapabilityValidator:
    """Test EnhancedCapabilityValidator class."""

    def test_validator_initialization(self):
        """Test validator initializes with default policies."""
        validator = EnhancedCapabilityValidator()

        assert len(validator.policies) > 0
        assert "file_access" in validator.policies
        assert "network_access" in validator.policies
        assert "system_access" in validator.policies
        assert validator.stats["validations_performed"] == 0

    def test_validator_with_resource_monitor(self):
        """Test validator with resource monitor."""
        monitor = Mock()
        validator = EnhancedCapabilityValidator(resource_monitor=monitor)

        assert validator.resource_monitor is monitor

    def test_add_policy(self):
        """Test adding custom policy."""
        validator = EnhancedCapabilityValidator()
        policy = ValidationPolicy(
            name="custom_policy",
            capability_types={"custom"},
            allowed_patterns=[re.compile(r".*")],
            blocked_patterns=[]
        )

        validator.add_policy(policy)
        assert "custom_policy" in validator.policies

    def test_file_policy_allows_tmp_directory(self):
        """Test file policy allows /tmp directory."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        # Mock token with usage_count
        token_mock = Mock()
        token_mock.usage_count = 0
        context.get_capability_token.return_value = token_mock

        result, violation = validator.validate_capability(
            context,
            capability_type="file",
            resource_path="/tmp/test.txt",
            operation="read"
        )

        assert result == ValidationResult.ALLOWED
        assert violation is None

    def test_file_policy_blocks_etc_directory(self):
        """Test file policy blocks /etc directory."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        result, violation = validator.validate_capability(
            context,
            capability_type="file",
            resource_path="/etc/passwd",
            operation="read"
        )

        assert result == ValidationResult.BLOCKED
        assert violation is not None
        assert violation.severity == "high"  # Implementation uses "high" for blocked patterns

    def test_file_policy_blocks_path_traversal(self):
        """Test file policy blocks path traversal."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        result, violation = validator.validate_capability(
            context,
            capability_type="file",
            resource_path="/tmp/../etc/passwd",
            operation="read"
        )

        assert result == ValidationResult.BLOCKED

    def test_network_policy_allows_https(self):
        """Test network policy allows HTTPS."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        # Mock token with usage_count
        token_mock = Mock()
        token_mock.usage_count = 0
        context.get_capability_token.return_value = token_mock

        result, violation = validator.validate_capability(
            context,
            capability_type="network",
            resource_path="https://example.com/api",
            operation="connect"
        )

        assert result == ValidationResult.ALLOWED

    def test_network_policy_blocks_localhost(self):
        """Test network policy blocks localhost."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        result, violation = validator.validate_capability(
            context,
            capability_type="network",
            resource_path="https://localhost/admin",
            operation="connect"
        )

        assert result == ValidationResult.BLOCKED

    def test_network_policy_blocks_private_networks(self):
        """Test network policy blocks private networks."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        result, violation = validator.validate_capability(
            context,
            capability_type="network",
            resource_path="https://192.168.1.1/",
            operation="connect"
        )

        assert result == ValidationResult.BLOCKED

    def test_system_policy_blocks_shell_access(self):
        """Test system policy blocks shell access."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        result, violation = validator.validate_capability(
            context,
            capability_type="subprocess",
            resource_path="/bin/bash",
            operation="execute"
        )

        assert result == ValidationResult.BLOCKED

    def test_missing_capability_denied(self):
        """Test request denied when capability missing."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = False

        result, violation = validator.validate_capability(
            context,
            capability_type="file",
            resource_path="/tmp/test.txt",
            operation="read"
        )

        assert result == ValidationResult.DENIED
        assert violation is not None
        assert "Missing capability" in violation.message

    def test_validation_caching(self):
        """Test validation results are cached."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        # Mock token with usage_count
        token_mock = Mock()
        token_mock.usage_count = 0
        context.get_capability_token.return_value = token_mock

        # First call
        validator.validate_capability(
            context,
            capability_type="file",
            resource_path="/tmp/test.txt",
            operation="read"
        )

        cache_misses_before = validator.stats["cache_misses"]

        # Second call (should hit cache)
        validator.validate_capability(
            context,
            capability_type="file",
            resource_path="/tmp/test.txt",
            operation="read"
        )

        assert validator.stats["cache_hits"] > 0
        assert validator.stats["cache_misses"] == cache_misses_before

    def test_suspicious_pattern_detection_ssh_keys(self):
        """Test detection of suspicious SSH key access."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        # Mock token with usage_count
        token_mock = Mock()
        token_mock.usage_count = 0
        context.get_capability_token.return_value = token_mock

        result, violation = validator.validate_capability(
            context,
            capability_type="file",
            resource_path="/home/user/.ssh/id_rsa",
            operation="read"
        )

        # Should be flagged as suspicious
        assert result in [ValidationResult.SUSPICIOUS, ValidationResult.BLOCKED]

    def test_suspicious_pattern_detection_tor(self):
        """Test detection of suspicious Tor access."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        # Mock token with usage_count
        token_mock = Mock()
        token_mock.usage_count = 0
        context.get_capability_token.return_value = token_mock

        result, violation = validator.validate_capability(
            context,
            capability_type="network",
            resource_path="https://something.onion/",
            operation="connect"
        )

        assert result in [ValidationResult.SUSPICIOUS, ValidationResult.BLOCKED]

    def test_statistics_tracking(self):
        """Test validator tracks statistics."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        # Mock token with usage_count
        token_mock = Mock()
        token_mock.usage_count = 0
        context.get_capability_token.return_value = token_mock

        initial_validations = validator.stats["validations_performed"]

        validator.validate_capability(
            context,
            capability_type="file",
            resource_path="/tmp/test.txt",
            operation="read"
        )

        assert validator.stats["validations_performed"] == initial_validations + 1

    def test_violation_history(self):
        """Test violations are recorded in history."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        validator.validate_capability(
            context,
            capability_type="file",
            resource_path="/etc/shadow",
            operation="read"
        )

        assert len(validator.violation_history) > 0

    def test_thread_safety_locks(self):
        """Test validator has thread safety locks."""
        validator = EnhancedCapabilityValidator()

        assert hasattr(validator, '_lock')
        assert hasattr(validator, '_cache_lock')

    def test_windows_path_support(self):
        """Test Windows path validation."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        # Mock token with usage_count
        token_mock = Mock()
        token_mock.usage_count = 0
        context.get_capability_token.return_value = token_mock

        # Windows user path should be allowed
        result, _ = validator.validate_capability(
            context,
            capability_type="file",
            resource_path="C:\\Users\\testuser\\Documents\\file.txt",
            operation="read"
        )

        assert result == ValidationResult.ALLOWED

    def test_windows_system_path_blocked(self):
        """Test Windows system path is blocked."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        result, _ = validator.validate_capability(
            context,
            capability_type="file",
            resource_path="C:\\Windows\\System32\\config\\SAM",
            operation="read"
        )

        assert result == ValidationResult.BLOCKED


class TestValidatorIntegration:
    """Test validator integration scenarios."""

    def test_multiple_validations(self):
        """Test multiple sequential validations."""
        validator = EnhancedCapabilityValidator()
        context = Mock()
        context.has_capability.return_value = True

        # Mock token with usage_count
        token_mock = Mock()
        token_mock.usage_count = 0
        context.get_capability_token.return_value = token_mock

        paths = [
            "/tmp/file1.txt",
            "/tmp/file2.txt",
            "/tmp/file3.txt",
        ]

        for path in paths:
            result, _ = validator.validate_capability(
                context,
                capability_type="file",
                resource_path=path,
                operation="read"
            )
            assert result == ValidationResult.ALLOWED

    def test_policy_override(self):
        """Test adding policy overrides default."""
        validator = EnhancedCapabilityValidator()

        # Add stricter policy
        strict_policy = ValidationPolicy(
            name="file_access",  # Override default
            capability_types={"file"},
            allowed_patterns=[],
            blocked_patterns=[re.compile(r".*")],  # Block everything
        )
        validator.add_policy(strict_policy)

        context = Mock()
        context.has_capability.return_value = True

        result, _ = validator.validate_capability(
            context,
            capability_type="file",
            resource_path="/tmp/test.txt",
            operation="read"
        )

        assert result == ValidationResult.BLOCKED
