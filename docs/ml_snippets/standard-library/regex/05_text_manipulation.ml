// ============================================
// Example: Text Manipulation
// Category: standard-library/regex
// Demonstrates: split(), sub(), subn(), escape()
// ============================================

import console;
import regex;

console.log("=== Text Manipulation ===\n");

// Example 1: split() - Basic splitting
console.log("Example 1: Split by delimite");
text = "apple,banana,cherry,date";
parts = regex.split(',', text);
console.log("Parts: " + str(parts));

// Example 2: split() with multiple delimiters
console.log("\nExample 2: Split by multiple delimiters");
text = "apple,banana;cherry:date";
parts = regex.split('[,;:]', text);
console.log("Parts: " + str(parts));

// Example 3: split() with whitespace
console.log("\nExample 3: Split by whitespace");
text = "The   quick  brown\tfox";
words = regex.split('\s+', text);
console.log("Words: " + str(words));

// Example 4: split() with maxsplit
console.log("\nExample 4: Limited splits");
text = "one,two,three,four,five";
parts = regex.split(',', text, 2);  // Max 2 splits
console.log("Limited split: " + str(parts));

// Example 5: sub() - Simple replacement
console.log("\nExample 5: Replace text");
text = "I have 5 apples and 3 oranges";
result = regex.sub('\d+', 'X', text);
console.log("Before: " + text);
console.log("After: " + result);

// Example 6: sub() with backreferences
console.log("\nExample 6: Swap with backreferences");
text = "First Last";
result = regex.sub('(\w+) (\w+)', '\2, \1', text);
console.log("Before: " + text);
console.log("After: " + result);  // "Last, First"

// Example 7: sub() for formatting phone numbers
console.log("\nExample 7: Format phone numbers");
phones = ["5551234", "8005678", "5559999"];
pattern = regex.compile('(\d{3})(\d{4})');

for (phone in phones) {
    formatted = pattern.sub('\1-\2', phone);
    console.log(phone + " -> " + formatted);
}

// Example 8: subn() - Replacement with count
console.log("\nExample 8: Replace and count");
text = "I have 5 apples and 3 oranges and 10 bananas";
result = regex.subn('\d+', 'X', text);
console.log("Result: " + result.result);
console.log("Replacements made: " + str(result.count));

// Example 9: sub() with limit
console.log("\nExample 9: Limited replacements");
text = "Replace this and this and this";
result = regex.sub('this', 'that', text, 2);  // Replace first 2
console.log("Result: " + result);

// Example 10: Redacting sensitive data
console.log("\nExample 10: Redact email addresses");
text = "Contact john@example.com or admin@site.org for help";
redacted = regex.sub('\w+@\w+\.\w+', '[EMAIL REDACTED]', text);
console.log("Original: " + text);
console.log("Redacted: " + redacted);

// Example 11: Redact credit cards
console.log("\nExample 11: Redact credit card numbers");
text = "Card: 1234-5678-9012-3456";
redacted = regex.sub('\d{4}-\d{4}-\d{4}-\d{4}', 'XXXX-XXXX-XXXX-XXXX', text);
console.log("Original: " + text);
console.log("Redacted: " + redacted);

// Example 12: Normalize whitespace
console.log("\nExample 12: Normalize whitespace");
text = "Too    many   spaces\t\there";
normalized = regex.sub('\s+', ' ', text);
console.log("Before: " + text);
console.log("After: " + normalized);

// Example 13: Remove HTML tags
console.log("\nExample 13: Remove HTML tags");
html = "<p>Hello <b>world</b>!</p>";
plain = regex.sub('<[^>]+>', '', html);
console.log("HTML: " + html);
console.log("Plain: " + plain);

// Example 14: escape() - Escape special characters
console.log("\nExample 14: Escape special regex characters");
specialChars = "Price: $5.99 (sale!)";
escaped = regex.escape(specialChars);
console.log("Original: " + specialChars);
console.log("Escaped: " + escaped);

// Use escaped string in pattern
pattern = regex.compile(escaped);
if (pattern.test(specialChars)) {
    console.log("Exact match found!");
}

// Example 15: Format dates
console.log("\nExample 15: Reformat dates");
dates = ["2025-10-05", "2025-11-15", "2025-12-25"];
pattern = regex.compile('(\d{4})-(\d{2})-(\d{2})');

console.log("US format (MM/DD/YYYY):");
for (date in dates) {
    usFormat = pattern.sub('\2/\3/\1', date);
    console.log("  " + date + " -> " + usFormat);
}

// Example 16: Clean data
console.log("\nExample 16: Clean and normalize data");
data = "  Item:  APPLE123   ";
cleaned = data;

// Remove leading/trailing whitespace (using trim in real code)
cleaned = regex.sub('^\s+|\s+$', '', cleaned);

// Normalize internal whitespace
cleaned = regex.sub('\s+', ' ', cleaned);

// Convert to lowercase (using string method in real code)
console.log("Cleaned: " + cleaned);

// Example 17: URL slug generation
console.log("\nExample 17: Generate URL slugs");
titles = [
    "Hello World!",
    "My First Post",
    "Special Characters: @#$"
];

for (title in titles) {
    slug = title;
    // Remove special characters
    slug = regex.sub('[^a-zA-Z0-9\s-]', '', slug);
    // Replace spaces with hyphens
    slug = regex.sub('\s+', '-', slug);
    // Lowercase (in real code)
    console.log(title + " -> " + slug);
}

// Example 18: Mask sensitive data partially
console.log("\nExample 18: Partial masking");
ssn = "123-45-6789";
masked = regex.sub('\d(?=\d{4})', 'X', ssn);
console.log("SSN: " + ssn);
console.log("Masked: " + masked);  // XXX-XX-6789

// Example 19: Multiple replacements
console.log("\nExample 19: Chain replacements");
text = "Visit http://example.com or https://site.org";
result = text;
result = regex.sub('http://', 'HTTP://', result);
result = regex.sub('https://', 'HTTPS://', result);
console.log("Before: " + text);
console.log("After: " + result);

// Example 20: Pattern-based text cleanup
console.log("\nExample 20: Remove duplicate words");
text = "The the quick quick brown fox";
cleaned = regex.sub('\b(\w+)\s+\1\b', '\1', text, 0, regex.IGNORECASE());
console.log("Before: " + text);
console.log("After: " + cleaned);

console.log("\n=== Text Manipulation Complete ===");
