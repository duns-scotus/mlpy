// ============================================
// Example: Collection Functions
// Category: language-reference/builtin
// Demonstrates: len(), range(), enumerate(), keys(), values()
// ============================================

import console;

console.log("=== Collection Functions ===\n");

// Example 1: len() - Get length
console.log("Example 1: len() - Get collection length");
console.log("len(\"hello\") = " + str(len("hello")));          // 5
console.log("len([1, 2, 3]) = " + str(len([1, 2, 3])));        // 3
console.log("len({a: 1, b: 2}) = " + str(len({a: 1, b: 2})));  // 2
console.log("len(\"\") = " + str(len("")));                    // 0
console.log("len([]) = " + str(len([])));                      // 0

// Example 2: range() - Generate number sequences
console.log("\nExample 2: range() - Generate sequences");
console.log("range(5) = " + str(range(5)));
console.log("range(2, 5) = " + str(range(2, 5)));
console.log("range(0, 10, 2) = " + str(range(0, 10, 2)));
console.log("range(5, 0, -1) = " + str(range(5, 0, -1)));

// Example 3: range() in loops
console.log("\nExample 3: Using range() in loops");
console.log("Counting to 5:");
for (i in range(1, 6)) {
    console.log("  Count: " + str(i));
}

console.log("Even numbers from 0 to 10:");
evenResult = "";
for (num in range(0, 11, 2)) {
    evenResult = evenResult + str(num) + " ";
}
console.log("  " + evenResult);

// Example 4: enumerate() - Get index-value pairs
console.log("\nExample 4: enumerate() - Get indices with values");
letters = ["a", "b", "c", "d"];
console.log("enumerate([\"a\", \"b\", \"c\", \"d\"]):");
for (pair in enumerate(letters)) {
    console.log("  Index " + str(pair[0]) + ": \"" + pair[1] + "\"");
}

console.log("\nenumerate with start=1:");
for (pair in enumerate(letters, 1)) {
    console.log("  #" + str(pair[0]) + ": \"" + pair[1] + "\"");
}

// Example 5: keys() and values() with objects
console.log("\nExample 5: keys() and values() with objects");
person = {
    name: "Alice",
    age: 30,
    city: "New York"
};

console.log("Object: " + str(person));
console.log("keys(person) = " + str(keys(person)));
console.log("values(person) = " + str(values(person)));

// Example 6: Iterating over object keys and values
console.log("\nExample 6: Iterating over objects");
console.log("Keys:");
for (key in keys(person)) {
    console.log("  " + key);
}

console.log("Values:");
for (value in values(person)) {
    console.log("  " + str(value));
}

console.log("Key-value pairs:");
for (key in keys(person)) {
    value = person[key];
    console.log("  " + key + " = " + str(value));
}

// Example 7: Array length for validation
console.log("\nExample 7: Using len() for validation");
function requireMinimumLength(arr, minimum) {
    if (len(arr) < minimum) {
        throw {message: "Array too short"};
    }
    return arr;
}

try {
    data = [1, 2, 3, 4, 5];
    validated = requireMinimumLength(data, 3);
    console.log("Valid array with " + str(len(validated)) + " items");
} except (err) {
    console.log("Error: Array too short");
}

try {
    shortData = [1, 2];
    validated = requireMinimumLength(shortData, 3);
    console.log("Valid array");
} except (err) {
    console.log("Error caught: Array has " + str(len(shortData)) + " items, needs 3");
}

// Example 8: Matrix operations with range
console.log("\nExample 8: Creating a multiplication table");
size = 5;
console.log(str(size) + "x" + str(size) + " multiplication table:");

for (i in range(1, size + 1)) {
    row = "";
    for (j in range(1, size + 1)) {
        product = i * j;
        row = row + str(product) + " ";
    }
    console.log(row);
}

// Example 9: Collecting statistics
console.log("\nExample 9: Data collection statistics");
collections = [
    [1, 2, 3],
    "hello world",
    {a: 1, b: 2, c: 3, d: 4},
    [],
    ""
];

console.log("Collection sizes:");
totalElements = 0;
for (coll in collections) {
    size = len(coll);
    console.log("  " + str(coll) + " -> length: " + str(size));
    totalElements = totalElements + size;
}
console.log("Total elements across all collections: " + str(totalElements));

// Example 10: Combining enumerate with range
console.log("\nExample 10: Indexed number generation");
squares = [];
for (i in range(1, 6)) {
    squares = squares + [i * i];
}

console.log("Square numbers:");
for (pair in enumerate(squares, 1)) {
    index = pair[0];
    value = pair[1];
    console.log("  Square #" + str(index) + ": " + str(value));
}

// Example 11: Object property counting
console.log("\nExample 11: Analyzing objects");
objects = [
    {name: "Alice", age: 30},
    {x: 1, y: 2, z: 3},
    {},
    {a: 1, b: 2, c: 3, d: 4, e: 5}
];

console.log("Object property counts:");
for (obj in objects) {
    propertyCount = len(keys(obj));
    console.log("  " + str(obj) + " has " + str(propertyCount) + " properties");
}

console.log("\n=== Collection Functions Complete ===");
