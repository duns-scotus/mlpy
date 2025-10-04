# ML Module System 2.0: Implementation Plan (Clean Slate Edition)

**Version**: 2.0.0-CLEAN-SLATE
**Date**: 2025-10-03 (Updated: 2025-01-06)
**Status**: STREAMLINED IMPLEMENTATION GUIDE - NO BACKWARD COMPATIBILITY
**Est. Duration**: 3-4 weeks (clean build from scratch)

---

## 🔴 IMPORTANT: Architecture Decision (2025-01-06)

**READ FIRST**: [ARCHITECTURE-PRIMITIVES-VS-MODULES.md](./ARCHITECTURE-PRIMITIVES-VS-MODULES.md)

**Key Changes**:
- **Primitives** (string, int, float, array, dict) are NOT modules - they're methods on values (no import needed)
- **Utility Modules** (console, math, regex, datetime, etc.) require explicit import
- **Phase 3** migrates ONLY utility modules with OOP patterns (Pattern objects, DateTime objects)
- **Phase 4** implements builtin.py + registers primitive methods with SafeAttributeRegistry

---

## Table of Contents

1. [Implementation Philosophy](#implementation-philosophy)
2. [Phase 0: Clean the Slate](#phase-0-clean-the-slate)
3. [Phase 1: Decorator System Foundation](#phase-1-decorator-system-foundation)
4. [Phase 2: Core Module Implementation](#phase-2-core-module-implementation)
5. [Phase 3: Advanced Modules & Capability Integration](#phase-3-advanced-modules--capability-integration)
6. [Phase 4: Builtin Module Implementation](#phase-4-builtin-module-implementation)
7. [Phase 5: Testing & Validation](#phase-5-testing--validation)
8. [Testing Strategy](#testing-strategy)
9. [Success Metrics](#success-metrics)

---

## Implementation Philosophy

### Core Principles

**1. Clean Slate Approach**
- NO backward compatibility with old stdlib
- No ML code in the wild to maintain
- Freedom to build it right from scratch
- Delete old implementations immediately

**2. Language-First Design**
- ml_core tests are our safety net (pure language features)
- Stdlib is a separate layer we rebuild cleanly
- No auto-imports - explicit imports only
- Generated code should be minimal and clean

**3. Test-Driven Development**
- Write tests ALONGSIDE new modules
- 95%+ coverage requirement maintained
- Security tests expanded, not reduced

**4. Capability-Ready Architecture**
- Decorators declare capabilities from day one
- Infrastructure ready for future policy system
- @ml_module(capabilities=[...]) is the integration point

**5. Amazing Developer Experience**
- One file per module with all logic
- Clear decorator pattern
- Self-documenting code
- Minimal boilerplate

### Risk Mitigation

**Technical Risks**:
- SafeAttributeRegistry integration → Extensive security tests
- Capability system integration → Comprehensive unit tests
- Performance regression → Benchmark after each phase

**Schedule Risks**: MINIMAL
- Building from scratch is faster than maintaining compatibility
- Clear validation points (ml_core tests)
- No migration complexity

---

## Phase 0: Clean the Slate

**Duration**: 30 minutes - 1 hour (+ 30 min preparatory test fixes)
**Goal**: Remove old stdlib auto-imports, validate ml_core tests pass

### Pre-Phase 0: Fix Unit Tests First

⚠️ **IMPORTANT**: Complete test fixes BEFORE Phase 0
**Document**: See `PRE-PHASE-0-TEST-FIXES.md` for detailed instructions

**Quick Summary**:
1. Delete `test_stdlib_imports_in_header` from `tests/unit/codegen/test_python_generator.py`
2. Add `@pytest.mark.skip` to all test classes in `tests/unit/test_regex_module.py`
3. Validate: `pytest tests/unit/ -v` (should pass/skip, no failures)

**Why**: These tests depend on old stdlib we're about to delete

### Critical Discovery

**What ml_core tests actually do**:
- ✅ Test pure ML language features (no stdlib imports)
- ✅ 25/25 tests passing (100% success rate)
- ❌ **DON'T import** any stdlib modules explicitly
- ⚠️ **BUT** generated Python has auto-imports (dead code)

**Auto-imports in python_generator.py (lines 120-121)**:
```python
self._emit_line("from mlpy.stdlib.console_bridge import console")
self._emit_line("from mlpy.stdlib import getCurrentTime, processData, typeof")
```

These are **NEVER USED** in ml_core tests!

### Tasks

#### 0.1 Remove Auto-Imports from Code Generator

**File**: `src/mlpy/ml/codegen/python_generator.py`

**Action**: Delete or comment out lines 120-121:

```python
# BEFORE (lines 118-122):
# Auto-import ML standard library (using specific imports to avoid syntax issues)
self._emit_line("# ML Standard Library imports")
self._emit_line("from mlpy.stdlib.console_bridge import console")
self._emit_line("from mlpy.stdlib import getCurrentTime, processData, typeof")
self._emit_line("")

# AFTER:
# ML Standard Library imports - REMOVED (explicit imports only)
# Programs must explicitly import what they need: import math, import string, etc.
```

#### 0.2 Validate ml_core Tests Still Pass

**Run ml_core test suite**:
```bash
python tests/ml_test_runner.py --full --category ml_core
```

**Expected result**: ✅ 25/25 tests PASS (no change)

**Why they pass**: ml_core tests use ONLY language features:
- Recursion, loops, functions, closures
- Arrays, objects, operators
- Control flow, exceptions
- NO stdlib function calls

#### 0.3 Clean stdlib __init__.py

**File**: `src/mlpy/stdlib/__init__.py`

**Action**: Delete ad-hoc helper functions (getCurrentTime, processData, typeof)

```python
# BEFORE (lines 34-63): Ad-hoc functions
def getCurrentTime(): ...
def processData(data): ...
def typeof(value): ...
def int(value): ...
def float(value): ...
def str(value): ...

# AFTER: Clean slate
# These will be reimplemented properly in builtin.py with decorators
```

#### 0.4 Archive Old Stdlib Modules

**Action**: Move old bridge modules to archive:
```bash
mkdir -p src/mlpy/stdlib/_archive_old_bridge
mv src/mlpy/stdlib/*_bridge.py src/mlpy/stdlib/_archive_old_bridge/
```

**Or delete entirely** (recommended):
```bash
rm src/mlpy/stdlib/*_bridge.py
```

**Keep only**:
- `registry.py` (will be rewritten)
- `runtime_helpers.py` (safe_attr_access - keep as-is)
- `__init__.py` (cleaned)

### Validation Checklist

- [ ] Auto-imports removed from python_generator.py
- [ ] ml_core tests pass: 25/25 (100%)
- [ ] stdlib/__init__.py cleaned (no ad-hoc functions)
- [ ] Old bridge modules archived or deleted
- [ ] Baseline established: "This is our clean starting point"

**Deliverables**:
- ✅ Clean python_generator.py (no auto-imports)
- ✅ ml_core tests validated (language features work)
- ✅ stdlib directory cleaned
- ✅ Ready for new module system

---

## Phase 1: Decorator System Foundation

**Duration**: 1.5 weeks
**Goal**: Implement complete decorator system, test without removing manual registration

### Tasks

#### 1.1 Implement @ml_module Decorator

**File**: `src/mlpy/stdlib/decorators.py`

**Implementation**:

```python
def ml_module(name, capabilities=None, description=None, version="1.0.0", auto_import=False):
    """
    Decorator marking Python class as ML stdlib module.
    """
    def decorator(cls):
        # Collect @ml_function decorated methods
        members = {}
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if hasattr(attr, '_ml_function_metadata'):
                members[attr._ml_function_metadata['name']] = attr._ml_function_metadata

        # Store metadata on class
        cls._ml_module_metadata = {
            'name': name,
            'capabilities': capabilities or [],
            'description': description or cls.__doc__ or "",
            'version': version,
            'auto_import': auto_import,
            'members': members,
        }

        # Register with stdlib registry
        from mlpy.stdlib.registry import get_stdlib_registry
        registry = get_stdlib_registry()

        from mlpy.ml.resolution.module_info import ModuleInfo
        module_info = ModuleInfo(
            name=name,
            module_path=name,
            ast=None,
            source_code=None,
            file_path=None,
            is_stdlib=True,
            is_python=True,
            capabilities_required=capabilities or [],
            module_metadata=cls._ml_module_metadata
        )

        registry.register_module(name, module_info)

        # Register custom classes with SafeAttributeRegistry
        if hasattr(cls, '_ml_custom_classes'):
            from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry
            safe_registry = get_safe_registry()
            for class_name, methods in cls._ml_custom_classes.items():
                safe_registry.register_custom_class(class_name, methods)

        return cls

    return decorator
```

**Tests**:
```python
# tests/unit/stdlib/test_decorators.py

def test_ml_module_stores_metadata():
    @ml_module(name="test", capabilities=["test:read"])
    class TestModule:
        """Test module."""
        pass

    assert hasattr(TestModule, '_ml_module_metadata')
    assert TestModule._ml_module_metadata['name'] == "test"
    assert TestModule._ml_module_metadata['capabilities'] == ["test:read"]

def test_ml_module_registers_with_registry():
    @ml_module(name="test_registry")
    class TestModule:
        pass

    from mlpy.stdlib.registry import get_stdlib_registry
    registry = get_stdlib_registry()
    module_info = registry.get_module("test_registry")

    assert module_info is not None
    assert module_info.name == "test_registry"
```

#### 1.2 Implement @ml_function Decorator

**Implementation with capability checking**:

```python
def ml_function(func=None, *, name=None, capabilities=None, params=None,
                returns=None, description=None, examples=None):
    """
    Decorator marking method as ML-callable with capability checking.
    """
    def decorator(fn):
        fn._ml_function_metadata = {
            'name': name or fn.__name__,
            'capabilities': capabilities or [],
            'params': params or {},
            'returns': returns,
            'description': description or fn.__doc__ or "",
            'examples': examples or [],
            'exposed': True,
        }

        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            # Get all required capabilities
            module_caps = getattr(self.__class__, '_ml_module_metadata', {}).get('capabilities', [])
            func_caps = fn._ml_function_metadata['capabilities']
            all_caps = set(module_caps + func_caps)

            # Check capabilities
            if all_caps:
                from mlpy.runtime.capabilities.manager import has_capability
                from mlpy.runtime.capabilities.exceptions import CapabilityNotFoundError

                for cap in all_caps:
                    if not has_capability(cap):
                        raise CapabilityNotFoundError(
                            cap,
                            message=f"Function '{fn.__name__}' requires capability '{cap}'"
                        )

            # Execute function
            return fn(self, *args, **kwargs)

        wrapper._ml_function_metadata = fn._ml_function_metadata
        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)
```

**Tests**:
```python
def test_ml_function_stores_metadata():
    @ml_function(params={"x": int}, returns=int)
    def test_func(self, x):
        return x * 2

    assert hasattr(test_func, '_ml_function_metadata')
    assert test_func._ml_function_metadata['params'] == {"x": int}

def test_ml_function_capability_checking():
    @ml_module(name="test", capabilities=["test:execute"])
    class TestModule:
        @ml_function
        def protected_func(self):
            return "success"

    # Without capability context - should fail
    module = TestModule()
    with pytest.raises(CapabilityNotFoundError):
        module.protected_func()

    # With capability context - should succeed
    from mlpy.runtime.capabilities.manager import get_capability_manager
    from mlpy.runtime.capabilities.tokens import create_capability_token

    manager = get_capability_manager()
    token = create_capability_token("test:execute")
    with manager.capability_context(capabilities=[token]):
        result = module.protected_func()
        assert result == "success"
```

#### 1.3 Implement @ml_class Decorator

**Implementation**:

```python
def ml_class(name=None, safe_expose=False, capabilities=None):
    """
    Decorator for safely exposing Python class to ML.
    """
    def decorator(cls):
        cls._ml_class_metadata = {
            'name': name or cls.__name__,
            'safe_expose': safe_expose,
            'capabilities': capabilities or [],
        }

        if safe_expose:
            # Collect safe methods from @ml_function decorators
            from mlpy.ml.codegen.safe_attribute_registry import SafeAttribute, AttributeAccessType
            safe_methods = {}

            for attr_name in dir(cls):
                if attr_name.startswith('_'):
                    continue

                attr = getattr(cls, attr_name)
                if hasattr(attr, '_ml_function_metadata'):
                    metadata = attr._ml_function_metadata
                    safe_methods[metadata['name']] = SafeAttribute(
                        name=metadata['name'],
                        access_type=AttributeAccessType.METHOD,
                        required_capabilities=metadata['capabilities'],
                        description=metadata['description']
                    )

            # Store for parent module to register
            # Find parent class with _ml_module_metadata
            for base in cls.__mro__[1:]:
                if hasattr(base, '_ml_module_metadata'):
                    if not hasattr(base, '_ml_custom_classes'):
                        base._ml_custom_classes = {}
                    base._ml_custom_classes[cls._ml_class_metadata['name']] = safe_methods
                    break

        return cls

    return decorator
```

**Tests**:
```python
def test_ml_class_safe_expose():
    @ml_class(name="TestClass", safe_expose=True)
    class TestClass:
        @ml_function
        def safe_method(self):
            return "safe"

    assert hasattr(TestClass, '_ml_class_metadata')
    assert TestClass._ml_class_metadata['safe_expose'] == True

def test_ml_class_registers_with_safe_registry():
    @ml_module(name="test")
    class TestModule:
        @ml_class(name="SafeClass", safe_expose=True)
        class SafeClass:
            @ml_function
            def method1(self):
                pass

            @ml_function
            def method2(self):
                pass

    # Check that custom class was registered
    from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry
    registry = get_safe_registry()

    # After @ml_module processes the class
    assert "SafeClass" in registry._custom_classes
    assert "method1" in registry._custom_classes["SafeClass"]
    assert "method2" in registry._custom_classes["SafeClass"]
```

#### 1.4 Test Decorator System with One Module

**Migrate math_bridge.py as proof-of-concept**:

**Create**: `src/mlpy/stdlib/math_decorated.py` (alongside existing math_bridge.py)

```python
"""
Math module using decorator system (Phase 1 proof-of-concept).
"""

from mlpy.stdlib.decorators import ml_module, ml_function
import math as py_math

@ml_module(
    name="math_decorated",
    capabilities=["execute:calculations"],
    description="Mathematical operations with decorator system",
    version="2.0.0"
)
class MathDecorated:
    """Mathematical operations using decorator system."""

    def __init__(self):
        self.PI = py_math.pi
        self.E = py_math.e

    @ml_function(
        params={"x": float},
        returns=float,
        description="Compute square root of x",
        examples=["math.sqrt(16) // 4.0"]
    )
    def sqrt(self, x: float) -> float:
        if x < 0:
            raise ValueError("Cannot compute square root of negative number")
        return py_math.sqrt(x)

    @ml_function(params={"x": float, "y": float}, returns=float)
    def pow(self, x: float, y: float) -> float:
        return py_math.pow(x, y)

    # ... implement remaining functions ...
```

**Tests**:
```python
# tests/unit/stdlib/test_math_decorated.py

def test_math_decorated_module_registration():
    from mlpy.stdlib.registry import get_stdlib_registry
    registry = get_stdlib_registry()
    module_info = registry.get_module("math_decorated")

    assert module_info is not None
    assert "execute:calculations" in module_info.capabilities_required

def test_math_decorated_sqrt():
    from mlpy.stdlib.math_decorated import MathDecorated
    math = MathDecorated()

    # Create capability context
    from mlpy.runtime.capabilities.manager import get_capability_manager
    from mlpy.runtime.capabilities.tokens import create_capability_token

    manager = get_capability_manager()
    token = create_capability_token("execute:calculations")

    with manager.capability_context(capabilities=[token]):
        result = math.sqrt(16)
        assert result == 4.0

def test_math_decorated_sqrt_without_capability():
    from mlpy.stdlib.math_decorated import MathDecorated
    math = MathDecorated()

    # Without capability - should fail
    with pytest.raises(CapabilityNotFoundError):
        math.sqrt(16)
```

**Deliverables**:
- ✅ Complete decorator implementation
- ✅ Decorator unit tests passing (100% coverage)
- ✅ Proof-of-concept module (math_decorated) working
- ✅ Capability checking functional
- ✅ SafeAttributeRegistry integration tested

---

## Phase 2: Capability Integration

**Duration**: 1 week
**Goal**: Connect capability system to imports and code generation

### Tasks

#### 2.1 Enhance ModuleResolver for Capability Extraction

**File**: `src/mlpy/ml/resolution/resolver.py`

**Add method**:

```python
class ModuleResolver:
    # ... existing methods ...

    def _enhance_with_capabilities(self, module_info: ModuleInfo) -> ModuleInfo:
        """Extract and populate capabilities in ModuleInfo."""
        if module_info.is_stdlib:
            # Already populated by @ml_module decorator
            pass
        elif module_info.file_path and module_info.ast:
            # Extract from .ml AST
            module_info.capabilities_required = self._extract_capabilities_from_ast(module_info.ast)

        return module_info

    def _extract_capabilities_from_ast(self, ast: Program) -> list[str]:
        """
        Extract capability declarations from .ml AST.

        Parses: capability Name { allow operation "resource"; }
        """
        capabilities = []

        for item in ast.items:
            if hasattr(item, '__class__') and item.__class__.__name__ == 'CapabilityStatement':
                if hasattr(item, 'grants'):
                    for grant in item.grants:
                        capability_str = f"{grant.operation}:{grant.resource}"
                        capabilities.append(capability_str)

        return capabilities
```

**Modify existing methods**:

```python
def _resolve_stdlib_module(self, module_path: str) -> ModuleInfo | None:
    """Try to resolve module from stdlib registry."""
    registry = get_stdlib_registry()
    module_info = registry.get_module(module_path)

    if module_info:
        # Capabilities already populated by decorator
        return module_info

    return None

def _load_ml_file(self, file_path: str, module_path: str) -> ModuleInfo:
    """Load and parse .ml file."""
    # ... existing code ...

    # NEW: Extract capabilities
    capabilities = self._extract_capabilities_from_ast(ast)

    return ModuleInfo(
        # ... existing fields ...
        capabilities_required=capabilities,  # ← NOW POPULATED
    )
```

**Tests**:
```python
def test_resolver_extracts_capabilities_from_decorator():
    resolver = ModuleResolver()
    module_info = resolver.resolve_import(["math_decorated"])

    assert "execute:calculations" in module_info.capabilities_required

def test_resolver_extracts_capabilities_from_ml_ast():
    # Create test .ml file with capability statement
    test_ml = """
    capability MathOps {
        allow execute "calculations";
    }

    function sqrt(x) {
        return Math.sqrt(x);
    }
    """

    # Write to temp file
    with tempfile.NamedTemporaryFile(suffix='.ml', delete=False) as f:
        f.write(test_ml.encode())
        temp_path = f.name

    try:
        resolver = ModuleResolver(import_paths=[os.path.dirname(temp_path)])
        module_name = os.path.basename(temp_path).replace('.ml', '')
        module_info = resolver.resolve_import([module_name])

        assert "execute:calculations" in module_info.capabilities_required
    finally:
        os.unlink(temp_path)
```

#### 2.2 Add Runtime Helper for Capability Granting

**File**: `src/mlpy/stdlib/runtime_helpers.py`

**Add function**:

```python
def _grant_capability(capability_type: str, from_import: str):
    """
    Grant capability to current context (called from generated code).

    Args:
        capability_type: Type of capability (e.g., "execute:calculations")
        from_import: Module that requires this capability
    """
    from mlpy.runtime.capabilities.manager import get_capability_manager
    from mlpy.runtime.capabilities.tokens import create_capability_token
    from mlpy.runtime.capabilities.context import get_current_context, set_current_context

    context = get_current_context()
    if not context:
        # Create default context if none exists
        manager = get_capability_manager()
        context = manager.create_context(name="main_execution")
        set_current_context(context)

    # Create capability token for this import
    token = create_capability_token(
        capability_type=capability_type,
        description=f"Granted by import {from_import}",
        created_by="import_system"
    )

    context.add_capability(token)
```

**Export**:
```python
__all__ = [
    # ... existing exports ...
    '_grant_capability',
]
```

**Tests**:
```python
def test_grant_capability_creates_token():
    from mlpy.runtime.capabilities.context import get_current_context, set_current_context
    from mlpy.runtime.capabilities.manager import get_capability_manager

    # Create context
    manager = get_capability_manager()
    context = manager.create_context(name="test")
    set_current_context(context)

    # Grant capability
    _grant_capability("test:read", "test_module")

    # Verify token exists
    assert context.has_capability("test:read")

def test_grant_capability_creates_context_if_missing():
    from mlpy.runtime.capabilities.context import get_current_context, set_current_context

    # Ensure no context
    set_current_context(None)

    # Grant capability should create context
    _grant_capability("test:read", "test_module")

    # Verify context was created
    context = get_current_context()
    assert context is not None
    assert context.has_capability("test:read")
```

#### 2.3 Enhance Code Generator for Capability Grants

**File**: `src/mlpy/ml/codegen/python_generator.py`

**Modify visit_import_statement**:

```python
def visit_import_statement(self, stmt: ImportStatement) -> str:
    """Generate import with capability granting."""
    # Resolve module (existing)
    module_info = self.resolver.resolve_import(
        stmt.target,
        source_file=self.source_file
    )

    # Record import
    self.context.imported_modules.add(module_info.module_path)

    # Generate Python import (existing logic)
    if module_info.is_stdlib:
        python_module_name = module_info.module_path.replace('.', '_')
        import_code = f"from mlpy.stdlib.{python_module_name}_bridge import {module_info.name}"
    elif module_info.is_python:
        import_code = f"import {module_info.module_path}"
    else:
        # User .ml module
        import_code = self._generate_ml_module_import(module_info)

    # NEW: Generate capability grants
    if module_info.capabilities_required:
        self._ensure_capability_helpers_imported()

        capability_grants = []
        for cap in module_info.capabilities_required:
            capability_grants.append(
                f"_grant_capability({repr(cap)}, from_import={repr(module_info.module_path)})"
            )

        return import_code + "\n" + "\n".join(capability_grants)

    return import_code

def _ensure_capability_helpers_imported(self):
    """Ensure capability runtime helpers are imported."""
    if not hasattr(self.context, 'capability_helpers_imported'):
        self.context.capability_helpers_imported = True
        # Add to imports (will be emitted in header)
        if not hasattr(self.context, 'required_imports'):
            self.context.required_imports = set()
        self.context.required_imports.add('_grant_capability')
```

**Modify header generation**:

```python
def _generate_header(self) -> str:
    """Generate Python file header with imports."""
    header_lines = []

    # Required runtime helpers
    runtime_helpers = ["safe_attr_access", "_safe_attr_access", "is_ml_object"]
    if hasattr(self.context, 'required_imports'):
        runtime_helpers.extend(self.context.required_imports)

    if runtime_helpers:
        header_lines.append(
            f"from mlpy.stdlib.runtime_helpers import {', '.join(sorted(set(runtime_helpers)))}"
        )

    # ... rest of header generation ...

    return "\n".join(header_lines)
```

**Tests**:
```python
def test_code_generator_emits_capability_grants():
    ml_code = """
    import math_decorated;
    result = math_decorated.sqrt(16);
    """

    from mlpy.ml.transpiler import MLTranspiler
    transpiler = MLTranspiler()
    python_code, issues, source_map = transpiler.transpile_to_python(ml_code)

    # Verify capability grant is emitted
    assert "_grant_capability('execute:calculations'" in python_code
    assert "from_import='math_decorated'" in python_code

def test_code_generator_imports_grant_capability():
    ml_code = "import math_decorated;"

    transpiler = MLTranspiler()
    python_code, _, _ = transpiler.transpile_to_python(ml_code)

    # Verify import
    assert "_grant_capability" in python_code
    assert "from mlpy.stdlib.runtime_helpers import" in python_code
```

#### 2.4 End-to-End Capability Flow Test

**Test file**: `tests/integration/test_capability_flow.py`

```python
def test_end_to_end_capability_flow():
    """Test complete capability flow from import to function execution."""

    # ML code that imports and uses module
    ml_code = """
    import math_decorated;
    result = math_decorated.sqrt(16);
    """

    # Transpile to Python
    from mlpy.ml.transpiler import MLTranspiler
    transpiler = MLTranspiler()
    python_code, issues, _ = transpiler.transpile_to_python(ml_code)

    assert python_code is not None
    assert len(issues) == 0

    # Execute generated Python
    from mlpy.runtime.capabilities.manager import get_capability_manager
    from mlpy.runtime.capabilities.context import set_current_context

    # Create execution context
    manager = get_capability_manager()
    context = manager.create_context(name="test_execution")
    set_current_context(context)

    # Execute
    exec_globals = {}
    exec(python_code, exec_globals)

    # Verify result
    assert exec_globals['result'] == 4.0

    # Verify capability was granted
    assert context.has_capability("execute:calculations")

def test_capability_denied_without_import():
    """Test that function fails without capability grant from import."""
    from mlpy.stdlib.math_decorated import MathDecorated
    from mlpy.runtime.capabilities.context import set_current_context
    from mlpy.runtime.capabilities.manager import get_capability_manager

    # Create context WITHOUT capability
    manager = get_capability_manager()
    context = manager.create_context(name="test_no_cap")
    set_current_context(context)

    math = MathDecorated()

    # Should fail without capability
    with pytest.raises(CapabilityNotFoundError):
        math.sqrt(16)
```

**Deliverables**:
- ✅ ModuleResolver extracts capabilities
- ✅ Code generator emits capability grants
- ✅ Runtime helper grants capabilities
- ✅ End-to-end flow tested and working
- ✅ All integration tests passing

---

## Phase 2: Core Module Implementation

**Duration**: 1 week
**Goal**: Build core stdlib modules from scratch with decorator system

### Build Strategy

**Clean implementation approach**:
1. Start with simplest module (math)
2. Write comprehensive unit tests ALONGSIDE
3. Build module with decorators from day one
4. Validate with ML test programs
5. Move to next module

### Tasks

#### 2.1 Implement Math Module (Pilot)

**File**: `src/mlpy/stdlib/math.py` (NEW - built from scratch)

```python
"""
ML Math Module - Mathematical operations and constants.

Built with decorator system from day one.
"""

from mlpy.stdlib.decorators import ml_module, ml_function
import math as py_math

@ml_module(
    name="math",
    capabilities=["math:execute"],
    description="Mathematical operations and constants",
    version="2.0.0"
)
class Math:
    """Mathematical operations with capability-based security."""

    def __init__(self):
        """Initialize math constants."""
        self.PI = py_math.pi
        self.E = py_math.e
        self.TAU = py_math.tau

    @ml_function(
        params={"x": float},
        returns=float,
        description="Compute square root of x",
        examples=["math.sqrt(16) // 4.0"]
    )
    def sqrt(self, x: float) -> float:
        """Square root with validation."""
        if x < 0:
            raise ValueError("Cannot compute square root of negative number")
        return py_math.sqrt(x)

    @ml_function(params={"x": float, "y": float}, returns=float)
    def pow(self, x: float, y: float) -> float:
        """Raise x to the power of y."""
        return py_math.pow(x, y)

    @ml_function(params={"x": float}, returns=float)
    def abs(self, x: float) -> float:
        """Absolute value of x."""
        return py_math.fabs(x)

    # Add: sin, cos, tan, floor, ceil, round, etc.
    # ~15-20 essential math functions

# Create singleton for ML imports
math = Math()
```

**Unit tests**: `tests/unit/stdlib/test_math.py`

```python
import pytest
from mlpy.stdlib.math import Math
from mlpy.runtime.capabilities.manager import get_capability_manager
from mlpy.runtime.capabilities.tokens import create_capability_token

def test_math_sqrt():
    """Test square root function."""
    math = Math()

    # Create capability context
    manager = get_capability_manager()
    token = create_capability_token("math:execute")

    with manager.capability_context(capabilities=[token]):
        assert math.sqrt(16) == 4.0
        assert math.sqrt(25) == 5.0

    # Test error handling
    with manager.capability_context(capabilities=[token]):
        with pytest.raises(ValueError):
            math.sqrt(-1)

def test_math_without_capability_fails():
    """Test that math functions fail without capability."""
    math = Math()

    # No capability context
    with pytest.raises(CapabilityNotFoundError):
        math.sqrt(16)

# Add tests for all functions
```

**ML integration test**: `tests/ml_integration/stdlib/test_math_module.ml`

```ml
import math;

result = {
    sqrt_16: math.sqrt(16),
    pow_2_3: math.pow(2, 3),
    pi: math.PI
};
```

#### 2.2 Build Core Modules (Week 1)

**Module order** (simplest to complex):

1. ✅ **math** - Pure functions, no state (pilot - done above)
2. **console** - Simple I/O (print, log, error)
3. **json** - Parse/stringify only
4. **string** - Text manipulation (20+ methods)

**For each module**:

```bash
# 1. Create module file
touch src/mlpy/stdlib/{module_name}.py

# 2. Write module with decorators
# - @ml_module decorator
# - @ml_function for each method
# - Capability declarations

# 3. Write unit tests ALONGSIDE
touch tests/unit/stdlib/test_{module_name}.py
pytest tests/unit/stdlib/test_{module_name}.py -v

# 4. Create ML integration test
touch tests/ml_integration/stdlib/test_{module_name}_module.ml
python tests/ml_test_runner.py --file tests/ml_integration/stdlib/test_{module_name}_module.ml

# 5. Validate
# - Unit tests: 100% coverage
# - ML test: executes correctly
# - Capability checking works
```

**Testing checklist per module**:
- [ ] @ml_module decorator with capabilities
- [ ] All methods have @ml_function
- [ ] Metadata complete (params, returns, description, examples)
- [ ] Unit tests cover all functions
- [ ] ML integration test validates imports work
- [ ] Capability checking functional
- [ ] No security vulnerabilities

**Deliverables**:
- ✅ 4 core modules built from scratch
- ✅ Unit tests: 100% coverage
- ✅ ML integration tests passing
- ✅ Capability system integrated
- ✅ Clean, documented code

---

## Phase 3: Utility Modules Migration (OOP Patterns)

**Duration**: 1 week
**Goal**: Migrate ONLY utility modules with modern OOP patterns

**⚠️ ARCHITECTURE CHANGE**: See [ARCHITECTURE-PRIMITIVES-VS-MODULES.md](./ARCHITECTURE-PRIMITIVES-VS-MODULES.md)

**Primitives** (string, int, float, array, dict) are **NOT migrated in Phase 3**. They will be registered as methods on primitive types in Phase 4.

### Tasks

#### 3.1 Migrate Utility Modules with OOP Patterns

**Modules to migrate** (status as of 2025-01-06):

1. ✅ **console** - Console output/logging (COMPLETED - 12 tests)
2. ✅ **math** - Mathematical operations (COMPLETED - 28 tests)
3. ⏳ **regex** - Pattern matching with Pattern objects (OOP)
4. ⏳ **datetime** - Date/time operations with DateTime objects (OOP)
5. ⏳ **collections** - Advanced data structures with Counter/etc objects (OOP)
6. ⏳ **functional** - Functional programming utilities (pure functions)
7. ⏳ **random** - Random number generation (pure functions)

**Modules to SKIP** (handled in Phase 4 as primitive methods):
- ❌ **string** - Will be primitive methods on str type
- ❌ **int_module** - Will be primitive methods on int type
- ❌ **float_module** - Will be primitive methods on float type

#### 3.1.1 Regex Module (OOP Pattern)

**File**: `src/mlpy/stdlib/regex_bridge.py`

**Modern OOP approach**:

```python
from mlpy.stdlib.decorators import ml_module, ml_function, ml_class

@ml_module(
    name="regex",
    description="Regular expression pattern matching",
    capabilities=["regex.compile", "regex.match"],
    version="1.0.0"
)
class RegexModule:
    @ml_function(description="Compile regex pattern", capabilities=["regex.compile"])
    def compile(self, pattern: str, flags: int = 0):
        """Compile pattern and return Pattern object."""
        import re
        py_pattern = re.compile(pattern, flags)
        return Pattern(py_pattern)

    @ml_function(description="Quick match test", capabilities=["regex.match"])
    def test(self, pattern: str, text: str) -> bool:
        """Quick test without creating Pattern object."""
        import re
        return bool(re.search(pattern, text))

@ml_class(description="Compiled regular expression pattern")
class Pattern:
    def __init__(self, py_pattern):
        self._pattern = py_pattern

    @ml_function(description="Find all matches")
    def findall(self, text: str) -> list:
        return self._pattern.findall(text)

    @ml_function(description="Test if pattern matches")
    def test(self, text: str) -> bool:
        return bool(self._pattern.search(text))

    @ml_function(description="Replace matches")
    def replace(self, text: str, replacement: str) -> str:
        return self._pattern.sub(replacement, text)

    @ml_function(description="Split by pattern")
    def split(self, text: str) -> list:
        return self._pattern.split(text)

# Global instance
regex = RegexModule()
```

**ML Usage**:
```ml
import regex

pattern = regex.compile("\\d+")      // Returns Pattern object
matches = pattern.findall("a1 b2")   // ["1", "2"]
hasMatch = pattern.test("hello 123") // true
```

#### 3.1.2 DateTime Module (OOP Pattern)

**File**: `src/mlpy/stdlib/datetime_bridge.py`

**Modern OOP approach**:

```python
@ml_module(
    name="datetime",
    description="Date and time operations",
    capabilities=["datetime.now", "datetime.parse"],
    version="1.0.0"
)
class DateTimeModule:
    @ml_function(description="Get current date/time", capabilities=["datetime.now"])
    def now(self):
        """Returns DateTime object."""
        from datetime import datetime as py_datetime
        return DateTime(py_datetime.now())

    @ml_function(description="Parse date string", capabilities=["datetime.parse"])
    def parse(self, date_string: str, format: str = None):
        """Returns DateTime object."""
        from datetime import datetime as py_datetime
        if format:
            dt = py_datetime.strptime(date_string, format)
        else:
            dt = py_datetime.fromisoformat(date_string)
        return DateTime(dt)

@ml_class(description="Date and time object")
class DateTime:
    def __init__(self, py_datetime):
        self._dt = py_datetime

    @ml_function(description="Format as string")
    def format(self, format_string: str) -> str:
        return self._dt.strftime(format_string)

    @ml_function(description="Add days")
    def addDays(self, days: int):
        from datetime import timedelta
        return DateTime(self._dt + timedelta(days=days))

    @ml_function(description="Get year")
    def year(self) -> int:
        return self._dt.year

    @ml_function(description="Get timestamp")
    def timestamp(self) -> float:
        return self._dt.timestamp()

# Global instance
datetime = DateTimeModule()
```

**ML Usage**:
```ml
import datetime

now = datetime.now()                 // Returns DateTime object
formatted = now.format("%Y-%m-%d")   // "2025-01-06"
nextWeek = now.addDays(7)            // DateTime object
year = now.year()                    // 2025
```

#### 3.1.3 Collections Module (OOP Pattern)

**Similar OOP pattern with Counter, OrderedDict, etc.**

#### 3.1.4 Functional Module (Pure Functions)

**Pure function approach** (no objects):

```python
@ml_module(name="functional", description="Functional programming utilities")
class FunctionalModule:
    @ml_function(description="Map function over array")
    def map(self, fn, array: list) -> list:
        return [fn(item) for item in array]

    @ml_function(description="Filter array by predicate")
    def filter(self, fn, array: list) -> list:
        return [item for item in array if fn(item)]

    @ml_function(description="Compose functions")
    def compose(self, *functions):
        # Function composition implementation
        ...
```

**Each module follows same pattern as Phase 2**

#### 3.2 Capability Integration in Code Generator

**Update**: `src/mlpy/ml/codegen/python_generator.py`

**Add capability granting on import**:

```python
def visit_import_statement(self, stmt: ImportStatement) -> str:
    """Generate import with capability granting."""
    # Resolve module
    module_info = self.resolver.resolve_import(stmt.target, source_file=self.source_file)

    # Generate Python import
    if module_info.is_stdlib:
        import_code = f"from mlpy.stdlib.{module_info.name} import {module_info.name}"
    else:
        import_code = f"import {module_info.module_path}"

    # Generate capability grants
    if module_info.capabilities_required:
        grants = []
        for cap in module_info.capabilities_required:
            grants.append(f"_grant_capability({repr(cap)}, from_import={repr(module_info.name)})")

        return import_code + "\n" + "\n".join(grants)

    return import_code
```

**Add runtime helper**: `src/mlpy/stdlib/runtime_helpers.py`

```python
def _grant_capability(capability_type: str, from_import: str):
    """Grant capability to current context (called from generated code)."""
    from mlpy.runtime.capabilities.manager import get_capability_manager
    from mlpy.runtime.capabilities.tokens import create_capability_token
    from mlpy.runtime.capabilities.context import get_current_context, set_current_context

    context = get_current_context()
    if not context:
        manager = get_capability_manager()
        context = manager.create_context(name="main_execution")
        set_current_context(context)

    token = create_capability_token(
        capability_type=capability_type,
        description=f"Granted by import {from_import}",
        created_by="import_system"
    )
    context.add_capability(token)
```

**Deliverables**:
- ✅ 5 advanced modules built
- ✅ Capability granting integrated
- ✅ End-to-end flow working (import → grant → execute)
- ✅ All tests passing

---

## Phase 4: Builtin Module Implementation ✅ ENHANCED IMPLEMENTATION COMPLETE

**Duration**: 3-4 days (Completed ahead of schedule)
**Goal**: Implement comprehensive builtin module with Phase 1-3 integration
**Status**: ✅ Complete with 77/77 tests passing (100%)

### Enhanced Design Overview

Based on comprehensive Phase 4 design review, the builtin module has been implemented with:
- **Enhanced typeof()**: Integrates with @ml_class metadata from Phase 1-3
- **Introspection functions**: help(), methods(), modules() for developer experience
- **Expanded utilities**: 22 total builtin functions covering all essential operations
- **Complete decorator integration**: Uses @ml_module and @ml_function throughout
- **Production-ready testing**: 77 comprehensive unit tests with 97% coverage

### Tasks

#### 4.1 Implement Core Builtin Module ✅ COMPLETE

**File**: `src/mlpy/stdlib/builtin.py` (141 lines, 22 functions)

**Implemented Functions**:

**Type Conversion (4 functions)**:
- `int()` - Convert to integer with intelligent float string handling
- `float()` - Convert to float with boolean support
- `str()` - Convert to string with ML-compatible boolean formatting ("true"/"false")
- `bool()` - Convert to boolean with ML semantics

**Type Checking (2 functions)**:
- `typeof()` - Enhanced with @ml_class metadata recognition (Pattern, DateTimeObject, etc.)
- `isinstance()` - Check type with custom class support

**Collection Functions (3 functions)**:
- `len()` - Universal length for strings, arrays, objects
- `range()` - Generate number ranges with start/stop/step
- `enumerate()` - Create (index, value) pairs from arrays

**I/O Functions (2 functions)**:
- `print()` - Output with ML boolean formatting
- `input()` - Read console input with prompt

**Introspection Functions (3 functions)**:
- `help()` - Show documentation from @ml_function/@ml_module/@ml_class metadata
- `methods()` - List all available methods for a value type
- `modules()` - List all imported modules from _MODULE_REGISTRY

**Math Utilities (4 functions)**:
- `abs()` - Absolute value
- `min()` - Minimum value (supports array or multiple args)
- `max()` - Maximum value (supports array or multiple args)
- `round()` - Round to precision

**Additional Utilities (4 functions)**:
- `zip()` - Zip multiple arrays into tuples
- `sorted()` - Return sorted copy with optional reverse
- `keys()` - Get object keys as array
- `values()` - Get object values as array

#### 4.2 Enhanced typeof() Implementation ✅ COMPLETE

**Key Feature**: Integration with @ml_class metadata from Phase 1-3

```python
@ml_function(description="Get type of value with class metadata awareness")
def typeof(self, value: Any) -> str:
    # Check for @ml_class metadata (from Phase 1-3)
    if hasattr(type(value), '_ml_class_metadata'):
        return type(value)._ml_class_metadata.name  # Returns "Pattern", "DateTimeObject", etc.

    # Standard type detection
    if isinstance(value, bool): return "boolean"
    elif isinstance(value, (int, float)): return "number"
    elif isinstance(value, str): return "string"
    elif isinstance(value, list): return "array"
    elif isinstance(value, dict): return "object"
    elif callable(value): return "function"
    else: return "unknown"
```

**Achievement**: typeof() now recognizes Pattern and DateTimeObject classes from Phase 3!

#### 4.3 Introspection Functions ✅ COMPLETE

**Developer Experience Enhancement**:

```python
@ml_function(description="Get help for function or module")
def help(self, target: Any) -> str:
    # Check for @ml_function metadata
    if hasattr(target, '_ml_function_metadata'):
        return target._ml_function_metadata.description

    # Check for @ml_module metadata
    if hasattr(target, '_ml_module_metadata'):
        return target._ml_module_metadata.description

    # Check for @ml_class metadata
    if hasattr(type(target), '_ml_class_metadata'):
        return type(target)._ml_class_metadata.description

    # Fallback to docstring
    return target.__doc__ or "No help available"

@ml_function(description="List all methods available on value")
def methods(self, value: Any) -> list:
    return sorted([attr for attr in dir(value) if not attr.startswith('_')])

@ml_function(description="List all imported modules")
def modules(self) -> list:
    return sorted(list(_MODULE_REGISTRY.keys()))
```

**Achievement**: ML developers can now discover and learn about functions/modules/classes!

#### 4.4 Comprehensive Unit Testing ✅ COMPLETE

**Test file**: `tests/unit/stdlib/test_builtin.py` (77 tests, 100% passing)

**Test Coverage**:
- ✅ Module registration (3 tests)
- ✅ Type conversion functions (13 tests)
- ✅ Type checking functions (8 tests including @ml_class integration)
- ✅ Collection functions (9 tests)
- ✅ I/O functions (4 tests)
- ✅ Introspection functions (6 tests)
- ✅ Math utilities (10 tests)
- ✅ Additional utilities (9 tests)
- ✅ Helper functions (3 tests)
- ✅ ML compatibility (4 tests)
- ✅ Error recovery (8 tests)

**Test Success Rate**: 77/77 (100%)
**Code Coverage**: 97% for builtin.py

**Deliverables**:
- ✅ Complete builtin module implemented (141 lines, 22 functions)
- ✅ Enhanced typeof() with @ml_class metadata integration
- ✅ Introspection functions (help, methods, modules)
- ✅ Comprehensive unit tests (77 tests, 100% passing)
- ✅ Full decorator integration with Phase 1-3
- ✅ Production-ready implementation

---

## Phase 5: Testing & Validation

**Duration**: 1 week
**Goal**: Comprehensive testing, performance validation, security audit

### Tasks

#### 5.1 Run Full Test Suite

```bash
# Unit tests
pytest tests/unit/ -v --cov=src/mlpy --cov-report=html

# Integration tests
python tests/ml_test_runner.py --full --matrix

# Security tests
python test_comprehensive_security_audit.py

# Performance benchmarks
python tests/performance/test_current_performance.py
```

**Success criteria**:
- Unit test coverage: ≥95%
- Integration test success: ≥94.4%
- Security tests: 100% exploit prevention
- Performance: Within 5% of baseline

#### 5.2 Security Audit

**Checklist**:
- [ ] All getattr/setattr route through safe_attr_access
- [ ] All dangerous patterns blocked
- [ ] No new attack vectors introduced
- [ ] Capability checking functional
- [ ] Token validation working

**Run security tests**:
```bash
# Sandbox escape attempts
pytest tests/security/test_sandbox_escape.py

# Capability bypass attempts
pytest tests/security/test_capability_bypass.py

# SafeAttributeRegistry integration
pytest tests/security/test_safe_access_integration.py
```

#### 5.3 Performance Benchmarking

**Compare baseline**:
```bash
# Collect new metrics
python tests/performance/test_current_performance.py > phase5_performance.txt

# Compare
diff baseline_performance.txt phase5_performance.txt

# Analyze
python tools/analyze_performance.py baseline_performance.txt phase5_performance.txt
```

**Target metrics**:
- Import time: <0.6ms (5% increase)
- Function call overhead: ~0.012ms (capability check)
- Total transpilation: <10.5ms (5% increase)

#### 5.4 Integration Testing with Real ML Programs

**Test suite**:
```bash
# Run all 36+ ML integration tests
python tests/ml_test_runner.py --full

# Expected results:
# - Parse success: ≥97.3% (maintained)
# - Security analysis: 100% threat detection
# - Transpilation: ≥94.4% success
# - Execution: ≥77.8% success
```

**Deliverables**:
- ✅ Full test suite passing
- ✅ Security audit complete
- ✅ Performance within targets
- ✅ Integration tests validated

---

## Phase 6: Documentation & Cleanup

**Duration**: 1 week
**Goal**: Complete documentation, remove old system, final validation

### Tasks

#### 6.1 Remove Manual Registration

**File**: `src/mlpy/stdlib/registry.py`

**Delete**:
- `_register_core_modules()` method (668 lines)
- All manual registration code

**Keep**:
- `ModuleRegistry` class structure
- `register_module()` method (called by decorators)
- `get_module()` method
- `discover_stdlib()` method

**Before** (800+ lines):
```python
class ModuleRegistry:
    def _register_core_modules(self):
        # 668 lines of manual registration
        ...

    # Other methods
```

**After** (130 lines):
```python
class ModuleRegistry:
    @classmethod
    def discover_stdlib(cls):
        """Auto-discover modules via decorators."""
        ...

    @classmethod
    def register_module(cls, name, module_info):
        """Register module (called by @ml_module)."""
        ...

    @classmethod
    def get_module(cls, name):
        """Get registered module."""
        ...
```

**Reduction**: -670 lines

#### 6.2 Remove Deprecated Modules

**Delete**:
- `src/mlpy/stdlib/math_bridge.py` (replaced by math_decorated.py)
- `src/mlpy/stdlib/string_bridge.py`
- `src/mlpy/stdlib/datetime_bridge.py`
- All other `*_bridge.py` files

**Rename decorated versions**:
```bash
mv src/mlpy/stdlib/math_decorated.py src/mlpy/stdlib/math.py
mv src/mlpy/stdlib/string_decorated.py src/mlpy/stdlib/string.py
# ... etc
```

**Update imports across codebase**:
```bash
# Find all imports of old modules
grep -r "from mlpy.stdlib.*_bridge import" src/

# Replace with new imports
# (automated via script or manual)
```

#### 6.3 Update Documentation

**Create/Update**:

1. **API Documentation**:
   - `docs/api/stdlib/decorators.md` - Decorator API reference
   - `docs/api/stdlib/builtin.md` - Builtin module reference
   - Update each stdlib module documentation

2. **Developer Guide**:
   - `docs/developer-guide/adding-stdlib-module.md` - How to add new modules
   - `docs/developer-guide/capability-system.md` - Capability integration guide
   - Update architecture documentation

3. **User Guide**:
   - `docs/user-guide/builtin-functions.md` - Builtin function reference
   - `docs/user-guide/capabilities.md` - Capability system for users
   - Update tutorial examples

4. **Migration Guide**:
   - `docs/migration/module-system-2.0.md` - Migration guide for contributors

#### 6.4 Final Validation

**Run complete validation**:

```bash
# All tests
pytest tests/ -v

# Integration
python tests/ml_test_runner.py --full --matrix

# Security
python test_comprehensive_security_audit.py

# Performance
python tests/performance/test_transpiler_benchmarks.py

# Coverage
pytest --cov=src/mlpy --cov-report=html --cov-report=term-missing
```

**Success criteria**:
- All tests passing
- Coverage ≥95%
- Security 100%
- Performance within 5% of baseline
- Documentation complete

**Deliverables**:
- ✅ Manual registration deleted
- ✅ Old modules removed
- ✅ Documentation complete
- ✅ Final validation successful
- ✅ Ready for production

---

## Testing Strategy

### Test Categories

**1. Unit Tests** (Target: 100% coverage of new code)
- Decorator functionality
- Capability integration
- Safe access integration
- Builtin module functions

**2. Integration Tests** (Target: All scenarios covered)
- End-to-end import flow
- Capability granting and checking
- Module interaction
- ML program execution

**3. Security Tests** (Target: 100% exploit prevention)
- Sandbox escape attempts
- Capability bypass attempts
- SafeAttributeRegistry bypass attempts
- Builtin security validation

**4. Performance Tests** (Target: <5% regression)
- Import performance
- Function call overhead
- Transpilation speed
- Memory usage

### Test Coverage Requirements

**Per Phase**:
- Phase 1: Decorator system - 100% coverage
- Phase 2: Capability integration - 100% coverage
- Phase 3: Module migration - 95% coverage (existing modules)
- Phase 4: Builtin module - 100% coverage
- Phase 5: Integration - All scenarios
- Phase 6: Final - 95%+ overall

### Continuous Validation

**After each phase**:
```bash
# Quick validation
pytest tests/unit/ -v
python tests/ml_test_runner.py --quick

# Full validation (before phase completion)
pytest tests/ -v --cov=src/mlpy
python tests/ml_test_runner.py --full
python test_comprehensive_security_audit.py
```

---

## Rollback Plan

### Rollback Points

**After Phase 1**:
- Decorators exist but not used (stubs only)
- Can disable decorator system without impact
- Rollback: Delete `decorators.py`, remove test files

**After Phase 2**:
- Capability integration added but not required
- Old system still functional
- Rollback: Remove capability granting code from code generator

**After Phase 3**:
- Both old and new modules exist
- Can switch imports back to old modules
- Rollback: Revert imports to `*_bridge` modules

**After Phase 4**:
- Builtin module added but can be optional
- Rollback: Remove auto-import from code generator

**After Phase 5**:
- System fully tested but old code still present
- Rollback: Keep both systems, disable new system

**After Phase 6**:
- Old code removed, point of no return
- Rollback: Git revert to before Phase 6

### Emergency Rollback Procedure

```bash
# 1. Identify failing phase
git log --oneline --grep="Phase [1-6]"

# 2. Revert to last working commit
git revert <commit-hash>

# 3. Run tests
pytest tests/ -v

# 4. If still failing, revert to before phase
git reset --hard <phase-start-commit>

# 5. Validate
python tests/ml_test_runner.py --full
```

---

## Success Metrics

### Technical Metrics

**Performance**:
- ✅ Transpilation time: Within 5% of baseline
- ✅ Function call overhead: <0.015ms
- ✅ Memory usage: No significant increase

**Quality**:
- ✅ Test coverage: ≥95%
- ✅ Security tests: 100% passing
- ✅ Integration tests: ≥94.4% success

**Code Quality**:
- ✅ Lines of code: Net reduction of 700+ lines
- ✅ Complexity: Reduced (no manual registration)
- ✅ Maintainability: Greatly improved

### Developer Experience Metrics

**Before**:
- Adding module: 5 files, 200+ lines, 2-3 hours
- Finding module code: Multiple files
- Understanding system: High complexity

**After**:
- Adding module: 1 file, 50 lines, 30 minutes
- Finding module code: Single file with decorators
- Understanding system: Clear decorator pattern

**Improvement**: 75% time reduction, 85% code reduction

### Production Readiness Checklist

- [ ] All phases complete
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Performance validated
- [ ] Security audited
- [ ] Migration guide published
- [ ] Examples updated
- [ ] Changelog prepared
- [ ] Release notes written
- [ ] Version tagged

---

## Timeline Summary (Clean Slate Edition)

| Phase | Duration | Effort | Deliverable |
|-------|----------|--------|-------------|
| Phase 0: Clean Slate | 1 hour | 1 hour | Old stdlib removed, ml_core validated |
| Phase 1: Decorators | 1 week | 40 hours | Decorator system + registry |
| Phase 2: Core Modules | 1 week | 40 hours | 4 core modules (math, console, json, string) |
| Phase 3: Advanced Modules | 1 week | 40 hours | 5 advanced + capability integration |
| Phase 4: Builtin | 3-4 days | 30 hours | Builtin module complete |
| Phase 5: Testing | 3 days | 24 hours | Full validation |
| **Total** | **3-4 weeks** | **175 hours** | **Production-ready system** |

**Optimistic estimate**: 3 weeks (if all goes smoothly)
**Realistic estimate**: 3-4 weeks
**Pessimistic estimate**: 5 weeks (if issues found)

**Why so much faster than original plan?**
- ✅ No backward compatibility overhead
- ✅ No migration complexity (build from scratch)
- ✅ No dual system maintenance
- ✅ Clean slate = clean code = faster development
- ✅ ml_core tests provide instant validation

---

## Conclusion

This clean slate implementation plan provides:

✅ **Streamlined approach** - No backward compatibility overhead
✅ **Fast timeline** - 3-4 weeks vs 8+ weeks
✅ **Clear validation** - ml_core tests as safety net
✅ **Better architecture** - Built right from day one
✅ **Capability-ready** - Integration from the start

**Next Steps**:
1. ✅ Execute Phase 0 (30 min - 1 hour)
   - Remove auto-imports from python_generator.py
   - Validate ml_core tests pass
   - Clean stdlib directory
2. Begin Phase 1 decorator implementation
3. Build modules one by one with tests

**Risk Assessment**: VERY LOW
- ml_core tests validate language features work
- No existing ML code to break
- Building from scratch = no technical debt
- Clear, simple validation at each step

**Confidence Level**: VERY HIGH
- Capability system already exists
- Decorator pattern is well-understood
- ml_core provides instant validation
- 3-4 week timeline is realistic and achievable

**Ready to Begin**: YES
- Phase 0 can be executed immediately
- All prerequisites in place
- Team has freedom to build it right
