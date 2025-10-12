// Sorting algorithms for debugging tests
// Tests: nested loops, array mutations, complex logic

function bubble_sort(list) {
    len = 0;
    for (item in list) {
        len = len + 1;
    }

    // Make a copy
    result = [];
    for (item in list) {
        result = result + [item];
    }

    n = len;
    i = 0;
    while (i < n - 1) {
        j = 0;
        while (j < n - i - 1) {
            if (result[j] > result[j + 1]) {
                // Swap
                temp = result[j];
                result[j] = result[j + 1];
                result[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }

    return result;
}

function selection_sort(list) {
    len = 0;
    for (item in list) {
        len = len + 1;
    }

    // Make a copy
    result = [];
    for (item in list) {
        result = result + [item];
    }

    i = 0;
    while (i < len - 1) {
        // Find minimum in remaining array
        min_idx = i;
        j = i + 1;
        while (j < len) {
            if (result[j] < result[min_idx]) {
                min_idx = j;
            }
            j = j + 1;
        }

        // Swap
        if (min_idx != i) {
            temp = result[i];
            result[i] = result[min_idx];
            result[min_idx] = temp;
        }

        i = i + 1;
    }

    return result;
}

function insertion_sort(list) {
    len = 0;
    for (item in list) {
        len = len + 1;
    }

    // Make a copy
    result = [];
    for (item in list) {
        result = result + [item];
    }

    i = 1;
    while (i < len) {
        key = result[i];
        j = i - 1;

        while (j >= 0 && result[j] > key) {
            result[j + 1] = result[j];
            j = j - 1;
        }

        result[j + 1] = key;
        i = i + 1;
    }

    return result;
}

function is_sorted(list) {
    len = 0;
    for (item in list) {
        len = len + 1;
    }

    if (len <= 1) {
        return true;
    }

    i = 0;
    while (i < len - 1) {
        if (list[i] > list[i + 1]) {
            return false;
        }
        i = i + 1;
    }

    return true;
}
