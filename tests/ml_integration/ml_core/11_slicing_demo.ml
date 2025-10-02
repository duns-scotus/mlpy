// Demonstration: Python-style slicing does NOT parse in ML
// This file should FAIL to parse, showing ML grammar limitations
// NO external function calls - attempting pure Python slice syntax

function test_slicing() {
    arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100];

    // Basic slicing - arr[start:end]
    slice1 = arr[1:4];      // Should get [20, 30, 40]
    slice2 = arr[0:3];      // Should get [10, 20, 30]

    // Open-ended slicing
    slice3 = arr[:5];       // Should get first 5 elements
    slice4 = arr[3:];       // Should get from index 3 to end
    slice5 = arr[:];        // Should get entire array copy

    // Negative indexing
    last = arr[-1];         // Should get last element (100)
    second_last = arr[-2];  // Should get second to last (90)

    // Negative slicing
    slice6 = arr[-3:-1];    // Should get [80, 90]
    slice7 = arr[-5:];      // Should get last 5 elements

    // Step notation
    slice8 = arr[::2];      // Every 2nd element
    slice9 = arr[1::2];     // Every 2nd element starting from index 1
    slice10 = arr[::-1];    // Reverse array

    return {
        slice1: slice1,
        slice2: slice2,
        slice3: slice3,
        slice4: slice4,
        slice5: slice5,
        last: last,
        second_last: second_last,
        slice6: slice6,
        slice7: slice7,
        slice8: slice8,
        slice9: slice9,
        slice10: slice10
    };
}

// Run test
result = test_slicing();
