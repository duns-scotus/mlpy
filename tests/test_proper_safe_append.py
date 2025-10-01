"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports

from mlpy.stdlib.collections_bridge import collections as ml_collections


def safe_append(arr, item):
    return ml_collections.append(arr, item)


def main():
    print("=== Testing Proper Safe Append ===")
    empty = []
    result1 = safe_append(empty, 1)
    print("Empty + 1: " + str(str(result1) + ""))
    small = [1, 2, 3]
    result2 = safe_append(small, 4)
    print("Small + 4: " + str(str(result2) + ""))
    medium = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result3 = safe_append(medium, 11)
    print("Medium + 11: " + str(str(result3) + ""))
    start = [1]
    step1 = safe_append(start, 2)
    step2 = safe_append(step1, 3)
    step3 = safe_append(step2, 4)
    step4 = safe_append(step3, 5)
    print("Chained appends: " + str(str(step4) + ""))
    mixed = ["hello", 42]
    result4 = safe_append(mixed, True)
    print("Mixed types: " + str(str(result4) + ""))
    print("=== Test Complete ===")


main()

# End of generated code
