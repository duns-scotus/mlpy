// ============================================
// Example: String Conversion Functions
// Category: language-reference/builtin
// Demonstrates: chr(), ord(), hex(), bin(), oct(), format()
// ============================================

import console;

console.log("=== String Conversion Functions ===\n");

// Example 1: chr() - Code point to character
console.log("Example 1: chr() - Code point to character");
console.log("chr(65) = \"" + chr(65) + "\"");      // "A"
console.log("chr(97) = \"" + chr(97) + "\"");      // "a"
console.log("chr(48) = \"" + chr(48) + "\"");      // "0"
console.log("chr(33) = \"" + chr(33) + "\"");      // "!"
console.log("chr(8364) = \"" + chr(8364) + "\"");  // "€"

// Example 2: ord() - Character to code point
console.log("\nExample 2: ord() - Character to code point");
console.log("ord(\"A\") = " + str(ord("A")));      // 65
console.log("ord(\"a\") = " + str(ord("a")));      // 97
console.log("ord(\"0\") = " + str(ord("0")));      // 48
console.log("ord(\"!\") = " + str(ord("!")));      // 33
console.log("ord(\"€\") = " + str(ord("€")));      // 8364

// Example 3: Creating alphabet
console.log("\nExample 3: Creating alphabet with chr()");
uppercase = "";
for (code in range(65, 91)) {
    uppercase = uppercase + chr(code);
}
console.log("Uppercase: " + uppercase);

lowercase = "";
for (code in range(97, 123)) {
    lowercase = lowercase + chr(code);
}
console.log("Lowercase: " + lowercase);

// Example 4: hex() - Decimal to hexadecimal
console.log("\nExample 4: hex() - Convert to hexadecimal");
console.log("hex(0) = " + hex(0));
console.log("hex(16) = " + hex(16));
console.log("hex(255) = " + hex(255));
console.log("hex(4095) = " + hex(4095));

// Example 5: bin() - Decimal to binary
console.log("\nExample 5: bin() - Convert to binary");
console.log("bin(0) = " + bin(0));
console.log("bin(1) = " + bin(1));
console.log("bin(10) = " + bin(10));
console.log("bin(255) = " + bin(255));

// Example 6: oct() - Decimal to octal
console.log("\nExample 6: oct() - Convert to octal");
console.log("oct(0) = " + oct(0));
console.log("oct(8) = " + oct(8));
console.log("oct(64) = " + oct(64));
console.log("oct(512) = " + oct(512));

// Example 7: format() - Format numbers
console.log("\nExample 7: format() - Format values");
pi = 3.14159265359;
console.log("format(pi, \".2f\") = " + format(pi, ".2f"));
console.log("format(pi, \".4f\") = " + format(pi, ".4f"));
console.log("format(42, \"05d\") = " + format(42, "05d"));
console.log("format(255, \"x\") = " + format(255, "x"));

// Example 8: Character code analysis
console.log("\nExample 8: Character code analysis");
text = "Hello";
console.log("Analyzing: \"" + text + "\"");

i = 0;
while (i < len(text)) {
    char = text[i];
    code = ord(char);
    console.log("  '" + char + "' -> " + str(code));
    i = i + 1;
}

// Example 9: Number base conversions
console.log("\nExample 9: Number base conversions");
numbers = [8, 16, 32, 64, 128, 256];

console.log("Number conversions:");
for (num in numbers) {
    console.log(str(num) + ":");
    console.log("  Binary:  " + bin(num));
    console.log("  Octal:   " + oct(num));
    console.log("  Hex:     " + hex(num));
}

// Example 10: Caesar cipher
console.log("\nExample 10: Caesar cipher (shift by 3)");
function caesarEncode(text, shift) {
    result = "";
    i = 0;
    while (i < len(text)) {
        char = text[i];
        code = ord(char);

        // Only shift letters
        if (code >= 65 && code <= 90) {
            // Uppercase
            newCode = ((code - 65 + shift) % 26) + 65;
            result = result + chr(newCode);
        } elif (code >= 97 && code <= 122) {
            // Lowercase
            newCode = ((code - 97 + shift) % 26) + 97;
            result = result + chr(newCode);
        } else {
            result = result + char;
        }

        i = i + 1;
    }
    return result;
}

original = "Hello World";
encoded = caesarEncode(original, 3);
console.log("Original: \"" + original + "\"");
console.log("Encoded:  \"" + encoded + "\"");

// Example 11: Price formatting
console.log("\nExample 11: Price formatting");
prices = [9.99, 1299.50, 45.0, 0.99, 10000.00];

console.log("Formatted prices:");
for (price in prices) {
    formatted = "$" + format(price, ".2f");
    console.log("  " + formatted);
}

// Example 12: Hexadecimal color codes
console.log("\nExample 12: RGB to hex color");
function rgbToHex(r, g, b) {
    // Remove "0x" prefix and pad with zeros if needed
    rHex = hex(r)[2:];
    gHex = hex(g)[2:];
    bHex = hex(b)[2:];

    // Pad to 2 digits
    if (len(rHex) == 1) {
        rHex = "0" + rHex;
    }
    if (len(gHex) == 1) {
        gHex = "0" + gHex;
    }
    if (len(bHex) == 1) {
        bHex = "0" + bHex;
    }

    return "#" + rHex + gHex + bHex;
}

colors = [
    {name: "Red", r: 255, g: 0, b: 0},
    {name: "Green", r: 0, g: 255, b: 0},
    {name: "Blue", r: 0, g: 0, b: 255},
    {name: "Yellow", r: 255, g: 255, b: 0}
];

console.log("Color codes:");
for (color in colors) {
    hexCode = rgbToHex(color.r, color.g, color.b);
    console.log("  " + color.name + ": " + hexCode);
}

// Example 13: Binary representation
console.log("\nExample 13: Binary number patterns");
numbers = [1, 2, 4, 8, 16, 32];
console.log("Powers of 2 in binary:");
for (num in numbers) {
    console.log("  " + str(num) + " = " + bin(num));
}

// Example 14: Formatted reports
console.log("\nExample 14: Formatted numeric reports");
data = [
    {name: "Revenue", value: 125000.50},
    {name: "Expenses", value: 87500.25},
    {name: "Profit", value: 37500.25}
];

console.log("=== Financial Report ===");
for (item in data) {
    formatted = format(item.value, ",.2f");
    console.log(item.name + ": $" + formatted);
}

// Example 15: Character range checks
console.log("\nExample 15: Character classification");
function classifyChar(char) {
    code = ord(char);

    if (code >= 48 && code <= 57) {
        return "digit";
    } elif (code >= 65 && code <= 90) {
        return "uppercase";
    } elif (code >= 97 && code <= 122) {
        return "lowercase";
    } elif (code == 32) {
        return "space";
    } else {
        return "special";
    }
}

testChars = "Aa5 !";
console.log("Classifying: \"" + testChars + "\"");
i = 0;
while (i < len(testChars)) {
    char = testChars[i];
    classification = classifyChar(char);
    console.log("  '" + char + "' (" + str(ord(char)) + ") -> " + classification);
    i = i + 1;
}

console.log("\n=== String Conversions Complete ===");
