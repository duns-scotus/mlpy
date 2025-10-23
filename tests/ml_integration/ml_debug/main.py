"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

def abs(x):
    if (x < 0):
        return (-x)
    return x

def max(a, b):
    if (a > b):
        return a
    return b

def factorial(n):
    if (n <= 1):
        return 1
    return (n * factorial((n - 1)))

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

def linear_search(list, target):
    i = 0
    len = list_length(list)
    while (i < len):
        if (list[i] == target):
            return i
        i = (i + 1)
    return -1

def binary_search(list, target):
    left = 0
    right = (list_length(list) - 1)
    while (left <= right):
        mid = ((left + right) // 2)
        if (list[mid] == target):
            return mid
        elif (list[mid] < target):
            left = (mid + 1)
        else:
            right = (mid - 1)
    return -1

def bubble_sort(list):
    len = list_length(list)
    result = []
    for item in list:
        result = (result + [item])
    i = 0
    while (i < (len - 1)):
        j = 0
        while (j < ((len - i) - 1)):
            if (result[j] > result[(j + 1)]):
                temp = result[j]
                result[j] = result[(j + 1)]
                result[(j + 1)] = temp
            j = (j + 1)
        i = (i + 1)
    return result

def create_node(value, left, right):
    node = {}
    node['value'] = value
    node['left'] = left
    node['right'] = right
    node['is_leaf'] = False
    return node

def create_empty_node():
    node = {}
    node['value'] = 0
    node['left'] = {}
    node['right'] = {}
    node['is_leaf'] = True
    return node

def is_empty_node(node):
    if (node == {}):
        return True
    return False

def tree_sum(node):
    has_value = False
    if (_safe_attr_access(node, 'value') != 0):
        has_value = True
    if (_safe_attr_access(node, 'value') == 0):
        has_value = True
    if (not has_value):
        return 0
    left_sum = tree_sum(_safe_attr_access(node, 'left'))
    right_sum = tree_sum(_safe_attr_access(node, 'right'))
    return ((_safe_attr_access(node, 'value') + left_sum) + right_sum)

def test_arithmetic():
    results = {}
    a = 10
    b = 20
    c = (a + b)
    d = (c * 2)
    e = (d - 5)
    results['sum'] = c
    results['product'] = d
    results['difference'] = e
    results['abs_neg'] = _safe_call(builtin.abs, -42)
    results['max_val'] = _safe_call(builtin.max, 100, 50)
    return results

def test_loops():
    results = {}
    count = 0
    i = 1
    while (i <= 10):
        count = (count + i)
        i = (i + 1)
    results['while_sum'] = count
    numbers = [1, 2, 3, 4, 5]
    total = 0
    for num in numbers:
        total = (total + num)
    results['for_sum'] = total
    return results

def test_conditionals():
    results = {}
    score = 85
    grade = ''
    if (score >= 90):
        grade = 'A'
    elif (score >= 80):
        grade = 'B'
    elif (score >= 70):
        grade = 'C'
    else:
        grade = 'F'
    results['grade'] = grade
    results['score'] = score
    return results

def test_recursion():
    results = {}
    results['fact_5'] = factorial(5)
    results['fact_7'] = factorial(7)
    return results

def test_arrays():
    results = {}
    arr = [5, 2, 8, 1, 9, 3]
    results['length'] = list_length(arr)
    results['sum'] = list_sum(arr)
    results['max'] = list_max(arr)
    results['find_8'] = linear_search(arr, 8)
    results['find_99'] = linear_search(arr, 99)
    sorted_arr = bubble_sort(arr)
    results['sorted'] = sorted_arr
    results['sorted_first'] = sorted_arr[0]
    results['sorted_last'] = sorted_arr[(list_length(sorted_arr) - 1)]
    results['bin_search_5'] = binary_search(sorted_arr, 5)
    return results

def test_objects():
    results = {}
    person = {}
    person['name'] = 'Alice'
    person['age'] = 30
    person['active'] = True
    results['person_name'] = _safe_attr_access(person, 'name')
    results['person_age'] = _safe_attr_access(person, 'age')
    point = {}
    point['x'] = 10
    point['y'] = 20
    results['point_x'] = _safe_attr_access(point, 'x')
    results['point_y'] = _safe_attr_access(point, 'y')
    results['distance'] = (_safe_call(builtin.abs, _safe_attr_access(point, 'x')) + _safe_call(builtin.abs, _safe_attr_access(point, 'y')))
    return results

def test_tree_structure():
    results = {}
    empty1 = {}
    empty1['value'] = 0
    empty1['left'] = {}
    empty1['right'] = {}
    empty2 = {}
    empty2['value'] = 0
    empty2['left'] = {}
    empty2['right'] = {}
    left = create_node(5, empty1, empty1)
    right = create_node(15, empty2, empty2)
    root = create_node(10, left, right)
    results['root_value'] = _safe_attr_access(root, 'value')
    results['left_value'] = _safe_attr_access(_safe_attr_access(root, 'left'), 'value')
    results['right_value'] = _safe_attr_access(_safe_attr_access(root, 'right'), 'value')
    results['manual_sum'] = ((_safe_attr_access(root, 'value') + _safe_attr_access(_safe_attr_access(root, 'left'), 'value')) + _safe_attr_access(_safe_attr_access(root, 'right'), 'value'))
    return results

def main():
    _safe_call(builtin.print, '=== ML Debugging Test Suite ===')
    all_results = {}
    _safe_call(builtin.print, 'Testing arithmetic...')
    all_results['arithmetic'] = test_arithmetic()
    _safe_call(builtin.print, 'Testing loops...')
    all_results['loops'] = test_loops()
    _safe_call(builtin.print, 'Testing conditionals...')
    all_results['conditionals'] = test_conditionals()
    _safe_call(builtin.print, 'Testing recursion...')
    all_results['recursion'] = test_recursion()
    _safe_call(builtin.print, 'Testing arrays...')
    all_results['arrays'] = test_arrays()
    _safe_call(builtin.print, 'Testing objects...')
    all_results['objects'] = test_objects()
    _safe_call(builtin.print, 'Testing tree structures...')
    all_results['trees'] = test_tree_structure()
    _safe_call(builtin.print, '=== All tests completed ===')
    return all_results

test_results = main()

# End of generated code