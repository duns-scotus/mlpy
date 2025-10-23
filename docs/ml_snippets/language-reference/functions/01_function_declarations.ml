// ============================================
// Example: Function Declarations
// Category: language-reference/functions
// Demonstrates: Named function syntax, parameters, return values
// ============================================

import console;

// Basic function with no parameters
function greet() {
    console.log("Hello, World!");
}

greet();

// Function with parameters
function add(a, b) {
    return a + b;
}

result = add(10, 20);
console.log("10 + 20 = " + str(result));

// Function with multiple statements
function calculateArea(width, height) {
    area = width * height;
    console.log("Calculating area: " + str(width) + " x " + str(height));
    return area;
}

roomArea = calculateArea(12, 15);
console.log("Room area: " + str(roomArea));

// Function with conditional logic
function getGrade(score) {
    if (score >= 90) {
        return "A";
    } elif (score >= 80) {
        return "B";
    } elif (score >= 70) {
        return "C";
    } elif (score >= 60) {
        return "D";
    } else {
        return "F";
    }
}

console.log("Grade for 85: " + getGrade(85));
console.log("Grade for 72: " + getGrade(72));
console.log("Grade for 95: " + getGrade(95));

// Function with early return
function findFirstNegative(numbers) {
    for (num in numbers) {
        if (num < 0) {
            return num;
        }
    }
    return null;
}

values = [5, 3, -2, 8, -1, 4];
firstNeg = findFirstNegative(values);
console.log("First negative: " + str(firstNeg));

// Function with loop and accumulation
function sumArray(arr) {
    total = 0;
    for (value in arr) {
        total = total + value;
    }
    return total;
}

numbers = [10, 20, 30, 40, 50];
sum = sumArray(numbers);
console.log("Sum: " + str(sum));

// Function calling other functions
function calculateAverage(arr) {
    if (len(arr) == 0) {
        return 0;
    }
    total = sumArray(arr);
    return total / len(arr);
}

avg = calculateAverage(numbers);
console.log("Average: " + str(avg));
