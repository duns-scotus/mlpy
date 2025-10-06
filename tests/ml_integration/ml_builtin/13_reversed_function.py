"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_reversed_arrays():
    results = {}
    results['reversed_123'] = _safe_call(builtin.reversed, [1, 2, 3])
    results['reversed_5'] = _safe_call(builtin.reversed, [1, 2, 3, 4, 5])
    results['reversed_strings'] = _safe_call(builtin.reversed, ['a', 'b', 'c'])
    results['reversed_mixed'] = _safe_call(builtin.reversed, [1, 'a', 2, 'b'])
    results['reversed_single'] = _safe_call(builtin.reversed, [42])
    results['reversed_empty'] = _safe_call(builtin.reversed, [])
    return results

def test_reversed_strings():
    results = {}
    results['reversed_hello'] = _safe_call(builtin.reversed, 'hello')
    results['reversed_abc'] = _safe_call(builtin.reversed, 'abc')
    results['reversed_single_char'] = _safe_call(builtin.reversed, 'x')
    results['reversed_empty_str'] = _safe_call(builtin.reversed, '')
    return results

def test_reversed_with_iteration():
    results = {}
    numbers = [10, 20, 30, 40, 50]
    reversed_nums = _safe_call(builtin.reversed, numbers)
    sum_reversed = 0
    for n in reversed_nums:
        sum_reversed = (sum_reversed + n)
    results['sum'] = sum_reversed
    results['reversed_order'] = reversed_nums
    return results

def test_reversed_for_palindrome_check():
    results = {}
    arr1 = [1, 2, 3, 2, 1]
    arr1_rev = _safe_call(builtin.reversed, arr1)
    is_palindrome = True
    for i in _safe_call(builtin.range, _safe_call(builtin.len, arr1)):
        if (arr1[i] != arr1_rev[i]):
            is_palindrome = False
    results['palindrome_check'] = is_palindrome
    arr2 = [1, 2, 3, 4, 5]
    arr2_rev = _safe_call(builtin.reversed, arr2)
    is_palindrome2 = True
    for i in _safe_call(builtin.range, _safe_call(builtin.len, arr2)):
        if (arr2[i] != arr2_rev[i]):
            is_palindrome2 = False
    results['non_palindrome'] = is_palindrome2
    return results

def test_reversed_with_sorting():
    results = {}
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_nums = _safe_call(builtin.sorted, nums)
    descending = _safe_call(builtin.reversed, sorted_nums)
    results['descending'] = descending
    results['first'] = descending[0]
    results['last'] = descending[(_safe_call(builtin.len, descending) - 1)]
    return results

def test_reversed_for_stack_operations():
    results = {}
    stack = [1, 2, 3, 4, 5]
    reversed_stack = _safe_call(builtin.reversed, stack)
    top_element = reversed_stack[0]
    results['top'] = top_element
    processed = []
    for item in reversed_stack:
        processed = (processed + [(item * 2)])
    results['processed'] = processed
    return results

def test_reversed_with_range():
    results = {}
    r = _safe_call(builtin.range, 1, 11)
    countdown = _safe_call(builtin.reversed, r)
    results['countdown'] = countdown
    results['start'] = countdown[0]
    results['end'] = countdown[(_safe_call(builtin.len, countdown) - 1)]
    return results

def test_reversed_for_queue_reversal():
    results = {}
    queue = ['first', 'second', 'third', 'fourth']
    reversed_queue = _safe_call(builtin.reversed, queue)
    results['original_first'] = queue[0]
    results['reversed_first'] = reversed_queue[0]
    results['queue_len'] = _safe_call(builtin.len, queue)
    results['reversed_len'] = _safe_call(builtin.len, reversed_queue)
    return results

def test_reversed_twice():
    results = {}
    original = [1, 2, 3, 4, 5]
    once = _safe_call(builtin.reversed, original)
    twice = _safe_call(builtin.reversed, once)
    results['original'] = original
    results['once'] = once
    results['twice'] = twice
    matches = True
    for i in _safe_call(builtin.range, _safe_call(builtin.len, original)):
        if (original[i] != twice[i]):
            matches = False
    results['matches_original'] = matches
    return results

def test_reversed_nested_arrays():
    results = {}
    nested = [[1, 2], [3, 4], [5, 6]]
    reversed_nested = _safe_call(builtin.reversed, nested)
    results['first_subarray'] = reversed_nested[0]
    results['last_subarray'] = reversed_nested[2]
    return results

def test_reversed_practical_uses():
    results = {}
    history = ['page1', 'page2', 'page3', 'page4', 'page5']
    recent_first = _safe_call(builtin.reversed, history)
    results['most_recent'] = recent_first[0]
    results['oldest'] = recent_first[(_safe_call(builtin.len, recent_first) - 1)]
    actions = ['action1', 'action2', 'action3']
    undo_order = _safe_call(builtin.reversed, actions)
    results['last_action'] = undo_order[0]
    frames = [0, 1, 2, 3, 4]
    reverse_frames = _safe_call(builtin.reversed, frames)
    results['frame_count'] = _safe_call(builtin.len, reverse_frames)
    results['first_frame'] = reverse_frames[0]
    return results

def main():
    all_results = {}
    all_results['arrays'] = test_reversed_arrays()
    all_results['strings'] = test_reversed_strings()
    all_results['iteration'] = test_reversed_with_iteration()
    all_results['palindrome'] = test_reversed_for_palindrome_check()
    all_results['sorting'] = test_reversed_with_sorting()
    all_results['stack'] = test_reversed_for_stack_operations()
    all_results['range_rev'] = test_reversed_with_range()
    all_results['queue'] = test_reversed_for_queue_reversal()
    all_results['twice'] = test_reversed_twice()
    all_results['nested'] = test_reversed_nested_arrays()
    all_results['practical'] = test_reversed_practical_uses()
    return all_results

test_results = main()

# End of generated code