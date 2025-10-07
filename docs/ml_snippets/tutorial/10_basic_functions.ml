// ============================================
// Example: Basic Functions
// Category: tutorial
// Demonstrates: Function definition and calling
// ============================================

import console;

// Simple function with no parameters
function greet() {
    console.log("Hello from a function!");
}

// Function with one parameter
function greetPerson(name) {
    console.log("Hello, " + name + "!");
}

// Function with return value
function square(x) {
    return x * x;
}

// Function with multiple parameters
function add(a, b) {
    return a + b;
}

// Function that uses another function
function addSquares(x, y) {
    return square(x) + square(y);
}

// Call functions
console.log("=== Function Calls ===");
greet();
greetPerson("Alice");

console.log("");
console.log("=== Functions with Return Values ===");
result = square(5);
console.log("square(5) = " + str(result));

sum = add(10, 20);
console.log("add(10, 20) = " + str(sum));

combined = addSquares(3, 4);
console.log("addSquares(3, 4) = " + str(combined));

// Functions for calculations
function calculateArea(width, height) {
    return width * height;
}

function calculatePerimeter(width, height) {
    return 2 * (width + height);
}

console.log("");
console.log("=== Rectangle Calculations ===");
w = 5;
h = 3;
console.log("Width: " + str(w) + ", Height: " + str(h));
console.log("Area: " + str(calculateArea(w, h)));
console.log("Perimeter: " + str(calculatePerimeter(w, h)));
