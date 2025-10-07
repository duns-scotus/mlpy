// ============================================
// Example: Arrow Functions (Anonymous Functions)
// Category: language-reference/functions
// Demonstrates: fn() => syntax, assigning to variables, inline usage
// ============================================

import console;

// Basic arrow function assigned to variable
add = fn(a, b) => a + b;
result = add(5, 3);
console.log("5 + 3 = " + str(result));

// Arrow function with single parameter
double = fn(x) => x * 2;
console.log("Double of 7: " + str(double(7)));

// Arrow function with no parameters
getMessage = fn() => "Hello from arrow function";
console.log(getMessage());

// Arrow function with multiple operations (using block)
calculateDiscount = fn(price, percent) => price - (price * percent / 100);
finalPrice = calculateDiscount(100, 20);
console.log("Price after 20% discount: " + str(finalPrice));

// Multiple arrow functions
multiply = fn(a, b) => a * b;
subtract = fn(a, b) => a - b;
divide = fn(a, b) => a / b;

console.log("10 * 3 = " + str(multiply(10, 3)));
console.log("10 - 3 = " + str(subtract(10, 3)));
console.log("10 / 2 = " + str(divide(10, 2)));

// Arrow function for string operations
toUpperCase = fn(text) => text;  // Note: ML doesn't have built-in upper(), this is illustrative
greet = fn(name) => "Hello, " + name + "!";

console.log(greet("Alice"));
console.log(greet("Bob"));

// Arrow function for boolean logic
isEven = fn(n) => n % 2 == 0;
isPositive = fn(n) => n > 0;
isInRange = fn(n, min, max) => n >= min && n <= max;

console.log("Is 4 even? " + str(isEven(4)));
console.log("Is 7 even? " + str(isEven(7)));
console.log("Is -5 positive? " + str(isPositive(-5)));
console.log("Is 15 in range [10, 20]? " + str(isInRange(15, 10, 20)));

// Arrow function with array operations
getFirst = fn(arr) => arr[0];
getLast = fn(arr) => arr[len(arr) - 1];
getLength = fn(arr) => len(arr);

data = [10, 20, 30, 40, 50];
console.log("First element: " + str(getFirst(data)));
console.log("Last element: " + str(getLast(data)));
console.log("Array length: " + str(getLength(data)));

// Arrow function with object access
getName = fn(person) => person.name;
getAge = fn(person) => person.age;

user = {name: "Charlie", age: 30};
console.log("Name: " + getName(user));
console.log("Age: " + str(getAge(user)));

// Comparing named function vs arrow function
// Named function:
function addNamed(x, y) {
    return x + y;
}

// Arrow function equivalent:
addArrow = fn(x, y) => x + y;

console.log("Named: " + str(addNamed(10, 20)));
console.log("Arrow: " + str(addArrow(10, 20)));
