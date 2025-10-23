// ============================================
// Example: Basic Math Operations
// Category: standard-library/math
// Demonstrates: sqrt, abs, min, max, pow
// ============================================

import console;
import math;

console.log("=== Basic Math Operations ===\n");

// Example 1: sqrt() - Square root
console.log("Example 1: math.sqrt() - Square root");
console.log("sqrt(16) = " + str(math.sqrt(16)));      // 4.0
console.log("sqrt(2) = " + str(math.sqrt(2)));        // ~1.414
console.log("sqrt(100) = " + str(math.sqrt(100)));    // 10.0
console.log("sqrt(-1) = " + str(math.sqrt(-1)));      // 0 (error case)

// Example 2: abs() - Absolute value
console.log("\nExample 2: math.abs() - Absolute value");
console.log("abs(-5) = " + str(math.abs(-5)));        // 5
console.log("abs(3.14) = " + str(math.abs(3.14)));    // 3.14
console.log("abs(-2.5) = " + str(math.abs(-2.5)));    // 2.5
console.log("abs(0) = " + str(math.abs(0)));          // 0

// Example 3: min() - Minimum of two values
console.log("\nExample 3: math.min() - Minimum");
console.log("min(10, 5) = " + str(math.min(10, 5)));      // 5
console.log("min(-1, -10) = " + str(math.min(-1, -10)));  // -10
console.log("min(3.14, 2.71) = " + str(math.min(3.14, 2.71)));  // 2.71

// Example 4: max() - Maximum of two values
console.log("\nExample 4: math.max() - Maximum");
console.log("max(10, 5) = " + str(math.max(10, 5)));      // 10
console.log("max(-1, -10) = " + str(math.max(-1, -10)));  // -1
console.log("max(3.14, 2.71) = " + str(math.max(3.14, 2.71)));  // 3.14

// Example 5: pow() - Power function
console.log("\nExample 5: math.pow() - Power");
console.log("pow(2, 3) = " + str(math.pow(2, 3)));      // 8
console.log("pow(5, 2) = " + str(math.pow(5, 2)));      // 25
console.log("pow(2, 0.5) = " + str(math.pow(2, 0.5)));  // ~1.414 (square root)
console.log("pow(10, -1) = " + str(math.pow(10, -1)));  // 0.1

// Example 6: Pythagorean theorem using sqrt and pow
console.log("\nExample 6: Pythagorean theorem");

function distance(x1, y1, x2, y2) {
    dx = x2 - x1;
    dy = y2 - y1;
    return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2));
}

dist = distance(0, 0, 3, 4);
console.log("Distance from (0,0) to (3,4): " + str(dist));  // 5.0

dist = distance(1, 1, 4, 5);
console.log("Distance from (1,1) to (4,5): " + str(dist));  // 5.0

// Example 7: Finding range of values
console.log("\nExample 7: Finding min/max in calculations");
values = [15, 23, 8, 42, 4];

minVal = values[0];
maxVal = values[0];

for (val in values) {
    minVal = math.min(minVal, val);
    maxVal = math.max(maxVal, val);
}

console.log("Values: " + str(values));
console.log("Minimum: " + str(minVal));
console.log("Maximum: " + str(maxVal));
console.log("Range: " + str(maxVal - minVal));

console.log("\n=== Basic Math Complete ===");
