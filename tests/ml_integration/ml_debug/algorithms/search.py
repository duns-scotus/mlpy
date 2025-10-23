"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

def linear_search(list, target):
    i = 0
    len = 0
    for item in list:
        len = (len + 1)
    while (i < len):
        if (list[i] == target):
            return i
        i = (i + 1)
    return -1

def binary_search(list, target):
    left = 0
    right = 0
    for item in list:
        right = (right + 1)
    right = (right - 1)
    while (left <= right):
        mid = ((left + right) / 2)
        if (list[mid] == target):
            return mid
        elif (list[mid] < target):
            left = (mid + 1)
        else:
            right = (mid - 1)
    return -1

def find_min_index(list, start, end):
    min_idx = start
    min_val = list[start]
    i = (start + 1)
    while (i <= end):
        if (list[i] < min_val):
            min_val = list[i]
            min_idx = i
        i = (i + 1)
    return min_idx

def find_max_index(list, start, end):
    max_idx = start
    max_val = list[start]
    i = (start + 1)
    while (i <= end):
        if (list[i] > max_val):
            max_val = list[i]
            max_idx = i
        i = (i + 1)
    return max_idx

def count_occurrences(list, target):
    count = 0
    for item in list:
        if (item == target):
            count = (count + 1)
    return count

def find_first_greater(list, threshold):
    i = 0
    len = 0
    for item in list:
        len = (len + 1)
    while (i < len):
        if (list[i] > threshold):
            return i
        i = (i + 1)
    return -1

# End of generated code