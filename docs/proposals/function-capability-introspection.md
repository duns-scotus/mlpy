# Function Capability Introspection Proposal

**Date:** October 27, 2025
**Status:** ✅ COMPLETED - October 27, 2025
**Priority:** Medium - Developer Experience Enhancement
**Complexity:** Low
**Estimated Effort:** 2-3 hours (Actual: ~2 hours)

---

## ✅ Implementation Status

**Completion Date:** October 27, 2025

### Completed Deliverables

1. ✅ **Implementation**
   - `requiredCapabilities()` function implemented in `src/mlpy/stdlib/builtin.py:651-716`
   - Enhanced `help()` function in `src/mlpy/stdlib/builtin.py:317-370`
   - Full metadata inspection support for `@ml_function` and `@ml_class` decorators

2. ✅ **Testing**
   - 8 comprehensive unit tests in `tests/unit/stdlib/test_builtin.py:531-643`
   - All unit tests passing (100% success rate)
   - ML integration test in `tests/ml_integration/ml_core/test_capability_introspection.ml`
   - Integration test successfully executes in sandbox

3. ✅ **Documentation**
   - Complete documentation added to `docs/source/user-guide/language-reference/builtin-functions.rst`
   - New "Capability Introspection" section with detailed examples
   - Enhanced `help()` documentation showing capability output format
   - Updated summary section with new functions

### Test Results

**Unit Tests:** 8/8 passing
- `test_required_capabilities_with_metadata` ✅
- `test_required_capabilities_no_metadata` ✅
- `test_required_capabilities_empty_capabilities` ✅
- `test_required_capabilities_builtin_functions` ✅
- `test_help_includes_capabilities` ✅
- `test_help_multiple_capabilities` ✅
- `test_help_no_capabilities_message` ✅
- `test_help_no_metadata_no_capability_info` ✅

**Integration Test:** Successful execution demonstrating all patterns

### Files Modified

- `src/mlpy/stdlib/builtin.py` - Added `requiredCapabilities()`, enhanced `help()`
- `tests/unit/stdlib/test_builtin.py` - Added comprehensive test suite
- `tests/ml_integration/ml_core/test_capability_introspection.ml` - Added integration test
- `docs/source/user-guide/language-reference/builtin-functions.rst` - Added complete documentation

---

## Executive Summary

ML programmers can currently check what capabilities *they have* (`hasCapability()`, `getCapabilities()`, `getCapabilityInfo()`), but they cannot inspect what capabilities *a function requires*. This proposal adds function capability introspection to enable defensive programming, better error messages, and graceful degradation.

**Current Gap:**
```ml
import file;

// ✅ Can check: "Do I have file.read capability?"
if (hasCapability("file.read")) {
    content = file.read("data.txt");
}

// ❌ Cannot check: "What capabilities does file.read() need?"
// ❌ Cannot check: "Can I call this function with my current capabilities?"
```

**Proposed Solution:**
1. Add new builtin: `requiredCapabilities(func)` - Returns list of required capabilities
2. Enhance `help(func)` - Include capability requirements in help text

---

## Problem Analysis

### Current Capability Introspection

The ML standard library provides three capability introspection functions:

```ml
// Check if specific capability is available
hasCapability("file.read") => true/false

// Get all available capabilities
getCapabilities() => ["file.read", "file.write", "network.http"]

// Get detailed capability information
getCapabilityInfo("file.read") => {
    type: "file.read",
    available: true,
    patterns: ["*.txt"],
    usage_count: 5
}
```

These functions answer: **"What capabilities do I have?"**

### The Missing Piece

No functions answer: **"What capabilities does this function need?"**

**Real-World Scenario:**
```ml
import file;
import http;

// Developer wants to know if they can call these functions
// Currently: trial and error, wait for CapabilityError
// Desired: proactive checking before calling

// Which capabilities do these need?
content = file.read("data.txt");        // Need: file.read
file.write("output.txt", content);      // Need: file.write
response = http.get("https://api.com"); // Need: network.http

// How can I check programmatically?
```

### Why This Matters

**1. Defensive Programming**
```ml
// Currently: Try and handle error
try {
    content = file.read("data.txt");
} except (e) {
    print("Failed: " + e.message);  // Vague error
}

// Proposed: Check requirements first
caps = requiredCapabilities(file.read);
hasAll = true;
for (cap in caps) {
    if (!hasCapability(cap)) {
        print("Missing required capability: " + cap);
        hasAll = false;
    }
}
if (hasAll) {
    content = file.read("data.txt");
}
```

**2. Better Error Messages**
```ml
// Currently: Generic capability error at runtime
// Proposed: Specific, helpful message before attempting

missing = [];
for (cap in requiredCapabilities(file.write)) {
    if (!hasCapability(cap)) {
        missing.push(cap);
    }
}
if (len(missing) > 0) {
    print("Cannot call file.write() - missing capabilities: " + str(missing));
    print("Request these capabilities in your capability block");
}
```

**3. Graceful Degradation**
```ml
// Provide fallback when capabilities unavailable
function saveData(data) {
    if (hasCapability("file.write")) {
        file.write("cache.json", data);
    } else {
        print("Note: File writing unavailable, data not cached");
    }
}

// Or check function requirements dynamically
function canUseFunction(func) {
    caps = requiredCapabilities(func);
    for (cap in caps) {
        if (!hasCapability(cap)) {
            return false;
        }
    }
    return true;
}

if (canUseFunction(file.write)) {
    file.write("data.txt", content);
} else {
    print("File writing not available");
}
```

**4. Interactive Development**
```ml
// Explore capabilities interactively
import file;

help(file.read);              // Shows description + capabilities
caps = requiredCapabilities(file.read);  // ["file.read"]
info = getCapabilityInfo(caps[0]);       // Check if available
```

---

## Proposed Solution

### Part 1: New Builtin - `requiredCapabilities(func)`

Add a new builtin function that returns the capability requirements of any function.

**Signature:**
```python
def requiredCapabilities(func: Callable) -> list[str]
```

**Behavior:**
- Returns list of capability type strings required by the function
- Returns empty list if function requires no capabilities
- Returns empty list if function has no metadata (e.g., Python built-ins)
- Works with any callable: module functions, methods, lambdas

**Examples:**
```ml
import file;
import console;

// Check file function requirements
caps = requiredCapabilities(file.read);
print(caps);  // ["file.read"]

caps = requiredCapabilities(file.write);
print(caps);  // ["file.write"]

// Check console functions (no capabilities needed)
caps = requiredCapabilities(console.log);
print(caps);  // []

// Check builtins (no capabilities needed)
caps = requiredCapabilities(print);
print(caps);  // []

// Check custom function
function myFunc() {
    return file.read("data.txt");
}
caps = requiredCapabilities(myFunc);
print(caps);  // [] (myFunc itself has no declared capabilities)
```

**Integration with Existing Functions:**

The new function complements the existing capability introspection trio:

```ml
// Context capabilities (what I have)
hasCapability("file.read")         // Do I have this specific capability?
getCapabilities()                   // What capabilities do I have?
getCapabilityInfo("file.read")     // Detailed info about my capability

// Function capabilities (what function needs)
requiredCapabilities(file.read)    // What does this function need?

// Combined usage
function canCall(func) {
    required = requiredCapabilities(func);
    for (cap in required) {
        if (!hasCapability(cap)) {
            return false;
        }
    }
    return true;
}

if (canCall(file.read)) {
    content = file.read("data.txt");
}
```

### Part 2: Enhanced `help(func)`

Update the existing `help()` function to include capability requirements in its output.

**Current Behavior:**
```ml
help(file.read);
// Returns: "Read file contents from path"
```

**Proposed Behavior:**
```ml
help(file.read);
// Returns: "Read file contents from path\nRequires: file.read"

help(console.log);
// Returns: "Print message to console\nCapabilities: None required"

help(print);
// Returns: "Print value to console\nCapabilities: None required"
```

**Format:**
- If function requires capabilities: Append `\nRequires: cap1, cap2, cap3`
- If function requires no capabilities: Append `\nCapabilities: None required`
- If function has no metadata: Existing behavior (no capability info)

**Examples:**
```ml
import file;
import http;

// Single capability
print(help(file.read));
// Output:
// Read file contents from path
// Requires: file.read

// Multiple capabilities (if any future functions have multiple)
print(help(someFunction));
// Output:
// Do something complex
// Requires: file.read, network.http

// No capabilities
print(help(console.log));
// Output:
// Print message to console
// Capabilities: None required
```

---

## Implementation Details

### Implementation for `requiredCapabilities(func)`

**Location:** `src/mlpy/stdlib/builtin.py`

**Add after existing capability functions (line ~624):**

```python
@ml_function(description="Get list of capabilities required by function", capabilities=[])
def requiredCapabilities(self, func: Callable) -> list:
    """Get list of capabilities required by a function.

    Inspects function metadata to determine what capabilities it needs.
    Returns empty list if function requires no capabilities or has no metadata.

    Args:
        func: Function or callable to inspect

    Returns:
        List of capability type strings (e.g., ["file.read", "network.http"])
        Empty list if no capabilities required

    Examples:
        import file;

        // Check file.read requirements
        caps = requiredCapabilities(file.read);
        print(caps);  // ["file.read"]

        // Check if we can call it
        canCall = true;
        for (cap in caps) {
            if (!hasCapability(cap)) {
                print("Missing: " + cap);
                canCall = false;
            }
        }

        if (canCall) {
            content = file.read("data.txt");
        }

        // Check builtin (no requirements)
        caps = requiredCapabilities(print);
        print(caps);  // []

        // Utility function for checking callability
        function canExecute(fn) {
            required = requiredCapabilities(fn);
            for (cap in required) {
                if (!hasCapability(cap)) {
                    return false;
                }
            }
            return true;
        }
    """
    # Check for @ml_function metadata
    if hasattr(func, '_ml_function_metadata'):
        metadata = func._ml_function_metadata
        return list(metadata.capabilities) if metadata.capabilities else []

    # Check for @ml_class metadata on methods
    if hasattr(func, '__self__'):
        obj = func.__self__
        if hasattr(type(obj), '_ml_class_metadata'):
            class_meta = type(obj)._ml_class_metadata
            method_name = func.__name__
            if method_name in class_meta.methods:
                method_meta = class_meta.methods[method_name]
                return list(method_meta.capabilities) if method_meta.capabilities else []

    # No metadata or no capabilities
    return []
```

### Implementation for Enhanced `help(func)`

**Location:** `src/mlpy/stdlib/builtin.py`

**Update existing `help()` function (line ~318):**

```python
@ml_function(description="Get help for function or module", capabilities=[])
def help(self, target: Any) -> str:
    """Show documentation for function, method, or module.

    Includes capability requirements if the function has metadata.

    Args:
        target: Function, method, or module to get help for

    Returns:
        Documentation string with capabilities info if available

    Examples:
        help(string.upper) => "Convert string to uppercase\nCapabilities: None required"
        help(file.read) => "Read file contents from path\nRequires: file.read"
        help(console) => "Console output and logging module"
    """
    description = None
    capabilities = None

    # Check for @ml_function metadata
    if hasattr(target, '_ml_function_metadata'):
        metadata = target._ml_function_metadata
        description = metadata.description if metadata.description else 'No description available'
        capabilities = metadata.capabilities

    # Check for @ml_module metadata
    elif hasattr(target, '_ml_module_metadata'):
        metadata = target._ml_module_metadata
        description = metadata.description if metadata.description else 'No description available'
        capabilities = metadata.capabilities

    # Check for @ml_class metadata
    elif hasattr(type(target), '_ml_class_metadata'):
        metadata = type(target)._ml_class_metadata
        description = metadata.description if metadata.description else 'No description available'
        capabilities = metadata.capabilities

    # Fallback to docstring
    elif hasattr(target, '__doc__') and target.__doc__:
        description = target.__doc__.strip()

    else:
        return f"No help available for {target}"

    # Add capability information
    if capabilities is not None:
        if capabilities and len(capabilities) > 0:
            cap_str = ", ".join(capabilities)
            description += f"\nRequires: {cap_str}"
        else:
            description += "\nCapabilities: None required"

    return description
```

---

## Usage Examples

### Example 1: Defensive File Operations

```ml
import file;

function safeReadFile(path) {
    // Check if we can call file.read
    required = requiredCapabilities(file.read);

    for (cap in required) {
        if (!hasCapability(cap)) {
            print("Error: Cannot read files - missing capability: " + cap);
            print("Add this to your capability block:");
            print("  capability FileRead {");
            print("    allow read;");
            print("  }");
            return null;
        }
    }

    // Safe to call
    return file.read(path);
}

content = safeReadFile("data.txt");
if (content != null) {
    print("Success: " + content);
}
```

### Example 2: Feature Detection

```ml
import file;
import http;

// Check what operations are available
print("Available operations:");

if (len(requiredCapabilities(file.read)) == 0 ||
    hasCapability(requiredCapabilities(file.read)[0])) {
    print("  ✓ File reading");
} else {
    print("  ✗ File reading (requires: " + str(requiredCapabilities(file.read)) + ")");
}

if (len(requiredCapabilities(http.get)) == 0 ||
    hasCapability(requiredCapabilities(http.get)[0])) {
    print("  ✓ HTTP requests");
} else {
    print("  ✗ HTTP requests (requires: " + str(requiredCapabilities(http.get)) + ")");
}
```

### Example 3: Interactive Exploration

```ml
import file;

// Get help with capabilities
print(help(file.read));
// Output:
// Read file contents from path
// Requires: file.read

print(help(file.write));
// Output:
// Write content to file
// Requires: file.write

// Check requirements programmatically
readCaps = requiredCapabilities(file.read);
writeCaps = requiredCapabilities(file.write);

print("File operations require:");
print("  Reading: " + str(readCaps));
print("  Writing: " + str(writeCaps));

// Check what we have
print("Current capabilities: " + str(getCapabilities()));

// Check each requirement
for (cap in readCaps) {
    if (hasCapability(cap)) {
        print("  ✓ Have " + cap);
    } else {
        print("  ✗ Missing " + cap);
        info = getCapabilityInfo(cap);
        if (info != null) {
            print("    Details: " + str(info));
        }
    }
}
```

### Example 4: Utility Helper Function

```ml
// Reusable helper for capability checking
function checkFunctionAccess(func, funcName) {
    required = requiredCapabilities(func);

    if (len(required) == 0) {
        print(funcName + " requires no capabilities - always available");
        return true;
    }

    print(funcName + " requires capabilities: " + str(required));

    missing = [];
    for (cap in required) {
        if (hasCapability(cap)) {
            print("  ✓ Have " + cap);
        } else {
            print("  ✗ Missing " + cap);
            missing.push(cap);
        }
    }

    return len(missing) == 0;
}

// Use it
import file;
import console;

if (checkFunctionAccess(file.read, "file.read")) {
    content = file.read("data.txt");
}

if (checkFunctionAccess(console.log, "console.log")) {
    console.log("Logging is available");
}
```

---

## Documentation Updates

### Update: User Guide - Builtin Functions

**File:** `docs/source/user-guide/language-reference/builtin-functions.rst`

**Section:** "Capability Introspection Functions"

**Add after `getCapabilityInfo()`:**

```rst
requiredCapabilities(func)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Get the list of capabilities required by a function.

**Signature:**
  ``requiredCapabilities(func: function) -> array``

**Arguments:**
  - ``func``: Function or callable to inspect

**Returns:**
  Array of capability type strings required by the function. Returns empty array if function requires no capabilities or has no metadata.

**Examples:**

.. code-block:: ml

    import file;

    // Check what capabilities a function needs
    caps = requiredCapabilities(file.read);
    print(caps);  // ["file.read"]

    // Check if we can call it
    canCall = true;
    for (cap in caps) {
        if (!hasCapability(cap)) {
            print("Missing capability: " + cap);
            canCall = false;
        }
    }

    if (canCall) {
        content = file.read("data.txt");
    }

    // Check builtin functions (no capabilities needed)
    caps = requiredCapabilities(print);
    print(caps);  // []

**Use Cases:**
  - Defensive programming - check before calling
  - Better error messages with specific missing capabilities
  - Graceful degradation when capabilities unavailable
  - Interactive exploration of function requirements

**See Also:**
  - :ref:`hasCapability` - Check if specific capability available
  - :ref:`getCapabilities` - List all available capabilities
  - :ref:`help` - Get function documentation including capabilities
```

### Update: User Guide - help() Function

**File:** `docs/source/user-guide/language-reference/builtin-functions.rst`

**Section:** "help(target)"

**Update examples to show capability output:**

```rst
help(target)
~~~~~~~~~~~~

Show documentation for function, method, or module. **Now includes capability requirements.**

**Examples:**

.. code-block:: ml

    import file;
    import console;

    // Help includes capability requirements
    print(help(file.read));
    // Output:
    // Read file contents from path
    // Requires: file.read

    print(help(file.write));
    // Output:
    // Write content to file
    // Requires: file.write

    // Functions with no requirements
    print(help(console.log));
    // Output:
    // Print message to console
    // Capabilities: None required

    print(help(print));
    // Output:
    // Print value to console
    // Capabilities: None required
```

### Update: User Guide - Capability System Tutorial

**File:** `docs/source/user-guide/toolkit/capabilities.rst`

**Add new section: "Inspecting Function Requirements"**

```rst
Inspecting Function Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ML provides introspection functions to check what capabilities functions require. This enables defensive programming and better error handling.

Context Capabilities vs. Function Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Context Capabilities** - What capabilities *you have*:

.. code-block:: ml

    // Check if you have a specific capability
    if (hasCapability("file.read")) {
        print("Can read files");
    }

    // List all your capabilities
    caps = getCapabilities();
    print("Available: " + str(caps));

    // Get detailed info about your capability
    info = getCapabilityInfo("file.read");
    print("Patterns: " + str(info.patterns));

**Function Requirements** - What capabilities *a function needs*:

.. code-block:: ml

    import file;

    // Check what a function requires
    required = requiredCapabilities(file.read);
    print("file.read needs: " + str(required));

    // Get help with capability info
    print(help(file.read));
    // Shows description + "Requires: file.read"

Defensive Programming Pattern
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check function requirements before calling:

.. code-block:: ml

    import file;

    function safeFileOperation(path, operation) {
        // Get requirements
        required = requiredCapabilities(operation);

        // Check each requirement
        for (cap in required) {
            if (!hasCapability(cap)) {
                print("Error: Missing capability " + cap);
                print("Cannot execute " + str(operation));
                return null;
            }
        }

        // Safe to call
        return operation(path);
    }

    // Use it
    content = safeFileOperation("data.txt", file.read);
    if (content != null) {
        print(content);
    }

Feature Detection
^^^^^^^^^^^^^^^^^

Enable/disable features based on available capabilities:

.. code-block:: ml

    import file;
    import http;

    function checkAvailableFeatures() {
        features = [];

        // Check file operations
        if (len(requiredCapabilities(file.read)) == 0 ||
            hasCapability("file.read")) {
            features.push("file_reading");
        }

        // Check network operations
        if (len(requiredCapabilities(http.get)) == 0 ||
            hasCapability("network.http")) {
            features.push("http_requests");
        }

        return features;
    }

    available = checkAvailableFeatures();
    print("Available features: " + str(available));

Interactive Exploration
^^^^^^^^^^^^^^^^^^^^^^^

Explore function capabilities interactively:

.. code-block:: ml

    import file;

    // What does this function do and need?
    print(help(file.read));
    // Shows: description + "Requires: file.read"

    // What capabilities does it need?
    caps = requiredCapabilities(file.read);
    print("Requirements: " + str(caps));

    // Do I have those capabilities?
    for (cap in caps) {
        if (hasCapability(cap)) {
            print("✓ Have " + cap);
            info = getCapabilityInfo(cap);
            print("  Details: " + str(info));
        } else {
            print("✗ Missing " + cap);
        }
    }

Complete Example
^^^^^^^^^^^^^^^^

.. code-block:: ml

    import file;

    // Helper function
    function canCallSafely(func) {
        required = requiredCapabilities(func);
        for (cap in required) {
            if (!hasCapability(cap)) {
                return false;
            }
        }
        return true;
    }

    // Check before using
    if (canCallSafely(file.read)) {
        content = file.read("config.json");
        print("Config loaded");
    } else {
        print("Cannot read files - using defaults");
        content = "{}";
    }
```

### Update: Standard Library Docs

**Files:** All stdlib module docs (file, http, etc.)

**Update each function documentation** to show capability requirements prominently:

```rst
read(path)
^^^^^^^^^^

Read file contents from path.

**Requires:** ``file.read`` capability

**Example:**

.. code-block:: ml

    import file;

    // Check capability before reading
    if (hasCapability("file.read")) {
        content = file.read("data.txt");
    } else {
        print("File reading not available");
    }

    // Or check function requirements
    caps = requiredCapabilities(file.read);
    print("Needs: " + str(caps));  // ["file.read"]
```

---

## Testing Plan

### Unit Tests

**File:** `tests/unit/stdlib/test_builtin.py`

**Add test cases:**

```python
def test_required_capabilities_with_metadata(builtin_instance):
    """Test requiredCapabilities with decorated function."""
    # Create a mock function with metadata
    from mlpy.stdlib.decorators import FunctionMetadata

    def mock_func():
        pass

    mock_func._ml_function_metadata = FunctionMetadata(
        name="mock_func",
        description="Test function",
        capabilities=["file.read", "file.write"]
    )

    result = builtin_instance.requiredCapabilities(mock_func)
    assert result == ["file.read", "file.write"]


def test_required_capabilities_no_metadata(builtin_instance):
    """Test requiredCapabilities with function without metadata."""
    def plain_func():
        pass

    result = builtin_instance.requiredCapabilities(plain_func)
    assert result == []


def test_required_capabilities_empty_capabilities(builtin_instance):
    """Test requiredCapabilities with empty capabilities list."""
    from mlpy.stdlib.decorators import FunctionMetadata

    def mock_func():
        pass

    mock_func._ml_function_metadata = FunctionMetadata(
        name="mock_func",
        description="Test function",
        capabilities=[]
    )

    result = builtin_instance.requiredCapabilities(mock_func)
    assert result == []


def test_help_includes_capabilities(builtin_instance):
    """Test that help() includes capability requirements."""
    from mlpy.stdlib.decorators import FunctionMetadata

    def mock_func():
        pass

    mock_func._ml_function_metadata = FunctionMetadata(
        name="mock_func",
        description="Test function",
        capabilities=["file.read"]
    )

    result = builtin_instance.help(mock_func)
    assert "Test function" in result
    assert "Requires: file.read" in result


def test_help_no_capabilities_message(builtin_instance):
    """Test that help() shows 'None required' for functions with empty capabilities."""
    from mlpy.stdlib.decorators import FunctionMetadata

    def mock_func():
        pass

    mock_func._ml_function_metadata = FunctionMetadata(
        name="mock_func",
        description="Test function",
        capabilities=[]
    )

    result = builtin_instance.help(mock_func)
    assert "Test function" in result
    assert "Capabilities: None required" in result
```

### Integration Tests

**File:** `tests/ml_integration/test_capability_introspection.ml`

```ml
// Test requiredCapabilities with stdlib functions
import file;
import console;

// Test 1: Function with capabilities
caps = requiredCapabilities(file.read);
print("file.read requires: " + str(caps));
// Expected: ["file.read"]

// Test 2: Function without capabilities
caps = requiredCapabilities(console.log);
print("console.log requires: " + str(caps));
// Expected: []

// Test 3: Builtin without capabilities
caps = requiredCapabilities(print);
print("print requires: " + str(caps));
// Expected: []

// Test 4: help() includes capabilities
helpText = help(file.read);
print("file.read help: " + helpText);
// Expected: Contains "Requires: file.read"

helpText = help(console.log);
print("console.log help: " + helpText);
// Expected: Contains "Capabilities: None required"

// Test 5: Defensive programming pattern
function canCall(func) {
    required = requiredCapabilities(func);
    for (cap in required) {
        if (!hasCapability(cap)) {
            return false;
        }
    }
    return true;
}

if (canCall(console.log)) {
    console.log("Console available");
}

print("All capability introspection tests passed");
```

---

## Migration & Backward Compatibility

**Backward Compatibility:**
- ✅ No breaking changes - only additions
- ✅ Existing `help()` behavior preserved (enhanced with additional info)
- ✅ New `requiredCapabilities()` function is additive

**Migration:**
- No migration needed - purely additive features
- Existing code continues to work unchanged
- New code can opt-in to enhanced introspection

---

## Success Criteria

✅ **Implementation:**
- [ ] `requiredCapabilities()` function implemented in `builtin.py`
- [ ] `help()` function enhanced to show capability requirements
- [ ] All unit tests pass
- [ ] Integration tests pass

✅ **Documentation:**
- [ ] Builtin functions reference updated
- [ ] Capability system tutorial updated with new examples
- [ ] Standard library docs updated to highlight capability requirements
- [ ] All examples tested and working

✅ **Developer Experience:**
- [ ] ML programmers can query function capability requirements
- [ ] Better error messages possible with capability introspection
- [ ] Defensive programming patterns enabled
- [ ] Interactive exploration improved

✅ **Testing:**
- [ ] Unit tests cover all edge cases
- [ ] Integration tests demonstrate real-world usage
- [ ] Documentation examples are executable and correct

---

## Future Enhancements

**Not in this proposal, but possible future additions:**

1. **Batch Capability Check:**
   ```ml
   canCallAll([file.read, file.write, http.get])  // Check multiple at once
   ```

2. **Capability Suggestions:**
   ```ml
   suggestCapabilities(file.read)  // Returns capability block template
   ```

3. **Transitive Capability Analysis:**
   ```ml
   allRequiredCapabilities(myFunction)  // All capabilities including called functions
   ```

4. **Capability Documentation in REPL:**
   ```ml
   >>> file.read
   <function file.read>
     Description: Read file contents from path
     Requires: file.read
     Usage: file.read(path: string) -> string
   ```

---

## Appendix: Complete API Overview

After implementation, the complete capability introspection API will be:

```ml
// ============================================================
// CONTEXT CAPABILITIES - What capabilities do I have?
// ============================================================

// Check if specific capability available
hasCapability("file.read") -> bool

// List all available capabilities
getCapabilities() -> ["file.read", "file.write", ...]

// Get detailed info about a capability
getCapabilityInfo("file.read") -> {
    type: "file.read",
    available: true,
    patterns: ["*.txt"],
    usage_count: 5,
    ...
}

// ============================================================
// FUNCTION REQUIREMENTS - What does this function need?
// ============================================================

// Get list of required capabilities (NEW)
requiredCapabilities(file.read) -> ["file.read"]

// Get help including capabilities (ENHANCED)
help(file.read) -> "Read file contents from path\nRequires: file.read"

// ============================================================
// COMBINED USAGE PATTERNS
// ============================================================

// Pattern 1: Check if you can call a function
function canCall(func) {
    required = requiredCapabilities(func);
    for (cap in required) {
        if (!hasCapability(cap)) {
            return false;
        }
    }
    return true;
}

// Pattern 2: Detailed capability check with reporting
function checkFunctionAccess(func) {
    required = requiredCapabilities(func);

    if (len(required) == 0) {
        return true;  // No requirements
    }

    missing = [];
    for (cap in required) {
        if (!hasCapability(cap)) {
            missing.push(cap);
        }
    }

    if (len(missing) > 0) {
        print("Missing capabilities: " + str(missing));
        for (cap in missing) {
            info = getCapabilityInfo(cap);
            if (info != null) {
                print("  " + cap + ": " + str(info));
            }
        }
        return false;
    }

    return true;
}

// Pattern 3: Interactive exploration
print(help(file.read));              // Description + requirements
caps = requiredCapabilities(file.read);  // Just the requirements
for (cap in caps) {
    info = getCapabilityInfo(cap);   // Detailed info
    print(cap + ": " + str(info));
}
```

---

**Priority:** Medium - Enhances developer experience but not critical
**Timeline:** Can be implemented as part of routine stdlib improvements
**Dependencies:** None - self-contained enhancement to builtin.py
