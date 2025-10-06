// sorting.ml - Generic sorting utilities
// Provides common sorting operations and utilities

// Swap elements at two indices in an array
function swap(arr, i, j) {
    temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}

// Check if array is sorted in ascending order
function is_sorted(arr) {
    i = 0;
    while (i < len(arr) - 1) {
        if (arr[i] > arr[i + 1]) {
            return false;
        }
        i = i + 1;
    }
    return true;
}

// Find minimum element in array
function find_min(arr) {
    if (len(arr) == 0) {
        return null;
    }

    min_val = arr[0];
    i = 1;
    while (i < len(arr)) {
        if (arr[i] < min_val) {
            min_val = arr[i];
        }
        i = i + 1;
    }
    return min_val;
}

// Find maximum element in array
function find_max(arr) {
    if (len(arr) == 0) {
        return null;
    }

    max_val = arr[0];
    i = 1;
    while (i < len(arr)) {
        if (arr[i] > max_val) {
            max_val = arr[i];
        }
        i = i + 1;
    }
    return max_val;
}

// Simple selection sort (for small arrays)
function selection_sort(arr) {
    n = len(arr);
    i = 0;
    while (i < n - 1) {
        min_idx = i;
        j = i + 1;
        while (j < n) {
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
            j = j + 1;
        }
        if (min_idx != i) {
            swap(arr, i, min_idx);
        }
        i = i + 1;
    }
    return arr;
}

// Reverse an array in place
function reverse(arr) {
    left = 0;
    right = len(arr) - 1;
    while (left < right) {
        swap(arr, left, right);
        left = left + 1;
        right = right - 1;
    }
    return arr;
}

// Sort in descending order
function sort_descending(arr) {
    selection_sort(arr);
    return reverse(arr);
}
