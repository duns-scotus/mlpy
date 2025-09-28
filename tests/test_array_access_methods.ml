// Test file to verify array access methods
// Testing both object.property and direct assignment approaches

import array;
import collections;

function safe_append(arr, item) {
    arr[arr.length] = item;
    return arr;
}

function main() {
    print("=== Testing Array Access Methods ===");

    test_array = [1, 2, 3, 4, 5];

    // Test 1: Direct property access
    print("Testing direct property access:");
    try {
        // This should work according to grammar
        direct_length = test_array.length;
        print("Direct length access: " + (direct_length + ""));
    } except (error) {
        print("Direct length access FAILED: " + (error + ""));
    }

    // Test 2: Module function access
    print("Testing module function access:");
    try {
        // Using collections or array module
        if (typeof(collections) != "unknown") {
            module_length = collections.length(test_array);
            print("Collections length: " + (module_length + ""));
        } else {
            print("Collections module not available");
        }
    } except (error) {
        print("Module length access FAILED: " + (error + ""));
    }

    // Test 3: Array assignment pattern (the problematic one)
    print("Testing array assignment patterns:");

    // Method 1: Direct assignment to length index
    test_array1 = [1, 2, 3];
    try {
        print("Before assignment: " + (test_array1 + ""));
        test_array1[test_array1.length] = 4;
        print("After direct assignment: " + (test_array1 + ""));
    } except (error) {
        print("Direct assignment FAILED: " + (error + ""));
    }

    // Method 2: Using safe_append function
    test_array2 = [1, 2, 3];
    try {
        print("Before safe_append: " + (test_array2 + ""));
        safe_append(test_array2, 4);
        print("After safe_append: " + (test_array2 + ""));
    } except (error) {
        print("Safe_append FAILED: " + (error + ""));
    }

    // Method 3: Using index assignment with known index
    test_array3 = [1, 2, 3];
    try {
        print("Before known index: " + (test_array3 + ""));
        test_array3[3] = 4;
        print("After known index assignment: " + (test_array3 + ""));
    } except (error) {
        print("Known index assignment FAILED: " + (error + ""));
    }

    // Test 4: Array methods if available
    print("Testing array methods:");
    try {
        // Test if push method exists
        test_array4 = [1, 2, 3];
        if (typeof(test_array4.push) == "function") {
            test_array4.push(4);
            print("Push method worked: " + (test_array4 + ""));
        } else {
            print("Push method not available");
        }
    } except (error) {
        print("Push method FAILED: " + (error + ""));
    }

    print("=== Array Access Methods Test Complete ===");
}

main();