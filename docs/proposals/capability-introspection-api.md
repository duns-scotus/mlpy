# Capability Introspection API for ML Programs

**Document Type:** Feature Proposal
**Status:** Ready for Review
**Created:** January 21, 2026
**Authors:** mlpy Development Team
**Priority:** High - Developer Experience Enhancement

---

## Executive Summary

### Problem Statement

Currently, ML programs have no way to discover what capabilities they have been granted. The only way to check if a capability is available is to:

1. **Try the operation and catch exceptions:**
   ```ml
   try {
       file.read("data.txt");
   } except (e) {
       print("File read capability not available");
   }
   ```

2. **Read documentation** to understand what capabilities each function requires
3. **Assume capabilities** based on execution context (unreliable)

This creates several issues:
- **Poor Developer Experience:** No way to check capabilities before attempting operations
- **No Defensive Programming:** Can't gracefully handle missing capabilities
- **Difficult Debugging:** Users can't see what permissions their code is running with
- **Security Opacity:** Users don't understand their execution environment

### Proposed Solution

Add three builtin functions for capability introspection:

```ml
// Check if specific capability is available
hasCapability("file.read")  // => true/false

// Get list of all available capabilities
getCapabilities()  // => ["file.read", "file.write", "network.http"]

// Get detailed information about a capability
getCapabilityInfo("file.read")  // => {type: "file.read", patterns: ["*.txt"], ...}
```

### Benefits

1. **Better Developer Experience:** Check capabilities before operations
2. **Defensive Programming:** Graceful degradation when capabilities are missing
3. **Easier Debugging:** Inspect execution environment at runtime
4. **Security Transparency:** Users understand what permissions they have
5. **Documentation Aid:** Self-documenting code that explains permission requirements

### Recommendation

**✅ PROCEED** with implementation - High value, low complexity, no security concerns.

**Estimated Effort:** 2-3 hours (simple builtin function addition)

---

## Table of Contents

1. [Current State Analysis](#current-state-analysis)
2. [Proposed API Design](#proposed-api-design)
3. [Use Cases & Examples](#use-cases--examples)
4. [Security Considerations](#security-considerations)
5. [Implementation Plan](#implementation-plan)
6. [Testing Strategy](#testing-strategy)
7. [Documentation Requirements](#documentation-requirements)
8. [Alternative Approaches](#alternative-approaches)
9. [Conclusion](#conclusion)

---

## Current State Analysis

### Existing Introspection Functions

ML already provides several introspection capabilities in the `builtin` module:

| Function | Purpose | Example |
|----------|---------|---------|
| `typeof(value)` | Get type of value | `typeof(x)  // "number"` |
| `isinstance(value, type)` | Check value type | `isinstance(x, "number")` |
| `help(target)` | Get help text | `help(math.sqrt)` |
| `methods(value)` | List object methods | `methods(myObj)` |
| `modules()` | List available modules | `modules()` |

**Gap:** No capability introspection exists.

### Current Capability System

The capability system exists at the Python runtime level:

```python
# Python: Create capability context
from mlpy.runtime.capabilities import CapabilityContext, CapabilityToken

with CapabilityContext() as ctx:
    ctx.add_capability(CapabilityToken(capability_type='file.read'))
    ctx.add_capability(CapabilityToken(capability_type='file.write'))
    # Execute ML code in this context
```

**Problem:** ML code has no visibility into this context.

### Current Exception-Based Discovery

```ml
// Only way to check capabilities currently
hasFileRead = false;
try {
    file.read("test.txt");
    hasFileRead = true;
} except {
    hasFileRead = false;
}
```

**Issues:**
- Verbose and error-prone
- Requires actual file to exist
- May trigger side effects
- Doesn't work for checking capabilities before operations

---

## Proposed API Design

### Function 1: `hasCapability(name)`

Check if a specific capability is available.

**Signature:**
```ml
hasCapability(name: string) -> boolean
```

**Parameters:**
- `name`: Capability type string (e.g., `"file.read"`, `"network.http"`)

**Returns:**
- `true` if capability is available and valid
- `false` if capability is not available or expired

**Examples:**
```ml
// Check before attempting operation
if (hasCapability("file.read")) {
    content = file.read("data.txt");
} else {
    print("File reading not permitted");
}

// Check multiple capabilities
if (hasCapability("file.read") && hasCapability("file.write")) {
    processFiles();
}

// Feature detection
hasNetwork = hasCapability("network.http");
```

**Implementation:**
```python
@ml_function(description="Check if capability is available", capabilities=[])
def hasCapability(self, name: str) -> bool:
    """Check if a specific capability is available in current context.

    Args:
        name: Capability type (e.g., "file.read", "network.http")

    Returns:
        True if capability is available, False otherwise
    """
    from mlpy.runtime.whitelist_validator import get_current_capability_context

    context = get_current_capability_context()
    if not context:
        return False

    return context.has_capability(name, check_parents=True)
```

---

### Function 2: `getCapabilities()`

Get list of all available capabilities.

**Signature:**
```ml
getCapabilities() -> array<string>
```

**Parameters:** None

**Returns:**
- Array of capability type strings
- Empty array if no capabilities available
- Includes parent context capabilities (inherited)

**Examples:**
```ml
// List all capabilities
caps = getCapabilities();
print("Available capabilities:");
for (cap in caps) {
    print("  - " + cap);
}

// Check if any file operations allowed
caps = getCapabilities();
hasAnyFileAccess = false;
for (cap in caps) {
    if (cap == "file.read" || cap == "file.write") {
        hasAnyFileAccess = true;
    }
}

// Defensive initialization based on available capabilities
function initialize() {
    caps = getCapabilities();
    print("Initializing with capabilities: " + str(caps));

    // Configure features based on capabilities
    if (hasCapability("network.http")) {
        initializeNetworking();
    }
    if (hasCapability("file.read")) {
        loadConfiguration();
    }
}
```

**Implementation:**
```python
@ml_function(description="Get all available capabilities", capabilities=[])
def getCapabilities(self) -> list:
    """Get list of all available capability types.

    Returns:
        List of capability type strings, or empty list if no context
    """
    from mlpy.runtime.whitelist_validator import get_current_capability_context

    context = get_current_capability_context()
    if not context:
        return []

    # Get all capabilities (including inherited from parents)
    all_caps = context.get_all_capabilities(include_parents=True)
    return sorted(all_caps.keys())
```

---

### Function 3: `getCapabilityInfo(name)` (Advanced)

Get detailed information about a capability.

**Signature:**
```ml
getCapabilityInfo(name: string) -> object | null
```

**Parameters:**
- `name`: Capability type string

**Returns:**
- Object with capability details (type, patterns, constraints)
- `null` if capability not available

**Return Object Structure:**
```ml
{
    type: "file.read",              // Capability type
    available: true,                 // Is it available?
    patterns: ["*.txt", "data/*"],  // Resource patterns (if applicable)
    operations: ["read"],            // Allowed operations (if applicable)
    expires_at: null,                // Expiration time (null = no expiration)
    usage_count: 5,                  // Times this capability has been used
    max_usage: null                  // Max usage limit (null = unlimited)
}
```

**Examples:**
```ml
// Get detailed info
info = getCapabilityInfo("file.read");
if (info != null) {
    print("File read capability:");
    print("  Patterns: " + str(info.patterns));
    print("  Usage: " + str(info.usage_count) + " times");
}

// Check resource pattern restrictions
info = getCapabilityInfo("file.read");
if (info != null && info.patterns != null) {
    print("Can only read files matching: " + str(info.patterns));
}

// Check usage limits
info = getCapabilityInfo("network.http");
if (info != null && info.max_usage != null) {
    remaining = info.max_usage - info.usage_count;
    print("HTTP requests remaining: " + str(remaining));
}
```

**Implementation:**
```python
@ml_function(description="Get detailed capability information", capabilities=[])
def getCapabilityInfo(self, name: str) -> dict | None:
    """Get detailed information about a specific capability.

    Args:
        name: Capability type (e.g., "file.read")

    Returns:
        Dictionary with capability details, or None if not available
    """
    from mlpy.runtime.whitelist_validator import get_current_capability_context

    context = get_current_capability_context()
    if not context:
        return None

    # Get capability token
    token = context.get_capability_token(name)
    if not token:
        return None

    # Build info object
    info = {
        'type': token.capability_type,
        'available': token.is_valid(),
        'usage_count': token.usage_count,
    }

    # Add constraint details if available
    if token.constraints:
        info['patterns'] = token.constraints.resource_patterns if token.constraints.resource_patterns else None
        info['operations'] = list(token.constraints.allowed_operations) if token.constraints.allowed_operations else None
        info['max_usage'] = token.constraints.max_usage_count
        info['expires_at'] = token.constraints.expires_at.isoformat() if token.constraints.expires_at else None
    else:
        info['patterns'] = None
        info['operations'] = None
        info['max_usage'] = None
        info['expires_at'] = None

    return info
```

---

## Use Cases & Examples

### Use Case 1: Defensive Feature Detection

**Scenario:** Library code that gracefully degrades based on available capabilities.

```ml
// Library: data_processor.ml
function loadData(source) {
    // Check if file reading is available
    if (hasCapability("file.read")) {
        return loadFromFile(source);
    } elif (hasCapability("network.http")) {
        return loadFromUrl(source);
    } else {
        print("ERROR: No data loading capabilities available");
        print("Required: file.read OR network.http");
        return null;
    }
}

function saveData(destination, data) {
    // Check if file writing is available
    if (hasCapability("file.write")) {
        return saveToFile(destination, data);
    } elif (hasCapability("network.http")) {
        return uploadToServer(destination, data);
    } else {
        print("WARNING: No data saving capabilities");
        print("Data will be lost when program exits");
        return false;
    }
}
```

---

### Use Case 2: Capability Validation on Startup

**Scenario:** Application that requires specific capabilities to function.

```ml
// App startup validation
function main() {
    print("Checking required capabilities...");

    required = ["file.read", "file.write", "network.http"];
    missing = [];

    for (cap in required) {
        if (!hasCapability(cap)) {
            missing = missing + [cap];
        }
    }

    if (missing != []) {
        print("ERROR: Missing required capabilities:");
        for (cap in missing) {
            print("  - " + cap);
        }
        print("");
        print("This application requires the following permissions:");
        print("  file.read  - Read configuration and data files");
        print("  file.write - Save results and logs");
        print("  network.http - Fetch remote data");
        print("");
        print("Please grant these capabilities and try again.");
        return 1;
    }

    print("All capabilities available. Starting application...");
    runApplication();
    return 0;
}
```

---

### Use Case 3: Debug Information

**Scenario:** Developer debugging capability issues.

```ml
// Debug: Print execution environment
function debugEnvironment() {
    print("=== Execution Environment ===");
    print("Available modules: " + str(modules()));
    print("");

    caps = getCapabilities();
    print("Available capabilities (" + str(len(caps)) + "):");

    if (caps == []) {
        print("  (none - running in restricted mode)");
    } else {
        for (cap in caps) {
            print("  - " + cap);

            // Show detailed info
            info = getCapabilityInfo(cap);
            if (info != null && info.patterns != null) {
                print("    Patterns: " + str(info.patterns));
            }
        }
    }
    print("");
}

// Call at program start for debugging
debugEnvironment();
```

---

### Use Case 4: Progressive Enhancement

**Scenario:** Application that adds features based on available capabilities.

```ml
// Configure application based on capabilities
function configureApp() {
    config = {
        features: [],
        fileAccess: false,
        networkAccess: false,
        persistentData: false
    };

    // Check file capabilities
    if (hasCapability("file.read")) {
        config.fileAccess = true;
        config.features = config.features + ["load-files"];

        if (hasCapability("file.write")) {
            config.persistentData = true;
            config.features = config.features + ["save-files", "export-data"];
        }
    }

    // Check network capabilities
    if (hasCapability("network.http")) {
        config.networkAccess = true;
        config.features = config.features + ["sync-cloud", "fetch-updates"];
    }

    print("Configured with features: " + str(config.features));
    return config;
}

config = configureApp();
```

---

### Use Case 5: Resource Constraint Awareness

**Scenario:** Application that adapts behavior based on capability constraints.

```ml
// Check if we can access specific file patterns
function canAccessFile(filepath) {
    info = getCapabilityInfo("file.read");

    if (info == null) {
        return false;
    }

    // If no patterns specified, can access any file
    if (info.patterns == null) {
        return true;
    }

    // Check if filepath matches any pattern
    // (simplified - real implementation would use regex/glob matching)
    for (pattern in info.patterns) {
        if (filepath == pattern) {
            return true;
        }
    }

    return false;
}

// Check usage limits before batch operation
function canPerformBatchRequest(count) {
    info = getCapabilityInfo("network.http");

    if (info == null) {
        return false;
    }

    // Check if we have usage limits
    if (info.max_usage != null) {
        remaining = info.max_usage - info.usage_count;
        return remaining >= count;
    }

    // No limits - can proceed
    return true;
}
```

---

## Security Considerations

### Is Capability Disclosure a Security Risk?

**Question:** Should malicious code be able to query capabilities?

**Answer:** ✅ **No security risk** - Transparency is beneficial.

**Reasoning:**

1. **Code Already Has Capabilities:** If code is running with capabilities, it can already use them. Knowing about them doesn't add attack surface.

2. **Try-Catch Alternative Exists:** Malicious code can already probe capabilities via exception handling:
   ```ml
   try {
       file.read("test.txt");  // Now I know I have file.read
   } except {
       // Don't have file.read
   }
   ```

3. **Transparency Improves Security:**
   - Users can see what permissions their code is running with
   - Debugging is easier (less frustration, fewer security bypasses)
   - Self-documenting code makes permission requirements explicit

4. **Capability Context is Intentional:** The Python code that grants capabilities has already made a security decision. ML code should be able to see that decision.

5. **No Privilege Escalation:** Knowing about capabilities doesn't grant them. You can only check what you already have.

### Potential Concerns

| Concern | Mitigation |
|---------|-----------|
| **Probing for vulnerabilities** | Code can already probe via try-catch; introspection is more explicit and auditable |
| **Exposing internal details** | Only expose capability types and constraints, not tokens or internal IDs |
| **Information leakage** | Capability context is intentionally created by host application - not a leak |
| **Attack fingerprinting** | Attackers already know common capability sets from documentation |

**Conclusion:** ✅ Safe to implement - no new security risks introduced.

---

## Implementation Plan

### Phase 1: Core Functions (1-2 hours)

**Add to `src/mlpy/stdlib/builtin.py`:**

1. **hasCapability(name)**
   - Check current context
   - Query `context.has_capability(name)`
   - Return boolean

2. **getCapabilities()**
   - Check current context
   - Query `context.get_all_capabilities()`
   - Return sorted list of capability type strings

3. **getCapabilityInfo(name)**
   - Check current context
   - Get capability token
   - Extract relevant details (type, constraints, usage)
   - Return dictionary (or null if not found)

### Phase 2: Testing (1 hour)

**Test file:** `tests/unit/test_capability_introspection.py`

Test scenarios:
- Functions return correct values when capability context exists
- Functions handle missing context gracefully (return false/empty/null)
- hasCapability returns correct boolean
- getCapabilities returns all capabilities (including inherited)
- getCapabilityInfo returns accurate constraint information
- Functions work correctly in ML code execution

### Phase 3: Documentation (30 minutes)

1. **Add to ML Language Reference:**
   - Document all three functions
   - Include examples
   - Explain return values

2. **Add to Capability System Guide:**
   - Explain introspection capabilities
   - Show best practices
   - Include defensive programming patterns

3. **Update Builtin Module Docs:**
   - Add to introspection section
   - Cross-reference capability documentation

### Phase 4: Examples (30 minutes)

Create example ML programs:
1. **capability_check.ml** - Basic capability checking
2. **defensive_features.ml** - Graceful degradation
3. **debug_environment.ml** - Debug info printing

---

## Testing Strategy

### Unit Tests

```python
# tests/unit/test_capability_introspection.py

def test_has_capability_returns_true_when_available():
    """Test hasCapability returns true for granted capabilities."""
    from mlpy.stdlib.builtin import builtin
    from mlpy.runtime.capabilities import CapabilityContext, CapabilityToken
    from mlpy.runtime.whitelist_validator import set_capability_context

    with CapabilityContext() as ctx:
        ctx.add_capability(CapabilityToken(capability_type='file.read'))
        set_capability_context(ctx)

        assert builtin.hasCapability('file.read') == True
        assert builtin.hasCapability('file.write') == False

        set_capability_context(None)


def test_has_capability_returns_false_when_no_context():
    """Test hasCapability returns false when no context."""
    from mlpy.stdlib.builtin import builtin
    from mlpy.runtime.whitelist_validator import set_capability_context

    set_capability_context(None)
    assert builtin.hasCapability('file.read') == False


def test_get_capabilities_returns_all_capabilities():
    """Test getCapabilities returns complete list."""
    from mlpy.stdlib.builtin import builtin
    from mlpy.runtime.capabilities import CapabilityContext, CapabilityToken
    from mlpy.runtime.whitelist_validator import set_capability_context

    with CapabilityContext() as ctx:
        ctx.add_capability(CapabilityToken(capability_type='file.read'))
        ctx.add_capability(CapabilityToken(capability_type='file.write'))
        ctx.add_capability(CapabilityToken(capability_type='network.http'))
        set_capability_context(ctx)

        caps = builtin.getCapabilities()
        assert sorted(caps) == ['file.read', 'file.write', 'network.http']

        set_capability_context(None)


def test_get_capability_info_returns_details():
    """Test getCapabilityInfo returns accurate details."""
    from mlpy.stdlib.builtin import builtin
    from mlpy.runtime.capabilities import CapabilityContext, CapabilityToken, CapabilityConstraint
    from mlpy.runtime.whitelist_validator import set_capability_context

    constraint = CapabilityConstraint(
        resource_patterns=['*.txt'],
        allowed_operations={'read'},
        max_usage_count=10
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
        assert info['patterns'] == ['*.txt']
        assert info['operations'] == ['read']
        assert info['max_usage'] == 10

        set_capability_context(None)
```

### Integration Tests

```ml
// tests/ml_integration/capability_introspection.ml

// Test hasCapability
function testHasCapability() {
    // Should return true for granted capabilities
    result = hasCapability("file.read");
    print("hasCapability('file.read'): " + str(result));

    // Should return false for non-granted capabilities
    result = hasCapability("non.existent");
    print("hasCapability('non.existent'): " + str(result));
}

// Test getCapabilities
function testGetCapabilities() {
    caps = getCapabilities();
    print("Available capabilities: " + str(caps));
    print("Count: " + str(len(caps)));
}

// Test getCapabilityInfo
function testGetCapabilityInfo() {
    info = getCapabilityInfo("file.read");
    if (info != null) {
        print("Capability info:");
        print("  Type: " + info.type);
        print("  Available: " + str(info.available));
        print("  Usage: " + str(info.usage_count));
    } else {
        print("No info available");
    }
}

// Run tests
testHasCapability();
testGetCapabilities();
testGetCapabilityInfo();
```

---

## Documentation Requirements

### 1. ML Language Reference Update

Add new section: **Capability Introspection**

```markdown
## Capability Introspection

ML programs can query their execution environment to discover available capabilities.

### hasCapability(name)

Check if a specific capability is available.

**Syntax:** `hasCapability(name: string) -> boolean`

**Examples:**
```ml
if (hasCapability("file.read")) {
    data = file.read("input.txt");
}
```

### getCapabilities()

Get list of all available capabilities.

**Syntax:** `getCapabilities() -> array<string>`

**Examples:**
```ml
caps = getCapabilities();
print("Capabilities: " + str(caps));
```

### getCapabilityInfo(name)

Get detailed information about a capability.

**Syntax:** `getCapabilityInfo(name: string) -> object | null`

**Examples:**
```ml
info = getCapabilityInfo("file.read");
if (info != null) {
    print("Patterns: " + str(info.patterns));
}
```
```

### 2. Capability System Guide Update

Add section on **Runtime Introspection**:

- Explain when to use capability checking
- Show defensive programming patterns
- Document best practices
- Include complete examples

### 3. Builtin Module Documentation

Update builtin module docs to include introspection functions in the table.

---

## Alternative Approaches

### Alternative 1: Single Function with Mode Parameter

```ml
// Single function with different modes
capability("check", "file.read")    // => true/false
capability("list")                   // => ["file.read", ...]
capability("info", "file.read")     // => {type: "file.read", ...}
```

**Pros:**
- Single function to remember
- Consistent naming

**Cons:**
- Less discoverable (mode strings are magic)
- Less type-safe
- Harder to document
- Non-idiomatic for ML

**Recommendation:** ❌ Reject - Multiple specific functions are clearer.

---

### Alternative 2: Capability Object API

```ml
// Get capability manager object
capMgr = getCapabilityManager();

// Use object methods
capMgr.has("file.read")
capMgr.list()
capMgr.info("file.read")
```

**Pros:**
- Object-oriented approach
- Namespace isolation

**Cons:**
- More complex for simple checks
- Requires object creation
- Less convenient for common case

**Recommendation:** ❌ Reject - Simple functions are more ergonomic.

---

### Alternative 3: Exception-Based Only (Status Quo)

```ml
// Only use try-catch for capability detection
try {
    file.read("test.txt");
    hasFileRead = true;
} except {
    hasFileRead = false;
}
```

**Pros:**
- No new API surface
- Works today

**Cons:**
- Verbose and error-prone
- Requires side effects (actually trying operations)
- Can't check before attempting
- Poor developer experience
- Doesn't work for checking constraints

**Recommendation:** ❌ Reject - Major UX issues, not a real alternative.

---

## Conclusion

### Summary

This proposal adds three builtin functions for capability introspection:

1. **hasCapability(name)** - Simple boolean check
2. **getCapabilities()** - List all available capabilities
3. **getCapabilityInfo(name)** - Get detailed capability information

**Benefits:**
- ✅ Better developer experience
- ✅ Defensive programming support
- ✅ Easier debugging
- ✅ Security transparency
- ✅ Self-documenting code

**Costs:**
- Minimal implementation effort (2-3 hours)
- Small API surface increase (3 functions)
- Documentation updates needed

**Security:**
- ✅ No new security risks
- ✅ Transparency improves security
- ✅ No privilege escalation possible

### Recommendation

**✅ STRONGLY RECOMMEND IMPLEMENTATION**

**Reasoning:**

1. **High Value:** Significantly improves developer experience with minimal cost
2. **Low Complexity:** Simple implementation using existing capability system
3. **No Security Issues:** Capability disclosure is safe and beneficial
4. **Fills Obvious Gap:** Introspection exists for types, modules, methods - should exist for capabilities
5. **Enables Best Practices:** Defensive programming, graceful degradation, clear error messages
6. **Quick Win:** 2-3 hours of work for substantial UX improvement

### Priority

**HIGH** - Should be implemented before GUI bridge or other major features.

**Rationale:** This is foundational infrastructure that will benefit all future capability-protected features (file I/O, networking, GUI, database, etc.). Implementing it early means better examples and better developer experience for all subsequent work.

---

## Next Steps

If approved:

1. **Immediate:** Implement three functions in `builtin.py` (1-2 hours)
2. **Testing:** Add unit and integration tests (1 hour)
3. **Documentation:** Update language reference and capability guide (30 minutes)
4. **Examples:** Create example ML programs (30 minutes)
5. **Review:** Code review and merge

**Total Effort:** ~3 hours from approval to completion

---

**Document Status:** Ready for Review and Approval
**Implementation Complexity:** Low (2-3 hours)
**Value:** High (Major DX improvement)
**Security Impact:** None (Safe to implement)
**Recommendation:** ✅ **PROCEED WITH IMPLEMENTATION**

---

**Document Metadata:**
- Created: January 21, 2026
- Last Updated: January 21, 2026
- Version: 1.0
- Authors: mlpy Development Team
