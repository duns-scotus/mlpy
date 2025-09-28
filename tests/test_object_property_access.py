"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData, typeof

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length

def main():
    print('=== Testing Object Property Access ===')
    print('Testing basic object operations:')
    test_obj = {'name': 'test', 'value': 42, 'active': True, 'timeout': 5000, 'nested': {'inner': 'data'}}
    try:
        print((str('Object name: ') + str(_safe_attr_access(test_obj, 'name'))))
        print((str('Object value: ') + str((str(_safe_attr_access(test_obj, 'value')) + str('')))))
        print((str('Object active: ') + str((str(_safe_attr_access(test_obj, 'active')) + str('')))))
        print((str('Object timeout: ') + str((str(_safe_attr_access(test_obj, 'timeout')) + str('')))))
        print((str('Nested property: ') + str(_safe_attr_access(_safe_attr_access(test_obj, 'nested'), 'inner'))))
    except error:
        print((str('Basic property access FAILED: ') + str((str(error) + str('')))))
    print('Testing dynamic property access:')
    try:
        prop_name = 'value'
        print('Dynamic access: Not testing - likely unsupported')
    except error:
        print((str('Dynamic property access FAILED: ') + str((str(error) + str('')))))
    print('Testing property assignment:')
    try:
        test_obj['name'] = 'modified'
        test_obj['value'] = 100
        test_obj['timeout'] = 10000
        print((str('Modified name: ') + str(_safe_attr_access(test_obj, 'name'))))
        print((str('Modified value: ') + str((str(_safe_attr_access(test_obj, 'value')) + str('')))))
        print((str('Modified timeout: ') + str((str(_safe_attr_access(test_obj, 'timeout')) + str('')))))
    except error:
        print((str('Property assignment FAILED: ') + str((str(error) + str('')))))
    print('Testing new property addition:')
    try:
        test_obj['new_property'] = 'added'
        print((str('New property: ') + str(_safe_attr_access(test_obj, 'new_property'))))
    except error:
        print((str('New property addition FAILED: ') + str((str(error) + str('')))))
    print('Testing object methods:')
    calculator = {'value': 0, 'add': lambda x: _safe_attr_access(calculator, 'value'), 'get_value': lambda : _safe_attr_access(calculator, 'value')}
    try:
        result1 = _safe_attr_access(calculator, 'add')(10)
        result2 = _safe_attr_access(calculator, 'add')(5)
        current = _safe_attr_access(calculator, 'get_value')()
        print((str('Calculator add(10): ') + str((str(result1) + str('')))))
        print((str('Calculator add(5): ') + str((str(result2) + str('')))))
        print((str('Calculator current value: ') + str((str(current) + str('')))))
    except error:
        print((str('Object methods FAILED: ') + str((str(error) + str('')))))
    print('Testing property existence:')
    try:
        has_name = (_safe_attr_access(test_obj, 'name') != None)
        has_missing = (_safe_attr_access(test_obj, 'missing_prop') != None)
        print((str('Has name property: ') + str((str(has_name) + str('')))))
        print((str('Has missing property: ') + str((str(has_missing) + str('')))))
    except error:
        print((str('Property existence check FAILED: ') + str((str(error) + str('')))))
    print('=== Object Property Access Test Complete ===')

main()

# End of generated code