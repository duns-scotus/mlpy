"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_abs_function():
    results = {}
    results['abs_5'] = _safe_call(builtin.abs, 5)
    results['abs_3_14'] = _safe_call(builtin.abs, 3.14)
    results['abs_neg_5'] = _safe_call(builtin.abs, -5)
    results['abs_neg_3_14'] = _safe_call(builtin.abs, -3.14)
    results['abs_zero'] = _safe_call(builtin.abs, 0)
    results['abs_zero_float'] = _safe_call(builtin.abs, 0.0)
    results['abs_large_pos'] = _safe_call(builtin.abs, 10000)
    results['abs_large_neg'] = _safe_call(builtin.abs, -10000)
    return results

def test_min_function():
    results = {}
    results['min_1_2_3'] = _safe_call(builtin.min, 1, 2, 3)
    results['min_5_2_8'] = _safe_call(builtin.min, 5, 2, 8)
    results['min_neg'] = _safe_call(builtin.min, -5, -2, -8)
    results['min_mixed'] = _safe_call(builtin.min, 10, -5, 0, 3)
    results['min_array_1'] = _safe_call(builtin.min, [3, 1, 4, 1, 5])
    results['min_array_2'] = _safe_call(builtin.min, [10, 20, 5, 15])
    results['min_array_neg'] = _safe_call(builtin.min, [-1, -5, -3])
    results['min_single'] = _safe_call(builtin.min, 42)
    return results

def test_max_function():
    results = {}
    results['max_1_2_3'] = _safe_call(builtin.max, 1, 2, 3)
    results['max_5_2_8'] = _safe_call(builtin.max, 5, 2, 8)
    results['max_neg'] = _safe_call(builtin.max, -5, -2, -8)
    results['max_mixed'] = _safe_call(builtin.max, 10, -5, 0, 3)
    results['max_array_1'] = _safe_call(builtin.max, [3, 1, 4, 1, 5])
    results['max_array_2'] = _safe_call(builtin.max, [10, 20, 5, 15])
    results['max_array_neg'] = _safe_call(builtin.max, [-1, -5, -3])
    results['max_single'] = _safe_call(builtin.max, 42)
    return results

def test_round_function():
    results = {}
    results['round_3_14'] = _safe_call(builtin.round, 3.14)
    results['round_3_5'] = _safe_call(builtin.round, 3.5)
    results['round_2_7'] = _safe_call(builtin.round, 2.7)
    results['round_neg_2_3'] = _safe_call(builtin.round, -2.3)
    results['round_neg_2_7'] = _safe_call(builtin.round, -2.7)
    results['round_3_14159_2'] = _safe_call(builtin.round, 3.14159, 2)
    results['round_2_71828_3'] = _safe_call(builtin.round, 2.71828, 3)
    results['round_123_456_1'] = _safe_call(builtin.round, 123.456, 1)
    results['round_int'] = _safe_call(builtin.round, 42)
    results['round_zero'] = _safe_call(builtin.round, 0)
    return results

def test_math_combinations():
    results = {}
    numbers1 = [-5, -2, -8, -1]
    min_val = _safe_call(builtin.min, numbers1)
    results['abs_min'] = _safe_call(builtin.abs, min_val)
    numbers2 = [-10, -5, -3, -7]
    max_val = _safe_call(builtin.max, numbers2)
    results['abs_max'] = _safe_call(builtin.abs, max_val)
    floats = [3.14, 2.71, 1.41, 2.23]
    max_float = _safe_call(builtin.max, floats)
    results['round_max'] = _safe_call(builtin.round, max_float, 1)
    values = [1, 5, 3, 9, 2, 7]
    min_v = _safe_call(builtin.min, values)
    max_v = _safe_call(builtin.max, values)
    results['range_min_max'] = (max_v - min_v)
    return results

def test_math_in_algorithms():
    results = {}
    x = 10
    y = 15
    diff = _safe_call(builtin.abs, (x - y))
    results['abs_diff'] = diff
    value = 150
    min_bound = 0
    max_bound = 100
    clamped = _safe_call(builtin.max, min_bound, _safe_call(builtin.min, value, max_bound))
    results['clamped'] = clamped
    num = 47
    rounded_tens = (_safe_call(builtin.round, (num / 10)) * 10)
    results['round_tens'] = rounded_tens
    return results

def test_distance_calculation():
    results = {}
    x1 = 5
    x2 = 12
    manhattan = _safe_call(builtin.abs, (x1 - x2))
    results['manhattan_1d'] = manhattan
    values = [-5, 3, -2, 7, -1]
    sum_abs = 0
    for v in values:
        sum_abs = (sum_abs + _safe_call(builtin.abs, v))
    results['sum_abs'] = sum_abs
    return results

def test_statistical_operations():
    results = {}
    data = [23, 45, 12, 67, 34, 89, 11]
    data_min = _safe_call(builtin.min, data)
    data_max = _safe_call(builtin.max, data)
    data_range = (data_max - data_min)
    results['range'] = data_range
    sum_val = 0
    count = _safe_call(builtin.len, data)
    for val in data:
        sum_val = (sum_val + val)
    average = (sum_val / count)
    results['avg_rounded'] = _safe_call(builtin.round, average, 1)
    return results

def main():
    all_results = {}
    all_results['abs_tests'] = test_abs_function()
    all_results['min_tests'] = test_min_function()
    all_results['max_tests'] = test_max_function()
    all_results['round_tests'] = test_round_function()
    all_results['combinations'] = test_math_combinations()
    all_results['algorithms'] = test_math_in_algorithms()
    all_results['distance'] = test_distance_calculation()
    all_results['statistics'] = test_statistical_operations()
    return all_results

test_results = main()

# End of generated code