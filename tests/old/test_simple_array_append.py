"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access


def main():
    print("=== Testing Array Append ===")
    test_array = [1, 2, 3]
    print("Original: " + str(str(test_array) + ""))
    new_arr = []
    i = 0
    while i < _safe_attr_access(test_array, "length"):
        new_arr[i] = test_array[i]
        i = i + 1
    new_arr[i] = 4
    print("After copy append: " + str(str(new_arr) + ""))

    def safe_append(arr, item):
        result = []
        j = 0
        while j < _safe_attr_access(arr, "length"):
            result[j] = arr[j]
            j = j + 1
        result[j] = item
        return result

    test_array2 = [10, 20, 30]
    result2 = safe_append(test_array2, 40)
    print("Functional append: " + str(str(result2) + ""))
    print("=== Test Complete ===")


main()

# End of generated code
