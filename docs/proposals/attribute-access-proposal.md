# Secure Python-Style Attribute Access Implementation Proposal

**Status**: Draft
**Version**: 1.0
**Date**: January 2025
**Author**: mlpy Development Team

## **Executive Summary**

This proposal outlines a comprehensive implementation plan for secure Python-style attribute access in mlpy, replacing the current dictionary-access-only model with a type-aware system that supports natural object method calls while maintaining security through explicit whitelisting.

## **Problem Statement**

### **Current Issue**
The mlpy transpiler currently treats ALL `obj.property` as `obj['property']` (dictionary access) except for imported modules. This breaks Python built-in type methods:

```ml
// ML Code → Current Transpilation → Result
arr.length()  → arr['length']()  → KeyError: 'length'
str.upper()   → str['upper']()   → TypeError: string indices must be integers
obj.name      → obj['name']       → ✅ Works for ML objects
string.length(text) → ml_string.length(text) → ✅ Works for modules
```

**Location**: `src/mlpy/ml/codegen/python_generator.py` lines 669-675

### **Impact**
- 6+ failing test files using `arr.length()`, `bucket.length()` patterns
- Unnatural API requiring `collections.length(arr)` instead of `arr.length()`
- Developer confusion coming from Python/JavaScript backgrounds

## **Cost/Benefit Analysis**

### **Benefits**
- **Developer Experience**: Natural `arr.length()`, `str.upper()` syntax matches Python/JavaScript expectations
- **Functionality**: Fixes 6+ failing test files immediately (`comprehensive_data_structures.ml`, etc.)
- **Consistency**: Unified object model where all objects have accessible methods
- **Security**: Centralized control over attribute access with explicit whitelisting
- **Performance**: Direct Python method calls for built-ins (faster than dictionary lookup)

### **Costs**
- **Implementation Complexity**: ~3-4 new files, modifications to 2 core files
- **Runtime Overhead**: Type checking for unknown objects (mitigated by compile-time detection)
- **Maintenance**: Need to maintain safe attribute whitelists as Python evolves
- **Testing**: Comprehensive security and functionality testing required

### **Risk Assessment**

#### **High Risk - Security Bypass**
**Risk**: Malicious code accessing dangerous attributes through type confusion
**Mitigation**:
- Strict whitelist-only approach (no blacklist fallback)
- Runtime type validation for all dynamic access
- Integration with existing security analyzer

#### **Medium Risk - Performance Impact**
**Risk**: Runtime type checking slows down attribute access
**Mitigation**:
- Compile-time type detection where possible
- Efficient runtime helpers with caching
- Benchmark against current dictionary access

#### **Low Risk - API Surface Expansion**
**Risk**: More Python methods exposed = larger attack surface
**Mitigation**:
- Conservative whitelist (only essential methods)
- Regular security audits of whitelisted methods
- Capability-based permissions for sensitive operations

## **Detailed Implementation Specifications**

### **Phase 1: Core Infrastructure**

#### **File 1: `src/mlpy/ml/codegen/safe_attribute_registry.py`** (NEW)

```python
from dataclasses import dataclass
from typing import Dict, Set, Type, Any, Optional
from enum import Enum

class AttributeAccessType(Enum):
    METHOD = "method"      # Callable attribute
    PROPERTY = "property"  # Non-callable attribute
    FORBIDDEN = "forbidden" # Explicitly blocked

@dataclass
class SafeAttribute:
    name: str
    access_type: AttributeAccessType
    capabilities_required: List[str] = None
    description: str = ""

class SafeAttributeRegistry:
    def __init__(self):
        self._safe_attributes: Dict[Type, Dict[str, SafeAttribute]] = {}
        self._custom_classes: Dict[str, Dict[str, SafeAttribute]] = {}
        self._init_builtin_types()

    def register_builtin_type(self, python_type: Type, attributes: Dict[str, SafeAttribute]):
        """Register safe attributes for Python built-in type"""

    def register_custom_class(self, class_name: str, attributes: Dict[str, SafeAttribute]):
        """Allow stdlib modules to register custom classes"""

    def is_safe_access(self, obj_type: Type, attr_name: str) -> bool:
        """Check if attribute access is safe for given type"""

    def get_attribute_info(self, obj_type: Type, attr_name: str) -> Optional[SafeAttribute]:
        """Get detailed information about safe attribute"""

    def _init_builtin_types(self):
        """Initialize whitelists for Python built-in types"""
```

**Specific Whitelists**:
```python
# String methods (28 safe methods)
str_safe_methods = {
    "upper", "lower", "strip", "lstrip", "rstrip", "replace", "split", "rsplit",
    "join", "startswith", "endswith", "find", "rfind", "index", "rindex",
    "count", "isdigit", "isalpha", "isalnum", "isspace", "istitle", "isupper",
    "islower", "capitalize", "title", "swapcase", "center", "ljust", "rjust"
}

# List methods (12 safe methods)
list_safe_methods = {
    "append", "extend", "insert", "remove", "pop", "index", "count",
    "sort", "reverse", "clear", "copy"
}
# Note: Deliberately exclude "length" - will map to len() function

# Dict methods (9 safe methods)
dict_safe_methods = {
    "get", "keys", "values", "items", "pop", "popitem", "update",
    "clear", "setdefault"
}

# Blocked patterns (15+ patterns)
dangerous_patterns = {
    "__class__", "__dict__", "__globals__", "__bases__", "__mro__", "__subclasses__",
    "__code__", "__closure__", "__defaults__", "__kwdefaults__", "__annotations__",
    "__module__", "__qualname__", "__doc__", "__weakref__"
}
```

#### **File 2: `src/mlpy/stdlib/runtime_helpers.py`** (NEW)

```python
from typing import Any, Union, Tuple
from .safe_attribute_registry import get_safe_registry

def safe_attr_access(obj: Any, attr_name: str, *args, **kwargs) -> Any:
    """Runtime helper for safe attribute access with type checking"""
    registry = get_safe_registry()
    obj_type = type(obj)

    # Check if access is safe
    if not registry.is_safe_access(obj_type, attr_name):
        if attr_name.startswith('__') and attr_name.endswith('__'):
            raise SecurityError(f"Access to dangerous attribute '{attr_name}' is forbidden")
        else:
            raise AttributeError(f"'{obj_type.__name__}' object has no accessible attribute '{attr_name}'")

    # Perform the actual access
    attr = getattr(obj, attr_name)
    if callable(attr) and (args or kwargs):
        return attr(*args, **kwargs)
    return attr

def safe_method_call(obj: Any, method_name: str, *args, **kwargs) -> Any:
    """Specialized helper for method calls"""

def get_safe_length(obj: Any) -> int:
    """Safe length access that maps to Python's len()"""
    return len(obj)

def is_ml_object(obj: Any) -> bool:
    """Detect if object is an ML object (dict with string keys)"""
    return isinstance(obj, dict) and all(isinstance(k, str) for k in obj.keys())
```

### **Phase 2: Core Transpiler Modifications**

#### **File 3: Modify `src/mlpy/ml/codegen/python_generator.py`**

**Location**: Lines 654-679 (MemberAccess handling)

**New Method Signatures**:
```python
def _generate_member_access(self, expr: MemberAccess) -> str:
    """Enhanced member access with type-aware routing"""

def _detect_object_type(self, expr: Expression) -> Optional[Type]:
    """Compile-time type detection for expressions"""

def _is_safe_builtin_access(self, obj_type: Type, attr_name: str) -> bool:
    """Check if builtin type access is safe"""

def _generate_safe_attribute_access(self, obj_code: str, attr_name: str,
                                   obj_type: Type = None) -> str:
    """Generate safe attribute access code"""

def _should_use_runtime_wrapper(self, expr: Expression) -> bool:
    """Determine if runtime type checking needed"""
```

**Modified Logic Flow**:
```python
elif isinstance(expr, MemberAccess):
    obj_code = self._generate_expression(expr.object)

    if isinstance(expr.member, str):
        # 1. Check if imported module (existing logic)
        if self._is_imported_module(expr.object):
            return f"{obj_code}.{expr.member}"

        # 2. NEW: Detect compile-time type
        obj_type = self._detect_object_type(expr.object)

        if obj_type and self._is_safe_builtin_access(obj_type, expr.member):
            # 3. NEW: Direct Python attribute access for safe built-ins
            return self._generate_safe_attribute_access(obj_code, expr.member, obj_type)

        elif obj_type is dict or self._is_ml_object_pattern(expr.object):
            # 4. ML objects use dictionary access (existing)
            return f"{obj_code}[{repr(expr.member)}]"

        else:
            # 5. NEW: Runtime type checking for unknown objects
            return f"_safe_attr_access({obj_code}, {repr(expr.member)})"
```

**Type Detection Implementation**:
```python
def _detect_object_type(self, expr: Expression) -> Optional[Type]:
    """Compile-time type detection"""
    if isinstance(expr, StringLiteral):
        return str
    elif isinstance(expr, ArrayLiteral):
        return list
    elif isinstance(expr, ObjectLiteral):
        return dict
    elif isinstance(expr, NumberLiteral):
        return int if isinstance(expr.value, int) else float
    elif isinstance(expr, Identifier):
        # Try to infer from context/assignments (future enhancement)
        return None
    return None
```

#### **File 4: Modify `src/mlpy/ml/codegen/context.py`**

**Add to GenerationContext**:
```python
@dataclass
class GenerationContext:
    # ... existing fields ...
    safe_registry: SafeAttributeRegistry = field(default_factory=lambda: get_safe_registry())
    runtime_helpers_imported: bool = False

def ensure_runtime_helpers_imported(self) -> str:
    """Generate import statement for runtime helpers if needed"""
    if not self.runtime_helpers_imported:
        self.runtime_helpers_imported = True
        return "from mlpy.stdlib.runtime_helpers import _safe_attr_access, get_safe_length"
    return ""
```

### **Phase 3: Security Integration**

#### **File 5: Modify `src/mlpy/ml/analysis/security_analyzer.py`**

**Enhanced Member Access Checking**:
```python
def visit_member_access(self, node: MemberAccess):
    """Enhanced security checking for member access"""
    attr_name = node.member

    # Existing reflection pattern check
    if attr_name in self.reflection_patterns:
        self._add_issue("critical", "reflection_abuse",
                       f"Dangerous reflection operation '{attr_name}' detected", node)
        return

    # NEW: Check against safe attribute registry
    registry = get_safe_registry()

    # Try to determine object type for compile-time checking
    if hasattr(node.object, 'name') and node.object.name in self.known_types:
        obj_type = self.known_types[node.object.name]
        if not registry.is_safe_access(obj_type, attr_name):
            self._add_issue("high", "unsafe_attribute_access",
                           f"Unsafe attribute access '{attr_name}' on {obj_type.__name__}", node)

    # Continue with existing logic
    if node.object:
        node.object.accept(self)
```

### **Phase 4: Standard Library Integration**

#### **File 6: Modify `src/mlpy/stdlib/registry.py`**

**Add Custom Class Registration**:
```python
class StandardLibraryRegistry:
    def __init__(self, capability_manager: CapabilityManager = None):
        # ... existing init ...
        self.safe_registry = SafeAttributeRegistry()

    def register_safe_class(self, class_name: str, attributes: Dict[str, SafeAttribute],
                           capabilities_required: List[str] = None) -> None:
        """Allow stdlib modules to register classes for safe attribute access"""
        # Validate capabilities
        if not self.validate_capabilities("stdlib", capabilities_required or []):
            raise SecurityError(f"Insufficient capabilities to register class {class_name}")

        self.safe_registry.register_custom_class(class_name, attributes)
```

### **Phase 5: Special Method Handling**

#### **Special Case: `.length()` → `len()`**

Instead of exposing `.__len__()` (dangerous), map `.length()` to `len()`:

```python
# In safe_attribute_registry.py
def _init_builtin_types(self):
    # Special mapping for length - generates len(obj) instead of obj.length()
    length_attribute = SafeAttribute("length", AttributeAccessType.METHOD, [],
                                   "Get length using Python's len() function")

    self._safe_attributes[list]["length"] = length_attribute
    self._safe_attributes[str]["length"] = length_attribute
    self._safe_attributes[dict]["length"] = length_attribute

# In python_generator.py
def _generate_safe_attribute_access(self, obj_code: str, attr_name: str, obj_type: Type) -> str:
    if attr_name == "length" and obj_type in (list, str, dict, tuple):
        return f"len({obj_code})"
    else:
        return f"{obj_code}.{attr_name}"
```

## **Implementation Timeline**

### **Phase 1** (2-3 days): Core Infrastructure
- Create `SafeAttributeRegistry` with comprehensive whitelists
- Create `runtime_helpers.py` with safe access functions
- Unit tests for registry and helpers

### **Phase 2** (2-3 days): Transpiler Integration
- Modify `python_generator.py` member access logic
- Implement compile-time type detection
- Integration tests with simple cases

### **Phase 3** (1 day): Security Integration
- Enhance `security_analyzer.py`
- Security penetration testing

### **Phase 4** (1 day): Testing & Validation
- Run full test suite
- Fix failing tests in `comprehensive_data_structures.ml` etc.
- Performance benchmarking

**Total Estimated Effort**: 6-8 days

## **Expected Code Generation Examples**

### **Before Implementation**
```ml
// ML Code
arr = [1, 2, 3];
len = arr.length();
text = "hello";
upper = text.upper();

// Generated Python (BROKEN)
arr = [1, 2, 3]
len = arr['length']()  # KeyError: 'length'
text = 'hello'
upper = text['upper']()  # TypeError: string indices must be integers
```

### **After Implementation**
```ml
// ML Code
arr = [1, 2, 3];
len = arr.length();
text = "hello";
upper = text.upper();
obj = {name: "John"};
name = obj.name;

// Generated Python (WORKING)
arr = [1, 2, 3]
len = len(arr)  # Maps .length() to len()
text = 'hello'
upper = text.upper()  # Direct Python method call
obj = {'name': 'John'}
name = obj['name']  # ML objects still use dict access
```

## **Security Considerations**

### **Whitelist-Only Approach**
- No method/attribute access allowed unless explicitly whitelisted
- Conservative initial whitelist focusing on essential functionality
- Regular security audits of whitelisted methods

### **Dangerous Pattern Blocking**
- All `__*__` patterns blocked (dunder methods)
- Introspection methods: `__class__`, `__dict__`, `__globals__`
- Dynamic attribute access: `getattr`, `setattr`, `delattr`
- Code introspection: `__code__`, `__closure__`, `__defaults__`

### **Runtime Type Validation**
- Unknown object types get runtime type checking
- Type confusion attacks prevented by strict type validation
- Integration with existing capability system

## **Success Metrics**

1. **Functionality**: All `arr.length()`, `str.upper()` patterns work
2. **Security**: Zero bypass of dangerous attribute access
3. **Performance**: ≤10% overhead vs current dictionary access
4. **Test Coverage**: All previously failing tests now pass (6+ files)
5. **Code Quality**: Maintains existing security and capability integration

## **Future Enhancements**

### **Type Inference Improvements**
- Static analysis to infer variable types from assignments
- Flow-sensitive type tracking across function boundaries
- Integration with planned type system

### **Performance Optimizations**
- Compile-time resolution for more patterns
- Caching for runtime type checks
- Specialized code paths for common operations

### **Standard Library Extensions**
- Allow ML standard library modules to register custom classes
- Capability-based permissions for class registration
- Documentation and examples for safe class registration

## **Conclusion**

This proposal provides a comprehensive solution to the current attribute access limitations while maintaining mlpy's security-first philosophy. The implementation offers natural Python-style object access patterns that developers expect, while ensuring all access is explicitly controlled through whitelisting and security validation.

The type-aware member access system bridges the gap between ML's declarative syntax and Python's rich object model, enabling more intuitive and powerful ML programs while preserving the security guarantees that make mlpy suitable for safe execution environments.