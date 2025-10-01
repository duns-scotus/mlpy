"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access


def safe_append(arr, item):
    arr[_safe_attr_access(arr, "length")] = item
    return arr


def main():
    print("=== Testing Array Assignment ===")
    test_array = [1, 2, 3]
    print("Before: " + str(str(test_array) + ""))
    test_array[_safe_attr_access(test_array, "length")] = 4
    print("After direct assignment: " + str(str(test_array) + ""))
    test_array2 = [1, 2, 3]
    print("Before safe_append: " + str(str(test_array2) + ""))
    safe_append(test_array2, 4)
    print("After safe_append: " + str(str(test_array2) + ""))
    print("=== Test Complete ===")


main()

# End of generated code
