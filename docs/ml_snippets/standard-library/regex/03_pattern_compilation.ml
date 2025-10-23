// ============================================
// Example: Pattern Compilation and Flags
// Category: standard-library/regex
// Demonstrates: compile(), IGNORECASE, MULTILINE, DOTALL, VERBOSE
// ============================================

import console;
import regex;

console.log("=== Pattern Compilation and Flags ===\n");

// Example 1: Basic pattern compilation
console.log("Example 1: Compiling patterns for reuse");
emailPattern = regex.compile('\w+@\w+\.\w+');

emails = [
    "john@example.com",
    "invalid",
    "admin@site.org"
];

console.log("Checking emails:");
for (email in emails) {
    if (emailPattern.test(email)) {
        console.log("  " + email + " - valid");
    } else {
        console.log("  " + email + " - invalid");
    }
}

// Example 2: IGNORECASE flag
console.log("\nExample 2: Case-insensitive matching");
pattern = regex.compile('hello', regex.IGNORECASE());

texts = ["hello", "HELLO", "Hello", "HeLLo"];
for (text in texts) {
    if (pattern.test(text)) {
        console.log(text + " matches (case-insensitive)");
    }
}

// Example 3: MULTILINE flag
console.log("\nExample 3: Multiline mode (^ and $ match line boundaries)");
text = "First line\nSecond line\nThird line";
pattern = regex.compile('^Second', regex.MULTILINE());

match = pattern.search(text);
if (match != null) {
    console.log("Found 'Second' at start of a line");
    console.log("Position: " + str(match.start()));
}

// Example 4: DOTALL flag
console.log("\nExample 4: DOTALL mode (. matches newlines)");
text = "<div>\n  Content\n</div>";

// Without DOTALL - won't match across newlines
pattern1 = regex.compile('<div>.*</div>');
match1 = pattern1.search(text);
if (match1 == null) {
    console.log("Without DOTALL: No match (. doesn't match newlines)");
}

// With DOTALL - matches across newlines
pattern2 = regex.compile('<div>.*</div>', regex.DOTALL());
match2 = pattern2.search(text);
if (match2 != null) {
    console.log("With DOTALL: Match found!");
}

// Example 5: Combining multiple flags
console.log("\nExample 5: Combining flags");
text = "Hello World\nhello universe";

// Combine IGNORECASE and MULTILINE
flags = regex.IGNORECASE() + regex.MULTILINE();
pattern = regex.compile('^hello', flags);

matches = pattern.finditer(text);
console.log("Found " + str(len(matches)) + " lines starting with 'hello' (case-insensitive)");

// Example 6: Pattern methods
console.log("\nExample 6: Using compiled pattern methods");
phonePattern = regex.compile('(\d{3})-(\d{4})');
text = "Call 555-1234 or 800-5678 for help";

// search() method
match = phonePattern.search(text);
if (match != null) {
    console.log("First phone: " + match.group(0));
}

// findall() method
allPhones = phonePattern.findall(text);
console.log("All phones: " + str(allPhones));

// count() method
count = phonePattern.count(text);
console.log("Total phone numbers: " + str(count));

// Example 7: Pattern reuse for validation
console.log("\nExample 7: Reusable validation patterns");
urlPattern = regex.compile('https?://[\w.]+(/[\w/]*)?');
ipPattern = regex.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}');
datePattern = regex.compile('\d{4}-\d{2}-\d{2}');

data = {
    url: "https://example.com/api",
    ip: "192.168.1.1",
    date: "2025-10-05"
};

console.log("Validation results:");
console.log("  URL valid: " + str(urlPattern.test(data.url)));
console.log("  IP valid: " + str(ipPattern.test(data.ip)));
console.log("  Date valid: " + str(datePattern.test(data.date)));

// Example 8: Pattern information
console.log("\nExample 8: Accessing pattern information");
pattern = regex.compile('\d+', regex.IGNORECASE());
console.log("Pattern: " + pattern.getPattern());
console.log("Flags: " + str(pattern.getFlags()));
console.log("String representation: " + pattern.toString());

// Example 9: Case-insensitive search with groups
console.log("\nExample 9: Case-insensitive with capturing groups");
pattern = regex.compile('(ERROR|WARNING|INFO):\s*(.+)', regex.IGNORECASE());
logs = [
    "ERROR: System failure",
    "warning: Low disk space",
    "Info: Task completed"
];

for (log in logs) {
    match = pattern.search(log);
    if (match != null) {
        level = match.group(1);
        message = match.group(2);
        console.log(level + " -> " + message);
    }
}

// Example 10: Performance comparison
console.log("\nExample 10: Compiled pattern performance");
text = "Find numbers 1, 2, 3, 4, 5, 6, 7, 8, 9, 10";
patternStr = '\d+';

// Using compiled pattern (more efficient for repeated use)
compiledPattern = regex.compile(patternStr);
count1 = compiledPattern.count(text);
console.log("Compiled pattern found " + str(count1) + " numbers");

// Module-level function (compiles pattern each time)
count2 = regex.count(patternStr, text);
console.log("Module function found " + str(count2) + " numbers");
console.log("(Compiled patterns are more efficient for repeated use)");

console.log("\n=== Pattern Compilation Complete ===");
