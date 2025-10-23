// ============================================
// Example: Finding Multiple Matches
// Category: standard-library/regex
// Demonstrates: findall(), finditer()
// ============================================

import console;
import regex;

console.log("=== Finding Multiple Matches ===\n");

// Example 1: findall() - Simple extraction
console.log("Example 1: Extract all numbers");
text = "I have 5 apples, 3 oranges, and 10 bananas";
numbers = regex.findall('\d+', text);

console.log("Numbers found: " + str(numbers));  // ["5", "3", "10"]
console.log("Count: " + str(len(numbers)));

// Example 2: findall() with groups
console.log("\nExample 2: Extract all phone numbers");
text = "Call 555-1234 or 800-5678 for assistance";
phones = regex.findall('(\d{3})-(\d{4})', text);

console.log("Phone numbers:");
for (phone in phones) {
    console.log("  " + phone);  // Note: groups returned as strings
}

// Example 3: finditer() for detailed information
console.log("\nExample 3: Iterate with match details");
text = "Find 42 and 123 and 7 in this text";
pattern = regex.compile('\d+');
matches = pattern.finditer(text);

console.log("Found " + str(len(matches)) + " numbers:");
for (match in matches) {
    value = match.group(0);
    position = match.start();
    console.log("  " + value + " at position " + str(position));
}

// Example 4: Extract emails
console.log("\nExample 4: Extract all email addresses");
text = "Contact: john@example.com, admin@site.org, or support@company.net";
emails = regex.findall('\w+@\w+\.\w+', text);

console.log("Email addresses:");
for (email in emails) {
    console.log("  " + email);
}

// Example 5: Extract URLs
console.log("\nExample 5: Extract all URLs");
text = "Visit https://example.com or http://site.org/docs for info";
urls = regex.findall('https?://[\w./]+', text);

console.log("URLs found:");
for (url in urls) {
    console.log("  " + url);
}

// Example 6: Extract hashtags
console.log("\nExample 6: Extract hashtags");
text = "Love #programming in #ML! #coding is fun #tech";
hashtags = regex.findall('#\w+', text);

console.log("Hashtags: " + str(hashtags));

// Example 7: Extract quoted strings
console.log("\nExample 7: Extract quoted strings");
text = "He said \"hello\" and she replied \"hi there\"";
quoted = regex.findall('"([^"]+)"', text);

console.log("Quoted strings:");
for (quotedStr in quoted) {
    console.log("  " + quotedStr);
}

// Example 8: Word extraction
console.log("\nExample 8: Extract all words");
text = "The quick brown fox jumps over the lazy dog";
words = regex.findall('\w+', text);

console.log("Words: " + str(words));
console.log("Word count: " + str(len(words)));

// Example 9: Extract key-value pairs
console.log("\nExample 9: Parse key-value pairs");
text = "width=800, height=600, fps=60";
pattern = regex.compile('(\w+)=(\d+)');
matches = pattern.finditer(text);

console.log("Configuration:");
for (match in matches) {
    key = match.group(1);
    value = match.group(2);
    console.log("  " + key + " = " + value);
}

// Example 10: Extract date components
console.log("\nExample 10: Extract dates");
text = "Events on 2025-10-05, 2025-11-15, and 2025-12-25";
pattern = regex.compile('(\d{4})-(\d{2})-(\d{2})');
matches = pattern.finditer(text);

console.log("Dates found:");
for (match in matches) {
    year = match.group(1);
    month = match.group(2);
    day = match.group(3);
    console.log("  Year: " + year + ", Month: " + month + ", Day: " + day);
}

// Example 11: Extract IP addresses
console.log("\nExample 11: Extract IP addresses");
text = "Servers at 192.168.1.1 and 10.0.0.1 are online";
ips = regex.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text);

console.log("IP addresses: " + str(ips));

// Example 12: Processing log entries
console.log("\nExample 12: Parse multiple log entries");
logs = "[ERROR] 10:32:15 - Failed\n[INFO] 10:32:20 - Started\n[WARN] 10:32:25 - Memory";
pattern = regex.compile('\[(\w+)\] ([\d:]+) - (.+)');
matches = pattern.finditer(logs);

console.log("Log entries:");
for (match in matches) {
    level = match.group(1);
    time = match.group(2);
    msg = match.group(3);
    console.log("  [" + level + "] " + time + ": " + msg);
}

// Example 13: Count word frequencies
console.log("\nExample 13: Count word occurrences");
text = "the quick brown fox jumps over the lazy dog the cat";
words = regex.findall('\w+', text);

// Count "the" occurrences
theCount = 0;
for (word in words) {
    if (word == "the") {
        theCount = theCount + 1;
    }
}
console.log("The word 'the' appears " + str(theCount) + " times");

// Example 14: Extract with positions
console.log("\nExample 14: Extract with position information");
text = "Error at line 10, warning at line 25, error at line 42";
pattern = regex.compile('(error|warning) at line (\d+)', regex.IGNORECASE());
matches = pattern.finditer(text);

console.log("Issues found:");
for (match in matches) {
    type = match.group(1);
    line = match.group(2);
    pos = match.start();
    console.log("  " + type + " on line " + line + " (text position: " + str(pos) + ")");
}

// Example 15: Extract and validate
console.log("\nExample 15: Extract and filte");
text = "Prices: $19.99, $5.00, $150.00, $0.99";
pricePattern = regex.compile('\$(\d+\.\d{2})');
matches = pricePattern.finditer(text);

console.log("Prices over $10:");
for (match in matches) {
    priceStr = match.group(1);
    // In real code, you'd convert to number and compare
    console.log("  $" + priceStr);
}

console.log("\n=== Finding Matches Complete ===");
