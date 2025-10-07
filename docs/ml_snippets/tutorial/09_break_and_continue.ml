// ============================================
// Example: Break and Continue
// Category: tutorial
// Demonstrates: Loop control with break and continue
// ============================================

import console;

// Break: exit loop early
console.log("=== Break: Finding First Match ===");
numbers = [3, 7, 12, 9, 15, 21, 8];
targetFound = false;
foundValue = -1;
for (num in numbers) {
    if (num > 10) {
        foundValue = num;
        targetFound = true;
        break;
    }
}
if (targetFound) {
    console.log("First number > 10: " + str(foundValue));
}

// Continue: skip certain iterations
console.log("");
console.log("=== Continue: Processing Only Even Numbers ===");
allNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
evenSum = 0;
for (n in allNumbers) {
    if (n % 2 != 0) {
        continue;
    }
    evenSum = evenSum + n;
}
console.log("Sum of even numbers: " + str(evenSum));

// Break in while loop
console.log("");
console.log("=== Break in While: Countdown with Early Stop ===");
countdown = 10;
while (countdown > 0) {
    console.log(str(countdown));
    countdown = countdown - 1;
    if (countdown == 5) {
        console.log("Aborted at 5!");
        break;
    }
}

// Continue in while loop
console.log("");
console.log("=== Continue in While: Skip Multiples of 3 ===");
i = 0;
while (i < 10) {
    i = i + 1;
    if (i % 3 == 0) {
        continue;
    }
    console.log(str(i));
}

// Practical example: search and validation
console.log("");
console.log("=== Practical: User Search ===");
users = [
    {name: "Alice", age: 25, active: true},
    {name: "Bob", age: 17, active: false},
    {name: "Carol", age: 30, active: true},
    {name: "Dave", age: 22, active: true}
];

console.log("Active adult users:");
for (user in users) {
    if (!user.active) {
        continue;
    }
    if (user.age < 18) {
        continue;
    }
    console.log("- " + user.name + " (age " + str(user.age) + ")");
}

// Nested loops with break
console.log("");
console.log("=== Nested Loops: Finding First Pair ===");
firstList = [1, 2, 3, 4];
secondList = [5, 6, 7, 8];
found = false;
for (a in firstList) {
    for (b in secondList) {
        if (a + b == 10) {
            console.log("Found pair: " + str(a) + " + " + str(b) + " = 10");
            found = true;
            break;
        }
    }
    if (found) {
        break;
    }
}
