// quicksort.ml - QuickSort Algorithm
// Efficient divide-and-conquer sorting algorithm

function partition(arr, low, high) {
    pivot = arr[high];
    i = low - 1;

    j = low;
    while (j < high) {
        if (arr[j] <= pivot) {
            i = i + 1;
            // Swap arr[i] and arr[j]
            temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
        j = j + 1;
    }

    // Swap arr[i+1] and arr[high] (pivot)
    temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;

    return i + 1;
}

function quicksort_helper(arr, low, high) {
    if (low < high) {
        pi = partition(arr, low, high);
        quicksort_helper(arr, low, pi - 1);
        quicksort_helper(arr, pi + 1, high);
    }
}

function quicksort(arr) {
    if (len(arr) <= 1) {
        return arr;
    }
    quicksort_helper(arr, 0, len(arr) - 1);
    return arr;
}

// Three-way partitioning for duplicate values
function quicksort_3way(arr, low, high) {
    if (low >= high) {
        return;
    }

    pivot = arr[low];
    lt = low;
    gt = high;
    i = low + 1;

    while (i <= gt) {
        if (arr[i] < pivot) {
            // Swap arr[lt] and arr[i]
            temp = arr[lt];
            arr[lt] = arr[i];
            arr[i] = temp;
            lt = lt + 1;
            i = i + 1;
        } elif (arr[i] > pivot) {
            // Swap arr[i] and arr[gt]
            temp = arr[i];
            arr[i] = arr[gt];
            arr[gt] = temp;
            gt = gt - 1;
        } else {
            i = i + 1;
        }
    }

    quicksort_3way(arr, low, lt - 1);
    quicksort_3way(arr, gt + 1, high);
}

function quicksort_with_duplicates(arr) {
    if (len(arr) <= 1) {
        return arr;
    }
    quicksort_3way(arr, 0, len(arr) - 1);
    return arr;
}
