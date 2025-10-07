// ============================================
// Example: Type Conversion
// Category: standard-library/builtin
// Demonstrates: int(), float(), str(), bool()
// ============================================

print("=== Type Conversion ===\n");

// Converting to integers
print("Converting to integers:");
print("  int(3.14) = " + str(int(3.14)));          // 3
print("  int(\"42\") = " + str(int("42")));         // 42
print("  int(\"3.99\") = " + str(int("3.99")));     // 3 (float parsing!)
print("  int(true) = " + str(int(true)));           // 1
print("  int(false) = " + str(int(false)));         // 0

// Converting to floats
print("\nConverting to floats:");
print("  float(42) = " + str(float(42)));           // 42.0
print("  float(\"3.14\") = " + str(float("3.14"))); // 3.14
print("  float(true) = " + str(float(true)));       // 1.0
print("  float(false) = " + str(float(false)));     // 0.0

// Converting to strings
print("\nConverting to strings:");
print("  str(42) = \"" + str(42) + "\"");
print("  str(3.14) = \"" + str(3.14) + "\"");
print("  str(true) = \"" + str(true) + "\"");      // "true" (lowercase!)
print("  str(false) = \"" + str(false) + "\"");    // "false" (lowercase!)

// Converting to booleans
print("\nConverting to booleans:");
print("  bool(1) = " + str(bool(1)));               // true
print("  bool(0) = " + str(bool(0)));               // false
print("  bool(\"\") = " + str(bool("")));           // false (empty string)
print("  bool(\"hello\") = " + str(bool("hello"))); // true
print("  bool([]) = " + str(bool([])));             // false (empty array)
print("  bool([1,2,3]) = " + str(bool([1,2,3])));   // true

// Practical example: User input processing
print("\n=== Practical Example: Processing User Input ===");

// Simulate user input (in real programs, use input())
userAge = "25";
userHeight = "5.9";
userName = "Alice";

// Convert and validate
age = int(userAge);
height = float(userHeight);

print("User: " + userName);
print("Age: " + str(age) + " years");
print("Height: " + str(height) + " feet");
print("Is adult: " + str(age >= 18));

// Safe conversion with error handling
print("\n=== Safe Conversion ===");
invalidNumber = "not-a-number";
result = int(invalidNumber);  // Returns 0 on error
print("int(\"not-a-number\") = " + str(result));  // 0

// Type conversion in calculations
print("\n=== Conversion in Calculations ===");
stringNumber = "10";
intResult = int(stringNumber) * 2;
print("int(\"10\") * 2 = " + str(intResult));

floatNumber = "3.5";
floatResult = float(floatNumber) + 1.5;
print("float(\"3.5\") + 1.5 = " + str(floatResult));

print("\n=== Type Conversion Complete ===");
