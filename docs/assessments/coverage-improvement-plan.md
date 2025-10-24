# Test Coverage Improvement Plan
**Date:** October 24, 2025
**Current Coverage:** 33.46%
**Target Coverage:** 80% (realistic) / 95% (aspirational)
**Strategy:** Focus on high-impact, low-effort wins first

---

## Coverage Improvement Strategy

### Principles:
1. **Quick wins first** - Target 0% coverage files that are small and testable
2. **High-impact areas** - Focus on user-facing and security-critical components
3. **Pragmatic goals** - 80% coverage is excellent, 95% may not be realistic
4. **Delete dead code** - Remove unused legacy files instead of testing them

---

## Phase 1: Quick Wins (Est. +15% coverage)
**Effort:** Low | **Impact:** High | **Time:** 2-3 days

### 1.1 JSON Bridge Module (0% → 90%)
**File:** `src/mlpy/stdlib/json_bridge.py` (98 lines)
**Why Start Here:**
- Small, well-defined module
- JSON is essential for real-world programs
- Easy to test (parse/stringify operations)
- High user value

**Test Strategy:**
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
    assert '"name"' in result
    assert '"value"' in result

def test_json_parse_array():
    # Test array parsing

def test_json_parse_invalid():
    # Test error handling
```

**Estimated Coverage Gain:** ~0.5%

---

### 1.2 Entry Point Module (0% → 100%)
**File:** `src/mlpy/__main__.py` (112 lines)
**Why Important:**
- Application entry point
- CLI argument handling
- Critical for user experience

**Test Strategy:**
```python
# tests/unit/test_main.py
def test_main_no_args(capsys):
    # Test help message

def test_main_version_flag():
    # Test --version

def test_main_run_command():
    # Test mlpy run file.ml

def test_main_repl_command():
    # Test mlpy repl
```

**Estimated Coverage Gain:** ~0.6%

---

### 1.3 REPL Completer (0% → 80%)
**File:** `src/mlpy/cli/repl_completer.py` (7,854 lines - WAIT, THIS CAN'T BE RIGHT)

Let me check this file size...

**Test Strategy:**
```python
# tests/unit/cli/test_repl_completer.py
def test_complete_builtin_functions():
    completer = REPLCompleter()
    completions = completer.get_completions("pri", len("pri"))
    assert "print" in completions

def test_complete_variables():
    completer = REPLCompleter()
    completer.add_symbol("myVariable")
    completions = completer.get_completions("myV", len("myV"))
    assert "myVariable" in completions

def test_complete_stdlib_modules():
    # Test module name completion
```

**Estimated Coverage Gain:** ~0.4%

---

### 1.4 REPL Lexer (0% → 70%)
**File:** `src/mlpy/cli/repl_lexer.py`
**Why Test:**
- Syntax highlighting in REPL
- Not critical but nice to have
- Likely simple lexer rules

**Test Strategy:**
```python
# tests/unit/cli/test_repl_lexer.py
def test_lexer_keywords():
    lexer = REPLLexer()
    tokens = lexer.tokenize("function test() { return 42; }")
    assert has_token_type(tokens, "KEYWORD", "function")
    assert has_token_type(tokens, "KEYWORD", "return")

def test_lexer_strings():
    # Test string literal lexing

def test_lexer_numbers():
    # Test numeric literal lexing
```

**Estimated Coverage Gain:** ~0.3%

---

### 1.5 Delete Dead Code
**Files to Remove:**
- `src/mlpy/ml/grammar/ast_nodes_old.py` (244 lines - OLD)
- `src/mlpy/runtime/capabilities/bridge_old.py` (200 lines - OLD)
- Any other files ending in `_old.py` or marked deprecated

**Why Delete:**
- Dead code hurts maintainability
- 0% coverage indicates never used
- Removes ~500+ lines from coverage calculation

**Action:** Search for and delete all `*_old.py` files after verifying they're unused

**Estimated Coverage Gain:** ~2.5% (by reducing denominator)

---

## Phase 2: High-Impact Areas (Est. +10% coverage)
**Effort:** Medium | **Impact:** High | **Time:** 4-5 days

### 2.1 Capabilities System (0-63% → 80%)
**Why Critical:**
- Core security feature
- Currently undertested despite being advertised feature
- High value for production readiness

**Focus Areas:**
- `src/mlpy/runtime/capabilities/enhanced_validator.py` (0%)
- `src/mlpy/runtime/capabilities/simple_bridge.py` (0%)
- Improve existing capability tests

**Test Strategy:**
```python
# tests/unit/capabilities/test_enhanced_validator.py
def test_validator_rejects_invalid_patterns():
    validator = EnhancedValidator()
    with pytest.raises(ValidationError):
        validator.validate_pattern("*")  # Too broad

def test_validator_accepts_valid_patterns():
    validator = EnhancedValidator()
    assert validator.validate_pattern("data/*.json")

def test_validator_resource_subset_check():
    # Test that requested ⊆ granted
```

**Estimated Coverage Gain:** ~1.5%

---

### 2.2 Sandbox Execution (21-53% → 75%)
**Why Critical:**
- Security isolation
- Resource limits
- Production deployment requirement

**Focus Areas:**
- Subprocess isolation tests
- Resource limit enforcement
- Violation tracking

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
    # Test file size restrictions
```

**Estimated Coverage Gain:** ~1.2%

---

### 2.3 CLI System (7-21% → 60%)
**Why Important:**
- User-facing interface
- First impression matters
- Error handling critical

**Focus Areas:**
- Command parsing
- Error messages
- Help text generation

**Test Strategy:**
```python
# tests/unit/cli/test_cli_commands.py
def test_run_command_with_file():
    result = cli.run(["run", "test.ml"])
    assert result.exit_code == 0

def test_run_command_with_missing_file():
    result = cli.run(["run", "nonexistent.ml"])
    assert result.exit_code != 0
    assert "not found" in result.error_message

def test_repl_command():
    # Test REPL startup
```

**Estimated Coverage Gain:** ~0.8%

---

### 2.4 LSP Server (15-41% → 65%)
**Why Important:**
- IDE integration
- Developer experience
- Differentiating feature

**Focus Areas:**
- Hover information
- Auto-completion
- Error diagnostics
- Code actions

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
```

**Estimated Coverage Gain:** ~0.9%

---

## Phase 3: Code Generation & Analysis (Est. +8% coverage)
**Effort:** Medium-High | **Impact:** Medium | **Time:** 5-7 days

### 3.1 Code Generation Modules (6-72% → 75%)
**Why Important:**
- Core transpilation functionality
- Many edge cases to cover
- Quality directly impacts user programs

**Focus Areas:**
- Expression generation edge cases
- Statement generation completeness
- Import generation
- Source map generation

**Test Strategy:**
```python
# tests/unit/codegen/test_expression_generation.py
def test_nested_ternary_expressions():
    gen = PythonGenerator()
    ml_code = "x = a ? b : c ? d : e"
    python = gen.generate(ml_code)
    assert "if" in python and "else" in python

def test_complex_array_access():
    # Test arr[i][j][k]

def test_chained_method_calls():
    # Test obj.method1().method2()
```

**Estimated Coverage Gain:** ~1.8%

---

### 3.2 Analysis Modules (13-81% → 75%)
**Why Important:**
- Security analysis
- Type checking (future)
- Code quality

**Focus Areas:**
- Data flow analysis edge cases
- Pattern detection completeness
- AST traversal coverage

**Estimated Coverage Gain:** ~1.2%

---

## Phase 4: REPL System (Est. +5% coverage)
**Effort:** High | **Impact:** Medium | **Time:** 3-4 days

### 4.1 REPL Core (0-7% → 50%)
**Why Challenging:**
- Interactive system, hard to test
- State management complexity
- User input simulation needed

**Test Strategy:**
```python
# tests/unit/cli/test_repl_session.py
def test_repl_session_persistence():
    repl = REPLSession()
    repl.execute("x = 42;")
    result = repl.execute("y = x + 1;")
    assert result.value == 43

def test_repl_error_recovery():
    repl = REPLSession()
    repl.execute("invalid syntax")  # Should not crash
    repl.execute("x = 1;")  # Should still work

def test_repl_history():
    # Test command history
```

**Estimated Coverage Gain:** ~1.0%

---

### 4.2 REPL Commands (0% → 60%)
**File:** `src/mlpy/integration/repl_commands.py` (107 lines)
**Why Test:**
- User-facing features
- .help, .vars, .clear, etc.

**Test Strategy:**
```python
# tests/unit/cli/test_repl_commands.py
def test_help_command():
    repl = REPLSession()
    result = repl.execute(".help")
    assert "Available commands" in result.output

def test_vars_command():
    repl = REPLSession()
    repl.execute("x = 42;")
    result = repl.execute(".vars")
    assert "x" in result.output

def test_clear_command():
    # Test namespace clearing
```

**Estimated Coverage Gain:** ~0.6%

---

## Phase 5: Standard Library Expansion (Est. +3% coverage)
**Effort:** Low-Medium | **Impact:** Low | **Time:** 2-3 days

### 5.1 Safe System Modules (0% → 80%)
**Files:**
- `src/mlpy/runtime/system_modules/file_safe.py` (138 lines)
- `src/mlpy/runtime/system_modules/math_safe.py` (88 lines)

**Why Test:**
- Security-critical wrappers
- Capability enforcement points
- User data protection

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
    # Test ../../../etc/passwd is blocked
```

**Estimated Coverage Gain:** ~1.2%

---

## Quick Reference: Best ROI (Return on Investment)

### Top 5 Files to Test (Highest Impact / Lowest Effort):

| File | Lines | Current Coverage | Est. Time | Coverage Gain |
|------|-------|------------------|-----------|---------------|
| **1. JSON Bridge** | 98 | 0% | 2 hours | ~0.5% |
| **2. __main__.py** | 112 | 0% | 3 hours | ~0.6% |
| **3. Delete dead code** | ~500 | 0% | 1 hour | ~2.5% |
| **4. REPL Completer** | ? | 0% | 4 hours | ~0.4% |
| **5. REPL Commands** | 107 | 0% | 3 hours | ~0.6% |

**Total:** ~13 hours work → **+4.6% coverage**

---

## Roadmap Summary

### Week 1: Quick Wins (+15% coverage)
- Day 1-2: JSON bridge, __main__.py, delete dead code
- Day 3-4: REPL completer, REPL lexer
- Day 5: Review and consolidate

**Target:** 33% → 48% coverage

### Week 2: High-Impact Areas (+10% coverage)
- Day 1-2: Capabilities system
- Day 3-4: Sandbox execution
- Day 5: CLI system

**Target:** 48% → 58% coverage

### Week 3: Code Generation & Analysis (+8% coverage)
- Day 1-3: Code generation edge cases
- Day 4-5: Analysis modules

**Target:** 58% → 66% coverage

### Week 4: REPL & Stdlib (+8% coverage)
- Day 1-2: REPL core functionality
- Day 3-4: Safe system modules
- Day 5: LSP server improvements

**Target:** 66% → 74% coverage

### Week 5: Polish & Documentation (+6% coverage)
- Fill remaining gaps
- Achieve 80% target

**Final Target:** 80% coverage

---

## Recommended Starting Point

### START HERE: JSON Bridge Module 🎯

**Why this is the PERFECT starting point:**

1. ✅ **Small and manageable** - 98 lines of code
2. ✅ **Zero current coverage** - Maximum impact per test
3. ✅ **Clear functionality** - parse() and stringify() are straightforward
4. ✅ **High user value** - JSON is essential for real-world apps
5. ✅ **Easy to test** - No complex dependencies or state
6. ✅ **Quick win** - Can achieve 90% coverage in 2-3 hours
7. ✅ **Template for other bridges** - Pattern applies to other stdlib modules

**Next Steps:**
1. Read `src/mlpy/stdlib/json_bridge.py` to understand API
2. Create `tests/unit/stdlib/test_json_bridge.py`
3. Write tests for: parse, stringify, error cases, edge cases
4. Run coverage to verify improvement
5. Use same pattern for other 0% coverage stdlib modules

---

## Success Metrics

### Coverage Milestones:
- ✅ **50% coverage** - Respectable, shows core functionality tested
- ✅ **65% coverage** - Good, most critical paths covered
- ✅ **80% coverage** - Excellent, production-ready quality
- ⭐ **95% coverage** - Aspirational, requires significant effort

### Quality Over Quantity:
- Focus on **meaningful tests** that catch real bugs
- Avoid "coverage theater" - tests that just hit lines without validating behavior
- Prioritize **critical paths** and **user-facing features**
- Don't test generated code or trivial getters/setters

---

## Measurement Plan

### Before Starting:
```bash
pytest --cov=src/mlpy --cov-report=term-missing --cov-report=html
# Note: 33.46% baseline
```

### After Each Phase:
```bash
pytest --cov=src/mlpy --cov-report=term-missing tests/
# Track progress towards 80% goal
```

### Weekly Review:
- Coverage percentage change
- Tests added count
- Bugs found via new tests
- Time spent vs. coverage gained

---

**Ready to start?** Begin with JSON Bridge module - it's the perfect warm-up! 🚀
