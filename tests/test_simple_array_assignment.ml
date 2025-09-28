// Simple test for array assignment patterns

function safe_append(arr, item) {
    arr[arr.length] = item;
    return arr;
}

function main() {
    print("=== Testing Array Assignment ===");

    // Test 1: Direct assignment to length index
    test_array = [1, 2, 3];
    print("Before: " + (test_array + ""));

    test_array[test_array.length] = 4;
    print("After direct assignment: " + (test_array + ""));

    // Test 2: Using safe_append function
    test_array2 = [1, 2, 3];
    print("Before safe_append: " + (test_array2 + ""));

    safe_append(test_array2, 4);
    print("After safe_append: " + (test_array2 + ""));

    print("=== Test Complete ===");
}

main();