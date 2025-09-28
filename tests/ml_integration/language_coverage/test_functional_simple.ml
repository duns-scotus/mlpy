// Simple test of functional module
import functional;
import string;

// Test basic functional operations
numbers = [1, 2, 3, 4, 5];

// Test map
doubled = functional.map(function(x) { return x * 2; }, numbers);
print("Doubled: " + string.toString(doubled.length));

// Test filter
evens = functional.filter(function(x) { return x % 2 == 0; }, numbers);
print("Evens: " + string.toString(evens.length));

// Test reduce
sum = functional.reduce(function(a, b) { return a + b; }, numbers, 0);
print("Sum: " + string.toString(sum));

print("Basic functional operations work!");