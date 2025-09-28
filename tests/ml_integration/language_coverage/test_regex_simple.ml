// Simple test of regex module
import regex;
import string;

// Test basic regex operations
text = "hello@example.com";
pattern = "@";

// Test regex.test
result = regex.test(pattern, text);
print("Contains @: " + string.toString(result));

// Test regex.replace_all
cleaned = regex.replace_all(text, "@", "_AT_");
print("Replaced: " + cleaned);

print("Basic regex operations work!");