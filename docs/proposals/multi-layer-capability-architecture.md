# Multi-Layer Capability Security Architecture

**Author:** Claude Code + User Specification
**Date:** October 2025
**Status:** Architectural Proposal
**Category:** Security Infrastructure

---

## Executive Summary

This document proposes a comprehensive multi-layer capability-based security system for mlpy with clear separation of concerns:

1. **Administrator Layer** - Grants capabilities to users/groups
2. **Sandbox Startup Layer** - Validates user authorization and initializes capability context
3. **Standard Library Layer** - Capability-aware implementations of sensitive operations
4. **ML Program Layer** - Declares usage, enforced and logged by runtime

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ADMINISTRATOR LAYER                       │
│  - Defines security policies                                │
│  - Grants capabilities to users/groups                      │
│  - Manages authorization rules                              │
└────────────────────┬────────────────────────────────────────┘
                     │ grants capabilities
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                  SANDBOX STARTUP LAYER                       │
│  - Authenticates user identity                              │
│  - Loads user's authorized capabilities                     │
│  - Creates restricted execution context                     │
└────────────────────┬────────────────────────────────────────┘
                     │ initializes stdlib with capabilities
                     ↓
┌─────────────────────────────────────────────────────────────┐
│               STANDARD LIBRARY LAYER                         │
│  - Capability-aware I/O operations                          │
│  - Capability-aware Network access                          │
│  - Capability-aware Database operations                     │
│  - Capability-aware Module imports                          │
└────────────────────┬────────────────────────────────────────┘
                     │ enforces capabilities
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                    ML PROGRAM LAYER                          │
│  - Declares capability requirements                         │
│  - Runtime validates against granted capabilities           │
│  - All operations logged and audited                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Administrator Layer

### Purpose
Define security policies and grant capabilities to users/groups/roles.

### Components

#### 1.1 Policy Definition Files

**Location:** `/etc/mlpy/policies/` or project-specific `.mlpy/policies/`

**Format Options:**

**Option A: YAML Policy Files**
```yaml
# /etc/mlpy/policies/data_scientist.yaml
policy:
  name: "Data Scientist Role"
  version: "1.0"

  # User/Group Assignment
  applies_to:
    users: ["alice", "bob"]
    groups: ["data_team", "analytics"]

  # Granted Capabilities
  capabilities:
    file:
      - patterns: ["data/*.csv", "data/*.json", "output/*.txt"]
        operations: [read, write]
        max_file_size: 10485760  # 10MB

    network:
      - hosts: ["api.internal.company.com"]
        operations: [https]
        ports: [443]
        rate_limit: 100  # requests per minute

    database:
      - connections: ["postgresql://analytics-db/"]
        operations: [select, insert]
        max_rows: 10000

    imports:
      - modules: ["pandas", "numpy", "sklearn"]
        stdlib_only: false

  # Resource Limits
  limits:
    max_memory: 2147483648  # 2GB
    max_cpu_time: 3600      # 1 hour
    max_processes: 4

  # Audit Settings
  audit:
    log_all_operations: true
    log_level: "INFO"
```

**Option B: Python Policy DSL**
```python
# /etc/mlpy/policies/untrusted_user.py
from mlpy.security import Policy, FileCapability, NetworkCapability

policy = Policy(name="Untrusted User")

# User assignment
policy.applies_to(
    users=["guest"],
    groups=["untrusted"]
)

# File access - highly restricted
policy.grant(
    FileCapability(
        patterns=["tmp/*.txt"],
        operations={"read"},
        max_file_size=1024*1024  # 1MB
    )
)

# No network access for untrusted users
# (nothing granted = denied by default)

# Limited stdlib imports only
policy.grant(
    ImportCapability(
        modules=["math", "string"],
        stdlib_only=True
    )
)

# Strict resource limits
policy.set_limits(
    max_memory=256*1024*1024,  # 256MB
    max_cpu_time=60,           # 1 minute
    max_processes=1
)
```

#### 1.2 Policy Management Tools

**CLI Administration:**
```bash
# List policies
mlpy-admin policy list

# View policy details
mlpy-admin policy show data_scientist

# Create new policy
mlpy-admin policy create researcher --template data_scientist

# Grant policy to user
mlpy-admin grant data_scientist --user alice

# Revoke policy from user
mlpy-admin revoke data_scientist --user alice

# Test policy against ML program
mlpy-admin policy test data_scientist script.ml
```

**Programmatic API:**
```python
from mlpy.admin import PolicyManager

manager = PolicyManager()

# Load policy
policy = manager.load_policy("data_scientist")

# Assign to user
manager.assign_policy(policy, user="alice")

# Check user's capabilities
caps = manager.get_user_capabilities("alice")
print(caps.can_access("file", "data/users.csv", "read"))  # True/False
```

---

## Layer 2: Sandbox Startup Layer

### Purpose
Authenticate user, load authorized capabilities, create restricted execution context.

### 2.1 Authentication Mechanisms

**Option A: OS-Level Authentication**
```python
import os
import pwd

class OSAuthenticator:
    """Authenticate using OS user credentials."""

    def authenticate(self) -> User:
        # Get current OS user
        uid = os.getuid()
        user_info = pwd.getpwuid(uid)

        return User(
            username=user_info.pw_name,
            uid=uid,
            groups=os.getgroups()
        )
```

**Option B: Token-Based Authentication**
```python
class TokenAuthenticator:
    """Authenticate using JWT/API tokens."""

    def authenticate(self, token: str) -> User:
        # Verify JWT token
        claims = jwt.decode(token, SECRET_KEY)

        return User(
            username=claims["sub"],
            user_id=claims["user_id"],
            roles=claims.get("roles", [])
        )
```

**Option C: Certificate-Based Authentication**
```python
class CertAuthenticator:
    """Authenticate using X.509 certificates."""

    def authenticate(self, cert_path: str) -> User:
        cert = load_certificate(cert_path)

        if not verify_certificate(cert, CA_CERT):
            raise AuthenticationError("Invalid certificate")

        return User(
            username=cert.subject.common_name,
            organization=cert.subject.organization_name
        )
```

### 2.2 Capability Loading at Startup

```python
class SandboxInitializer:
    """Initialize sandbox with user-specific capabilities."""

    def __init__(self, policy_manager: PolicyManager):
        self.policy_manager = policy_manager

    def initialize_sandbox(self, user: User) -> SandboxContext:
        """Create sandbox context with user's capabilities."""

        # 1. Load all policies that apply to this user
        policies = self.policy_manager.get_applicable_policies(user)

        # 2. Merge capabilities from all policies
        merged_caps = self._merge_capabilities(policies)

        # 3. Create capability tokens
        tokens = []
        for cap_spec in merged_caps:
            token = create_capability_token(
                capability_type=cap_spec.type,
                resource_patterns=cap_spec.patterns,
                allowed_operations=cap_spec.operations,
                **cap_spec.constraints
            )
            tokens.append(token)

        # 4. Create sandbox context
        context = SandboxContext(
            user=user,
            capabilities=tokens,
            limits=self._merge_limits(policies),
            audit_config=self._merge_audit_config(policies)
        )

        # 5. Initialize audit logging
        self._setup_audit_logging(context)

        return context

    def _merge_capabilities(self, policies: list[Policy]) -> list[CapabilitySpec]:
        """Merge capabilities from multiple policies (union)."""
        merged = {}

        for policy in policies:
            for cap in policy.capabilities:
                key = (cap.type, tuple(cap.patterns))
                if key in merged:
                    # Merge operations (union)
                    merged[key].operations.update(cap.operations)
                else:
                    merged[key] = cap

        return list(merged.values())
```

### 2.3 Sandbox Execution Flow

```python
def execute_ml_program_secure(
    script_path: str,
    user: User | None = None,
    auth_token: str | None = None
) -> ExecutionResult:
    """Execute ML program with full security enforcement."""

    # 1. Authenticate user
    if user is None:
        authenticator = get_authenticator()
        user = authenticator.authenticate(auth_token)

    # 2. Initialize sandbox with user's capabilities
    initializer = SandboxInitializer(PolicyManager())
    sandbox_ctx = initializer.initialize_sandbox(user)

    # 3. Parse ML program to extract capability declarations
    ml_code = read_file(script_path)
    declared_caps = parse_ml_capability_declarations(ml_code)

    # 4. Validate declared vs granted capabilities
    validator = CapabilityValidator()
    validation_result = validator.validate(
        declared=declared_caps,
        granted=sandbox_ctx.capabilities
    )

    if not validation_result.valid:
        raise CapabilityDeniedError(
            f"Program requires capabilities not granted to user {user.username}",
            denied=validation_result.denied_capabilities
        )

    # 5. Execute in sandbox with granted capabilities
    with sandbox_ctx.create_execution_environment() as env:
        # Initialize stdlib with capabilities
        stdlib = initialize_capability_aware_stdlib(sandbox_ctx.capabilities)

        # Execute ML program
        result = env.execute(
            ml_code,
            stdlib=stdlib,
            audit_logger=sandbox_ctx.audit_logger
        )

    return result
```

---

## Layer 3: Standard Library Layer

### Purpose
Implement capability-aware versions of sensitive operations (I/O, Network, Database, Imports).

### 3.1 Capability-Aware File I/O

```python
# src/mlpy/stdlib/secure_file_bridge.py

from mlpy.runtime.capabilities import requires_capability, get_current_context

class SecureFileOperations:
    """Capability-aware file operations."""

    @requires_capability("file", auto_use=False)
    def read(self, path: str) -> str:
        """Read file with capability enforcement."""
        context = get_current_context()

        # Check and use capability
        if not context.can_access_resource("file", path, "read"):
            raise PermissionError(f"No capability to read {path}")

        context.use_capability("file", path, "read")

        # Log the operation
        audit_log.info(f"File read: {path}", user=context.user)

        # Perform operation
        with open(path, 'r') as f:
            return f.read()

    @requires_capability("file", auto_use=False)
    def write(self, path: str, content: str) -> None:
        """Write file with capability enforcement."""
        context = get_current_context()

        # Check capability
        if not context.can_access_resource("file", path, "write"):
            raise PermissionError(f"No capability to write {path}")

        # Check file size limit
        size_limit = context.get_capability("file").constraints.max_file_size
        if size_limit and len(content) > size_limit:
            raise ResourceLimitError(
                f"Content size {len(content)} exceeds limit {size_limit}"
            )

        context.use_capability("file", path, "write")
        audit_log.info(f"File write: {path}, size: {len(content)}", user=context.user)

        with open(path, 'w') as f:
            f.write(content)
```

### 3.2 Capability-Aware Network Access

```python
# src/mlpy/stdlib/secure_network_bridge.py

class SecureNetworkOperations:
    """Capability-aware network operations."""

    @requires_capability("network", auto_use=False)
    def http_get(self, url: str) -> dict:
        """HTTP GET with capability enforcement."""
        context = get_current_context()

        # Parse URL
        parsed = urlparse(url)
        host = parsed.netloc

        # Check capability for this host
        if not context.can_access_resource("network", host, "https"):
            raise PermissionError(f"No capability to access {host}")

        # Check rate limiting
        if not self._check_rate_limit(context, host):
            raise RateLimitExceededError(f"Rate limit exceeded for {host}")

        context.use_capability("network", host, "https")
        audit_log.info(f"HTTP GET: {url}", user=context.user)

        # Perform request
        response = requests.get(url)
        return response.json()
```

### 3.3 Capability-Aware Database Access

```python
# src/mlpy/stdlib/secure_database_bridge.py

class SecureDatabaseOperations:
    """Capability-aware database operations."""

    @requires_capability("database", auto_use=False)
    def query(self, connection_string: str, sql: str) -> list[dict]:
        """Execute SQL query with capability enforcement."""
        context = get_current_context()

        # Determine operation type (SELECT, INSERT, UPDATE, DELETE)
        operation = self._parse_sql_operation(sql)

        # Check capability
        if not context.can_access_resource("database", connection_string, operation):
            raise PermissionError(
                f"No capability for {operation} on {connection_string}"
            )

        # Check row limit for SELECT operations
        if operation == "select":
            row_limit = context.get_capability("database").constraints.max_rows
            if row_limit:
                sql = self._add_limit_clause(sql, row_limit)

        context.use_capability("database", connection_string, operation)
        audit_log.info(
            f"Database {operation}: {connection_string}",
            sql=sql[:100],  # First 100 chars for audit
            user=context.user
        )

        # Execute query
        conn = self._get_connection(connection_string)
        return conn.execute(sql).fetchall()
```

### 3.4 Capability-Aware Module Imports

```python
# src/mlpy/stdlib/secure_import_bridge.py

class SecureImportSystem:
    """Capability-aware module import system."""

    @requires_capability("import", auto_use=False)
    def import_module(self, module_name: str) -> object:
        """Import module with capability enforcement."""
        context = get_current_context()

        # Check if module is allowed
        if not context.can_access_resource("import", module_name, "import"):
            raise PermissionError(f"No capability to import {module_name}")

        # Check stdlib-only restriction
        import_cap = context.get_capability("import")
        if import_cap.constraints.get("stdlib_only") and not self._is_stdlib(module_name):
            raise PermissionError(
                f"Only stdlib imports allowed, {module_name} is third-party"
            )

        context.use_capability("import", module_name, "import")
        audit_log.info(f"Module import: {module_name}", user=context.user)

        # Perform import
        return importlib.import_module(module_name)
```

---

## Layer 4: ML Program Layer

### Purpose
ML programmer declares required capabilities, runtime validates and enforces.

### 4.1 ML Capability Declaration Syntax

```ml
// ML program declares what it needs
capability FileAccess {
    resource "data/*.csv";
    resource "output/*.txt";
    allow read;
    allow write;
}

capability NetworkAccess {
    resource "api.example.com";
    allow https;
}

// Use capabilities via stdlib
import file;
import network;

function processData() {
    // Runtime checks: does user have FileAccess for data/*.csv with read?
    data = file.read("data/input.csv");

    // Runtime checks: does user have NetworkAccess for api.example.com with https?
    result = network.get("https://api.example.com/process", data);

    // Runtime checks: does user have FileAccess for output/*.txt with write?
    file.write("output/result.txt", result);
}
```

### 4.2 Runtime Validation Logic

```python
class CapabilityValidator:
    """Validates ML program capabilities against granted capabilities."""

    def validate(
        self,
        declared: list[CapabilityDeclaration],
        granted: list[CapabilityToken]
    ) -> ValidationResult:
        """Validate declared capabilities are subset of granted."""

        valid = []
        denied = []

        for decl in declared:
            if self._is_granted(decl, granted):
                valid.append(decl)
            else:
                denied.append(decl)

        return ValidationResult(
            valid=(len(denied) == 0),
            valid_capabilities=valid,
            denied_capabilities=denied
        )

    def _is_granted(
        self,
        declared: CapabilityDeclaration,
        granted: list[CapabilityToken]
    ) -> bool:
        """Check if declared capability is covered by granted tokens."""

        for token in granted:
            # Check type matches
            if token.capability_type != declared.type:
                continue

            # Check all resource patterns are covered
            if not all(
                self._pattern_covered(dp, token.constraints.resource_patterns)
                for dp in declared.resource_patterns
            ):
                continue

            # Check all operations are allowed
            if not declared.operations.issubset(token.constraints.allowed_operations):
                continue

            # All checks passed
            return True

        # No matching token found
        return False
```

### 4.3 Audit Logging

```python
class CapabilityAuditLogger:
    """Logs all capability usage for security auditing."""

    def log_capability_use(
        self,
        user: User,
        capability_type: str,
        resource: str,
        operation: str,
        success: bool,
        metadata: dict = None
    ):
        """Log capability usage event."""

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": {
                "username": user.username,
                "uid": user.uid,
                "groups": user.groups
            },
            "capability": {
                "type": capability_type,
                "resource": resource,
                "operation": operation
            },
            "success": success,
            "metadata": metadata or {}
        }

        # Write to audit log
        self.audit_log.info(json.dumps(log_entry))

        # Send to SIEM if configured
        if self.siem_enabled:
            self.siem_client.send_event(log_entry)

# Example audit log entries:
# {"timestamp": "2025-10-03T10:30:45", "user": {"username": "alice"},
#  "capability": {"type": "file", "resource": "data/users.csv", "operation": "read"},
#  "success": true}
#
# {"timestamp": "2025-10-03T10:30:46", "user": {"username": "alice"},
#  "capability": {"type": "network", "resource": "external-api.com", "operation": "https"},
#  "success": false, "metadata": {"reason": "capability_not_granted"}}
```

---

## Authentication & Authorization Mechanisms

### Option 1: OS-Level (Simple, Development)

**Pros:**
- No additional infrastructure needed
- Uses existing OS user management
- Simple to implement

**Cons:**
- Limited to single-machine deployment
- No fine-grained role management
- Difficult to audit across systems

**Implementation:**
```python
class OSAuthProvider:
    def authenticate(self) -> User:
        uid = os.getuid()
        user_info = pwd.getpwuid(uid)
        return User(username=user_info.pw_name, uid=uid)
```

### Option 2: LDAP/Active Directory (Enterprise)

**Pros:**
- Centralized user management
- Group-based policies
- Enterprise integration

**Cons:**
- Requires LDAP infrastructure
- Complex setup
- Network dependency

**Implementation:**
```python
class LDAPAuthProvider:
    def authenticate(self, username: str, password: str) -> User:
        conn = ldap.initialize(LDAP_SERVER)
        conn.simple_bind_s(f"uid={username},{BASE_DN}", password)

        # Get user groups
        groups = conn.search_s(BASE_DN, ldap.SCOPE_SUBTREE,
                               f"(memberUid={username})")

        return User(username=username, groups=[g[1]['cn'][0] for g in groups])
```

### Option 3: JWT Token-Based (API/Cloud)

**Pros:**
- Stateless authentication
- Works across distributed systems
- Easy API integration
- Modern cloud-native approach

**Cons:**
- Requires token management infrastructure
- Token revocation complexity
- Expiration management

**Implementation:**
```python
class JWTAuthProvider:
    def authenticate(self, token: str) -> User:
        claims = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])

        return User(
            username=claims["sub"],
            roles=claims.get("roles", []),
            groups=claims.get("groups", []),
            permissions=claims.get("permissions", [])
        )
```

### Option 4: mTLS Certificate-Based (High Security)

**Pros:**
- Strong cryptographic authentication
- No password management
- Mutual authentication
- Perfect for machine-to-machine

**Cons:**
- Certificate infrastructure required
- Complex key management
- Certificate rotation overhead

**Implementation:**
```python
class mTLSAuthProvider:
    def authenticate(self, cert: X509Certificate) -> User:
        # Verify certificate chain
        if not verify_cert_chain(cert, CA_CERT):
            raise AuthenticationError("Invalid certificate chain")

        # Extract user info from certificate
        return User(
            username=cert.subject.common_name,
            organization=cert.subject.organization_name,
            roles=cert.extensions.get("roles", [])
        )
```

### Recommended: Pluggable Auth Provider Pattern

```python
class AuthenticationManager:
    """Pluggable authentication system."""

    def __init__(self):
        self.providers: dict[str, AuthProvider] = {}

    def register_provider(self, name: str, provider: AuthProvider):
        self.providers[name] = provider

    def authenticate(self, method: str, **credentials) -> User:
        provider = self.providers.get(method)
        if not provider:
            raise ValueError(f"Unknown auth method: {method}")

        return provider.authenticate(**credentials)

# Usage:
auth_mgr = AuthenticationManager()
auth_mgr.register_provider("os", OSAuthProvider())
auth_mgr.register_provider("jwt", JWTAuthProvider())
auth_mgr.register_provider("ldap", LDAPAuthProvider())

# Authenticate using different methods
user1 = auth_mgr.authenticate("os")
user2 = auth_mgr.authenticate("jwt", token=jwt_token)
user3 = auth_mgr.authenticate("ldap", username="alice", password="secret")
```

---

## Policy Decision Points (PDP)

### Where Authorization Decisions Are Made

```python
class PolicyDecisionPoint:
    """Centralized policy decision engine."""

    def can_execute(
        self,
        user: User,
        capability_type: str,
        resource: str,
        operation: str
    ) -> PolicyDecision:
        """Decide if user can perform operation on resource."""

        # 1. Load all applicable policies
        policies = self.policy_store.get_policies_for_user(user)

        # 2. Evaluate each policy
        decisions = []
        for policy in policies:
            decision = policy.evaluate(capability_type, resource, operation)
            decisions.append(decision)

        # 3. Combine decisions (default: any ALLOW grants access)
        return self._combine_decisions(decisions)

    def _combine_decisions(self, decisions: list[PolicyDecision]) -> PolicyDecision:
        """Combine multiple policy decisions."""

        # Check for explicit DENY (overrides everything)
        if any(d.effect == "DENY" for d in decisions):
            return PolicyDecision(effect="DENY", reason="Explicit deny")

        # Check for ALLOW
        if any(d.effect == "ALLOW" for d in decisions):
            return PolicyDecision(effect="ALLOW")

        # Default DENY
        return PolicyDecision(effect="DENY", reason="No applicable policy")
```

---

## Implementation Roadmap

### Phase 1: Core Infrastructure (Weeks 1-2)
- [ ] Policy definition format (YAML)
- [ ] Policy storage and loading
- [ ] Basic authentication (OS-level)
- [ ] Capability validator
- [ ] Audit logging framework

### Phase 2: Stdlib Integration (Weeks 3-4)
- [ ] Capability-aware file operations
- [ ] Capability-aware network operations
- [ ] Capability-aware database operations
- [ ] Capability-aware import system

### Phase 3: Sandbox Integration (Weeks 5-6)
- [ ] Sandbox initialization with capabilities
- [ ] User context management
- [ ] Runtime enforcement
- [ ] Audit trail

### Phase 4: Advanced Auth (Weeks 7-8)
- [ ] JWT authentication provider
- [ ] LDAP integration
- [ ] Pluggable auth system
- [ ] Role-based access control (RBAC)

### Phase 5: Administration Tools (Weeks 9-10)
- [ ] Policy management CLI
- [ ] Web-based admin interface
- [ ] Audit log viewer
- [ ] Capability testing tools

---

## Security Guarantees

With this architecture, we guarantee:

1. ✅ **Least Privilege:** Users only get explicitly granted capabilities
2. ✅ **Defense in Depth:** Multiple enforcement layers (policy, runtime, stdlib)
3. ✅ **Auditability:** All operations logged with user context
4. ✅ **Isolation:** Sandbox enforces hard limits on resources
5. ✅ **Transparency:** ML programs declare what they need
6. ✅ **Flexibility:** Pluggable auth, storage, enforcement
7. ✅ **Scalability:** Works from single-user dev to multi-tenant cloud

---

## Example: Complete Flow

### 1. Administrator Creates Policy
```bash
mlpy-admin policy create data_scientist.yaml
```

```yaml
# data_scientist.yaml
policy:
  name: "Data Scientist"
  applies_to:
    users: ["alice"]
  capabilities:
    file:
      - patterns: ["data/*.csv"]
        operations: [read]
```

### 2. User Runs ML Program
```bash
mlpy run analysis.ml --auth-token <jwt>
```

### 3. Runtime Validates
```python
# System authenticates user from JWT
user = auth.authenticate(jwt_token)  # → alice

# System loads alice's policies
policies = policy_mgr.get_policies(user)  # → data_scientist.yaml

# System initializes sandbox with granted capabilities
sandbox = initialize_sandbox(user, policies)
# → file capability: data/*.csv, read
```

### 4. ML Program Declares and Uses
```ml
capability FileAccess {
    resource "data/*.csv";
    allow read;
}

import file;
data = file.read("data/sales.csv");  // ✅ Granted - succeeds
```

### 5. Runtime Enforces
```python
# file.read() checks capability
context.can_access_resource("file", "data/sales.csv", "read")  # → True
# Operation proceeds and is logged
audit_log.info("alice read data/sales.csv")
```

### 6. Denied Operation
```ml
file.write("secret/passwords.txt", data);  // ❌ Not granted - fails
```

```python
# file.write() checks capability
context.can_access_resource("file", "secret/passwords.txt", "write")  # → False
# Exception raised
raise PermissionError("No capability for secret/passwords.txt write")
# Denied attempt logged
audit_log.warning("alice DENIED write to secret/passwords.txt")
```

---

## Conclusion

This multi-layer architecture provides:

- **Clear separation of concerns** between admin, system, and user
- **Flexible authentication** supporting multiple methods
- **Fine-grained authorization** at resource and operation level
- **Comprehensive auditing** for security compliance
- **Stdlib integration** making enforcement transparent
- **ML program declarations** making security explicit

The system is designed to be:
- **Secure by default** (deny unless explicitly granted)
- **Auditable** (all operations logged)
- **Flexible** (pluggable components)
- **Scalable** (from dev to production)

Next steps: Prioritize implementation phases and build incrementally.
