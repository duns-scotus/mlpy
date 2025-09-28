"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData, typeof

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length

def safe_append(arr, item):
    if (_safe_attr_access(arr, 'length') == 0):
        return [item]
    elif (_safe_attr_access(arr, 'length') == 1):
        return [arr[0], item]
    elif (_safe_attr_access(arr, 'length') == 2):
        return [arr[0], arr[1], item]
    elif (_safe_attr_access(arr, 'length') == 3):
        return [arr[0], arr[1], arr[2], item]
    elif (_safe_attr_access(arr, 'length') == 4):
        return [arr[0], arr[1], arr[2], arr[3], item]
    elif (_safe_attr_access(arr, 'length') == 5):
        return [arr[0], arr[1], arr[2], arr[3], arr[4], item]
    elif (_safe_attr_access(arr, 'length') == 6):
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], item]
    elif (_safe_attr_access(arr, 'length') == 7):
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], item]
    elif (_safe_attr_access(arr, 'length') == 8):
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], item]
    elif (_safe_attr_access(arr, 'length') == 9):
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], item]
    elif (_safe_attr_access(arr, 'length') == 10):
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], item]
    else:
        print('Warning: Array too large for safe_append, max size 10')
        return arr

def main():
    print('=== Testing Best Safe Append ===')
    arr1 = []
    result1 = safe_append(arr1, 1)
    print((str('Empty + 1: ') + str((str(result1) + str('')))))
    arr2 = [1, 2]
    result2 = safe_append(arr2, 3)
    print((str('Two + 3: ') + str((str(result2) + str('')))))
    arr5 = [1, 2, 3, 4, 5]
    result5 = safe_append(arr5, 6)
    print((str('Five + 6: ') + str((str(result5) + str('')))))
    start = [1]
    step1 = safe_append(start, 2)
    step2 = safe_append(step1, 3)
    step3 = safe_append(step2, 4)
    print((str('Chained appends: ') + str((str(step3) + str('')))))
    print('=== Test Complete ===')

main()

# End of generated code