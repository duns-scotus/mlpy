"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData, typeof

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length

def main():
    print('=== Testing Array Append with Pre-allocation ===')
    test_array = [1, 2, 3]
    print((str('Original: ') + str((str(test_array) + str('')))))
    new_arr = [None, None, None, None]
    i = 0
    while (i < _safe_attr_access(test_array, 'length')):
        new_arr[i] = test_array[i]
        i = (i + 1)
    new_arr[i] = 4
    print((str('Pre-allocated append: ') + str((str(new_arr) + str('')))))
    def array_append(arr, item):
        if (_safe_attr_access(arr, 'length') == 1):
            return [arr[0], item]
        elif (_safe_attr_access(arr, 'length') == 2):
            return [arr[0], arr[1], item]
        elif (_safe_attr_access(arr, 'length') == 3):
            return [arr[0], arr[1], arr[2], item]
        elif (_safe_attr_access(arr, 'length') == 4):
            return [arr[0], arr[1], arr[2], arr[3], item]
        elif (_safe_attr_access(arr, 'length') == 5):
            return [arr[0], arr[1], arr[2], arr[3], arr[4], item]
        else:
            return arr
    test_array2 = [10, 20]
    result2 = array_append(test_array2, 30)
    print((str('Function append: ') + str((str(result2) + str('')))))
    test_array3 = [100, 200, 300]
    result3 = array_append(test_array3, 400)
    print((str('Function append 3: ') + str((str(result3) + str('')))))
    print('=== Test Complete ===')

main()

# End of generated code