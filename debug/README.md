# mlpy Debug Tools

This directory contains debugging and comparison tools for systematic ML language development and validation.

## Tools Overview

### `compare_slicing.py` - Dynamic ML vs Python Comparison
**Purpose:** Comprehensive slicing behavior validation using live ML execution.

**Features:**
- Executes ML code dynamically via REPLTestHelper
- Compares ML results with Python expectations
- 24 comprehensive test cases covering all slice patterns
- Detailed mismatch analysis

**Usage:**
```bash
# Basic comparison
python debug/compare_slicing.py

# Show transpiled Python code for each test
python debug/compare_slicing.py --debug

# Verbose execution details
python debug/compare_slicing.py --verbose
```

**Output:**
- Comparison table with PASS/FAIL status
- Summary statistics (X/24 cases match)
- Detailed issue analysis for failures

**Test Coverage:**
- Basic slicing: `arr[1:4]`, `arr[0:3]`
- Open-ended: `arr[:3]`, `arr[2:]`, `arr[:]`
- Negative indices: `arr[-1:]`, `arr[:-1]`, `arr[-3:-1]`
- Step slicing: `arr[::2]`, `arr[1::2]`
- Reverse: `arr[::-1]`, `arr[::-2]`
- Complex: `arr[-1::-1]`, `arr[-2::-1]`
- Edge cases: `arr[10:]`, `arr[3:1]`, `arr[0:0]`

### `debug_negative_slice.py` - Negative Index Debug Tool
**Purpose:** Focused debugging for negative index and negative step slicing.

**Features:**
- Shows ML expression, transpiled Python, and results side-by-side
- Executes both ML and Python for direct comparison
- Quick visual verification

**Usage:**
```bash
python debug/debug_negative_slice.py
```

**Output:**
```
### Negative start (from last)
ML Expression: `arr[-1:]`
Transpiled Python: `arr[-1:]`
ML Result: [50]
Python Result: [50]
[OK] Match
```

## Systematic Debugging Workflow

### 1. Quick Syntax Check
```bash
# Parse ML file and show AST
python -m mlpy parse <file.ml>
```

### 2. Quick Execution Test
```bash
# Execute ML file
python -m mlpy run <file.ml>
```

### 3. Feature Comparison Testing
Use comparison tools like `compare_slicing.py` to validate language features:

```python
# Pattern for creating new comparison tools
from repl_test_helper import REPLTestHelper

repl = REPLTestHelper(security_enabled=False)
repl.execute_ml("setup code;")

ml_result = repl.execute_ml("test expression;")
python_result = eval("equivalent python")

assert ml_result == python_result
```

### 4. Layer-by-Layer Debugging

When debugging a language feature issue, test at each layer:

#### **Layer 1: Lexer (Tokens)**
```python
from lark import Lark
with open('src/mlpy/ml/grammar/ml.lark') as f:
    grammar = f.read()
parser = Lark(grammar, start='program', parser='lalr')
tokens = list(parser.lex('code here'))
for tok in tokens:
    print(f'Token: {tok.type:20} Value: "{tok.value}"')
```

#### **Layer 2: Parser (Parse Tree)**
```python
from lark import Lark
parser = Lark(grammar, start='program', parser='lalr', transformer=None)
tree = parser.parse('code here')
print(tree.pretty())
```

#### **Layer 3: Transformer (AST)**
```python
from mlpy.ml.grammar.parser import MLParser
parser = MLParser()
ast = parser.parse('code here')
# Inspect AST nodes
```

#### **Layer 4: Code Generator (Python Output)**
```python
from mlpy.ml.transpiler import MLTranspiler
transpiler = MLTranspiler()
result = transpiler.transpile_to_python('code here')
print(result[0])
```

#### **Layer 5: Execution (Runtime)**
```python
from repl_test_helper import REPLTestHelper
repl = REPLTestHelper(security_enabled=False)
result = repl.execute_ml('code here;')
print(result)
```

## Creating New Debug Tools

### Template for Comparison Tools

```python
#!/usr/bin/env python3
"""Description of what this tool tests."""

import sys
sys.path.insert(0, 'tests/helpers')

from repl_test_helper import REPLTestHelper

# Initialize REPL
repl = REPLTestHelper(security_enabled=False)

# Test cases: (description, ml_code, expected_result)
test_cases = [
    ("Description", "ml code;", expected_value),
    # ... more cases
]

# Run tests
print("=" * 80)
print("TEST SUITE NAME")
print("=" * 80)

for desc, ml_code, expected in test_cases:
    ml_result = repl.execute_ml(ml_code)
    match = "PASS" if ml_result == expected else "FAIL"
    print(f"[{match}] {desc}: {ml_code}")
    if ml_result != expected:
        print(f"  Expected: {expected}")
        print(f"  Got:      {ml_result}")
```

## Best Practices

### When to Create Debug Tools

1. **New Language Feature:** Create comparison tool with comprehensive test cases
2. **Bug Investigation:** Create minimal reproduction tool
3. **Regression Testing:** Extend existing comparison tools

### Naming Conventions

- `compare_<feature>.py` - Comprehensive feature validation
- `debug_<issue>.py` - Focused bug investigation
- `test_<component>.py` - Component-specific testing

### Documentation

Each debug tool should have:
- Docstring explaining purpose
- Usage examples in comments
- Clear output format
- Test case documentation

## Integration with Development Workflow

### Before Committing Features

1. Run relevant comparison tools
2. Verify 100% test pass rate
3. Add new test cases for edge cases
4. Update this README if new tools added

### When Investigating Bugs

1. Create minimal reproduction case
2. Use layer-by-layer debugging
3. Create focused debug tool
4. Verify fix with comparison tool
5. Add regression test case

## Memory Aid: Quick Commands

```bash
# Parse only
python -m mlpy parse <file.ml>

# Execute
python -m mlpy run <file.ml>

# Slicing validation
python debug/compare_slicing.py

# Debug with transpiled code
python debug/compare_slicing.py --debug

# Create new comparison tool
cp debug/compare_slicing.py debug/compare_<new_feature>.py
# Edit test cases...
```

## Tool Development History

| Tool | Created | Purpose | Test Cases | Status |
|------|---------|---------|-----------|--------|
| `compare_slicing.py` | Oct 2, 2025 | Slicing validation | 24 | ✅ Active |
| `debug_negative_slice.py` | Oct 2, 2025 | Negative index debug | 4 | ✅ Active |

---

**Remember:** Good debug tools save hours of manual testing and catch regressions early!
