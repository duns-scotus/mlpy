// ============================================
// Example: Comprehensive Math Application
// Category: standard-library/math
// Demonstrates: Real-world mathematical computations
// ============================================

import console;
import math;

console.log("=== Statistical Analysis System ===\n");

// Example 1: Statistical calculations on dataset
console.log("Example 1: Dataset statistics");

dataset = [23.5, 18.2, 45.7, 32.1, 28.9, 37.4, 41.2, 19.8, 52.3, 29.7];

// Calculate mean
function mean(values) {
    sum = 0;
    for (val in values) {
        sum = sum + val;
    }
    return sum / len(values);
}

// Calculate standard deviation
function stdDev(values) {
    avg = mean(values);
    sumSquares = 0;

    for (val in values) {
        diff = val - avg;
        sumSquares = sumSquares + math.pow(diff, 2);
    }

    variance = sumSquares / len(values);
    return math.sqrt(variance);
}

// Find range
function dataRange(values) {
    if (len(values) == 0) {
        return 0;
    }

    minVal = values[0];
    maxVal = values[0];

    for (val in values) {
        minVal = math.min(minVal, val);
        maxVal = math.max(maxVal, val);
    }

    return maxVal - minVal;
}

avgValue = mean(dataset);
stdDevValue = stdDev(dataset);
rangeValue = dataRange(dataset);

console.log("Dataset: " + str(dataset));
console.log("Mean: " + str(math.round(avgValue * 100) / 100));
console.log("Standard Deviation: " + str(math.round(stdDevValue * 100) / 100));
console.log("Range: " + str(rangeValue));

// Example 2: Geometric calculations
console.log("\nExample 2: Geometric shape calculations");

function circleArea(radius) {
    return math.pi * math.pow(radius, 2);
}

function circleCircumference(radius) {
    return 2 * math.pi * radius;
}

function sphereVolume(radius) {
    return (4.0 / 3.0) * math.pi * math.pow(radius, 3);
}

function sphereSurfaceArea(radius) {
    return 4 * math.pi * math.pow(radius, 2);
}

radius = 5.5;
console.log("Circle with radius " + str(radius) + ":");
console.log("  Area: " + str(math.round(circleArea(radius) * 100) / 100));
console.log("  Circumference: " + str(math.round(circleCircumference(radius) * 100) / 100));
console.log("Sphere with radius " + str(radius) + ":");
console.log("  Volume: " + str(math.round(sphereVolume(radius) * 100) / 100));
console.log("  Surface Area: " + str(math.round(sphereSurfaceArea(radius) * 100) / 100));

// Example 3: Financial calculations
console.log("\nExample 3: Financial calculations");

function compoundInterest(principal, rate, time, compoundsPerYear) {
    // A = P(1 + r/n)^(nt)
    ratePerPeriod = rate / compoundsPerYear;
    numPeriods = compoundsPerYear * time;
    return principal * math.pow(1 + ratePerPeriod, numPeriods);
}

function continuousCompounding(principal, rate, time) {
    // A = Pe^(rt)
    return principal * math.exp(rate * time);
}

principal = 10000;
rate = 0.05;  // 5% annual rate
years = 10;

quarterly = compoundInterest(principal, rate, years, 4);
monthly = compoundInterest(principal, rate, years, 12);
daily = compoundInterest(principal, rate, years, 365);
continuous = continuousCompounding(principal, rate, years);

console.log("Initial investment: $" + str(principal));
console.log("Annual rate: " + str(rate * 100) + "%");
console.log("Time period: " + str(years) + " years");
console.log("Final values:");
console.log("  Quarterly compounding: $" + str(math.round(quarterly * 100) / 100));
console.log("  Monthly compounding: $" + str(math.round(monthly * 100) / 100));
console.log("  Daily compounding: $" + str(math.round(daily * 100) / 100));
console.log("  Continuous compounding: $" + str(math.round(continuous * 100) / 100));

// Example 4: Distance and angle calculations
console.log("\nExample 4: Navigation calculations");

function distance2D(x1, y1, x2, y2) {
    dx = x2 - x1;
    dy = y2 - y1;
    return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2));
}

function bearing(x1, y1, x2, y2) {
    dx = x2 - x1;
    dy = y2 - y1;
    angleRad = math.atan2(dy, dx);
    angleDeg = math.radToDeg(angleRad);
    return angleDeg;
}

// Points on a map
pointA = {x: 0, y: 0, name: "Start"};
pointB = {x: 30, y: 40, name: "Checkpoint 1"};
pointC = {x: 80, y: 60, name: "Destination"};

distAB = distance2D(pointA.x, pointA.y, pointB.x, pointB.y);
distBC = distance2D(pointB.x, pointB.y, pointC.x, pointC.y);
totalDist = distAB + distBC;

bearingAB = bearing(pointA.x, pointA.y, pointB.x, pointB.y);
bearingBC = bearing(pointB.x, pointB.y, pointC.x, pointC.y);

console.log("Route planning:");
console.log("  " + pointA.name + " to " + pointB.name + ":");
console.log("    Distance: " + str(math.round(distAB * 10) / 10) + " units");
console.log("    Bearing: " + str(math.round(bearingAB * 10) / 10) + " degrees");
console.log("  " + pointB.name + " to " + pointC.name + ":");
console.log("    Distance: " + str(math.round(distBC * 10) / 10) + " units");
console.log("    Bearing: " + str(math.round(bearingBC * 10) / 10) + " degrees");
console.log("  Total distance: " + str(math.round(totalDist * 10) / 10) + " units");

// Example 5: Scientific calculations
console.log("\nExample 5: Scientific measurements");

function decibels(intensity, reference) {
    // dB = 10 * log10(I / I0)
    return 10 * math.log(intensity / reference, 10);
}

function phValue(hydrogenConcentration) {
    // pH = -log10([H+])
    return -math.log(hydrogenConcentration, 10);
}

function halfLifeRemaining(initialAmount, halfLife, time) {
    // N(t) = N0 * (1/2)^(t/t_half)
    return initialAmount * math.pow(0.5, time / halfLife);
}

// Sound intensity measurements
refIntensity = math.pow(10, -12);  // Reference intensity (threshold of hearing)
soundLevels = [
    {name: "Whisper", intensity: math.pow(10, -10)},
    {name: "Normal conversation", intensity: math.pow(10, -6)},
    {name: "Busy traffic", intensity: 0.001},
    {name: "Rock concert", intensity: 1.0}
];

console.log("Sound levels in decibels:");
for (sound in soundLevels) {
    db = decibels(sound.intensity, refIntensity);
    console.log("  " + sound.name + ": " + str(math.round(db * 10) / 10) + " dB");
}

// pH calculations
console.log("\nAcidity measurements (pH):");
solutions = [
    {name: "Stomach acid", concentration: 0.1},
    {name: "Lemon juice", concentration: 0.01},
    {name: "Coffee", concentration: 0.00001},
    {name: "Pure water", concentration: math.pow(10, -7)}
];

for (sol in solutions) {
    ph = phValue(sol.concentration);
    console.log("  " + sol.name + ": pH " + str(math.round(ph * 10) / 10));
}

// Radioactive decay
console.log("\nRadioactive decay simulation:");
initialAmount = 100;
halfLife = 5.27;  // years
times = [0, 5, 10, 15, 20];

console.log("Initial amount: " + str(initialAmount) + " grams");
console.log("Half-life: " + str(halfLife) + " years");
for (t in times) {
    remaining = halfLifeRemaining(initialAmount, halfLife, t);
    console.log("  After " + str(t) + " years: " + str(math.round(remaining * 100) / 100) + " grams");
}

// Example 6: Number theory applications
console.log("\nExample 6: Cryptographic key generation");

function isPrime(n) {
    if (n < 2) {
        return false;
    }
    if (n == 2) {
        return true;
    }
    if (n % 2 == 0) {
        return false;
    }

    limit = math.floor(math.sqrt(n));
    i = 3;
    while (i <= limit) {
        if (n % i == 0) {
            return false;
        }
        i = i + 2;
    }
    return true;
}

function totient(n) {
    // Euler's totient function - count of coprime numbers
    count = 0;
    i = 1;
    while (i <= n) {
        if (math.gcd(i, n) == 1) {
            count = count + 1;
        }
        i = i + 1;
    }
    return count;
}

primes = [];
i = 2;
while (i < 50) {
    if (isPrime(i)) {
        primes = primes + [i];
    }
    i = i + 1;
}

console.log("Prime numbers less than 50:");
console.log("  " + str(primes));
console.log("  Count: " + str(len(primes)));

// Totient function examples
console.log("\nEuler's totient function:");
testValues = [10, 12, 15, 20, 25];
for (val in testValues) {
    phi = totient(val);
    console.log("  phi(" + str(val) + ") = " + str(phi));
}

console.log("\n=== Analysis Complete ===");
