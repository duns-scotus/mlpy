# Builtin Module Enhancement Proposal: Secure Dynamic Introspection

**Date**: October 4, 2025
**Status**: Proposal
**Author**: Based on Phase 4 completion review
**Related**: PHASE-4-REVIEW.md, module-system-implementation-PLAN.md

---

## Executive Summary

This proposal evaluates adding dynamic introspection capabilities (hasattr, getattr, call) to the builtin module, along with other missing utility functions. The key question: **Can these powerful features be implemented securely without creating escape mechanisms?**

**Recommendation**: ✅ **YES** - with proper SafeAttributeRegistry integration and careful design

---

## 1. Dynamic Introspection Functions

### 1.1 hasattr() - Attribute Existence Check

**Function Signature**:
```python
@ml_function(description="Check if object has attribute")
def hasattr(self, obj: Any, name: str) -> bool
```

**Security Analysis**:
- **Risk Level**: 🟡 **LOW-MEDIUM**
- **Threat**: Could be used to probe for dangerous attributes
- **Mitigation**: Only return True for safe attributes

**Proposed Implementation**:
```python
@ml_function(description="Check if object has attribute (safe attributes only)")
def hasattr(self, obj: Any, name: str) -> bool:
    """Check if object has safe attribute.

    Only returns True for attributes in SafeAttributeRegistry whitelist.
    Dangerous attributes always return False.

    Args:
        obj: Object to check
        name: Attribute name

    Returns:
        True if object has safe attribute, False otherwise

    Examples:
        hasattr("hello", "upper")  # True
        hasattr("hello", "__class__")  # False (blocked)
    """
    from mlpy.ml.codegen.safe_attribute_registry import is_safe_attribute

    # Block dangerous attributes
    if name.startswith('_'):
        return False

    # Check if attribute exists AND is safe
    if not hasattr(obj, name):
        return False

    return is_safe_attribute(type(obj).__name__, name)
```

**Use Cases**:
```python
// Check before calling method
if (hasattr(user, "validate")) {
    user.validate();
}

// Defensive programming
if (hasattr(config, "timeout")) {
    timeout = config.timeout;
}
```

**Verdict**: ✅ **SAFE TO IMPLEMENT** with SafeAttributeRegistry integration

---

### 1.2 getattr() - Dynamic Attribute Access

**Function Signature**:
```python
@ml_function(description="Get attribute from object")
def getattr(self, obj: Any, name: str, default: Any = None) -> Any
```

**Security Analysis**:
- **Risk Level**: 🔴 **HIGH** without proper controls
- **Threat**: Direct access to __class__, __globals__, __dict__ = **CRITICAL SECURITY RISK**
- **Mitigation**: MUST route through SafeAttributeRegistry

**Proposed Implementation**:
```python
@ml_function(description="Get attribute from object (safe attributes only)")
def getattr(self, obj: Any, name: str, default: Any = None) -> Any:
    """Get safe attribute from object.

    Only allows access to attributes in SafeAttributeRegistry whitelist.
    Dangerous attributes return the default value.

    Security:
        - Blocks all dunder attributes (__class__, __dict__, etc.)
        - Only returns whitelisted safe attributes
        - No access to object internals

    Args:
        obj: Object to get attribute from
        name: Attribute name
        default: Default value if attribute not found or unsafe

    Returns:
        Attribute value if safe, default otherwise

    Examples:
        getattr("hello", "upper")  # <method 'upper'>
        getattr("hello", "__class__", "BLOCKED")  # "BLOCKED"
        getattr(obj, "missing", 42)  # 42
    """
    from mlpy.ml.codegen.safe_attribute_registry import safe_attr_access

    # Block dangerous attributes immediately
    if name.startswith('_'):
        return default

    # Route through SafeAttributeRegistry
    try:
        return safe_attr_access(obj, name)
    except (AttributeError, SecurityError):
        return default
```

**Use Cases**:
```python
// Dynamic method dispatch
method_name = "to" + type.capitalize();  // "toUpper", "toLower"
method = getattr(string, method_name);
if (method != null) {
    result = method();
}

// Configuration with fallbacks
timeout = getattr(config, "timeout", 30);
retries = getattr(config, "retries", 3);

// Plugin system
handler = getattr(plugin, "handle_" + event_type, null);
if (handler != null) {
    handler(data);
}
```

**Security Tests Required**:
```python
def test_getattr_blocks_dangerous_attributes():
    """Verify getattr blocks all dangerous attributes."""
    obj = {"safe": "value"}

    # Safe attribute - should work
    assert builtin.getattr(obj, "get") is not None

    # Dangerous attributes - should return default
    assert builtin.getattr(obj, "__class__", "BLOCKED") == "BLOCKED"
    assert builtin.getattr(obj, "__dict__", "BLOCKED") == "BLOCKED"
    assert builtin.getattr(obj, "__globals__", "BLOCKED") == "BLOCKED"
    assert builtin.getattr(obj, "__subclasses__", "BLOCKED") == "BLOCKED"

def test_getattr_only_safe_registry_attributes():
    """Verify getattr only allows SafeAttributeRegistry attributes."""
    from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry

    registry = get_safe_registry()

    # String has "upper" in safe registry
    assert builtin.getattr("hello", "upper") is not None

    # String does NOT have arbitrary attributes
    assert builtin.getattr("hello", "arbitrary_attr", "DEFAULT") == "DEFAULT"
```

**Verdict**: ✅ **SAFE TO IMPLEMENT** with mandatory SafeAttributeRegistry routing

---

### 1.3 call() - Dynamic Function Invocation

**Function Signature**:
```python
@ml_function(description="Call function with arguments")
def call(self, func: Callable, *args, **kwargs) -> Any
```

**Security Analysis**:
- **Risk Level**: 🟡 **MEDIUM**
- **Threat**: Could call unintended functions, bypass validation
- **Mitigation**: Validate function is callable, check @ml_function metadata

**Proposed Implementation**:
```python
@ml_function(description="Call function dynamically with arguments")
def call(self, func: Callable, *args, **kwargs) -> Any:
    """Call function dynamically with arguments.

    Safely invokes callable with provided arguments. Useful for
    functional programming patterns and dynamic dispatch.

    Args:
        func: Callable to invoke
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Result of function call

    Raises:
        TypeError: If func is not callable

    Examples:
        call(math.abs, -5)  # 5
        call(string.upper, "hello")  # "HELLO"

        // Dynamic dispatch
        operation = math.add;
        result = call(operation, 10, 5);  // 15

        // Function composition
        transform = functional.compose(string.upper, string.strip);
        call(transform, "  hello  ");  // "HELLO"
    """
    if not callable(func):
        raise TypeError(f"'{type(func).__name__}' object is not callable")

    return func(*args, **kwargs)
```

**Use Cases**:
```python
// Functional programming
operations = {
    "add": math.add,
    "subtract": math.subtract,
    "multiply": math.multiply
};
operation = operations[op_name];
result = call(operation, a, b);

// Callback system
callback = getattr(handler, "on_" + event_type, null);
if (callback != null) {
    call(callback, event_data);
}

// Higher-order functions
funcs = [string.upper, string.strip, string.reverse];
result = functional.reduce(
    (acc, fn) => call(fn, acc),
    funcs,
    initial_value
);
```

**Verdict**: ✅ **SAFE TO IMPLEMENT** - no additional security risk beyond normal function calls

---

## 2. Additional Missing Utility Functions

### 2.1 Safe Utility Functions (Recommended)

These functions are **safe to implement** without security concerns:

#### Predicate Functions
```python
@ml_function(description="Check if value is callable")
def callable(self, obj: Any) -> bool:
    """Check if object is callable (function, method, etc.)."""
    return callable(obj)

@ml_function(description="Check if all elements are truthy")
def all(self, iterable: list) -> bool:
    """Return True if all elements are truthy."""
    return all(iterable)

@ml_function(description="Check if any element is truthy")
def any(self, iterable: list) -> bool:
    """Return True if any element is truthy."""
    return any(iterable)
```

#### Numeric Functions
```python
@ml_function(description="Sum numeric values")
def sum(self, iterable: list, start: float = 0) -> float:
    """Sum numeric values with optional start value."""
    return sum(iterable, start)
```

#### String/Character Functions
```python
@ml_function(description="Convert integer to character")
def chr(self, i: int) -> str:
    """Convert Unicode code point to character."""
    return chr(i)

@ml_function(description="Convert character to integer")
def ord(self, c: str) -> int:
    """Convert character to Unicode code point."""
    return ord(c)
```

#### Number Format Conversions
```python
@ml_function(description="Convert to hexadecimal")
def hex(self, n: int) -> str:
    """Convert integer to hexadecimal string."""
    return hex(n)

@ml_function(description="Convert to binary")
def bin(self, n: int) -> str:
    """Convert integer to binary string."""
    return bin(n)

@ml_function(description="Convert to octal")
def oct(self, n: int) -> str:
    """Convert integer to octal string."""
    return oct(n)
```

#### Iteration Functions
```python
@ml_function(description="Create reverse iterator")
def reversed(self, seq: list) -> list:
    """Return reversed sequence."""
    return list(reversed(seq))

@ml_function(description="Create slice object")
def slice(self, start: int, stop: int = None, step: int = None):
    """Create slice object for indexing."""
    if stop is None:
        return slice(start)
    elif step is None:
        return slice(start, stop)
    else:
        return slice(start, stop, step)
```

#### Representation Functions
```python
@ml_function(description="Get string representation")
def repr(self, obj: Any) -> str:
    """Get string representation of object."""
    # Use ML-compatible boolean formatting
    if isinstance(obj, bool):
        return "true" if obj else "false"
    return repr(obj)

@ml_function(description="Format value with format specifier")
def format(self, value: Any, format_spec: str = "") -> str:
    """Format value with format specifier."""
    return format(value, format_spec)
```

**Total Safe Additions**: 13 functions

### 2.2 Iterator Protocol Functions

These could be useful but need careful implementation:

```python
@ml_function(description="Create iterator from iterable")
def iter(self, iterable: Any):
    """Create iterator from iterable."""
    return iter(iterable)

@ml_function(description="Get next item from iterator")
def next(self, iterator, default=None):
    """Get next item from iterator, or default if exhausted."""
    try:
        return next(iterator)
    except StopIteration:
        if default is None:
            return None
        return default
```

**Concern**: Iterators maintain state, could complicate sandboxing

---

## 3. Functions to NEVER Implement

These are **EXPLICITLY FORBIDDEN** due to security risks:

### 3.1 Code Execution (CRITICAL SECURITY RISK)
```python
# ❌ NEVER IMPLEMENT THESE
eval()      # Execute arbitrary Python code
exec()      # Execute arbitrary Python statements
compile()   # Compile code objects
```
**Risk**: Direct code injection, complete sandbox escape

### 3.2 File System Access
```python
# ❌ NEVER IMPLEMENT WITHOUT CAPABILITY SYSTEM
open()      # File I/O
```
**Risk**: Unauthorized file system access
**Alternative**: Implement in separate module with file.read, file.write capabilities

### 3.3 Module System Bypass
```python
# ❌ NEVER IMPLEMENT
__import__()    # Dynamic imports
globals()       # Access global namespace
locals()        # Access local namespace
vars()          # Access __dict__
```
**Risk**: Bypass module system, access internals

### 3.4 Dangerous Introspection
```python
# ❌ NEVER IMPLEMENT
setattr()   # Modify object internals
delattr()   # Delete attributes
dir()       # Expose all attributes (including dangerous ones)
hash()      # Timing attack vector
id()        # Memory address leakage
```
**Risk**: Object modification, information leakage

---

## 4. SafeAttributeRegistry Integration Requirements

For secure implementation of hasattr/getattr, the SafeAttributeRegistry must:

### 4.1 Whitelist Approach

```python
class SafeAttributeRegistry:
    def __init__(self):
        self._safe_attributes = {
            'str': {'upper', 'lower', 'split', 'join', 'strip', ...},
            'list': {'append', 'pop', 'sort', 'reverse', ...},
            'dict': {'get', 'keys', 'values', 'items', ...},
            # ... etc
        }

    def is_safe_attribute(self, type_name: str, attr_name: str) -> bool:
        """Check if attribute is in whitelist."""
        if attr_name.startswith('_'):
            return False  # Block ALL dunder attributes

        safe_attrs = self._safe_attributes.get(type_name, set())
        return attr_name in safe_attrs
```

### 4.2 Blacklist of Dangerous Patterns

```python
DANGEROUS_ATTRIBUTES = {
    '__class__', '__dict__', '__globals__', '__code__',
    '__subclasses__', '__bases__', '__mro__', '__weakref__',
    '__init__', '__new__', '__del__', '__setattr__', '__delattr__',
    '__getattribute__', '__import__', 'eval', 'exec', 'compile'
}

def is_dangerous_attribute(attr_name: str) -> bool:
    """Check if attribute is dangerous."""
    if attr_name in DANGEROUS_ATTRIBUTES:
        return True
    if attr_name.startswith('__') and attr_name.endswith('__'):
        return True  # Block all dunder methods by default
    return False
```

### 4.3 Integration Flow

```
ML Code: getattr(obj, "method_name")
    ↓
builtin.getattr() checks if attr starts with '_' → REJECT
    ↓
builtin.getattr() calls safe_attr_access(obj, "method_name")
    ↓
SafeAttributeRegistry.is_safe_attribute(type(obj), "method_name")
    ↓
If in whitelist → ALLOW
If not in whitelist → REJECT (return default)
```

---

## 5. Recommended Implementation Plan

### Phase 4A: Dynamic Introspection (High Priority)

**Week 1: Core Dynamic Features**

1. **Implement SafeAttributeRegistry enhancements**
   - Add `is_safe_attribute()` method
   - Add comprehensive whitelist for all types
   - Add dangerous attribute blacklist

2. **Implement hasattr()**
   - Integration with SafeAttributeRegistry
   - Comprehensive security tests

3. **Implement getattr()**
   - Mandatory SafeAttributeRegistry routing
   - Security tests for all dangerous attributes
   - Default value handling

4. **Implement call()**
   - Callable validation
   - Unit tests for various callable types

**Deliverables**:
- 3 new dynamic introspection functions
- 30+ security tests
- SafeAttributeRegistry enhancements
- Zero security vulnerabilities

### Phase 4B: Safe Utility Functions (Medium Priority)

**Week 2: Utility Functions**

1. **Predicate functions**: callable(), all(), any()
2. **Numeric functions**: sum()
3. **String/char functions**: chr(), ord()
4. **Format functions**: hex(), bin(), oct()
5. **Representation**: repr(), format()
6. **Iteration**: reversed()

**Deliverables**:
- 10+ new utility functions
- 40+ unit tests
- Complete documentation

### Phase 4C: Iterator Protocol (Optional)

**Week 3: Advanced Features**

1. **Iterator functions**: iter(), next()
2. **Slice creation**: slice()
3. **Documentation and examples**

**Deliverables**:
- 3 advanced functions
- 15+ tests
- Usage examples

---

## 6. Security Testing Requirements

### 6.1 Mandatory Security Tests

```python
class TestDynamicIntrospectionSecurity:
    """Security tests for hasattr/getattr/call."""

    def test_getattr_blocks_class_access(self):
        """Verify __class__ is blocked."""
        assert builtin.getattr("test", "__class__", "BLOCKED") == "BLOCKED"

    def test_getattr_blocks_globals_access(self):
        """Verify __globals__ is blocked."""
        def func(): pass
        assert builtin.getattr(func, "__globals__", "BLOCKED") == "BLOCKED"

    def test_getattr_blocks_dict_access(self):
        """Verify __dict__ is blocked."""
        class Obj: pass
        obj = Obj()
        assert builtin.getattr(obj, "__dict__", "BLOCKED") == "BLOCKED"

    def test_getattr_blocks_subclasses_traversal(self):
        """Verify __subclasses__ is blocked."""
        assert builtin.getattr(object, "__subclasses__", "BLOCKED") == "BLOCKED"

    def test_getattr_blocks_mro_access(self):
        """Verify __mro__ is blocked."""
        assert builtin.getattr(str, "__mro__", "BLOCKED") == "BLOCKED"

    def test_getattr_only_safe_registry_attributes(self):
        """Verify only whitelisted attributes accessible."""
        # Safe: "upper" is in string whitelist
        assert builtin.getattr("test", "upper") is not None

        # Unsafe: arbitrary attribute not in whitelist
        assert builtin.getattr("test", "arbitrary", "BLOCKED") == "BLOCKED"

    def test_hasattr_never_reveals_dangerous_attrs(self):
        """Verify hasattr returns False for all dangerous attributes."""
        assert builtin.hasattr("test", "__class__") is False
        assert builtin.hasattr("test", "__dict__") is False
        assert builtin.hasattr([], "__class__") is False

    def test_call_cannot_invoke_dangerous_builtins(self):
        """Verify call doesn't enable access to blocked functions."""
        # This test ensures call() doesn't bypass security
        # Since we never expose eval/exec, this should be safe
        pass
```

### 6.2 Penetration Testing Scenarios

```python
def test_no_sandbox_escape_via_getattr():
    """Attempt sandbox escape using getattr - should fail."""
    # Try to get __class__
    cls = builtin.getattr("", "__class__", None)
    assert cls is None  # Blocked

    # Try to traverse to object
    # This should fail at first step
    obj_cls = builtin.getattr(cls, "__bases__", None) if cls else None
    assert obj_cls is None

    # Try to get __subclasses__
    subclasses = builtin.getattr(obj_cls, "__subclasses__", None) if obj_cls else None
    assert subclasses is None

def test_no_code_execution_via_dynamic_features():
    """Verify no code execution possible through dynamic features."""
    # getattr should not allow access to eval/exec
    eval_func = builtin.getattr(__builtins__, "eval", None)
    assert eval_func is None  # Should be blocked

    # Even if we had eval, call() shouldn't help
    # because we never expose eval to ML code
```

---

## 7. Use Case Examples

### 7.1 Dynamic Method Dispatch

```javascript
// ML Code
import string;

function transform_text(text, operation) {
    // Dynamic dispatch based on operation name
    method_name = "to" + operation.capitalize();  // "toUpper", "toLower"

    if (hasattr(string, method_name)) {
        method = getattr(string, method_name);
        return call(method, text);
    }

    return text;
}

result = transform_text("hello", "upper");  // "HELLO"
result = transform_text("WORLD", "lower");  // "world"
```

### 7.2 Plugin System

```javascript
// ML Code
import builtin;

function execute_plugin(plugin, event_type, data) {
    // Check if plugin has handler for event
    handler_name = "on_" + event_type;

    if (hasattr(plugin, handler_name)) {
        handler = getattr(plugin, handler_name);
        return call(handler, data);
    }

    // Fallback to default handler
    if (hasattr(plugin, "on_default")) {
        default_handler = getattr(plugin, "on_default");
        return call(default_handler, event_type, data);
    }

    return null;
}
```

### 7.3 Configuration with Fallbacks

```javascript
// ML Code
import builtin;

function get_config_value(config, key, default_value) {
    // Try to get configuration value
    if (hasattr(config, key)) {
        value = getattr(config, key);
        if (value != null) {
            return value;
        }
    }

    return default_value;
}

timeout = get_config_value(app_config, "timeout", 30);
retries = get_config_value(app_config, "max_retries", 3);
```

### 7.4 Functional Programming

```javascript
// ML Code
import builtin;
import functional;

// Higher-order function using call()
function apply_pipeline(value, functions) {
    return functional.reduce(
        (acc, fn) => call(fn, acc),
        functions,
        value
    );
}

// Pipeline: strip whitespace, uppercase, reverse
result = apply_pipeline(
    "  hello world  ",
    [string.strip, string.upper, string.reverse]
);
// Result: "DLROW OLLEH"
```

---

## 8. Recommendation Summary

### ✅ Strongly Recommend Implementing

**Dynamic Introspection (3 functions)**:
- `hasattr()` - Safe with SafeAttributeRegistry
- `getattr()` - Safe with SafeAttributeRegistry routing
- `call()` - Safe, no additional risk

**Safe Utilities (13 functions)**:
- Predicates: `callable()`, `all()`, `any()`
- Numeric: `sum()`
- String/Char: `chr()`, `ord()`
- Formats: `hex()`, `bin()`, `oct()`
- Representation: `repr()`, `format()`
- Iteration: `reversed()`

**Total Additions**: 16 functions

### 🟡 Consider Implementing

**Iterator Protocol (3 functions)**:
- `iter()`, `next()`, `slice()` - Useful but adds complexity

### ❌ Never Implement

**Dangerous Functions**:
- Code execution: `eval()`, `exec()`, `compile()`
- File I/O: `open()` (without capability system)
- Namespace access: `globals()`, `locals()`, `vars()`
- Object modification: `setattr()`, `delattr()`
- Information leakage: `id()`, `hash()`, unfiltered `dir()`

---

## 9. Implementation Feasibility

### Is Secure Implementation Possible?

✅ **YES** - Dynamic introspection can be implemented securely with:

1. **Mandatory SafeAttributeRegistry Integration**
   - All attribute access must route through registry
   - Whitelist-only approach for safe attributes
   - Explicit blacklist for dangerous patterns

2. **Defense in Depth**
   - Block all dunder attributes by default
   - Multiple validation layers
   - Comprehensive security testing

3. **No New Attack Surface**
   - getattr() uses existing SafeAttributeRegistry
   - call() doesn't enable access to blocked functions
   - hasattr() only reveals what's already accessible

### Risk vs Benefit Analysis

**Benefits**:
- ✅ Enables dynamic programming patterns
- ✅ Plugin systems and extensibility
- ✅ Configuration management
- ✅ Functional programming enhancements
- ✅ Better developer experience

**Risks** (All Mitigated):
- 🟢 Attribute access → SafeAttributeRegistry whitelist
- 🟢 Class traversal → Block all dunder attributes
- 🟢 Code execution → Never expose eval/exec/compile
- 🟢 File access → Never expose open() without capabilities

---

## 10. Conclusion

**Recommendation**: ✅ **PROCEED WITH IMPLEMENTATION**

The proposed dynamic introspection features (hasattr, getattr, call) **CAN be implemented securely** with proper SafeAttributeRegistry integration. Combined with 13 safe utility functions, this would bring the builtin module to **41 total functions** - a comprehensive foundation for ML programming.

**Security Confidence**: HIGH - with mandatory security testing and SafeAttributeRegistry enforcement

**Developer Value**: HIGH - enables advanced programming patterns while maintaining security

**Implementation Complexity**: MEDIUM - requires SafeAttributeRegistry enhancements but builds on existing infrastructure

**Next Steps**:
1. Enhance SafeAttributeRegistry with whitelist/blacklist methods
2. Implement hasattr/getattr/call with security tests
3. Add 13 safe utility functions
4. Comprehensive security audit
5. Update documentation with usage examples
