"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

def get_length(arr):
    len = 0
    try:
        i = 0
        while True:
            temp = arr[i]
            i = (i + 1)
            len = (len + 1)
    except Exception as e:
        pass
    finally:
        pass
    return len

def is_array(x):
    try:
        n = x[0]
        return True
    except Exception as e:
        return False
    finally:
        pass

def is_number(x):
    test = (x + 0)
    return ((test == x) or (test != test))

def get_type(value):
    if is_array(value):
        return 'array'
    if is_number(value):
        return 'number'
    return 'other'

def deep_clone(obj):
    obj_type = get_type(obj)
    if (obj_type == 'array'):
        result = []
        len = get_length(obj)
        i = 0
        while (i < len):
            result = (result + [deep_clone(obj[i])])
            i = (i + 1)
        return result
    return obj

def transform_multiply(obj, factor):
    obj_type = get_type(obj)
    if (obj_type == 'number'):
        return (obj * factor)
    if (obj_type == 'array'):
        result = []
        len = get_length(obj)
        i = 0
        while (i < len):
            result = (result + [transform_multiply(obj[i], factor)])
            i = (i + 1)
        return result
    return obj

def transform_capitalize(obj):
    obj_type = get_type(obj)
    if (obj_type == 'array'):
        result = []
        len = get_length(obj)
        i = 0
        while (i < len):
            result = (result + [transform_capitalize(obj[i])])
            i = (i + 1)
        return result
    return obj

def flatten(obj, result):
    obj_type = get_type(obj)
    if (obj_type == 'array'):
        len = get_length(obj)
        i = 0
        while (i < len):
            result = flatten(obj[i], result)
            i = (i + 1)
        return result
    result = (result + [obj])
    return result

def map_nested(obj, func):
    obj_type = get_type(obj)
    if (obj_type == 'array'):
        result = []
        len = get_length(obj)
        i = 0
        while (i < len):
            result = (result + [map_nested(obj[i], func)])
            i = (i + 1)
        return result
    if (obj_type == 'number'):
        return _safe_call(func, obj)
    return obj

def filter_numbers(obj, threshold, result):
    obj_type = get_type(obj)
    if (obj_type == 'number'):
        if (obj > threshold):
            result = (result + [obj])
        return result
    if (obj_type == 'array'):
        len = get_length(obj)
        i = 0
        while (i < len):
            result = filter_numbers(obj[i], threshold, result)
            i = (i + 1)
        return result
    return result

def sum_all_numbers(obj):
    obj_type = get_type(obj)
    if (obj_type == 'number'):
        return obj
    if (obj_type == 'array'):
        sum = 0
        len = get_length(obj)
        i = 0
        while (i < len):
            sum = (sum + sum_all_numbers(obj[i]))
            i = (i + 1)
        return sum
    return 0

def max_depth(obj):
    obj_type = get_type(obj)
    if (obj_type == 'array'):
        max = 0
        len = get_length(obj)
        i = 0
        while (i < len):
            depth = max_depth(obj[i])
            if (depth > max):
                max = depth
            i = (i + 1)
        return (max + 1)
    return 0

def main():
    results = {}
    nested1 = [1, [2, 3], [[4, 5], 6], 7]
    results['flatten1'] = flatten(nested1, [])
    nested2 = [[[1, 2]], [3, [4, [5, 6]]], 7]
    results['flatten2'] = flatten(nested2, [])
    def double(x):
        return (x * 2)
    test_array = [1, [2, 3], [4, [5, 6]]]
    results['mapped'] = map_nested(test_array, double)
    sum_test = [1, [2, 3], [[4, 5], 6]]
    results['sum'] = sum_all_numbers(sum_test)
    filter_test = [1, [2, 5], [[3, 7], 9], 2]
    results['filtered'] = filter_numbers(filter_test, 3, [])
    depth_test1 = [1, 2, 3]
    depth_test2 = [1, [2, 3]]
    depth_test3 = [1, [2, [3, [4]]]]
    results['depth1'] = max_depth(depth_test1)
    results['depth2'] = max_depth(depth_test2)
    results['depth3'] = max_depth(depth_test3)
    complex = [1, [2, 3], [[4, 5], [6, [7, 8]]], 9]
    results['complex_flatten'] = flatten(complex, [])
    results['complex_sum'] = sum_all_numbers(complex)
    results['complex_depth'] = max_depth(complex)
    def triple(x):
        return (x * 3)
    transform_test = [1, [2, [3, 4]], 5]
    results['tripled'] = map_nested(transform_test, triple)
    return results

test_results = main()

# End of generated code