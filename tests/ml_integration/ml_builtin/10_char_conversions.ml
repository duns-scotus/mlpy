// Test builtin module: Character conversion functions
// Features tested: chr(), ord()
// NO imports needed - builtin functions are auto-imported

function test_chr_ascii() {
    results = {};

    // Uppercase letters
    results.chr_65 = chr(65);                    // "A"
    results.chr_90 = chr(90);                    // "Z"

    // Lowercase letters
    results.chr_97 = chr(97);                    // "a"
    results.chr_122 = chr(122);                  // "z"

    // Digits
    results.chr_48 = chr(48);                    // "0"
    results.chr_57 = chr(57);                    // "9"

    // Space and punctuation
    results.chr_32 = chr(32);                    // " "
    results.chr_33 = chr(33);                    // "!"
    results.chr_63 = chr(63);                    // "?"

    return results;
}

function test_ord_ascii() {
    results = {};

    // Uppercase letters
    results.ord_A = ord("A");                    // 65
    results.ord_Z = ord("Z");                    // 90

    // Lowercase letters
    results.ord_a = ord("a");                    // 97
    results.ord_z = ord("z");                    // 122

    // Digits
    results.ord_0 = ord("0");                    // 48
    results.ord_9 = ord("9");                    // 57

    // Space and punctuation
    results.ord_space = ord(" ");                // 32
    results.ord_exclaim = ord("!");              // 33
    results.ord_question = ord("?");             // 63

    return results;
}

function test_chr_ord_roundtrip() {
    results = {};

    // Roundtrip: code -> char -> code
    results.roundtrip_65 = ord(chr(65));         // 65
    results.roundtrip_97 = ord(chr(97));         // 97
    results.roundtrip_48 = ord(chr(48));         // 48

    // Roundtrip: char -> code -> char
    results.roundtrip_A = chr(ord("A"));         // "A"
    results.roundtrip_z = chr(ord("z"));         // "z"
    results.roundtrip_5 = chr(ord("5"));         // "5"

    return results;
}

function test_alphabet_generation() {
    results = {};

    // Generate uppercase alphabet
    uppercase = [];
    for (i in range(65, 91)) {  // 65='A' to 90='Z'
        uppercase = uppercase + [chr(i)];
    }
    results.uppercase_count = len(uppercase);    // 26
    results.first_letter = uppercase[0];         // "A"
    results.last_letter = uppercase[25];         // "Z"

    // Generate lowercase alphabet
    lowercase = [];
    for (i in range(97, 123)) {  // 97='a' to 122='z'
        lowercase = lowercase + [chr(i)];
    }
    results.lowercase_count = len(lowercase);    // 26
    results.first_lower = lowercase[0];          // "a"
    results.last_lower = lowercase[25];          // "z"

    return results;
}

function test_digit_generation() {
    results = {};

    // Generate digit characters
    digits = [];
    for (i in range(48, 58)) {  // 48='0' to 57='9'
        digits = digits + [chr(i)];
    }

    results.digit_count = len(digits);           // 10
    results.first_digit = digits[0];             // "0"
    results.last_digit = digits[9];              // "9"

    return results;
}

function test_character_range_check() {
    results = {};

    // Check if character is uppercase letter
    char_code = ord("B");
    is_uppercase = char_code >= 65 && char_code <= 90;
    results.B_is_uppercase = is_uppercase;       // true

    // Check if character is lowercase letter
    char_code2 = ord("m");
    is_lowercase = char_code2 >= 97 && char_code2 <= 122;
    results.m_is_lowercase = is_lowercase;       // true

    // Check if character is digit
    char_code3 = ord("7");
    is_digit = char_code3 >= 48 && char_code3 <= 57;
    results.seven_is_digit = is_digit;           // true

    return results;
}

function test_case_conversion() {
    results = {};

    // Uppercase to lowercase (manual)
    upper_code = ord("A");
    lower_code = upper_code + 32;  // Difference between 'A' and 'a'
    results.A_to_a = chr(lower_code);            // "a"

    // Lowercase to uppercase (manual)
    lower_code2 = ord("z");
    upper_code2 = lower_code2 - 32;
    results.z_to_Z = chr(upper_code2);           // "Z"

    return results;
}

function test_character_arithmetic() {
    results = {};

    // Next character
    code_A = ord("A");
    code_B = code_A + 1;
    results.next_after_A = chr(code_B);          // "B"

    // Previous character
    code_Z = ord("Z");
    code_Y = code_Z - 1;
    results.prev_before_Z = chr(code_Y);         // "Y"

    // Skip characters
    code_a = ord("a");
    code_c = code_a + 2;
    results.skip_from_a = chr(code_c);           // "c"

    return results;
}

function test_caesar_cipher() {
    results = {};

    // Simple Caesar cipher (shift by 3)
    message = "ABC";
    encrypted = [];

    // Manual iteration over string characters
    for (i in range(len(message))) {
        // Get character code and shift
        code = ord("A") + i;  // Simplified: assume A, B, C
        shifted = code + 3;
        encrypted = encrypted + [chr(shifted)];
    }

    results.encrypted_len = len(encrypted);      // 3

    return results;
}

function test_character_classification() {
    results = {};

    // Count character types in a range
    uppercase_count = 0;
    lowercase_count = 0;
    digit_count = 0;
    other_count = 0;

    for (i in range(48, 123)) {  // '0' to 'z'
        if (i >= 65 && i <= 90) {
            uppercase_count = uppercase_count + 1;
        } elif (i >= 97 && i <= 122) {
            lowercase_count = lowercase_count + 1;
        } elif (i >= 48 && i <= 57) {
            digit_count = digit_count + 1;
        } else {
            other_count = other_count + 1;
        }
    }

    results.uppercase = uppercase_count;         // 26
    results.lowercase = lowercase_count;         // 26
    results.digits = digit_count;                // 10
    results.other = other_count;                 // 13 (58-64, 91-96)

    return results;
}

function main() {
    all_results = {};

    all_results.chr_ascii = test_chr_ascii();
    all_results.ord_ascii = test_ord_ascii();
    all_results.roundtrip = test_chr_ord_roundtrip();
    all_results.alphabet = test_alphabet_generation();
    all_results.digits = test_digit_generation();
    all_results.range_check = test_character_range_check();
    all_results.case_conv = test_case_conversion();
    all_results.arithmetic = test_character_arithmetic();
    all_results.caesar = test_caesar_cipher();
    all_results.classification = test_character_classification();

    return all_results;
}

// Run tests
test_results = main();
