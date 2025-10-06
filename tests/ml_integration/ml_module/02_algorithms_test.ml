// Test: User Module Import - Algorithm Submodules
// Tests importing and using algorithm submodules (bubble, quicksort, heapsort)

import user_modules.algorithms.bubble;
import user_modules.algorithms.quicksort;
import user_modules.algorithms.heapsort;

function verify_sorted(arr) {
    i = 0;
    while (i < len(arr) - 1) {
        if (arr[i] > arr[i + 1]) {
            return false;
        }
        i = i + 1;
    }
    return true;
}

function test_bubble_sort() {
    arr = [64, 34, 25, 12, 22, 11, 90];

    print("Testing bubble_sort:");
    print("  Before: [64, 34, 25, 12, 22, 11, 90]");

    sorted_arr = user_modules.algorithms.bubble.bubble_sort(arr);

    print("  After: " + str(sorted_arr));

    is_sorted = verify_sorted(sorted_arr);

    if (is_sorted == true) {
        if (sorted_arr[0] == 11) {
            if (sorted_arr[len(sorted_arr) - 1] == 90) {
                return true;
            }
        }
    }
    return false;
}

function test_bubble_sort_optimized() {
    arr = [5, 2, 9, 1, 5, 6];

    print("Testing bubble_sort_optimized:");
    print("  Before: [5, 2, 9, 1, 5, 6]");

    sorted_arr = user_modules.algorithms.bubble.bubble_sort_optimized(arr);

    print("  After: " + str(sorted_arr));

    is_sorted = verify_sorted(sorted_arr);

    if (is_sorted == true) {
        if (sorted_arr[0] == 1) {
            return true;
        }
    }
    return false;
}

function test_quicksort() {
    arr = [10, 7, 8, 9, 1, 5];

    print("Testing quicksort:");
    print("  Before: [10, 7, 8, 9, 1, 5]");

    sorted_arr = user_modules.algorithms.quicksort.quicksort(arr);

    print("  After: " + str(sorted_arr));

    is_sorted = verify_sorted(sorted_arr);

    if (is_sorted == true) {
        if (sorted_arr[0] == 1) {
            if (sorted_arr[len(sorted_arr) - 1] == 10) {
                return true;
            }
        }
    }
    return false;
}

function test_quicksort_with_duplicates() {
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3];

    print("Testing quicksort_with_duplicates:");
    print("  Before: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]");

    sorted_arr = user_modules.algorithms.quicksort.quicksort_with_duplicates(arr);

    print("  After: " + str(sorted_arr));

    is_sorted = verify_sorted(sorted_arr);

    if (is_sorted == true) {
        return true;
    }
    return false;
}

function test_heapsort() {
    arr = [12, 11, 13, 5, 6, 7];

    print("Testing heapsort:");
    print("  Before: [12, 11, 13, 5, 6, 7]");

    sorted_arr = user_modules.algorithms.heapsort.heapsort(arr);

    print("  After: " + str(sorted_arr));

    is_sorted = verify_sorted(sorted_arr);

    if (is_sorted == true) {
        if (sorted_arr[0] == 5) {
            if (sorted_arr[len(sorted_arr) - 1] == 13) {
                return true;
            }
        }
    }
    return false;
}

function test_heapsort_descending() {
    arr = [4, 10, 3, 5, 1];

    print("Testing heapsort_descending:");
    print("  Before: [4, 10, 3, 5, 1]");

    sorted_arr = user_modules.algorithms.heapsort.heapsort_descending(arr);

    print("  After: " + str(sorted_arr));

    // Check descending order
    i = 0;
    is_desc = true;
    while (i < len(sorted_arr) - 1) {
        if (sorted_arr[i] < sorted_arr[i + 1]) {
            is_desc = false;
        }
        i = i + 1;
    }

    if (is_desc == true) {
        if (sorted_arr[0] == 10) {
            if (sorted_arr[len(sorted_arr) - 1] == 1) {
                return true;
            }
        }
    }
    return false;
}

function main() {
    print("===== User Module Test: Algorithm Submodules =====");
    print("");

    test1 = test_bubble_sort();
    print("Test 1 (bubble_sort): " + str(test1));
    print("");

    test2 = test_bubble_sort_optimized();
    print("Test 2 (bubble_sort_optimized): " + str(test2));
    print("");

    test3 = test_quicksort();
    print("Test 3 (quicksort): " + str(test3));
    print("");

    test4 = test_quicksort_with_duplicates();
    print("Test 4 (quicksort_with_duplicates): " + str(test4));
    print("");

    test5 = test_heapsort();
    print("Test 5 (heapsort): " + str(test5));
    print("");

    test6 = test_heapsort_descending();
    print("Test 6 (heapsort_descending): " + str(test6));
    print("");

    // Count passing tests
    passed = 0;
    if (test1) { passed = passed + 1; }
    if (test2) { passed = passed + 1; }
    if (test3) { passed = passed + 1; }
    if (test4) { passed = passed + 1; }
    if (test5) { passed = passed + 1; }
    if (test6) { passed = passed + 1; }

    print("===== Summary =====");
    print("Tests passed: " + str(passed) + "/6");

    if (passed == 6) {
        print("All tests PASSED!");
        return 0;
    } else {
        print("Some tests FAILED!");
        return 1;
    }
}

main();
