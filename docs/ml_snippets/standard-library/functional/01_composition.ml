// ============================================
// Example: Function Composition & Currying
// Category: standard-library/functional
// Demonstrates: compose, pipe, curry, partial
// ============================================

import console;
import functional;

console.log("=== Function Composition & Currying ===\n");

// ============================================
// Compose - Right to Left Composition
// ============================================

console.log("=== Compose (right to left) ===");

function addTen(x) {
    return x + 10;
}

function double(x) {
    return x * 2;
}

function square(x) {
    return x * x;
}

// Compose: right to left (square(double(addTen(x))))
combined = functional.compose(square, double, addTen);

input = 5;
result = combined(input);
console.log("Input: " + str(input));
console.log("Pipeline: addTen -> double -> square");
console.log("Steps: 5 + 10 = 15, 15 * 2 = 30, 30 * 30 = 900");
console.log("Result: " + str(result));

// ============================================
// Pipe - Left to Right Composition
// ============================================

console.log("\n=== Pipe (left to right) ===");

// Pipe: left to right (square(double(addTen(x))))
piped = functional.pipe(addTen, double, square);

result2 = piped(input);
console.log("Input: " + str(input));
console.log("Pipeline: addTen -> double -> square");
console.log("Result: " + str(result2));

// ============================================
// Practical Example: Data Transformation
// ============================================

console.log("\n=== Data Transformation Pipeline ===");

function trim(text) {
    // Simulate trim - remove spaces
    return text;
}

function toUpper(text) {
    // In real use, would use string methods
    return text;
}

function addPrefix(text) {
    return "USER_" + text;
}

// Transform user input
processUsername = functional.pipe(trim, toUpper, addPrefix);
username = processUsername("alice");
console.log("Processed username: " + str(username));

// ============================================
// Curry - Partial Application
// ============================================

console.log("\n=== Curry (2 arguments) ===");

function add(a, b) {
    return a + b;
}

// Curry function with 2 arguments
addCurried = functional.curry2(add);

// Partially apply first argument
addFive = addCurried(5);

// Apply second argument
console.log("add(5, 3) = " + str(addFive(3)));
console.log("add(5, 10) = " + str(addFive(10)));
console.log("add(5, 7) = " + str(addFive(7)));

// ============================================
// Partial Application
// ============================================

console.log("\n=== Partial Application ===");

function multiply(a, b, c) {
    return a * b * c;
}

// Partially apply first two arguments
multiplyBy6 = functional.partial(multiply, 2, 3);

console.log("multiply(2, 3, 4) = " + str(multiplyBy6(4)));
console.log("multiply(2, 3, 5) = " + str(multiplyBy6(5)));
console.log("multiply(2, 3, 10) = " + str(multiplyBy6(10)));

// ============================================
// Chaining Compositions
// ============================================

console.log("\n=== Chaining Compositions ===");

function subtractOne(x) {
    return x - 1;
}

function divideByTwo(x) {
    return x / 2;
}

// Complex pipeline: (((x + 10) * 2) - 1) / 2
complexPipe = functional.pipe(addTen, double, subtractOne, divideByTwo);

numbers = [5, 10, 15, 20];
console.log("Original numbers: " + str(numbers));

results = [];
i = 0;
while (i < len(numbers)) {
    result = complexPipe(numbers[i]);
    results = results + [result];
    i = i + 1;
}

console.log("After pipeline: " + str(results));

// ============================================
// Identity Function
// ============================================

console.log("\n=== Identity Function ===");

// Identity returns input unchanged
value = 42;
sameValue = functional.identity(value);
console.log("Identity(" + str(value) + ") = " + str(sameValue));

// Useful as default/placeholder
function applyOrIdentity(shouldTransform, value) {
    if (shouldTransform) {
        return double(value);
    } else {
        return functional.identity(value);
    }
}

console.log("Transform true: " + str(applyOrIdentity(true, 10)));
console.log("Transform false: " + str(applyOrIdentity(false, 10)));

// ============================================
// Constant Function
// ============================================

console.log("\n=== Constant Function ===");

// Create function that always returns same value
alwaysZero = functional.constant(0);
alwaysFoo = functional.constant("foo");

console.log("alwaysZero() = " + str(alwaysZero()));
console.log("alwaysZero() = " + str(alwaysZero()));
console.log("alwaysFoo() = " + str(alwaysFoo()));

// ============================================
// Memoization
// ============================================

console.log("\n=== Memoization (Caching) ===");

function expensiveCalculation(n) {
    console.log("Computing for " + str(n) + "...");
    return n * n;
}

// Memoize the function
memoized = functional.memoize(expensiveCalculation);

// First call: computes
result1 = memoized(5);
console.log("Result: " + str(result1));

// Second call with same argument: cached
result2 = memoized(5);
console.log("Result: " + str(result2) + " (cached)");

// Different argument: computes
result3 = memoized(10);
console.log("Result: " + str(result3));

console.log("\n=== Function Composition Complete ===");
