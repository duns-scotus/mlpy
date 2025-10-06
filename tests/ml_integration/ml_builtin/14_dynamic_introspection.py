"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

def test_hasattr_with_safe_attributes():
    results = {}
    results['has_upper'] = _safe_call(builtin.hasattr, 'hello', 'upper')
    results['has_lower'] = _safe_call(builtin.hasattr, 'HELLO', 'lower')
    results['has_append'] = _safe_call(builtin.hasattr, [1, 2, 3], 'append')
    results['has_class'] = _safe_call(builtin.hasattr, 'test', '__class__')
    results['has_dict'] = _safe_call(builtin.hasattr, [], '__dict__')
    return results

def test_call_with_builtin_functions():
    results = {}
    abs_func = builtin.abs
    results['call_abs'] = _safe_call(builtin.call, abs_func, -5)
    max_func = builtin.max
    results['call_max'] = _safe_call(builtin.call, max_func, 10, 20, 30)
    min_func = builtin.min
    results['call_min'] = _safe_call(builtin.call, min_func, 5, 2, 8)
    return results

def test_call_with_lambdas():
    results = {}
    add = lambda x, y: (x + y)
    results['call_add'] = _safe_call(builtin.call, add, 10, 5)
    multiply = lambda x, y: (x * y)
    results['call_multiply'] = _safe_call(builtin.call, multiply, 6, 7)
    return results

def test_call_with_user_functions():
    results = {}
    def double(x):
        return (x * 2)
    def triple(x):
        return (x * 3)
    results['call_double'] = _safe_call(builtin.call, double, 21)
    results['call_triple'] = _safe_call(builtin.call, triple, 14)
    return results

def test_dynamic_function_selection():
    results = {}
    def select_operation(op_name):
        if (op_name == 'double'):
            return lambda x: (x * 2)
        elif (op_name == 'square'):
            return lambda x: (x * x)
        elif (op_name == 'negate'):
            return lambda x: (-x)
        else:
            return lambda x: x
    double_fn = select_operation('double')
    results['double_result'] = _safe_call(builtin.call, double_fn, 10)
    square_fn = select_operation('square')
    results['square_result'] = _safe_call(builtin.call, square_fn, 5)
    negate_fn = select_operation('negate')
    results['negate_result'] = _safe_call(builtin.call, negate_fn, 7)
    return results

def test_function_composition_with_call():
    results = {}
    add_10 = lambda x: (x + 10)
    multiply_2 = lambda x: (x * 2)
    val = 5
    step1 = _safe_call(builtin.call, add_10, val)
    step2 = _safe_call(builtin.call, multiply_2, step1)
    results['step1'] = step1
    results['step2'] = step2
    return results

def test_functional_programming_patterns():
    results = {}
    def apply_twice(func, value):
        result = _safe_call(builtin.call, func, value)
        result = _safe_call(builtin.call, func, result)
        return result
    increment = lambda x: (x + 1)
    results['apply_twice_inc'] = apply_twice(increment, 10)
    double = lambda x: (x * 2)
    results['apply_twice_double'] = apply_twice(double, 3)
    return results

def test_callable_check_before_call():
    results = {}
    func = lambda x: (x * 2)
    not_func = 42
    if _safe_call(builtin.callable, func):
        results['func_callable'] = True
        results['func_result'] = _safe_call(builtin.call, func, 5)
    if _safe_call(builtin.callable, not_func):
        results['not_func_callable'] = True
    else:
        results['not_func_callable'] = False
    return results

def test_map_like_with_call():
    results = {}
    numbers = [1, 2, 3, 4, 5]
    transform = lambda x: (x * x)
    transformed = []
    for n in numbers:
        transformed = (transformed + [_safe_call(builtin.call, transform, n)])
    results['transformed'] = transformed
    return results

def test_filter_like_with_call():
    results = {}
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    is_even = lambda x: ((x - ((x / 2) * 2)) == 0)
    filtered = []
    for n in numbers:
        if _safe_call(builtin.call, is_even, n):
            filtered = (filtered + [n])
    results['filtered'] = filtered
    return results

def test_reduce_like_with_call():
    results = {}
    numbers = [1, 2, 3, 4, 5]
    add = lambda a, b: (a + b)
    accumulator = 0
    for n in numbers:
        accumulator = _safe_call(builtin.call, add, accumulator, n)
    results['sum'] = accumulator
    return results

def test_strategy_pattern_with_call():
    results = {}
    strategies = {'add': lambda a, b: (a + b), 'multiply': lambda a, b: (a * b), 'subtract': lambda a, b: (a - b)}
    result_add = _safe_call(builtin.call, _safe_attr_access(strategies, 'add'), 10, 5)
    result_multiply = _safe_call(builtin.call, _safe_attr_access(strategies, 'multiply'), 10, 5)
    result_subtract = _safe_call(builtin.call, _safe_attr_access(strategies, 'subtract'), 10, 5)
    results['add'] = result_add
    results['multiply'] = result_multiply
    results['subtract'] = result_subtract
    return results

def test_pipeline_with_call():
    results = {}
    operations = [lambda x: (x + 10), lambda x: (x * 2), lambda x: (x - 5)]
    value = 5
    for op in operations:
        value = _safe_call(builtin.call, op, value)
    results['final'] = value
    return results

def main():
    all_results = {}
    all_results['hasattr_tests'] = test_hasattr_with_safe_attributes()
    all_results['call_builtins'] = test_call_with_builtin_functions()
    all_results['call_lambdas'] = test_call_with_lambdas()
    all_results['call_user_funcs'] = test_call_with_user_functions()
    all_results['dynamic_select'] = test_dynamic_function_selection()
    all_results['composition'] = test_function_composition_with_call()
    all_results['functional'] = test_functional_programming_patterns()
    all_results['callable_check'] = test_callable_check_before_call()
    all_results['map_like'] = test_map_like_with_call()
    all_results['filter_like'] = test_filter_like_with_call()
    all_results['reduce_like'] = test_reduce_like_with_call()
    all_results['strategy'] = test_strategy_pattern_with_call()
    all_results['pipeline'] = test_pipeline_with_call()
    return all_results

test_results = main()

# End of generated code