// ============================================
// Example: I/O and Formatting
// Category: standard-library/builtin
// Demonstrates: print(), format(), chr(), ord(), hex(), bin(), oct(), repr()
// ============================================

print("=== I/O and Formatting ===\n");

// print() - Console output (ML-compatible booleans)
print("Basic printing:");
print("  Number:", 42);
print("  String:", "hello");
print("  Boolean:", true);  // Prints "true" not "True"
print("  Array:", [1, 2, 3]);

// format() - Advanced number formatting
print("\n=== Number Formatting ===");

pi = 3.14159265359;
print("Pi with different precisions:");
print("  2 decimals: " + format(pi, ".2f"));
print("  4 decimals: " + format(pi, ".4f"));
print("  6 decimals: " + format(pi, ".6f"));

// Integer formatting
num = 42;
print("\nInteger formatting:");
print("  Default: " + format(num, "d"));
print("  Padded: " + format(num, "05d"));  // 00042
print("  Hex: " + format(num, "x"));       // 2a
print("  Binary: " + format(num, "b"));    // 101010

// Large numbers with separators
bigNum = 1000000;
print("\nLarge number: " + str(bigNum));
print("  With comma separator: " + format(bigNum, ","));

// Percentage formatting
score = 0.875;
print("\nPercentage:");
print("  " + format(score * 100, ".1f") + "%");

// chr() and ord() - Character/codepoint conversion
print("\n=== Character Encoding ===");

print("Character to codepoint:");
print("  ord('A') = " + str(ord("A")));     // 65
print("  ord('a') = " + str(ord("a")));     // 97
print("  ord('0') = " + str(ord("0")));     // 48
print("  ord(' ') = " + str(ord(" ")));     // 32

print("\nCodepoint to character:");
print("  chr(65) = '" + chr(65) + "'");     // 'A'
print("  chr(97) = '" + chr(97) + "'");     // 'a'
print("  chr(48) = '" + chr(48) + "'");     // '0'
print("  chr(8364) = '" + chr(8364) + "'"); // '€'

// Practical: Simple cipher
print("\n=== Caesar Cipher ===");

function caesarShift(text, shift) {
    result = "";
    i = 0;
    while (i < len(text)) {
        char = text[i:i+1];
        code = ord(char);

        // Shift uppercase letters
        if (code >= 65 && code <= 90) {
            newCode = ((code - 65 + shift) % 26) + 65;
            result = result + chr(newCode);
        }
        // Shift lowercase letters
        elif (code >= 97 && code <= 122) {
            newCode = ((code - 97 + shift) % 26) + 97;
            result = result + chr(newCode);
        }
        // Keep other characters
        else {
            result = result + char;
        }

        i = i + 1;
    }
    return result;
}

message = "Hello World";
encoded = caesarShift(message, 3);
decoded = caesarShift(encoded, 23);  // 26 - 3 = 23

print("Original: " + message);
print("Encoded: " + encoded);
print("Decoded: " + decoded);

// hex(), bin(), oct() - Base conversions
print("\n=== Number Base Conversions ===");

number = 255;
print("Number: " + str(number));
print("  Binary: " + bin(number));      // 0b11111111
print("  Octal: " + oct(number));       // 0o377
print("  Hexadecimal: " + hex(number)); // 0xff

number = 16;
print("\nNumber: " + str(number));
print("  Binary: " + bin(number));      // 0b10000
print("  Octal: " + oct(number));       // 0o20
print("  Hexadecimal: " + hex(number)); // 0x10

// Practical: Color code converter
print("\n=== RGB to Hex Color ===");

function rgbToHex(r, g, b) {
    // Remove '0x' prefix and pad to 2 digits
    rHex = hex(r)[2:];
    if (len(rHex) < 2) {
        rHex = "0" + rHex;
    }

    gHex = hex(g)[2:];
    if (len(gHex) < 2) {
        gHex = "0" + gHex;
    }

    bHex = hex(b)[2:];
    if (len(bHex) < 2) {
        bHex = "0" + bHex;
    }

    return "#" + rHex + gHex + bHex;
}

print("RGB(255, 0, 0) = " + rgbToHex(255, 0, 0));     // #ff0000 (red)
print("RGB(0, 255, 0) = " + rgbToHex(0, 255, 0));     // #00ff00 (green)
print("RGB(0, 0, 255) = " + rgbToHex(0, 0, 255));     // #0000ff (blue)
print("RGB(128, 128, 128) = " + rgbToHex(128, 128, 128)); // #808080 (gray)

// repr() - String representation
print("\n=== String Representation ===");

print("repr(42) = " + repr(42));
print("repr(3.14) = " + repr(3.14));
print("repr(true) = " + repr(true));     // "true"
print("repr('hello') = " + repr("hello"));

// Practical: Data table formatting
print("\n=== Formatted Table ===");

headers = ["Name", "Age", "Score"];
rows = [
    ["Alice", 25, 92.5],
    ["Bob", 30, 87.3],
    ["Charlie", 28, 95.1]
];

// Print header
print(headers[0] + "\t" + headers[1] + "\t" + headers[2]);
print("--------------------------------");

// Print rows
i = 0;
while (i < len(rows)) {
    row = rows[i];
    name = row[0];
    age = row[1];
    score = row[2];

    print(name + "\t" + str(age) + "\t" + format(score, ".1f"));
    i = i + 1;
}

// Summary statistics
scores = [92.5, 87.3, 95.1];
avgScore = sum(scores) / len(scores);
print("\nAverage Score: " + format(avgScore, ".2f"));

print("\n=== I/O and Formatting Complete ===");
