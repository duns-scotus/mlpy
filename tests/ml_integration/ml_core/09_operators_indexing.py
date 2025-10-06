"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

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

def test_arithmetic():
    a = 10
    b = 3
    return {'add': (a + b), 'subtract': (a - b), 'multiply': (a * b), 'divide': (a / b), 'modulo': (a - ((a / b) * b)), 'negate': (-a), 'complex': (((a + b) * 2) - b)}

def test_comparison():
    a = 5
    b = 3
    c = 5
    return {'equal': (a == c), 'not_equal': (a != b), 'greater': (a > b), 'less': (b < a), 'greater_equal': (a >= c), 'less_equal': (b <= a), 'chain': ((a > b) and (b > 0))}

def test_logical():
    return {'and_true': (True and True), 'and_false': (True and False), 'or_true': (False or True), 'or_false': (False or False), 'not_true': (not False), 'not_false': (not True), 'complex': ((5 > 3) and (2 < 4)), 'short_circuit': (True or ((1 / 0) == 0))}

def test_inc_dec():
    a = 10
    b = (a + 1)
    c = (a - 1)
    a = (a + 1)
    d = a
    a = (a - 1)
    e = a
    return {'inc': b, 'dec': c, 'after_inc': d, 'after_dec': e}

def test_compound():
    a = 5
    a = (a + 3)
    add_result = a
    a = (a - 2)
    sub_result = a
    a = (a * 4)
    mul_result = a
    a = (a / 2)
    div_result = a
    return {'add': add_result, 'sub': sub_result, 'mul': mul_result, 'div': div_result}

def test_array_indexing():
    arr = [10, 20, 30, 40, 50]
    return {'first': arr[0], 'second': arr[1], 'third': arr[2], 'last': arr[4], 'middle': arr[2]}

def test_array_assignment():
    arr = [1, 2, 3, 4, 5]
    arr[0] = 10
    arr[2] = 30
    arr[4] = 50
    return {'modified': arr, 'first': arr[0], 'third': arr[2], 'fifth': arr[4]}

def test_nested_indexing():
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    return {'row0_col0': matrix[0][0], 'row0_col2': matrix[0][2], 'row1_col1': matrix[1][1], 'row2_col0': matrix[2][0], 'row2_col2': matrix[2][2]}

def test_object_access():
    obj = {'name': 'test', 'value': 42, 'nested': {'inner': 100}}
    return {'name': _safe_attr_access(obj, 'name'), 'value': _safe_attr_access(obj, 'value'), 'nested_inner': _safe_attr_access(_safe_attr_access(obj, 'nested'), 'inner')}

def test_object_assignment():
    obj = {'x': 1, 'y': 2, 'z': 3}
    obj['x'] = 10
    obj['y'] = 20
    obj['z'] = 30
    return {'modified': obj, 'x': _safe_attr_access(obj, 'x'), 'y': _safe_attr_access(obj, 'y'), 'z': _safe_attr_access(obj, 'z')}

def test_mixed_indexing():
    data = [{'id': 1, 'value': 10}, {'id': 2, 'value': 20}, {'id': 3, 'value': 30}]
    return {'first_id': _safe_attr_access(data[0], 'id'), 'second_value': _safe_attr_access(data[1], 'value'), 'third_id': _safe_attr_access(data[2], 'id')}

def test_precedence():
    return {'mult_first': (2 + (3 * 4)), 'parens': ((2 + 3) * 4), 'complex': ((10 + (5 * 2)) - 3), 'with_parens': ((10 + 5) * (2 - 3)), 'logical': ((5 > 3) and (2 < 4)), 'compare_arith': ((2 + 3) > 4)}

def test_ternary():
    a = 10
    b = 5
    max = a if (a > b) else b
    min = a if (a < b) else b
    equal = 'equal' if (a == b) else 'not equal'
    nested = 'very large' if (a > 15) else 'medium' if (a > b) else 'small'
    return {'max': max, 'min': min, 'equal': equal, 'nested': nested}

def test_string_ops():
    str1 = 'Hello'
    str2 = 'World'
    num = 42
    return {'concat': (str((str(str1) + str(' '))) + str(str2)), 'with_num': (str((str(str1) + str(' '))) + str(num)), 'repeated': (str1 + str1)}

def test_boundaries():
    arr = [1, 2, 3]
    first = arr[0]
    last = arr[2]
    len = 3
    calculated_last = arr[(len - 1)]
    return {'first': first, 'last': last, 'calculated': calculated_last, 'zero_index': arr[0], 'max_index': arr[2]}

def test_evaluation_order():
    counter = 0
    def increment():
        nonlocal counter
        counter = (counter + 1)
        return counter
    a = increment()
    b = increment()
    c = increment()
    return {'a': a, 'b': b, 'c': c, 'counter': counter}

def main():
    results = {}
    results['arithmetic'] = test_arithmetic()
    results['comparison'] = test_comparison()
    results['logical'] = test_logical()
    results['inc_dec'] = test_inc_dec()
    results['compound'] = test_compound()
    results['array_index'] = test_array_indexing()
    results['array_assign'] = test_array_assignment()
    results['nested_index'] = test_nested_indexing()
    results['object_access'] = test_object_access()
    results['object_assign'] = test_object_assignment()
    results['mixed_index'] = test_mixed_indexing()
    results['precedence'] = test_precedence()
    results['ternary'] = test_ternary()
    results['string_ops'] = test_string_ops()
    results['boundaries'] = test_boundaries()
    results['eval_order'] = test_evaluation_order()
    return results

test_results = main()

# End of generated code