// ============================================
// Example: List Operations
// Category: standard-library/functional
// Demonstrates: take, drop, chunk, flatten, reverse, unique, range, repeat, groupBy
// ============================================

import console;
import functional;

console.log("=== List Operations ===\n");

// ============================================
// Range - Generate Number Sequences
// ============================================

console.log("=== Range (generate sequences) ===");

range10 = functional.range(10);
console.log("range(10): " + str(range10));

range5to15 = functional.range(5, 15);
console.log("range(5, 15): " + str(range5to15));

rangeStep = functional.range(0, 20, 3);
console.log("range(0, 20, 3): " + str(rangeStep));

// ============================================
// Take - Get First N Elements
// ============================================

console.log("\n=== Take (first N) ===");

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
console.log("List: " + str(numbers));

firstFive = functional.take(5, numbers);
console.log("Take 5: " + str(firstFive));

firstThree = functional.take(3, numbers);
console.log("Take 3: " + str(firstThree));

// ============================================
// Drop - Skip First N Elements
// ============================================

console.log("\n=== Drop (skip first N) ===");

afterFive = functional.drop(5, numbers);
console.log("Drop 5: " + str(afterFive));

afterSeven = functional.drop(7, numbers);
console.log("Drop 7: " + str(afterSeven));

// ============================================
// Chunk - Split into Groups
// ============================================

console.log("\n=== Chunk (split into groups) ===");

longList = functional.range(1, 13);
console.log("List: " + str(longList));

chunksOf3 = functional.chunk(3, longList);
console.log("Chunk by 3: " + str(chunksOf3));

chunksOf4 = functional.chunk(4, longList);
console.log("Chunk by 4: " + str(chunksOf4));

// ============================================
// Flatten - Unnest Lists
// ============================================

console.log("\n=== Flatten (unnest) ===");

nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]];
console.log("Nested: " + str(nested));

flat = functional.flatten(nested);
console.log("Flattened: " + str(flat));

// ============================================
// Reverse - Flip Order
// ============================================

console.log("\n=== Reverse ===");

original = [1, 2, 3, 4, 5];
console.log("Original: " + str(original));

reversed = functional.reverse(original);
console.log("Reversed: " + str(reversed));

// ============================================
// Unique - Remove Duplicates
// ============================================

console.log("\n=== Unique (remove duplicates) ===");

withDupes = [1, 2, 2, 3, 1, 4, 3, 5, 2];
console.log("With duplicates: " + str(withDupes));

uniqueVals = functional.unique(withDupes);
console.log("Unique: " + str(uniqueVals));

// ============================================
// Repeat - Duplicate Values
// ============================================

console.log("\n=== Repeat ===");

zeros = functional.repeat(0, 5);
console.log("Repeat 0 five times: " + str(zeros));

fives = functional.repeat(5, 3);
console.log("Repeat 5 three times: " + str(fives));

// ============================================
// ZipWith - Combine with Function
// ============================================

console.log("\n=== ZipWith (combine with function) ===");

list1 = [1, 2, 3, 4];
list2 = [10, 20, 30, 40];

function add(a, b) {
    return a + b;
}

sums = functional.zipWith(add, list1, list2);
console.log("List 1: " + str(list1));
console.log("List 2: " + str(list2));
console.log("Sums: " + str(sums));

function multiply(a, b) {
    return a * b;
}

products = functional.zipWith(multiply, list1, list2);
console.log("Products: " + str(products));

// ============================================
// GroupBy - Group Elements by Key
// ============================================

console.log("\n=== GroupBy (group by key) ===");

items = [
    {type: "fruit", name: "apple"},
    {type: "vegetable", name: "carrot"},
    {type: "fruit", name: "banana"},
    {type: "vegetable", name: "broccoli"},
    {type: "fruit", name: "orange"}
];

function getType(item) {
    return item.type;
}

grouped = functional.groupBy(getType, items);
console.log("Grouped by type: " + str(grouped));

// Group numbers by even/odd
numberList = [1, 2, 3, 4, 5, 6, 7, 8];

function evenOdd(n) {
    if (n % 2 == 0) {
        return "even";
    }
    return "odd";
}

evenOddGroups = functional.groupBy(evenOdd, numberList);
console.log("\nNumbers: " + str(numberList));
console.log("Grouped by even/odd: " + str(evenOddGroups));

// ============================================
// Practical Example: Pagination
// ============================================

console.log("\n=== Practical: Pagination ===");

allItems = functional.range(1, 51);
pageSize = 10;

console.log("Total items: " + str(len(allItems)));
console.log("Page size: " + str(pageSize));

// Get page 2 (0-indexed)
pageNumber = 2;
offset = pageNumber * pageSize;

page = functional.take(pageSize, functional.drop(offset, allItems));
console.log("\nPage " + str(pageNumber + 1) + ": " + str(page));

// ============================================
// Practical Example: Data Batching
// ============================================

console.log("\n=== Practical: Batch Processing ===");

largeDataset = functional.range(1, 21);
batchSize = 5;

console.log("Dataset: " + str(largeDataset));
console.log("Batch size: " + str(batchSize));

batches = functional.chunk(batchSize, largeDataset);
console.log("Number of batches: " + str(len(batches)));
console.log("Batches: " + str(batches));

// Process each batch
function sumBatch(batch) {
    total = 0;
    i = 0;
    while (i < len(batch)) {
        total = total + batch[i];
        i = i + 1;
    }
    return total;
}

batchSums = functional.map(sumBatch, batches);
console.log("Batch sums: " + str(batchSums));

// ============================================
// Practical Example: Sliding Window
// ============================================

console.log("\n=== Practical: Sliding Window ===");

timeSeries = [10, 15, 12, 18, 20, 22, 19, 25];
windowSize = 3;

console.log("Time series: " + str(timeSeries));
console.log("Window size: " + str(windowSize));

// Create sliding windows
windows = [];
i = 0;
while (i <= len(timeSeries) - windowSize) {
    window = functional.take(windowSize, functional.drop(i, timeSeries));
    windows = windows + [window];
    i = i + 1;
}

console.log("Windows: " + str(windows));

// Calculate moving average
function average(nums) {
    total = 0;
    j = 0;
    while (j < len(nums)) {
        total = total + nums[j];
        j = j + 1;
    }
    return total / len(nums);
}

movingAvg = functional.map(average, windows);
console.log("Moving averages: " + str(movingAvg));

console.log("\n=== List Operations Complete ===");
