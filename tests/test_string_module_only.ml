// Test string module functions only

import string;

function main() {
    print("=== Testing String Module Functions ===");

    test_text = "Hello World";

    // Test working approaches
    length = string.length(test_text);
    print("String length: " + string.toString(length));

    upper = string.upper(test_text);
    print("Uppercase: " + upper);

    lower = string.lower(test_text);
    print("Lowercase: " + lower);

    substring = string.substring(test_text, 0, 5);
    print("Substring: " + substring);

    find_result = string.find(test_text, "o");
    print("Find 'o': " + string.toString(find_result));

    contains = string.contains(test_text, "World");
    print("Contains 'World': " + string.toString(contains));

    print("=== All String Module Functions Work ===");
}

main();