// ============================================
// Example: Basic List Operations
// Category: standard-library/collections
// Demonstrates: append, prepend, concat, first, last, length, get
// ============================================

import console;
import collections;

console.log("=== Basic List Operations ===\n");

// Starting list
numbers = [10, 20, 30];
console.log("Original list: " + str(numbers));
console.log("Length: " + str(collections.length(numbers)));

// Append element to end
console.log("\n=== Append (add to end) ===");
withFour = collections.append(numbers, 40);
console.log("After append(40): " + str(withFour));
console.log("Original unchanged: " + str(numbers));  // Pure functional!

// Prepend element to beginning
console.log("\n=== Prepend (add to start) ===");
withZero = collections.prepend(numbers, 0);
console.log("After prepend(0): " + str(withZero));

// Concatenate lists
console.log("\n=== Concatenate Lists ===");
moreNumbers = [40, 50, 60];
combined = collections.concat(numbers, moreNumbers);
console.log("List 1: " + str(numbers));
console.log("List 2: " + str(moreNumbers));
console.log("Combined: " + str(combined));

// Access elements
console.log("\n=== Accessing Elements ===");
first = collections.first(numbers);
last = collections.last(numbers);
console.log("First: " + str(first));
console.log("Last: " + str(last));

// Get by index (safe - returns null if out of bounds)
second = collections.get(numbers, 1);
outOfBounds = collections.get(numbers, 10);
console.log("Index 1: " + str(second));
console.log("Index 10: " + str(outOfBounds));  // null

// Check if empty
console.log("\n=== Empty Check ===");
empty = [];
console.log("Is [] empty? " + str(collections.isEmpty(empty)));
console.log("Is [1,2,3] empty? " + str(collections.isEmpty(numbers)));

// Practical example: Building a list
console.log("\n=== Building a List ===");
list = [];
list = collections.append(list, "first");
list = collections.append(list, "second");
list = collections.append(list, "third");
console.log("Built list: " + str(list));
console.log("Length: " + str(collections.length(list)));

console.log("\n=== Basic Operations Complete ===");
