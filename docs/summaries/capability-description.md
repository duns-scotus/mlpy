# mlpy Capability System: Complete Technical Documentation

**Author:** Claude Code
**Date:** October 2025
**Status:** Production-Ready

---

## Overview

The mlpy capability system is a **capability-based security framework** that enforces fine-grained access control using unforgeable tokens. It implements the **object-capability security model** where possessing a capability token grants specific, limited permissions to system resources.

This system provides **defense-in-depth** security by complementing static security analysis with dynamic runtime enforcement.

---

## Architecture: Core Components

### 1. Capability Tokens (`src/mlpy/runtime/capabilities/tokens.py`)

**Purpose:** Unforgeable permission certificates with cryptographic integrity

#### Key Features:

- **Unique Identity**
  - UUID-based token ID
  - Capability type identifier (e.g., "file", "network", "FileAccess")

- **Constraints System**
  - **Resource patterns:** Glob patterns for allowed resources (e.g., `*.txt`, `data/*.json`, `/secure/*.data`)
  - **Allowed operations:** Set of permitted actions (e.g., `{read, write, execute}`)
  - **Time limits:** Optional expiration dates and maximum usage counts
  - **Resource limits:** Max file size, memory allocation, CPU time
  - **Network constraints:** Allowed hosts and port numbers

- **Security Features**
  - **SHA256 checksum:** Tamper detection and integrity validation
  - **Usage tracking:** Count and timestamp of last usage
  - **Automatic validation:** Invalid/expired tokens rejected on every access

#### Token Creation Example:

```python
from mlpy.runtime.capabilities import create_capability_token
from datetime import timedelta

token = create_capability_token(
    capability_type="file",
    resource_patterns=["*.txt", "data/*.json"],
    allowed_operations={"read", "write"},
    expires_in=timedelta(hours=1),
    max_usage_count=100,
    max_file_size=1024*1024  # 1MB
)
```

#### Validation Rules:

Every token usage validates:
1. ✓ Checksum integrity (not tampered)
2. ✓ Not expired (time-based)
3. ✓ Within usage limits (count-based)
4. ✓ Resource pattern matches
5. ✓ Operation is allowed

---

### 2. Capability Contexts (`src/mlpy/runtime/capabilities/context.py`)

**Purpose:** Thread-safe hierarchical containers that hold and manage capability tokens

#### Key Features:

- **Hierarchical Inheritance**
  - Parent-child context relationships
  - Children automatically inherit parent capabilities
  - Local capabilities override inherited ones

- **Thread Safety**
  - Thread-local storage for isolation
  - RLock-based synchronization
  - Each thread has independent context

- **Context Lifecycle**
  - Context managers for clean entry/exit
  - Automatic expired token cleanup
  - Parent-child relationship maintenance

#### Context Hierarchy Example:

```
Root Context (capabilities: file:*.txt read, network:api.example.com https)
  ├── Child Context A (inherits: file+network, adds: file:*.json write)
  └── Child Context B (inherits: file+network, adds: database:* read)
      └── Grandchild Context (inherits: file+network+database)
```

#### Context Operations:

```python
from mlpy.runtime.capabilities import get_capability_manager

manager = get_capability_manager()

# Create context with file capability
with manager.create_file_capability_context(["*.txt"]) as parent:
    # Child inherits file capability
    child = parent.create_child_context("child_context")

    # Add additional capability to child
    network_token = create_network_capability(["api.example.com"])
    child.add_capability(network_token)

    # Check capabilities
    assert child.has_capability("file")     # Inherited from parent
    assert child.has_capability("network")  # Added locally
```

---

### 3. Capability Manager (`src/mlpy/runtime/capabilities/manager.py`)

**Purpose:** Global singleton managing all contexts and enforcing capability checks

#### Responsibilities:

1. **Context Management**
   - Maintain thread-local current context
   - Create pre-configured contexts (file, network)
   - Manage context stack for nested contexts

2. **Capability Enforcement**
   - Validate capability availability
   - Check resource access permissions
   - Record capability usage

3. **Convenience API**
   - Helper functions for common capabilities
   - Global access to capability system
   - Simplified context creation

#### Manager API:

```python
from mlpy.runtime.capabilities import get_capability_manager

manager = get_capability_manager()

# Check if capability exists
if manager.has_capability("file"):
    # Use capability for specific resource
    manager.use_capability("file", "config.txt", "read")

# Create pre-configured context
with manager.create_file_capability_context(["*.txt"]) as ctx:
    # Code with file access capability
    pass
```

---

## Workflow: From Declaration to Enforcement

### Step 1: Declaration (ML Language)

Developer declares capabilities in ML source code:

```ml
capability FileAccess {
    resource "*.txt";
    resource "data/*.json";
    allow read;
    allow write;
}

function readConfig(filename) {
    // Function implementation
    return file.read(filename);
}
```

### Step 2: Code Generation (Transpiler)

The ML transpiler generates Python code with capability infrastructure:

```python
"""Generated Python code from mlpy ML transpiler."""

import contextlib
from mlpy.runtime.capabilities import create_capability_token, get_capability_manager

# Capability declaration: FileAccess
def _create_FileAccess_capability():
    """Create capability token for FileAccess."""
    return create_capability_token(
        capability_type="FileAccess",
        resource_patterns=["*.txt", "data/*.json"],
        allowed_operations={"read", "write"},
        description="Generated capability for FileAccess"
    )

@contextlib.contextmanager
def FileAccess_context():
    """Capability context manager for FileAccess."""
    manager = get_capability_manager()
    token = _create_FileAccess_capability()
    with manager.capability_context("FileAccess_context", [token]):
        yield

def readConfig(filename):
    # Function implementation
    return file.read(filename)
```

### Step 3: Runtime Execution

Generated code executes within capability context:

```python
# Code runs within capability context
with FileAccess_context():
    result = readConfig("config.txt")  # Has FileAccess capability
```

### Step 4: Enforcement

Two primary enforcement mechanisms:

#### A. Decorator-Based Enforcement

Python standard library functions protected by decorators:

```python
from mlpy.runtime.capabilities import requires_capability

@requires_capability("file", "*.txt", "read")
def safe_file_reader(filename):
    """Can only be called with 'file' capability."""
    with open(filename) as f:
        return f.read()
```

**Enforcement Flow:**
1. Decorator checks capability exists before function execution
2. If missing: raises `CapabilityNotFoundError`
3. If present: records usage and executes function

#### B. Manual Enforcement

Critical operations perform explicit checks:

```python
from mlpy.runtime.capabilities import get_current_context, CapabilityNotFoundError

def dangerous_operation(resource_path):
    context = get_current_context()

    # Check capability exists
    if not context.has_capability("file"):
        raise CapabilityNotFoundError("file")

    # Use capability (validates and records usage)
    context.use_capability("file", resource_path, "write")

    # Perform operation
    perform_write(resource_path)
```

---

## Security Model

### Actors and Responsibilities

#### 1. ML Developer (User)
**Role:** Declares capability requirements

**Actions:**
- Declares capabilities in ML code with `capability { }` blocks
- Specifies resource patterns and operations
- Cannot forge or bypass capabilities (enforced by runtime)

**Example:**
```ml
capability DataAccess {
    resource "data/*.csv";
    allow read;
}
```

#### 2. Transpiler (Code Generator)
**Role:** Generates capability infrastructure

**Actions:**
- Parses capability declarations from ML AST
- Generates token factory functions
- Creates context manager wrappers
- Ensures all code runs within capability contexts

**Output:** Python code with capability system integrated

#### 3. Runtime System (Enforcement Engine)
**Role:** Validates and enforces capabilities

**Actions:**
- Validates tokens before every use
- Checks resource patterns match requested resources
- Records usage for auditing and limits
- Prevents unauthorized access attempts
- Automatically cleans up expired tokens

**Enforcement Points:**
- Function decorators (`@requires_capability`)
- Context validation (`has_capability()`)
- Token usage recording (`use_capability()`)

#### 4. Sandbox (Isolation Layer)
**Role:** Process-level security boundary

**Actions:**
- Serializes contexts for subprocess execution
- Inherits parent process capabilities
- Isolates untrusted code execution
- Enforces resource limits (CPU, memory, time)

---

## Enforcement Points

### 1. Decorator-Based Protection

Python functions require capabilities via decorators:

```python
@requires_capability("network", "api.example.com", "https")
def fetch_api_data(endpoint):
    url = f"https://api.example.com/{endpoint}"
    return requests.get(url).json()

# Calling without capability raises CapabilityNotFoundError
# Calling with capability succeeds and records usage
```

### 2. Safe Attribute Access

**Note:** The `safe_attr_access()` function in `runtime_helpers.py` is **NOT** part of the capability system. It's a separate security mechanism that whitelists Python object attributes/methods accessible from ML code.

**Capability system enforcement is separate and complementary.**

### 3. Context-Based Checks

Operations manually verify capability availability:

```python
def protected_function(resource):
    context = get_current_context()

    if not context.can_access_resource("file", resource, "read"):
        raise PermissionError(f"Cannot access {resource}")

    # Proceed with operation
    return read_resource(resource)
```

### 4. Automatic Token Validation

Every token operation validates:
- **Integrity:** SHA256 checksum verification
- **Expiration:** Time-based validity check
- **Usage limits:** Count-based restriction check
- **Resource matching:** Glob pattern validation
- **Operation allowance:** Permission set check

**Validation happens automatically on every `use_token()` call.**

---

## Grant and Revoke Operations

### Granting Capabilities

```python
from mlpy.runtime.capabilities import create_file_capability, get_current_context

# 1. Create capability token
token = create_file_capability(
    patterns=["*.txt"],
    operations={"read"}
)

# 2. Get current context
context = get_current_context()

# 3. Add capability to context
context.add_capability(token)

# Now context has file capability for *.txt with read permission
```

### Revoking Capabilities

```python
# Explicit removal
context = get_current_context()
context.remove_capability("file")

# Automatic expiration (set when creating token)
token = create_capability_token(
    capability_type="temporary",
    expires_in=timedelta(minutes=5)  # Auto-expires in 5 minutes
)

# Usage count limits (auto-revokes after N uses)
token = create_capability_token(
    capability_type="limited",
    max_usage_count=10  # Only usable 10 times
)
```

### Capability Inheritance

```python
# Parent grants capability
manager = get_capability_manager()

with manager.create_file_capability_context(["*.txt"]) as parent_ctx:
    # Child automatically inherits file capability
    child_ctx = parent_ctx.create_child_context("child")

    # Verify inheritance
    assert child_ctx.has_capability("file")  # True (inherited)

    # Child can add additional capabilities
    network_token = create_network_capability(["api.example.com"])
    child_ctx.add_capability(network_token)

    # Child now has both file (inherited) and network (local)
    assert child_ctx.has_capability("file")     # True
    assert child_ctx.has_capability("network")  # True

    # Parent doesn't have child's network capability
    assert not parent_ctx.has_capability("network")  # True
```

---

## Security Properties

### 1. Unforgeability
- Tokens have cryptographic SHA256 checksums
- Tampering detection via checksum validation
- Immutable token creation metadata

### 2. Fine-Grained Control
- Resource-level granularity with glob patterns
- Operation-specific permissions (read vs write vs execute)
- Constraint combinations (time + usage + resource)

### 3. Auditability
- Usage tracking with timestamps
- Usage count monitoring
- Context hierarchy tracking
- Token lifecycle metadata

### 4. Time-Limited Access
- Optional expiration timestamps
- Maximum usage count limits
- Automatic cleanup of expired tokens

### 5. Hierarchical Delegation
- Parent-child capability inheritance
- Local override of inherited capabilities
- Isolation of sibling contexts

### 6. Thread Safety
- RLock synchronization on all operations
- Thread-local context storage
- Safe concurrent access to contexts

### 7. Self-Cleaning
- Automatic expired token removal
- Cleanup on context exit
- Periodic validation checks

---

## Design Philosophy

### Principle of Least Privilege

**Grant minimal necessary permissions:**
- Use narrow resource patterns (e.g., `config/*.json` not `*`)
- Limit operations (e.g., `{read}` not `{read, write, execute}`)
- Set time windows (e.g., `expires_in=timedelta(hours=1)`)
- Restrict usage counts (e.g., `max_usage_count=10`)

**Example:**
```python
# BAD: Too permissive
bad_token = create_capability_token(
    capability_type="file",
    resource_patterns=["*"],  # Everything!
    allowed_operations={"read", "write", "execute", "delete"}  # All operations!
)

# GOOD: Minimal necessary
good_token = create_capability_token(
    capability_type="file",
    resource_patterns=["config/*.json"],  # Only config JSON files
    allowed_operations={"read"},  # Read-only
    expires_in=timedelta(minutes=5),  # Short-lived
    max_usage_count=1  # Single use
)
```

### Defense in Depth

The capability system is one layer in a multi-layer security model:

1. **ML Security Analysis (Static)**
   - Parse-time security checks
   - Malicious pattern detection
   - Data flow analysis
   - Pre-transpilation validation

2. **Capability System (Dynamic)**
   - Runtime permission checks
   - Token-based access control
   - Usage monitoring and limits
   - Context isolation

3. **Sandbox Isolation (Process-Level)**
   - True process separation
   - Resource limit enforcement (CPU, memory, time)
   - Capability serialization across boundaries
   - Subprocess monitoring

4. **Safe Attribute Registry (API-Level)**
   - Whitelist-based Python API access
   - Attribute/method access control
   - Type-safe operations
   - ML-Python boundary enforcement

**All layers work together to provide comprehensive security.**

---

## Integration with ML Language

### Capability Declaration Syntax

```ml
capability CapabilityName {
    resource "pattern1";
    resource "pattern2";
    allow operation1;
    allow operation2;
}
```

### Generated Python Structure

```python
def _create_CapabilityName_capability():
    return create_capability_token(
        capability_type="CapabilityName",
        resource_patterns=["pattern1", "pattern2"],
        allowed_operations={"operation1", "operation2"}
    )

@contextlib.contextmanager
def CapabilityName_context():
    manager = get_capability_manager()
    token = _create_CapabilityName_capability()
    with manager.capability_context("CapabilityName_context", [token]):
        yield
```

### Usage in ML Programs

```ml
capability FileReader {
    resource "*.txt";
    allow read;
}

function processFiles() {
    // This code runs with FileReader capability
    files = directory.list("*.txt");
    functional.map(fn(f) => file.read(f), files);
}
```

**Transpiled execution:**
```python
with FileReader_context():
    processFiles()  # Runs with file read capability
```

---

## Implementation Details

### Key Files

- `src/mlpy/runtime/capabilities/tokens.py` - Token implementation
- `src/mlpy/runtime/capabilities/context.py` - Context management
- `src/mlpy/runtime/capabilities/manager.py` - Global manager
- `src/mlpy/runtime/capabilities/decorators.py` - Function protection
- `src/mlpy/runtime/capabilities/exceptions.py` - Error types
- `src/mlpy/ml/codegen/python_generator.py` - Capability code generation

### Token Validation Algorithm

```python
def is_valid(token):
    # 1. Check integrity
    if not validate_checksum(token):
        return False

    # 2. Check expiration
    if is_expired(token):
        return False

    # 3. Check usage limits
    if usage_count >= max_usage_count:
        return False

    return True

def can_access_resource(token, resource_path, operation):
    # 1. Validate token
    if not is_valid(token):
        return False

    # 2. Check resource pattern
    if not matches_pattern(resource_path, token.resource_patterns):
        return False

    # 3. Check operation
    if operation not in token.allowed_operations:
        return False

    return True
```

### Context Hierarchy Resolution

```python
def has_capability(context, capability_type):
    # 1. Check local capabilities
    if capability_type in context.local_tokens:
        if context.local_tokens[capability_type].is_valid():
            return True
        else:
            # Remove expired token
            del context.local_tokens[capability_type]

    # 2. Check parent context recursively
    if context.parent_context:
        return has_capability(context.parent_context, capability_type)

    # 3. Not found
    return False
```

---

## Best Practices

### 1. Always Use Minimal Permissions

```ml
// GOOD: Specific and minimal
capability ConfigReader {
    resource "config/*.json";
    allow read;
}

// BAD: Too broad
capability EverythingAccess {
    resource "*";
    allow read;
    allow write;
    allow execute;
}
```

### 2. Set Time Limits for Temporary Operations

```python
# Create time-limited capability for one-time operation
token = create_capability_token(
    capability_type="temporary_file_access",
    resource_patterns=["temp/*.tmp"],
    allowed_operations={"write"},
    expires_in=timedelta(seconds=30),
    max_usage_count=1
)
```

### 3. Use Context Inheritance Wisely

```python
# Create shared base context
with manager.create_file_capability_context(["*.txt"]) as base:
    # Each worker gets isolated child context
    for worker_id in range(10):
        child = base.create_child_context(f"worker_{worker_id}")
        # child inherits file capability, can add worker-specific ones
        start_worker(child)
```

### 4. Validate Capabilities Before Critical Operations

```python
def delete_file(path):
    # Always check capability before destructive operations
    context = get_current_context()

    if not context.can_access_resource("file", path, "delete"):
        raise PermissionError(f"Cannot delete {path}")

    # Record usage
    context.use_capability("file", path, "delete")

    # Perform deletion
    os.remove(path)
```

---

## Conclusion

The mlpy capability system provides **production-ready, enterprise-grade access control** through:

✓ **Unforgeable tokens** with cryptographic integrity
✓ **Fine-grained permissions** at resource + operation level
✓ **Hierarchical contexts** with inheritance
✓ **Automatic enforcement** via decorators and runtime checks
✓ **Comprehensive auditing** with usage tracking
✓ **Thread-safe operations** with proper synchronization
✓ **Self-cleaning lifecycle** with automatic expiration

This is the **primary security mechanism** for enforcing the principle of least privilege in mlpy programs, working in concert with static security analysis and sandbox isolation to provide defense-in-depth protection.
