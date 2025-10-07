// ============================================
// Example: Conditional Statements (if/elif/else)
// Category: language-reference/control-flow
// Demonstrates: if, elif, else branching
// ============================================

import console;

// Simple if statement
x = 10;
if (x > 5) {
    console.log("x is greater than 5");
}

// if-else statement
age = 20;
if (age >= 18) {
    status = "Adult";
} else {
    status = "Minor";
}
console.log("Status: " + status);

// if-elif-else statement
score = 85;
if (score >= 90) {
    grade = "A";
} elif (score >= 80) {
    grade = "B";
} elif (score >= 70) {
    grade = "C";
} elif (score >= 60) {
    grade = "D";
} else {
    grade = "F";
}
console.log("Grade: " + grade);

// Nested conditionals
x = 5;
y = 10;
if (x > 0) {
    if (y > 0) {
        console.log("Both positive");
    } else {
        console.log("x positive, y non-positive");
    }
} else {
    console.log("x non-positive");
}

// Using elif instead of nesting (preferred)
value = 7;
if (value > 10) {
    result = "large";
} elif (value > 5) {
    result = "medium";
} else {
    result = "small";
}
console.log("Result: " + result);
