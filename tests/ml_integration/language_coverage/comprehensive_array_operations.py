"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports

from mlpy.stdlib.collections_bridge import collections as ml_collections
from mlpy.stdlib.math_bridge import math as ml_math
from mlpy.stdlib.string_bridge import string as ml_string


def array_creation_basics():
    print("=== Array Creation and Basics ===")
    empty_array = []
    number_array = [1, 2, 3, 4, 5]
    string_array = ["apple", "banana", "cherry", "date"]
    boolean_array = [True, False, True, False]
    mixed_array = [1, "hello", True, 3.14, False]
    print("Empty array: " + str(empty_array))
    print("Number array: " + str(number_array))
    print("String array: " + str(string_array))
    print("Boolean array: " + str(boolean_array))
    print("Mixed array: " + str(mixed_array))
    print("\\nArray Lengths:")
    print("Empty array length: " + str(ml_collections.length(empty_array)))
    print("Number array length: " + str(ml_collections.length(number_array)))
    print("String array length: " + str(ml_collections.length(string_array)))
    print("Mixed array length: " + str(ml_collections.length(mixed_array)))
    nested_numbers = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    jagged_array = [[1, 2], [3, 4, 5, 6], [7]]
    mixed_nested = [["a", "b"], [1, 2], [True, False]]
    print("\\nNested Arrays:")
    print("Nested numbers: " + str(nested_numbers))
    print("Jagged array: " + str(jagged_array))
    print("Mixed nested: " + str(mixed_nested))
    return {
        "empty": empty_array,
        "numbers": number_array,
        "strings": string_array,
        "mixed": mixed_array,
        "nested": nested_numbers,
    }


def array_access_modification():
    print("\\n=== Array Access and Modification ===")
    numbers = [10, 20, 30, 40, 50]
    fruits = ["apple", "banana", "cherry"]
    print("Original numbers: " + str(numbers))
    print("Original fruits: " + str(fruits))
    first_number = numbers[0]
    last_number = numbers[4]
    middle_fruit = fruits[1]
    print("\\nElement Access:")
    print("First number: " + str(first_number))
    print("Last number: " + str(last_number))
    print("Middle fruit: " + str(middle_fruit))
    numbers[2] = 999
    fruits[0] = "orange"
    print("\\nAfter Modifications:")
    print("Modified numbers: " + str(numbers))
    print("Modified fruits: " + str(fruits))
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("\\nOriginal matrix: " + str(matrix))
    element_0_1 = matrix[0][1]
    element_2_2 = matrix[2][2]
    print("Element [0][1]: " + str(element_0_1))
    print("Element [2][2]: " + str(element_2_2))
    matrix[1][1] = 100
    print("Modified matrix: " + str(matrix))
    return {
        "numbers": numbers,
        "fruits": fruits,
        "matrix": matrix,
        "accessed_elements": {"first": first_number, "last": last_number, "middle": middle_fruit},
    }


def array_manipulation_operations():
    print("\\n=== Array Manipulation Operations ===")
    original_array = [1, 2, 3]
    appended_array = ml_collections.append(original_array, 4)
    double_appended = ml_collections.append(appended_array, 5)
    print("Original array: " + str(original_array))
    print("After appending 4: " + str(appended_array))
    print("After appending 5: " + str(double_appended))
    prepended_array = ml_collections.prepend(original_array, 0)
    double_prepended = ml_collections.prepend(prepended_array, 1)
    print("\\nPrepend Operations:")
    print("Original array: " + str(original_array))
    print("After prepending 0: " + str(prepended_array))
    print("After prepending -1: " + str(double_prepended))
    array1 = [1, 2, 3]
    array2 = [4, 5, 6]
    array3 = [7, 8, 9]
    concatenated = ml_collections.concat(array1, array2)
    triple_concat = ml_collections.concat(concatenated, array3)
    print("\\nConcatenation Operations:")
    print("Array 1: " + str(array1))
    print("Array 2: " + str(array2))
    print("Array 3: " + str(array3))
    print("Concatenated 1+2: " + str(concatenated))
    print("Triple concatenated: " + str(triple_concat))

    def build_sequence(start, count):
        result = []
        i = 0
        while i < count:
            result = ml_collections.append(result, (start + i))
            i = i + 1
        return result

    sequence1 = build_sequence(1, 10)
    sequence2 = build_sequence(100, 5)
    print("\\nProgrammatic Array Building:")
    print("Sequence 1-10: " + str(sequence1))
    print("Sequence 100-104: " + str(sequence2))
    return {
        "original": original_array,
        "appended": double_appended,
        "prepended": double_prepended,
        "concatenated": triple_concat,
        "sequences": {"seq1": sequence1, "seq2": sequence2},
    }


def array_search_query_operations():
    print("\\n=== Array Search and Query Operations ===")
    numbers = [10, 25, 30, 15, 40, 25, 60]
    fruits = ["apple", "banana", "cherry", "banana", "date"]
    print("Numbers array: " + str(numbers))
    print("Fruits array: " + str(fruits))
    contains_25 = ml_collections.contains(numbers, 25)
    contains_100 = ml_collections.contains(numbers, 100)
    contains_banana = ml_collections.contains(fruits, "banana")
    contains_grape = ml_collections.contains(fruits, "grape")
    print("\\nContains Operations:")
    print("Numbers contains 25: " + str(contains_25))
    print("Numbers contains 100: " + str(contains_100))
    print("Fruits contains 'banana': " + str(contains_banana))
    print("Fruits contains 'grape': " + str(contains_grape))
    index_25 = ml_collections.indexOf(numbers, 25)
    index_banana = ml_collections.indexOf(fruits, "banana")
    index_missing = ml_collections.indexOf(numbers, 999)
    print("\\nIndex Operations:")
    print("Index of 25 in numbers: " + str(index_25))
    print("Index of 'banana' in fruits: " + str(index_banana))
    print("Index of missing element: " + str(index_missing))
    first_number = ml_collections.first(numbers)
    last_number = ml_collections.last(numbers)
    first_fruit = ml_collections.first(fruits)
    last_fruit = ml_collections.last(fruits)
    print("\\nFirst and Last Elements:")
    print("First number: " + str(first_number))
    print("Last number: " + str(last_number))
    print("First fruit: " + str(first_fruit))
    print("Last fruit: " + str(last_fruit))
    valid_get = ml_collections.get(numbers, 3)
    invalid_get = ml_collections.get(numbers, 100)
    print("\\nSafe Get Operations:")
    print("Get index 3: " + str(valid_get))
    print("Get index 100 (out of bounds): " + str(invalid_get))
    return {
        "numbers": numbers,
        "fruits": fruits,
        "search_results": {
            "contains_25": contains_25,
            "contains_banana": contains_banana,
            "index_25": index_25,
            "index_banana": index_banana,
        },
        "boundaries": {
            "first_number": first_number,
            "last_number": last_number,
            "first_fruit": first_fruit,
            "last_fruit": last_fruit,
        },
    }


def array_slicing_transformation():
    print("\\n=== Array Slicing and Transformation ===")
    numbers = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    print("Original numbers: " + str(numbers))
    slice_2_5 = ml_collections.slice(numbers, 2, 5)
    slice_from_3 = ml_collections.slice(numbers, 3, ml_collections.length(numbers))
    slice_first_4 = ml_collections.slice(numbers, 0, 4)
    print("\\nSlicing Operations:")
    print("Slice [2:5]: " + str(slice_2_5))
    print("Slice from index 3: " + str(slice_from_3))
    print("Slice first 4: " + str(slice_first_4))
    original_fruits = ["apple", "banana", "cherry", "date"]
    reversed_fruits = ml_collections.reverse(original_fruits)
    reversed_numbers = ml_collections.reverse(numbers)
    print("\\nReverse Operations:")
    print("Original fruits: " + str(original_fruits))
    print("Reversed fruits: " + str(reversed_fruits))
    print("Reversed numbers: " + str(reversed_numbers))

    def double_numbers(arr):
        result = []
        i = 0
        while i < ml_collections.length(arr):
            element = ml_collections.get(arr, i)
            doubled = element * 2
            result = ml_collections.append(result, doubled)
            i = i + 1
        return result

    def uppercase_strings(arr):
        result = []
        i = 0
        while i < ml_collections.length(arr):
            element = ml_collections.get(arr, i)
            uppercased = ml_string.upper(element)
            result = ml_collections.append(result, uppercased)
            i = i + 1
        return result

    small_numbers = [1, 2, 3, 4, 5]
    doubled_numbers = double_numbers(small_numbers)
    uppercased_fruits = uppercase_strings(original_fruits)
    print("\\nCustom Transformations:")
    print("Original small numbers: " + str(small_numbers))
    print("Doubled numbers: " + str(doubled_numbers))
    print("Original fruits: " + str(original_fruits))
    print("Uppercased fruits: " + str(uppercased_fruits))
    return {
        "original": numbers,
        "slices": {
            "slice_2_5": slice_2_5,
            "slice_from_3": slice_from_3,
            "slice_first_4": slice_first_4,
        },
        "reversed": {"fruits": reversed_fruits, "numbers": reversed_numbers},
        "transformations": {"doubled": doubled_numbers, "uppercased": uppercased_fruits},
    }


def array_filtering_reduction():
    print("\\n=== Array Filtering and Reduction ===")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    mixed_numbers = [2, 5, 8, 12, 0, 1, 7, 3]
    print("Numbers: " + str(numbers))
    print("Mixed numbers: " + str(mixed_numbers))

    def filter_even(arr):
        result = []
        i = 0
        while i < ml_collections.length(arr):
            element = ml_collections.get(arr, i)
            if (element % 2) == 0:
                result = ml_collections.append(result, element)
            i = i + 1
        return result

    def filter_positive(arr):
        result = []
        i = 0
        while i < ml_collections.length(arr):
            element = ml_collections.get(arr, i)
            if element > 0:
                result = ml_collections.append(result, element)
            i = i + 1
        return result

    def filter_greater_than(arr, threshold):
        result = []
        i = 0
        while i < ml_collections.length(arr):
            element = ml_collections.get(arr, i)
            if element > threshold:
                result = ml_collections.append(result, element)
            i = i + 1
        return result

    even_numbers = filter_even(numbers)
    positive_numbers = filter_positive(mixed_numbers)
    large_numbers = filter_greater_than(numbers, 5)
    print("\\nFiltering Results:")
    print("Even numbers: " + str(even_numbers))
    print("Positive numbers: " + str(positive_numbers))
    print("Numbers > 5: " + str(large_numbers))

    def sum_array(arr):
        total = 0
        i = 0
        while i < ml_collections.length(arr):
            element = ml_collections.get(arr, i)
            total = total + element
            i = i + 1
        return total

    def product_array(arr):
        product = 1
        i = 0
        while i < ml_collections.length(arr):
            element = ml_collections.get(arr, i)
            product = product * element
            i = i + 1
        return product

    def find_min(arr):
        if ml_collections.length(arr) == 0:
            return 0
        min_value = ml_collections.first(arr)
        i = 1
        while i < ml_collections.length(arr):
            element = ml_collections.get(arr, i)
            if element < min_value:
                min_value = element
            i = i + 1
        return min_value

    def find_max(arr):
        if ml_collections.length(arr) == 0:
            return 0
        max_value = ml_collections.first(arr)
        i = 1
        while i < ml_collections.length(arr):
            element = ml_collections.get(arr, i)
            if element > max_value:
                max_value = element
            i = i + 1
        return max_value

    sum_numbers = sum_array(numbers)
    product_small = product_array([1, 2, 3, 4])
    min_mixed = find_min(mixed_numbers)
    max_mixed = find_max(mixed_numbers)
    print("\\nReduction Results:")
    print("Sum of numbers 1-10: " + str(sum_numbers))
    print("Product of [1,2,3,4]: " + str(product_small))
    print("Min of mixed numbers: " + str(min_mixed))
    print("Max of mixed numbers: " + str(max_mixed))
    return {
        "original_arrays": {"numbers": numbers, "mixed": mixed_numbers},
        "filtered": {"even": even_numbers, "positive": positive_numbers, "large": large_numbers},
        "reduced": {
            "sum": sum_numbers,
            "product": product_small,
            "min": min_mixed,
            "max": max_mixed,
        },
    }


def array_sorting_comparison():
    print("\\n=== Array Sorting and Comparison ===")
    unsorted_numbers = [64, 34, 25, 12, 22, 11, 90]
    unsorted_strings = ["banana", "apple", "cherry", "date"]
    print("Unsorted numbers: " + str(unsorted_numbers))
    print("Unsorted strings: " + str(unsorted_strings))

    def bubble_sort_numbers(arr):
        sorted_arr = []
        i = 0
        while i < ml_collections.length(arr):
            element = ml_collections.get(arr, i)
            sorted_arr = ml_collections.append(sorted_arr, element)
            i = i + 1
        n = ml_collections.length(sorted_arr)
        i = 0
        while i < (n - 1):
            j = 0
            while j < ((n - i) - 1):
                current = sorted_arr[j]
                next = sorted_arr[(j + 1)]
                if current > next:
                    sorted_arr[j] = next
                    sorted_arr[(j + 1)] = current
                j = j + 1
            i = i + 1
        return sorted_arr

    def bubble_sort_strings(arr):
        sorted_arr = []
        i = 0
        while i < ml_collections.length(arr):
            element = ml_collections.get(arr, i)
            sorted_arr = ml_collections.append(sorted_arr, element)
            i = i + 1
        n = ml_collections.length(sorted_arr)
        i = 0
        while i < (n - 1):
            j = 0
            while j < ((n - i) - 1):
                current = sorted_arr[j]
                next = sorted_arr[(j + 1)]
                if ml_string.compare(current, next) > 0:
                    sorted_arr[j] = next
                    sorted_arr[(j + 1)] = current
                j = j + 1
            i = i + 1
        return sorted_arr

    sorted_numbers = bubble_sort_numbers(unsorted_numbers)
    sorted_strings = bubble_sort_strings(unsorted_strings)
    print("\\nSorting Results:")
    print("Sorted numbers: " + str(sorted_numbers))
    print("Sorted strings: " + str(sorted_strings))

    def arrays_equal(arr1, arr2):
        if ml_collections.length(arr1) != ml_collections.length(arr2):
            return False
        i = 0
        while i < ml_collections.length(arr1):
            element1 = ml_collections.get(arr1, i)
            element2 = ml_collections.get(arr2, i)
            if element1 != element2:
                return False
            i = i + 1
        return True

    def array_contains_all(arr, elements):
        i = 0
        while i < ml_collections.length(elements):
            element = ml_collections.get(elements, i)
            if ml_collections.contains(arr, element):
                return False
            i = i + 1
        return True

    array1 = [1, 2, 3]
    array2 = [1, 2, 3]
    array3 = [1, 2, 4]
    equal_1_2 = arrays_equal(array1, array2)
    equal_1_3 = arrays_equal(array1, array3)
    contains_all_test = array_contains_all([1, 2, 3, 4, 5], [1, 3, 5])
    print("\\nArray Comparison:")
    print("Arrays [1,2,3] and [1,2,3] equal: " + str(equal_1_2))
    print("Arrays [1,2,3] and [1,2,4] equal: " + str(equal_1_3))
    print("Array [1,2,3,4,5] contains all [1,3,5]: " + str(contains_all_test))
    return {
        "original": {"numbers": unsorted_numbers, "strings": unsorted_strings},
        "sorted": {"numbers": sorted_numbers, "strings": sorted_strings},
        "comparisons": {
            "equal_1_2": equal_1_2,
            "equal_1_3": equal_1_3,
            "contains_all": contains_all_test,
        },
    }


def advanced_array_algorithms():
    print("\\n=== Advanced Array Algorithms ===")

    def binary_search(sorted_arr, target):
        left = 0
        right = ml_collections.length(sorted_arr) - 1
        while left <= right:
            mid = (left + right) / 2
            mid = ml_math.floor(mid)
            mid_value = sorted_arr[mid]
            if mid_value == target:
                return mid
            elif mid_value < target:
                left = mid + 1
            else:
                right = mid - 1
        return 1

    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    search_target = 11
    search_missing = 8
    found_index = binary_search(sorted_array, search_target)
    missing_index = binary_search(sorted_array, search_missing)
    print("Binary Search Test:")
    print("Sorted array: " + str(sorted_array))
    print(

            str(str("Searching for " + str(search_target)) + ": found at index ")
            + str(found_index)

    )
    print(

            str(str("Searching for " + str(search_missing)) + ": found at index ")
            + str(missing_index)

    )

    def rotate_left(arr, positions):
        if (ml_collections.length(arr) == 0) or (positions == 0):
            return arr
        actual_positions = positions % ml_collections.length(arr)
        result = []
        i = actual_positions
        while i < ml_collections.length(arr):
            element = ml_collections.get(arr, i)
            result = ml_collections.append(result, element)
            i = i + 1
        i = 0
        while i < actual_positions:
            element = ml_collections.get(arr, i)
            result = ml_collections.append(result, element)
            i = i + 1
        return result

    def rotate_right(arr, positions):
        return rotate_left(arr, (ml_collections.length(arr) - positions))

    original_rotation = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rotated_left_2 = rotate_left(original_rotation, 2)
    rotated_right_3 = rotate_right(original_rotation, 3)
    print("\\nArray Rotation:")
    print("Original: " + str(original_rotation))
    print("Rotated left by 2: " + str(rotated_left_2))
    print("Rotated right by 3: " + str(rotated_right_3))

    def find_duplicates(arr):
        seen = []
        duplicates = []
        i = 0
        while i < ml_collections.length(arr):
            element = ml_collections.get(arr, i)
            if ml_collections.contains(seen, element):
                if ml_collections.contains(duplicates, element):
                    duplicates = ml_collections.append(duplicates, element)
            else:
                seen = ml_collections.append(seen, element)
            i = i + 1
        return duplicates

    array_with_dups = [1, 2, 3, 2, 4, 5, 3, 6, 1]
    found_duplicates = find_duplicates(array_with_dups)
    print("\\nDuplicate Detection:")
    print("Array with duplicates: " + str(array_with_dups))
    print("Found duplicates: " + str(found_duplicates))
    return {
        "binary_search": {
            "array": sorted_array,
            "found_target": search_target,
            "found_index": found_index,
            "missing_target": search_missing,
        },
        "rotation": {
            "original": original_rotation,
            "left_2": rotated_left_2,
            "right_3": rotated_right_3,
        },
        "duplicates": {"original": array_with_dups, "found": found_duplicates},
    }


def main():
    print("========================================")
    print("  COMPREHENSIVE ARRAY OPERATIONS TEST")
    print("========================================")
    results = {}
    results["creation"] = array_creation_basics()
    results["access"] = array_access_modification()
    results["manipulation"] = array_manipulation_operations()
    results["search"] = array_search_query_operations()
    results["slicing"] = array_slicing_transformation()
    results["filtering"] = array_filtering_reduction()
    results["sorting"] = array_sorting_comparison()
    results["algorithms"] = advanced_array_algorithms()
    print("\\n========================================")
    print("  ALL ARRAY TESTS COMPLETED")
    print("========================================")
    return results


main()

# End of generated code
