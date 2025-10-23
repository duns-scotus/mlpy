// ============================================
// Example: Trigonometric Functions
// Category: standard-library/math
// Demonstrates: sin, cos, tan, asin, acos, atan, atan2
// ============================================

import console;
import math;

console.log("=== Trigonometric Functions ===\n");

// Example 1: Constants
console.log("Example 1: Math constants");
console.log("pi = " + str(math.pi));  // ~3.14159
console.log("e = " + str(math.e));    // ~2.71828

// Example 2: sin(), cos(), tan() with pi
console.log("\nExample 2: Basic trig functions");
console.log("sin(0) = " + str(math.sin(0)));            // 0
console.log("sin(pi/2) = " + str(math.sin(math.pi / 2)));  // 1
console.log("cos(0) = " + str(math.cos(0)));            // 1
console.log("cos(pi) = " + str(math.sin(math.pi)));          // ~0
console.log("tan(0) = " + str(math.tan(0)));            // 0

// Example 3: Angle conversion - degrees to radians
console.log("\nExample 3: Angle conversion");
degrees45 = 45;
radians45 = math.degToRad(degrees45);
console.log("45 degrees = " + str(radians45) + " radians");

degrees90 = 90;
radians90 = math.degToRad(degrees90);
console.log("90 degrees = " + str(radians90) + " radians");

degrees180 = 180;
radians180 = math.degToRad(degrees180);
console.log("180 degrees = " + str(radians180) + " radians");

// Example 4: Angle conversion - radians to degrees
console.log("\nExample 4: Radians to degrees");
console.log("pi radians = " + str(math.radToDeg(math.pi)) + " degrees");      // 180
console.log("pi/2 radians = " + str(math.radToDeg(math.pi / 2)) + " degrees");  // 90
console.log("2*pi radians = " + str(math.radToDeg(2 * math.pi)) + " degrees");  // 360

// Example 5: Trigonometry with degree input
console.log("\nExample 5: Trig functions with degrees");
angle = 30;  // degrees
angleRad = math.degToRad(angle);
console.log("sin(30 degrees) = " + str(math.sin(angleRad)));  // 0.5
console.log("cos(30 degrees) = " + str(math.cos(angleRad)));  // ~0.866

angle = 45;
angleRad = math.degToRad(angle);
console.log("sin(45 degrees) = " + str(math.sin(angleRad)));  // ~0.707
console.log("cos(45 degrees) = " + str(math.cos(angleRad)));  // ~0.707

// Example 6: Inverse trig functions
console.log("\nExample 6: Inverse trig functions");
console.log("asin(0.5) = " + str(math.asin(0.5)));      // ~0.524 radians
console.log("acos(0.5) = " + str(math.acos(0.5)));      // ~1.047 radians
console.log("atan(1) = " + str(math.atan(1)));          // ~0.785 radians (pi/4)

// Convert results to degrees
arcsinDeg = math.radToDeg(math.asin(0.5));
console.log("asin(0.5) in degrees = " + str(arcsinDeg));  // 30 degrees

// Example 7: atan2() for angle between two points
console.log("\nExample 7: atan2() for point angles");

function angleBetweenPoints(x, y) {
    angleRad = math.atan2(y, x);
    angleDeg = math.radToDeg(angleRad);
    return angleDeg;
}

angle1 = angleBetweenPoints(1, 0);
console.log("Angle to (1, 0): " + str(angle1) + " degrees");  // 0

angle2 = angleBetweenPoints(0, 1);
console.log("Angle to (0, 1): " + str(angle2) + " degrees");  // 90

angle3 = angleBetweenPoints(1, 1);
console.log("Angle to (1, 1): " + str(angle3) + " degrees");  // 45

// Example 8: Circle calculations
console.log("\nExample 8: Circle calculations");

function circleCircumference(radius) {
    return 2 * math.pi * radius;
}

function circleArea(radius) {
    return math.pi * radius * radius;
}

r = 5;
console.log("Circle with radius " + str(r) + ":");
console.log("  Circumference: " + str(circleCircumference(r)));
console.log("  Area: " + str(circleArea(r)));

// Example 9: Wave calculation
console.log("\nExample 9: Sine wave values");
console.log("Sine wave at different angles:");

angles = [0, 30, 60, 90, 120, 150, 180];
for (deg in angles) {
    rad = math.degToRad(deg);
    sineValue = math.sin(rad);
    console.log("  " + str(deg) + " degrees: " + str(round(sineValue, 3)));
}

console.log("\n=== Trigonometry Complete ===");
