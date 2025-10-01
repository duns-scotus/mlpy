"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib import typeof
from mlpy.stdlib.collections_bridge import collections as ml_collections
from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access


def safe_append(arr, item):
    arr[_safe_attr_access(arr, "length")] = item
    return arr


def main():
    print("=== Testing Array Access Methods ===")
    test_array = [1, 2, 3, 4, 5]
    print("Testing direct property access:")
    try:
        direct_length = _safe_attr_access(test_array, "length")
        print("Direct length access: " + str(str(direct_length) + ""))
    except error:
        print("Direct length access FAILED: " + str(str(error) + ""))
    print("Testing module function access:")
    try:
        if typeof(collections) != "unknown":
            module_length = ml_collections.length(test_array)
            print("Collections length: " + str(str(module_length) + ""))
        else:
            print("Collections module not available")
    except error:
        print("Module length access FAILED: " + str(str(error) + ""))
    print("Testing array assignment patterns:")
    test_array1 = [1, 2, 3]
    try:
        print("Before assignment: " + str(str(test_array1) + ""))
        test_array1[_safe_attr_access(test_array1, "length")] = 4
        print("After direct assignment: " + str(str(test_array1) + ""))
    except error:
        print("Direct assignment FAILED: " + str(str(error) + ""))
    test_array2 = [1, 2, 3]
    try:
        print("Before safe_append: " + str(str(test_array2) + ""))
        safe_append(test_array2, 4)
        print("After safe_append: " + str(str(test_array2) + ""))
    except error:
        print("Safe_append FAILED: " + str(str(error) + ""))
    test_array3 = [1, 2, 3]
    try:
        print("Before known index: " + str(str(test_array3) + ""))
        test_array3[3] = 4
        print("After known index assignment: " + str(str(test_array3) + ""))
    except error:
        print("Known index assignment FAILED: " + str(str(error) + ""))
    print("Testing array methods:")
    try:
        test_array4 = [1, 2, 3]
        if typeof(_safe_attr_access(test_array4, "push")) == "function":
            _safe_attr_access(test_array4, "push")(4)
            print("Push method worked: " + str(str(test_array4) + ""))
        else:
            print("Push method not available")
    except error:
        print("Push method FAILED: " + str(str(error) + ""))
    print("=== Array Access Methods Test Complete ===")


main()

# End of generated code
