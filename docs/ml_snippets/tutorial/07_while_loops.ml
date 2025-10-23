// ============================================
// Example: While Loops
// Category: tutorial
// Demonstrates: While loop basics and patterns
// ============================================

import console;

// Basic counter
console.log("=== Basic Counter ===");
count = 0;
while (count < 5) {
    console.log("Count: " + str(count));
    count = count + 1;
}

// Sum of numbers
console.log("");
console.log("=== Sum of Numbers 1 to 10 ===");
total = 0;
number = 1;
while (number <= 10) {
    total = total + number;
    number = number + 1;
}
console.log("Total: " + str(total));

// Countdown
console.log("");
console.log("=== Countdown ===");
countdown = 5;
while (countdown > 0) {
    console.log(str(countdown) + "...");
    countdown = countdown - 1;
}
console.log("Liftoff!");

// Finding first match
console.log("");
console.log("=== Finding First Power of 2 Greater Than 100 ===");
power = 1;
exponent = 0;
while (power <= 100) {
    power = power * 2;
    exponent = exponent + 1;
}
console.log("2^" + str(exponent) + " = " + str(power));

// Building a string
console.log("");
console.log("=== Building Pattern ===");
pattern = "";
stars = 1;
while (stars <= 5) {
    line = "";
    i = 0;
    while (i < stars) {
        line = line + "*";
        i = i + 1;
    }
    console.log(line);
    stars = stars + 1;
}
