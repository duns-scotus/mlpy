// ============================================
// Example: Break and Continue Statements
// Category: language-reference/control-flow
// Demonstrates: break, continue, search patterns, filtering
// ============================================

import console;

// Break from while loop
console.log("Break example (count to 5 with infinite loop):");
count = 0;
while (true) {
    console.log("  " + str(count));
    count = count + 1;
    if (count >= 5) {
        break;
    }
}

// Break from for loop (search pattern)
console.log("\nSearch for number > 7:");
numbers = [1, 5, 8, 3, 9, 2];
for (num in numbers) {
    console.log("  Checking: " + str(num));
    if (num > 7) {
        console.log("  Found: " + str(num));
        break;
    }
}

// Continue in while loop (skip even numbers)
console.log("\nOdd numbers from 1 to 10:");
counter = 0;
while (counter < 10) {
    counter = counter + 1;
    if (counter % 2 == 0) {
        continue;
    }
    console.log("  " + str(counter));
}

// Continue in for loop (filter pattern)
console.log("\nSkip multiples of 3:");
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
for (val in values) {
    if (val % 3 == 0) {
        continue;
    }
    console.log("  " + str(val));
}

// Practical example: sum only positive numbers
console.log("\nSum of positive numbers:");
allValues = [-5, 3, -2, 8, -1, 6, -3, 4];
positiveSum = 0;
for (value in allValues) {
    if (value < 0) {
        continue;
    }
    positiveSum = positiveSum + value;
}
console.log("Sum: " + str(positiveSum));

// Search with found flag
console.log("\nSearch for target value:");
target = 42;
items = [10, 20, 42, 30, 40];
found = false;

for (item in items) {
    if (item == target) {
        found = true;
        console.log("Found target: " + str(target));
        break;
    }
}

if (!found) {
    console.log("Target not found");
}

// Break only exits innermost loop
console.log("\nNested loop with break:");
for (i in range(3)) {
    console.log("Outer: " + str(i));
    for (j in range(3)) {
        console.log("  Inner: " + str(j));
        if (j == 1) {
            break;
        }
    }
}
