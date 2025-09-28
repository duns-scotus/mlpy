// Test the best safe_append implementation

function safe_append(arr, item) {
    // Handle arrays up to reasonable size with explicit returns
    if (arr.length == 0) {
        return [item];
    } elif (arr.length == 1) {
        return [arr[0], item];
    } elif (arr.length == 2) {
        return [arr[0], arr[1], item];
    } elif (arr.length == 3) {
        return [arr[0], arr[1], arr[2], item];
    } elif (arr.length == 4) {
        return [arr[0], arr[1], arr[2], arr[3], item];
    } elif (arr.length == 5) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], item];
    } elif (arr.length == 6) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], item];
    } elif (arr.length == 7) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], item];
    } elif (arr.length == 8) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], item];
    } elif (arr.length == 9) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], item];
    } elif (arr.length == 10) {
        return [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], item];
    } else {
        // For larger arrays, just return the original (limitation)
        print("Warning: Array too large for safe_append, max size 10");
        return arr;
    }
}

function main() {
    print("=== Testing Best Safe Append ===");

    // Test with different sizes
    arr1 = [];
    result1 = safe_append(arr1, 1);
    print("Empty + 1: " + (result1 + ""));

    arr2 = [1, 2];
    result2 = safe_append(arr2, 3);
    print("Two + 3: " + (result2 + ""));

    arr5 = [1, 2, 3, 4, 5];
    result5 = safe_append(arr5, 6);
    print("Five + 6: " + (result5 + ""));

    // Test chaining
    start = [1];
    step1 = safe_append(start, 2);
    step2 = safe_append(step1, 3);
    step3 = safe_append(step2, 4);
    print("Chained appends: " + (step3 + ""));

    print("=== Test Complete ===");
}

main();