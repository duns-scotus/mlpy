// ============================================
// Example: Array Functions
// Category: language-reference/builtin
// Demonstrates: sorted(), reversed(), zip(), all(), any()
// ============================================

import console;

console.log("=== Array Functions ===\n");

// Example 1: sorted() - Sort arrays
console.log("Example 1: sorted() - Sort arrays");
numbers = [3, 1, 4, 1, 5, 9, 2, 6];
console.log("Original: " + str(numbers));
console.log("sorted(numbers) = " + str(sorted(numbers)));
console.log("sorted(numbers, true) = " + str(sorted(numbers, true)));  // Descending

words = ["dog", "cat", "elephant", "ant"];
console.log("\nOriginal: " + str(words));
console.log("sorted(words) = " + str(sorted(words)));

// Example 2: reversed() - Reverse sequences
console.log("\nExample 2: reversed() - Reverse sequences");
items = [1, 2, 3, 4, 5];
console.log("Original: " + str(items));
console.log("reversed(items) = " + str(reversed(items)));

text = "hello";
console.log("\nOriginal: \"" + text + "\"");
console.log("reversed(text) = " + str(reversed(text)));

// Example 3: zip() - Combine arrays
console.log("\nExample 3: zip() - Combine arrays");
names = ["Alice", "Bob", "Carol"];
ages = [30, 25, 35];
cities = ["New York", "Paris", "Tokyo"];

console.log("names = " + str(names));
console.log("ages = " + str(ages));
console.log("zip(names, ages) = " + str(zip(names, ages)));
console.log("zip(names, ages, cities) = " + str(zip(names, ages, cities)));

// Example 4: all() - Check all truthy
console.log("\nExample 4: all() - Check all truthy");
console.log("all([true, true, true]) = " + str(all([true, true, true])));
console.log("all([true, false, true]) = " + str(all([true, false, true])));
console.log("all([1, 2, 3]) = " + str(all([1, 2, 3])));
console.log("all([1, 0, 3]) = " + str(all([1, 0, 3])));
console.log("all([]) = " + str(all([])));  // Empty is true

// Example 5: any() - Check any truthy
console.log("\nExample 5: any() - Check any truthy");
console.log("any([false, false, true]) = " + str(any([false, false, true])));
console.log("any([false, false, false]) = " + str(any([false, false, false])));
console.log("any([0, 0, 1]) = " + str(any([0, 0, 1])));
console.log("any([0, 0, 0]) = " + str(any([0, 0, 0])));
console.log("any([]) = " + str(any([])));  // Empty is false

// Example 6: Leaderboard sorting
console.log("\nExample 6: Leaderboard sorting");
scores = [85, 92, 78, 95, 88];
players = ["Alice", "Bob", "Carol", "David", "Eve"];

console.log("Unsorted scores: " + str(scores));
sortedScores = sorted(scores, true);  // Highest first
console.log("Leaderboard: " + str(sortedScores));

// Example 7: Validation with all()
console.log("\nExample 7: Validation with all()");
function allPositive(numbers) {
    checks = [];
    for (num in numbers) {
        checks = checks + [num > 0];
    }
    return all(checks);
}

testData1 = [1, 2, 3, 4, 5];
testData2 = [1, -2, 3, 4, 5];

console.log("Data: " + str(testData1));
console.log("All positive? " + str(allPositive(testData1)));

console.log("Data: " + str(testData2));
console.log("All positive? " + str(allPositive(testData2)));

// Example 8: Search with any()
console.log("\nExample 8: Search with any()");
function containsNegative(numbers) {
    checks = [];
    for (num in numbers) {
        checks = checks + [num < 0];
    }
    return any(checks);
}

data1 = [1, 2, 3, 4, 5];
data2 = [1, 2, -3, 4, 5];

console.log("Data: " + str(data1));
console.log("Contains negative? " + str(containsNegative(data1)));

console.log("Data: " + str(data2));
console.log("Contains negative? " + str(containsNegative(data2)));

// Example 9: Data pairing with zip()
console.log("\nExample 9: Creating data records");
products = ["Laptop", "Mouse", "Keyboard"];
prices = [999.99, 29.99, 79.99];
stock = [5, 50, 25];

console.log("Product catalog:");
for (item in zip(products, prices, stock)) {
    product = item[0];
    price = item[1];
    quantity = item[2];
    console.log("  " + product + ": $" + str(price) + " (" + str(quantity) + " in stock)");
}

// Example 10: Palindrome check with reversed()
console.log("\nExample 10: Palindrome check");
function isPalindrome(text) {
    chars = [];
    i = 0;
    while (i < len(text)) {
        chars = chars + [text[i]];
        i = i + 1;
    }
    reversedChars = reversed(chars);
    return chars == reversedChars;
}

words = ["radar", "hello", "level", "world", "noon"];
for (word in words) {
    result = isPalindrome(word);
    console.log("\"" + word + "\" is palindrome: " + str(result));
}

// Example 11: Combining sorted and reversed
console.log("\nExample 11: Sorting in different orders");
values = [5, 2, 8, 1, 9, 3];

console.log("Original: " + str(values));
console.log("Sorted ascending: " + str(sorted(values)));
console.log("Sorted descending: " + str(sorted(values, true)));
console.log("Reversed original: " + str(reversed(values)));

// Example 12: Complex validation
console.log("\nExample 12: Complex validation");
function validateAllScores(scores) {
    // All scores must be between 0 and 100
    validChecks = [];
    for (score in scores) {
        isValid = score >= 0 && score <= 100;
        validChecks = validChecks + [isValid];
    }
    return all(validChecks);
}

function hasPassingScore(scores) {
    // Check if any score is >= 60
    passingChecks = [];
    for (score in scores) {
        isPassing = score >= 60;
        passingChecks = passingChecks + [isPassing];
    }
    return any(passingChecks);
}

testScores = [75, 82, 68, 91];
console.log("Scores: " + str(testScores));
console.log("All valid (0-100)? " + str(validateAllScores(testScores)));
console.log("Has passing score (>=60)? " + str(hasPassingScore(testScores)));

invalidScores = [75, 82, -5, 91];
console.log("\nScores: " + str(invalidScores));
console.log("All valid (0-100)? " + str(validateAllScores(invalidScores)));
console.log("Has passing score (>=60)? " + str(hasPassingScore(invalidScores)));

// Example 13: Creating lookup tables with zip
console.log("\nExample 13: Creating lookup tables");
keys = ["name", "age", "city"];
values = ["Alice", 30, "New York"];

// Create object from parallel arrays
obj = {};
for (pair in zip(keys, values)) {
    key = pair[0];
    value = pair[1];
    obj[key] = value;
}

console.log("Created object: " + str(obj));
console.log("Name: " + str(obj.name));
console.log("Age: " + str(obj.age));
console.log("City: " + str(obj.city));

console.log("\n=== Array Functions Complete ===");
