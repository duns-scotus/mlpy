// bubble.ml - Bubble Sort Algorithm
// Simple comparison-based sorting algorithm

function bubble_sort(arr) {
    n = len(arr);
    i = 0;

    while (i < n - 1) {
        j = 0;
        swapped = false;

        while (j < n - i - 1) {
            if (arr[j] > arr[j + 1]) {
                // Swap elements
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                swapped = true;
            }
            j = j + 1;
        }

        // If no swaps occurred, array is sorted
        if (swapped == false) {
            return arr;
        }

        i = i + 1;
    }

    return arr;
}

// Optimized bubble sort with early termination
function bubble_sort_optimized(arr) {
    n = len(arr);

    i = 0;
    while (i < n - 1) {
        last_swap = 0;
        j = 0;

        while (j < n - i - 1) {
            if (arr[j] > arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                last_swap = j;
            }
            j = j + 1;
        }

        // If no swaps, we're done
        if (last_swap == 0) {
            return arr;
        }

        i = i + 1;
    }

    return arr;
}
