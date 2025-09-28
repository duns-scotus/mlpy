// Simple test for array append approaches

function main() {
    print("=== Testing Array Append ===");

    // Approach 1: Copy to new array (should work)
    test_array = [1, 2, 3];
    print("Original: " + (test_array + ""));

    new_arr = [];
    i = 0;
    while (i < test_array.length) {
        new_arr[i] = test_array[i];
        i = i + 1;
    }
    new_arr[i] = 4;
    print("After copy append: " + (new_arr + ""));

    // Approach 2: Functional safe_append
    function safe_append(arr, item) {
        result = [];
        j = 0;
        while (j < arr.length) {
            result[j] = arr[j];
            j = j + 1;
        }
        result[j] = item;
        return result;
    }

    test_array2 = [10, 20, 30];
    result2 = safe_append(test_array2, 40);
    print("Functional append: " + (result2 + ""));

    print("=== Test Complete ===");
}

main();