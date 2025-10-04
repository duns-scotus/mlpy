# Pre-Phase 0: Unit Test Fixes

**Purpose**: Fix unit tests that depend on old stdlib before clean slate module rewrite
**Duration**: 30 minutes
**Status**: Required before Phase 0 execution

---

## Problem Statement

Several unit tests have **mixed concerns** - they test language features (parsing, code generation) but use ML `import` statements that depend on the old stdlib modules we're about to delete.

**Critical Discovery**:
- ml_core integration tests: ✅ SAFE (no stdlib imports)
- Some unit tests: ❌ WILL BREAK (depend on old stdlib)

---

## Tests That Will Break

### 1. `tests/unit/codegen/test_python_generator.py::test_stdlib_imports_in_header`

**Lines**: 402-409

**Current code**:
```python
def test_stdlib_imports_in_header(self, generator):
    """Test ML stdlib imports in header."""
    program = Program([])

    code, _ = generator.generate(program)

    # Should import console
    assert "console" in code  # ← FAILS when auto-imports removed
```

**Why it breaks**: Expects auto-imports in generated code (lines 120-121 of python_generator.py)

**Fix**: Delete this test method entirely

**Rationale**:
- Tests ad-hoc auto-import behavior we're removing
- New design = explicit imports only
- No auto-imports = nothing to test

### 2. `tests/unit/test_regex_module.py` (ENTIRE FILE)

**Lines**: 1-260 (entire file)

**Current approach**: Tests regex module VIA ML import
```python
helper = REPLTestHelper(security_enabled=False)
helper.execute_ml("import regex")  # ← FAILS when regex_bridge.py removed
helper.execute_ml('result = regex.test("hello", "world")')
assert repl.get_variable("result") is True
```

**Why it breaks**: Uses `import regex` which requires regex_bridge.py

**Fix Option A - Skip during transition** (Quick - 2 minutes):
```python
import pytest

@pytest.mark.skip(reason="Regex module being rewritten in Phase 3 - will be restored with new implementation")
class TestRegexImport:
    """Test regex module import behavior."""
    # ... all test methods ...

@pytest.mark.skip(reason="Regex module being rewritten in Phase 3")
class TestRegexStaticMethods:
    # ... all test methods ...

@pytest.mark.skip(reason="Regex module being rewritten in Phase 3")
class TestRegexPatternClass:
    # ... all test methods ...

@pytest.mark.skip(reason="Regex module being rewritten in Phase 3")
class TestRegexErrorHandling:
    # ... all test methods ...

@pytest.mark.skip(reason="Regex module being rewritten in Phase 3")
class TestRegexConvenienceMethods:
    # ... all test methods ...

@pytest.mark.skip(reason="Regex module being rewritten in Phase 3")
class TestRegexSafeAttributeAccess:
    # ... all test methods ...
```

**Fix Option B - Rewrite to test directly** (Better - 20 minutes):
```python
import pytest
from mlpy.stdlib.regex_bridge import Regex  # Direct import

class TestRegexDirectAPI:
    """Test Regex class API directly (no ML import)."""

    @pytest.fixture
    def regex(self):
        """Provide Regex instance."""
        return Regex()

    def test_regex_test_matches(self, regex):
        """Test regex.test() returns true for matching pattern."""
        result = regex.test("hello", "hello world")
        assert result is True

    def test_regex_test_no_match(self, regex):
        """Test regex.test() returns false for non-matching pattern."""
        result = regex.test("goodbye", "hello world")
        assert result is False

    def test_regex_findall_multiple_matches(self, regex):
        """Test regex.findAll() returns all matches."""
        result = regex.findAll("[0-9]+", "I have 5 apples and 3 oranges")
        assert result == ["5", "3"]

    # ... rewrite remaining tests to call methods directly ...
```

**Recommendation**: Use **Option A (skip)** for now - restore tests in Phase 3 with new regex module

---

## Tests That Are SAFE (No Changes Needed)

### ✅ Parser Tests
- `tests/unit/test_parser.py::test_import_statement`
- Only parses `import math.functions`, doesn't need actual module
- **Status**: SAFE

### ✅ Code Generation Tests
- `tests/unit/test_python_generator.py::test_import_statements`
- Only checks `"import math" in python_code`, doesn't execute
- **Status**: SAFE

### ✅ Security Tests
- `tests/unit/test_security_analyzer.py::test_unsafe_imports`
- `tests/unit/test_repl_errors.py::test_dangerous_import_*`
- `tests/unit/analysis/test_ast_analyzer.py::test_detect_dangerous_import`
- Test blocking dangerous imports (`import os`, `import subprocess`)
- Don't need stdlib modules to work
- **Status**: SAFE

### ✅ Integration Tests (ml_core)
- `tests/ml_integration/ml_core/*.ml` (all 25 files)
- Test pure language features, no stdlib imports
- **Status**: SAFE (our validation checkpoint)

---

## Implementation Checklist

### Step 1: Fix test_python_generator.py
- [ ] Open `tests/unit/codegen/test_python_generator.py`
- [ ] Navigate to line 402
- [ ] **Delete** `test_stdlib_imports_in_header` method (lines 402-409)
- [ ] Save file

### Step 2: Fix test_regex_module.py (Option A - Quick)
- [ ] Open `tests/unit/test_regex_module.py`
- [ ] Add `@pytest.mark.skip(reason="...")` to all 6 test classes:
  - `TestRegexImport` (line 16)
  - `TestRegexStaticMethods` (line 34)
  - `TestRegexPatternClass` (line 115)
  - `TestRegexErrorHandling` (line 168)
  - `TestRegexConvenienceMethods` (line 198)
  - `TestRegexSafeAttributeAccess` (line 247)
- [ ] Save file

### Step 3: Validate Changes
- [ ] Run affected unit tests:
  ```bash
  pytest tests/unit/codegen/test_python_generator.py -v
  pytest tests/unit/test_regex_module.py -v
  ```
- [ ] Expected results:
  - `test_python_generator.py`: All tests pass (1 test deleted)
  - `test_regex_module.py`: All tests skipped (6 classes marked)

### Step 4: Run Full Unit Test Suite
- [ ] Run all unit tests to verify nothing else breaks:
  ```bash
  pytest tests/unit/ -v
  ```
- [ ] Expected: All tests pass or skip (none fail)

### Step 5: Validate ml_core Still Works
- [ ] Run integration tests:
  ```bash
  python tests/ml_test_runner.py --full --category ml_core
  ```
- [ ] Expected: **25/25 tests PASS** (100% success)

---

## Exact File Changes

### File 1: `tests/unit/codegen/test_python_generator.py`

**DELETE lines 402-409**:
```python
    def test_stdlib_imports_in_header(self, generator):
        """Test ML stdlib imports in header."""
        program = Program([])

        code, _ = generator.generate(program)

        # Should import console
        assert "console" in code
```

### File 2: `tests/unit/test_regex_module.py`

**ADD at the top of each test class**:

```python
# After line 16 (before class TestRegexImport):
@pytest.mark.skip(reason="Regex module being rewritten in Phase 3 - will be restored with new implementation")
class TestRegexImport:
    ...

# After line 34 (before class TestRegexStaticMethods):
@pytest.mark.skip(reason="Regex module being rewritten in Phase 3")
class TestRegexStaticMethods:
    ...

# After line 115 (before class TestRegexPatternClass):
@pytest.mark.skip(reason="Regex module being rewritten in Phase 3")
class TestRegexPatternClass:
    ...

# After line 168 (before class TestRegexErrorHandling):
@pytest.mark.skip(reason="Regex module being rewritten in Phase 3")
class TestRegexErrorHandling:
    ...

# After line 198 (before class TestRegexConvenienceMethods):
@pytest.mark.skip(reason="Regex module being rewritten in Phase 3")
class TestRegexConvenienceMethods:
    ...

# After line 247 (before class TestRegexSafeAttributeAccess):
@pytest.mark.skip(reason="Regex module being rewritten in Phase 3")
class TestRegexSafeAttributeAccess:
    ...
```

---

## Validation Commands

```bash
# 1. Verify fixed tests
pytest tests/unit/codegen/test_python_generator.py::TestPythonCodeGenerator -v
pytest tests/unit/test_regex_module.py -v

# 2. Run full unit test suite
pytest tests/unit/ -v --tb=short

# 3. Validate ml_core integration tests (CRITICAL)
python tests/ml_test_runner.py --full --category ml_core

# 4. Check overall test count
pytest tests/unit/ --collect-only | grep "test session starts"
```

**Success Criteria**:
- ✅ No unit test failures
- ✅ Regex tests show as "SKIPPED" (not failed)
- ✅ ml_core: 25/25 PASS
- ✅ Ready for Phase 0

---

## Why This Matters

**Without these fixes**:
- Phase 0 Step 1 (remove auto-imports) → `test_stdlib_imports_in_header` FAILS
- Phase 0 Step 4 (delete old modules) → `test_regex_module.py` FAILS
- False failures block progress

**With these fixes**:
- ✅ Unit tests aligned with new design
- ✅ No false failures during module rewrite
- ✅ Clear path to Phase 0 execution
- ✅ Tests will be restored/rewritten in Phase 3 with new modules

---

## Timeline

| Task | Duration | Cumulative |
|------|----------|------------|
| Delete test_stdlib_imports_in_header | 2 min | 2 min |
| Add @pytest.mark.skip to test_regex_module.py | 5 min | 7 min |
| Run validation tests | 3 min | 10 min |
| Run full unit suite | 5 min | 15 min |
| Validate ml_core tests | 2 min | 17 min |
| **Total** | **17 min** | **17 min** |

**Buffer for issues**: +13 min → **30 min total**

---

## Post-Completion Status

After completing this preparatory work:

✅ **Unit tests aligned** with clean slate approach
✅ **No false failures** from old stdlib dependencies
✅ **ml_core validated** as our safety net
✅ **Ready for Phase 0** - can remove auto-imports and delete old stdlib

**Next Step**: Execute Phase 0 (Clean the Slate) from implementation plan
