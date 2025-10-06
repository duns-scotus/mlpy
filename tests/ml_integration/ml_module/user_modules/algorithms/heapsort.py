"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def heapify(arr, n, i):
    largest = i
    left = ((2 * i) + 1)
    right = ((2 * i) + 2)
    if (left < n):
        if (arr[left] > arr[largest]):
            largest = left
    if (right < n):
        if (arr[right] > arr[largest]):
            largest = right
    if (largest != i):
        temp = arr[i]
        arr[i] = arr[largest]
        arr[largest] = temp
        heapify(arr, n, largest)

def heapsort(arr):
    n = _safe_call(builtin.len, arr)
    i = (_safe_call(builtin.int, (n / 2)) - 1)
    while (i >= 0):
        heapify(arr, n, i)
        i = (i - 1)
    i = (n - 1)
    while (i > 0):
        temp = arr[0]
        arr[0] = arr[i]
        arr[i] = temp
        heapify(arr, i, 0)
        i = (i - 1)
    return arr

def heapify_min(arr, n, i):
    smallest = i
    left = ((2 * i) + 1)
    right = ((2 * i) + 2)
    if (left < n):
        if (arr[left] < arr[smallest]):
            smallest = left
    if (right < n):
        if (arr[right] < arr[smallest]):
            smallest = right
    if (smallest != i):
        temp = arr[i]
        arr[i] = arr[smallest]
        arr[smallest] = temp
        heapify_min(arr, n, smallest)

def heapsort_descending(arr):
    n = _safe_call(builtin.len, arr)
    i = (_safe_call(builtin.int, (n / 2)) - 1)
    while (i >= 0):
        heapify_min(arr, n, i)
        i = (i - 1)
    i = (n - 1)
    while (i > 0):
        temp = arr[0]
        arr[0] = arr[i]
        arr[i] = temp
        heapify_min(arr, i, 0)
        i = (i - 1)
    return arr

# End of generated code