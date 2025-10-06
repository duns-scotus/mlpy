// heapsort.ml - HeapSort Algorithm
// Efficient sorting algorithm using binary heap data structure

function heapify(arr, n, i) {
    largest = i;
    left = 2 * i + 1;
    right = 2 * i + 2;

    // If left child is larger than root
    if (left < n) {
        if (arr[left] > arr[largest]) {
            largest = left;
        }
    }

    // If right child is larger than largest so far
    if (right < n) {
        if (arr[right] > arr[largest]) {
            largest = right;
        }
    }

    // If largest is not root
    if (largest != i) {
        // Swap
        temp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = temp;

        // Recursively heapify the affected sub-tree
        heapify(arr, n, largest);
    }
}

function heapsort(arr) {
    n = len(arr);

    // Build max heap
    i = int(n / 2) - 1;
    while (i >= 0) {
        heapify(arr, n, i);
        i = i - 1;
    }

    // Extract elements from heap one by one
    i = n - 1;
    while (i > 0) {
        // Move current root to end
        temp = arr[0];
        arr[0] = arr[i];
        arr[i] = temp;

        // Call heapify on the reduced heap
        heapify(arr, i, 0);

        i = i - 1;
    }

    return arr;
}

// Build a min heap instead of max heap
function heapify_min(arr, n, i) {
    smallest = i;
    left = 2 * i + 1;
    right = 2 * i + 2;

    if (left < n) {
        if (arr[left] < arr[smallest]) {
            smallest = left;
        }
    }

    if (right < n) {
        if (arr[right] < arr[smallest]) {
            smallest = right;
        }
    }

    if (smallest != i) {
        temp = arr[i];
        arr[i] = arr[smallest];
        arr[smallest] = temp;
        heapify_min(arr, n, smallest);
    }
}

function heapsort_descending(arr) {
    n = len(arr);

    // Build min heap
    i = int(n / 2) - 1;
    while (i >= 0) {
        heapify_min(arr, n, i);
        i = i - 1;
    }

    // Extract elements from heap
    i = n - 1;
    while (i > 0) {
        temp = arr[0];
        arr[0] = arr[i];
        arr[i] = temp;
        heapify_min(arr, i, 0);
        i = i - 1;
    }

    return arr;
}
