# Test Coverage Improvement Proposal
**Date:** October 29, 2025
**Current Coverage:** 35% (6,127 / 17,628 lines)
**Target Coverage:** 75% (realistic) / 85% (aspirational)
**Status:** Active Proposal

---

## Executive Summary

This proposal consolidates previous coverage improvement plans and provides a pragmatic, data-driven approach to improving mlpy's test coverage from 35% to 75%+. Based on actual coverage data from October 29, 2025, we've identified high-impact areas and created a phased improvement plan.

### Key Principles
1. **Fix failing tests first** - 15 tests currently failing, blocking accurate coverage measurement
2. **High-impact, low-effort wins** - Target 0% coverage files that are small and testable
3. **User-facing priorities** - CLI, REPL, and stdlib have direct user impact
4. **Security-critical components** - Capabilities and sandbox systems must be thoroughly tested
5. **Pragmatic targets** - 75% is excellent, 85% is aspirational, 95% may not be realistic

---

## Current State Analysis

### Test Suite Status
- **Total Lines:** 17,628 statements
- **Covered Lines:** 6,127 statements (35%)
- **Missing Lines:** 11,501 statements (65%)
- **Failing Tests:** 15 tests failing
- **Test Files:** 100+ unit and integration tests

### Coverage by Category

| Category | Files | Avg Coverage | Status | Priority |
|----------|-------|--------------|--------|----------|
| **CLI & REPL** | 6 | 7-25% | 🔴 Critical Gap | HIGH |
| **Standard Library** | 17 | 34-82% | 🟡 Partial | HIGH |
| **Analysis** | 11 | 13-81% | 🟡 Mixed | MEDIUM |
| **Code Generation** | 15 | 6-84% | 🟡 Mixed | MEDIUM |
| **Runtime/Capabilities** | 11 | 0-63% | 🔴 Critical Gap | HIGH |
| **Debugging** | 7 | 0-77% | 🟡 Partial | MEDIUM |
| **LSP Server** | 5 | 15-41% | 🟡 Partial | MEDIUM |
| **Integration** | 5 | 17-59% | 🟡 Partial | LOW |

### Critical 0% Coverage Files (High Priority)
1. `src/mlpy/__main__.py` - Entry point (3 lines)
2. `src/mlpy/ml/grammar/advanced_ast_nodes.py` - Advanced features (350 lines)
3. `src/mlpy/debugging/repl.py` - Debug REPL (350 lines)
4. `src/mlpy/integration/repl_commands.py` - REPL commands (107 lines)
5. `src/mlpy/runtime/capabilities/enhanced_validator.py` - Security (219 lines)
6. `src/mlpy/runtime/capabilities/simple_bridge.py` - Security (48 lines)
7. `src/mlpy/runtime/system_modules/file_safe.py` - Safe file ops (138 lines)
8. `src/mlpy/runtime/system_modules/math_safe.py` - Safe math ops (88 lines)

---

## Phase 1: Critical Bug Fixes (Week 1)
**Goal:** Fix failing tests to establish accurate baseline
**Estimated Effort:** 16 hours
**Expected Coverage Gain:** +2-3%

### Priority 1: REPL Parse Error Tests (7 failures)
**Files:** `tests/unit/test_repl_errors.py`, `tests/unit/test_repl_helper.py`

**Issue:** Error message format changed but tests not updated
```python
# Current expectation: 'Parse Error'
# Actual format: Different error format
```

**Action Items:**
1. Investigate current error message format in REPL
2. Update test expectations to match actual format
3. Fix `test_assert_ml_error` and `test_assert_ml_parse_error` helper methods
4. Verify all 7 REPL error tests pass

**Estimated Time:** 4 hours

---

### Priority 2: Security Analyzer Test (1 failure)
**File:** `tests/unit/test_security_analyzer.py::test_dangerous_function_calls`

**Issue:** Threat categorization mismatch
```python
# Expected: 'code_injection'
# Actual: 'dunder_function_call'
```

**Action Items:**
1. Review security analyzer threat categorization logic
2. Fix categorization or update test expectations
3. Ensure malicious code detection still works correctly

**Estimated Time:** 2 hours

---

### Priority 3: Capabilities Manager Test (1 failure)
**File:** `tests/unit/runtime/test_capabilities_manager.py::test_add_capability_no_context_raises_error`

**Issue:** Missing validation for capability context requirement
```python
# Expected: CapabilityContextError raised
# Actual: No error raised
```

**Action Items:**
1. Add context validation in `CapabilityManager.add_capability()`
2. Ensure security enforcement works correctly
3. Update related tests if needed

**Estimated Time:** 2 hours

---

### Priority 4: Transpiler Parse Error Test (1 failure)
**File:** `tests/unit/test_transpiler.py::test_parse_error_handling`

**Action Items:**
1. Debug transpiler error handling logic
2. Fix error propagation or update test expectations

**Estimated Time:** 2 hours

---

### Priority 5: Integration Tests (4 failures)
**Files:**
- `test_extension_module_e2e.py`
- `test_async_executor.py`
- `test_ml_callback.py`

**Action Items:**
1. Fix extension paths parameter support
2. Fix ML callback error handler
3. Fix extension module E2E test

**Estimated Time:** 4 hours

---

### Priority 6: Performance Test (1 failure)
**File:** `tests/performance/test_transpiler_benchmarks.py::test_program_size_scaling`

**Issue:** Timing variance (57ms vs 50ms expected)

**Action Items:**
1. Mark as flaky test or relax threshold to 60ms
2. Consider environment-specific thresholds

**Estimated Time:** 30 minutes

---

## Phase 2: High-Impact User-Facing Components (Week 2)
**Goal:** Cover critical user-facing features
**Estimated Effort:** 24 hours
**Expected Coverage Gain:** +15-20%

### 2.1: Entry Point Module (0% → 100%)
**File:** `src/mlpy/__main__.py` (3 lines)

**Test Strategy:**
```python
# tests/unit/test_main_entry.py
def test_main_entry_point():
    # Test mlpy command execution

def test_main_with_args():
    # Test argument passing
```

**Estimated Time:** 1 hour
**Coverage Gain:** +0.02%

---

### 2.2: REPL Core Functionality (7% → 50%)
**File:** `src/mlpy/cli/repl.py` (957 lines, 892 uncovered)

**Coverage:** Currently 7% (65/957 lines covered)

**Test Strategy:**
```python
# tests/unit/cli/test_repl_session.py
def test_repl_variable_persistence():
    repl = REPLSession()
    repl.execute("x = 42;")
    result = repl.execute("y = x + 1;")
    assert result.value == 43

def test_repl_multi_line_input():
    # Test function definitions across lines

def test_repl_error_recovery():
    repl = REPLSession()
    repl.execute("invalid syntax")  # Should not crash
    result = repl.execute("x = 1;")  # Should still work
    assert result.value == 1

def test_repl_control_structures():
    # Test for loops, while loops, if statements

def test_repl_special_commands():
    # Test .help, .vars, .clear, .exit
```

**Focus Areas:**
- Multi-line input handling (lines 410-442)
- Control structure execution
- Variable persistence between commands
- Error recovery
- Special command handling

**Estimated Time:** 8 hours
**Coverage Gain:** +5-7%

---

### 2.3: REPL Commands (0% → 80%)
**File:** `src/mlpy/integration/repl_commands.py` (107 lines, 107 uncovered)

**Test Strategy:**
```python
# tests/unit/integration/test_repl_commands.py
def test_help_command():
    repl = REPLSession()
    result = repl.execute(".help")
    assert "Available commands" in result.output

def test_vars_command():
    repl = REPLSession()
    repl.execute("x = 42;")
    result = repl.execute(".vars")
    assert "x" in result.output
    assert "42" in result.output

def test_clear_command():
    repl = REPLSession()
    repl.execute("x = 42;")
    repl.execute(".clear")
    result = repl.execute("x")
    assert "not defined" in result.error

def test_type_command():
    # Test .type inspection

def test_doc_command():
    # Test .doc documentation
```

**Estimated Time:** 3 hours
**Coverage Gain:** +0.6%

---

### 2.4: CLI Commands (11% → 60%)
**File:** `src/mlpy/cli/commands.py` (397 lines, 355 uncovered)

**Test Strategy:**
```python
# tests/unit/cli/test_cli_commands.py
def test_run_command_with_file():
    result = run_ml_file("test.ml")
    assert result.exit_code == 0

def test_run_command_missing_file():
    result = run_ml_file("nonexistent.ml")
    assert result.exit_code != 0
    assert "not found" in result.error_message

def test_repl_command():
    # Test REPL startup

def test_transpile_command():
    # Test ML → Python transpilation

def test_check_command():
    # Test security analysis without execution
```

**Estimated Time:** 4 hours
**Coverage Gain:** +2%

---

### 2.5: Standard Library Modules (34-82% → 80%)
**Target Files:**
- `json_bridge.py` - 41% → 80% (98 lines)
- `http_bridge.py` - 44% → 80% (118 lines)
- `file_bridge.py` - 43% → 80% (90 lines)
- `functional_bridge.py` - 43% → 80% (218 lines)
- `regex_bridge.py` - 44% → 80% (226 lines)

**Test Strategy for JSON Bridge:**
```python
# tests/unit/stdlib/test_json_bridge.py
def test_json_parse_object():
    json = get_json_module()
    result = json.parse('{"name": "test", "value": 42}')
    assert result['name'] == 'test'
    assert result['value'] == 42

def test_json_stringify_object():
    json = get_json_module()
    obj = {'name': 'test', 'value': 42}
    result = json.stringify(obj)
    assert '"name"' in result and '"value"' in result

def test_json_parse_array():
    # Test array parsing

def test_json_parse_invalid():
    # Test error handling

def test_json_stringify_with_indent():
    # Test pretty printing
```

**Apply Similar Pattern to:**
- HTTP bridge: GET/POST/PUT/DELETE requests, headers, error handling
- File bridge: read/write/append operations, path handling
- Functional bridge: map/filter/reduce/curry/compose operations
- Regex bridge: match/replace/split/test operations

**Estimated Time:** 8 hours
**Coverage Gain:** +4-5%

---

## Phase 3: Security-Critical Components (Week 3)
**Goal:** Ensure security systems are thoroughly tested
**Estimated Effort:** 16 hours
**Expected Coverage Gain:** +8-12%

### 3.1: Enhanced Capability Validator (0% → 80%)
**File:** `src/mlpy/runtime/capabilities/enhanced_validator.py` (219 lines, 219 uncovered)

**Test Strategy:**
```python
# tests/unit/capabilities/test_enhanced_validator.py
def test_validator_rejects_overly_broad_patterns():
    validator = EnhancedValidator()
    with pytest.raises(ValidationError):
        validator.validate_pattern("*")  # Too broad
    with pytest.raises(ValidationError):
        validator.validate_pattern("**/*")  # Too broad

def test_validator_accepts_specific_patterns():
    validator = EnhancedValidator()
    assert validator.validate_pattern("data/*.json")
    assert validator.validate_pattern("config/app.yaml")

def test_validator_resource_subset_check():
    validator = EnhancedValidator()
    granted = ["data/*.json", "logs/*.log"]
    requested = ["data/user.json"]
    assert validator.is_subset(requested, granted)

    requested_invalid = ["etc/passwd"]
    assert not validator.is_subset(requested_invalid, granted)

def test_validator_path_traversal_detection():
    validator = EnhancedValidator()
    with pytest.raises(SecurityError):
        validator.validate_pattern("../../../etc/passwd")
```

**Estimated Time:** 4 hours
**Coverage Gain:** +1.2%

---

### 3.2: Simple Bridge (0% → 80%)
**File:** `src/mlpy/runtime/capabilities/simple_bridge.py` (48 lines, 48 uncovered)

**Test Strategy:**
```python
# tests/unit/capabilities/test_simple_bridge.py
def test_bridge_requires_capability():
    with pytest.raises(CapabilityError):
        simple_bridge.call_without_capability()

def test_bridge_with_valid_capability():
    with capability_context("resource", "pattern", "read"):
        result = simple_bridge.call_with_capability()
        assert result is not None
```

**Estimated Time:** 2 hours
**Coverage Gain:** +0.3%

---

### 3.3: Safe System Modules (0% → 80%)
**Files:**
- `file_safe.py` (138 lines)
- `math_safe.py` (88 lines)

**Test Strategy:**
```python
# tests/unit/system_modules/test_file_safe.py
def test_file_safe_read_with_capability():
    with capability_context("file", "test.txt", "read"):
        content = file_safe.read("test.txt")
        assert content is not None

def test_file_safe_read_without_capability():
    with pytest.raises(CapabilityError):
        file_safe.read("test.txt")

def test_file_safe_path_traversal_blocked():
    with capability_context("file", "*", "read"):
        with pytest.raises(SecurityError):
            file_safe.read("../../../etc/passwd")

def test_file_safe_write_with_capability():
    # Test safe write operations

# tests/unit/system_modules/test_math_safe.py
def test_math_safe_operations():
    # Test mathematical operations are safe

def test_math_safe_no_eval():
    # Ensure no eval/exec usage
```

**Estimated Time:** 4 hours
**Coverage Gain:** +1.3%

---

### 3.4: Sandbox System (50% → 75%)
**File:** `src/mlpy/runtime/sandbox/sandbox.py` (225 lines, 113 uncovered)

**Test Strategy:**
```python
# tests/unit/sandbox/test_resource_limits.py
def test_memory_limit_enforcement():
    sandbox = Sandbox(max_memory_mb=100)
    # Test memory limit violations

def test_cpu_time_limit():
    sandbox = Sandbox(max_cpu_seconds=5)
    # Test CPU time limits

def test_file_size_limit():
    sandbox = Sandbox(max_file_size_mb=10)
    # Test file size restrictions

def test_sandbox_isolation():
    # Test process isolation
```

**Estimated Time:** 4 hours
**Coverage Gain:** +1.5%

---

### 3.5: Capabilities Manager (29% → 70%)
**File:** `src/mlpy/runtime/capabilities/manager.py` (148 lines, 105 uncovered)

**Test Strategy:**
```python
# tests/unit/capabilities/test_manager.py
def test_manager_grant_capability():
    manager = CapabilityManager()
    token = manager.grant("file", "data/*.json", "read")
    assert token is not None

def test_manager_revoke_capability():
    # Test capability revocation

def test_manager_check_capability():
    # Test capability validation

def test_manager_hierarchy():
    # Test parent-child capability inheritance
```

**Estimated Time:** 2 hours
**Coverage Gain:** +0.6%

---

## Phase 4: Code Generation & Analysis (Week 4) ✅ **ASSESSMENT COMPLETE**
**Goal:** Improve core transpiler components
**Estimated Effort:** 16 hours
**Expected Coverage Gain:** +8-12%
**Status:** Assessment completed November 2, 2025

### Current Phase 4 Module Coverage Status

**Excellent Coverage (75%+) - No Action Needed:**
- ✅ enhanced_source_maps.py: **100%** (121 lines)
- ✅ context.py: **100%** (23 lines)
- ✅ allowed_functions_registry.py: **96%** (73 lines)
- ✅ safe_attribute_registry.py: **96%** (93 lines)
- ✅ statement_visitors.py: **84%** (246 lines)
- ✅ expression_helpers.py: **74%** (172 lines)
- ✅ python_generator.py: **72%** (165 lines)

**Needs Improvement (<75%) - Priority Targets:**
- ⚠️ **generator_base.py:** **15%** (192 lines, 164 uncovered) - **HIGHEST PRIORITY**
- ⚠️ **module_handlers.py:** **9%** (160 lines, 145 uncovered) - **HIGH PRIORITY**
- ⚠️ **function_call_helpers.py:** **30%** (207 lines, 144 uncovered) - **MEDIUM PRIORITY**
- ⚠️ expression_visitors.py: **28%** (65 lines, 47 uncovered)
- ⚠️ source_map_helpers.py: **62%** (29 lines, 11 uncovered)
- ⚠️ utility_helpers.py: **69%** (32 lines, 10 uncovered)
- ⚠️ literal_visitors.py: **57%** (14 lines, 6 uncovered)

**Total Potential Coverage Gain:** ~470 uncovered lines across priority targets

---

### 4.1: Generator Base (15% → 60%) **NEW PRIORITY #1**
**File:** `src/mlpy/ml/codegen/core/generator_base.py` (192 lines, 164 uncovered)

**Current Coverage:** 15% (28/192 lines)
**Uncovered Lines:** 52-65, 79-96, 110-234, 242-250, 254-258, 262-270, 274-275, 279-300, 304, 312, 316, 320, 328-339, 343-359, 363-376, 389, 393-398

**Test Strategy:**
```python
# tests/unit/codegen/test_generator_base.py
def test_generator_initialization():
    # Test base generator setup with context

def test_context_management():
    # Test generation context handling and scoping

def test_indentation_tracking():
    # Test proper Python indentation generation

def test_visit_methods():
    # Test AST visitor pattern methods

def test_helper_method_delegation():
    # Test delegation to specialized helpers
```

**Estimated Time:** 4 hours
**Coverage Gain:** +0.93% (164 lines)

---

### 4.2: Module Handlers (9% → 60%) **NEW PRIORITY #2**
**File:** `src/mlpy/ml/codegen/helpers/module_handlers.py` (160 lines, 145 uncovered)

**Current Coverage:** 9% (15/160 lines)
**Uncovered Lines:** 59-60, 85-94, 142-153, 163-173, 206-242, 273-316, 337-352, 401-524

**Test Strategy:**
```python
# tests/unit/codegen/test_module_handlers.py
def test_import_statement_generation():
    gen = PythonGenerator()
    ml_code = "import math;"
    python = gen.generate(ml_code)
    assert "import" in python

def test_qualified_import():
    # Test import module as alias

def test_selective_import():
    # Test from module import function

def test_stdlib_module_mapping():
    # Test ML stdlib → Python mapping
```

**Estimated Time:** 4 hours
**Coverage Gain:** +0.9%

---

### 4.2: Function Call Helpers (26% → 60%)
**File:** `src/mlpy/ml/codegen/helpers/function_call_helpers.py` (207 lines, 154 uncovered)

**Test Strategy:**
```python
# tests/unit/codegen/test_function_call_helpers.py
def test_simple_function_call():
    # Test print("hello")

def test_method_call():
    # Test obj.method()

def test_chained_method_calls():
    # Test obj.method1().method2()

def test_function_with_arguments():
    # Test function(arg1, arg2, kwarg=value)
```

**Estimated Time:** 4 hours
**Coverage Gain:** +0.9%

---

### 4.3: Generator Base (15% → 50%)
**File:** `src/mlpy/ml/codegen/core/generator_base.py` (192 lines, 164 uncovered)

**Test Strategy:**
```python
# tests/unit/codegen/test_generator_base.py
def test_generator_initialization():
    # Test base generator setup

def test_context_management():
    # Test generation context handling

def test_indentation_tracking():
    # Test proper Python indentation
```

**Estimated Time:** 3 hours
**Coverage Gain:** +0.9%

---

### 4.4: Analysis Components (13-81% → 70%)
**Target Files:**
- `optimizer.py` - 17% → 70% (388 lines)
- `type_checker.py` - 16% → 70% (431 lines)
- `security_deep.py` - 26% → 70% (376 lines)

**Test Strategy:**
```python
# tests/unit/analysis/test_optimizer.py
def test_constant_folding():
    # Test 2 + 2 → 4 optimization

def test_dead_code_elimination():
    # Test removal of unreachable code

def test_loop_optimization():
    # Test loop invariant code motion

# tests/unit/analysis/test_type_checker.py
def test_basic_type_inference():
    # Test variable type inference

def test_function_return_type():
    # Test function return type checking

def test_type_error_detection():
    # Test invalid type operations

# tests/unit/analysis/test_security_deep.py
def test_deep_data_flow_analysis():
    # Test complex taint propagation

def test_control_flow_security():
    # Test conditional security checks
```

**Estimated Time:** 5 hours
**Coverage Gain:** +4-5%

---

## Phase 5: Advanced Features & Polish (Week 5)
**Goal:** Cover remaining gaps and achieve 75% target
**Estimated Effort:** 16 hours
**Expected Coverage Gain:** +5-10%

### 5.1: LSP Server (15-41% → 65%)
**Files:**
- `server.py` - 15% → 65% (272 lines)
- `handlers.py` - 25% → 65% (167 lines)
- `semantic_tokens.py` - 36% → 65% (218 lines)

**Test Strategy:**
```python
# tests/unit/lsp/test_lsp_features.py
def test_hover_on_function():
    lsp = LSPServer()
    response = lsp.hover("file.ml", line=5, col=10)
    assert response.contents is not None

def test_completion_stdlib_modules():
    lsp = LSPServer()
    completions = lsp.complete("file.ml", line=1, col=7, text="import ")
    assert any("math" in c.label for c in completions)

def test_diagnostics_syntax_error():
    # Test error reporting

def test_semantic_tokens():
    # Test syntax highlighting tokens
```

**Estimated Time:** 6 hours
**Coverage Gain:** +2-3%

---

### 5.2: Debugging System (0-77% → 60%)
**Files:**
- `repl.py` - 0% → 60% (350 lines)
- `error_formatter.py` - 20% → 60% (190 lines)
- `variable_formatter.py` - 16% → 60% (120 lines)

**Test Strategy:**
```python
# tests/unit/debugging/test_debug_repl.py
def test_debug_repl_breakpoint():
    # Test breakpoint handling

def test_debug_repl_step_through():
    # Test step execution

def test_debug_repl_variable_inspection():
    # Test variable viewing

# tests/unit/debugging/test_formatters.py
def test_error_formatting():
    # Test error message formatting

def test_variable_formatting():
    # Test variable display formatting
```

**Estimated Time:** 6 hours
**Coverage Gain:** +2-3%

---

### 5.3: Advanced AST Nodes (0% → 40%)
**File:** `src/mlpy/ml/grammar/advanced_ast_nodes.py` (350 lines, 350 uncovered)

**Note:** This is for future advanced features (pattern matching, generics, async/await). Low priority unless actively being developed.

**Test Strategy:**
```python
# tests/unit/grammar/test_advanced_ast_nodes.py
def test_pattern_match_ast():
    # Test pattern match AST construction

def test_generic_type_ast():
    # Test generic type AST nodes

def test_async_await_ast():
    # Test async/await AST nodes
```

**Estimated Time:** 4 hours (optional)
**Coverage Gain:** +2%

---

## Implementation Guidelines

### Testing Best Practices
1. **Test Behavior, Not Implementation** - Focus on what code does, not how it does it
2. **Use Descriptive Test Names** - `test_json_parse_handles_nested_objects()`
3. **One Assertion Per Test** - Or related assertions for the same behavior
4. **Use Fixtures for Setup** - Reduce duplication with pytest fixtures
5. **Mock External Dependencies** - Don't depend on network, filesystem, etc.
6. **Test Error Cases** - Not just happy paths

### Coverage Measurement
```bash
# Before starting each phase
pytest --cov=src/mlpy --cov-report=term-missing --cov-report=html

# After completing tests
pytest --cov=src/mlpy --cov-report=term-missing tests/

# Weekly review
pytest --cov=src/mlpy --cov-report=html
# Open htmlcov/index.html to review coverage
```

### Code Review Checklist
- [ ] Tests pass locally
- [ ] Coverage increased as expected
- [ ] No regressions in existing tests
- [ ] Test names are descriptive
- [ ] Tests are maintainable
- [ ] Edge cases covered
- [ ] Error cases tested

---

## Timeline & Milestones

### Week 1: Critical Bug Fixes
- **Start:** 35% coverage
- **Goal:** Fix all 15 failing tests
- **End:** ~37% coverage
- **Milestone:** Stable test suite baseline

### Week 2: User-Facing Components
- **Start:** 37% coverage
- **Goal:** REPL, CLI, stdlib testing
- **End:** ~55% coverage
- **Milestone:** Core user features well-tested

### Week 3: Security Components
- **Start:** 55% coverage
- **Goal:** Capabilities, sandbox, safe modules
- **End:** ~65% coverage
- **Milestone:** Security systems verified

### Week 4: Code Generation & Analysis
- **Start:** 65% coverage
- **Goal:** Codegen helpers, analysis modules
- **End:** ~73% coverage
- **Milestone:** Transpiler pipeline tested

### Week 5: Advanced Features & Polish
- **Start:** 73% coverage
- **Goal:** LSP, debugging, remaining gaps
- **End:** ~75-80% coverage
- **Milestone:** Production-ready quality

---

## Success Metrics

### Coverage Targets
- **50% coverage** - ✅ Respectable, core functionality tested
- **65% coverage** - ✅ Good, most critical paths covered
- **75% coverage** - ✅ **TARGET: Excellent, production-ready**
- **85% coverage** - ⭐ Aspirational, comprehensive testing
- **95% coverage** - 🎯 Unlikely, requires testing generated code

### Quality Metrics
- **Zero Failing Tests** - All tests pass consistently
- **Fast Test Suite** - < 2 minutes for full suite
- **Maintainable Tests** - Easy to update when code changes
- **Meaningful Coverage** - Tests catch real bugs, not just hit lines

---

## Risks & Mitigations

### Risk: Tests Break During Development
**Mitigation:**
- Run tests frequently during development
- Fix broken tests immediately
- Use CI/CD to catch breaks early

### Risk: Coverage Theater (Tests That Don't Test)
**Mitigation:**
- Review test quality, not just coverage numbers
- Ensure tests assert actual behavior
- Include negative test cases

### Risk: Time Overruns
**Mitigation:**
- Focus on Phases 1-3 first (critical components)
- Phases 4-5 are optional polish
- 65% coverage is still excellent

### Risk: Flaky Tests
**Mitigation:**
- Mark timing-sensitive tests as flaky
- Use mocks for external dependencies
- Ensure tests are deterministic

---

## Future Considerations

### Post-75% Coverage
Once 75% coverage is achieved, focus on:
1. **Mutation Testing** - Ensure tests actually catch bugs
2. **Integration Testing** - More end-to-end workflow tests
3. **Performance Testing** - Benchmarking and regression detection
4. **Fuzz Testing** - Random input generation for edge cases

### Maintenance
- **Weekly Coverage Reviews** - Track coverage trends
- **New Code Requirement** - All new code must include tests
- **Coverage Gates** - CI/CD fails if coverage drops below 70%

---

## Appendix: Quick Reference

### Top 10 Files by Impact (ROI)
| File | Lines | Coverage | Est. Time | Coverage Gain |
|------|-------|----------|-----------|---------------|
| 1. repl.py | 957 | 7% | 8h | +5-7% |
| 2. Standard Library (combined) | ~1800 | 34-82% | 8h | +4-5% |
| 3. enhanced_validator.py | 219 | 0% | 4h | +1.2% |
| 4. optimizer.py | 388 | 17% | 3h | +1.5% |
| 5. type_checker.py | 431 | 16% | 3h | +1.5% |
| 6. sandbox.py | 225 | 50% | 4h | +1.5% |
| 7. module_handlers.py | 160 | 6% | 4h | +0.9% |
| 8. function_call_helpers.py | 207 | 26% | 4h | +0.9% |
| 9. file_safe.py | 138 | 0% | 2h | +0.8% |
| 10. repl_commands.py | 107 | 0% | 3h | +0.6% |

**Total:** ~43 hours → +18-22% coverage gain

---

## Status Tracking

### Document History
- **October 24, 2025:** Initial plan created (coverage-improvement-plan.md)
- **October 29, 2025:** Consolidated into unified proposal (this document)
- **Status:** Active - Ready for Phase 1 implementation

### Related Documents
- **OUTDATED:** `docs/assessments/coverage-improvement-plan.md` - Superseded by this proposal
- **OUTDATED:** `docs/summaries/test-coverage-assessment.md` - Superseded by this proposal
- **Reference:** `htmlcov/index.html` - Current coverage report (October 29, 2025)

---

**Next Steps:** Begin Phase 1 - Fix all 15 failing tests to establish stable baseline.
