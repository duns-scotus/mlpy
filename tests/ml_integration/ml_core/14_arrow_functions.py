"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

def test_simple_arrow():
    double = lambda x: (x * 2)
    result = _safe_call(double, 5)
    return result

def test_arrow_multiple_params():
    add = lambda a, b: (a + b)
    result = _safe_call(add, 10, 20)
    return result

def test_arrow_no_params():
    get_ten = lambda : 10
    result = _safe_call(get_ten)
    return result

def test_arrow_expression():
    square = lambda x: (x * x)
    val = _safe_call(square, 7)
    return val

def test_arrow_map_pattern():
    arr = [1, 2, 3, 4, 5]
    transformer = lambda x: (x * 3)
    result = []
    i = 0
    while (i < 5):
        result = (result + [_safe_call(transformer, arr[i])])
        i = (i + 1)
    return result

def apply_function(func, value):
    return _safe_call(func, value)

def test_arrow_as_argument():
    triple = lambda x: (x * 3)
    result = apply_function(triple, 10)
    return result

def test_arrow_currying():
    make_adder = lambda x: lambda y: (x + y)
    add_5 = _safe_call(make_adder, 5)
    result = _safe_call(add_5, 10)
    return result

def test_arrow_conditional():
    abs_value = lambda x: (0 - x) if (x < 0) else x
    results = {}
    results['positive'] = _safe_call(abs_value, 10)
    results['negative'] = _safe_call(abs_value, -10)
    results['zero'] = _safe_call(abs_value, 0)
    return results

def test_arrow_array_ops():
    get_first = lambda arr: arr[0]
    get_last = lambda arr: arr[4]
    test_arr = [10, 20, 30, 40, 50]
    results = {}
    results['first'] = _safe_call(get_first, test_arr)
    results['last'] = _safe_call(get_last, test_arr)
    return results

def test_arrow_object_ops():
    get_x = lambda obj: _safe_attr_access(obj, 'x')
    get_y = lambda obj: _safe_attr_access(obj, 'y')
    point = {'x': 100, 'y': 200}
    results = {}
    results['x_val'] = _safe_call(get_x, point)
    results['y_val'] = _safe_call(get_y, point)
    return results

def test_arrow_filter_pattern():
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    is_even = lambda x: ((x % 2) == 0)
    evens = []
    i = 0
    while (i < 10):
        if _safe_call(is_even, arr[i]):
            evens = (evens + [arr[i]])
        i = (i + 1)
    return evens

def test_arrow_complex_expression():
    calculate = lambda a, b: ((a + b) + (a * b))
    val = _safe_call(calculate, 3, 4)
    return val

def test_arrow_dispatch():
    operations = [lambda x: (x + 10), lambda x: (x * 2), lambda x: (x * x)]
    results = []
    value = 5
    i = 0
    while (i < 3):
        func = operations[i]
        result = _safe_call(func, value)
        results = (results + [result])
        i = (i + 1)
    return results

def compose(f, g):
    return lambda x: _safe_call(f, _safe_call(g, x))

def test_arrow_composition():
    add_one = lambda x: (x + 1)
    double = lambda x: (x * 2)
    double_then_add_one = compose(add_one, double)
    result = _safe_call(double_then_add_one, 5)
    return result

def test_arrow_logical():
    and_fn = lambda a, b: (a and b)
    or_fn = lambda a, b: (a or b)
    not_fn = lambda a: (not a)
    results = {}
    results['and_true'] = _safe_call(and_fn, True, True)
    results['and_false'] = _safe_call(and_fn, True, False)
    results['or_true'] = _safe_call(or_fn, False, True)
    results['or_false'] = _safe_call(or_fn, False, False)
    results['not_true'] = _safe_call(not_fn, True)
    results['not_false'] = _safe_call(not_fn, False)
    return results

def main():
    results = {}
    results['simple'] = test_simple_arrow()
    results['multiple_params'] = test_arrow_multiple_params()
    results['no_params'] = test_arrow_no_params()
    results['expression'] = test_arrow_expression()
    results['map'] = test_arrow_map_pattern()
    results['as_arg'] = test_arrow_as_argument()
    results['currying'] = test_arrow_currying()
    results['conditional'] = test_arrow_conditional()
    results['array_ops'] = test_arrow_array_ops()
    results['object_ops'] = test_arrow_object_ops()
    results['filter'] = test_arrow_filter_pattern()
    results['complex_expr'] = test_arrow_complex_expression()
    results['dispatch'] = test_arrow_dispatch()
    results['composition'] = test_arrow_composition()
    results['logical'] = test_arrow_logical()
    return results

test_results = main()

# End of generated code