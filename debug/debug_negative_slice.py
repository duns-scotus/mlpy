#!/usr/bin/env python3
"""Debug negative index slicing to see transpiled code."""

import sys
sys.path.insert(0, 'tests/helpers')

from repl_test_helper import REPLTestHelper

repl = REPLTestHelper(security_enabled=False)

# Setup
repl.execute_ml("arr = [10, 20, 30, 40, 50];")

# Test cases with issues
test_cases = [
    ("arr[-1:]", "Negative start (from last)"),
    ("arr[:-1]", "Negative end (all but last)"),
    ("arr[-3:-1]", "Negative start and end"),
    ("arr[::-1]", "Reverse with negative step"),
]

print("=" * 80)
print("NEGATIVE INDEX SLICING DEBUG")
print("=" * 80)

for ml_expr, description in test_cases:
    print(f"\n### {description}")
    print(f"ML Expression: `{ml_expr}`")

    transpiled = repl.get_transpiled_python(ml_expr + ";")

    # Extract just the actual slice line
    lines = transpiled.split('\n')
    slice_line = None
    for line in lines:
        if 'arr[' in line and not line.strip().startswith('#'):
            slice_line = line.strip()
            break

    print(f"Transpiled Python: `{slice_line}`")

    # Execute and show result
    try:
        ml_result = repl.execute_ml(ml_expr + ";")
        print(f"ML Result: {ml_result}")
    except Exception as e:
        print(f"ML Error: {e}")

    # Show what Python would do
    arr = [10, 20, 30, 40, 50]
    python_result = eval(ml_expr)
    print(f"Python Result: {python_result}")

    if ml_result != python_result:
        print(f"[X] MISMATCH!")
    else:
        print(f"[OK] Match")
