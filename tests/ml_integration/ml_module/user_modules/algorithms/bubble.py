"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def bubble_sort(arr):
    n = _safe_call(builtin.len, arr)
    i = 0
    while (i < (n - 1)):
        j = 0
        swapped = False
        while (j < ((n - i) - 1)):
            if (arr[j] > arr[(j + 1)]):
                temp = arr[j]
                arr[j] = arr[(j + 1)]
                arr[(j + 1)] = temp
                swapped = True
            j = (j + 1)
        if (swapped == False):
            return arr
        i = (i + 1)
    return arr

def bubble_sort_optimized(arr):
    n = _safe_call(builtin.len, arr)
    i = 0
    while (i < (n - 1)):
        last_swap = 0
        j = 0
        while (j < ((n - i) - 1)):
            if (arr[j] > arr[(j + 1)]):
                temp = arr[j]
                arr[j] = arr[(j + 1)]
                arr[(j + 1)] = temp
                last_swap = j
            j = (j + 1)
        if (last_swap == 0):
            return arr
        i = (i + 1)
    return arr

# End of generated code