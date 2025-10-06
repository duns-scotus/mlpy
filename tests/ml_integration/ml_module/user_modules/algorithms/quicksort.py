"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def partition(arr, low, high):
    pivot = arr[high]
    i = (low - 1)
    j = low
    while (j < high):
        if (arr[j] <= pivot):
            i = (i + 1)
            temp = arr[i]
            arr[i] = arr[j]
            arr[j] = temp
        j = (j + 1)
    temp = arr[(i + 1)]
    arr[(i + 1)] = arr[high]
    arr[high] = temp
    return (i + 1)

def quicksort_helper(arr, low, high):
    if (low < high):
        pi = partition(arr, low, high)
        quicksort_helper(arr, low, (pi - 1))
        quicksort_helper(arr, (pi + 1), high)

def quicksort(arr):
    if (_safe_call(builtin.len, arr) <= 1):
        return arr
    quicksort_helper(arr, 0, (_safe_call(builtin.len, arr) - 1))
    return arr

def quicksort_3way(arr, low, high):
    if (low >= high):
        return
    pivot = arr[low]
    lt = low
    gt = high
    i = (low + 1)
    while (i <= gt):
        if (arr[i] < pivot):
            temp = arr[lt]
            arr[lt] = arr[i]
            arr[i] = temp
            lt = (lt + 1)
            i = (i + 1)
        elif (arr[i] > pivot):
            temp = arr[i]
            arr[i] = arr[gt]
            arr[gt] = temp
            gt = (gt - 1)
        else:
            i = (i + 1)
    quicksort_3way(arr, low, (lt - 1))
    quicksort_3way(arr, (gt + 1), high)

def quicksort_with_duplicates(arr):
    if (_safe_call(builtin.len, arr) <= 1):
        return arr
    quicksort_3way(arr, 0, (_safe_call(builtin.len, arr) - 1))
    return arr

# End of generated code