// ============================================
// Example: List Manipulation
// Category: standard-library/collections
// Demonstrates: slice, reverse, unique, flatten, sort, chunk, take, drop
// ============================================

import console;
import collections;

console.log("=== List Manipulation ===\n");

// Slice - extract portion
console.log("=== Slice (extract portion) ===");
numbers = [10, 20, 30, 40, 50, 60, 70];
console.log("Original: " + str(numbers));

firstThree = collections.slice(numbers, 0, 3);
console.log("First 3 (0:3): " + str(firstThree));

middle = collections.slice(numbers, 2, 5);
console.log("Middle (2:5): " + str(middle));

fromThree = collections.slice(numbers, 3, null);
console.log("From index 3: " + str(fromThree));

// Reverse - flip order
console.log("\n=== Reverse ===");
reversed = collections.reverse(numbers);
console.log("Reversed: " + str(reversed));
console.log("Original unchanged: " + str(numbers));

// Unique - remove duplicates
console.log("\n=== Unique (remove duplicates) ===");
withDupes = [1, 2, 2, 3, 1, 4, 3, 5];
console.log("With duplicates: " + str(withDupes));

uniqueVals = collections.unique(withDupes);
console.log("Unique values: " + str(uniqueVals));

// Flatten - nested lists to single list
console.log("\n=== Flatten (unnest) ===");
nested = [[1, 2], [3, 4], [5, 6]];
console.log("Nested: " + str(nested));

flat = collections.flatten(nested);
console.log("Flattened: " + str(flat));

deepNested = [[1, 2], [3, [4, 5]], [6]];
console.log("\nDeeply nested: " + str(deepNested));
flatOnce = collections.flatten(deepNested);
console.log("Flatten once: " + str(flatOnce));

// Sort - order elements
console.log("\n=== Sort ===");
unsorted = [3, 1, 4, 1, 5, 9, 2, 6];
console.log("Unsorted: " + str(unsorted));

sorted = collections.sort(unsorted);
console.log("Sorted: " + str(sorted));

// Sort by custom function
console.log("\n=== Sort By Custom Function ===");
words = ["elephant", "cat", "dog", "butterfly"];
console.log("Words: " + str(words));

function byLength(word) {
    return len(word);
}
byLen = collections.sortBy(words, byLength);
console.log("Sorted by length: " + str(byLen));

// Take - get first N elements
console.log("\n=== Take (first N) ===");
many = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
console.log("List: " + str(many));

firstFive = collections.take(many, 5);
console.log("Take 5: " + str(firstFive));

// Drop - skip first N elements
console.log("\n=== Drop (skip first N) ===");
afterDrop = collections.drop(many, 5);
console.log("Drop 5: " + str(afterDrop));

// Chunk - split into groups
console.log("\n=== Chunk (split into groups) ===");
longList = [1, 2, 3, 4, 5, 6, 7, 8, 9];
console.log("List: " + str(longList));

chunks = collections.chunk(longList, 3);
console.log("Chunk by 3: " + str(chunks));

chunksOfTwo = collections.chunk(longList, 2);
console.log("Chunk by 2: " + str(chunksOfTwo));

// Zip - combine lists into pairs
console.log("\n=== Zip (combine lists) ===");
names = ["Alice", "Bob", "Charlie"];
ages = [25, 30, 35];
console.log("Names: " + str(names));
console.log("Ages: " + str(ages));

pairs = collections.zip(names, ages);
console.log("Zipped: " + str(pairs));

// Practical example: Data cleaning
console.log("\n=== Practical: Data Cleaning ===");
rawData = [5, 3, 8, 3, 5, 1, 9, 3, 7, 5];
console.log("Raw data: " + str(rawData));

// Remove duplicates
cleaned = collections.unique(rawData);
console.log("Remove duplicates: " + str(cleaned));

// Sort for analysis
sorted = collections.sort(cleaned);
console.log("Sorted: " + str(sorted));

// Get top 3
top3 = collections.slice(sorted, -3, null);
console.log("Top 3 values: " + str(top3));

// Practical example: Pagination
console.log("\n=== Practical: Pagination ===");
allItems = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];
pageSize = 5;
pageNum = 2;  // 0-indexed

skip = pageNum * pageSize;
page = collections.take(collections.drop(allItems, skip), pageSize);
console.log("Page " + str(pageNum + 1) + " (items " + str(skip + 1) + "-" + str(skip + collections.length(page)) + "): " + str(page));

console.log("\n=== List Manipulation Complete ===");
