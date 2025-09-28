// Test array append with pre-allocated arrays

function main() {
    print("=== Testing Array Append with Pre-allocation ===");

    // Test 1: Pre-allocate with known size
    test_array = [1, 2, 3];
    print("Original: " + (test_array + ""));

    // Pre-allocate new array with enough elements
    new_arr = [null, null, null, null];
    i = 0;
    while (i < test_array.length) {
        new_arr[i] = test_array[i];
        i = i + 1;
    }
    new_arr[i] = 4;
    print("Pre-allocated append: " + (new_arr + ""));

    // Test 2: Use string concatenation approach (build a new array)
    function array_append(arr, item) {
        // Since we can't dynamically resize, we'll create a new array with known size
        if (arr.length == 1) {
            return [arr[0], item];
        } elif (arr.length == 2) {
            return [arr[0], arr[1], item];
        } elif (arr.length == 3) {
            return [arr[0], arr[1], arr[2], item];
        } elif (arr.length == 4) {
            return [arr[0], arr[1], arr[2], arr[3], item];
        } elif (arr.length == 5) {
            return [arr[0], arr[1], arr[2], arr[3], arr[4], item];
        } else {
            // Fallback for larger arrays - just return original
            return arr;
        }
    }

    test_array2 = [10, 20];
    result2 = array_append(test_array2, 30);
    print("Function append: " + (result2 + ""));

    test_array3 = [100, 200, 300];
    result3 = array_append(test_array3, 400);
    print("Function append 3: " + (result3 + ""));

    print("=== Test Complete ===");
}

main();