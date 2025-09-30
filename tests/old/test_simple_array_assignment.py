"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData, typeof

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length

def safe_append(arr, item):
    arr[_safe_attr_access(arr, 'length')] = item
    return arr

def main():
    print('=== Testing Array Assignment ===')
    test_array = [1, 2, 3]
    print((str('Before: ') + str((str(test_array) + str('')))))
    test_array[_safe_attr_access(test_array, 'length')] = 4
    print((str('After direct assignment: ') + str((str(test_array) + str('')))))
    test_array2 = [1, 2, 3]
    print((str('Before safe_append: ') + str((str(test_array2) + str('')))))
    safe_append(test_array2, 4)
    print((str('After safe_append: ') + str((str(test_array2) + str('')))))
    print('=== Test Complete ===')

main()

# End of generated code