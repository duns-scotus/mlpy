"""Enhanced capability validation system with advanced security checks."""

import ipaddress
import re
import threading
import time
import urllib.parse
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from re import Pattern
from typing import Any

from ..sandbox.resource_monitor import ResourceMonitor
from .context import CapabilityContext


class ValidationResult(Enum):
    """Result of capability validation."""

    ALLOWED = "allowed"
    DENIED = "denied"
    REQUIRES_ELEVATION = "requires_elevation"
    SUSPICIOUS = "suspicious"
    BLOCKED = "blocked"


@dataclass
class ValidationContext:
    """Context for capability validation."""

    operation: str
    resource_path: str
    capability_type: str
    user_context: str
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityViolation:
    """Security violation detected during validation."""

    severity: str
    message: str
    location: str
    recommendation: str
    blocked: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationPolicy:
    """Policy for capability validation."""

    name: str
    capability_types: set[str]
    allowed_patterns: list[Pattern[str]]
    blocked_patterns: list[Pattern[str]]
    max_usage_count: int | None = None
    time_restrictions: dict[str, Any] | None = None
    elevation_required: bool = False
    monitoring_level: str = "normal"  # none, normal, strict


class EnhancedCapabilityValidator:
    """Enhanced capability validator with advanced security features."""

    def __init__(self, resource_monitor: ResourceMonitor | None = None):
        """Initialize the enhanced validator."""
        self.resource_monitor = resource_monitor
        self.policies: dict[str, ValidationPolicy] = {}
        self.violation_history: list[SecurityViolation] = []
        self.validation_cache: dict[str, tuple[ValidationResult, float]] = {}
        self.suspicious_patterns: dict[str, list[Pattern[str]]] = {}

        # Thread safety
        self._lock = threading.RLock()
        self._cache_lock = threading.RLock()

        # Statistics
        self.stats = {
            "validations_performed": 0,
            "validations_allowed": 0,
            "validations_denied": 0,
            "security_violations": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }

        # Initialize default policies and patterns
        self._initialize_default_policies()
        self._initialize_suspicious_patterns()

    def _initialize_default_policies(self) -> None:
        """Initialize default validation policies."""
        # File access policy
        file_policy = ValidationPolicy(
            name="file_access",
            capability_types={"file", "file_read", "file_write"},
            allowed_patterns=[
                re.compile(r"^/tmp/.*"),
                re.compile(r"^/home/[^/]+/.*"),
                re.compile(r"^\.(/.*)?$"),
                re.compile(r"^[a-zA-Z]:\\Users\\[^\\]+\\.*"),  # Windows paths
            ],
            blocked_patterns=[
                re.compile(r"^/etc/.*"),
                re.compile(r"^/root/.*"),
                re.compile(r"^/boot/.*"),
                re.compile(r"^/proc/.*"),
                re.compile(r"^/sys/.*"),
                re.compile(r".*\.\./.*"),  # Path traversal
                re.compile(r"^[a-zA-Z]:\\Windows\\.*"),  # Windows system
                re.compile(r"^[a-zA-Z]:\\Program Files\\.*"),  # Windows programs
            ],
            max_usage_count=1000,
            monitoring_level="normal",
        )
        self.add_policy(file_policy)

        # Network access policy
        network_policy = ValidationPolicy(
            name="network_access",
            capability_types={"network", "http", "socket"},
            allowed_patterns=[
                re.compile(r"^https?://[a-zA-Z0-9.-]+/.*"),
                re.compile(r"^[a-zA-Z0-9.-]+:[0-9]+$"),
            ],
            blocked_patterns=[
                re.compile(r"^https?://localhost/.*"),
                re.compile(r"^https?://127\.0\.0\.1/.*"),
                re.compile(r"^https?://0\.0\.0\.0/.*"),
                re.compile(r"^https?://10\.[0-9.]+/.*"),  # Private networks
                re.compile(r"^https?://192\.168\.[0-9.]+/.*"),
                re.compile(r".*:[1-9][0-9]{4,}$"),  # High ports (potential backdoors)
            ],
            max_usage_count=100,
            monitoring_level="strict",
        )
        self.add_policy(network_policy)

        # System access policy (high security)
        system_policy = ValidationPolicy(
            name="system_access",
            capability_types={"system", "subprocess", "environment"},
            allowed_patterns=[
                re.compile(r"^/usr/bin/[a-zA-Z0-9_-]+$"),
                re.compile(r"^/bin/[a-zA-Z0-9_-]+$"),
            ],
            blocked_patterns=[
                re.compile(r".*sh$"),  # Shell access
                re.compile(r".*bash$"),
                re.compile(r".*zsh$"),
                re.compile(r".*cmd\.exe$"),
                re.compile(r".*powershell\.exe$"),
                re.compile(r".*rm\s+-rf.*"),  # Dangerous commands
                re.compile(r".*sudo.*"),
                re.compile(r".*su\s+.*"),
            ],
            elevation_required=True,
            monitoring_level="strict",
        )
        self.add_policy(system_policy)

    def _initialize_suspicious_patterns(self) -> None:
        """Initialize patterns for detecting suspicious activity."""
        # File access suspicious patterns
        self.suspicious_patterns["file"] = [
            re.compile(r".*\.ssh/.*"),  # SSH keys
            re.compile(r".*\.gnupg/.*"),  # GPG keys
            re.compile(r".*wallet\.dat$"),  # Cryptocurrency wallets
            re.compile(r".*\.pem$"),  # Certificate files
            re.compile(r".*\.key$"),  # Key files
            re.compile(r".*/shadow$"),  # Password files
            re.compile(r".*/passwd$"),
            re.compile(r".*config.*"),  # Config files
        ]

        # Network suspicious patterns
        self.suspicious_patterns["network"] = [
            re.compile(r".*\.onion/.*"),  # Tor hidden services
            re.compile(r".*malware.*"),  # Malware-related domains
            re.compile(r".*phishing.*"),
            re.compile(r".*:6667$"),  # IRC (potential C&C)
            re.compile(r".*:1337$"),  # Common hacker port
            re.compile(r".*:31337$"),  # Elite hacker port
        ]

        # System suspicious patterns
        self.suspicious_patterns["system"] = [
            re.compile(r".*keylogger.*"),
            re.compile(r".*backdoor.*"),
            re.compile(r".*rootkit.*"),
            re.compile(r".*stealer.*"),
            re.compile(r".*ransomware.*"),
        ]

    def add_policy(self, policy: ValidationPolicy) -> None:
        """Add a validation policy."""
        with self._lock:
            self.policies[policy.name] = policy

    def validate_capability(
        self,
        context: CapabilityContext,
        capability_type: str,
        resource_path: str,
        operation: str,
        user_context: str = "unknown",
    ) -> tuple[ValidationResult, SecurityViolation | None]:
        """Validate a capability request with enhanced security checks."""
        validation_ctx = ValidationContext(
            operation=operation,
            resource_path=resource_path,
            capability_type=capability_type,
            user_context=user_context,
        )

        # Check cache first
        cache_key = f"{capability_type}:{resource_path}:{operation}"
        with self._cache_lock:
            if cache_key in self.validation_cache:
                result, timestamp = self.validation_cache[cache_key]
                if time.time() - timestamp < 30:  # 30-second cache
                    self.stats["cache_hits"] += 1
                    return result, None

            self.stats["cache_misses"] += 1

        # Perform validation
        with self._lock:
            self.stats["validations_performed"] += 1

            # Step 1: Check if context has the capability
            if not context.has_capability(capability_type):
                violation = SecurityViolation(
                    severity="high",
                    message=f"Missing capability: {capability_type}",
                    location=resource_path,
                    recommendation=f"Add {capability_type} capability token to context",
                )
                self._record_violation(violation)
                result = ValidationResult.DENIED
            else:
                # Step 2: Validate against policies
                result, violation = self._validate_against_policies(validation_ctx, context)

            # Step 3: Check for suspicious patterns
            if result == ValidationResult.ALLOWED:
                suspicion_level = self._check_suspicious_patterns(validation_ctx)
                if suspicion_level > 0.7:
                    result = ValidationResult.SUSPICIOUS
                    violation = SecurityViolation(
                        severity="medium",
                        message=f"Suspicious activity detected: {capability_type} access to {resource_path}",
                        location=resource_path,
                        recommendation="Review resource access patterns",
                        blocked=False,
                    )

            # Step 4: Apply resource monitoring if available
            if self.resource_monitor and result == ValidationResult.ALLOWED:
                if not self._check_resource_limits(validation_ctx):
                    result = ValidationResult.DENIED
                    violation = SecurityViolation(
                        severity="high",
                        message="Resource limits exceeded",
                        location=resource_path,
                        recommendation="Reduce resource usage or increase limits",
                    )

            # Update statistics
            if result == ValidationResult.ALLOWED:
                self.stats["validations_allowed"] += 1
            else:
                self.stats["validations_denied"] += 1

            # Cache the result
            with self._cache_lock:
                self.validation_cache[cache_key] = (result, time.time())

            return result, violation

    def _validate_against_policies(
        self, ctx: ValidationContext, capability_context: CapabilityContext
    ) -> tuple[ValidationResult, SecurityViolation | None]:
        """Validate request against configured policies."""
        applicable_policies = [
            policy
            for policy in self.policies.values()
            if ctx.capability_type in policy.capability_types
        ]

        if not applicable_policies:
            # No specific policy - use basic validation
            return ValidationResult.ALLOWED, None

        for policy in applicable_policies:
            # Check blocked patterns first
            for pattern in policy.blocked_patterns:
                if pattern.search(ctx.resource_path):
                    violation = SecurityViolation(
                        severity="high",
                        message=f"Access blocked by policy {policy.name}: {ctx.resource_path}",
                        location=ctx.resource_path,
                        recommendation=f"Resource matches blocked pattern in {policy.name} policy",
                    )
                    return ValidationResult.BLOCKED, violation

            # Check allowed patterns
            allowed = False
            for pattern in policy.allowed_patterns:
                if pattern.search(ctx.resource_path):
                    allowed = True
                    break

            if not allowed and policy.allowed_patterns:
                violation = SecurityViolation(
                    severity="medium",
                    message=f"Access denied by policy {policy.name}: {ctx.resource_path}",
                    location=ctx.resource_path,
                    recommendation=f"Resource does not match allowed patterns in {policy.name} policy",
                )
                return ValidationResult.DENIED, violation

            # Check usage limits
            if policy.max_usage_count:
                token = capability_context.get_capability_token(ctx.capability_type)
                if token and token.usage_count >= policy.max_usage_count:
                    violation = SecurityViolation(
                        severity="medium",
                        message=f"Usage limit exceeded for {ctx.capability_type}",
                        location=ctx.resource_path,
                        recommendation="Reset usage count or increase limit",
                    )
                    return ValidationResult.DENIED, violation

            # Check if elevation is required
            if policy.elevation_required:
                return ValidationResult.REQUIRES_ELEVATION, None

        return ValidationResult.ALLOWED, None

    def _check_suspicious_patterns(self, ctx: ValidationContext) -> float:
        """Check for suspicious patterns and return suspicion level (0.0-1.0)."""
        suspicion_score = 0.0

        patterns = self.suspicious_patterns.get(ctx.capability_type, [])
        for pattern in patterns:
            if pattern.search(ctx.resource_path):
                suspicion_score += 0.3

        # Check for other suspicious indicators
        if ".." in ctx.resource_path:  # Path traversal
            suspicion_score += 0.4

        if any(
            term in ctx.resource_path.lower() for term in ["password", "secret", "key", "token"]
        ):
            suspicion_score += 0.3

        if ctx.operation == "write" and any(
            ext in ctx.resource_path.lower() for ext in [".exe", ".bat", ".sh"]
        ):
            suspicion_score += 0.5

        return min(1.0, suspicion_score)

    def _check_resource_limits(self, ctx: ValidationContext) -> bool:
        """Check resource limits using resource monitor."""
        if not self.resource_monitor:
            return True

        try:
            # Simulate resource usage for this operation
            estimated_usage = {
                "memory": 1024 * 1024,  # 1MB per operation
                "cpu_time": 0.1,  # 100ms per operation
                "file_handles": 1 if ctx.capability_type == "file" else 0,
                "network_connections": 1 if ctx.capability_type == "network" else 0,
            }

            self.resource_monitor._enforce_limits(estimated_usage)
            return True

        except Exception:
            return False

    def _record_violation(self, violation: SecurityViolation) -> None:
        """Record a security violation."""
        self.violation_history.append(violation)
        self.stats["security_violations"] += 1

        # Keep only recent violations (last 1000)
        if len(self.violation_history) > 1000:
            self.violation_history = self.violation_history[-1000:]

    def validate_file_path(self, file_path: str, operation: str) -> tuple[bool, str | None]:
        """Validate file path for security issues."""
        path_obj = Path(file_path)

        # Check for path traversal
        if ".." in str(path_obj):
            return False, "Path traversal detected"

        # Check for absolute paths outside allowed directories
        if path_obj.is_absolute():
            allowed_roots = ["/tmp", "/home", "/var/tmp"]
            if not any(str(path_obj).startswith(root) for root in allowed_roots):
                return False, f"Absolute path outside allowed directories: {file_path}"

        # Check for suspicious file extensions
        suspicious_extensions = {".exe", ".bat", ".cmd", ".ps1", ".sh", ".py", ".pl"}
        if operation == "write" and path_obj.suffix.lower() in suspicious_extensions:
            return False, f"Writing executable file: {path_obj.suffix}"

        # Check for system files
        system_patterns = [
            r"/etc/.*",
            r"/root/.*",
            r"/boot/.*",
            r"/proc/.*",
            r"/sys/.*",
            r"C:\\Windows\\.*",
            r"C:\\Program Files\\.*",
        ]

        for pattern in system_patterns:
            if re.match(pattern, str(path_obj), re.IGNORECASE):
                return False, f"Access to system directory: {file_path}"

        return True, None

    def validate_network_target(self, target: str) -> tuple[bool, str | None]:
        """Validate network target for security issues."""
        try:
            # Parse URL or host:port
            if "://" in target:
                parsed = urllib.parse.urlparse(target)
                host = parsed.hostname
                port = parsed.port or (443 if parsed.scheme == "https" else 80)
            else:
                if ":" in target:
                    host, port_str = target.rsplit(":", 1)
                    port = int(port_str)
                else:
                    host = target
                    port = 80

            # Check for localhost/private networks
            if host in ["localhost", "127.0.0.1", "0.0.0.0"]:
                return False, "Access to localhost blocked"

            try:
                ip = ipaddress.ip_address(host)
                if ip.is_private:
                    return False, f"Access to private network blocked: {host}"
                if ip.is_loopback:
                    return False, f"Access to loopback address blocked: {host}"
            except ValueError:
                # Not an IP address, check domain patterns
                pass

            # Check for suspicious ports
            suspicious_ports = {22, 23, 135, 445, 1337, 31337, 6667}
            if port in suspicious_ports:
                return False, f"Access to suspicious port blocked: {port}"

            # Check for high ports (potential backdoors)
            if port > 10000:
                return False, f"Access to high port blocked: {port}"

            return True, None

        except Exception as e:
            return False, f"Invalid network target: {e}"

    def get_security_report(self) -> dict[str, Any]:
        """Generate security report."""
        with self._lock:
            recent_violations = [
                v
                for v in self.violation_history
                if time.time() - v.metadata.get("timestamp", 0) < 3600  # Last hour
            ]

            violation_by_severity = {}
            for violation in recent_violations:
                severity = violation.severity
                violation_by_severity[severity] = violation_by_severity.get(severity, 0) + 1

            return {
                "statistics": self.stats.copy(),
                "recent_violations": len(recent_violations),
                "violations_by_severity": violation_by_severity,
                "policies": len(self.policies),
                "cache_hit_rate": (
                    self.stats["cache_hits"]
                    / (self.stats["cache_hits"] + self.stats["cache_misses"])
                    if (self.stats["cache_hits"] + self.stats["cache_misses"]) > 0
                    else 0.0
                ),
                "top_violations": [
                    {"severity": v.severity, "message": v.message, "location": v.location}
                    for v in recent_violations[:10]
                ],
            }

    def clear_cache(self) -> None:
        """Clear validation cache."""
        with self._cache_lock:
            self.validation_cache.clear()

    def reset_stats(self) -> None:
        """Reset statistics."""
        with self._lock:
            self.stats = {
                "validations_performed": 0,
                "validations_allowed": 0,
                "validations_denied": 0,
                "security_violations": 0,
                "cache_hits": 0,
                "cache_misses": 0,
            }

    def create_custom_policy(
        self,
        name: str,
        capability_types: set[str],
        allowed_patterns: list[str],
        blocked_patterns: list[str],
        **kwargs,
    ) -> ValidationPolicy:
        """Create a custom validation policy."""
        allowed_regex = [re.compile(pattern) for pattern in allowed_patterns]
        blocked_regex = [re.compile(pattern) for pattern in blocked_patterns]

        policy = ValidationPolicy(
            name=name,
            capability_types=capability_types,
            allowed_patterns=allowed_regex,
            blocked_patterns=blocked_regex,
            **kwargs,
        )

        self.add_policy(policy)
        return policy
