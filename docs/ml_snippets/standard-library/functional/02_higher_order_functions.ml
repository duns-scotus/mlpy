// ============================================
// Example: Higher-Order Functions
// Category: standard-library/functional
// Demonstrates: map, filter, reduce, find, every, some, forEach
// ============================================

import console;
import functional;

console.log("=== Higher-Order Functions ===\n");

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
console.log("Working with: " + str(numbers) + "\n");

// ============================================
// Map - Transform Elements
// ============================================

console.log("=== Map (transform) ===");

function double(x) {
    return x * 2;
}

doubled = functional.map(double, numbers);
console.log("Doubled: " + str(doubled));

function square(x) {
    return x * x;
}

squared = functional.map(square, numbers);
console.log("Squared: " + str(squared));

// ============================================
// Filter - Select Elements
// ============================================

console.log("\n=== Filter (select) ===");

function isEven(x) {
    return x % 2 == 0;
}

evens = functional.filter(isEven, numbers);
console.log("Evens: " + str(evens));

function greaterThanFive(x) {
    return x > 5;
}

large = functional.filter(greaterThanFive, numbers);
console.log("Greater than 5: " + str(large));

// ============================================
// Reduce - Aggregate Values
// ============================================

console.log("\n=== Reduce (aggregate) ===");

function add(acc, x) {
    return acc + x;
}

sum = functional.reduce(add, numbers, 0);
console.log("Sum: " + str(sum));

function multiply(acc, x) {
    return acc * x;
}

product = functional.reduce(multiply, numbers, 1);
console.log("Product: " + str(product));

// Build string from numbers
function buildString(acc, x) {
    if (acc == "") {
        return str(x);
    }
    return acc + ", " + str(x);
}

joined = functional.reduce(buildString, numbers, "");
console.log("Joined: " + str(joined));

// ============================================
// Find - Locate Element
// ============================================

console.log("\n=== Find (locate) ===");

function isGreaterThanSeven(x) {
    return x > 7;
}

firstLarge = functional.find(isGreaterThanSeven, numbers);
console.log("First > 7: " + str(firstLarge));

function isTwenty(x) {
    return x == 20;
}

notFound = functional.find(isTwenty, numbers);
console.log("Find 20: " + str(notFound));

// ============================================
// Every - Test All Elements
// ============================================

console.log("\n=== Every (test all) ===");

function isPositive(x) {
    return x > 0;
}

allPositive = functional.every(isPositive, numbers);
console.log("All positive? " + str(allPositive));

allEven = functional.every(isEven, numbers);
console.log("All even? " + str(allEven));

// ============================================
// Some - Test Any Element
// ============================================

console.log("\n=== Some (test any) ===");

anyEven = functional.some(isEven, numbers);
console.log("Any even? " + str(anyEven));

function isHundred(x) {
    return x == 100;
}

anyHundred = functional.some(isHundred, numbers);
console.log("Any equal 100? " + str(anyHundred));

// ============================================
// ForEach - Execute for Each
// ============================================

console.log("\n=== ForEach (execute) ===");

console.log("Printing each number:");
function printNumber(x) {
    console.log("  - " + str(x));
}

functional.forEach(printNumber, [1, 2, 3, 4, 5]);

// ============================================
// Zip - Combine Lists
// ============================================

console.log("\n=== Zip (combine) ===");

names = ["Alice", "Bob", "Charlie"];
ages = [25, 30, 35];

pairs = functional.zip(names, ages);
console.log("Names: " + str(names));
console.log("Ages: " + str(ages));
console.log("Zipped: " + str(pairs));

// ============================================
// Chaining Operations
// ============================================

console.log("\n=== Chaining Operations ===");

// Pipeline: filter evens -> map double -> reduce sum
step1 = functional.filter(isEven, numbers);
console.log("Step 1 - Filter evens: " + str(step1));

step2 = functional.map(double, step1);
console.log("Step 2 - Double: " + str(step2));

step3 = functional.reduce(add, step2, 0);
console.log("Step 3 - Sum: " + str(step3));

// ============================================
// Practical Example: Process Scores
// ============================================

console.log("\n=== Practical: Grade Analysis ===");

scores = [78, 92, 85, 67, 95, 73, 88, 91, 54, 82];
console.log("Scores: " + str(scores));

// Find passing scores
function isPassing(score) {
    return score >= 70;
}

passing = functional.filter(isPassing, scores);
console.log("Passing (>=70): " + str(passing));
console.log("Count: " + str(len(passing)) + "/" + str(len(scores)));

// Calculate average
totalScore = functional.reduce(add, passing, 0);
average = totalScore / len(passing);
console.log("Average passing score: " + str(round(average, 1)));

// Check if any failed
function isFailing(score) {
    return score < 70;
}

anyFailed = functional.some(isFailing, scores);
console.log("Any students failed? " + str(anyFailed));

// Check if all passed
allPassed = functional.every(isPassing, scores);
console.log("All students passed? " + str(allPassed));

// Find first excellent score (>= 90)
function isExcellent(score) {
    return score >= 90;
}

firstExcellent = functional.find(isExcellent, scores);
console.log("First excellent score: " + str(firstExcellent));

// ============================================
// Practical Example: Data Processing
// ============================================

console.log("\n=== Practical: Data Transformation ===");

rawData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
console.log("Raw data: " + str(rawData));

// Complex transformation pipeline
function isOdd(x) {
    return x % 2 == 1;
}

function triple(x) {
    return x * 3;
}

// Filter odd numbers, triple them, sum the results
odds = functional.filter(isOdd, rawData);
console.log("Odd numbers: " + str(odds));

tripled = functional.map(triple, odds);
console.log("Tripled: " + str(tripled));

sumTripled = functional.reduce(add, tripled, 0);
console.log("Sum of tripled odds: " + str(sumTripled));

console.log("\n=== Higher-Order Functions Complete ===");
