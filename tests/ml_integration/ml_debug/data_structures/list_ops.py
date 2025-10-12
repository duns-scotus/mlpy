"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

def list_length(list):
    count = 0
    for item in list:
        count = (count + 1)
    return count

def list_sum(list):
    total = 0
    for item in list:
        total = (total + item)
    return total

def list_max(list):
    if (list_length(list) == 0):
        return 0
    max_val = list[0]
    for item in list:
        if (item > max_val):
            max_val = item
    return max_val

def list_min(list):
    if (list_length(list) == 0):
        return 0
    min_val = list[0]
    for item in list:
        if (item < min_val):
            min_val = item
    return min_val

def list_contains(list, value):
    for item in list:
        if (item == value):
            return True
    return False

def list_reverse(list):
    len = list_length(list)
    result = []
    i = (len - 1)
    while (i >= 0):
        result = (result + [list[i]])
        i = (i - 1)
    return result

def list_filter_even(list):
    result = []
    for item in list:
        remainder = (item - ((item / 2) * 2))
        if (remainder == 0):
            result = (result + [item])
    return result

def list_map_double(list):
    result = []
    for item in list:
        result = (result + [(item * 2)])
    return result

def list_slice(list, start, end):
    result = []
    i = start
    while (i < end):
        if ((i >= 0) and (i < list_length(list))):
            result = (result + [list[i]])
        i = (i + 1)
    return result

# End of generated code