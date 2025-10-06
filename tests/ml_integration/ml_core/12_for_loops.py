"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

def test_basic_for():
    arr = [1, 2, 3, 4, 5]
    sum = 0
    for item in arr:
        sum = (sum + item)
    return sum

def test_for_break():
    arr = [1, 2, 3, 4, 5]
    sum = 0
    for item in arr:
        if (item == 3):
            break
        sum = (sum + item)
    return sum

def test_for_continue():
    arr = [1, 2, 3, 4, 5]
    sum = 0
    for item in arr:
        if (item == 3):
            continue
        sum = (sum + item)
    return sum

def test_nested_for():
    outer = [1, 2, 3]
    inner = [10, 20]
    total = 0
    for o in outer:
        for i in inner:
            total = (total + (o * i))
    return total

def test_nested_break():
    outer = [1, 2, 3]
    inner = [10, 20, 30]
    results = []
    for o in outer:
        for i in inner:
            if (i == 20):
                break
            results = (results + [(o * i)])
    return results

def test_nested_continue():
    outer = [1, 2, 3]
    inner = [10, 20, 30]
    results = []
    for o in outer:
        if (o == 2):
            continue
        for i in inner:
            results = (results + [(o * i)])
    return results

def test_for_empty():
    arr = []
    count = 0
    for item in arr:
        count = (count + 1)
    return count

def test_for_build_array():
    source = [1, 2, 3, 4, 5]
    doubled = []
    for num in source:
        doubled = (doubled + [(num * 2)])
    return doubled

def main():
    results = {}
    results['basic'] = test_basic_for()
    results['break_test'] = test_for_break()
    results['continue_test'] = test_for_continue()
    results['nested'] = test_nested_for()
    results['nested_break'] = test_nested_break()
    results['nested_continue'] = test_nested_continue()
    results['empty'] = test_for_empty()
    results['build_array'] = test_for_build_array()
    return results

test_results = main()

# End of generated code