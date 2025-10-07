// ============================================
// Example: Comments and Control Flow
// Category: tutorial
// Demonstrates: Comments, if/elif/else statements
// ============================================

import console;

// This is a single-line comment
// Comments help explain your code

// Variables for our examples
temperature = 28;
humidity = 65;

// Simple if statement
console.log("=== Simple If Statement ===");
if (temperature > 30) {
    console.log("It's hot outside!");
}

// If-else statement
console.log("");
console.log("=== If-Else Statement ===");
if (temperature > 25) {
    console.log("Weather is warm (" + str(temperature) + "°C)");
} else {
    console.log("Weather is cool (" + str(temperature) + "°C)");
}

// If-elif-else chain
console.log("");
console.log("=== If-Elif-Else Chain ===");
if (temperature < 10) {
    comfort = "cold";
} elif (temperature < 20) {
    comfort = "cool";
} elif (temperature < 30) {
    comfort = "comfortable";
} else {
    comfort = "hot";
}
console.log("Temperature: " + str(temperature) + "°C - Comfort level: " + comfort);

// Nested conditions
console.log("");
console.log("=== Nested Conditions ===");
if (temperature > 20) {
    if (humidity > 70) {
        console.log("Warm and humid - might rain");
    } else {
        console.log("Warm and dry - nice day");
    }
} else {
    console.log("Cool weather");
}

// Practical example: grade calculator
console.log("");
console.log("=== Grade Calculator ===");
score = 87;

if (score >= 90) {
    grade = "A";
    message = "Excellent work!";
} elif (score >= 80) {
    grade = "B";
    message = "Good job!";
} elif (score >= 70) {
    grade = "C";
    message = "Satisfactory.";
} elif (score >= 60) {
    grade = "D";
    message = "Needs improvement.";
} else {
    grade = "F";
    message = "Please see instructor.";
}

console.log("Score: " + str(score));
console.log("Grade: " + grade);
console.log("Feedback: " + message);
