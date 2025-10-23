# Codegen API Usage Documentation
**Date:** October 23, 2025
**Purpose:** Document all usages of the codegen module API to ensure backward compatibility

## Public API Exports

### Module: `mlpy.ml.codegen`

**Exported Symbols (`__init__.py`):**
```python
from .python_generator import PythonCodeGenerator, generate_python_code
__all__ = ["PythonCodeGenerator", "generate_python_code"]
```

## External Consumers

### 1. `src/mlpy/ml/transpiler.py`

**Import Pattern:**
```python
from mlpy.ml.codegen.python_generator import generate_python_code
```

**Usage:**
```python
# Line ~89
python_code, source_map = generate_python_code(
    optimized_ast,
    source_file=ml_file,
    generate_source_maps=True,
    import_paths=import_paths,
    allow_current_dir=allow_current_dir,
    module_output_mode=module_output_mode,
    repl_mode=False
)
```

**API Contract:**
- Function: `generate_python_code()`
- Parameters: `ast, source_file, generate_source_maps, import_paths, allow_current_dir, module_output_mode, repl_mode`
- Returns: `tuple[str, dict[str, Any] | None]` (Python code, source map)

### 2. `src/mlpy/debugging/safe_expression_eval.py`

**Import Pattern:**
```python
from mlpy.ml.codegen.python_generator import PythonCodeGenerator
```

**Usage:**
```python
# Line ~35
generator = PythonCodeGenerator(
    source_file=None,
    generate_source_maps=False,
    repl_mode=True
)
python_code, _ = generator.generate(expression_ast)
```

**API Contract:**
- Class: `PythonCodeGenerator`
- Constructor Parameters: `source_file, generate_source_maps, import_paths, allow_current_dir, module_output_mode, repl_mode`
- Method: `generate(ast: Program) -> tuple[str, dict]`

### 3. Test Suite

**Import Patterns:**
```python
# From test_python_generator.py
from mlpy.ml.codegen.python_generator import (
    PythonCodeGenerator,
    generate_python_code,
    SourceMapping,
    CodeGenerationContext,
)

# From test_allowed_functions_registry.py
from mlpy.ml.codegen.allowed_functions_registry import AllowedFunctionsRegistry

# From test_safe_attribute_registry.py
from mlpy.ml.codegen.safe_attribute_registry import (
    AttributeAccessType,
    SafeAttribute,
    SafeAttributeRegistry,
    get_safe_registry,
)

# From test_enhanced_source_maps.py
from mlpy.ml.codegen.enhanced_source_maps import (
    EnhancedSourceMapGenerator,
    EnhancedSourceMap,
)
```

**Total Test Files:** 4
**Total Tests:** 238

## API Compatibility Requirements

### Must Preserve

1. **Module-level function:**
   ```python
   generate_python_code(ast, source_file=None, generate_source_maps=True,
                       import_paths=None, allow_current_dir=True,
                       module_output_mode='separate', repl_mode=False)
   ```

2. **PythonCodeGenerator class:**
   ```python
   class PythonCodeGenerator:
       def __init__(self, source_file=None, generate_source_maps=True,
                   import_paths=None, allow_current_dir=False,
                   module_output_mode='separate', repl_mode=False)
       def generate(self, ast: Program) -> tuple[str, dict]
   ```

3. **Supporting classes:**
   - `SourceMapping` (dataclass)
   - `CodeGenerationContext` (dataclass)

4. **All visitor methods** (for subclassing/extension):
   - `visit_*` methods must remain available
   - Method signatures must not change

## Import Compatibility Matrix

| Import Pattern | Status | Must Work |
|----------------|--------|-----------|
| `from mlpy.ml.codegen import PythonCodeGenerator` | ✅ Yes | ✅ Required |
| `from mlpy.ml.codegen import generate_python_code` | ✅ Yes | ✅ Required |
| `from mlpy.ml.codegen.python_generator import PythonCodeGenerator` | ✅ Yes | ✅ Required |
| `from mlpy.ml.codegen.python_generator import generate_python_code` | ✅ Yes | ✅ Required |
| `from mlpy.ml.codegen.python_generator import SourceMapping` | ✅ Yes | ⚠️ Test only |
| `from mlpy.ml.codegen.python_generator import CodeGenerationContext` | ✅ Yes | ⚠️ Test only |

## Refactoring Strategy for API Preservation

### Approach: Facade Pattern with Mixins

**Old Import (must still work):**
```python
from mlpy.ml.codegen.python_generator import PythonCodeGenerator
```

**New Implementation:**
```python
# python_generator.py (new - facade)
from .core.generator_base import GeneratorBase
from .visitors.statement_visitor import StatementVisitorMixin
from .visitors.expression_visitor import ExpressionVisitorMixin
# ... other mixins

class PythonCodeGenerator(
    GeneratorBase,
    StatementVisitorMixin,
    ExpressionVisitorMixin,
    # ... all mixins
):
    """Facade class composing all code generation capabilities."""
    pass

def generate_python_code(ast, ...):
    """Module-level API function."""
    generator = PythonCodeGenerator(...)
    return generator.generate(ast)

# Re-export supporting classes for backward compatibility
from .core.context import SourceMapping, CodeGenerationContext
__all__ = ['PythonCodeGenerator', 'generate_python_code', 'SourceMapping', 'CodeGenerationContext']
```

**Result:** All existing imports continue to work without modification.

## Verification Tests

After refactoring, run:

```bash
# Test external usage from transpiler
pytest tests/unit/transpiler/ -v

# Test external usage from debugger
pytest tests/unit/debugging/ -v -k expression

# Test all codegen tests
pytest tests/unit/codegen/ -v

# Test integration
python tests/ml_test_runner.py --full
```

All tests must pass with 100% success rate.
