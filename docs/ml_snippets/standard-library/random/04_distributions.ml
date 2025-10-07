// ============================================
// Example: Statistical Distributions
// Category: standard-library/random
// Demonstrates: randomNormal, gaussian, uniform, triangular
// ============================================

import console;
import random;
import math;

console.log("=== Statistical Distributions ===\n");

// ============================================
// Uniform Distribution
// ============================================

console.log("=== Uniform Distribution ===");

console.log("uniform(0, 10) - 10 samples:");
i = 0;
while (i < 10) {
    value = random.uniform(0, 10);
    console.log("  " + str(round(value, 2)));
    i = i + 1;
}

// Verify uniform spread
console.log("\nUniform distribution analysis (1000 samples, 0-10):");
bucket0 = 0;
bucket1 = 0;
bucket2 = 0;
bucket3 = 0;
bucket4 = 0;

i = 0;
while (i < 1000) {
    value = random.uniform(0, 10);

    if (value >= 0 && value < 2) {
        bucket0 = bucket0 + 1;
    } elif (value >= 2 && value < 4) {
        bucket1 = bucket1 + 1;
    } elif (value >= 4 && value < 6) {
        bucket2 = bucket2 + 1;
    } elif (value >= 6 && value < 8) {
        bucket3 = bucket3 + 1;
    } else {
        bucket4 = bucket4 + 1;
    }
    i = i + 1;
}

console.log("  0-2:   " + str(bucket0) + " samples");
console.log("  2-4:   " + str(bucket1) + " samples");
console.log("  4-6:   " + str(bucket2) + " samples");
console.log("  6-8:   " + str(bucket3) + " samples");
console.log("  8-10:  " + str(bucket4) + " samples");

// ============================================
// Normal (Gaussian) Distribution
// ============================================

console.log("\n=== Normal Distribution ===");

// Standard normal (mean=0, stddev=1)
console.log("Standard normal (mean=0, stddev=1) - 10 samples:");
i = 0;
while (i < 10) {
    value = random.randomNormal(0, 1);
    console.log("  " + str(round(value, 2)));
    i = i + 1;
}

// Custom mean and standard deviation
console.log("\nNormal(mean=100, stddev=15) - IQ scores simulation:");
i = 0;
while (i < 10) {
    iq = random.randomNormal(100, 15);
    console.log("  IQ: " + str(round(iq, 0)));
    i = i + 1;
}

// Analyze distribution
console.log("\nNormal distribution analysis (1000 samples, mean=50, stddev=10):");
samples = [];
i = 0;
while (i < 1000) {
    value = random.randomNormal(50, 10);
    samples = samples + [value];
    i = i + 1;
}

// Calculate mean
sum = 0;
i = 0;
while (i < len(samples)) {
    sum = sum + samples[i];
    i = i + 1;
}
mean = sum / len(samples);

// Calculate standard deviation
sumSquaredDiff = 0;
i = 0;
while (i < len(samples)) {
    diff = samples[i] - mean;
    sumSquaredDiff = sumSquaredDiff + (diff * diff);
    i = i + 1;
}
variance = sumSquaredDiff / len(samples);
stddev = math.sqrt(variance);

console.log("  Sample mean: " + str(round(mean, 2)) + " (expected: 50)");
console.log("  Sample stddev: " + str(round(stddev, 2)) + " (expected: 10)");

// ============================================
// Gaussian (Alias for Normal)
// ============================================

console.log("\n=== Gaussian Distribution (alias) ===");

console.log("Gaussian(mean=0, stddev=1) - 5 samples:");
i = 0;
while (i < 5) {
    value = random.gaussian(0, 1);
    console.log("  " + str(round(value, 3)));
    i = i + 1;
}

// ============================================
// Triangular Distribution
// ============================================

console.log("\n=== Triangular Distribution ===");

// Triangular with specified mode
console.log("Triangular(low=0, high=10, mode=7) - 10 samples:");
i = 0;
while (i < 10) {
    value = random.triangular(0, 10, 7);
    console.log("  " + str(round(value, 2)));
    i = i + 1;
}

// Triangular with default mode (midpoint)
console.log("\nTriangular(low=0, high=100, mode=auto) - 10 samples:");
i = 0;
while (i < 10) {
    value = random.triangular(0, 100, null);
    console.log("  " + str(round(value, 1)));
    i = i + 1;
}

// ============================================
// Practical Example: Test Score Simulation
// ============================================

console.log("\n=== Practical: Test Score Simulation ===");

console.log("Simulating test scores for 30 students (normal distribution):");
console.log("Mean: 75, Standard Deviation: 10");

scores = [];
i = 0;
while (i < 30) {
    score = random.randomNormal(75, 10);

    // Clamp between 0-100
    if (score < 0) {
        score = 0;
    }
    if (score > 100) {
        score = 100;
    }

    scores = scores + [score];
    i = i + 1;
}

// Grade distribution
gradeA = 0;  // >= 90
gradeB = 0;  // 80-89
gradeC = 0;  // 70-79
gradeD = 0;  // 60-69
gradeF = 0;  // < 60

i = 0;
while (i < len(scores)) {
    score = scores[i];
    if (score >= 90) {
        gradeA = gradeA + 1;
    } elif (score >= 80) {
        gradeB = gradeB + 1;
    } elif (score >= 70) {
        gradeC = gradeC + 1;
    } elif (score >= 60) {
        gradeD = gradeD + 1;
    } else {
        gradeF = gradeF + 1;
    }
    i = i + 1;
}

console.log("\nGrade Distribution:");
console.log("  A (90-100): " + str(gradeA) + " students");
console.log("  B (80-89):  " + str(gradeB) + " students");
console.log("  C (70-79):  " + str(gradeC) + " students");
console.log("  D (60-69):  " + str(gradeD) + " students");
console.log("  F (<60):    " + str(gradeF) + " students");

// ============================================
// Practical Example: Response Time Simulation
// ============================================

console.log("\n=== Practical: Response Time Simulation ===");

console.log("Simulating server response times (triangular distribution):");
console.log("Most responses around 50ms, range 10-200ms");

responseTimes = [];
i = 0;
while (i < 100) {
    time = random.triangular(10, 200, 50);
    responseTimes = responseTimes + [time];
    i = i + 1;
}

// Analyze response times
fast = 0;     // < 50ms
normal = 0;   // 50-100ms
slow = 0;     // 100-150ms
verySlow = 0; // >= 150ms

i = 0;
while (i < len(responseTimes)) {
    time = responseTimes[i];
    if (time < 50) {
        fast = fast + 1;
    } elif (time < 100) {
        normal = normal + 1;
    } elif (time < 150) {
        slow = slow + 1;
    } else {
        verySlow = verySlow + 1;
    }
    i = i + 1;
}

console.log("\nResponse Time Distribution:");
console.log("  Fast (<50ms):      " + str(fast) + " requests");
console.log("  Normal (50-100ms): " + str(normal) + " requests");
console.log("  Slow (100-150ms):  " + str(slow) + " requests");
console.log("  Very Slow (>=150): " + str(verySlow) + " requests");

// ============================================
// Practical Example: Height Simulation
// ============================================

console.log("\n=== Practical: Population Height Simulation ===");

console.log("Simulating heights (normal distribution):");
console.log("Men: mean=175cm, stddev=7cm");
console.log("Women: mean=162cm, stddev=6cm");

menHeights = [];
womenHeights = [];

i = 0;
while (i < 50) {
    menHeight = random.randomNormal(175, 7);
    womenHeight = random.randomNormal(162, 6);

    menHeights = menHeights + [menHeight];
    womenHeights = womenHeights + [womenHeight];

    i = i + 1;
}

// Calculate averages
menSum = 0;
womenSum = 0;
i = 0;
while (i < len(menHeights)) {
    menSum = menSum + menHeights[i];
    womenSum = womenSum + womenHeights[i];
    i = i + 1;
}

menAvg = menSum / len(menHeights);
womenAvg = womenSum / len(womenHeights);

console.log("\nSimulation Results (50 samples each):");
console.log("  Men average: " + str(round(menAvg, 1)) + "cm");
console.log("  Women average: " + str(round(womenAvg, 1)) + "cm");

// ============================================
// Practical Example: Dice Simulation
// ============================================

console.log("\n=== Practical: Fair vs Loaded Dice ===");

console.log("\nFair dice (uniform distribution 1-6):");
roll1 = 0;
roll2 = 0;
roll3 = 0;
roll4 = 0;
roll5 = 0;
roll6 = 0;

i = 0;
while (i < 60) {
    roll = random.randomInt(1, 7);
    if (roll == 1) {
        roll1 = roll1 + 1;
    } elif (roll == 2) {
        roll2 = roll2 + 1;
    } elif (roll == 3) {
        roll3 = roll3 + 1;
    } elif (roll == 4) {
        roll4 = roll4 + 1;
    } elif (roll == 5) {
        roll5 = roll5 + 1;
    } else {
        roll6 = roll6 + 1;
    }
    i = i + 1;
}

console.log("  1: " + str(roll1) + " times");
console.log("  2: " + str(roll2) + " times");
console.log("  3: " + str(roll3) + " times");
console.log("  4: " + str(roll4) + " times");
console.log("  5: " + str(roll5) + " times");
console.log("  6: " + str(roll6) + " times");

console.log("\nLoaded dice (triangular, favors 5-6):");
loaded1 = 0;
loaded2 = 0;
loaded3 = 0;
loaded4 = 0;
loaded5 = 0;
loaded6 = 0;

i = 0;
while (i < 60) {
    // Triangular distribution skewed toward higher numbers
    value = random.triangular(1, 7, 5.5);
    roll = round(value, 0);
    if (roll < 1) {
        roll = 1;
    }
    if (roll > 6) {
        roll = 6;
    }

    if (roll == 1) {
        loaded1 = loaded1 + 1;
    } elif (roll == 2) {
        loaded2 = loaded2 + 1;
    } elif (roll == 3) {
        loaded3 = loaded3 + 1;
    } elif (roll == 4) {
        loaded4 = loaded4 + 1;
    } elif (roll == 5) {
        loaded5 = loaded5 + 1;
    } else {
        loaded6 = loaded6 + 1;
    }
    i = i + 1;
}

console.log("  1: " + str(loaded1) + " times");
console.log("  2: " + str(loaded2) + " times");
console.log("  3: " + str(loaded3) + " times");
console.log("  4: " + str(loaded4) + " times");
console.log("  5: " + str(loaded5) + " times");
console.log("  6: " + str(loaded6) + " times");

console.log("\n=== Statistical Distributions Complete ===");
