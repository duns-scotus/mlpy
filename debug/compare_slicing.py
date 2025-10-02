#!/usr/bin/env python3
"""Compare Python slicing with ML slicing results."""

import sys
import argparse

sys.path.insert(0, 'tests/helpers')

from repl_test_helper import REPLTestHelper

# Parse command line arguments
parser = argparse.ArgumentParser(description='Compare ML and Python slicing behavior')
parser.add_argument('--debug', action='store_true', help='Show transpiled Python code')
parser.add_argument('--verbose', action='store_true', help='Show execution details')
args = parser.parse_args()

# Python reference
arr = [10, 20, 30, 40, 50]

# Initialize REPL helper for dynamic ML execution
repl = REPLTestHelper(security_enabled=False)

# Setup ML array in REPL session
repl.execute_ml("arr = [10, 20, 30, 40, 50];")

# Function to execute ML slice and get result
def get_ml_slice_result(slice_expr: str, show_transpiled=False):
    """Execute ML slice expression and return result."""
    try:
        result = repl.execute_ml(slice_expr)
        if show_transpiled:
            transpiled = repl.get_transpiled_python(slice_expr)
            print(f"  [DEBUG] Transpiled: {transpiled}")
        return result
    except Exception as e:
        return f"ERROR: {str(e)}"

# Python test cases
test_cases = [
    ("case1", "arr[1:4]", arr[1:4]),
    ("case2", "arr[0:3]", arr[0:3]),
    ("case3", "arr[2:5]", arr[2:5]),
    ("case4", "arr[:3]", arr[:3]),
    ("case5", "arr[2:]", arr[2:]),
    ("case6", "arr[:]", arr[:]),
    ("case7", "arr[-1:]", arr[-1:]),
    ("case8", "arr[-2:]", arr[-2:]),
    ("case9", "arr[-3:]", arr[-3:]),
    ("case10", "arr[:-1]", arr[:-1]),
    ("case11", "arr[:-2]", arr[:-2]),
    ("case12", "arr[-3:-1]", arr[-3:-1]),
    ("case13", "arr[-4:-2]", arr[-4:-2]),
    ("case14", "arr[::2]", arr[::2]),
    ("case15", "arr[::3]", arr[::3]),
    ("case16", "arr[1::2]", arr[1::2]),
    ("case17", "arr[::-1]", arr[::-1]),
    ("case18", "arr[::-2]", arr[::-2]),
    ("case19", "arr[-1::-1]", arr[-1::-1]),
    ("case20", "arr[-2::-1]", arr[-2::-1]),
    ("case21", "arr[10:]", arr[10:]),
    ("case22", "arr[3:1]", arr[3:1]),
    ("case23", "arr[0:0]", arr[0:0]),
    ("case24", "arr[5:10]", arr[5:10]),
]

# Generate comparison table
print("=" * 80)
print("ML SLICING vs PYTHON SLICING - DYNAMIC COMPARISON")
print("Using REPLTestHelper for live ML execution")
print("=" * 80)
print()
print("| CASE | ML SYNTAX | ML RESULT | PYTHON EXPECTATION | MATCH? | ISSUE |")
print("|------|-----------|-----------|-------------------|--------|-------|")

ml_results = {}  # Store ML results for later analysis
for case_name, syntax, python_result in test_cases:
    # Execute ML code dynamically
    if args.verbose:
        print(f"\n[VERBOSE] Executing: {syntax}")

    ml_result = get_ml_slice_result(syntax + ";", show_transpiled=args.debug)
    ml_results[case_name] = ml_result

    # Check if ML execution resulted in an error
    is_ml_error = isinstance(ml_result, str) and ml_result.startswith("ERROR:")
    match = "YES" if ml_result == python_result else "NO"

    # Determine issue
    issue = ""
    if is_ml_error:
        issue = "ML Execution Error"
    elif ml_result != python_result:
        if "-" in syntax and ":-" not in syntax and "::-" not in syntax:
            # Has negative index but not negative step
            if syntax.startswith("arr[-"):
                issue = "Negative start index"
            elif ":-" in syntax:
                issue = "Negative end index"
            else:
                issue = "Negative indices"
        elif "::-" in syntax:
            issue = "Negative step (reverse)"
        elif "-1::-1" in syntax or "-2::-1" in syntax:
            issue = "Negative start + reverse"
        else:
            issue = "Unknown difference"

    # Format results for table
    ml_str = str(ml_result) if len(str(ml_result)) < 25 else str(ml_result)[:22] + "..."
    py_str = str(python_result) if len(str(python_result)) < 25 else str(python_result)[:22] + "..."

    print(f"| {case_name:4} | {syntax:20} | {ml_str:20} | {py_str:20} | {match:6} | {issue:30} |")

# Summary
total = len(test_cases)
matches = sum(1 for case_name, _, py_result in test_cases if ml_results[case_name] == py_result)
print(f"\n**Summary:** {matches}/{total} cases match ({matches*100//total}% compatibility)")

# Detailed analysis
print("\n## Detailed Issue Analysis:\n")

failures = [(case, syntax, ml_results[case], py_result)
            for case, syntax, py_result in test_cases
            if ml_results[case] != py_result]

for case_name, syntax, ml_result, python_result in failures:
    print(f"### {case_name}: `{syntax}`")
    print(f"- **ML Result:**     {ml_result}")
    print(f"- **Python Result:** {python_result}")
    print()
