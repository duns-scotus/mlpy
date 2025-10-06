"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

# ============================================================================
# User Module Definitions (Inline)
# ============================================================================

# Module: user_modules.sorting
class user_modules:
    sorting = None
# --- Begin User Module: user_modules.sorting ---
class user_modules_sorting:
    def swap(arr, i, j):
        temp = arr[i]
        arr[i] = arr[j]
        arr[j] = temp
    def is_sorted(arr):
        i = 0
        while (i < (_safe_call(builtin.len, arr) - 1)):
            if (arr[i] > arr[(i + 1)]):
                return False
            i = (i + 1)
        return True
    def find_min(arr):
        if (_safe_call(builtin.len, arr) == 0):
            return None
        min_val = arr[0]
        i = 1
        while (i < _safe_call(builtin.len, arr)):
            if (arr[i] < min_val):
                min_val = arr[i]
            i = (i + 1)
        return min_val
    def find_max(arr):
        if (_safe_call(builtin.len, arr) == 0):
            return None
        max_val = arr[0]
        i = 1
        while (i < _safe_call(builtin.len, arr)):
            if (arr[i] > max_val):
                max_val = arr[i]
            i = (i + 1)
        return max_val
    def selection_sort(arr):
        n = _safe_call(builtin.len, arr)
        i = 0
        while (i < (n - 1)):
            min_idx = i
            j = (i + 1)
            while (j < n):
                if (arr[j] < arr[min_idx]):
                    min_idx = j
                j = (j + 1)
            if (min_idx != i):
                swap(arr, i, min_idx)
            i = (i + 1)
        return arr
    def reverse(arr):
        left = 0
        right = (_safe_call(builtin.len, arr) - 1)
        while (left < right):
            swap(arr, left, right)
            left = (left + 1)
            right = (right - 1)
        return arr
    def sort_descending(arr):
        selection_sort(arr)
        return reverse(arr)
# --- End User Module: user_modules.sorting ---

user_modules_sorting = user_modules_sorting()
user_modules = user_modules()
user_modules.sorting = user_modules_sorting

# ============================================================================
# Main Program Code
# ============================================================================


def test_is_sorted():
    sorted_arr = [1, 2, 3, 4, 5]
    unsorted_arr = [5, 2, 8, 1, 9]
    result1 = _safe_method_call(_safe_attr_access(user_modules, 'sorting'), 'is_sorted', sorted_arr)
    result2 = _safe_method_call(_safe_attr_access(user_modules, 'sorting'), 'is_sorted', unsorted_arr)
    _safe_call(builtin.print, 'Testing is_sorted:')
    _safe_call(builtin.print, (str('  Sorted array [1,2,3,4,5]: ') + str(_safe_call(builtin.str, result1))))
    _safe_call(builtin.print, (str('  Unsorted array [5,2,8,1,9]: ') + str(_safe_call(builtin.str, result2))))
    if (result1 == True):
        if (result2 == False):
            return True
    return False

def test_find_min_max():
    arr = [5, 2, 8, 1, 9, 3]
    min_val = _safe_method_call(_safe_attr_access(user_modules, 'sorting'), 'find_min', arr)
    max_val = _safe_method_call(_safe_attr_access(user_modules, 'sorting'), 'find_max', arr)
    _safe_call(builtin.print, 'Testing find_min and find_max:')
    _safe_call(builtin.print, '  Array: [5, 2, 8, 1, 9, 3]')
    _safe_call(builtin.print, (str('  Min: ') + str(_safe_call(builtin.str, min_val))))
    _safe_call(builtin.print, (str('  Max: ') + str(_safe_call(builtin.str, max_val))))
    if (min_val == 1):
        if (max_val == 9):
            return True
    return False

def test_selection_sort():
    arr = [64, 25, 12, 22, 11]
    _safe_call(builtin.print, 'Testing selection_sort:')
    _safe_call(builtin.print, '  Before: [64, 25, 12, 22, 11]')
    sorted_arr = _safe_method_call(_safe_attr_access(user_modules, 'sorting'), 'selection_sort', arr)
    _safe_call(builtin.print, (str('  After: ') + str(_safe_call(builtin.str, sorted_arr))))
    is_sorted = _safe_method_call(_safe_attr_access(user_modules, 'sorting'), 'is_sorted', sorted_arr)
    if (is_sorted == True):
        if (sorted_arr[0] == 11):
            if (sorted_arr[4] == 64):
                return True
    return False

def test_reverse():
    arr = [1, 2, 3, 4, 5]
    _safe_call(builtin.print, 'Testing reverse:')
    _safe_call(builtin.print, '  Before: [1, 2, 3, 4, 5]')
    reversed_arr = _safe_method_call(_safe_attr_access(user_modules, 'sorting'), 'reverse', arr)
    _safe_call(builtin.print, (str('  After: ') + str(_safe_call(builtin.str, reversed_arr))))
    if (reversed_arr[0] == 5):
        if (reversed_arr[4] == 1):
            return True
    return False

def test_sort_descending():
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    _safe_call(builtin.print, 'Testing sort_descending:')
    _safe_call(builtin.print, '  Before: [3, 1, 4, 1, 5, 9, 2, 6]')
    sorted_arr = _safe_method_call(_safe_attr_access(user_modules, 'sorting'), 'sort_descending', arr)
    _safe_call(builtin.print, (str('  After: ') + str(_safe_call(builtin.str, sorted_arr))))
    if (sorted_arr[0] == 9):
        if (sorted_arr[(_safe_call(builtin.len, sorted_arr) - 1)] == 1):
            return True
    return False

def main():
    _safe_call(builtin.print, '===== User Module Test: sorting.ml =====')
    _safe_call(builtin.print, '')
    test1 = test_is_sorted()
    _safe_call(builtin.print, (str('Test 1 (is_sorted): ') + str(_safe_call(builtin.str, test1))))
    _safe_call(builtin.print, '')
    test2 = test_find_min_max()
    _safe_call(builtin.print, (str('Test 2 (find_min_max): ') + str(_safe_call(builtin.str, test2))))
    _safe_call(builtin.print, '')
    test3 = test_selection_sort()
    _safe_call(builtin.print, (str('Test 3 (selection_sort): ') + str(_safe_call(builtin.str, test3))))
    _safe_call(builtin.print, '')
    test4 = test_reverse()
    _safe_call(builtin.print, (str('Test 4 (reverse): ') + str(_safe_call(builtin.str, test4))))
    _safe_call(builtin.print, '')
    test5 = test_sort_descending()
    _safe_call(builtin.print, (str('Test 5 (sort_descending): ') + str(_safe_call(builtin.str, test5))))
    _safe_call(builtin.print, '')
    passed = 0
    if test1:
        passed = (passed + 1)
    if test2:
        passed = (passed + 1)
    if test3:
        passed = (passed + 1)
    if test4:
        passed = (passed + 1)
    if test5:
        passed = (passed + 1)
    _safe_call(builtin.print, '===== Summary =====')
    _safe_call(builtin.print, (str((str('Tests passed: ') + str(_safe_call(builtin.str, passed)))) + str('/5')))
    if (passed == 5):
        _safe_call(builtin.print, 'All tests PASSED!')
        return 0
    else:
        _safe_call(builtin.print, 'Some tests FAILED!')
        return 1

main()

# End of generated code