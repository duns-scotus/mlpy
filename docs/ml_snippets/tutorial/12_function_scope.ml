// ============================================
// Example: Function Scope
// Category: tutorial
// Demonstrates: Variable scope in functions
// ============================================

import console;

// Global variable
globalValue = 100;

// Function using global variable
function showGlobal() {
    console.log("Global value: " + str(globalValue));
}

// Function with local variable
function useLocal() {
    localValue = 50;
    console.log("Local value: " + str(localValue));
}

// Function that modifies and returns
function addToGlobal(x) {
    return globalValue + x;
}

// Nested function calls
function outer(a) {
    return inner(a * 2);
}

function inner(b) {
    return b + 10;
}

// Function that takes function result as parameter
function processValue(value) {
    doubled = value * 2;
    return doubled + 5;
}

function getValue() {
    return 20;
}

// Demonstrate scope
console.log("=== Global Variables ===");
console.log("globalValue = " + str(globalValue));
showGlobal();

console.log("");
console.log("=== Local Variables ===");
useLocal();

console.log("");
console.log("=== Using Global in Calculation ===");
result = addToGlobal(25);
console.log("addToGlobal(25) = " + str(result));

console.log("");
console.log("=== Nested Function Calls ===");
nestedResult = outer(5);
console.log("outer(5) = " + str(nestedResult));

console.log("");
console.log("=== Passing Function Results ===");
value = getValue();
console.log("getValue() = " + str(value));
processed = processValue(value);
console.log("processValue(getValue()) = " + str(processed));

// Using function results in expressions
console.log("");
console.log("=== Functions in Expressions ===");
x = getValue() + 10;
console.log("getValue() + 10 = " + str(x));

y = processValue(getValue()) * 2;
console.log("processValue(getValue()) * 2 = " + str(y));
