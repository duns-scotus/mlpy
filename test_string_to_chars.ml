// Test file for string.toChars() function
// Demonstrates converting strings to character arrays and processing them

import string;

function test_string_to_chars() {
    print("=== String toChars() Function Test ===");

    // Basic string to chars conversion
    text = "Hello";
    chars = string.toChars(text);
    print("Text:", text);
    print("Characters:", chars);
    print("Character count:", string.length(text));

    // Test with special characters and numbers
    special_text = "Hi! 123";
    special_chars = string.toChars(special_text);
    print("\nSpecial text:", special_text);
    print("Special characters:", special_chars);

    // Process characters - count vowels
    vowel_count = 0;
    vowels = string.toChars("aeiouAEIOU");

    for (char in chars) {
        for (vowel in vowels) {
            if (char == vowel) {
                vowel_count = vowel_count + 1;
            }
        }
    }

    print("\nVowel analysis for '", text, "':");
    print("Vowels found:", vowel_count);

    // Character array processing
    char_array = string.toChars(text);
    print("\nCharacter array processing:");
    print("Original chars:", char_array);
    print("First character:", char_array[0]);
    print("Last character:", char_array[string.length(text) - 1]);

    // Test empty string
    empty_chars = string.toChars("");
    print("\nEmpty string test:");
    print("Empty chars:", empty_chars);
    print("Empty length:", string.length(""));

    return {
        original: text,
        characters: chars,
        vowel_count: vowel_count,
        char_array: char_array,
        special_test: special_chars
    };
}

// Run the test
result = test_string_to_chars();
print("\n=== Test Results Summary ===");
print("Test completed successfully!");
print("Result object:", result);