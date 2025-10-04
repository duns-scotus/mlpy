# Capability System: Current State, Future Vision, and Implementation Guideline

**Document Type:** Architectural Analysis & Design Guideline
**Author:** Claude Code + User Requirements
**Date:** October 2025
**Status:** Design Specification
**Purpose:** Foundation for future implementation proposals

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current System Analysis](#current-system-analysis)
3. [Future Vision: Multi-Layer Architecture](#future-vision-multi-layer-architecture)
4. [Authentication Mechanisms](#authentication-mechanisms)
5. [Gap Analysis](#gap-analysis)
6. [Design Principles](#design-principles)
7. [Next Steps](#next-steps)

---

## Executive Summary

### What We Have Now
The current mlpy capability system provides **token-based permissions with runtime enforcement**, but lacks **external authorization**. ML programs can self-grant any capability they declare, making it suitable for trusted code but insufficient for multi-tenant or untrusted execution environments.

### What We Need
A **four-layer security architecture** where:
1. **Administrators** define security policies and grant capabilities to users
2. **Sandbox runtime** authenticates users and validates capabilities at startup
3. **Standard library** enforces capabilities on all sensitive operations
4. **ML programs** declare requirements, which are validated against granted capabilities

### Current Gap
**Missing:** External policy enforcement and user authentication layer. The capability infrastructure exists but isn't connected to user identity or administrative control.

---

## Current System Analysis

### What Currently Exists

#### 1. Capability Token Infrastructure ✅
**Location:** `src/mlpy/runtime/capabilities/tokens.py`

**Status:** PRODUCTION READY

**Features:**
- Unforgeable tokens with UUID identity and SHA256 checksums
- Fine-grained constraints:
  - Resource patterns (glob matching: `*.txt`, `data/*.json`)
  - Allowed operations (sets: `{read, write, execute}`)
  - Time limits (expiration, usage count)
  - Resource limits (file size, memory, CPU)
  - Network constraints (hosts, ports)
- Automatic validation on every use
- Usage tracking and auditing

**Example:**
```python
token = create_capability_token(
    capability_type="file",
    resource_patterns=["data/*.csv"],
    allowed_operations={"read", "write"},
    expires_in=timedelta(hours=1),
    max_usage_count=100
)
```

#### 2. Capability Context System ✅
**Location:** `src/mlpy/runtime/capabilities/context.py`

**Status:** PRODUCTION READY

**Features:**
- Thread-local capability storage
- Hierarchical parent-child inheritance
- Context managers for scope control
- Automatic expired token cleanup
- Thread-safe operations with RLock

**Example:**
```python
# Parent context with file capability
with manager.create_file_capability_context(["*.txt"]) as parent:
    # Child inherits file capability
    child = parent.create_child_context("child")
    assert child.has_capability("file")  # True (inherited)
```

#### 3. Capability Manager ✅
**Location:** `src/mlpy/runtime/capabilities/manager.py`

**Status:** PRODUCTION READY

**Features:**
- Global singleton for capability management
- Pre-configured context factories (file, network)
- Convenience functions for enforcement
- Thread-local current context tracking

#### 4. Code Generation ✅
**Location:** `src/mlpy/ml/codegen/python_generator.py`

**Status:** PRODUCTION READY

**What it does:**
- Parses ML `capability` declarations from source
- Generates Python capability infrastructure:
  ```python
  def _create_FileAccess_capability():
      return create_capability_token(...)

  @contextlib.contextmanager
  def FileAccess_context():
      manager = get_capability_manager()
      token = _create_FileAccess_capability()
      with manager.capability_context("FileAccess", [token]):
          yield
  ```
- Wraps ML code execution in capability contexts

### How It Currently Works

#### ML Code:
```ml
capability FileAccess {
    resource "*.txt";
    allow read;
    allow write;
}

function readConfig() {
    return file.read("config.txt");
}
```

#### Generated Python:
```python
# Capability infrastructure (auto-generated)
def _create_FileAccess_capability():
    return create_capability_token(
        capability_type="FileAccess",
        resource_patterns=["*.txt"],
        allowed_operations={"read", "write"}
    )

@contextlib.contextmanager
def FileAccess_context():
    manager = get_capability_manager()
    token = _create_FileAccess_capability()
    with manager.capability_context("FileAccess", [token]):
        yield

# ML function (transpiled)
def readConfig():
    return file.read("config.txt")

# Execution (auto-wrapped)
with FileAccess_context():
    readConfig()
```

### Current System Strengths

✅ **Solid Foundation:**
- Complete token infrastructure with cryptographic integrity
- Thread-safe context management with inheritance
- Automatic validation and cleanup
- Integration with code generation

✅ **Runtime Enforcement:**
- Tokens validated on every use
- Pattern matching for resources
- Operation-level permissions
- Usage tracking and limits

✅ **Developer Experience:**
- Clean ML syntax for capability declarations
- Automatic Python infrastructure generation
- Context managers for scoped capabilities

### Critical Limitation: Self-Granting

**The Problem:**
```ml
// ML programmer writes:
capability GodMode {
    resource "*";              // Everything!
    allow read;
    allow write;
    allow delete;
    allow execute;
}

// System generates token and grants it automatically
// No validation against external policy
// No user authentication
// ML programmer gets exactly what they declared
```

**Result:** Current system is **documentation of intent**, not **security enforcement**.

**Suitable For:**
- ✅ Trusted internal code
- ✅ Development environments
- ✅ Single-user scenarios
- ✅ Capability-aware library development

**NOT Suitable For:**
- ❌ Untrusted code execution
- ❌ Multi-tenant environments
- ❌ Production security isolation
- ❌ User-level permission enforcement

---

## Future Vision: Multi-Layer Architecture

### The Four-Layer Model

```
┌─────────────────────────────────────────────────────────────┐
│                 Layer 1: ADMINISTRATOR                       │
│  Role: Define policies, grant capabilities to users         │
│  Who: System admin, security team                           │
│  Output: Security policies (YAML/JSON)                      │
└────────────────────┬────────────────────────────────────────┘
                     │ Policy files
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              Layer 2: SANDBOX STARTUP                        │
│  Role: Authenticate user, load authorized capabilities      │
│  Who: mlpy runtime                                          │
│  Input: User credentials + Policy files                     │
│  Output: Restricted execution context                       │
└────────────────────┬────────────────────────────────────────┘
                     │ Granted capabilities
                     ↓
┌─────────────────────────────────────────────────────────────┐
│             Layer 3: STANDARD LIBRARY                        │
│  Role: Enforce capabilities on sensitive operations         │
│  Who: file, network, database, import bridges               │
│  Check: Does user have capability before operation?         │
└────────────────────┬────────────────────────────────────────┘
                     │ Validated operations
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                Layer 4: ML PROGRAM                           │
│  Role: Declare requirements, get validated                  │
│  Who: ML programmer                                         │
│  Input: Capability declarations                             │
│  Validation: Declared ⊆ Granted                             │
└─────────────────────────────────────────────────────────────┘
```

### Layer 1: Administrator Controls

**Administrator Defines Policy:**
```yaml
# /etc/mlpy/policies/data_scientist.yaml
policy:
  name: "Data Scientist Role"

  # Who this applies to
  applies_to:
    users: ["alice", "bob"]
    groups: ["data_team", "analytics"]

  # What they're allowed to do
  capabilities:
    file:
      - patterns: ["data/*.csv", "data/*.json", "output/*.txt"]
        operations: [read, write]
        max_file_size: 10485760  # 10MB

    network:
      - hosts: ["api.internal.company.com"]
        operations: [https]
        ports: [443]

    database:
      - connections: ["postgresql://analytics-db/"]
        operations: [select, insert]
        max_rows: 10000

  # Resource limits
  limits:
    max_memory: 2147483648  # 2GB
    max_cpu_time: 3600      # 1 hour
```

**Administrator Grants Policy:**
```bash
# Grant policy to user
mlpy-admin grant data_scientist --user alice

# View user's capabilities
mlpy-admin show --user alice
  User: alice
  Policies: data_scientist
  Capabilities:
    - file: data/*.csv, data/*.json, output/*.txt (read, write)
    - network: api.internal.company.com (https)
    - database: postgresql://analytics-db/ (select, insert)
```

### Layer 2: Sandbox Startup Validation

**When User Runs ML Program:**
```bash
mlpy run analysis.ml --user alice
```

**Runtime Flow:**
1. **Authenticate user** (verify identity)
2. **Load policies** that apply to user
3. **Parse ML program** capability declarations
4. **Validate**: declared ⊆ granted
5. **Initialize sandbox** with granted capabilities
6. **Execute** if validation passes

**Code:**
```python
def execute_ml_program_secure(script_path: str, user: User):
    # 1. Load user's granted capabilities from policies
    policy_mgr = PolicyManager()
    granted_caps = policy_mgr.get_capabilities(user)
    # → [file:data/*.csv (read,write), network:api.internal.com (https)]

    # 2. Parse ML program's capability declarations
    ml_code = read_file(script_path)
    declared_caps = parse_ml_capabilities(ml_code)
    # → [file:data/*.csv (read)]

    # 3. Validate: declared must be subset of granted
    validator = CapabilityValidator()
    if not validator.validate(declared_caps, granted_caps):
        raise SecurityError("Program requires capabilities not granted to user")

    # 4. Execute with granted (not declared) capabilities
    with create_sandbox_context(granted_caps):
        execute_ml_code(ml_code)
```

### Layer 3: Standard Library Enforcement

**Capability-Aware File Operations:**
```python
# src/mlpy/stdlib/secure_file_bridge.py

class SecureFileOperations:
    @requires_capability("file", auto_use=False)
    def read(self, path: str) -> str:
        context = get_current_context()

        # Check: Does user have file capability for this path with read operation?
        if not context.can_access_resource("file", path, "read"):
            audit_log.warning(f"DENIED: {context.user} read {path}")
            raise PermissionError(f"No capability to read {path}")

        # Record usage
        context.use_capability("file", path, "read")
        audit_log.info(f"ALLOWED: {context.user} read {path}")

        # Perform operation
        with open(path, 'r') as f:
            return f.read()
```

**Capability-Aware Network Operations:**
```python
class SecureNetworkOperations:
    @requires_capability("network", auto_use=False)
    def http_get(self, url: str) -> dict:
        context = get_current_context()
        host = urlparse(url).netloc

        # Check capability for this host
        if not context.can_access_resource("network", host, "https"):
            audit_log.warning(f"DENIED: {context.user} access {host}")
            raise PermissionError(f"No capability to access {host}")

        context.use_capability("network", host, "https")
        audit_log.info(f"ALLOWED: {context.user} GET {url}")

        return requests.get(url).json()
```

### Layer 4: ML Program Declaration

**ML Programmer Declares Needs:**
```ml
// Programmer declares what the program needs
capability FileAccess {
    resource "data/*.csv";
    allow read;
}

capability NetworkAccess {
    resource "api.internal.company.com";
    allow https;
}

import file;
import network;

function analyze() {
    // Runtime validates: user has file:data/*.csv,read?
    data = file.read("data/sales.csv");

    // Runtime validates: user has network:api.internal.company.com,https?
    result = network.get("https://api.internal.company.com/process", data);

    return result;
}
```

**Validation at Runtime:**
```python
# User alice runs the program
# alice has granted: file:data/*.csv (read,write), network:api.internal.com (https)

declared = [
    Capability(type="file", patterns=["data/*.csv"], ops=["read"]),
    Capability(type="network", patterns=["api.internal.company.com"], ops=["https"])
]

granted = alice.capabilities

# Validate each declared capability
for cap in declared:
    if not is_granted(cap, granted):
        raise PermissionError(f"User alice lacks {cap}")

# All validated ✓ - execute program
```

### Complete Example Flow

**Step 1: Admin Creates Policy**
```bash
mlpy-admin policy create data_scientist.yaml
mlpy-admin grant data_scientist --user alice
```

**Step 2: Alice Runs Program**
```bash
alice@laptop:~$ mlpy run analysis.ml
```

**Step 3: Runtime Authenticates**
```python
user = authenticate()  # → alice
```

**Step 4: Runtime Loads Granted Capabilities**
```python
granted = load_policies(user)
# → file:data/*.csv (read), network:api.internal.com (https)
```

**Step 5: Runtime Parses ML Declarations**
```python
declared = parse_ml_capabilities("analysis.ml")
# → file:data/*.csv (read), network:api.internal.com (https)
```

**Step 6: Runtime Validates**
```python
validate(declared, granted)  # ✓ declared ⊆ granted
```

**Step 7: Program Executes**
```ml
// This succeeds - alice has file:data/*.csv,read
data = file.read("data/sales.csv");  ✓

// This succeeds - alice has network:api.internal.com,https
result = network.get("https://api.internal.company.com/...");  ✓

// This FAILS - alice does NOT have file:secret/*,write
file.write("secret/passwords.txt", data);  ✗
```

**Step 8: Audit Log**
```
[2025-10-03 10:30:00] alice ALLOWED file.read data/sales.csv
[2025-10-03 10:30:01] alice ALLOWED network.get api.internal.company.com
[2025-10-03 10:30:02] alice DENIED file.write secret/passwords.txt
```

---

## Authentication Mechanisms

### What is Authentication?

**Authentication** = Proving who you are
**Authorization** = Determining what you're allowed to do

The system needs to know **who is running the ML program** before it can determine **what capabilities they have**.

### JWT Tokens: Modern Authentication

#### What is a JWT?

**JWT = JSON Web Token**

A compact, URL-safe, digitally signed token that proves user identity.

**Structure:** `HEADER.PAYLOAD.SIGNATURE`

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9  ← Header (algorithm, type)
.
eyJzdWIiOiJhbGljZSIsInJvbGUiOiJkYXRhX3NjaWVudGlzdCIsImV4cCI6MTczMDAwMDAwMH0  ← Payload (claims)
.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c  ← Signature (proof of integrity)
```

**Decoded Payload:**
```json
{
  "sub": "alice",                    // Subject (username)
  "email": "alice@company.com",      // Email
  "roles": ["data_scientist"],       // User's roles
  "groups": ["analytics", "ml"],     // User's groups
  "exp": 1730000000,                 // Expiration timestamp
  "iat": 1729900000                  // Issued at timestamp
}
```

#### How User Gets a JWT

**Login Flow:**
```
User                    Auth Server                mlpy Runtime
  │                          │                          │
  │  1. Username/Password    │                          │
  ├─────────────────────────>│                          │
  │                          │                          │
  │                     2. Verify credentials           │
  │                     3. Create JWT                   │
  │                          │                          │
  │  4. Return JWT           │                          │
  │<─────────────────────────┤                          │
  │                          │                          │
  │  5. Store token                                     │
  │  (~/.mlpy/token)         │                          │
  │                          │                          │
  │  6. Run ML program       │                          │
  │  (passes token)          │                          │
  ├─────────────────────────────────────────────────────>│
  │                          │                          │
  │                          │                     7. Verify JWT signature
  │                          │                     8. Extract user info
  │                          │                     9. Load capabilities
  │                          │                    10. Execute with limits
```

**Step-by-Step:**

**1. User Logs In:**
```bash
mlpy login
Username: alice
Password: ****
```

**2. Server Verifies Credentials:**
```python
def login(username, password):
    user = db.get_user(username)
    if not verify_password(password, user.password_hash):
        return {"error": "Invalid credentials"}, 401

    return create_jwt(user)
```

**3. Server Creates JWT:**
```python
import jwt
from datetime import datetime, timedelta

def create_jwt(user):
    payload = {
        "sub": user.username,
        "email": user.email,
        "roles": user.roles,
        "groups": user.groups,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"token": token}
```

**4. User Stores Token:**
```bash
# Saved to ~/.mlpy/token
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZSIsInJvbGVzIjpbImRhdGFfc2NpZW50aXN0Il19.abc123
```

**5. User Runs Program:**
```bash
mlpy run analysis.ml
# Token automatically loaded from ~/.mlpy/token
```

**6. Runtime Verifies JWT:**
```python
def verify_jwt(token):
    try:
        # Verify signature and decode
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        return User(
            username=payload["sub"],
            email=payload["email"],
            roles=payload["roles"],
            groups=payload["groups"]
        )
    except jwt.ExpiredSignatureError:
        raise AuthError("Token expired - please login again")
    except jwt.InvalidTokenError:
        raise AuthError("Invalid token")
```

#### JWT Advantages

✅ **Stateless:** Server doesn't store sessions
✅ **Portable:** Works across different services
✅ **Self-contained:** All user info in the token
✅ **Verifiable:** Cryptographic signature prevents tampering
✅ **Expirable:** Automatic security through expiration
✅ **Scalable:** No session database needed

### Alternative Authentication Methods

#### Option A: OS-Level Authentication
**Who:** System users (alice, bob)
**How:** Uses OS user identity
**Best for:** Single-machine, development

```python
import os, pwd

def authenticate():
    uid = os.getuid()
    user_info = pwd.getpwuid(uid)
    return User(username=user_info.pw_name, uid=uid)
```

#### Option B: LDAP/Active Directory
**Who:** Enterprise users
**How:** Centralized directory service
**Best for:** Corporate environments

```python
import ldap

def authenticate(username, password):
    conn = ldap.initialize(LDAP_SERVER)
    conn.simple_bind_s(f"uid={username},dc=company,dc=com", password)
    # Get user's groups from LDAP
    return User(username=username, groups=ldap_groups)
```

#### Option C: API Keys → JWT Exchange
**Who:** Automated systems, CI/CD
**How:** Long-lived key exchanges for short-lived JWT
**Best for:** Machine-to-machine

```bash
# Service has API key
mlpy login --api-key sk_prod_abc123xyz

# Exchange for JWT
POST /auth/token
  api_key: sk_prod_abc123xyz

# Get JWT
{"token": "eyJhbG...", "expires_in": 3600}
```

#### Option D: Certificate-Based (mTLS)
**Who:** High-security services
**How:** X.509 certificates
**Best for:** Service mesh, high-trust environments

```python
def authenticate(cert_path):
    cert = load_certificate(cert_path)
    if not verify_cert_chain(cert, CA_CERT):
        raise AuthError("Invalid certificate")
    return User(username=cert.subject.common_name)
```

### Recommended: Pluggable Authentication

```python
class AuthenticationManager:
    """Support multiple auth methods."""

    def __init__(self):
        self.providers = {}

    def register(self, name: str, provider: AuthProvider):
        self.providers[name] = provider

    def authenticate(self, method: str, **credentials) -> User:
        return self.providers[method].authenticate(**credentials)

# Usage
auth = AuthenticationManager()
auth.register("jwt", JWTAuthProvider())
auth.register("os", OSAuthProvider())
auth.register("ldap", LDAPAuthProvider())

# Authenticate different ways
user1 = auth.authenticate("jwt", token=jwt_token)
user2 = auth.authenticate("os")
user3 = auth.authenticate("ldap", username="alice", password="secret")
```

---

## Gap Analysis

### What We Have vs. What We Need

| Component | Current Status | Future Need | Gap |
|-----------|----------------|-------------|-----|
| **Capability Tokens** | ✅ Complete | Same | None |
| **Context System** | ✅ Complete | Same | None |
| **Manager** | ✅ Complete | Same | None |
| **Code Generation** | ✅ Complete | Add validation step | Minor |
| **Policy Storage** | ❌ Missing | YAML/JSON policies | **Major** |
| **User Authentication** | ❌ Missing | JWT/OS/LDAP support | **Major** |
| **Policy Validation** | ❌ Missing | declared ⊆ granted check | **Major** |
| **Capability-Aware Stdlib** | ⚠️ Partial | file, network, db, import | **Medium** |
| **Audit Logging** | ⚠️ Basic | Comprehensive SIEM integration | **Medium** |
| **Admin Tools** | ❌ Missing | CLI for policy management | **Major** |

### Critical Missing Pieces

#### 1. Policy System (HIGH PRIORITY)
**Need:** Load, store, and manage security policies

```python
class PolicyManager:
    def load_policy(self, name: str) -> Policy: ...
    def get_policies_for_user(self, user: User) -> list[Policy]: ...
    def get_capabilities(self, user: User) -> list[CapabilityToken]: ...
    def assign_policy(self, policy: Policy, user: User): ...
```

#### 2. Authentication Layer (HIGH PRIORITY)
**Need:** Verify user identity before execution

```python
class Authenticator:
    def authenticate(self, **credentials) -> User: ...

class JWTAuthenticator(Authenticator):
    def authenticate(self, token: str) -> User: ...
```

#### 3. Validation Layer (HIGH PRIORITY)
**Need:** Ensure ML declarations ⊆ granted capabilities

```python
class CapabilityValidator:
    def validate(
        self,
        declared: list[CapabilityDeclaration],
        granted: list[CapabilityToken]
    ) -> ValidationResult: ...
```

#### 4. Secure Standard Library (MEDIUM PRIORITY)
**Need:** Capability checks in all sensitive operations

```python
class SecureFileOps:
    @requires_capability("file")
    def read(self, path: str) -> str:
        # Check capability before operation
        ...

class SecureNetworkOps:
    @requires_capability("network")
    def http_get(self, url: str) -> dict:
        # Check capability before request
        ...
```

#### 5. Admin Tooling (MEDIUM PRIORITY)
**Need:** Manage policies without editing files

```bash
mlpy-admin policy create <name>
mlpy-admin grant <policy> --user <username>
mlpy-admin revoke <policy> --user <username>
mlpy-admin show --user <username>
mlpy-admin audit --user <username> --since "2025-10-01"
```

---

## Design Principles

### 1. Principle of Least Privilege
**Always grant minimal necessary permissions**

```yaml
# GOOD: Narrow scope
file:
  - patterns: ["data/input/*.csv"]
    operations: [read]

# BAD: Too broad
file:
  - patterns: ["*"]
    operations: [read, write, delete, execute]
```

### 2. Deny by Default
**Nothing is allowed unless explicitly granted**

```python
def has_capability(user, capability):
    policies = load_policies(user)

    # Check if any policy grants this capability
    for policy in policies:
        if policy.grants(capability):
            return True

    # Default: deny
    return False
```

### 3. Separation of Concerns
**Each layer has one responsibility**

- **Admin:** Define policy (what users CAN do)
- **Runtime:** Enforce policy (what users ARE DOING)
- **Stdlib:** Check capabilities (is this allowed?)
- **ML Code:** Declare needs (what program WANTS)

### 4. Defense in Depth
**Multiple enforcement layers**

1. **Policy validation** (before execution starts)
2. **Context initialization** (at sandbox startup)
3. **Stdlib enforcement** (at every operation)
4. **Audit logging** (for post-execution review)

### 5. Fail Secure
**Errors should deny access, not grant it**

```python
try:
    if validate_capability(user, resource, operation):
        return perform_operation()
except Exception as e:
    # Error occurred - deny access (fail secure)
    log_security_error(e)
    raise PermissionError("Access denied due to validation error")
```

### 6. Auditability
**Every operation must be logged**

```python
def perform_operation(user, resource, operation):
    # Log attempt
    audit_log.info(f"{user} attempting {operation} on {resource}")

    if has_capability(user, resource, operation):
        # Log success
        audit_log.info(f"{user} ALLOWED {operation} on {resource}")
        return do_operation()
    else:
        # Log denial
        audit_log.warning(f"{user} DENIED {operation} on {resource}")
        raise PermissionError()
```

---

## Next Steps

### Phase 1: Design Detailed Implementation (Weeks 1-2)

Create implementation proposals for:

1. **Policy System Design**
   - Policy file format (YAML schema)
   - Storage mechanism (filesystem, database)
   - Loading and caching strategy
   - Policy merging algorithm (multiple policies per user)

2. **Authentication Integration**
   - JWT implementation details
   - Token storage and lifecycle
   - Provider interface design
   - Error handling and token refresh

3. **Validation Architecture**
   - Capability comparison algorithm
   - Pattern matching rules
   - Error messages and reporting
   - Performance optimization

4. **Stdlib Security Wrapper Design**
   - File operations enforcement
   - Network operations enforcement
   - Database operations enforcement
   - Import system enforcement

### Phase 2: Implementation Priority Order

**HIGH PRIORITY (Critical Path):**
1. Policy file format and loader
2. JWT authentication provider
3. Capability validator (declared ⊆ granted)
4. Sandbox initialization with validation

**MEDIUM PRIORITY (Core Features):**
5. Secure file operations
6. Secure network operations
7. Basic audit logging
8. Admin CLI tools

**LOW PRIORITY (Nice to Have):**
9. LDAP/AD integration
10. Web-based admin UI
11. SIEM integration
12. Advanced audit analytics

### Phase 3: Validation Strategy

**Test Cases:**
1. User with policy can execute valid ML program ✓
2. User without policy cannot execute program ✗
3. ML program requiring more than granted fails ✗
4. Capability inheritance works correctly ✓
5. Token expiration denies access ✗
6. Audit log captures all attempts ✓

**Success Criteria:**
- [ ] Admin can define policy and grant to user
- [ ] User can authenticate (JWT or other method)
- [ ] Runtime validates ML program against policy
- [ ] Stdlib enforces capabilities on operations
- [ ] All operations appear in audit log
- [ ] Unauthorized operations are blocked and logged

### Phase 4: Documentation Requirements

**For Implementation:**
- Detailed API specifications
- Database/file schemas
- Sequence diagrams for flows
- Error handling specifications

**For Users:**
- Policy writing guide
- Authentication setup guide
- Capability declaration reference
- Troubleshooting guide

**For Administrators:**
- Policy management procedures
- User provisioning workflows
- Audit log analysis guide
- Security best practices

---

## Conclusion

### Current State
We have a **solid capability infrastructure** with:
- ✅ Token system with cryptographic integrity
- ✅ Context hierarchy and inheritance
- ✅ Runtime enforcement mechanisms
- ✅ Code generation integration

### Missing Pieces
We need to add **external authorization** through:
- ❌ Policy definition and storage
- ❌ User authentication (JWT/LDAP/OS)
- ❌ Validation layer (declared ⊆ granted)
- ❌ Secure stdlib wrappers
- ❌ Admin tooling

### Path Forward
1. **Design** detailed implementation proposals (based on this guideline)
2. **Implement** in priority order (policy → auth → validation → stdlib)
3. **Test** with realistic scenarios (untrusted code, multi-tenant)
4. **Document** for users and administrators

### Key Insight
The current system handles **"what capabilities exist"**. The future system will add **"who has which capabilities"**. The infrastructure is ready - we need to connect it to user identity and administrative control.

This document serves as the **foundation for all future implementation work**. Every implementation proposal should reference this guideline and explain how it fits into the overall architecture.

---

## References

- Current capability implementation: `src/mlpy/runtime/capabilities/`
- Code generation: `src/mlpy/ml/codegen/python_generator.py`
- Detailed architecture proposal: `docs/proposals/multi-layer-capability-architecture.md`
- Capability system description: `docs/summaries/capability-description.md`
