# Codegen Refactoring - Baseline Metrics
**Date:** October 23, 2025
**Pre-Refactoring State**

## Test Results

### Unit Tests
- **Total Tests:** 238
- **Passed:** 238 (100%)
- **Failed:** 0
- **Execution Time:** 0.79s

**Test Files:**
- test_allowed_functions_registry.py: 38 tests
- test_enhanced_source_maps.py: 28 tests
- test_python_generator.py: 135 tests
- test_safe_attribute_registry.py: 37 tests

### Integration Tests
- **Total ML Programs:** 69
- **Passed:** 69 (100%)
- **Failed:** 0
- **Average Time:** 610.2ms per file
- **Total Lines:** 12,777 lines of ML code

**All Stages:** 100% success rate
- Parse: 69/69
- AST: 69/69
- Transform: 69/69
- Typecheck: 69/69
- Security_deep: 69/69
- Optimize: 69/69
- Security: 69/69
- Codegen: 69/69
- Execution: 69/69

## File Structure (Before Refactoring)

```
src/mlpy/ml/codegen/
├── __init__.py                      (5 lines)
├── python_generator.py              (2,259 lines) ⚠️ TARGET FOR REFACTORING
├── allowed_functions_registry.py    (282 lines)
├── safe_attribute_registry.py       (661 lines)
└── enhanced_source_maps.py          (303 lines)

Total: 3,510 lines
```

## Public API Surface

**Exported from `__init__.py`:**
```python
from .python_generator import PythonCodeGenerator, generate_python_code
__all__ = ["PythonCodeGenerator", "generate_python_code"]
```

**External Consumers:**
1. `src/mlpy/ml/transpiler.py` - Uses `generate_python_code()` function
2. `src/mlpy/debugging/safe_expression_eval.py` - Uses `PythonCodeGenerator` class
3. Test suite - 238 tests importing from codegen module

## Current Performance
- Unit test execution: 0.79s
- Integration test execution: 42.1s total (610ms average per file)
- No performance regressions expected from refactoring

## Success Criteria for Refactoring

After refactoring, these metrics must be maintained or improved:

- ✅ Unit tests: 238/238 passing (100%)
- ✅ Integration tests: 69/69 passing (100%)
- ✅ Performance: <1s unit tests, ~610ms integration average
- ✅ API compatibility: 100% backward compatible
- ✅ File size: Max file <500 lines (from 2,259)

## Rollback Information

**Tag:** `baseline-before-codegen-refactor`
**Commit:** 1d8f609
**Branch:** documentation-rewrite

**Rollback Command:**
```bash
git reset --hard baseline-before-codegen-refactor
```
