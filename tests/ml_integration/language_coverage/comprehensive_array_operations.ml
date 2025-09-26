// Comprehensive Array Operations Test
// Demonstrates all aspects of array manipulation in ML

import collections;
import string;

// Array creation and basic operations
function array_creation_basics() {
    print("=== Array Creation and Basics ===");

    // Different ways to create arrays
    empty_array = [];
    number_array = [1, 2, 3, 4, 5];
    string_array = ["apple", "banana", "cherry", "date"];
    boolean_array = [true, false, true, false];
    mixed_array = [1, "hello", true, 3.14, false];

    print("Empty array: " + empty_array);
    print("Number array: " + number_array);
    print("String array: " + string_array);
    print("Boolean array: " + boolean_array);
    print("Mixed array: " + mixed_array);

    // Array lengths
    print("\nArray Lengths:");
    print("Empty array length: " + collections.length(empty_array));
    print("Number array length: " + collections.length(number_array));
    print("String array length: " + collections.length(string_array));
    print("Mixed array length: " + collections.length(mixed_array));

    // Nested arrays
    nested_numbers = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
    jagged_array = [[1, 2], [3, 4, 5, 6], [7]];
    mixed_nested = [["a", "b"], [1, 2], [true, false]];

    print("\nNested Arrays:");
    print("Nested numbers: " + nested_numbers);
    print("Jagged array: " + jagged_array);
    print("Mixed nested: " + mixed_nested);

    return {
        empty: empty_array,
        numbers: number_array,
        strings: string_array,
        mixed: mixed_array,
        nested: nested_numbers
    };
}

// Array access and modification
function array_access_modification() {
    print("\n=== Array Access and Modification ===");

    numbers = [10, 20, 30, 40, 50];
    fruits = ["apple", "banana", "cherry"];

    print("Original numbers: " + numbers);
    print("Original fruits: " + fruits);

    // Element access
    first_number = numbers[0];
    last_number = numbers[4];
    middle_fruit = fruits[1];

    print("\nElement Access:");
    print("First number: " + first_number);
    print("Last number: " + last_number);
    print("Middle fruit: " + middle_fruit);

    // Element modification
    numbers[2] = 999;
    fruits[0] = "orange";

    print("\nAfter Modifications:");
    print("Modified numbers: " + numbers);
    print("Modified fruits: " + fruits);

    // Nested array access and modification
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
    print("\nOriginal matrix: " + matrix);

    // Access nested elements
    element_0_1 = matrix[0][1];
    element_2_2 = matrix[2][2];
    print("Element [0][1]: " + element_0_1);
    print("Element [2][2]: " + element_2_2);

    // Modify nested elements
    matrix[1][1] = 100;
    print("Modified matrix: " + matrix);

    return {
        numbers: numbers,
        fruits: fruits,
        matrix: matrix,
        accessed_elements: {
            first: first_number,
            last: last_number,
            middle: middle_fruit
        }
    };
}

// Array manipulation operations
function array_manipulation_operations() {
    print("\n=== Array Manipulation Operations ===");

    original_array = [1, 2, 3];

    // Append operations
    appended_array = collections.append(original_array, 4);
    double_appended = collections.append(appended_array, 5);

    print("Original array: " + original_array);
    print("After appending 4: " + appended_array);
    print("After appending 5: " + double_appended);

    // Prepend operations
    prepended_array = collections.prepend(original_array, 0);
    double_prepended = collections.prepend(prepended_array, -1);

    print("\nPrepend Operations:");
    print("Original array: " + original_array);
    print("After prepending 0: " + prepended_array);
    print("After prepending -1: " + double_prepended);

    // Concatenation operations
    array1 = [1, 2, 3];
    array2 = [4, 5, 6];
    array3 = [7, 8, 9];

    concatenated = collections.concat(array1, array2);
    triple_concat = collections.concat(concatenated, array3);

    print("\nConcatenation Operations:");
    print("Array 1: " + array1);
    print("Array 2: " + array2);
    print("Array 3: " + array3);
    print("Concatenated 1+2: " + concatenated);
    print("Triple concatenated: " + triple_concat);

    // Build arrays programmatically
    function build_sequence(start, count) {
        result = [];
        i = 0;
        while (i < count) {
            result = collections.append(result, start + i);
            i = i + 1;
        }
        return result;
    }

    sequence1 = build_sequence(1, 10);
    sequence2 = build_sequence(100, 5);

    print("\nProgrammatic Array Building:");
    print("Sequence 1-10: " + sequence1);
    print("Sequence 100-104: " + sequence2);

    return {
        original: original_array,
        appended: double_appended,
        prepended: double_prepended,
        concatenated: triple_concat,
        sequences: {
            seq1: sequence1,
            seq2: sequence2
        }
    };
}

// Array search and query operations
function array_search_query_operations() {
    print("\n=== Array Search and Query Operations ===");

    numbers = [10, 25, 30, 15, 40, 25, 60];
    fruits = ["apple", "banana", "cherry", "banana", "date"];

    print("Numbers array: " + numbers);
    print("Fruits array: " + fruits);

    // Contains operations
    contains_25 = collections.contains(numbers, 25);
    contains_100 = collections.contains(numbers, 100);
    contains_banana = collections.contains(fruits, "banana");
    contains_grape = collections.contains(fruits, "grape");

    print("\nContains Operations:");
    print("Numbers contains 25: " + contains_25);
    print("Numbers contains 100: " + contains_100);
    print("Fruits contains 'banana': " + contains_banana);
    print("Fruits contains 'grape': " + contains_grape);

    // Index operations
    index_25 = collections.indexOf(numbers, 25);
    index_banana = collections.indexOf(fruits, "banana");
    index_missing = collections.indexOf(numbers, 999);

    print("\nIndex Operations:");
    print("Index of 25 in numbers: " + index_25);
    print("Index of 'banana' in fruits: " + index_banana);
    print("Index of missing element: " + index_missing);

    // First and last elements
    first_number = collections.first(numbers);
    last_number = collections.last(numbers);
    first_fruit = collections.first(fruits);
    last_fruit = collections.last(fruits);

    print("\nFirst and Last Elements:");
    print("First number: " + first_number);
    print("Last number: " + last_number);
    print("First fruit: " + first_fruit);
    print("Last fruit: " + last_fruit);

    // Safe get operations
    valid_get = collections.get(numbers, 3);
    invalid_get = collections.get(numbers, 100);

    print("\nSafe Get Operations:");
    print("Get index 3: " + valid_get);
    print("Get index 100 (out of bounds): " + invalid_get);

    return {
        numbers: numbers,
        fruits: fruits,
        search_results: {
            contains_25: contains_25,
            contains_banana: contains_banana,
            index_25: index_25,
            index_banana: index_banana
        },
        boundaries: {
            first_number: first_number,
            last_number: last_number,
            first_fruit: first_fruit,
            last_fruit: last_fruit
        }
    };
}

// Array slicing and transformation
function array_slicing_transformation() {
    print("\n=== Array Slicing and Transformation ===");

    numbers = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90];

    print("Original numbers: " + numbers);

    // Slicing operations
    slice_2_5 = collections.slice(numbers, 2, 5);
    slice_from_3 = collections.slice(numbers, 3, collections.length(numbers));
    slice_first_4 = collections.slice(numbers, 0, 4);

    print("\nSlicing Operations:");
    print("Slice [2:5]: " + slice_2_5);
    print("Slice from index 3: " + slice_from_3);
    print("Slice first 4: " + slice_first_4);

    // Reverse operations
    original_fruits = ["apple", "banana", "cherry", "date"];
    reversed_fruits = collections.reverse(original_fruits);
    reversed_numbers = collections.reverse(numbers);

    print("\nReverse Operations:");
    print("Original fruits: " + original_fruits);
    print("Reversed fruits: " + reversed_fruits);
    print("Reversed numbers: " + reversed_numbers);

    // Custom transformation functions
    function double_numbers(arr) {
        result = [];
        i = 0;
        while (i < collections.length(arr)) {
            element = collections.get(arr, i);
            doubled = element * 2;
            result = collections.append(result, doubled);
            i = i + 1;
        }
        return result;
    }

    function uppercase_strings(arr) {
        result = [];
        i = 0;
        while (i < collections.length(arr)) {
            element = collections.get(arr, i);
            uppercased = string.upper(element);
            result = collections.append(result, uppercased);
            i = i + 1;
        }
        return result;
    }

    small_numbers = [1, 2, 3, 4, 5];
    doubled_numbers = double_numbers(small_numbers);
    uppercased_fruits = uppercase_strings(original_fruits);

    print("\nCustom Transformations:");
    print("Original small numbers: " + small_numbers);
    print("Doubled numbers: " + doubled_numbers);
    print("Original fruits: " + original_fruits);
    print("Uppercased fruits: " + uppercased_fruits);

    return {
        original: numbers,
        slices: {
            slice_2_5: slice_2_5,
            slice_from_3: slice_from_3,
            slice_first_4: slice_first_4
        },
        reversed: {
            fruits: reversed_fruits,
            numbers: reversed_numbers
        },
        transformations: {
            doubled: doubled_numbers,
            uppercased: uppercased_fruits
        }
    };
}

// Array filtering and reduction
function array_filtering_reduction() {
    print("\n=== Array Filtering and Reduction ===");

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    mixed_numbers = [-2, 5, -8, 12, 0, -1, 7, 3];

    print("Numbers: " + numbers);
    print("Mixed numbers: " + mixed_numbers);

    // Custom filtering functions
    function filter_even(arr) {
        result = [];
        i = 0;
        while (i < collections.length(arr)) {
            element = collections.get(arr, i);
            if (element % 2 == 0) {
                result = collections.append(result, element);
            }
            i = i + 1;
        }
        return result;
    }

    function filter_positive(arr) {
        result = [];
        i = 0;
        while (i < collections.length(arr)) {
            element = collections.get(arr, i);
            if (element > 0) {
                result = collections.append(result, element);
            }
            i = i + 1;
        }
        return result;
    }

    function filter_greater_than(arr, threshold) {
        result = [];
        i = 0;
        while (i < collections.length(arr)) {
            element = collections.get(arr, i);
            if (element > threshold) {
                result = collections.append(result, element);
            }
            i = i + 1;
        }
        return result;
    }

    even_numbers = filter_even(numbers);
    positive_numbers = filter_positive(mixed_numbers);
    large_numbers = filter_greater_than(numbers, 5);

    print("\nFiltering Results:");
    print("Even numbers: " + even_numbers);
    print("Positive numbers: " + positive_numbers);
    print("Numbers > 5: " + large_numbers);

    // Reduction operations
    function sum_array(arr) {
        total = 0;
        i = 0;
        while (i < collections.length(arr)) {
            element = collections.get(arr, i);
            total = total + element;
            i = i + 1;
        }
        return total;
    }

    function product_array(arr) {
        product = 1;
        i = 0;
        while (i < collections.length(arr)) {
            element = collections.get(arr, i);
            product = product * element;
            i = i + 1;
        }
        return product;
    }

    function find_min(arr) {
        if (collections.length(arr) == 0) {
            return 0;
        }
        min_value = collections.first(arr);
        i = 1;
        while (i < collections.length(arr)) {
            element = collections.get(arr, i);
            if (element < min_value) {
                min_value = element;
            }
            i = i + 1;
        }
        return min_value;
    }

    function find_max(arr) {
        if (collections.length(arr) == 0) {
            return 0;
        }
        max_value = collections.first(arr);
        i = 1;
        while (i < collections.length(arr)) {
            element = collections.get(arr, i);
            if (element > max_value) {
                max_value = element;
            }
            i = i + 1;
        }
        return max_value;
    }

    sum_numbers = sum_array(numbers);
    product_small = product_array([1, 2, 3, 4]);
    min_mixed = find_min(mixed_numbers);
    max_mixed = find_max(mixed_numbers);

    print("\nReduction Results:");
    print("Sum of numbers 1-10: " + sum_numbers);
    print("Product of [1,2,3,4]: " + product_small);
    print("Min of mixed numbers: " + min_mixed);
    print("Max of mixed numbers: " + max_mixed);

    return {
        original_arrays: {
            numbers: numbers,
            mixed: mixed_numbers
        },
        filtered: {
            even: even_numbers,
            positive: positive_numbers,
            large: large_numbers
        },
        reduced: {
            sum: sum_numbers,
            product: product_small,
            min: min_mixed,
            max: max_mixed
        }
    };
}

// Array sorting and comparison
function array_sorting_comparison() {
    print("\n=== Array Sorting and Comparison ===");

    unsorted_numbers = [64, 34, 25, 12, 22, 11, 90];
    unsorted_strings = ["banana", "apple", "cherry", "date"];

    print("Unsorted numbers: " + unsorted_numbers);
    print("Unsorted strings: " + unsorted_strings);

    // Bubble sort implementation
    function bubble_sort_numbers(arr) {
        sorted_arr = [];
        // Copy array
        i = 0;
        while (i < collections.length(arr)) {
            element = collections.get(arr, i);
            sorted_arr = collections.append(sorted_arr, element);
            i = i + 1;
        }

        // Bubble sort algorithm
        n = collections.length(sorted_arr);
        i = 0;
        while (i < n - 1) {
            j = 0;
            while (j < n - i - 1) {
                current = sorted_arr[j];
                next = sorted_arr[j + 1];
                if (current > next) {
                    // Swap elements
                    sorted_arr[j] = next;
                    sorted_arr[j + 1] = current;
                }
                j = j + 1;
            }
            i = i + 1;
        }
        return sorted_arr;
    }

    function bubble_sort_strings(arr) {
        sorted_arr = [];
        // Copy array
        i = 0;
        while (i < collections.length(arr)) {
            element = collections.get(arr, i);
            sorted_arr = collections.append(sorted_arr, element);
            i = i + 1;
        }

        // Bubble sort algorithm for strings
        n = collections.length(sorted_arr);
        i = 0;
        while (i < n - 1) {
            j = 0;
            while (j < n - i - 1) {
                current = sorted_arr[j];
                next = sorted_arr[j + 1];
                // Simple string comparison
                if (string.compare(current, next) > 0) {
                    // Swap elements
                    sorted_arr[j] = next;
                    sorted_arr[j + 1] = current;
                }
                j = j + 1;
            }
            i = i + 1;
        }
        return sorted_arr;
    }

    sorted_numbers = bubble_sort_numbers(unsorted_numbers);
    sorted_strings = bubble_sort_strings(unsorted_strings);

    print("\nSorting Results:");
    print("Sorted numbers: " + sorted_numbers);
    print("Sorted strings: " + sorted_strings);

    // Array comparison functions
    function arrays_equal(arr1, arr2) {
        if (collections.length(arr1) != collections.length(arr2)) {
            return false;
        }
        i = 0;
        while (i < collections.length(arr1)) {
            element1 = collections.get(arr1, i);
            element2 = collections.get(arr2, i);
            if (element1 != element2) {
                return false;
            }
            i = i + 1;
        }
        return true;
    }

    function array_contains_all(arr, elements) {
        i = 0;
        while (i < collections.length(elements)) {
            element = collections.get(elements, i);
            if (!collections.contains(arr, element)) {
                return false;
            }
            i = i + 1;
        }
        return true;
    }

    array1 = [1, 2, 3];
    array2 = [1, 2, 3];
    array3 = [1, 2, 4];

    equal_1_2 = arrays_equal(array1, array2);
    equal_1_3 = arrays_equal(array1, array3);

    contains_all_test = array_contains_all([1, 2, 3, 4, 5], [1, 3, 5]);

    print("\nArray Comparison:");
    print("Arrays [1,2,3] and [1,2,3] equal: " + equal_1_2);
    print("Arrays [1,2,3] and [1,2,4] equal: " + equal_1_3);
    print("Array [1,2,3,4,5] contains all [1,3,5]: " + contains_all_test);

    return {
        original: {
            numbers: unsorted_numbers,
            strings: unsorted_strings
        },
        sorted: {
            numbers: sorted_numbers,
            strings: sorted_strings
        },
        comparisons: {
            equal_1_2: equal_1_2,
            equal_1_3: equal_1_3,
            contains_all: contains_all_test
        }
    };
}

// Advanced array algorithms
function advanced_array_algorithms() {
    print("\n=== Advanced Array Algorithms ===");

    // Binary search implementation (requires sorted array)
    function binary_search(sorted_arr, target) {
        left = 0;
        right = collections.length(sorted_arr) - 1;

        while (left <= right) {
            mid = (left + right) / 2;
            mid = mid - (mid % 1); // Convert to integer

            mid_value = sorted_arr[mid];

            if (mid_value == target) {
                return mid;
            } elif (mid_value < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }

    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
    search_target = 11;
    search_missing = 8;

    found_index = binary_search(sorted_array, search_target);
    missing_index = binary_search(sorted_array, search_missing);

    print("Binary Search Test:");
    print("Sorted array: " + sorted_array);
    print("Searching for " + search_target + ": found at index " + found_index);
    print("Searching for " + search_missing + ": found at index " + missing_index);

    // Array rotation
    function rotate_left(arr, positions) {
        if (collections.length(arr) == 0 || positions == 0) {
            return arr;
        }

        actual_positions = positions % collections.length(arr);
        result = [];

        // Add elements from position onwards
        i = actual_positions;
        while (i < collections.length(arr)) {
            element = collections.get(arr, i);
            result = collections.append(result, element);
            i = i + 1;
        }

        // Add elements from beginning to position
        i = 0;
        while (i < actual_positions) {
            element = collections.get(arr, i);
            result = collections.append(result, element);
            i = i + 1;
        }

        return result;
    }

    function rotate_right(arr, positions) {
        return rotate_left(arr, collections.length(arr) - positions);
    }

    original_rotation = [1, 2, 3, 4, 5, 6, 7, 8, 9];
    rotated_left_2 = rotate_left(original_rotation, 2);
    rotated_right_3 = rotate_right(original_rotation, 3);

    print("\nArray Rotation:");
    print("Original: " + original_rotation);
    print("Rotated left by 2: " + rotated_left_2);
    print("Rotated right by 3: " + rotated_right_3);

    // Find duplicates
    function find_duplicates(arr) {
        seen = [];
        duplicates = [];

        i = 0;
        while (i < collections.length(arr)) {
            element = collections.get(arr, i);

            if (collections.contains(seen, element)) {
                if (!collections.contains(duplicates, element)) {
                    duplicates = collections.append(duplicates, element);
                }
            } else {
                seen = collections.append(seen, element);
            }
            i = i + 1;
        }

        return duplicates;
    }

    array_with_dups = [1, 2, 3, 2, 4, 5, 3, 6, 1];
    found_duplicates = find_duplicates(array_with_dups);

    print("\nDuplicate Detection:");
    print("Array with duplicates: " + array_with_dups);
    print("Found duplicates: " + found_duplicates);

    return {
        binary_search: {
            array: sorted_array,
            found_target: search_target,
            found_index: found_index,
            missing_target: search_missing
        },
        rotation: {
            original: original_rotation,
            left_2: rotated_left_2,
            right_3: rotated_right_3
        },
        duplicates: {
            original: array_with_dups,
            found: found_duplicates
        }
    };
}

// Main test runner
function main() {
    print("========================================");
    print("  COMPREHENSIVE ARRAY OPERATIONS TEST");
    print("========================================");

    results = {};

    results.creation = array_creation_basics();
    results.access = array_access_modification();
    results.manipulation = array_manipulation_operations();
    results.search = array_search_query_operations();
    results.slicing = array_slicing_transformation();
    results.filtering = array_filtering_reduction();
    results.sorting = array_sorting_comparison();
    results.algorithms = advanced_array_algorithms();

    print("\n========================================");
    print("  ALL ARRAY TESTS COMPLETED");
    print("========================================");

    return results;
}

// Execute all array tests
main();