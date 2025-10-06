"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

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

# End of generated code