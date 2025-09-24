"""Capability token implementation with UUID-based identity and constraint validation."""

import fnmatch
import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from .exceptions import CapabilityExpiredError, CapabilityValidationError


@dataclass
class CapabilityConstraint:
    """Represents a constraint on capability usage."""

    # Resource pattern matching
    resource_patterns: list[str] = field(default_factory=list)

    # Permission levels
    allowed_operations: set[str] = field(default_factory=set)

    # Time constraints
    max_usage_count: int | None = None
    expires_at: datetime | None = None

    # Resource limits
    max_file_size: int | None = None  # bytes
    max_memory: int | None = None  # bytes
    max_cpu_time: float | None = None  # seconds

    # Network constraints
    allowed_hosts: list[str] = field(default_factory=list)
    allowed_ports: list[int] = field(default_factory=list)

    def matches_resource(self, resource_path: str) -> bool:
        """Check if resource path matches any of the patterns."""
        if not self.resource_patterns:
            return True  # No restrictions

        return any(fnmatch.fnmatch(resource_path, pattern) for pattern in self.resource_patterns)

    def allows_operation(self, operation: str) -> bool:
        """Check if operation is allowed."""
        if not self.allowed_operations:
            return True  # No restrictions

        return operation in self.allowed_operations

    def is_expired(self) -> bool:
        """Check if constraint is expired."""
        if self.expires_at is None:
            return False

        return datetime.now() > self.expires_at


@dataclass
class CapabilityToken:
    """A capability token that grants specific permissions with constraints."""

    # Core identity
    token_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    capability_type: str = ""

    # Constraints and permissions
    constraints: CapabilityConstraint = field(default_factory=CapabilityConstraint)

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    description: str = ""

    # Usage tracking
    usage_count: int = 0
    last_used_at: datetime | None = None

    # Security
    _checksum: str | None = field(default=None, init=False)

    def __post_init__(self):
        """Initialize token after creation."""
        if self._checksum is None:
            self._checksum = self._calculate_checksum()

    def _calculate_checksum(self) -> str:
        """Calculate security checksum for token integrity."""
        token_data = {
            "token_id": self.token_id,
            "capability_type": self.capability_type,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "constraints": {
                "resource_patterns": sorted(self.constraints.resource_patterns),
                "allowed_operations": sorted(self.constraints.allowed_operations),
                "max_usage_count": self.constraints.max_usage_count,
                "expires_at": (
                    self.constraints.expires_at.isoformat() if self.constraints.expires_at else None
                ),
            },
        }

        token_json = json.dumps(token_data, sort_keys=True)
        return hashlib.sha256(token_json.encode()).hexdigest()

    def validate_integrity(self) -> bool:
        """Validate token hasn't been tampered with."""
        current_checksum = self._calculate_checksum()
        return current_checksum == self._checksum

    def is_valid(self) -> bool:
        """Check if token is valid for use."""
        # Check integrity
        if not self.validate_integrity():
            return False

        # Check expiration
        if self.constraints.is_expired():
            return False

        # Check usage count
        if (
            self.constraints.max_usage_count is not None
            and self.usage_count >= self.constraints.max_usage_count
        ):
            return False

        return True

    def can_access_resource(self, resource_path: str, operation: str) -> bool:
        """Check if token allows access to specific resource and operation."""
        if not self.is_valid():
            return False

        # Check resource pattern matching
        if not self.constraints.matches_resource(resource_path):
            return False

        # Check operation permission
        if not self.constraints.allows_operation(operation):
            return False

        return True

    def use_token(self, resource_path: str, operation: str) -> None:
        """Use the token for a specific resource access."""
        if not self.can_access_resource(resource_path, operation):
            if not self.is_valid():
                if self.constraints.is_expired():
                    raise CapabilityExpiredError(
                        self.capability_type,
                        (
                            self.constraints.expires_at.isoformat()
                            if self.constraints.expires_at
                            else "unknown"
                        ),
                    )
                else:
                    raise CapabilityValidationError("Token is invalid", self.token_id)
            else:
                raise CapabilityValidationError(
                    f"Access denied for resource '{resource_path}' with operation '{operation}'",
                    self.token_id,
                )

        # Record usage
        self.usage_count += 1
        self.last_used_at = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        """Convert token to dictionary for serialization."""
        return {
            "token_id": self.token_id,
            "capability_type": self.capability_type,
            "constraints": {
                "resource_patterns": self.constraints.resource_patterns,
                "allowed_operations": list(self.constraints.allowed_operations),
                "max_usage_count": self.constraints.max_usage_count,
                "expires_at": (
                    self.constraints.expires_at.isoformat() if self.constraints.expires_at else None
                ),
                "max_file_size": self.constraints.max_file_size,
                "max_memory": self.constraints.max_memory,
                "max_cpu_time": self.constraints.max_cpu_time,
                "allowed_hosts": self.constraints.allowed_hosts,
                "allowed_ports": self.constraints.allowed_ports,
            },
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "description": self.description,
            "usage_count": self.usage_count,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "checksum": self._checksum,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CapabilityToken":
        """Create token from dictionary."""
        constraints_data = data.get("constraints", {})
        constraints = CapabilityConstraint(
            resource_patterns=constraints_data.get("resource_patterns", []),
            allowed_operations=set(constraints_data.get("allowed_operations", [])),
            max_usage_count=constraints_data.get("max_usage_count"),
            expires_at=(
                datetime.fromisoformat(constraints_data["expires_at"])
                if constraints_data.get("expires_at")
                else None
            ),
            max_file_size=constraints_data.get("max_file_size"),
            max_memory=constraints_data.get("max_memory"),
            max_cpu_time=constraints_data.get("max_cpu_time"),
            allowed_hosts=constraints_data.get("allowed_hosts", []),
            allowed_ports=constraints_data.get("allowed_ports", []),
        )

        token = cls(
            token_id=data["token_id"],
            capability_type=data["capability_type"],
            constraints=constraints,
            created_at=datetime.fromisoformat(data["created_at"]),
            created_by=data.get("created_by", "system"),
            description=data.get("description", ""),
            usage_count=data.get("usage_count", 0),
            last_used_at=(
                datetime.fromisoformat(data["last_used_at"]) if data.get("last_used_at") else None
            ),
        )

        # Validate checksum
        expected_checksum = data.get("checksum")
        if expected_checksum and token._checksum != expected_checksum:
            raise CapabilityValidationError("Token checksum validation failed", token.token_id)

        return token


def create_capability_token(
    capability_type: str,
    resource_patterns: list[str] | None = None,
    allowed_operations: set[str] | None = None,
    expires_in: timedelta | None = None,
    max_usage_count: int | None = None,
    description: str = "",
    **kwargs,
) -> CapabilityToken:
    """Create a new capability token with specified constraints.

    Args:
        capability_type: Type of capability (e.g., "file.read", "network.http")
        resource_patterns: List of glob patterns for allowed resources
        allowed_operations: Set of allowed operations
        expires_in: Token expiration time from now
        max_usage_count: Maximum number of times token can be used
        description: Human-readable description
        **kwargs: Additional constraint parameters

    Returns:
        New CapabilityToken instance
    """
    constraints = CapabilityConstraint(
        resource_patterns=resource_patterns or [],
        allowed_operations=allowed_operations or set(),
        max_usage_count=max_usage_count,
        expires_at=datetime.now() + expires_in if expires_in else None,
        max_file_size=kwargs.get("max_file_size"),
        max_memory=kwargs.get("max_memory"),
        max_cpu_time=kwargs.get("max_cpu_time"),
        allowed_hosts=kwargs.get("allowed_hosts", []),
        allowed_ports=kwargs.get("allowed_ports", []),
    )

    return CapabilityToken(
        capability_type=capability_type,
        constraints=constraints,
        description=description,
        created_by=kwargs.get("created_by", "system"),
    )


def create_file_capability(
    patterns: list[str], operations: set[str] = None, max_file_size: int | None = None, **kwargs
) -> CapabilityToken:
    """Create a file access capability token."""
    return create_capability_token(
        capability_type="file",
        resource_patterns=patterns,
        allowed_operations=operations or {"read", "write"},
        max_file_size=max_file_size,
        **kwargs,
    )


def create_network_capability(
    hosts: list[str], ports: list[int] = None, operations: set[str] = None, **kwargs
) -> CapabilityToken:
    """Create a network access capability token."""
    return create_capability_token(
        capability_type="network",
        allowed_operations=operations or {"http", "https"},
        allowed_hosts=hosts,
        allowed_ports=ports or [80, 443],
        **kwargs,
    )
