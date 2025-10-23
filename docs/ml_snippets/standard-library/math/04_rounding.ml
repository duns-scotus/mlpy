// ============================================
// Example: Rounding Functions
// Category: standard-library/math
// Demonstrates: floor, ceil, round, sign
// ============================================

import console;
import math;

console.log("=== Rounding Functions ===\n");

// Example 1: floor() - Round down
console.log("Example 1: math.floor() - Round down");
console.log("floor(3.2) = " + str(math.floor(3.2)));      // 3
console.log("floor(3.7) = " + str(math.floor(3.7)));      // 3
console.log("floor(3.9) = " + str(math.floor(3.9)));      // 3
console.log("floor(-2.3) = " + str(math.floor(-2.3)));    // -3
console.log("floor(-2.7) = " + str(math.floor(-2.7)));    // -3

// Example 2: ceil() - Round up
console.log("\nExample 2: math.ceil() - Round up");
console.log("ceil(3.2) = " + str(math.ceil(3.2)));        // 4
console.log("ceil(3.7) = " + str(math.ceil(3.7)));        // 4
console.log("ceil(3.1) = " + str(math.ceil(3.1)));        // 4
console.log("ceil(-2.3) = " + str(math.ceil(-2.3)));      // -2
console.log("ceil(-2.7) = " + str(math.ceil(-2.7)));      // -2

// Example 3: round() - Round to nearest integer
console.log("\nExample 3: math.round() - Round to nearest");
console.log("round(3.2) = " + str(math.round(3.2)));      // 3
console.log("round(3.7) = " + str(math.round(3.7)));      // 4
console.log("round(3.5) = " + str(math.round(3.5)));      // 4
console.log("round(-2.3) = " + str(math.round(-2.3)));    // -2
console.log("round(-2.7) = " + str(math.round(-2.7)));    // -3

// Example 4: sign() - Get sign of number
console.log("\nExample 4: math.sign() - Get sign");
console.log("sign(5) = " + str(math.sign(5)));            // 1
console.log("sign(-5) = " + str(math.sign(-5)));          // -1
console.log("sign(0) = " + str(math.sign(0)));            // 0
console.log("sign(3.14) = " + str(math.sign(3.14)));      // 1
console.log("sign(-2.71) = " + str(math.sign(-2.71)));    // -1

// Example 5: Comparing rounding methods
console.log("\nExample 5: Comparing rounding methods");
values = [2.1, 2.5, 2.9, -2.1, -2.5, -2.9];

console.log("Value | Floor | Ceil | Round");
console.log("------+-------+------+------");
for (val in values) {
    flr = math.floor(val);
    cl = math.ceil(val);
    rnd = math.round(val);
    console.log(str(val) + " | " + str(flr) + " | " + str(cl) + " | " + str(rnd));
}

// Example 6: Price rounding
console.log("\nExample 6: Price rounding");
prices = [19.99, 24.50, 31.25, 45.01];

console.log("Original prices and rounded:");
for (price in prices) {
    roundedDown = math.floor(price);
    roundedUp = math.ceil(price);
    roundedNearest = math.round(price);

    console.log("$" + str(price));
    console.log("  Floor: $" + str(roundedDown));
    console.log("  Ceil: $" + str(roundedUp));
    console.log("  Round: $" + str(roundedNearest));
}

// Example 7: Calculate pages needed
console.log("\nExample 7: Calculate pages needed");

function pagesNeeded(items, itemsPerPage) {
    return math.ceil(items / itemsPerPage);
}

totalItems = 47;
itemsPerPage = 10;
pages = pagesNeeded(totalItems, itemsPerPage);

console.log("Total items: " + str(totalItems));
console.log("Items per page: " + str(itemsPerPage));
console.log("Pages needed: " + str(pages));  // 5

// Example 8: Integer division with floor
console.log("\nExample 8: Integer division");
dividends = [17, 18, 19, 20, 21];
divisor = 4;

console.log("Integer division by " + str(divisor) + ":");
for (dividend in dividends) {
    quotient = math.floor(dividend / divisor);
    remainder = dividend % divisor;
    console.log(str(dividend) + " / " + str(divisor) + " = " + str(quotient) + " remainder " + str(remainder));
}

// Example 9: Sign-based logic
console.log("\nExample 9: Sign-based comparisons");

function describe(value) {
    s = math.sign(value);

    if (s == 1) {
        return "positive";
    } elif (s == -1) {
        return "negative";
    } else {
        return "zero";
    }
}

testValues = [10, -5, 0, 3.14, -2.71];
console.log("Value descriptions:");
for (val in testValues) {
    desc = describe(val);
    console.log("  " + str(val) + " is " + desc);
}

// Example 10: Rounding to decimal places
console.log("\nExample 10: Manual decimal place rounding");

function roundToPlaces(value, places) {
    multiplier = math.pow(10, places);
    return math.round(value * multiplier) / multiplier;
}

pi = math.pi;
console.log("Pi rounded to different decimal places:");
console.log("  0 places: " + str(roundToPlaces(pi, 0)));  // 3
console.log("  1 place: " + str(roundToPlaces(pi, 1)));   // 3.1
console.log("  2 places: " + str(roundToPlaces(pi, 2)));  // 3.14
console.log("  3 places: " + str(roundToPlaces(pi, 3)));  // 3.142
console.log("  4 places: " + str(roundToPlaces(pi, 4)));  // 3.1416

console.log("\n=== Rounding Complete ===");
