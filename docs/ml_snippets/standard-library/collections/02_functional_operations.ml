// ============================================
// Example: Functional Operations
// Category: standard-library/collections
// Demonstrates: map, filter, reduce, find, every, some
// ============================================

import console;
import collections;

console.log("=== Functional Operations ===\n");

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Map - transform each element
console.log("=== Map (transform) ===");
console.log("Original: " + str(numbers));

// Note: Using standard function syntax, not arrow functions
function double(n) {
    return n * 2;
}
doubled = collections.map(numbers, double);
console.log("Doubled: " + str(doubled));

function square(n) {
    return n * n;
}
squared = collections.map(numbers, square);
console.log("Squared: " + str(squared));

// Filter - select elements
console.log("\n=== Filter (select) ===");
function isEven(n) {
    return n % 2 == 0;
}
evens = collections.filter(numbers, isEven);
console.log("Evens: " + str(evens));

function greaterThanFive(n) {
    return n > 5;
}
large = collections.filter(numbers, greaterThanFive);
console.log("Greater than 5: " + str(large));

// Reduce - aggregate to single value
console.log("\n=== Reduce (aggregate) ===");
function add(acc, n) {
    return acc + n;
}
sum = collections.reduce(numbers, add, 0);
console.log("Sum: " + str(sum));

function multiply(acc, n) {
    return acc * n;
}
product = collections.reduce(numbers, multiply, 1);
console.log("Product: " + str(product));

// Find - get first matching element
console.log("\n=== Find (first match) ===");
function isGreaterThanSeven(n) {
    return n > 7;
}
firstLarge = collections.find(numbers, isGreaterThanSeven);
console.log("First > 7: " + str(firstLarge));  // 8

function isTwenty(n) {
    return n == 20;
}
notFound = collections.find(numbers, isTwenty);
console.log("Find 20: " + str(notFound));  // null

// Every - check if all match
console.log("\n=== Every (all match?) ===");
function isPositive(n) {
    return n > 0;
}
allPositive = collections.every(numbers, isPositive);
console.log("All positive? " + str(allPositive));  // true

function isEvenNum(n) {
    return n % 2 == 0;
}
allEven = collections.every(numbers, isEvenNum);
console.log("All even? " + str(allEven));  // false

// Some - check if any match
console.log("\n=== Some (any match?) ===");
anyEven = collections.some(numbers, isEvenNum);
console.log("Any even? " + str(anyEven));  // true

function isHundred(n) {
    return n == 100;
}
anyHundred = collections.some(numbers, isHundred);
console.log("Any equal 100? " + str(anyHundred));  // false

// Chain operations
console.log("\n=== Chaining Operations ===");
// Filter evens, then double them, then sum
evenNums = collections.filter(numbers, isEven);
doubledEvens = collections.map(evenNums, double);
sumOfDoubledEvens = collections.reduce(doubledEvens, add, 0);

console.log("Original: " + str(numbers));
console.log("Filter evens: " + str(evenNums));
console.log("Double: " + str(doubledEvens));
console.log("Sum: " + str(sumOfDoubledEvens));

// Practical example: Process scores
console.log("\n=== Practical: Process Scores ===");
scores = [78, 92, 85, 67, 95, 73, 88, 91];
console.log("Scores: " + str(scores));

function isPassing(score) {
    return score >= 70;
}
passingScores = collections.filter(scores, isPassing);
console.log("Passing (>=70): " + str(passingScores));

function sumScores(acc, score) {
    return acc + score;
}
totalPassing = collections.reduce(passingScores, sumScores, 0);
averagePassing = totalPassing / collections.length(passingScores);
console.log("Average passing score: " + str(round(averagePassing, 1)));

// Check if any failed
function isFailing(score) {
    return score < 70;
}
anyFailed = collections.some(scores, isFailing);
console.log("Any students failed? " + str(anyFailed));

// Check if all passed
allPassed = collections.every(scores, isPassing);
console.log("All students passed? " + str(allPassed));

console.log("\n=== Functional Operations Complete ===");
