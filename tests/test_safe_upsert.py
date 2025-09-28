"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData, typeof

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length

from mlpy.stdlib.collections_bridge import collections as ml_collections

def safe_upsert(arr, pos, item):
    if (pos < _safe_attr_access(arr, 'length')):
        new_arr = []
        i = 0
        while (i < _safe_attr_access(arr, 'length')):
            if (i == pos):
                new_arr = ml_collections.append(new_arr, item)
            else:
                new_arr = ml_collections.append(new_arr, arr[i])
            i = (i + 1)
        return new_arr
    else:
        return ml_collections.append(arr, item)

def safe_append(arr, item):
    return safe_upsert(arr, _safe_attr_access(arr, 'length'), item)

def main():
    print('=== Testing Safe Upsert ===')
    arr1 = [1, 2, 3, 4, 5]
    result1 = safe_upsert(arr1, 2, 99)
    print((str('Update pos 2: ') + str((str(result1) + str('')))))
    arr2 = [10, 20, 30]
    result2 = safe_upsert(arr2, 0, 100)
    print((str('Update pos 0: ') + str((str(result2) + str('')))))
    arr3 = [1, 2, 3]
    result3 = safe_upsert(arr3, 2, 300)
    print((str('Update last pos: ') + str((str(result3) + str('')))))
    arr4 = [1, 2, 3]
    result4 = safe_upsert(arr4, 3, 4)
    print((str('Append at length: ') + str((str(result4) + str('')))))
    result5 = safe_upsert(arr4, 5, 6)
    print((str('Append beyond length: ') + str((str(result5) + str('')))))
    arr6 = [1, 2, 3]
    result6 = safe_append(arr6, 4)
    print((str('Safe append: ') + str((str(result6) + str('')))))
    start = [1, 2, 3]
    step1 = safe_upsert(start, 1, 20)
    step2 = safe_upsert(step1, 3, 4)
    step3 = safe_upsert(step2, 0, 10)
    print((str('Chained upserts: ') + str((str(step3) + str('')))))
    print('=== Test Complete ===')

main()

# End of generated code