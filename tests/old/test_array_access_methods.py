"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData, typeof

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length

from mlpy.stdlib.array_bridge import array as ml_array

from mlpy.stdlib.collections_bridge import collections as ml_collections

def safe_append(arr, item):
    arr[_safe_attr_access(arr, 'length')] = item
    return arr

def main():
    print('=== Testing Array Access Methods ===')
    test_array = [1, 2, 3, 4, 5]
    print('Testing direct property access:')
    try:
        direct_length = _safe_attr_access(test_array, 'length')
        print((str('Direct length access: ') + str((str(direct_length) + str('')))))
    except error:
        print((str('Direct length access FAILED: ') + str((str(error) + str('')))))
    print('Testing module function access:')
    try:
        if (typeof(collections) != 'unknown'):
            module_length = ml_collections.length(test_array)
            print((str('Collections length: ') + str((str(module_length) + str('')))))
        else:
            print('Collections module not available')
    except error:
        print((str('Module length access FAILED: ') + str((str(error) + str('')))))
    print('Testing array assignment patterns:')
    test_array1 = [1, 2, 3]
    try:
        print((str('Before assignment: ') + str((str(test_array1) + str('')))))
        test_array1[_safe_attr_access(test_array1, 'length')] = 4
        print((str('After direct assignment: ') + str((str(test_array1) + str('')))))
    except error:
        print((str('Direct assignment FAILED: ') + str((str(error) + str('')))))
    test_array2 = [1, 2, 3]
    try:
        print((str('Before safe_append: ') + str((str(test_array2) + str('')))))
        safe_append(test_array2, 4)
        print((str('After safe_append: ') + str((str(test_array2) + str('')))))
    except error:
        print((str('Safe_append FAILED: ') + str((str(error) + str('')))))
    test_array3 = [1, 2, 3]
    try:
        print((str('Before known index: ') + str((str(test_array3) + str('')))))
        test_array3[3] = 4
        print((str('After known index assignment: ') + str((str(test_array3) + str('')))))
    except error:
        print((str('Known index assignment FAILED: ') + str((str(error) + str('')))))
    print('Testing array methods:')
    try:
        test_array4 = [1, 2, 3]
        if (typeof(_safe_attr_access(test_array4, 'push')) == 'function'):
            _safe_attr_access(test_array4, 'push')(4)
            print((str('Push method worked: ') + str((str(test_array4) + str('')))))
        else:
            print('Push method not available')
    except error:
        print((str('Push method FAILED: ') + str((str(error) + str('')))))
    print('=== Array Access Methods Test Complete ===')

main()

# End of generated code