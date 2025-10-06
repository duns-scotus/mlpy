"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_sum_integers():
    results = {}
    results['sum_1_to_5'] = _safe_call(builtin.sum, [1, 2, 3, 4, 5])
    results['sum_evens'] = _safe_call(builtin.sum, [2, 4, 6, 8, 10])
    results['sum_with_neg'] = _safe_call(builtin.sum, [10, -5, 3, -2])
    results['sum_all_neg'] = _safe_call(builtin.sum, [-1, -2, -3, -4])
    results['sum_with_zero'] = _safe_call(builtin.sum, [1, 0, 2, 0, 3])
    results['sum_only_zeros'] = _safe_call(builtin.sum, [0, 0, 0])
    results['sum_empty'] = _safe_call(builtin.sum, [])
    results['sum_single'] = _safe_call(builtin.sum, [42])
    return results

def test_sum_floats():
    results = {}
    results['sum_floats'] = _safe_call(builtin.sum, [1.5, 2.5, 3.0])
    results['sum_decimals'] = _safe_call(builtin.sum, [0.1, 0.2, 0.3])
    results['sum_mixed'] = _safe_call(builtin.sum, [1, 2.5, 3, 4.5])
    return results

def test_sum_with_start():
    results = {}
    results['sum_start_10'] = _safe_call(builtin.sum, [1, 2, 3], 10)
    results['sum_start_100'] = _safe_call(builtin.sum, [5, 10, 15], 100)
    results['sum_start_neg'] = _safe_call(builtin.sum, [10, 20], -5)
    results['sum_start_float'] = _safe_call(builtin.sum, [1, 2, 3], 0.5)
    return results

def test_sum_in_calculations():
    results = {}
    values = [10, 20, 30, 40, 50]
    total = _safe_call(builtin.sum, values)
    count = _safe_call(builtin.len, values)
    average = (total / count)
    results['total'] = total
    results['count'] = count
    results['average'] = average
    scores = [85, 90, 95]
    total_score = _safe_call(builtin.sum, scores)
    max_possible = (100 * _safe_call(builtin.len, scores))
    percentage = ((total_score / max_possible) * 100)
    results['total_score'] = total_score
    results['percentage'] = _safe_call(builtin.round, percentage, 1)
    return results

def test_sum_with_filtering():
    results = {}
    numbers = [5, -3, 8, -2, 10, -1]
    positives = []
    for n in numbers:
        if (n > 0):
            positives = (positives + [n])
    results['sum_positives'] = _safe_call(builtin.sum, positives)
    numbers2 = [1, 2, 3, 4, 5, 6, 7, 8]
    evens = []
    for n in numbers2:
        if ((n - ((n / 2) * 2)) == 0):
            evens = (evens + [n])
    results['sum_evens'] = _safe_call(builtin.sum, evens)
    return results

def test_sum_in_loops():
    results = {}
    values = [1, 2, 3, 4, 5]
    cumulative = []
    for i in _safe_call(builtin.range, _safe_call(builtin.len, values)):
        slice_vals = []
        for j in _safe_call(builtin.range, (i + 1)):
            slice_vals = (slice_vals + [values[j]])
        cumulative = (cumulative + [_safe_call(builtin.sum, slice_vals)])
    results['cumulative'] = cumulative
    return results

def test_sum_for_statistics():
    results = {}
    data = [10, 12, 14, 16, 18]
    total = _safe_call(builtin.sum, data)
    count = _safe_call(builtin.len, data)
    mean = (total / count)
    results['mean'] = mean
    squared_diffs = []
    for val in data:
        diff = (val - mean)
        squared_diffs = (squared_diffs + [(diff * diff)])
    sum_squared_diffs = _safe_call(builtin.sum, squared_diffs)
    results['sum_squared_diffs'] = sum_squared_diffs
    return results

def test_sum_with_transformations():
    results = {}
    numbers = [1, 2, 3, 4, 5]
    squares = []
    for n in numbers:
        squares = (squares + [(n * n)])
    results['sum_of_squares'] = _safe_call(builtin.sum, squares)
    values = [-5, 3, -2, 7, -1]
    abs_values = []
    for v in values:
        abs_values = (abs_values + [_safe_call(builtin.abs, v)])
    results['sum_of_abs'] = _safe_call(builtin.sum, abs_values)
    return results

def test_sum_edge_cases():
    results = {}
    large_nums = []
    for i in _safe_call(builtin.range, 100):
        large_nums = (large_nums + [100])
    results['large_sum'] = _safe_call(builtin.sum, large_nums)
    results['single_large'] = _safe_call(builtin.sum, [1000000])
    results['mixed_scale'] = _safe_call(builtin.sum, [1000000, 1, 2, 3])
    return results

def test_practical_use_cases():
    results = {}
    prices = [19.99, 24.99, 9.99, 15.0]
    subtotal = _safe_call(builtin.sum, prices)
    tax = (subtotal * 0.08)
    total = (subtotal + tax)
    results['subtotal'] = _safe_call(builtin.round, subtotal, 2)
    results['total'] = _safe_call(builtin.round, total, 2)
    assignments = [85, 90, 88, 92]
    midterm = 78
    final = 85
    assignment_avg = (_safe_call(builtin.sum, assignments) / _safe_call(builtin.len, assignments))
    overall = (((assignment_avg * 0.5) + (midterm * 0.25)) + (final * 0.25))
    results['assignment_avg'] = _safe_call(builtin.round, assignment_avg, 1)
    results['overall'] = _safe_call(builtin.round, overall, 1)
    return results

def main():
    all_results = {}
    all_results['integers'] = test_sum_integers()
    all_results['floats'] = test_sum_floats()
    all_results['with_start'] = test_sum_with_start()
    all_results['calculations'] = test_sum_in_calculations()
    all_results['filtering'] = test_sum_with_filtering()
    all_results['loops'] = test_sum_in_loops()
    all_results['statistics'] = test_sum_for_statistics()
    all_results['transformations'] = test_sum_with_transformations()
    all_results['edge_cases'] = test_sum_edge_cases()
    all_results['practical'] = test_practical_use_cases()
    return all_results

test_results = main()

# End of generated code