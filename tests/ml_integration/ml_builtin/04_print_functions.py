"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_print_numbers():
    results = {}
    _safe_call(builtin.print, 42)
    _safe_call(builtin.print, 0)
    _safe_call(builtin.print, -100)
    _safe_call(builtin.print, 3.14)
    _safe_call(builtin.print, 0.0)
    _safe_call(builtin.print, -2.5)
    results['printed_numbers'] = True
    return results

def test_print_booleans():
    results = {}
    _safe_call(builtin.print, True)
    _safe_call(builtin.print, False)
    results['printed_booleans'] = True
    return results

def test_print_strings():
    results = {}
    _safe_call(builtin.print, 'Hello, World!')
    _safe_call(builtin.print, '')
    _safe_call(builtin.print, 'ML is awesome')
    results['printed_strings'] = True
    return results

def test_print_arrays():
    results = {}
    _safe_call(builtin.print, [1, 2, 3, 4, 5])
    _safe_call(builtin.print, [])
    _safe_call(builtin.print, ['a', 'b', 'c'])
    _safe_call(builtin.print, [True, False])
    results['printed_arrays'] = True
    return results

def test_print_objects():
    results = {}
    _safe_call(builtin.print, {'a': 1, 'b': 2})
    _safe_call(builtin.print, {})
    _safe_call(builtin.print, {'name': 'Alice', 'age': 30})
    results['printed_objects'] = True
    return results

def test_print_multiple_values():
    results = {}
    _safe_call(builtin.print, 'Number:', 42)
    _safe_call(builtin.print, 'Boolean:', True)
    _safe_call(builtin.print, 'String:', 'hello')
    _safe_call(builtin.print, 'Array:', [1, 2, 3])
    _safe_call(builtin.print, 'Object:', {'x': 10, 'y': 20})
    results['printed_multiple'] = True
    return results

def test_print_computations():
    results = {}
    _safe_call(builtin.print, '2 + 2 =', (2 + 2))
    _safe_call(builtin.print, '10 * 5 =', (10 * 5))
    _safe_call(builtin.print, '100 / 4 =', (100 / 4))
    x = 10
    y = 20
    _safe_call(builtin.print, 'x + y =', (x + y))
    results['printed_computations'] = True
    return results

def test_print_in_loops():
    results = {}
    for i in _safe_call(builtin.range, 1, 6):
        _safe_call(builtin.print, 'Number:', i)
    fruits = ['apple', 'banana', 'cherry']
    for fruit in fruits:
        _safe_call(builtin.print, 'Fruit:', fruit)
    results['printed_in_loops'] = True
    return results

def test_print_conditionals():
    results = {}
    x = 10
    if (x > 0):
        _safe_call(builtin.print, 'x is positive')
    elif (x < 0):
        _safe_call(builtin.print, 'x is negative')
    else:
        _safe_call(builtin.print, 'x is zero')
    value = 42
    t = _safe_call(builtin.typeof, value)
    _safe_call(builtin.print, 'Type of', value, 'is', t)
    results['printed_conditionals'] = True
    return results

def test_print_formatted_output():
    results = {}
    name = 'Alice'
    age = 30
    _safe_call(builtin.print, 'Name:', name, 'Age:', age)
    _safe_call(builtin.print, 'ID | Name  | Value')
    _safe_call(builtin.print, '1  | Item1 | 100')
    _safe_call(builtin.print, '2  | Item2 | 200')
    for i in _safe_call(builtin.range, 5):
        _safe_call(builtin.print, 'Progress:', (i + 1), '/ 5')
    results['printed_formatted'] = True
    return results

def main():
    all_results = {}
    _safe_call(builtin.print, '=== Builtin Print Function Tests ===')
    _safe_call(builtin.print, '')
    _safe_call(builtin.print, 'Test 1: Printing numbers')
    all_results['numbers'] = test_print_numbers()
    _safe_call(builtin.print, '')
    _safe_call(builtin.print, 'Test 2: Printing booleans')
    all_results['booleans'] = test_print_booleans()
    _safe_call(builtin.print, '')
    _safe_call(builtin.print, 'Test 3: Printing strings')
    all_results['strings'] = test_print_strings()
    _safe_call(builtin.print, '')
    _safe_call(builtin.print, 'Test 4: Printing arrays')
    all_results['arrays'] = test_print_arrays()
    _safe_call(builtin.print, '')
    _safe_call(builtin.print, 'Test 5: Printing objects')
    all_results['objects'] = test_print_objects()
    _safe_call(builtin.print, '')
    _safe_call(builtin.print, 'Test 6: Printing multiple values')
    all_results['multiple'] = test_print_multiple_values()
    _safe_call(builtin.print, '')
    _safe_call(builtin.print, 'Test 7: Printing computations')
    all_results['computations'] = test_print_computations()
    _safe_call(builtin.print, '')
    _safe_call(builtin.print, 'Test 8: Printing in loops')
    all_results['loops'] = test_print_in_loops()
    _safe_call(builtin.print, '')
    _safe_call(builtin.print, 'Test 9: Printing with conditionals')
    all_results['conditionals'] = test_print_conditionals()
    _safe_call(builtin.print, '')
    _safe_call(builtin.print, 'Test 10: Formatted output')
    all_results['formatted'] = test_print_formatted_output()
    _safe_call(builtin.print, '')
    _safe_call(builtin.print, '=== All Tests Complete ===')
    return all_results

test_results = main()

# End of generated code