"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_keys_function():
    results = {}
    obj1 = {'a': 1, 'b': 2, 'c': 3}
    keys1 = _safe_call(builtin.keys, obj1)
    results['keys_abc'] = _safe_call(builtin.sorted, keys1)
    obj2 = {'name': 'Alice', 'age': 30, 'city': 'NYC'}
    keys2 = _safe_call(builtin.keys, obj2)
    results['keys_count'] = _safe_call(builtin.len, keys2)
    obj3 = {}
    keys3 = _safe_call(builtin.keys, obj3)
    results['keys_empty'] = keys3
    obj4 = {'x': 10, 'y': 20, 'z': 30}
    keys4 = _safe_call(builtin.keys, obj4)
    results['keys_xyz'] = _safe_call(builtin.sorted, keys4)
    return results

def test_values_function():
    results = {}
    obj1 = {'a': 1, 'b': 2, 'c': 3}
    vals1 = _safe_call(builtin.values, obj1)
    results['values_123'] = _safe_call(builtin.sorted, vals1)
    obj2 = {'name': 'Bob', 'age': 25, 'active': True}
    vals2 = _safe_call(builtin.values, obj2)
    results['values_count'] = _safe_call(builtin.len, vals2)
    obj3 = {}
    vals3 = _safe_call(builtin.values, obj3)
    results['values_empty'] = vals3
    obj4 = {'a': 10, 'b': 20, 'c': 30, 'd': 40}
    vals4 = _safe_call(builtin.values, obj4)
    sum_vals = 0
    for v in vals4:
        sum_vals = (sum_vals + v)
    results['values_sum'] = sum_vals
    return results

def test_keys_and_values_iteration():
    results = {}
    obj = {'x': 100, 'y': 200, 'z': 300}
    key_list = _safe_call(builtin.keys, obj)
    key_string = ''
    for k in _safe_call(builtin.sorted, key_list):
        key_string = (key_string + k)
    results['key_string'] = key_string
    val_list = _safe_call(builtin.values, obj)
    val_sum = 0
    for v in val_list:
        val_sum = (val_sum + v)
    results['val_sum'] = val_sum
    return results

def test_reconstructing_object():
    results = {}
    original = {'name': 'Alice', 'score': 95, 'passed': True}
    k = _safe_call(builtin.keys, original)
    v = _safe_call(builtin.values, original)
    results['num_keys'] = _safe_call(builtin.len, k)
    results['num_values'] = _safe_call(builtin.len, v)
    pairs = _safe_call(builtin.zip, k, v)
    results['pair_count'] = _safe_call(builtin.len, pairs)
    return results

def test_filtering_by_keys():
    results = {}
    data = {'apple': 10, 'banana': 20, 'avocado': 5, 'cherry': 15}
    all_keys = _safe_call(builtin.keys, data)
    a_keys = []
    for key in all_keys:
        if (_safe_call(builtin.len, key) > 0):
            a_keys = (a_keys + [key])
    results['total_keys'] = _safe_call(builtin.len, all_keys)
    results['filtered_keys'] = _safe_call(builtin.len, a_keys)
    return results

def test_filtering_by_values():
    results = {}
    scores = {'Alice': 85, 'Bob': 92, 'Charlie': 78, 'David': 95, 'Eve': 88}
    all_values = _safe_call(builtin.values, scores)
    high_count = 0
    for val in all_values:
        if (val >= 90):
            high_count = (high_count + 1)
    results['high_scores'] = high_count
    max_score = _safe_call(builtin.max, all_values)
    results['max_score'] = max_score
    min_score = _safe_call(builtin.min, all_values)
    results['min_score'] = min_score
    return results

def test_object_statistics():
    results = {}
    measurements = {'temp1': 72, 'temp2': 75, 'temp3': 68, 'temp4': 71, 'temp5': 74}
    vals = _safe_call(builtin.values, measurements)
    num_measurements = _safe_call(builtin.len, vals)
    total = 0
    for v in vals:
        total = (total + v)
    average = (total / num_measurements)
    results['count'] = num_measurements
    results['total'] = total
    results['average'] = _safe_call(builtin.round, average, 1)
    results['min_temp'] = _safe_call(builtin.min, vals)
    results['max_temp'] = _safe_call(builtin.max, vals)
    return results

def test_keys_values_symmetry():
    results = {}
    obj1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
    k1 = _safe_call(builtin.keys, obj1)
    v1 = _safe_call(builtin.values, obj1)
    results['keys_len'] = _safe_call(builtin.len, k1)
    results['values_len'] = _safe_call(builtin.len, v1)
    results['same_length'] = (_safe_call(builtin.len, k1) == _safe_call(builtin.len, v1))
    obj2 = {}
    k2 = _safe_call(builtin.keys, obj2)
    v2 = _safe_call(builtin.values, obj2)
    results['empty_keys_len'] = _safe_call(builtin.len, k2)
    results['empty_values_len'] = _safe_call(builtin.len, v2)
    results['empty_same'] = (_safe_call(builtin.len, k2) == _safe_call(builtin.len, v2))
    return results

def test_practical_use_cases():
    results = {}
    config = {'timeout': 30, 'retries': 3, 'debug': False, 'port': 8080}
    config_keys = _safe_call(builtin.keys, config)
    config_vals = _safe_call(builtin.values, config)
    results['config_size'] = _safe_call(builtin.len, config_keys)
    user = {'username': 'alice', 'email': 'alice@example.com', 'age': 30, 'active': True, 'role': 'admin'}
    results['user_properties'] = _safe_call(builtin.len, _safe_call(builtin.keys, user))
    inventory = {'item1': 10, 'item2': 25, 'item3': 15, 'item4': 30}
    inv_vals = _safe_call(builtin.values, inventory)
    total_items = 0
    for v in inv_vals:
        total_items = (total_items + v)
    results['total_inventory'] = total_items
    return results

def main():
    all_results = {}
    all_results['keys_tests'] = test_keys_function()
    all_results['values_tests'] = test_values_function()
    all_results['iteration'] = test_keys_and_values_iteration()
    all_results['reconstruct'] = test_reconstructing_object()
    all_results['filter_keys'] = test_filtering_by_keys()
    all_results['filter_values'] = test_filtering_by_values()
    all_results['statistics'] = test_object_statistics()
    all_results['symmetry'] = test_keys_values_symmetry()
    all_results['practical'] = test_practical_use_cases()
    return all_results

test_results = main()

# End of generated code