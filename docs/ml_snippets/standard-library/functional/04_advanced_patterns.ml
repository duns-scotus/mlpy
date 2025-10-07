// ============================================
// Example: Advanced Functional Patterns
// Category: standard-library/functional
// Demonstrates: partition, ifElse, cond, takeWhile, times, juxt
// ============================================

import console;
import functional;

console.log("=== Advanced Functional Patterns ===\n");

// ============================================
// Partition - Split by Condition
// ============================================

console.log("=== Partition (split by condition) ===");

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
console.log("Numbers: " + str(numbers));

function isEven(x) {
    return x % 2 == 0;
}

parts = functional.partition(isEven, numbers);
console.log("Partitioned: " + str(parts));
console.log("Evens: " + str(parts[0]));
console.log("Odds: " + str(parts[1]));

// Partition by score
scores = [78, 92, 85, 67, 95, 73, 88, 91, 54, 82];

function isPassing(score) {
    return score >= 70;
}

scoreGroups = functional.partition(isPassing, scores);
console.log("\nScores: " + str(scores));
console.log("Passing: " + str(scoreGroups[0]));
console.log("Failing: " + str(scoreGroups[1]));

// ============================================
// IfElse - Conditional Function Application
// ============================================

console.log("\n=== IfElse (conditional branching) ===");

function isPositive(x) {
    return x > 0;
}

function double(x) {
    return x * 2;
}

function negate(x) {
    return -x;
}

// Double if positive, negate if negative
processNumber = functional.ifElse(isPositive, double, negate);

console.log("Process 5: " + str(processNumber(5)));
console.log("Process -3: " + str(processNumber(-3)));
console.log("Process 10: " + str(processNumber(10)));

// ============================================
// Cond - Multi-Condition Dispatch
// ============================================

console.log("\n=== Cond (multi-condition) ===");

function isSmall(x) {
    return x < 10;
}

function isMedium(x) {
    return x >= 10 && x < 100;
}

function isLarge(x) {
    return x >= 100;
}

function small(x) {
    return "small: " + str(x);
}

function medium(x) {
    return "medium: " + str(x);
}

function large(x) {
    return "large: " + str(x);
}

// Create condition list: [[predicate, action], ...]
conditions = [
    [isSmall, small],
    [isMedium, medium],
    [isLarge, large]
];

categorize = functional.cond(conditions);

console.log("Categorize 5: " + str(categorize(5)));
console.log("Categorize 50: " + str(categorize(50)));
console.log("Categorize 500: " + str(categorize(500)));

// ============================================
// TakeWhile - Take Until Condition Fails
// ============================================

console.log("\n=== TakeWhile (take until false) ===");

numberList = [2, 4, 6, 8, 9, 10, 12, 14];
console.log("Numbers: " + str(numberList));

taken = functional.takeWhile(isEven, numberList);
console.log("Take while even: " + str(taken));

// Take while less than 50
values = [10, 20, 30, 40, 50, 60, 70];

function lessThanFifty(x) {
    return x < 50;
}

beforeFifty = functional.takeWhile(lessThanFifty, values);
console.log("\nValues: " + str(values));
console.log("Take while < 50: " + str(beforeFifty));

// ============================================
// Times - Execute N Times
// ============================================

console.log("\n=== Times (execute N times) ===");

function makeGreeting(i) {
    return "Hello #" + str(i);
}

greetings = functional.times(5, makeGreeting);
console.log("Greetings: " + str(greetings));

function square(i) {
    return i * i;
}

squares = functional.times(10, square);
console.log("Squares: " + str(squares));

// ============================================
// Juxt - Apply Multiple Functions
// ============================================

console.log("\n=== Juxt (apply multiple functions) ===");

function addTen(x) {
    return x + 10;
}

function triple(x) {
    return x * 3;
}

// Apply all functions to same input
applyAll = functional.juxt([addTen, double, triple, square]);

result = applyAll(5);
console.log("Apply all to 5: " + str(result));
console.log("  addTen(5) = " + str(result[0]));
console.log("  double(5) = " + str(result[1]));
console.log("  triple(5) = " + str(result[2]));
console.log("  square(5) = " + str(result[3]));

// ============================================
// Practical Example: Grade Categorization
// ============================================

console.log("\n=== Practical: Grade System ===");

function isA(score) {
    return score >= 90;
}

function isB(score) {
    return score >= 80 && score < 90;
}

function isC(score) {
    return score >= 70 && score < 80;
}

function isD(score) {
    return score >= 60 && score < 70;
}

function gradeA(score) {
    return "A";
}

function gradeB(score) {
    return "B";
}

function gradeC(score) {
    return "C";
}

function gradeD(score) {
    return "D";
}

function gradeF(score) {
    return "F";
}

gradeConditions = [
    [isA, gradeA],
    [isB, gradeB],
    [isC, gradeC],
    [isD, gradeD]
];

assignGrade = functional.cond(gradeConditions);

testScores = [95, 87, 72, 65, 55, 92, 81];
console.log("Scores: " + str(testScores));

grades = functional.map(assignGrade, testScores);
console.log("Grades: " + str(grades));

// ============================================
// Practical Example: Data Validation
// ============================================

console.log("\n=== Practical: Data Validation ===");

userData = [
    {age: 25, score: 85},
    {age: 17, score: 92},
    {age: 30, score: 78},
    {age: 16, score: 65},
    {age: 22, score: 88}
];

function isAdult(user) {
    return user.age >= 18;
}

partitioned = functional.partition(isAdult, userData);
adults = partitioned[0];
minors = partitioned[1];

console.log("Adults: " + str(len(adults)) + " users");
console.log("Minors: " + str(len(minors)) + " users");

// ============================================
// Practical Example: Signal Processing
// ============================================

console.log("\n=== Practical: Signal Processing ===");

signal = [0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0, -1, -2];
console.log("Signal: " + str(signal));

function isNonNegative(x) {
    return x >= 0;
}

// Take positive portion
positivePortion = functional.takeWhile(isNonNegative, signal);
console.log("Positive portion: " + str(positivePortion));

// ============================================
// Practical Example: Statistics
// ============================================

console.log("\n=== Practical: Statistical Analysis ===");

dataset = [12, 15, 18, 22, 25, 28, 30, 35, 40, 45];

function min(nums) {
    smallest = nums[0];
    i = 1;
    while (i < len(nums)) {
        if (nums[i] < smallest) {
            smallest = nums[i];
        }
        i = i + 1;
    }
    return smallest;
}

function max(nums) {
    largest = nums[0];
    i = 1;
    while (i < len(nums)) {
        if (nums[i] > largest) {
            largest = nums[i];
        }
        i = i + 1;
    }
    return largest;
}

function sum(nums) {
    total = 0;
    i = 0;
    while (i < len(nums)) {
        total = total + nums[i];
        i = i + 1;
    }
    return total;
}

function mean(nums) {
    return sum(nums) / len(nums);
}

// Apply all statistics at once
stats = functional.juxt([min, max, sum, mean]);
results = stats(dataset);

console.log("Dataset: " + str(dataset));
console.log("Min: " + str(results[0]));
console.log("Max: " + str(results[1]));
console.log("Sum: " + str(results[2]));
console.log("Mean: " + str(round(results[3], 1)));

console.log("\n=== Advanced Patterns Complete ===");
