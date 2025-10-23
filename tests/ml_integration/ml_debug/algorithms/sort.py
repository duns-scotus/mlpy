"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

def bubble_sort(list):
    len = 0
    for item in list:
        len = (len + 1)
    result = []
    for item in list:
        result = (result + [item])
    n = len
    i = 0
    while (i < (n - 1)):
        j = 0
        while (j < ((n - i) - 1)):
            if (result[j] > result[(j + 1)]):
                temp = result[j]
                result[j] = result[(j + 1)]
                result[(j + 1)] = temp
            j = (j + 1)
        i = (i + 1)
    return result

def selection_sort(list):
    len = 0
    for item in list:
        len = (len + 1)
    result = []
    for item in list:
        result = (result + [item])
    i = 0
    while (i < (len - 1)):
        min_idx = i
        j = (i + 1)
        while (j < len):
            if (result[j] < result[min_idx]):
                min_idx = j
            j = (j + 1)
        if (min_idx != i):
            temp = result[i]
            result[i] = result[min_idx]
            result[min_idx] = temp
        i = (i + 1)
    return result

def insertion_sort(list):
    len = 0
    for item in list:
        len = (len + 1)
    result = []
    for item in list:
        result = (result + [item])
    i = 1
    while (i < len):
        key = result[i]
        j = (i - 1)
        while ((j >= 0) and (result[j] > key)):
            result[(j + 1)] = result[j]
            j = (j - 1)
        result[(j + 1)] = key
        i = (i + 1)
    return result

def is_sorted(list):
    len = 0
    for item in list:
        len = (len + 1)
    if (len <= 1):
        return True
    i = 0
    while (i < (len - 1)):
        if (list[i] > list[(i + 1)]):
            return False
        i = (i + 1)
    return True

# End of generated code