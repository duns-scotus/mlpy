// ============================================
// Example: Basic Random Generation
// Category: standard-library/random
// Demonstrates: random, randomFloat, randomInt, randomBool
// ============================================

import console;
import random;

console.log("=== Basic Random Generation ===\n");

// ============================================
// Random Float (0-1)
// ============================================

console.log("=== Random Float (0-1) ===");

console.log("Generating 5 random floats:");
i = 0;
while (i < 5) {
    value = random.random();
    console.log("  " + str(value));
    i = i + 1;
}

// ============================================
// Random Float in Range
// ============================================

console.log("\n=== Random Float in Range ===");

// Temperature simulation (15-30 degrees)
console.log("Simulated temperatures (15-30 degrees):");
i = 0;
while (i < 5) {
    temp = random.randomFloat(15, 30);
    console.log("  " + str(round(temp, 1)) + " degrees");
    i = i + 1;
}

// Price variations (10-50 dollars)
console.log("\nSimulated prices ($10-$50):");
i = 0;
while (i < 3) {
    price = random.randomFloat(10, 50);
    console.log("  $" + str(round(price, 2)));
    i = i + 1;
}

// ============================================
// Random Integer
// ============================================

console.log("\n=== Random Integer ===");

// Dice rolls (1-6)
console.log("Dice rolls (1-6):");
i = 0;
while (i < 10) {
    roll = random.randomInt(1, 7);
    console.log("  Roll " + str(i + 1) + ": " + str(roll));
    i = i + 1;
}

// Random years (2000-2025)
console.log("\nRandom years (2000-2025):");
i = 0;
while (i < 5) {
    year = random.randomInt(2000, 2026);
    console.log("  " + str(year));
    i = i + 1;
}

// ============================================
// Random Boolean
// ============================================

console.log("\n=== Random Boolean ===");

// Coin flips (50/50)
console.log("Coin flips (10 flips):");
heads = 0;
tails = 0;
i = 0;
while (i < 10) {
    flip = random.randomBool();
    if (flip) {
        console.log("  Flip " + str(i + 1) + ": Heads");
        heads = heads + 1;
    } else {
        console.log("  Flip " + str(i + 1) + ": Tails");
        tails = tails + 1;
    }
    i = i + 1;
}
console.log("Result: " + str(heads) + " heads, " + str(tails) + " tails");

// ============================================
// Weighted Boolean
// ============================================

console.log("\n=== Weighted Boolean ===");

// 70% chance of rain
console.log("Weather forecast (70% rain chance, 10 days):");
rainyDays = 0;
i = 0;
while (i < 10) {
    willRain = random.randomBoolWeighted(0.7);
    if (willRain) {
        console.log("  Day " + str(i + 1) + ": Rainy");
        rainyDays = rainyDays + 1;
    } else {
        console.log("  Day " + str(i + 1) + ": Sunny");
    }
    i = i + 1;
}
console.log("Total rainy days: " + str(rainyDays) + "/10");

// 20% chance of critical hit
console.log("\nGame attacks (20% critical hit chance):");
criticals = 0;
i = 0;
while (i < 10) {
    isCritical = random.randomBoolWeighted(0.2);
    if (isCritical) {
        damage = random.randomInt(50, 100);
        console.log("  Attack " + str(i + 1) + ": CRITICAL! " + str(damage) + " damage");
        criticals = criticals + 1;
    } else {
        damage = random.randomInt(10, 30);
        console.log("  Attack " + str(i + 1) + ": Normal - " + str(damage) + " damage");
    }
    i = i + 1;
}
console.log("Critical hits: " + str(criticals) + "/10");

// ============================================
// Practical Example: Random Password Generator
// ============================================

console.log("\n=== Practical: Random Password Generator ===");

function generatePassword(length) {
    // Simplified: generate numeric password
    password = "";
    i = 0;
    while (i < length) {
        digit = random.randomInt(0, 10);
        password = password + str(digit);
        i = i + 1;
    }
    return password;
}

console.log("Generated passwords:");
i = 0;
while (i < 5) {
    pwd = generatePassword(8);
    console.log("  " + pwd);
    i = i + 1;
}

// ============================================
// Practical Example: Random Data Generator
// ============================================

console.log("\n=== Practical: Random Test Data ===");

function generateUser(id) {
    age = random.randomInt(18, 65);
    score = random.randomInt(0, 100);
    active = random.randomBool();

    return {
        id: id,
        age: age,
        score: score,
        active: active
    };
}

console.log("Generated users:");
users = [];
i = 0;
while (i < 5) {
    user = generateUser(i + 1);
    users = users + [user];
    status = "";
    if (user.active) {
        status = "active";
    } else {
        status = "inactive";
    }
    console.log("  User " + str(user.id) + ": age=" + str(user.age) + ", score=" + str(user.score) + ", " + status);
    i = i + 1;
}

// Calculate statistics
totalScore = 0;
activeCount = 0;
i = 0;
while (i < len(users)) {
    totalScore = totalScore + users[i].score;
    if (users[i].active) {
        activeCount = activeCount + 1;
    }
    i = i + 1;
}

avgScore = totalScore / len(users);
console.log("\nStatistics:");
console.log("  Average score: " + str(round(avgScore, 1)));
console.log("  Active users: " + str(activeCount) + "/" + str(len(users)));

console.log("\n=== Basic Random Generation Complete ===");
