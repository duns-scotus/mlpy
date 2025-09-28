// Test different approaches to array assignment

function main() {
    print("=== Testing Array Assignment Approaches ===");

    // Approach 1: Direct dynamic assignment (known to fail)
    print("1. Testing direct dynamic assignment:");
    test_array1 = [1, 2, 3];
    try {
        test_array1[test_array1.length] = 4;
        print("Direct assignment SUCCESS: " + (test_array1 + ""));
    } except error {
        print("Direct assignment FAILED: " + (error + ""));
    }

    // Approach 2: Copy to new array with known indices
    print("2. Testing copy to new array:");
    test_array2 = [1, 2, 3];
    try {
        new_arr = [];
        i = 0;
        while (i < test_array2.length) {
            new_arr[i] = test_array2[i];
            i = i + 1;
        }
        new_arr[i] = 4;
        print("Copy approach SUCCESS: " + (new_arr + ""));
    } except error {
        print("Copy approach FAILED: " + (error + ""));
    }

    // Approach 3: Pre-populate array with nulls
    print("3. Testing pre-populated array:");
    test_array3 = [1, 2, 3];
    try {
        // Create new array with known size
        new_size = test_array3.length + 1;
        prepop_arr = [null, null, null, null];  // Known size
        i = 0;
        while (i < test_array3.length) {
            prepop_arr[i] = test_array3[i];
            i = i + 1;
        }
        prepop_arr[test_array3.length] = 4;
        print("Pre-populated SUCCESS: " + (prepop_arr + ""));
    } except error {
        print("Pre-populated FAILED: " + (error + ""));
    }

    // Approach 4: Use safe_append function with mutation
    print("4. Testing safe_append with mutation:");
    test_array4 = [1, 2, 3];
    function safe_append_mut(arr, item) {
        // Try to mutate original array by copying all elements
        new_arr = [];
        i = 0;
        while (i < arr.length) {
            new_arr[i] = arr[i];
            i = i + 1;
        }
        new_arr[i] = item;

        // Copy back to original array (if possible)
        j = 0;
        while (j < new_arr.length) {
            if (j < arr.length) {
                arr[j] = new_arr[j];
            }
            j = j + 1;
        }
        return new_arr;
    }

    try {
        result = safe_append_mut(test_array4, 4);
        print("Safe append SUCCESS: " + (result + ""));
        print("Original array: " + (test_array4 + ""));
    } except error {
        print("Safe append FAILED: " + (error + ""));
    }

    // Approach 5: Simply return new array (functional approach)
    print("5. Testing functional safe_append:");
    test_array5 = [1, 2, 3];
    function safe_append_func(arr, item) {
        new_arr = [];
        i = 0;
        while (i < arr.length) {
            new_arr[i] = arr[i];
            i = i + 1;
        }
        new_arr[i] = item;
        return new_arr;
    }

    try {
        result5 = safe_append_func(test_array5, 4);
        print("Functional append SUCCESS: " + (result5 + ""));
    } except error {
        print("Functional append FAILED: " + (error + ""));
    }

    print("=== Array Assignment Test Complete ===");
}

main();