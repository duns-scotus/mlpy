// ============================================
// Example: Array Techniques
// Category: tutorial
// Demonstrates: Advanced array operations and patterns
// ============================================

import console;

// Combining arrays
console.log("=== Combining Arrays ===");
arr1 = [1, 2, 3];
arr2 = [4, 5, 6];
combined = arr1 + arr2;
console.log("Array 1: " + str(arr1));
console.log("Array 2: " + str(arr2));
console.log("Combined: " + str(combined));

// Building arrays incrementally
console.log("");
console.log("=== Building Arrays ===");
result = [];
result = result + [10];
result = result + [20];
result = result + [30];
console.log("Built array: " + str(result));

// Processing arrays with functions
function multiplyBy(arr, factor) {
    output = [];
    for (value in arr) {
        output = output + [value * factor];
    }
    return output;
}

console.log("");
console.log("=== Array Transformation ===");
numbers = [1, 2, 3, 4, 5];
doubled = multiplyBy(numbers, 2);
tripled = multiplyBy(numbers, 3);
console.log("Original: " + str(numbers));
console.log("Doubled: " + str(doubled));
console.log("Tripled: " + str(tripled));

// Filtering arrays
function filterGreaterThan(arr, threshold) {
    filtered = [];
    for (value in arr) {
        if (value > threshold) {
            filtered = filtered + [value];
        }
    }
    return filtered;
}

console.log("");
console.log("=== Array Filtering ===");
values = [5, 15, 8, 23, 12, 30, 7];
aboveTen = filterGreaterThan(values, 10);
aboveTwenty = filterGreaterThan(values, 20);
console.log("All values: " + str(values));
console.log("Above 10: " + str(aboveTen));
console.log("Above 20: " + str(aboveTwenty));

// Finding elements
function findFirstMatch(arr, target) {
    for (value in arr) {
        if (value == target) {
            return value;
        }
    }
    return -1;
}

console.log("");
console.log("=== Array Search ===");
searchList = [10, 20, 30, 40, 50];
found = findFirstMatch(searchList, 30);
notFound = findFirstMatch(searchList, 99);
console.log("Search in: " + str(searchList));
console.log("Find 30: " + str(found));
console.log("Find 99: " + str(notFound));

// Partitioning arrays
function partition(arr, predicate) {
    passed = [];
    failed = [];
    for (value in arr) {
        if (predicate(value)) {
            passed = passed + [value];
        } else {
            failed = failed + [value];
        }
    }
    return {passed: passed, failed: failed};
}

function isEven(n) {
    return n % 2 == 0;
}

console.log("");
console.log("=== Array Partitioning ===");
allNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
groups = partition(allNumbers, isEven);
console.log("All numbers: " + str(allNumbers));
console.log("Even numbers: " + str(groups.passed));
console.log("Odd numbers: " + str(groups.failed));
