// Test different import access patterns
import string;
import regex;

// Test individual function calls vs object access
text = "hello";

// This should work - individual functions from registry
result1 = string.upper(text);
print("String object access: " + result1);

// Test if individual regex functions work from registry
pattern = "h.*o";
result2 = regex.test(pattern, text);
print("Regex function access: " + string.toString(result2));

print("Import mechanism test completed!");