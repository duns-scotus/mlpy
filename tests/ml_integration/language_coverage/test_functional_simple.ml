// Simple test of functional module
import functional;
import string;

// Test basic functional operations
numbers = [1, 2, 3, 4, 5];

// Test map - using arrow functions
doubled = functional.map(fn(x) => x * 2, numbers);
print("Doubled: " + string.toString(doubled.length));

// Test filter - using arrow functions
evens = functional.filter(fn(x) => x % 2 == 0, numbers);
print("Evens: " + string.toString(evens.length));

// Test reduce - using arrow functions
sum = functional.reduce(fn(a, b) => a + b, numbers, 0);
print("Sum: " + string.toString(sum));

print("Basic functional operations work!");