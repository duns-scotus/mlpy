// ============================================
// Example: Function Patterns
// Category: tutorial
// Demonstrates: Common function patterns and uses
// ============================================

import console;

// Function with conditional logic
function max(a, b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

// Function with loop
function sumArray(numbers) {
    total = 0;
    for (num in numbers) {
        total = total + num;
    }
    return total;
}

// Function that builds an array
function doubleValues(numbers) {
    result = [];
    for (num in numbers) {
        result = result + [num * 2];
    }
    return result;
}

// Function that filters
function getEvens(numbers) {
    evens = [];
    for (num in numbers) {
        if (num % 2 == 0) {
            evens = evens + [num];
        }
    }
    return evens;
}

// Function with early return
function findFirst(numbers, target) {
    for (num in numbers) {
        if (num > target) {
            return num;
        }
    }
    return -1;
}

// Function that calls other functions
function calculateStats(numbers) {
    total = sumArray(numbers);
    count = len(numbers);
    average = total / count;
    return average;
}

// Using the functions
console.log("=== Maximum Value ===");
console.log("max(10, 25) = " + str(max(10, 25)));
console.log("max(50, 30) = " + str(max(50, 30)));

console.log("");
console.log("=== Array Sum ===");
values = [10, 20, 30, 40, 50];
console.log("Numbers: " + str(values));
console.log("Sum: " + str(sumArray(values)));

console.log("");
console.log("=== Doubling Values ===");
original = [1, 2, 3, 4, 5];
doubled = doubleValues(original);
console.log("Original: " + str(original));
console.log("Doubled: " + str(doubled));

console.log("");
console.log("=== Filtering Even Numbers ===");
allNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
evenNumbers = getEvens(allNumbers);
console.log("All numbers: " + str(allNumbers));
console.log("Even numbers: " + str(evenNumbers));

console.log("");
console.log("=== Finding First Match ===");
searchList = [3, 7, 12, 9, 15];
found = findFirst(searchList, 10);
console.log("Numbers: " + str(searchList));
console.log("First number > 10: " + str(found));

console.log("");
console.log("=== Calculating Average ===");
scores = [85, 92, 78, 95, 88];
average = calculateStats(scores);
console.log("Scores: " + str(scores));
console.log("Average: " + str(average));
