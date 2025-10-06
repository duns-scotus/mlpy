"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_simple_ternary():
    x = 10
    result = 100 if (x > 5) else 200
    return result

def test_ternary_false():
    x = 3
    result = 100 if (x > 5) else 200
    return result

def test_ternary_in_expression():
    x = 7
    result = (10 if (x > 5) else 20 + 5)
    return result

def test_nested_ternary():
    x = 15
    result = 'large' if (x > 20) else 'medium' if (x > 10) else 'small'
    return result

def test_ternary_comparison():
    a = 10
    b = 20
    max = a if (a > b) else b
    return max

def test_ternary_return(x):
    return 'even' if ((x % 2) == 0) else 'odd'

def test_ternary_arrays():
    condition = True
    result = [1, 2, 3] if condition else [4, 5, 6]
    return result

def test_ternary_objects():
    flag = False
    result = {'x': 1, 'y': 2} if flag else {'x': 3, 'y': 4}
    return result

def test_multiple_ternary():
    x = 10
    y = 5
    a = 1 if (x > 5) else 0
    b = 1 if (y > 5) else 0
    return (a + b)

def test_ternary_logical():
    x = 10
    y = 20
    result = 'both' if ((x > 5) and (y > 15)) else 'not both'
    return result

def test_ternary_chain():
    score = 75
    grade = 'A' if (score >= 90) else 'B' if (score >= 80) else 'C' if (score >= 70) else 'D' if (score >= 60) else 'F'
    return grade

def test_ternary_null():
    x = None
    result = 'is null' if (x == None) else 'not null'
    return result

def test_ternary_in_loop():
    arr = [1, 2, 3, 4, 5]
    result = []
    for num in arr:
        val = (num * 2) if ((num % 2) == 0) else (num * 3)
        result = (result + [val])
    return result

def abs_value(x):
    return (0 - x) if (x < 0) else x

def test_abs_value():
    results = {}
    results['positive'] = abs_value(5)
    results['negative'] = abs_value(-5)
    results['zero'] = abs_value(0)
    return results

def min(a, b):
    return a if (a < b) else b

def max(a, b):
    return a if (a > b) else b

def test_min_max():
    results = {}
    results['min_val'] = _safe_call(builtin.min, 10, 20)
    results['max_val'] = _safe_call(builtin.max, 10, 20)
    return results

def main():
    results = {}
    results['simple'] = test_simple_ternary()
    results['false_cond'] = test_ternary_false()
    results['in_expression'] = test_ternary_in_expression()
    results['nested'] = test_nested_ternary()
    results['comparison'] = test_ternary_comparison()
    results['return_even'] = test_ternary_return(10)
    results['return_odd'] = test_ternary_return(7)
    results['arrays'] = test_ternary_arrays()
    results['objects'] = test_ternary_objects()
    results['multiple'] = test_multiple_ternary()
    results['logical'] = test_ternary_logical()
    results['chain'] = test_ternary_chain()
    results['null_check'] = test_ternary_null()
    results['in_loop'] = test_ternary_in_loop()
    results['abs'] = test_abs_value()
    results['minmax'] = test_min_max()
    return results

test_results = main()

# End of generated code