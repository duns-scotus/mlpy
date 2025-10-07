// ============================================
// Example: For Loops
// Category: tutorial
// Demonstrates: For loop basics and array iteration
// ============================================

import console;

// Basic array iteration
console.log("=== Iterating Over Array ===");
fruits = ["apple", "banana", "cherry", "date"];
for (fruit in fruits) {
    console.log("I like " + fruit);
}

// Summing array values
console.log("");
console.log("=== Summing Values ===");
scores = [85, 92, 78, 95, 88];
total = 0;
for (score in scores) {
    total = total + score;
}
average = total / len(scores);
console.log("Total: " + str(total));
console.log("Average: " + str(average));

// Finding maximum value
console.log("");
console.log("=== Finding Maximum ===");
numbers = [23, 67, 12, 89, 45, 91, 34];
maximum = numbers[0];
for (num in numbers) {
    if (num > maximum) {
        maximum = num;
    }
}
console.log("Maximum value: " + str(maximum));

// Building new array
console.log("");
console.log("=== Doubling Values ===");
original = [1, 2, 3, 4, 5];
doubled = [];
for (value in original) {
    doubled = doubled + [value * 2];
}
console.log("Original: " + str(original));
console.log("Doubled: " + str(doubled));

// Filtering array
console.log("");
console.log("=== Filtering Even Numbers ===");
allNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
evenNumbers = [];
for (n in allNumbers) {
    if (n % 2 == 0) {
        evenNumbers = evenNumbers + [n];
    }
}
console.log("Even numbers: " + str(evenNumbers));

// Processing objects in array
console.log("");
console.log("=== Processing Student Records ===");
students = [
    {name: "Alice", grade: 85},
    {name: "Bob", grade: 92},
    {name: "Carol", grade: 78}
];
for (student in students) {
    console.log(student.name + ": " + str(student.grade));
}
