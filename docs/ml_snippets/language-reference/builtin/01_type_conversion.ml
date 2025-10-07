// ============================================
// Example: Type Conversion Functions
// Category: language-reference/builtin
// Demonstrates: int(), float(), str(), bool()
// ============================================

import console;

console.log("=== Type Conversion Functions ===\n");

// Example 1: int() - Convert to integer
console.log("Example 1: int() - Convert to integer");
console.log("int(3.14) = " + str(int(3.14)));          // 3
console.log("int(\"42\") = " + str(int("42")));        // 42
console.log("int(\"3.9\") = " + str(int("3.9")));      // 3
console.log("int(true) = " + str(int(true)));          // 1
console.log("int(false) = " + str(int(false)));        // 0
console.log("int(\"invalid\") = " + str(int("invalid")));  // 0 (error returns 0)

// Example 2: float() - Convert to floating-point
console.log("\nExample 2: float() - Convert to float");
console.log("float(42) = " + str(float(42)));          // 42.0
console.log("float(\"3.14\") = " + str(float("3.14")));  // 3.14
console.log("float(true) = " + str(float(true)));      // 1.0
console.log("float(false) = " + str(float(false)));    // 0.0
console.log("float(\"bad\") = " + str(float("bad")));  // 0.0 (error returns 0.0)

// Example 3: str() - Convert to string
console.log("\nExample 3: str() - Convert to string");
console.log("str(42) = \"" + str(42) + "\"");
console.log("str(3.14) = \"" + str(3.14) + "\"");
console.log("str(true) = \"" + str(true) + "\"");    // "true" (lowercase)
console.log("str(false) = \"" + str(false) + "\"");  // "false" (lowercase)
console.log("str([1, 2, 3]) = \"" + str([1, 2, 3]) + "\"");

// Example 4: bool() - Convert to boolean
console.log("\nExample 4: bool() - Convert to boolean");
console.log("bool(1) = " + str(bool(1)));          // true
console.log("bool(0) = " + str(bool(0)));          // false
console.log("bool(\"\") = " + str(bool("")));      // false
console.log("bool(\"hello\") = " + str(bool("hello")));  // true
console.log("bool([]) = " + str(bool([])));        // false
console.log("bool([1]) = " + str(bool([1])));      // true

// Example 5: Practical use - User input processing
console.log("\nExample 5: Practical type conversion");
userInput = "25";
userAge = int(userInput);
console.log("Input string: \"" + userInput + "\"");
console.log("Converted to int: " + str(userAge));
console.log("Can drink alcohol: " + str(userAge >= 21));

// Example 6: Temperature converter
console.log("\nExample 6: Temperature converter");
function celsiusToFahrenheit(celsius) {
    fahrenheit = (celsius * 9.0 / 5.0) + 32.0;
    return fahrenheit;
}

tempStrings = ["0", "25", "100"];
for (tempStr in tempStrings) {
    celsius = float(tempStr);
    fahrenheit = celsiusToFahrenheit(celsius);
    console.log(str(celsius) + "°C = " + str(fahrenheit) + "°F");
}

// Example 7: Chaining conversions
console.log("\nExample 7: Chaining conversions");
value = "3.14159";
console.log("Original string: \"" + value + "\"");

asFloat = float(value);
console.log("As float: " + str(asFloat));

asInt = int(asFloat);
console.log("Float to int: " + str(asInt));

backToString = str(asInt);
console.log("Back to string: \"" + backToString + "\"");

asBool = bool(asInt);
console.log("As boolean: " + str(asBool));

// Example 8: Handling conversion errors gracefully
console.log("\nExample 8: Safe conversion with error handling");
inputs = ["123", "45.67", "invalid", "", "true"];

for (input in inputs) {
    intValue = int(input);
    floatValue = float(input);

    console.log("Input: \"" + input + "\"");
    console.log("  As int: " + str(intValue));
    console.log("  As float: " + str(floatValue));
}

console.log("\n=== Type Conversion Complete ===");
