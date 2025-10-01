# ML Module System 2.0: Implementation Plan

**Version**: 2.0.0-FINAL
**Date**: 2025-10-02
**Status**: COMPREHENSIVE PHASED IMPLEMENTATION GUIDE
**Est. Duration**: 6-8 weeks (conservative estimate)

---

## Table of Contents

1. [Implementation Philosophy](#implementation-philosophy)
2. [Phase 0: Preparation & Setup](#phase-0-preparation--setup)
3. [Phase 1: Decorator System Foundation](#phase-1-decorator-system-foundation)
4. [Phase 2: Capability Integration](#phase-2-capability-integration)
5. [Phase 3: Stdlib Module Migration](#phase-3-stdlib-module-migration)
6. [Phase 4: Builtin Module Implementation](#phase-4-builtin-module-implementation)
7. [Phase 5: Testing & Validation](#phase-5-testing--validation)
8. [Phase 6: Documentation & Cleanup](#phase-6-documentation--cleanup)
9. [Testing Strategy](#testing-strategy)
10. [Rollback Plan](#rollback-plan)
11. [Success Metrics](#success-metrics)

---

## Implementation Philosophy

### Core Principles

**1. Zero Breaking Changes**
- Every phase must maintain backward compatibility
- Existing tests continue passing
- Safe_access system untouched
- Capability system core untouched

**2. Incremental Delivery**
- Each phase delivers working, testable functionality
- Can pause after any phase without breaking system
- Early phases provide value independently

**3. Test-Driven Development**
- Write tests before implementation
- 95%+ coverage requirement maintained
- Security tests expanded, not reduced

**4. Gradual Migration**
- Decorators added alongside existing registration
- Manual registration removed only after migration complete
- Both systems coexist during transition

**5. Documentation-First**
- API documentation written before implementation
- Examples created during development
- Migration guides prepared in advance

### Risk Mitigation

**Technical Risks**:
- SafeAttributeRegistry integration errors → Mitigate with extensive security tests
- Capability system bugs → Comprehensive unit tests for each integration point
- Performance regression → Benchmark before/after each phase

**Schedule Risks**:
- Unexpected complexity → Buffer time in each phase
- Testing reveals issues → Dedicated bug-fix time allocated
- Resource unavailability → Clear phase boundaries allow pause

---

## Phase 0: Preparation & Setup

**Duration**: 1 week
**Goal**: Establish foundation, create test infrastructure

### Tasks

#### 0.1 Create Test Infrastructure

**New test files**:
```
tests/unit/stdlib/test_decorators.py        # Decorator unit tests
tests/integration/test_capability_flow.py   # End-to-end capability testing
tests/integration/test_safe_access_integration.py  # Safe access integration
tests/security/test_decorator_security.py   # Security validation
```

**Test categories**:
- Decorator functionality tests
- Capability granting tests
- Safe access integration tests
- Performance benchmarks

#### 0.2 Establish Baseline Metrics

**Collect baseline data**:
```bash
# Performance baseline
python tests/performance/test_current_performance.py > baseline_performance.txt

# Test coverage baseline
pytest --cov=src/mlpy --cov-report=html
cp -r htmlcov baseline_coverage/

# Security test results
python test_comprehensive_security_audit.py > baseline_security.txt

# Integration test results
python tests/ml_test_runner.py --full > baseline_integration.txt
```

**Establish targets**:
- Performance: Within 5% of baseline
- Coverage: Maintain 95%+ for core modules
- Security: 100% exploit prevention maintained
- Integration: 94.4% success rate maintained or improved

#### 0.3 Create Decorator Stub File

**Create**: `src/mlpy/stdlib/decorators.py`

```python
"""
ML stdlib decorator system (Phase 1 implementation).

Provides decorators for automatic module registration and capability enforcement.
"""

from functools import wraps
from typing import Callable, Any

# Stubs for Phase 0 (implemented in Phase 1)

def ml_module(name: str, capabilities=None, description=None, version="1.0.0", auto_import=False):
    """Decorator for ML stdlib modules (stub)."""
    def decorator(cls):
        # Phase 0: Just pass through, no functionality yet
        return cls
    return decorator

def ml_function(func=None, *, name=None, capabilities=None, params=None,
                returns=None, description=None, examples=None):
    """Decorator for ML-callable functions (stub)."""
    def decorator(fn):
        # Phase 0: Just pass through
        return fn

    if func is None:
        return decorator
    else:
        return decorator(func)

def ml_class(name=None, safe_expose=False, capabilities=None):
    """Decorator for safe class exposure (stub)."""
    def decorator(cls):
        # Phase 0: Just pass through
        return cls
    return decorator
```

#### 0.4 Document Current Architecture

**Create documentation**:
- Document current module registration flow
- Document safe_access integration points
- Document capability system API
- Create migration checklist

**Deliverables**:
- ✅ Test infrastructure ready
- ✅ Baseline metrics collected
- ✅ Decorator stubs created
- ✅ Architecture documented

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

## Phase 3: Stdlib Module Migration

**Duration**: 2 weeks
**Goal**: Migrate all stdlib modules to decorator system

### Migration Strategy

**Incremental approach**:
1. Create decorated version alongside existing
2. Test decorated version thoroughly
3. Update imports to use decorated version
4. Mark old version as deprecated
5. Remove old version after validation

### Tasks

#### 3.1 Create Migration Script

**Script**: `tools/migrate_module_to_decorators.py`

```python
"""
Helper script to migrate stdlib module to decorator system.

Usage: python tools/migrate_module_to_decorators.py math
"""

import sys
import os

TEMPLATE = '''"""
{module_name} module using decorator system.

Migrated from {module_name}_bridge.py
"""

from mlpy.stdlib.decorators import ml_module, ml_function
# Add necessary imports here

@ml_module(
    name="{module_name}",
    capabilities=[],  # TODO: Add capabilities
    description="",  # TODO: Add description
    version="2.0.0"
)
class {class_name}:
    """TODO: Add docstring."""

    def __init__(self):
        pass  # TODO: Initialize

    @ml_function(
        params={{}},  # TODO: Add parameters
        returns=None,  # TODO: Add return type
        description=""  # TODO: Add description
    )
    def example_function(self):
        """TODO: Implement function."""
        pass

# Create singleton instance
{module_name} = {class_name}()
'''

def migrate_module(module_name):
    class_name = module_name.capitalize()
    output = TEMPLATE.format(module_name=module_name, class_name=class_name)

    output_path = f"src/mlpy/stdlib/{module_name}_decorated.py"
    with open(output_path, 'w') as f:
        f.write(output)

    print(f"Created: {output_path}")
    print(f"Next steps:")
    print(f"1. Review and complete {output_path}")
    print(f"2. Add unit tests in tests/unit/stdlib/test_{module_name}_decorated.py")
    print(f"3. Test thoroughly")
    print(f"4. Update imports")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python migrate_module_to_decorators.py <module_name>")
        sys.exit(1)

    module_name = sys.argv[1]
    migrate_module(module_name)
```

#### 3.2 Migrate Modules (Order of Priority)

**Priority 1: Core Modules** (Week 1)

1. **math** - Already done as proof-of-concept
2. **string** - Complex, many methods
3. **datetime** - Custom classes, good test of @ml_class
4. **json** - Simple, good early win

**Priority 2: Utility Modules** (Week 2)

5. **regex** - Custom classes (Regex, Pattern)
6. **collections** - Object manipulation
7. **functional** - Higher-order functions
8. **random** - Simple module

**For each module**:

```bash
# 1. Create decorated version
python tools/migrate_module_to_decorators.py <module>

# 2. Implement fully (copy logic from _bridge version)

# 3. Create comprehensive tests
# tests/unit/stdlib/test_<module>_decorated.py

# 4. Run tests
pytest tests/unit/stdlib/test_<module>_decorated.py -v

# 5. Integration test
python tests/ml_test_runner.py --module <module>

# 6. Mark old version as deprecated
# Add deprecation warning to _bridge.py
```

#### 3.3 Example Migration: string Module

**Before** (`string_bridge.py`, 400+ lines):
```python
class String:
    """String manipulation functions."""

    def upper(self, text: str) -> str:
        """Convert to uppercase."""
        return text.upper()

    # ... 20+ methods ...

# Manual registration in registry.py (60+ lines)
```

**After** (`string_decorated.py`, 250 lines):
```python
@ml_module(
    name="string",
    capabilities=[],
    description="String manipulation and formatting",
    version="2.0.0"
)
class String:
    """String manipulation functions with decorator system."""

    @ml_function(
        params={"text": str},
        returns=str,
        description="Convert string to uppercase",
        examples=["string.upper('hello') // 'HELLO'"]
    )
    def upper(self, text: str) -> str:
        """Convert to uppercase."""
        return text.upper()

    # ... remaining methods with @ml_function ...

# Manual registration: DELETED (0 lines)
```

**Testing checklist per module**:
- [ ] All methods decorated with @ml_function
- [ ] Metadata populated (params, returns, description)
- [ ] Unit tests pass (100% coverage)
- [ ] Integration tests pass (ML code using module)
- [ ] Performance within 5% of baseline
- [ ] Documentation accessible via info()

**Deliverables**:
- ✅ All 8 stdlib modules migrated to decorators
- ✅ All unit tests passing
- ✅ All integration tests passing
- ✅ Performance maintained
- ✅ Old versions marked deprecated

---

## Phase 4: Builtin Module Implementation

**Duration**: 1 week
**Goal**: Implement complete builtin module with safe dynamic access

### Tasks

#### 4.1 Implement Core Builtin Module

**File**: `src/mlpy/stdlib/builtin.py`

(Use the comprehensive implementation from builtin.py proposal)

**Key components**:
- Type conversion functions (int, float, str, bool)
- Type checking functions (type, typeof, isinstance) with SafeAttributeRegistry awareness
- SECURE dynamic access (getattr, setattr, hasattr) routing through safe_attr_access
- Introspection functions (dir, info)
- Container functions (len)
- I/O functions (print, input)
- System functions (exit, version)

#### 4.2 Implement Safe Class Wrappers

**In builtin.py**:

```python
@ml_class(name="string", safe_expose=True)
class SafeStringClass:
    # Complete implementation from proposal
    ...

@ml_class(name="list", safe_expose=True)
class SafeListClass:
    ...

@ml_class(name="dict", safe_expose=True)
class SafeDictClass:
    ...

@ml_class(name="float", safe_expose=True)
class SafeFloatClass:
    ...
```

#### 4.3 Integrate Auto-Import

**Modify python_generator.py**:

```python
def _generate_header(self) -> str:
    """Generate Python file header with imports."""
    header_lines = []

    # Auto-import builtin module
    header_lines.append("# Auto-imported builtin functions")
    header_lines.append("from mlpy.stdlib.builtin import (")
    header_lines.append("    int, float, str, bool,")
    header_lines.append("    type, typeof, isinstance,")
    header_lines.append("    dir, info, hasattr, getattr, setattr, call,")
    header_lines.append("    len, print, input, exit, version,")
    header_lines.append("    string, list, dict, builtin")
    header_lines.append(")")
    header_lines.append("")

    # ... rest of header ...
```

#### 4.4 Security Testing

**Test file**: `tests/security/test_builtin_security.py`

```python
def test_getattr_blocks_dangerous_attributes():
    """Verify getattr blocks __class__, __globals__, etc."""
    from mlpy.stdlib.builtin import builtin

    test_str = "hello"

    # Safe attribute - should work
    result = builtin.getattr(test_str, "upper")
    assert callable(result)

    # Dangerous attribute - should return default
    result = builtin.getattr(test_str, "__class__", "BLOCKED")
    assert result == "BLOCKED"

    result = builtin.getattr(test_str, "__globals__", "BLOCKED")
    assert result == "BLOCKED"

def test_setattr_blocks_dangerous_modifications():
    """Verify setattr blocks modification of unsafe attributes."""
    from mlpy.stdlib.builtin import builtin

    obj = type('TestObj', (), {})()

    # ML object - should work
    ml_obj = {"name": "John"}
    builtin.setattr(ml_obj, "age", 30)
    assert ml_obj["age"] == 30

    # Unsafe Python object modification - should fail
    with pytest.raises(SecurityError):
        builtin.setattr(obj, "__class__", "evil")

def test_type_enhanced_with_safe_types():
    """Verify type() returns rich information for safe types."""
    from mlpy.stdlib.builtin import builtin

    # Basic types
    assert builtin.type(42) == "number"
    assert builtin.type("hello") == "string"
    assert builtin.type([1,2,3]) == "array"
    assert builtin.type({"a": 1}) == "object"

    # Registered safe type (after SafeStringClass registered)
    from mlpy.stdlib.builtin import SafeStringClass
    string_wrapper = SafeStringClass()
    # type() should recognize as registered safe type
```

**Deliverables**:
- ✅ Complete builtin module implemented
- ✅ Safe class wrappers functional
- ✅ Auto-import working
- ✅ Security tests passing (100% exploit prevention)
- ✅ Integration with SafeAttributeRegistry verified

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

## Timeline Summary

| Phase | Duration | Effort | Deliverable |
|-------|----------|--------|-------------|
| Phase 0: Preparation | 1 week | 40 hours | Test infrastructure, baselines |
| Phase 1: Decorators | 1.5 weeks | 60 hours | Decorator system working |
| Phase 2: Capabilities | 1 week | 40 hours | Capability integration |
| Phase 3: Migration | 2 weeks | 80 hours | All modules migrated |
| Phase 4: Builtin | 1 week | 40 hours | Builtin module complete |
| Phase 5: Testing | 1 week | 40 hours | Full validation |
| Phase 6: Cleanup | 1 week | 40 hours | Documentation, cleanup |
| **Total** | **8.5 weeks** | **340 hours** | **Production-ready system** |

**Conservative estimate**: 8.5 weeks
**Optimistic estimate**: 6 weeks (if all goes smoothly)
**Pessimistic estimate**: 11 weeks (if issues found)

---

## Conclusion

This implementation plan provides:

✅ **Clear phases** with defined deliverables
✅ **Comprehensive testing** at each stage
✅ **Rollback points** for safety
✅ **Success metrics** for validation
✅ **Conservative timeline** with buffer

**Next Steps**:
1. Review and approve this plan
2. Allocate resources (1-2 developers)
3. Set up Phase 0 test infrastructure
4. Begin Phase 1 implementation

**Risk Assessment**: LOW
- Building on existing, working systems
- Incremental approach with validation
- Clear rollback strategy
- Conservative timeline

**Confidence Level**: HIGH
- Infrastructure 80% complete
- Clear implementation path
- Comprehensive testing strategy
- Well-defined success criteria
