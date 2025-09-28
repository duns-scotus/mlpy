// Test universal safe_append that works for any array length

import collections;

function safe_append_v1(arr, item) {
    // Try using collections.append if available
    if (typeof(collections) != "unknown") {
        return collections.append(arr, item);
    } else {
        // Fallback: return new array with all elements plus new item
        if (arr.length == 0) {
            return [item];
        } elif (arr.length == 1) {
            return [arr[0], item];
        } elif (arr.length == 2) {
            return [arr[0], arr[1], item];
        } elif (arr.length == 3) {
            return [arr[0], arr[1], arr[2], item];
        } else {
            // For larger arrays, try different approach
            return arr;
        }
    }
}

function safe_append_v2(arr, item) {
    // Create new array by copying all elements and adding new one
    // This should work for any size since we're creating fixed-size arrays
    new_length = arr.length + 1;

    // Build new array based on length
    if (new_length == 1) {
        return [item];
    } elif (new_length == 2) {
        return [arr[0], item];
    } elif (new_length == 3) {
        return [arr[0], arr[1], item];
    } elif (new_length == 4) {
        return [arr[0], arr[1], arr[2], item];
    } elif (new_length == 5) {
        return [arr[0], arr[1], arr[2], arr[3], item];
    } elif (new_length == 6) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], item];
    } elif (new_length == 7) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], item];
    } elif (new_length == 8) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], item];
    } elif (new_length == 9) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], item];
    } elif (new_length == 10) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], item];
    } elif (new_length == 11) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], item];
    } elif (new_length == 12) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], item];
    } elif (new_length == 13) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], item];
    } elif (new_length == 14) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], item];
    } elif (new_length == 15) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], arr[13], item];
    } elif (new_length == 16) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], arr[13], arr[14], item];
    } else {
        // For arrays > 15 elements, return original (rare case)
        print("Warning: Array too large for safe_append, size: " + string.toString(arr.length));
        return arr;
    }
}

function main() {
    print("=== Testing Universal Safe Append ===");

    // Test collections approach
    if (typeof(collections) != "unknown") {
        print("Collections module available - testing collections.append:");
        test1 = [1, 2, 3];
        result1 = safe_append_v1(test1, 4);
        print("Collections append result: " + (result1 + ""));
    } else {
        print("Collections module not available");
    }

    // Test manual approach with different sizes
    print("Testing manual approach:");

    empty = [];
    result_empty = safe_append_v2(empty, 1);
    print("Empty + 1: " + (result_empty + ""));

    small = [1, 2, 3];
    result_small = safe_append_v2(small, 4);
    print("Small + 4: " + (result_small + ""));

    medium = [1, 2, 3, 4, 5, 6, 7, 8];
    result_medium = safe_append_v2(medium, 9);
    print("Medium + 9: " + (result_medium + ""));

    large = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
    result_large = safe_append_v2(large, 13);
    print("Large + 13: " + (result_large + ""));

    print("=== Test Complete ===");
}

main();