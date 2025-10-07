// ============================================
// Example: Utility Functions
// Category: standard-library/builtin
// Demonstrates: abs(), min(), max(), round(), sum(), all(), any(), reversed()
// ============================================

print("=== Utility Functions ===\n");

// abs() - Absolute value
print("Absolute values:");
print("  abs(-5) = " + str(abs(-5)));           // 5
print("  abs(3.14) = " + str(abs(3.14)));       // 3.14
print("  abs(-42.7) = " + str(abs(-42.7)));     // 42.7

// min() and max() - Find extremes
print("\n=== Finding Minimum and Maximum ===");

numbers = [42, 7, 23, 91, 15, 3, 67];
print("Numbers: " + str(numbers));
print("  min(numbers) = " + str(min(numbers)));   // 3
print("  max(numbers) = " + str(max(numbers)));   // 91

// min/max with multiple arguments
print("\nDirect comparison:");
print("  min(5, 2, 8, 1, 9) = " + str(min(5, 2, 8, 1, 9)));  // 1
print("  max(5, 2, 8, 1, 9) = " + str(max(5, 2, 8, 1, 9)));  // 9

// round() - Rounding numbers
print("\n=== Rounding ===");

pi = 3.14159265359;
print("Pi = " + str(pi));
print("  round(pi) = " + str(round(pi)));           // 3
print("  round(pi, 2) = " + str(round(pi, 2)));     // 3.14
print("  round(pi, 4) = " + str(round(pi, 4)));     // 3.1416

price = 19.99;
print("\nPrice = $" + str(price));
print("  Rounded: $" + str(round(price)));          // 20

// sum() - Sum array elements
print("\n=== Summing Arrays ===");

values = [10, 20, 30, 40, 50];
print("Values: " + str(values));
print("  sum(values) = " + str(sum(values)));       // 150

// sum() with start value
print("  sum(values, 100) = " + str(sum(values, 100)));  // 250

// Practical: Calculate average
print("\nCalculating average:");
total = sum(values);
count = len(values);
average = total / count;
print("  Average: " + str(average));

// all() - Check if all elements are truthy
print("\n=== All Elements Check ===");

allTrue = [true, true, true];
print("all([true, true, true]) = " + str(all(allTrue)));  // true

someTrue = [true, false, true];
print("all([true, false, true]) = " + str(all(someTrue))); // false

allPositive = [1, 2, 3, 4];
print("all([1, 2, 3, 4]) = " + str(all(allPositive))); // true

hasZero = [1, 0, 3];
print("all([1, 0, 3]) = " + str(all(hasZero)));  // false (0 is falsy)

// Practical: Validation
print("\nValidating data:");

function validateAges(ages) {
    // Check all ages are positive
    positiveChecks = [];
    i = 0;
    while (i < len(ages)) {
        positiveChecks = positiveChecks + [ages[i] > 0];
        i = i + 1;
    }
    return all(positiveChecks);
}

validAges = [25, 30, 35, 40];
invalidAges = [25, -5, 35, 40];

print("  Valid ages [25, 30, 35, 40]: " + str(validateAges(validAges)));
print("  Invalid ages [25, -5, 35, 40]: " + str(validateAges(invalidAges)));

// any() - Check if any element is truthy
print("\n=== Any Element Check ===");

allFalse = [false, false, false];
print("any([false, false, false]) = " + str(any(allFalse)));  // false

someTrue = [false, true, false];
print("any([false, true, false]) = " + str(any(someTrue)));  // true

hasPositive = [0, -1, 0, 5];
print("any([0, -1, 0, 5]) = " + str(any(hasPositive)));  // true (5 is truthy)

// Practical: Search
print("\nSearching for pattern:");

function containsKeyword(texts, keyword) {
    matches = [];
    i = 0;
    while (i < len(texts)) {
        // Simple contains check (in real code, use indexOf or regex)
        text = texts[i];
        matches = matches + [len(text) > 0];  // Simplified check
        i = i + 1;
    }
    return any(matches);
}

messages = ["Hello world", "Good morning", "Have a nice day"];
print("  Messages contain text: " + str(containsKeyword(messages, "hello")));

// reversed() - Reverse sequences
print("\n=== Reversing Sequences ===");

numbers = [1, 2, 3, 4, 5];
print("Original: " + str(numbers));
print("Reversed: " + str(reversed(numbers)));

text = "hello";
letters = reversed(text);
reversedText = "";
i = 0;
while (i < len(letters)) {
    reversedText = reversedText + letters[i];
    i = i + 1;
}
print("\nOriginal text: " + text);
print("Reversed text: " + reversedText);

// Practical: Palindrome checker
print("\n=== Palindrome Checker ===");

function isPalindrome(text) {
    letters = [];
    i = 0;
    while (i < len(text)) {
        letters = letters + [text[i:i+1]];
        i = i + 1;
    }

    reversedLetters = reversed(letters);

    i = 0;
    while (i < len(letters)) {
        if (letters[i] != reversedLetters[i]) {
            return false;
        }
        i = i + 1;
    }

    return true;
}

words = ["racecar", "hello", "level", "world", "noon"];
print("Testing palindromes:");
i = 0;
while (i < len(words)) {
    word = words[i];
    result = isPalindrome(word);
    status = result ? "is" : "is not";
    print("  '" + word + "' " + status + " a palindrome");
    i = i + 1;
}

// Combining utilities
print("\n=== Statistical Analysis ===");

dataset = [15, 23, 7, 42, 31, 18, 9, 27];
print("Dataset: " + str(dataset));

// Basic statistics
total = sum(dataset);
count = len(dataset);
average = total / count;
minimum = min(dataset);
maximum = max(dataset);
rangeVal = maximum - minimum;

print("\nStatistics:");
print("  Count: " + str(count));
print("  Sum: " + str(total));
print("  Average: " + str(round(average, 2)));
print("  Min: " + str(minimum));
print("  Max: " + str(maximum));
print("  Range: " + str(rangeVal));

// Check data quality
aboveAvg = [];
i = 0;
while (i < len(dataset)) {
    aboveAvg = aboveAvg + [dataset[i] > average];
    i = i + 1;
}
hasAboveAvg = any(aboveAvg);

// Check if all values are positive
allPositive = [];
i = 0;
while (i < len(dataset)) {
    allPositive = allPositive + [dataset[i] > 0];
    i = i + 1;
}
allAboveZero = all(allPositive);

print("\nQuality checks:");
print("  Has values above average: " + str(hasAboveAvg));
print("  All values positive: " + str(allAboveZero));

print("\n=== Utilities Complete ===");
