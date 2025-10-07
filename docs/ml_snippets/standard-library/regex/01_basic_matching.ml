// ============================================
// Example: Basic Pattern Matching
// Category: standard-library/regex
// Demonstrates: search, match, fullmatch, test
// ============================================

import console;
import regex;

console.log("=== Basic Pattern Matching ===\n");

// Example 1: search() - Find pattern anywhere
console.log("Example 1: regex.search() - Find anywhere");
text = "The answer is 42";
match = regex.search('\d+', text);

if (match != null) {
    console.log("Found: " + match.group(0));        // "42"
    console.log("At position: " + str(match.start()));  // 14
} else {
    console.log("No match found");
}

// Example 2: match() - Match from start
console.log("\nExample 2: regex.match() - Match from start");
text1 = "42 is the answe";
text2 = "The answer is 42";

match1 = regex.match('\d+', text1);
if (match1 != null) {
    console.log("Text1 matched: " + match1.group(0));  // "42"
}

match2 = regex.match('\d+', text2);
if (match2 == null) {
    console.log("Text2 did not match (number not at start)");
}

// Example 3: fullmatch() - Match entire string
console.log("\nExample 3: regex.fullmatch() - Match entire string");
text1 = "42";
text2 = "42 extra";

match1 = regex.fullmatch('\d+', text1);
if (match1 != null) {
    console.log("Text1 fully matched: " + match1.group(0));
}

match2 = regex.fullmatch('\d+', text2);
if (match2 == null) {
    console.log("Text2 did not fully match (has extra characters)");
}

// Example 4: test() - Quick boolean check
console.log("\nExample 4: regex.test() - Quick check");
emails = [
    "user@example.com",
    "invalid.email",
    "admin@site.org",
    "not an email"
];

emailPattern = '\w+@\w+\.\w+';
console.log("Valid emails:");
for (email in emails) {
    if (regex.test(emailPattern, email)) {
        console.log("  " + email + " - valid");
    } else {
        console.log("  " + email + " - invalid");
    }
}

// Example 5: Multiple search patterns
console.log("\nExample 5: Different pattern types");
text = "Contact: john@example.com or call 555-1234";

// Find email
emailMatch = regex.search('\w+@\w+\.\w+', text);
if (emailMatch != null) {
    console.log("Email found: " + emailMatch.group(0));
}

// Find phone number
phoneMatch = regex.search('\d{3}-\d{4}', text);
if (phoneMatch != null) {
    console.log("Phone found: " + phoneMatch.group(0));
}

// Example 6: Extracting numbers
console.log("\nExample 6: Extracting numbers from text");
texts = [
    "Price: $19.99",
    "Temperature: -5 degrees",
    "Items: 42",
    "No numbers here"
];

for (t in texts) {
    match = regex.search('-?\d+\.?\d*', t);
    if (match != null) {
        console.log(t + " -> " + match.group(0));
    } else {
        console.log(t + " -> No numbe");
    }
}

// Example 7: Word boundaries
console.log("\nExample 7: Word boundaries");
text = "The cat catches the scattered cats";

// Find "cat" as whole word
match = regex.search('\bcat\b', text);
if (match != null) {
    console.log("Found 'cat' at position " + str(match.start()));
}

// Example 8: Position information
console.log("\nExample 8: Match position details");
text = "Find the number 42 in this text";
match = regex.search('\d+', text);

if (match != null) {
    console.log("Matched text: " + match.value());
    console.log("Start position: " + str(match.start()));
    console.log("End position: " + str(match.end()));
    span = match.span();
    console.log("Span: [" + str(span[0]) + ", " + str(span[1]) + "]");
}

// Example 9: Pattern validation
console.log("\nExample 9: Validating patterns");
validPattern = '\d+';
invalidPattern = '[a-z';  // Missing closing bracket
namedGroupPattern = '(?P<name>\w+)';

if (regex.isValid(validPattern)) {
    console.log("Valid: " + validPattern);
}

if (!regex.isValid(invalidPattern)) {
    console.log("Invalid: " + invalidPattern);
}

if (regex.isValid(namedGroupPattern)) {
    console.log("Valid: " + namedGroupPattern);
}

// Example 10: Counting matches
console.log("\nExample 10: Counting matches");
text = "I have 5 apples, 3 oranges, and 10 bananas";
count = regex.count('\d+', text);
console.log("Number of numbers in text: " + str(count));  // 3

text = "hello world hello universe hello";
count = regex.count('hello', text);
console.log("Number of 'hello' occurrences: " + str(count));  // 3

console.log("\n=== Basic Matching Complete ===");
