// Test safe_upsert that updates existing index or appends

import collections;

function safe_upsert(arr, pos, item) {
    // If position exists in array, update it
    if (pos < arr.length) {
        // Create new array with updated value at position
        new_arr = [];
        i = 0;
        while (i < arr.length) {
            if (i == pos) {
                new_arr = collections.append(new_arr, item);
            } else {
                new_arr = collections.append(new_arr, arr[i]);
            }
            i = i + 1;
        }
        return new_arr;
    } else {
        // Position is beyond array length, append item
        return collections.append(arr, item);
    }
}

// For the common case of arr[arr.length] = item, we can use:
function safe_append(arr, item) {
    return safe_upsert(arr, arr.length, item);
}

function main() {
    print("=== Testing Safe Upsert ===");

    // Test updating existing position
    arr1 = [1, 2, 3, 4, 5];
    result1 = safe_upsert(arr1, 2, 99);  // Update position 2
    print("Update pos 2: " + (result1 + ""));

    // Test updating first position
    arr2 = [10, 20, 30];
    result2 = safe_upsert(arr2, 0, 100);  // Update position 0
    print("Update pos 0: " + (result2 + ""));

    // Test updating last position
    arr3 = [1, 2, 3];
    result3 = safe_upsert(arr3, 2, 300);  // Update last position
    print("Update last pos: " + (result3 + ""));

    // Test appending (position beyond array length)
    arr4 = [1, 2, 3];
    result4 = safe_upsert(arr4, 3, 4);  // pos 3 = arr.length, so append
    print("Append at length: " + (result4 + ""));

    result5 = safe_upsert(arr4, 5, 6);  // pos 5 > arr.length, so append
    print("Append beyond length: " + (result5 + ""));

    // Test the common safe_append pattern
    arr6 = [1, 2, 3];
    result6 = safe_append(arr6, 4);  // Equivalent to arr[arr.length] = 4
    print("Safe append: " + (result6 + ""));

    // Test chaining upserts
    start = [1, 2, 3];
    step1 = safe_upsert(start, 1, 20);    // Update position 1
    step2 = safe_upsert(step1, 3, 4);     // Append at end
    step3 = safe_upsert(step2, 0, 10);    // Update position 0
    print("Chained upserts: " + (step3 + ""));

    print("=== Test Complete ===");
}

main();