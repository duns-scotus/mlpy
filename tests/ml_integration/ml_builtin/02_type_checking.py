"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_typeof_primitives():
    results = {}
    results['typeof_true'] = _safe_call(builtin.typeof, True)
    results['typeof_false'] = _safe_call(builtin.typeof, False)
    results['typeof_int'] = _safe_call(builtin.typeof, 42)
    results['typeof_float'] = _safe_call(builtin.typeof, 3.14)
    results['typeof_negative'] = _safe_call(builtin.typeof, -100)
    results['typeof_zero'] = _safe_call(builtin.typeof, 0)
    results['typeof_string'] = _safe_call(builtin.typeof, 'hello')
    results['typeof_empty_str'] = _safe_call(builtin.typeof, '')
    results['typeof_array'] = _safe_call(builtin.typeof, [1, 2, 3])
    results['typeof_empty_array'] = _safe_call(builtin.typeof, [])
    results['typeof_object'] = _safe_call(builtin.typeof, {'a': 1, 'b': 2})
    results['typeof_empty_obj'] = _safe_call(builtin.typeof, {})
    results['typeof_function'] = _safe_call(builtin.typeof, test_typeof_primitives)
    return results

def test_isinstance_primitives():
    results = {}
    results['true_is_boolean'] = _safe_call(builtin.isinstance, True, 'boolean')
    results['false_is_boolean'] = _safe_call(builtin.isinstance, False, 'boolean')
    results['int_is_not_boolean'] = _safe_call(builtin.isinstance, 42, 'boolean')
    results['int_is_number'] = _safe_call(builtin.isinstance, 42, 'number')
    results['float_is_number'] = _safe_call(builtin.isinstance, 3.14, 'number')
    results['str_is_not_number'] = _safe_call(builtin.isinstance, '42', 'number')
    results['str_is_string'] = _safe_call(builtin.isinstance, 'hello', 'string')
    results['int_is_not_string'] = _safe_call(builtin.isinstance, 42, 'string')
    results['array_is_array'] = _safe_call(builtin.isinstance, [1, 2, 3], 'array')
    results['obj_is_not_array'] = _safe_call(builtin.isinstance, {'a': 1}, 'array')
    results['obj_is_object'] = _safe_call(builtin.isinstance, {'a': 1}, 'object')
    results['array_is_not_object'] = _safe_call(builtin.isinstance, [1, 2], 'object')
    results['func_is_function'] = _safe_call(builtin.isinstance, test_isinstance_primitives, 'function')
    results['int_is_not_function'] = _safe_call(builtin.isinstance, 42, 'function')
    return results

def test_type_guards():
    results = {}
    value = 42
    if (_safe_call(builtin.typeof, value) == 'number'):
        results['number_guard'] = True
    else:
        results['number_guard'] = False
    value2 = 'hello'
    if (_safe_call(builtin.typeof, value2) == 'string'):
        results['string_guard'] = True
    else:
        results['string_guard'] = False
    value3 = [1, 2, 3]
    if (_safe_call(builtin.typeof, value3) == 'array'):
        results['array_guard'] = True
    else:
        results['array_guard'] = False
    value4 = {'a': 1, 'b': 2}
    if (_safe_call(builtin.typeof, value4) == 'object'):
        results['object_guard'] = True
    else:
        results['object_guard'] = False
    return results

def process_by_type(value):
    type_name = _safe_call(builtin.typeof, value)
    if (type_name == 'number'):
        return (value * 2)
    elif (type_name == 'string'):
        return value
    elif (type_name == 'array'):
        return _safe_call(builtin.len, value)
    elif (type_name == 'object'):
        return _safe_call(builtin.len, _safe_call(builtin.keys, value))
    elif (type_name == 'boolean'):
        return _safe_call(builtin.int, value)
    else:
        return 'unknown'

def test_polymorphic_function():
    results = {}
    results['process_number'] = process_by_type(42)
    results['process_string'] = process_by_type('hello')
    results['process_array'] = process_by_type([1, 2, 3, 4])
    results['process_object'] = process_by_type({'a': 1, 'b': 2, 'c': 3})
    results['process_boolean'] = process_by_type(True)
    return results

def test_type_checking_in_conditionals():
    results = {}
    values = [42, 'hello', True, [1, 2, 3], {'a': 1}]
    number_count = 0
    string_count = 0
    boolean_count = 0
    array_count = 0
    object_count = 0
    for val in values:
        t = _safe_call(builtin.typeof, val)
        if (t == 'number'):
            number_count = (number_count + 1)
        elif (t == 'string'):
            string_count = (string_count + 1)
        elif (t == 'boolean'):
            boolean_count = (boolean_count + 1)
        elif (t == 'array'):
            array_count = (array_count + 1)
        elif (t == 'object'):
            object_count = (object_count + 1)
    results['numbers'] = number_count
    results['strings'] = string_count
    results['booleans'] = boolean_count
    results['arrays'] = array_count
    results['objects'] = object_count
    return results

def main():
    all_results = {}
    all_results['typeof_tests'] = test_typeof_primitives()
    all_results['isinstance_tests'] = test_isinstance_primitives()
    all_results['guards'] = test_type_guards()
    all_results['polymorphic'] = test_polymorphic_function()
    all_results['counting'] = test_type_checking_in_conditionals()
    return all_results

test_results = main()

# End of generated code