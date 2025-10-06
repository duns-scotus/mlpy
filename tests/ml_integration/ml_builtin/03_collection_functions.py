"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_len_function():
    results = {}
    results['len_hello'] = _safe_call(builtin.len, 'hello')
    results['len_empty_str'] = _safe_call(builtin.len, '')
    results['len_long_str'] = _safe_call(builtin.len, 'Hello, World!')
    results['len_array_5'] = _safe_call(builtin.len, [1, 2, 3, 4, 5])
    results['len_empty_array'] = _safe_call(builtin.len, [])
    results['len_nested'] = _safe_call(builtin.len, [[1, 2], [3, 4]])
    results['len_object_2'] = _safe_call(builtin.len, {'a': 1, 'b': 2})
    results['len_empty_obj'] = _safe_call(builtin.len, {})
    results['len_object_5'] = _safe_call(builtin.len, {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})
    return results

def test_range_function():
    results = {}
    results['range_5'] = _safe_call(builtin.range, 5)
    results['range_3'] = _safe_call(builtin.range, 3)
    results['range_0'] = _safe_call(builtin.range, 0)
    results['range_1'] = _safe_call(builtin.range, 1)
    results['range_1_5'] = _safe_call(builtin.range, 1, 5)
    results['range_3_7'] = _safe_call(builtin.range, 3, 7)
    results['range_0_10'] = _safe_call(builtin.range, 0, 10)
    results['range_0_10_2'] = _safe_call(builtin.range, 0, 10, 2)
    results['range_1_10_3'] = _safe_call(builtin.range, 1, 10, 3)
    results['range_0_20_5'] = _safe_call(builtin.range, 0, 20, 5)
    return results

def test_enumerate_function():
    results = {}
    arr1 = ['a', 'b', 'c']
    results['enum_abc'] = _safe_call(builtin.enumerate, arr1)
    arr2 = ['x', 'y', 'z']
    results['enum_xyz_from_1'] = _safe_call(builtin.enumerate, arr2, 1)
    results['enum_empty'] = _safe_call(builtin.enumerate, [])
    arr3 = [10, 20, 30, 40]
    results['enum_numbers'] = _safe_call(builtin.enumerate, arr3)
    return results

def test_len_in_loops():
    results = {}
    arr = [10, 20, 30, 40, 50]
    arr_len = _safe_call(builtin.len, arr)
    sum = 0
    i = 0
    while (i < arr_len):
        sum = (sum + arr[i])
        i = (i + 1)
    results['sum_using_len'] = sum
    results['array_length'] = arr_len
    str = 'hello'
    str_len = _safe_call(builtin.len, str)
    results['string_length'] = str_len
    return results

def test_range_in_loops():
    results = {}
    sum = 0
    for i in _safe_call(builtin.range, 10):
        sum = (sum + i)
    results['sum_0_to_9'] = sum
    squares = []
    for n in _safe_call(builtin.range, 1, 6):
        squares = (squares + [(n * n)])
    results['squares_1_to_5'] = squares
    evens = []
    for n in _safe_call(builtin.range, 0, 10, 2):
        evens = (evens + [n])
    results['evens_0_to_8'] = evens
    return results

def test_enumerate_in_loops():
    results = {}
    fruits = ['apple', 'banana', 'cherry']
    fruit_map = {}
    for pair in _safe_call(builtin.enumerate, fruits):
        idx = pair[0]
        fruit = pair[1]
        fruit_map[idx] = fruit
    results['fruit_0'] = fruit_map[0]
    results['fruit_1'] = fruit_map[1]
    results['fruit_2'] = fruit_map[2]
    numbers = [5, 10, 15, 20, 25]
    target = 15
    found_index = -1
    for pair in _safe_call(builtin.enumerate, numbers):
        idx = pair[0]
        val = pair[1]
        if (val == target):
            found_index = idx
    results['found_index'] = found_index
    return results

def test_combined_functions():
    results = {}
    r = _safe_call(builtin.range, 10, 20)
    results['range_len'] = _safe_call(builtin.len, r)
    arr = ['a', 'b', 'c', 'd']
    enum_arr = _safe_call(builtin.enumerate, arr)
    results['enum_len'] = _safe_call(builtin.len, enum_arr)
    r2 = _safe_call(builtin.range, 5)
    enum_r2 = _safe_call(builtin.enumerate, r2)
    results['enum_range_len'] = _safe_call(builtin.len, enum_r2)
    return results

def main():
    all_results = {}
    all_results['len_tests'] = test_len_function()
    all_results['range_tests'] = test_range_function()
    all_results['enumerate_tests'] = test_enumerate_function()
    all_results['len_loops'] = test_len_in_loops()
    all_results['range_loops'] = test_range_in_loops()
    all_results['enum_loops'] = test_enumerate_in_loops()
    all_results['combined'] = test_combined_functions()
    return all_results

test_results = main()

# End of generated code