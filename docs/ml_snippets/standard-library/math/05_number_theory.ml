// ============================================
// Example: Number Theory Functions
// Category: standard-library/math
// Demonstrates: factorial, gcd, lcm
// ============================================

import console;
import math;

console.log("=== Number Theory Functions ===\n");

// Example 1: factorial() - Factorial calculation
console.log("Example 1: math.factorial() - n!");
console.log("factorial(0) = " + str(math.factorial(0)));    // 1
console.log("factorial(1) = " + str(math.factorial(1)));    // 1
console.log("factorial(5) = " + str(math.factorial(5)));    // 120
console.log("factorial(7) = " + str(math.factorial(7)));    // 5040
console.log("factorial(10) = " + str(math.factorial(10)));  // 3628800

// Example 2: gcd() - Greatest Common Divisor
console.log("\nExample 2: math.gcd() - Greatest Common Divisor");
console.log("gcd(12, 18) = " + str(math.gcd(12, 18)));      // 6
console.log("gcd(24, 36) = " + str(math.gcd(24, 36)));      // 12
console.log("gcd(17, 19) = " + str(math.gcd(17, 19)));      // 1 (coprime)
console.log("gcd(100, 50) = " + str(math.gcd(100, 50)));    // 50
console.log("gcd(48, 180) = " + str(math.gcd(48, 180)));    // 12

// Example 3: lcm() - Least Common Multiple
console.log("\nExample 3: math.lcm() - Least Common Multiple");
console.log("lcm(4, 6) = " + str(math.lcm(4, 6)));          // 12
console.log("lcm(12, 18) = " + str(math.lcm(12, 18)));      // 36
console.log("lcm(5, 7) = " + str(math.lcm(5, 7)));          // 35 (coprime)
console.log("lcm(10, 15) = " + str(math.lcm(10, 15)));      // 30
console.log("lcm(21, 6) = " + str(math.lcm(21, 6)));        // 42

// Example 4: Permutations using factorial
console.log("\nExample 4: Permutations calculation");

function permutations(n, r) {
    // P(n,r) = n! / (n-r)!
    return math.factorial(n) / math.factorial(n - r);
}

n = 5;
r = 3;
perms = permutations(n, r);
console.log("P(" + str(n) + "," + str(r) + ") = " + str(perms));  // 60

n = 10;
r = 2;
perms = permutations(n, r);
console.log("P(" + str(n) + "," + str(r) + ") = " + str(perms));  // 90

// Example 5: Combinations using factorial
console.log("\nExample 5: Combinations calculation");

function combinations(n, r) {
    // C(n,r) = n! / (r! * (n-r)!)
    return math.factorial(n) / (math.factorial(r) * math.factorial(n - r));
}

n = 5;
r = 2;
combs = combinations(n, r);
console.log("C(" + str(n) + "," + str(r) + ") = " + str(combs));  // 10

n = 10;
r = 3;
combs = combinations(n, r);
console.log("C(" + str(n) + "," + str(r) + ") = " + str(combs));  // 120

// Example 6: Simplifying fractions with gcd
console.log("\nExample 6: Simplifying fractions");

function simplifyFraction(numerator, denominator) {
    divisor = math.gcd(numerator, denominator);
    return {
        numerator: numerator / divisor,
        denominator: denominator / divisor
    };
}

fractions = [
    {num: 12, den: 18},
    {num: 48, den: 64},
    {num: 100, den: 150},
    {num: 17, den: 51}
];

console.log("Simplifying fractions:");
for (frac in fractions) {
    simplified = simplifyFraction(frac.num, frac.den);
    console.log("  " + str(frac.num) + "/" + str(frac.den) + " = " +
                str(simplified.numerator) + "/" + str(simplified.denominator));
}

// Example 7: Finding LCM of multiple numbers
console.log("\nExample 7: LCM of multiple numbers");

function lcmMultiple(numbers) {
    if (len(numbers) == 0) {
        return 0;
    }

    result = numbers[0];
    i = 1;
    while (i < len(numbers)) {
        result = math.lcm(result, numbers[i]);
        i = i + 1;
    }
    return result;
}

numbers = [4, 6, 8, 12];
result = lcmMultiple(numbers);
console.log("LCM of " + str(numbers) + " = " + str(result));  // 24

numbers = [3, 5, 7];
result = lcmMultiple(numbers);
console.log("LCM of " + str(numbers) + " = " + str(result));  // 105

// Example 8: Finding GCD of multiple numbers
console.log("\nExample 8: GCD of multiple numbers");

function gcdMultiple(numbers) {
    if (len(numbers) == 0) {
        return 0;
    }

    result = numbers[0];
    i = 1;
    while (i < len(numbers)) {
        result = math.gcd(result, numbers[i]);
        i = i + 1;
    }
    return result;
}

numbers = [12, 18, 24, 30];
result = gcdMultiple(numbers);
console.log("GCD of " + str(numbers) + " = " + str(result));  // 6

numbers = [100, 150, 200];
result = gcdMultiple(numbers);
console.log("GCD of " + str(numbers) + " = " + str(result));  // 50

// Example 9: Checking if numbers are coprime
console.log("\nExample 9: Checking coprime numbers");

function areCoprime(a, b) {
    return math.gcd(a, b) == 1;
}

pairs = [
    {a: 15, b: 28},
    {a: 12, b: 18},
    {a: 17, b: 19},
    {a: 20, b: 25}
];

console.log("Checking coprime pairs:");
for (pair in pairs) {
    coprime = areCoprime(pair.a, pair.b);
    status = "coprime";
    if (!coprime) {
        status = "not coprime";
    }
    console.log("  " + str(pair.a) + " and " + str(pair.b) + ": " + status);
}

// Example 10: Factorial growth demonstration
console.log("\nExample 10: Factorial growth");

console.log("Factorial values:");
i = 0;
while (i <= 12) {
    fact = math.factorial(i);
    console.log("  " + str(i) + "! = " + str(fact));
    i = i + 1;
}

console.log("\n=== Number Theory Complete ===");
