// ============================================
// Example: Working with Data Types
// Category: tutorial
// Demonstrates: Different data types and operations
// ============================================

import console;

// Numbers
age = 25;
price = 19.99;
console.log("Age: " + str(age) + " (type: " + typeof(age) + ")");
console.log("Price: " + str(price) + " (type: " + typeof(price) + ")");

// Strings
firstName = "John";
lastName = "Doe";
fullName = firstName + " " + lastName;
console.log("Full name: " + fullName);

// Booleans
isStudent = true;
hasLicense = false;
console.log("Is student: " + str(isStudent));
console.log("Has license: " + str(hasLicense));

// Arrays
scores = [85, 92, 78, 95, 88];
console.log("First score: " + str(scores[0]));
console.log("Last score: " + str(scores[4]));

// Objects
book = {
    title: "ML Programming",
    author: "Jane Smith",
    year: 2024,
    pages: 350
};
console.log("Book: " + book.title + " by " + book.author);
console.log("Published: " + str(book.year) + " (" + str(book.pages) + " pages)");
