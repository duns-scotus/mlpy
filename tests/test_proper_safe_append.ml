// Test proper safe_append using collections module

import collections;

function safe_append(arr, item) {
    // Use collections.append which should handle any array size
    return collections.append(arr, item);
}

function main() {
    print("=== Testing Proper Safe Append ===");

    // Test with different sizes
    empty = [];
    result1 = safe_append(empty, 1);
    print("Empty + 1: " + (result1 + ""));

    small = [1, 2, 3];
    result2 = safe_append(small, 4);
    print("Small + 4: " + (result2 + ""));

    medium = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    result3 = safe_append(medium, 11);
    print("Medium + 11: " + (result3 + ""));

    // Test chaining
    start = [1];
    step1 = safe_append(start, 2);
    step2 = safe_append(step1, 3);
    step3 = safe_append(step2, 4);
    step4 = safe_append(step3, 5);
    print("Chained appends: " + (step4 + ""));

    // Test with different data types
    mixed = ["hello", 42];
    result4 = safe_append(mixed, true);
    print("Mixed types: " + (result4 + ""));

    print("=== Test Complete ===");
}

main();