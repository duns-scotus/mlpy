// Test core language: Quicksort algorithm
// Features tested: recursion, arrays, indexing, comparison operators, try/except
// NO external function calls - pure language features only

// Helper: get array length using try/except
function get_length(arr) {
    len = 0;
    try {
        i = 0;
        while (true) {
            temp = arr[i];
            i = i + 1;
            len = len + 1;
        }
    } except (e) {
        // Index out of bounds, we found the length
    }
    return len;
}

// Helper: append item to array by creating new array
function append(arr, item) {
    // Use array concatenation instead of indexing
    return arr + [item];
}

// Helper: concatenate two arrays
function concat(arr1, arr2) {
    // Use array concatenation
    return arr1 + arr2;
}

// Helper: copy array by building new array
function copy_array(arr) {
    len = get_length(arr);
    result = [];
    i = 0;
    while (i < len) {
        result = result + [arr[i]];
        i = i + 1;
    }
    return result;
}

// Quicksort implementation
function quicksort(arr) {
    len = get_length(arr);

    if (len <= 1) {
        return arr;
    }

    pivot_index = len // 2;
    pivot = arr[pivot_index];

    less = [];
    equal = [];
    greater = [];

    i = 0;
    while (i < len) {
        if (arr[i] < pivot) {
            less = append(less, arr[i]);
        } elif (arr[i] == pivot) {
            equal = append(equal, arr[i]);
        } else {
            greater = append(greater, arr[i]);
        }
        i = i + 1;
    }

    sorted_less = quicksort(less);
    sorted_greater = quicksort(greater);

    result = concat(sorted_less, equal);
    result = concat(result, sorted_greater);

    return result;
}

// Bubble sort for comparison
function bubble_sort(arr) {
    len = get_length(arr);

    if (len <= 1) {
        return arr;
    }

    // Copy array using helper
    result = copy_array(arr);

    n = len;
    swapped = true;

    while (swapped) {
        swapped = false;
        i = 1;
        while (i < n) {
            if (result[i - 1] > result[i]) {
                temp = result[i - 1];
                result[i - 1] = result[i];
                result[i] = temp;
                swapped = true;
            }
            i = i + 1;
        }
        n = n - 1;
    }

    return result;
}

// Selection sort
function selection_sort(arr) {
    len = get_length(arr);

    if (len <= 1) {
        return arr;
    }

    // Copy array using helper
    result = copy_array(arr);

    i = 0;
    while (i < len - 1) {
        min_idx = i;
        j = i + 1;

        while (j < len) {
            if (result[j] < result[min_idx]) {
                min_idx = j;
            }
            j = j + 1;
        }

        if (min_idx != i) {
            temp = result[i];
            result[i] = result[min_idx];
            result[min_idx] = temp;
        }

        i = i + 1;
    }

    return result;
}

// Merge two sorted arrays
function merge(left, right) {
    left_len = get_length(left);
    right_len = get_length(right);
    result = [];
    i = 0;
    j = 0;

    while (i < left_len && j < right_len) {
        if (left[i] <= right[j]) {
            result = result + [left[i]];
            i = i + 1;
        } else {
            result = result + [right[j]];
            j = j + 1;
        }
    }

    while (i < left_len) {
        result = result + [left[i]];
        i = i + 1;
    }

    while (j < right_len) {
        result = result + [right[j]];
        j = j + 1;
    }

    return result;
}

// Merge sort
function merge_sort(arr) {
    len = get_length(arr);

    if (len <= 1) {
        return arr;
    }

    mid = len // 2;

    // Build left array
    left = [];
    i = 0;
    while (i < mid) {
        left = left + [arr[i]];
        i = i + 1;
    }

    // Build right array
    right = [];
    j = 0;
    while (mid + j < len) {
        right = right + [arr[mid + j]];
        j = j + 1;
    }

    sorted_left = merge_sort(left);
    sorted_right = merge_sort(right);

    return merge(sorted_left, sorted_right);
}

// Main test function
function main() {
    test_array = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50, 23, 36, 18, 77];

    results = {};
    results.original = test_array;
    results.quicksort = quicksort(test_array);
    results.bubble = bubble_sort(test_array);
    results.selection = selection_sort(test_array);
    results.merge = merge_sort(test_array);

    // Test with already sorted array
    sorted_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    results.sorted_quick = quicksort(sorted_array);

    // Test with reverse sorted array
    reverse_array = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1];
    results.reverse_quick = quicksort(reverse_array);

    // Test with single element
    single = [42];
    results.single = quicksort(single);

    // Test with duplicates
    duplicates = [5, 2, 8, 2, 9, 1, 5, 5];
    results.duplicates = quicksort(duplicates);

    return results;
}

// Run tests
test_results = main();
