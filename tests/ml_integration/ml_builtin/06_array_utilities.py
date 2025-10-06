"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_zip_function():
    results = {}
    arr1 = [1, 2, 3]
    arr2 = ['a', 'b', 'c']
    results['zip_nums_letters'] = _safe_call(builtin.zip, arr1, arr2)
    arr3 = [10, 20, 30]
    arr4 = [100, 200, 300]
    arr5 = [1000, 2000, 3000]
    results['zip_three'] = _safe_call(builtin.zip, arr3, arr4, arr5)
    short = [1, 2]
    long = ['a', 'b', 'c', 'd']
    results['zip_different'] = _safe_call(builtin.zip, short, long)
    bools = [True, False, True]
    nums = [1, 0, 1]
    results['zip_bools'] = _safe_call(builtin.zip, bools, nums)
    return results

def test_sorted_function():
    results = {}
    nums1 = [3, 1, 4, 1, 5, 9, 2, 6]
    results['sorted_asc'] = _safe_call(builtin.sorted, nums1)
    nums2 = [3, 1, 4, 1, 5, 9, 2, 6]
    results['sorted_desc'] = _safe_call(builtin.sorted, nums2, True)
    words = ['zebra', 'apple', 'mango', 'banana']
    results['sorted_strings'] = _safe_call(builtin.sorted, words)
    negs = [-5, -1, -3, -2, -4]
    results['sorted_negs'] = _safe_call(builtin.sorted, negs)
    mixed = [3, -1, 4, -2, 0, 5]
    results['sorted_mixed'] = _safe_call(builtin.sorted, mixed)
    floats = [3.14, 2.71, 1.41, 2.23, 0.57]
    results['sorted_floats'] = _safe_call(builtin.sorted, floats)
    results['sorted_empty'] = _safe_call(builtin.sorted, [])
    results['sorted_single'] = _safe_call(builtin.sorted, [42])
    return results

def test_zip_and_iterate():
    results = {}
    names = ['Alice', 'Bob', 'Charlie']
    ages = [30, 25, 35]
    zipped = _safe_call(builtin.zip, names, ages)
    person_info = {}
    for pair in zipped:
        name = pair[0]
        age = pair[1]
        person_info[name] = age
    results['alice_age'] = person_info['Alice']
    results['bob_age'] = person_info['Bob']
    results['charlie_age'] = person_info['Charlie']
    arr_a = [1, 2, 3, 4]
    arr_b = [10, 20, 30, 40]
    zipped2 = _safe_call(builtin.zip, arr_a, arr_b)
    pair_sums = []
    for pair in zipped2:
        sum_val = (pair[0] + pair[1])
        pair_sums = (pair_sums + [sum_val])
    results['pair_sums'] = pair_sums
    return results

def test_sorted_and_process():
    results = {}
    scores = [85, 92, 78, 95, 88]
    sorted_scores = _safe_call(builtin.sorted, scores)
    top_3 = []
    count = 0
    for score in _safe_call(builtin.sorted, scores, True):
        if (count < 3):
            top_3 = (top_3 + [score])
            count = (count + 1)
    results['top_3'] = top_3
    sorted_s = _safe_call(builtin.sorted, scores)
    mid_idx = (_safe_call(builtin.len, sorted_s) // 2)
    results['median'] = sorted_s[mid_idx]
    return results

def test_combining_zip_and_sorted():
    results = {}
    ids = [3, 1, 4, 2]
    names = ['Charlie', 'Alice', 'David', 'Bob']
    pairs = _safe_call(builtin.zip, ids, names)
    results['zipped_pairs'] = pairs
    return results

def test_parallel_arrays():
    results = {}
    quantities = [10, 5, 8, 3]
    prices = [2.5, 5.0, 3.25, 10.0]
    zipped = _safe_call(builtin.zip, quantities, prices)
    costs = []
    for pair in zipped:
        qty = pair[0]
        price = pair[1]
        cost = (qty * price)
        costs = (costs + [cost])
    results['item_costs'] = costs
    total = 0
    for c in costs:
        total = (total + c)
    results['total_cost'] = total
    return results

def test_sorting_for_ranking():
    results = {}
    scores = [85, 95, 78, 92, 88]
    sorted_desc = _safe_call(builtin.sorted, scores, True)
    results['ranked'] = sorted_desc
    position = 0
    for s in sorted_desc:
        position = (position + 1)
        if (s == 88):
            break
    results['score_88_rank'] = position
    return results

def test_edge_cases():
    results = {}
    results['zip_empty_1'] = _safe_call(builtin.zip, [], [1, 2, 3])
    results['zip_empty_2'] = _safe_call(builtin.zip, [1, 2], [])
    results['zip_both_empty'] = _safe_call(builtin.zip, [], [])
    already_sorted = [1, 2, 3, 4, 5]
    results['sort_sorted'] = _safe_call(builtin.sorted, already_sorted)
    reverse_sorted = [5, 4, 3, 2, 1]
    results['sort_reverse'] = _safe_call(builtin.sorted, reverse_sorted)
    dups = [3, 1, 2, 3, 1, 2]
    results['sort_dups'] = _safe_call(builtin.sorted, dups)
    return results

def main():
    all_results = {}
    all_results['zip_tests'] = test_zip_function()
    all_results['sorted_tests'] = test_sorted_function()
    all_results['zip_iterate'] = test_zip_and_iterate()
    all_results['sorted_process'] = test_sorted_and_process()
    all_results['zip_sorted_combo'] = test_combining_zip_and_sorted()
    all_results['parallel_arrays'] = test_parallel_arrays()
    all_results['ranking'] = test_sorting_for_ranking()
    all_results['edge_cases'] = test_edge_cases()
    return all_results

test_results = main()

# End of generated code