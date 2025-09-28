"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData, typeof

from mlpy.stdlib.collections_bridge import collections as ml_collections

def safe_append(arr, item):
    return ml_collections.append(arr, item)

def main():
    print('=== Testing Proper Safe Append ===')
    empty = []
    result1 = safe_append(empty, 1)
    print((str('Empty + 1: ') + str((str(result1) + str('')))))
    small = [1, 2, 3]
    result2 = safe_append(small, 4)
    print((str('Small + 4: ') + str((str(result2) + str('')))))
    medium = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result3 = safe_append(medium, 11)
    print((str('Medium + 11: ') + str((str(result3) + str('')))))
    start = [1]
    step1 = safe_append(start, 2)
    step2 = safe_append(step1, 3)
    step3 = safe_append(step2, 4)
    step4 = safe_append(step3, 5)
    print((str('Chained appends: ') + str((str(step4) + str('')))))
    mixed = ['hello', 42]
    result4 = safe_append(mixed, True)
    print((str('Mixed types: ') + str((str(result4) + str('')))))
    print('=== Test Complete ===')

main()

# End of generated code