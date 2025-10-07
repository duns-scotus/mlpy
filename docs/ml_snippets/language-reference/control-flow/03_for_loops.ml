// ============================================
// Example: For Loops
// Category: language-reference/control-flow
// Demonstrates: for..in loops, array iteration, range(), enumerate()
// ============================================

import console;

// Iterating over arrays
console.log("Array iteration:");
numbers = [10, 20, 30, 40, 50];
for (num in numbers) {
    console.log("  " + str(num));
}

// String iteration
console.log("\nString iteration:");
text = "Hello";
for (char in text) {
    console.log("  " + char);
}

// Using range() for counting
console.log("\nCounting with range(5):");
for (i in range(5)) {
    console.log("  " + str(i));
}

// Range with start and end
console.log("\nRange from 1 to 10:");
for (i in range(1, 11)) {
    console.log("  " + str(i));
}

// Range with step
console.log("\nEven numbers from 0 to 10:");
for (i in range(0, 11, 2)) {
    console.log("  " + str(i));
}

// Nested for loops
console.log("\nMultiplication table (3x3):");
for (i in range(1, 4)) {
    for (j in range(1, 4)) {
        product = i * j;
        console.log("  " + str(i) + " x " + str(j) + " = " + str(product));
    }
}

// Using enumerate() for index and value
console.log("\nEnumerate example:");
items = ["apple", "banana", "cherry"];
for (pair in enumerate(items)) {
    index = pair[0];
    value = pair[1];
    console.log("  " + str(index) + ": " + value);
}

// Accumulation with for loop
console.log("\nSum of squares:");
squareSum = 0;
for (n in range(1, 6)) {
    squareSum = squareSum + (n * n);
}
console.log("Sum: " + str(squareSum));
