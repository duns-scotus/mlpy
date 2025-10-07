// ============================================
// Example: Functional Programming with Arrow Functions
// Category: language-reference/functions
// Demonstrates: Using arrow functions with functional.map, functional.filter
//              Higher-order functions and function composition
// ============================================

import console;
import functional;

console.log("=== Functional Programming with Arrow Functions ===\n");

// Using functional.map with arrow functions
console.log("Example 1: Map - Transform each element");
numbers = [1, 2, 3, 4, 5];
console.log("Original: " + str(numbers));

// Double each number
doubled = functional.map(fn(x) => x * 2, numbers);
console.log("Doubled: " + str(doubled));

// Square each number
squared = functional.map(fn(x) => x * x, numbers);
console.log("Squared: " + str(squared));

// Convert to strings
strings = functional.map(fn(x) => "Number: " + str(x), numbers);
console.log("Strings: " + str(strings));

// Using functional.filter with arrow functions
console.log("\nExample 2: Filter - Select elements matching criteria");
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
console.log("Original: " + str(values));

// Filter even numbers
evens = functional.filter(fn(x) => x % 2 == 0, values);
console.log("Evens: " + str(evens));

// Filter numbers greater than 5
greaterThan5 = functional.filter(fn(x) => x > 5, values);
console.log("Greater than 5: " + str(greaterThan5));

// Filter numbers in range
inRange = functional.filter(fn(x) => x >= 3 && x <= 7, values);
console.log("In range [3, 7]: " + str(inRange));

// Combining map and filter
console.log("\nExample 3: Chaining operations");
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
console.log("Original: " + str(data));

// Get even numbers, then square them
step1 = functional.filter(fn(x) => x % 2 == 0, data);
console.log("After filter (evens): " + str(step1));
step2 = functional.map(fn(x) => x * x, step1);
console.log("After map (squared): " + str(step2));

// Working with objects
console.log("\nExample 4: Processing object arrays");
students = [
    {name: "Alice", score: 85},
    {name: "Bob", score: 92},
    {name: "Carol", score: 78},
    {name: "David", score: 95},
    {name: "Eve", score: 88}
];

// Extract names
names = functional.map(fn(student) => student.name, students);
console.log("All names: " + str(names));

// Extract scores
scores = functional.map(fn(student) => student.score, students);
console.log("All scores: " + str(scores));

// Filter high scorers (>= 90)
highScorers = functional.filter(fn(student) => student.score >= 90, students);
console.log("\nHigh scorers (>= 90):");
for (student in highScorers) {
    console.log("  " + student.name + ": " + str(student.score));
}

// Get names of high scorers
highScorerNames = functional.map(
    fn(student) => student.name,
    functional.filter(fn(student) => student.score >= 90, students)
);
console.log("High scorer names: " + str(highScorerNames));

// Complex transformations
console.log("\nExample 5: Complex data transformations");
products = [
    {name: "Laptop", price: 1000, inStock: true},
    {name: "Mouse", price: 25, inStock: true},
    {name: "Keyboard", price: 75, inStock: false},
    {name: "Monitor", price: 300, inStock: true},
    {name: "Headphones", price: 150, inStock: false}
];

// Get available products
available = functional.filter(fn(p) => p.inStock, products);
console.log("Available products:");
for (product in available) {
    console.log("  " + product.name + ": $" + str(product.price));
}

// Calculate total value of available products
availablePrices = functional.map(fn(p) => p.price, available);
totalValue = 0;
for (price in availablePrices) {
    totalValue = totalValue + price;
}
console.log("Total available inventory value: $" + str(totalValue));

// Apply discount to expensive items
console.log("\nExample 6: Conditional transformations");
discountThreshold = 100;
discountPercent = 20;

applyDiscount = fn(product) => product.price >= discountThreshold
    ? product.price * (100 - discountPercent) / 100
    : product.price;

discountedPrices = functional.map(applyDiscount, products);
console.log("Original prices: " + str(functional.map(fn(p) => p.price, products)));
console.log("Discounted prices: " + str(discountedPrices));

// Using arrow functions for predicates
console.log("\nExample 7: Predicate functions");
testData = [-5, -3, 0, 3, 5, 8, -2, 10];

isPositive = fn(x) => x > 0;
isNegative = fn(x) => x < 0;
isZero = fn(x) => x == 0;
isLarge = fn(x) => x > 5;

positives = functional.filter(isPositive, testData);
negatives = functional.filter(isNegative, testData);
zeros = functional.filter(isZero, testData);
largeNumbers = functional.filter(isLarge, testData);

console.log("Original: " + str(testData));
console.log("Positives: " + str(positives));
console.log("Negatives: " + str(negatives));
console.log("Zeros: " + str(zeros));
console.log("Large (> 5): " + str(largeNumbers));

console.log("\n=== Functional Programming Complete ===");
