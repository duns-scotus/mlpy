// ============================================
// Example: Capturing Groups
// Category: standard-library/regex
// Demonstrates: group(), groups(), groupDict(), named groups
// ============================================

import console;
import regex;

console.log("=== Capturing Groups ===\n");

// Example 1: Basic group capturing
console.log("Example 1: Basic numbered groups");
text = "Call 555-1234 for information";
match = regex.search('(\d{3})-(\d{4})', text);

if (match != null) {
    console.log("Full match: " + match.group(0));    // "555-1234"
    console.log("Area code: " + match.group(1));     // "555"
    console.log("Number: " + match.group(2));        // "1234"
}

// Example 2: groups() - All captured groups
console.log("\nExample 2: Getting all groups as array");
text = "Date: 2025-10-05";
match = regex.search('(\d{4})-(\d{2})-(\d{2})', text);

if (match != null) {
    allGroups = match.groups();
    console.log("Year: " + allGroups[0]);    // "2025"
    console.log("Month: " + allGroups[1]);   // "10"
    console.log("Day: " + allGroups[2]);     // "05"
    console.log("Group count: " + str(match.groupCount()));  // 3
}

// Example 3: Named groups
console.log("\nExample 3: Named capturing groups");
pattern = '(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})';
text = "Event on 2025-10-05";
match = regex.search(pattern, text);

if (match != null) {
    console.log("Year: " + match.group("yea"));
    console.log("Month: " + match.group("month"));
    console.log("Day: " + match.group("day"));
}

// Example 4: groupDict() - Named groups as object
console.log("\nExample 4: Named groups as dictionary");
pattern = '(?P<protocol>https?)://(?P<domain>[\w.]+)(?P<path>/[\w/]*)?';
text = "Visit https://example.com/docs/api";
match = regex.search(pattern, text);

if (match != null) {
    groups = match.groupDict();
    console.log("Protocol: " + groups.protocol);
    console.log("Domain: " + groups.domain);
    console.log("Path: " + str(groups.path));
}

// Example 5: Parsing email addresses
console.log("\nExample 5: Parsing email addresses");
pattern = '(?P<username>\w+)@(?P<domain>\w+)\.(?P<tld>\w+)';
emails = [
    "john@example.com",
    "admin@site.org",
    "user@company.net"
];

for (email in emails) {
    match = regex.search(pattern, email);
    if (match != null) {
        parts = match.groupDict();
        console.log(email + ":");
        console.log("  Username: " + parts.username);
        console.log("  Domain: " + parts.domain);
        console.log("  TLD: " + parts.tld);
    }
}

// Example 6: Parsing log entries
console.log("\nExample 6: Parsing log entries");
logPattern = '\[(?P<level>\w+)\] (?P<timestamp>[\d:]+) - (?P<message>.+)';
logs = [
    "[ERROR] 10:32:15 - Connection failed",
    "[INFO] 10:32:20 - Server started",
    "[WARN] 10:32:25 - High memory usage"
];

for (log in logs) {
    match = regex.search(logPattern, log);
    if (match != null) {
        data = match.groupDict();
        console.log("Level: " + data.level);
        console.log("Time: " + data.timestamp);
        console.log("Message: " + data.message);
        console.log("---");
    }
}

// Example 7: Optional groups
console.log("\nExample 7: Optional capturing groups");
pattern = '(\d{3})-?(\d{4})';  // Dash is optional
texts = ["555-1234", "5551234"];

for (text in texts) {
    match = regex.search(pattern, text);
    if (match != null) {
        console.log(text + " -> Area: " + match.group(1) + ", Num: " + match.group(2));
    }
}

// Example 8: Nested groups
console.log("\nExample 8: Nested capturing groups");
pattern = '((https?)://([\w.]+))';
text = "Link: https://example.com";
match = regex.search(pattern, text);

if (match != null) {
    console.log("Full URL: " + match.group(1));      // "https://example.com"
    console.log("Protocol: " + match.group(2));      // "https"
    console.log("Domain: " + match.group(3));        // "example.com"
}

// Example 9: Group position information
console.log("\nExample 9: Group positions");
text = "Price: $19.99 - Sale: $14.99";
pattern = '\$(\d+\.\d+)';
match = regex.search(pattern, text);

if (match != null) {
    console.log("Full match: " + match.group(0));
    console.log("Full match position: " + str(match.start(0)));
    console.log("Group 1 value: " + match.group(1));
    console.log("Group 1 position: " + str(match.start(1)));
}

// Example 10: Processing structured data
console.log("\nExample 10: Processing structured data");
pattern = '(?P<name>\w+)\s*=\s*(?P<value>\d+)';
configLines = [
    "width = 800",
    "height = 600",
    "fps = 60"
];

config = {};
for (line in configLines) {
    match = regex.search(pattern, line);
    if (match != null) {
        data = match.groupDict();
        console.log("Setting " + data.name + " to " + data.value);
        // Note: In real code you'd store: config[data.name] = data.value;
    }
}

console.log("\n=== Capturing Groups Complete ===");
