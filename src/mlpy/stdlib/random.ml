// @description: Random number generation for ML standard library
// @version: 1.0.0

/**
 * ML Random Number Standard Library
 * Provides pseudo-random number generation using Linear Congruential Generator (LCG)
 */

// Global random state
random_seed = 12345;

// Linear Congruential Generator constants (from Numerical Recipes)
lcg_a = 1664525;
lcg_c = 1013904223;
lcg_m = 4294967296; // 2^32

// Set the random seed
function setSeed(seed) {
    random_seed = seed;
    return seed;
}

// Get current seed
function getSeed() {
    return random_seed;
}

// Generate next random integer
function nextInt() {
    random_seed = (lcg_a * random_seed + lcg_c) % lcg_m;
    return random_seed;
}

// Generate random float between 0 and 1
function random() {
    return nextInt() / lcg_m;
}

// Generate random float between min and max
function randomFloat(min, max) {
    if (min == null) {
        min = 0;
    }
    if (max == null) {
        max = 1;
    }
    return min + random() * (max - min);
}

// Generate random integer between min (inclusive) and max (exclusive)
function randomInt(min, max) {
    if (min == null) {
        min = 0;
    }
    if (max == null) {
        max = 100;
    }

    range = max - min;
    return min + (nextInt() % range);
}

// Generate random boolean
function randomBool() {
    return random() < 0.5;
}

// Generate random boolean with given probability of true
function randomBoolWeighted(probability) {
    return random() < probability;
}

// Choose random element from array
function choice(list) {
    if (list == null || length(list) == 0) {
        return null;
    }

    index = randomInt(0, length(list));
    return list[index];
}

// Shuffle array (Fisher-Yates algorithm)
function shuffle(list) {
    len = length(list);
    shuffled = [];

    // Copy original list
    i = 0;
    while (i < len) {
        shuffled[i] = list[i];
        i = i + 1;
    }

    // Shuffle in place
    i = len - 1;
    while (i > 0) {
        j = randomInt(0, i + 1);

        // Swap elements
        temp = shuffled[i];
        shuffled[i] = shuffled[j];
        shuffled[j] = temp;

        i = i - 1;
    }

    return shuffled;
}

// Generate random sample of n elements from list
function sample(list, n) {
    len = length(list);

    if (n >= len) {
        return shuffle(list);
    }

    shuffled = shuffle(list);
    result = [];

    i = 0;
    while (i < n) {
        result[i] = shuffled[i];
        i = i + 1;
    }

    return result;
}

// Generate random number from normal distribution (Box-Muller transform)
has_spare_normal = false;
spare_normal = 0;

function randomNormal(mean, stddev) {
    if (mean == null) {
        mean = 0;
    }
    if (stddev == null) {
        stddev = 1;
    }

    if (has_spare_normal) {
        has_spare_normal = false;
        return spare_normal * stddev + mean;
    }

    has_spare_normal = true;

    u = random();
    v = random();

    mag = stddev * sqrt(-2 * ln(u));
    spare_normal = mag * cos(2 * pi * v);

    return mag * sin(2 * pi * v) + mean;
}

// Approximation functions needed for normal distribution
function ln(x) {
    // Natural logarithm approximation using series expansion
    if (x <= 0) {
        return -999; // Error case
    }

    if (x == 1) {
        return 0;
    }

    // Use series expansion for ln(1 + y) where x = 1 + y
    y = x - 1;

    if (abs(y) < 0.5) {
        // Taylor series: ln(1+y) = y - y²/2 + y³/3 - y⁴/4 + ...
        y2 = y * y;
        y3 = y2 * y;
        y4 = y3 * y;

        return y - y2/2 + y3/3 - y4/4;
    } else {
        // For larger values, use iterative approach
        result = 0;
        power = x;

        // Simple approximation
        i = 0;
        while (i < 20 && power > 1.1) {
            power = sqrt(power);
            result = result * 2;
            i = i + 1;
        }

        // Use series expansion on reduced value
        y = power - 1;
        y2 = y * y;
        series = y - y2/2 + y*y2/3;

        return (result + series);
    }
}

function sin(x) {
    // Taylor series approximation for sine
    // sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...

    // Reduce angle to [-π, π] range
    while (x > pi) {
        x = x - 2 * pi;
    }
    while (x < -pi) {
        x = x + 2 * pi;
    }

    x2 = x * x;
    x3 = x * x2;
    x5 = x3 * x2;
    x7 = x5 * x2;

    return x - x3/6 + x5/120 - x7/5040;
}

function cos(x) {
    // cos(x) = sin(x + π/2)
    return sin(x + pi/2);
}

// Helper function for square root (from math.ml but simplified)
function sqrt(x) {
    if (x < 0) {
        return 0; // Error case
    }

    if (x == 0) {
        return 0;
    }

    guess = x / 2;
    i = 0;

    while (i < 10) {
        better_guess = (guess + x / guess) / 2;
        if (abs(better_guess - guess) < 1e-10) {
            return better_guess;
        }
        guess = better_guess;
        i = i + 1;
    }

    return guess;
}

function abs(x) {
    if (x < 0) {
        return -x;
    }
    return x;
}

// Helper to get length of array (would be from collections.ml)
function length(list) {
    count = 0;
    i = 0;
    while (i >= 0) {
        if (list[i] != null) {
            count = count + 1;
            i = i + 1;
        } else {
            return count;
        }
    }
    return count;
}

// Constants
pi = 3.141592653589793;