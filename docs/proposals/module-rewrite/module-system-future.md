# Future Module System Design

## Vision Statement

The future mlpy module system will be a **decorator-driven, security-first, introspection-friendly** architecture that makes creating Python-to-ML bridges as simple as adding a few decorators to Python code. Every module will automatically expose its capabilities, enforce security constraints, and provide rich introspection for ML programmers.

## Design Principles

1. **Simplicity**: Adding a new stdlib module should be < 50 lines of Python code
2. **Security-First**: Capabilities are enforced, not documented
3. **Auto-Discovery**: No manual registration, decorators handle everything
4. **Introspection**: ML code can query modules, functions, documentation
5. **Consistency**: One clear pattern for all module types
6. **Flexibility**: Same system works for Python modules, ML modules, user modules

## Architecture Overview

### Component Topology (Future)

```
┌─────────────────────────────────────────────────────────────┐
│                    ML Source Code (.ml)                      │
│         import builtin;  import math;  import mymodule;      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Parser & AST (ImportStatement)                  │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│         Module Resolver (Enhanced)                           │
│  ┌──────────────────────────────────────────────────┐       │
│  │ 1. Check cache                                   │       │
│  │ 2. Check decorator registry (auto-discovered)    │       │
│  │ 3. Try user ML modules from import paths         │       │
│  │ 4. Grant required capabilities to current context│       │
│  └──────────────────────────────────────────────────┘       │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│    Code Generator (Simplified)                               │
│  visit_import_statement():                                   │
│    # No hardcoded lists!                                     │
│    module_info = resolver.resolve_import(node.target)        │
│    if module_info.is_python:                                 │
│      emit: from {module_info.python_path} import Module      │
│    else:                                                     │
│      # ML module - transpile and import                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│      Runtime with Capability Checks                          │
│  When ML calls math.sqrt(x):                                 │
│    1. Check capability: has_capability("execute:calculations")│
│    2. If granted: call Python math.sqrt(x)                   │
│    3. If denied: raise CapabilityError                       │
└─────────────────────────────────────────────────────────────┘
```

### File Structure (Future)

```
src/mlpy/stdlib/
├── __init__.py              # Auto-discovers and exports all @ml_module decorated classes
├── decorators.py            # NEW: All decorator implementations
│
├── builtin.py               # NEW: Core builtin module (type(), len(), print(), etc.)
├── math.py                  # Renamed from math_bridge.py, uses decorators
├── string.py                # Renamed from string_bridge.py
├── datetime.py              # Renamed from datetime_bridge.py
├── json.py                  # Renamed from json_bridge.py
├── regex.py                 # Renamed from regex_bridge.py
├── functional.py            # Renamed from functional_bridge.py
├── collections.py           # Renamed from collections_bridge.py
├── random.py                # Renamed from random_bridge.py
│
├── runtime_helpers.py       # Keep for safe attribute access
└── registry.py              # SIMPLIFIED: Just discovery, not manual registration
```

**Key Changes**:
- ✅ Drop `_bridge` suffix (Python modules are the modules!)
- ✅ Drop `.ml` files (stdlib is Python, not ML)
- ✅ Add `builtin.py` for core functionality
- ✅ Add `decorators.py` for decorator system
- ✅ Simplify `registry.py` to auto-discovery only

## Decorator System Design

### Core Decorators

#### 1. `@ml_module` - Module Declaration

**Purpose**: Mark a Python class as an ML stdlib module.

**Signature**:

```python
@ml_module(
    name: str,                           # ML module name
    capabilities: list[str] = None,      # Required capabilities for the module
    description: str = None,             # Module description (auto from docstring)
    version: str = "1.0.0",             # Module version
    auto_export: bool = True            # Auto-export all decorated methods
)
```

**Usage**:

```python
from mlpy.stdlib.decorators import ml_module, ml_function, ml_constant

@ml_module(
    name="math",
    capabilities=["execute:calculations"],
    description="Mathematical operations and constants",
    version="2.0.0"
)
class Math:
    """Advanced mathematical operations with capability-based security."""

    # Module implementation...
```

**What it does**:
1. Registers the class with the module registry
2. Extracts metadata (description from docstring if not provided)
3. Creates a module wrapper that enforces capabilities
4. Makes the class discoverable by auto-discovery system

#### 2. `@ml_function` - Function/Method Declaration

**Purpose**: Mark a method as exposed to ML.

**Signature**:

```python
@ml_function(
    name: str = None,                   # ML function name (auto from method name)
    capabilities: list[str] = None,     # Required capabilities (inherits from module)
    params: dict[str, type] = None,     # Parameter types for validation
    returns: type = None,               # Return type for documentation
    validate: Callable = None,          # Custom validation function
    description: str = None,            # Function description (auto from docstring)
    examples: list[str] = None         # Usage examples for documentation
)
```

**Usage**:

```python
@ml_module(name="math", capabilities=["execute:calculations"])
class Math:

    @ml_function(
        params={"x": float},
        returns=float,
        description="Compute square root of x",
        examples=["math.sqrt(16) // 4.0", "math.sqrt(2.0) // 1.414..."]
    )
    def sqrt(self, x: float) -> float:
        """Compute the square root of x using Python's math.sqrt."""
        if x < 0:
            raise ValueError("Cannot compute square root of negative number")
        return py_math.sqrt(x)

    @ml_function(params={"x": float, "y": float}, returns=float)
    def pow(self, x: float, y: float) -> float:
        """Raise x to the power of y."""
        return py_math.pow(x, y)
```

**What it does**:
1. Marks method as exposed to ML (non-decorated methods are private)
2. Generates capability-checking wrapper
3. Validates parameters if `params` specified
4. Adds metadata for introspection
5. Collects examples for documentation

#### 3. `@ml_constant` - Constant Declaration

**Purpose**: Mark a class attribute as an ML constant.

**Signature**:

```python
@ml_constant(
    name: str = None,                   # ML constant name (auto from attribute name)
    description: str = None,            # Constant description
    immutable: bool = True             # Whether constant can be modified from ML
)
```

**Usage**:

```python
@ml_module(name="math")
class Math:

    @ml_constant(description="The mathematical constant π (pi)")
    pi = 3.141592653589793

    @ml_constant(description="Euler's number e")
    e = 2.718281828459045

    @ml_constant(description="Tau (2π)")
    tau = 6.283185307179586
```

**What it does**:
1. Exposes constant to ML with documentation
2. Enforces immutability if specified
3. Adds metadata for introspection

#### 4. `@ml_class` - Class Declaration (Advanced)

**Purpose**: Expose a Python class to ML with methods and properties.

**Signature**:

```python
@ml_class(
    name: str,                          # ML class name
    capabilities: list[str] = None,     # Required capabilities
    description: str = None,            # Class description
    instantiable: bool = True          # Whether ML can create instances
)
```

**Usage** (Future feature for object-oriented stdlib):

```python
@ml_class(
    name="DateTime",
    capabilities=["read:system_time"],
    description="Date and time manipulation class"
)
class DateTime:
    """Represents a date and time value."""

    @ml_function(name="now", static=True)
    def now(cls):
        """Get current date and time."""
        return cls(datetime.now())

    @ml_function(name="format")
    def format(self, pattern: str) -> str:
        """Format datetime as string."""
        return self._dt.strftime(pattern)
```

### Helper Decorators

#### 5. `@requires_capability` - Capability Guard

**Purpose**: Additional capability check beyond module-level.

```python
from mlpy.stdlib.decorators import requires_capability

@ml_module(name="file", capabilities=["file:read"])
class File:

    @ml_function
    @requires_capability("file:write")  # Additional capability for write ops
    def write_file(self, path: str, content: str):
        """Write content to file (requires file:write capability)."""
        with open(path, 'w') as f:
            f.write(content)
```

#### 6. `@validate_params` - Parameter Validation

**Purpose**: Advanced parameter validation with custom logic.

```python
from mlpy.stdlib.decorators import validate_params

def validate_positive(x):
    if x <= 0:
        raise ValueError("Value must be positive")

@ml_module(name="math")
class Math:

    @ml_function
    @validate_params(x=validate_positive)
    def sqrt(self, x: float) -> float:
        """Square root (requires positive number)."""
        return py_math.sqrt(x)
```

## Builtin Module Specification

### Purpose

The `builtin` module provides **core functionality** that every ML program needs:
- Type conversion: `int()`, `float()`, `str()`, `bool()`
- Type checking: `type()`, `typeof()`, `isinstance()`
- Introspection: `dir()`, `info()`, `hasattr()`, `getattr()`
- Utility: `len()`, `print()`, `input()`, `exit()`, `version()`
- Object manipulation: `del()`, `setattr()`, `call()`

### Auto-Import Behavior

The builtin module is **automatically imported** in every ML program. ML programmers can use builtin functions without `import`:

```ml
// These work without any imports
x = int("42");
name = typeof(x);       // "number"
items = len([1, 2, 3]); // 3
print("Hello!");
```

### Module API Design

**File**: `src/mlpy/stdlib/builtin.py`

**Structure**:

```python
from mlpy.stdlib.decorators import ml_module, ml_function, ml_class, ml_constant

@ml_module(
    name="builtin",
    capabilities=[],  # No capabilities required - core functionality
    description="Core built-in functions and classes for ML",
    version="2.0.0",
    auto_import=True  # Automatically imported in all ML programs
)
class Builtin:
    """
    Core ML built-in functionality.

    This module is automatically imported and provides essential functions
    for type conversion, introspection, I/O, and utility operations.
    """

    # ============================================================
    # Type Conversion Functions
    # ============================================================

    @ml_function(
        params={"value": Any},
        returns=int,
        description="Convert value to integer",
        examples=[
            'int("42") // 42',
            'int(3.14) // 3',
            'int(true) // 1'
        ]
    )
    def int(self, value) -> int:
        """Convert value to integer with ML semantics."""
        # Implementation handles bool, float, string conversion

    @ml_function(params={"value": Any}, returns=float)
    def float(self, value) -> float:
        """Convert value to floating-point number."""

    @ml_function(params={"value": Any}, returns=str)
    def str(self, value) -> str:
        """Convert value to string with ML semantics (true/false not True/False)."""

    @ml_function(params={"value": Any}, returns=bool)
    def bool(self, value) -> bool:
        """Convert value to boolean."""

    # ============================================================
    # Type Checking Functions
    # ============================================================

    @ml_function(params={"value": Any}, returns=str)
    def type(self, value) -> str:
        """
        Get the type of a value as a string.

        Returns one of: "boolean", "number", "string", "array", "object",
        "function", "class", "module", "unknown"
        """

    @ml_function(params={"value": Any}, returns=str)
    def typeof(self, value) -> str:
        """Alias for type() - get the type of a value."""

    @ml_function(params={"value": Any, "type_name": str}, returns=bool)
    def isinstance(self, value, type_name: str) -> bool:
        """
        Check if value is of specified type.

        Examples:
            isinstance(42, "number") // true
            isinstance("hello", "string") // true
            isinstance([1,2,3], "array") // true
        """

    # ============================================================
    # Introspection Functions
    # ============================================================

    @ml_function(params={"obj": Any}, returns=list)
    def dir(self, obj) -> list:
        """
        List available attributes and methods of an object or module.

        Returns array of strings representing available members.

        Examples:
            members = dir(math);  // ["pi", "e", "sqrt", "sin", ...]
            methods = dir([1,2,3]);  // ["length", "push", "pop", ...]
        """

    @ml_function(params={"obj": Any}, returns=str)
    def info(self, obj) -> str:
        """
        Get documentation string for an object, function, or module.

        Returns formatted documentation with signature and description.

        Examples:
            doc = info(math.sqrt);  // "sqrt(x: float) -> float\n\n..."
            module_doc = info(math);  // "Math module documentation..."
        """

    @ml_function(params={"obj": Any, "attr": str}, returns=bool)
    def hasattr(self, obj, attr: str) -> bool:
        """
        Check if object has attribute.

        Examples:
            hasattr(math, "pi") // true
            hasattr(math, "nonexistent") // false
        """

    @ml_function(params={"obj": Any, "attr": str}, returns=Any)
    def getattr(self, obj, attr: str):
        """
        Get attribute value from object dynamically.

        Examples:
            value = getattr(math, "pi");  // Same as math.pi
            func = getattr(math, "sqrt");  // Get function reference
        """

    @ml_function(params={"obj": Any, "attr": str, "value": Any}, returns=None)
    def setattr(self, obj, attr: str, value):
        """
        Set attribute value on object dynamically.

        Examples:
            setattr(obj, "name", "John");  // Same as obj.name = "John"
        """

    @ml_function(params={"func": Callable, "args": list}, returns=Any)
    def call(self, func, args: list):
        """
        Call a function with array of arguments.

        Enables dynamic function calling without capability escape.

        Examples:
            result = call(math.sqrt, [16]);  // 4.0
            call(print, ["Hello", "World"]);
        """

    # ============================================================
    # Container Functions
    # ============================================================

    @ml_function(params={"container": Any}, returns=int)
    def len(self, container) -> int:
        """
        Get length of string, array, or object (number of keys).

        Examples:
            len("hello") // 5
            len([1,2,3]) // 3
            len({a: 1, b: 2}) // 2
        """

    # ============================================================
    # I/O Functions
    # ============================================================

    @ml_function(params={"args": list})
    def print(self, *args):
        """
        Print values to console (space-separated).

        Examples:
            print("Hello");
            print("Result:", 42);
            print(x, y, z);
        """

    @ml_function(params={"prompt": str}, returns=str)
    def input(self, prompt: str = "") -> str:
        """
        Read line of input from user.

        Examples:
            name = input("Enter name: ");
            age = int(input("Enter age: "));
        """

    # ============================================================
    # Object Manipulation
    # ============================================================

    @ml_function(params={"obj": Any})
    def del(self, obj):
        """
        Delete object reference.

        Note: This only removes the reference, not the underlying object
        if other references exist.
        """

    # ============================================================
    # System Functions
    # ============================================================

    @ml_function(params={"code": int}, returns=None)
    def exit(self, code: int = 0):
        """
        Exit program with status code.

        Examples:
            exit(0);  // Exit successfully
            exit(1);  // Exit with error
        """

    @ml_function(returns=str)
    def version(self) -> str:
        """
        Get mlpy version information.

        Returns version string like "mlpy 2.0.0"
        """

    # ============================================================
    # Built-in Classes (Advanced)
    # ============================================================

    @ml_class(name="String", capabilities=[])
    class String:
        """String manipulation class with methods."""

        @ml_function
        def upper(self) -> str:
            """Convert to uppercase."""

        @ml_function
        def lower(self) -> str:
            """Convert to lowercase."""

        @ml_function
        def split(self, separator: str = " ") -> list:
            """Split string into array."""

        # ... more string methods

    @ml_class(name="List", capabilities=[])
    class List:
        """Array/list manipulation class."""

        @ml_function
        def push(self, item):
            """Add item to end of array."""

        @ml_function
        def pop(self):
            """Remove and return last item."""

        @ml_function
        def map(self, func):
            """Apply function to each element."""

        # ... more array methods

    @ml_class(name="Dict", capabilities=[])
    class Dict:
        """Dictionary/object manipulation class."""

        @ml_function
        def keys(self) -> list:
            """Get list of keys."""

        @ml_function
        def values(self) -> list:
            """Get list of values."""

        @ml_function
        def has(self, key: str) -> bool:
            """Check if key exists."""

        # ... more dict methods
```

### Auto-Import Implementation

**How builtin is made available**:

1. Code generator detects `auto_import=True` on builtin module
2. Generates preamble that imports builtin into global scope:

```python
# Auto-generated preamble in every ML program
from mlpy.stdlib.builtin import builtin

# Expose builtin functions to global scope
int = builtin.int
float = builtin.float
str = builtin.str
bool = builtin.bool
type = builtin.type
typeof = builtin.typeof
len = builtin.len
print = builtin.print
input = builtin.input
dir = builtin.dir
info = builtin.info
hasattr = builtin.hasattr
getattr = builtin.getattr
setattr = builtin.setattr
call = builtin.call
del_obj = builtin.del  # 'del' is Python keyword
exit = builtin.exit
version = builtin.version
isinstance = builtin.isinstance

# User code follows...
```

## Automatic Module Discovery

### Registry Auto-Discovery

**File**: `src/mlpy/stdlib/registry.py` (simplified)

**New Approach**:

```python
class ModuleRegistry:
    """Auto-discovering module registry using decorators."""

    _instance = None
    _modules: dict[str, MLModuleMetadata] = {}

    @classmethod
    def register(cls, metadata: MLModuleMetadata):
        """Register module (called by @ml_module decorator)."""
        cls._modules[metadata.name] = metadata

    @classmethod
    def get(cls, name: str) -> MLModuleMetadata | None:
        """Get module by name."""
        return cls._modules.get(name)

    @classmethod
    def discover_stdlib(cls):
        """
        Auto-discover all stdlib modules.

        Imports all Python files in mlpy.stdlib/, triggering decorator
        registration.
        """
        import importlib
        import pkgutil
        import mlpy.stdlib

        for importer, modname, ispkg in pkgutil.iter_modules(mlpy.stdlib.__path__):
            if not modname.startswith('_'):  # Skip private modules
                importlib.import_module(f'mlpy.stdlib.{modname}')

        # All @ml_module decorators have now run, registry is populated!
```

**How it works**:

1. At startup, `discover_stdlib()` imports all files in `mlpy.stdlib/`
2. Each file has `@ml_module` decorators that call `ModuleRegistry.register()`
3. Registry is fully populated without any manual registration code
4. New modules only need to add `@ml_module` decorator and be in stdlib directory

**Example** - Adding a new module:

```python
# src/mlpy/stdlib/crypto.py

from mlpy.stdlib.decorators import ml_module, ml_function
import hashlib

@ml_module(name="crypto", capabilities=["execute:cryptography"])
class Crypto:
    """Cryptographic functions."""

    @ml_function
    def sha256(self, text: str) -> str:
        """Compute SHA-256 hash of text."""
        return hashlib.sha256(text.encode()).hexdigest()

    @ml_function
    def md5(self, text: str) -> str:
        """Compute MD5 hash of text."""
        return hashlib.md5(text.encode()).hexdigest()
```

**That's it!** Module is automatically discovered and available. No changes needed to:
- ❌ `python_generator.py` (no hardcoded list)
- ❌ `registry.py` (no manual registration)
- ❌ `__init__.py` (auto-exported)

## Capability Integration

### Module-Level Capabilities

When ML code imports a module, the required capabilities are automatically granted to the current context:

```python
# In ModuleResolver.resolve_import()
def resolve_import(self, import_target: list[str], source_file: str = None):
    module_info = self._resolve_module(import_target)

    # NEW: Grant capabilities when importing
    if module_info.capabilities_required:
        current_context = get_current_context()
        if not current_context:
            raise CapabilityError("Cannot import module outside capability context")

        for cap in module_info.capabilities_required:
            # Create capability token for this module
            token = CapabilityToken(
                capability_type=cap,
                constraints=CapabilityConstraint(
                    resource_patterns=[f"module:{module_info.name}:*"]
                )
            )
            current_context.add_capability(token)

    return module_info
```

### Function-Level Capability Checks

When ML code calls a decorated function, the wrapper checks capabilities:

```python
# Generated by @ml_function decorator
def sqrt_wrapper(x):
    # Check if current context has required capability
    if not has_capability("execute:calculations"):
        raise CapabilityNotFoundError(
            "Function math.sqrt requires capability 'execute:calculations'"
        )

    # Track capability usage
    use_capability("execute:calculations", resource="math.sqrt", operation="call")

    # Call actual function
    return math_instance.sqrt(x)
```

### Capability Metadata in Introspection

ML code can query capability requirements:

```ml
import builtin;
import math;

// Query module capabilities
caps = info(math).capabilities;  // ["execute:calculations"]

// Query function capabilities
func_caps = info(math.sqrt).capabilities;  // ["execute:calculations"]

// Check if we have capability
if (hasattr(builtin, "has_capability")) {
    can_use = builtin.has_capability("execute:calculations");
}
```

## Introspection Implementation

### `dir()` Implementation

```python
@ml_function
def dir(self, obj) -> list:
    """List available members of object or module."""
    if hasattr(obj, '_ml_module_metadata'):
        # This is an ML module - return decorated members
        metadata = obj._ml_module_metadata
        return sorted([
            name for name, member_meta in metadata.members.items()
            if member_meta.exposed
        ])

    elif hasattr(obj, '__dict__'):
        # Regular Python object
        return sorted([
            name for name in dir(obj)
            if not name.startswith('_')
        ])

    else:
        return []
```

### `info()` Implementation

```python
@ml_function
def info(self, obj) -> str:
    """Get documentation for object."""
    if hasattr(obj, '_ml_function_metadata'):
        # This is a decorated function
        meta = obj._ml_function_metadata
        signature = f"{meta.name}({', '.join(f'{p}: {t.__name__}' for p, t in (meta.params or {}).items())})"
        if meta.returns:
            signature += f" -> {meta.returns.__name__}"

        doc = f"{signature}\n\n"
        doc += meta.description or obj.__doc__ or "No documentation available."

        if meta.examples:
            doc += "\n\nExamples:\n"
            for ex in meta.examples:
                doc += f"  {ex}\n"

        if meta.capabilities:
            doc += f"\n\nRequires capabilities: {', '.join(meta.capabilities)}"

        return doc

    elif hasattr(obj, '_ml_module_metadata'):
        # This is a module
        meta = obj._ml_module_metadata
        doc = f"Module: {meta.name} (v{meta.version})\n\n"
        doc += meta.description or "No documentation available."

        if meta.capabilities:
            doc += f"\n\nRequires capabilities: {', '.join(meta.capabilities)}"

        # List available functions
        functions = [name for name, m in meta.members.items() if m.kind == 'function']
        if functions:
            doc += f"\n\nFunctions: {', '.join(sorted(functions))}"

        return doc

    else:
        # Fallback to Python docstring
        return obj.__doc__ or "No documentation available."
```

### Usage Example

```ml
import builtin;
import math;

// List module contents
members = dir(math);
print("Math module has:", len(members), "members");
print("Members:", members);

// Get function documentation
sqrt_doc = info(math.sqrt);
print(sqrt_doc);

// Get module documentation
math_doc = info(math);
print(math_doc);

// Dynamic function calling
func_name = "sqrt";
if (hasattr(math, func_name)) {
    sqrt_func = getattr(math, func_name);
    result = call(sqrt_func, [16.0]);
    print("Dynamic call result:", result);
}
```

## Code Generation Integration

### Simplified Import Handling

**Before** (Hardcoded):

```python
def visit_import_statement(self, node: ImportStatement):
    module_path = ".".join(node.target)

    # HARDCODED LIST!
    if module_path in ["math", "json", "datetime", "random", ...]:
        python_module_path = f"mlpy.stdlib.{module_path}_bridge"
        self._emit_line(f"from {python_module_path} import {module_path}", node)
    else:
        self._emit_line(f"# WARNING: Unknown import", node)
```

**After** (Dynamic):

```python
def visit_import_statement(self, node: ImportStatement):
    module_path = ".".join(node.target)

    # Resolve module dynamically
    module_info = self.resolver.resolve_import(node.target, self.source_file)

    if module_info.is_python:
        # Python stdlib module
        self._emit_line(
            f"from {module_info.python_path} import {module_info.export_name}",
            node
        )
    else:
        # ML module - would need transpilation
        # For now, assume transpiled modules are pre-compiled
        self._emit_line(
            f"from mlpy.userlib.{module_path} import module as {node.alias or module_path}",
            node
        )

    # Capability granting happens in resolver, not here!
```

## User Module Support

The same decorator system works for user modules!

**User Module Example** (`mymodule.py`):

```python
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="mymodule", capabilities=["user:custom"])
class MyModule:
    """User-defined module example."""

    @ml_function
    def my_function(self, x: int) -> int:
        """Double the input."""
        return x * 2
```

**ML Code**:

```ml
import mymodule;  // Automatically discovered if in import paths

result = mymodule.my_function(21);  // 42
```

**Setup**:

1. User creates `mymodule.py` with `@ml_module` decorator
2. User runs: `mlpy run --import-paths ./my_modules script.ml`
3. Resolver discovers user module via decorator registry
4. Code generator creates import
5. Capabilities are checked at runtime
6. It just works!

## Summary of Improvements

### Compared to Current System

| Aspect | Current | Future |
|--------|---------|--------|
| **Adding new module** | 4 files, 100+ lines | 1 file, ~30 lines |
| **Capability enforcement** | Not enforced | Enforced at runtime |
| **Introspection** | None | `dir()`, `info()`, `hasattr()`, etc. |
| **Built-in functions** | Scattered in `__init__.py` | Organized in `builtin` module |
| **User modules** | Not supported | Fully supported |
| **Documentation** | Docstrings hidden | Accessible via `info()` |
| **Auto-discovery** | Manual registration | Automatic via decorators |
| **Code generator** | Hardcoded module list | Dynamic resolution |
| **Capability granting** | Not implemented | Automatic on import |
| **Metadata** | Duplicated | Single source of truth |

### Lines of Code Reduction

| Component | Current | Future | Reduction |
|-----------|---------|--------|-----------|
| `registry.py` _register_core_modules() | 668 lines | **Deleted** | -100% |
| Adding new module (total) | ~150 lines | ~30 lines | -80% |
| `python_generator.py` import handling | 37 lines | ~15 lines | -60% |
| `__init__.py` | 138 lines | ~20 lines | -85% |

### Developer Experience

**Adding a new stdlib module (crypto)**:

**Current**:
1. Create `crypto_bridge.py` (50 lines)
2. Create `crypto.ml` (optional, 100+ lines)
3. Update `registry.py` `_register_core_modules()` (50+ lines)
4. Update `python_generator.py` hardcoded list (1 line)
5. Update `__init__.py` imports and `__all__` (2 lines)
6. Total: 5 files, ~200+ lines of code

**Future**:
1. Create `crypto.py` with decorators (30 lines)
2. Total: 1 file, 30 lines of code

**Reduction**: From 5 files / 200+ lines → 1 file / 30 lines = **85% reduction**

## Conclusion

The future module system transforms mlpy from a prototype with ad-hoc module management into a production-ready platform with:

✅ **Decorator-driven design** - Automatic registration, metadata extraction
✅ **Security-first** - Capabilities enforced, not just documented
✅ **Introspection-friendly** - ML code can explore modules and functions
✅ **Organized built-ins** - Clear `builtin` module for core functionality
✅ **User extensible** - Same system works for user modules
✅ **Maintainable** - 80%+ reduction in boilerplate code
✅ **Documented** - Documentation accessible from ML code

This design provides a solid foundation for mlpy to grow into a mature, secure scripting language with a rich ecosystem of modules.
