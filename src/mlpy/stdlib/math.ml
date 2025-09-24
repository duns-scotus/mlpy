// @description: Mathematical operations and constants with capability-based security
// @capability: read:math_constants
// @capability: execute:calculations
// @version: 1.0.0

/**
 * ML Math Standard Library
 * Provides mathematical operations with security validation
 */

capability MathOperations {
    allow read "math_constants";
    allow execute "calculations";
}

// Mathematical constants
pi = 3.141592653589793;
e = 2.718281828459045;
tau = 6.283185307179586;

// Basic mathematical functions
function abs(x) {
    if (x < 0) {
        return -x;
    } else {
        return x;
    }
}

function max(a, b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

function min(a, b) {
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

function pow(base, exponent) {
    // Simple power implementation for positive integer exponents
    if (exponent == 0) {
        return 1;
    }

    result = 1;
    i = 0;
    while (i < exponent) {
        result = result * base;
        i = i + 1;
    }

    return result;
}

function sqrt(x) {
    // Newton's method for square root
    if (x < 0) {
        return -1; // Error case
    }

    if (x == 0) {
        return 0;
    }

    guess = x / 2;
    i = 0;

    while (i < 10) { // 10 iterations should be enough for reasonable precision
        better_guess = (guess + x / guess) / 2;
        if (abs(better_guess - guess) < 1e-10) {
            break;
        }
        guess = better_guess;
        i = i + 1;
    }

    return guess;
}

function factorial(n) {
    if (n <= 1) {
        return 1;
    }

    result = 1;
    i = 2;
    while (i <= n) {
        result = result * i;
        i = i + 1;
    }

    return result;
}

function gcd(a, b) {
    // Greatest common divisor using Euclidean algorithm
    while (b != 0) {
        temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// Trigonometric functions (simplified approximations)
function sin_approx(x) {
    // Taylor series approximation: sin(x) ≈ x - x³/6 + x⁵/120
    x2 = x * x;
    x3 = x * x2;
    x5 = x3 * x2;

    return x - x3/6 + x5/120;
}

function cos_approx(x) {
    // Taylor series approximation: cos(x) ≈ 1 - x²/2 + x⁴/24
    x2 = x * x;
    x4 = x2 * x2;

    return 1 - x2/2 + x4/24;
}