// ============================================
// Example: While Loops
// Category: language-reference/control-flow
// Demonstrates: while loops, loop conditions, accumulation
// ============================================

import console;

// Basic while loop
console.log("Counting to 5:");
count = 0;
while (count < 5) {
    console.log("  " + str(count));
    count = count + 1;
}

// Sum calculation with while
console.log("\nCalculating sum of 1 to 10:");
totalSum = 0;
i = 1;
while (i <= 10) {
    totalSum = totalSum + i;
    i = i + 1;
}
console.log("Sum: " + str(totalSum));

// Power of 2 sequence
console.log("\nPowers of 2 less than 1000:");
value = 1;
while (value < 1000) {
    console.log("  " + str(value));
    value = value * 2;
}

// Countdown
console.log("\nCountdown:");
counter = 5;
while (counter > 0) {
    console.log("  " + str(counter));
    counter = counter - 1;
}
console.log("Liftoff!");

// Finding first value exceeding threshold
console.log("\nFinding when factorial exceeds 1000:");
n = 1;
factorial = 1;
while (factorial <= 1000) {
    factorial = factorial * n;
    n = n + 1;
}
console.log("Factorial of " + str(n - 1) + " = " + str(factorial));
