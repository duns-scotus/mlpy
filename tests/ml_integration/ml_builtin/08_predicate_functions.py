"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_callable_function():
    results = {}
    results['func_is_callable'] = _safe_call(builtin.callable, test_callable_function)
    results['int_not_callable'] = _safe_call(builtin.callable, 42)
    results['str_not_callable'] = _safe_call(builtin.callable, 'hello')
    results['array_not_callable'] = _safe_call(builtin.callable, [1, 2, 3])
    results['obj_not_callable'] = _safe_call(builtin.callable, {'a': 1})
    results['bool_not_callable'] = _safe_call(builtin.callable, True)
    return results

def test_all_function():
    results = {}
    results['all_true'] = _safe_call(builtin.all, [True, True, True])
    results['all_numbers'] = _safe_call(builtin.all, [1, 2, 3, 4, 5])
    results['all_strings'] = _safe_call(builtin.all, ['a', 'b', 'c'])
    results['one_false'] = _safe_call(builtin.all, [True, False, True])
    results['one_zero'] = _safe_call(builtin.all, [1, 2, 0, 4])
    results['one_empty_str'] = _safe_call(builtin.all, ['a', '', 'c'])
    results['all_empty'] = _safe_call(builtin.all, [])
    results['all_single_true'] = _safe_call(builtin.all, [True])
    results['all_single_false'] = _safe_call(builtin.all, [False])
    return results

def test_any_function():
    results = {}
    results['one_true'] = _safe_call(builtin.any, [False, False, True])
    results['one_number'] = _safe_call(builtin.any, [0, 0, 1])
    results['one_string'] = _safe_call(builtin.any, ['', '', 'a'])
    results['all_false'] = _safe_call(builtin.any, [False, False, False])
    results['all_zeros'] = _safe_call(builtin.any, [0, 0, 0])
    results['all_empty_strs'] = _safe_call(builtin.any, ['', '', ''])
    results['all_true'] = _safe_call(builtin.any, [True, True, True])
    results['all_numbers'] = _safe_call(builtin.any, [1, 2, 3])
    results['any_empty'] = _safe_call(builtin.any, [])
    results['any_single_true'] = _safe_call(builtin.any, [True])
    results['any_single_false'] = _safe_call(builtin.any, [False])
    return results

def test_all_with_mixed_types():
    results = {}
    results['mixed_truthy'] = _safe_call(builtin.all, [1, 'hello', True, [1]])
    results['mixed_with_zero'] = _safe_call(builtin.all, [1, 'hello', 0])
    results['mixed_with_empty_str'] = _safe_call(builtin.all, [1, '', True])
    results['mixed_with_false'] = _safe_call(builtin.all, [1, 'x', False])
    results['mixed_with_empty_arr'] = _safe_call(builtin.all, [1, 'x', []])
    return results

def test_any_with_mixed_types():
    results = {}
    results['one_truthy'] = _safe_call(builtin.any, [0, '', False, [], 1])
    results['all_falsy'] = _safe_call(builtin.any, [0, '', False, []])
    return results

def test_all_in_validation():
    results = {}
    numbers1 = [5, 10, 15, 20]
    checks1 = []
    for n in numbers1:
        checks1 = (checks1 + [(n > 0)])
    results['all_positive'] = _safe_call(builtin.all, checks1)
    numbers2 = [2, 4, 6, 8]
    checks2 = []
    for n in numbers2:
        is_even = ((n - ((n / 2) * 2)) == 0)
        checks2 = (checks2 + [is_even])
    results['all_even'] = _safe_call(builtin.all, checks2)
    numbers3 = [2, 4, 5, 8]
    checks3 = []
    for n in numbers3:
        is_even = ((n - ((n / 2) * 2)) == 0)
        checks3 = (checks3 + [is_even])
    results['not_all_even'] = _safe_call(builtin.all, checks3)
    return results

def test_any_in_search():
    results = {}
    numbers1 = [1, 2, 3, 4, 5]
    target1 = 3
    matches1 = []
    for n in numbers1:
        matches1 = (matches1 + [(n == target1)])
    results['found_3'] = _safe_call(builtin.any, matches1)
    numbers2 = [1, 2, 4, 5]
    target2 = 3
    matches2 = []
    for n in numbers2:
        matches2 = (matches2 + [(n == target2)])
    results['not_found_3'] = _safe_call(builtin.any, matches2)
    values = [5, 3, 2, 1, 8]
    threshold = 7
    checks = []
    for v in values:
        checks = (checks + [(v > threshold)])
    results['any_above_threshold'] = _safe_call(builtin.any, checks)
    return results

def test_combining_all_and_any():
    results = {}
    values = [2, 4, 6, 8]
    all_positive = True
    for v in values:
        if (v <= 0):
            all_positive = False
    any_above_5 = False
    for v in values:
        if (v > 5):
            any_above_5 = True
    results['all_pos_and_any_high'] = (all_positive and any_above_5)
    return results

def test_short_circuit_behavior():
    results = {}
    large_list = []
    for i in _safe_call(builtin.range, 1000):
        large_list = (large_list + [True])
    large_list = (large_list + [False])
    results['all_with_false_at_end'] = _safe_call(builtin.all, large_list)
    large_list2 = []
    for i in _safe_call(builtin.range, 1000):
        large_list2 = (large_list2 + [False])
    large_list2 = ([True] + large_list2)
    results['any_with_true_at_start'] = _safe_call(builtin.any, large_list2)
    return results

def test_practical_use_cases():
    results = {}
    username = 'alice'
    password = 'pass123'
    email = 'alice@example.com'
    validations = [(_safe_call(builtin.len, username) > 0), (_safe_call(builtin.len, password) >= 6), (_safe_call(builtin.len, email) > 0)]
    results['form_valid'] = _safe_call(builtin.all, validations)
    errors = [False, False, False, False]
    results['has_errors'] = _safe_call(builtin.any, errors)
    errors_with_one = [False, True, False]
    results['has_errors_2'] = _safe_call(builtin.any, errors_with_one)
    return results

def main():
    all_results = {}
    all_results['callable_tests'] = test_callable_function()
    all_results['all_tests'] = test_all_function()
    all_results['any_tests'] = test_any_function()
    all_results['all_mixed'] = test_all_with_mixed_types()
    all_results['any_mixed'] = test_any_with_mixed_types()
    all_results['validation'] = test_all_in_validation()
    all_results['search'] = test_any_in_search()
    all_results['combining'] = test_combining_all_and_any()
    all_results['short_circuit'] = test_short_circuit_behavior()
    all_results['practical'] = test_practical_use_cases()
    return all_results

test_results = main()

# End of generated code