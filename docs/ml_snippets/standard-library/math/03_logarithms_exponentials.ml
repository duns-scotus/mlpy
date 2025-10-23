// ============================================
// Example: Logarithms and Exponentials
// Category: standard-library/math
// Demonstrates: ln, log, exp, pow
// ============================================

import console;
import math;

console.log("=== Logarithms and Exponentials ===\n");

// Example 1: exp() - Exponential function (e^x)
console.log("Example 1: math.exp() - e^x");
console.log("exp(0) = " + str(math.exp(0)));    // 1
console.log("exp(1) = " + str(math.exp(1)));    // e (~2.718)
console.log("exp(2) = " + str(math.exp(2)));    // e^2 (~7.389)
console.log("exp(-1) = " + str(math.exp(-1)));  // 1/e (~0.368)

// Example 2: ln() - Natural logarithm (base e)
console.log("\nExample 2: math.ln() - Natural logarithm");
console.log("ln(1) = " + str(math.ln(1)));          // 0
console.log("ln(e) = " + str(math.ln(math.e)));     // 1
console.log("ln(10) = " + str(math.ln(10)));        // ~2.303
console.log("ln(-1) = " + str(math.ln(-1)));        // -999 (error)
console.log("ln(0) = " + str(math.ln(0)));          // -999 (error)

// Example 3: log() - Logarithm with custom base
console.log("\nExample 3: math.log() - Logarithm with base");
console.log("log(100, 10) = " + str(math.log(100, 10)));  // 2 (log base 10)
console.log("log(8, 2) = " + str(math.log(8, 2)));        // 3 (log base 2)
console.log("log(27, 3) = " + str(math.log(27, 3)));      // 3 (log base 3)
console.log("log(1000, 10) = " + str(math.log(1000, 10)));  // 3

// Example 4: Relationship between exp and ln
console.log("\nExample 4: Inverse relationship");
x = 5;
console.log("x = " + str(x));
console.log("exp(ln(x)) = " + str(math.exp(math.ln(x))));  // 5
console.log("ln(exp(x)) = " + str(math.ln(math.exp(x))));  // 5

// Example 5: Exponential growth
console.log("\nExample 5: Exponential growth calculation");

function compoundInterest(principal, rate, years) {
    // A = P * e^(rt)
    return principal * math.exp(rate * years);
}

principal = 1000;
rate = 0.05;  // 5% annual rate
years = 10;

final = compoundInterest(principal, rate, years);
console.log("Initial: $" + str(principal));
console.log("Rate: " + str(rate * 100) + "%");
console.log("Years: " + str(years));
console.log("Final: $" + str(round(final, 2)));

// Example 6: Logarithmic scales
console.log("\nExample 6: Decibel calculation (log scale)");

function decibels(power, reference) {
    // dB = 10 * log10(P / P0)
    return 10 * math.log(power / reference, 10);
}

reference = 1;
powers = [10, 100, 1000, 10000];

console.log("Power levels in decibels:");
for (p in powers) {
    db = decibels(p, reference);
    console.log("  Power " + str(p) + ": " + str(db) + " dB");
}

// Example 7: Half-life calculations
console.log("\nExample 7: Half-life decay");

function decay(initial, halfLife, time) {
    // N(t) = N0 * e^(-ln(2) * t / t_half)
    decayRate = -math.ln(2) / halfLife;
    return initial * math.exp(decayRate * time);
}

initial = 100;
halfLife = 5;  // years

console.log("Initial amount: " + str(initial));
console.log("Half-life: " + str(halfLife) + " years");

times = [0, 5, 10, 15, 20];
for (t in times) {
    amount = decay(initial, halfLife, t);
    console.log("  After " + str(t) + " years: " + str(round(amount, 2)));
}

// Example 8: Population growth
console.log("\nExample 8: Population growth model");

function populationGrowth(initial, growthRate, years) {
    // P(t) = P0 * e^(r * t)
    return initial * math.exp(growthRate * years);
}

initialPop = 1000;
growthRate = 0.02;  // 2% per year

console.log("Initial population: " + str(initialPop));
console.log("Growth rate: " + str(growthRate * 100) + "%");

yearList = [0, 5, 10, 15, 20];
for (year in yearList) {
    pop = populationGrowth(initialPop, growthRate, year);
    console.log("  Year " + str(year) + ": " + str(round(pop, 0)));
}

// Example 9: pH calculations (log scale)
console.log("\nExample 9: pH calculation");

function pH(hydrogenConcentration) {
    // pH = -log10([H+])
    return -math.log(hydrogenConcentration, 10);
}

concentrations = [1, 0.1, 0.01, 0.001, 0.0001];
for (conc in concentrations) {
    phValue = pH(conc);
    console.log("  [H+] = " + str(conc) + " -> pH = " + str(round(phValue, 1)));
}

console.log("\n=== Logarithms and Exponentials Complete ===");
