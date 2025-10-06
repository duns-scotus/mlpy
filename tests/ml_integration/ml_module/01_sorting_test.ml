// Test: User Module Import - Sorting Utilities
// Tests importing and using the sorting.ml user module

import user_modules.sorting;

function test_is_sorted() {
    sorted_arr = [1, 2, 3, 4, 5];
    unsorted_arr = [5, 2, 8, 1, 9];

    result1 = user_modules.sorting.is_sorted(sorted_arr);
    result2 = user_modules.sorting.is_sorted(unsorted_arr);

    print("Testing is_sorted:");
    print("  Sorted array [1,2,3,4,5]: " + str(result1));
    print("  Unsorted array [5,2,8,1,9]: " + str(result2));

    if (result1 == true) {
        if (result2 == false) {
            return true;
        }
    }
    return false;
}

function test_find_min_max() {
    arr = [5, 2, 8, 1, 9, 3];

    min_val = user_modules.sorting.find_min(arr);
    max_val = user_modules.sorting.find_max(arr);

    print("Testing find_min and find_max:");
    print("  Array: [5, 2, 8, 1, 9, 3]");
    print("  Min: " + str(min_val));
    print("  Max: " + str(max_val));

    if (min_val == 1) {
        if (max_val == 9) {
            return true;
        }
    }
    return false;
}

function test_selection_sort() {
    arr = [64, 25, 12, 22, 11];

    print("Testing selection_sort:");
    print("  Before: [64, 25, 12, 22, 11]");

    sorted_arr = user_modules.sorting.selection_sort(arr);

    print("  After: " + str(sorted_arr));

    // Verify sorted
    is_sorted = user_modules.sorting.is_sorted(sorted_arr);

    if (is_sorted == true) {
        if (sorted_arr[0] == 11) {
            if (sorted_arr[4] == 64) {
                return true;
            }
        }
    }
    return false;
}

function test_reverse() {
    arr = [1, 2, 3, 4, 5];

    print("Testing reverse:");
    print("  Before: [1, 2, 3, 4, 5]");

    reversed_arr = user_modules.sorting.reverse(arr);

    print("  After: " + str(reversed_arr));

    if (reversed_arr[0] == 5) {
        if (reversed_arr[4] == 1) {
            return true;
        }
    }
    return false;
}

function test_sort_descending() {
    arr = [3, 1, 4, 1, 5, 9, 2, 6];

    print("Testing sort_descending:");
    print("  Before: [3, 1, 4, 1, 5, 9, 2, 6]");

    sorted_arr = user_modules.sorting.sort_descending(arr);

    print("  After: " + str(sorted_arr));

    if (sorted_arr[0] == 9) {
        if (sorted_arr[len(sorted_arr) - 1] == 1) {
            return true;
        }
    }
    return false;
}

function main() {
    print("===== User Module Test: sorting.ml =====");
    print("");

    test1 = test_is_sorted();
    print("Test 1 (is_sorted): " + str(test1));
    print("");

    test2 = test_find_min_max();
    print("Test 2 (find_min_max): " + str(test2));
    print("");

    test3 = test_selection_sort();
    print("Test 3 (selection_sort): " + str(test3));
    print("");

    test4 = test_reverse();
    print("Test 4 (reverse): " + str(test4));
    print("");

    test5 = test_sort_descending();
    print("Test 5 (sort_descending): " + str(test5));
    print("");

    // Count passing tests
    passed = 0;
    if (test1) { passed = passed + 1; }
    if (test2) { passed = passed + 1; }
    if (test3) { passed = passed + 1; }
    if (test4) { passed = passed + 1; }
    if (test5) { passed = passed + 1; }

    print("===== Summary =====");
    print("Tests passed: " + str(passed) + "/5");

    if (passed == 5) {
        print("All tests PASSED!");
        return 0;
    } else {
        print("Some tests FAILED!");
        return 1;
    }
}

main();
