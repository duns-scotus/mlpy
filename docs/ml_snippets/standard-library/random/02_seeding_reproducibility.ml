// ============================================
// Example: Seeding and Reproducibility
// Category: standard-library/random
// Demonstrates: setSeed, getSeed, nextInt, reproducible sequences
// ============================================

import console;
import random;

console.log("=== Seeding and Reproducibility ===\n");

// ============================================
// Setting and Getting Seed
// ============================================

console.log("=== Seed Management ===");

// Set specific seed
seed = random.setSeed(42);
console.log("Set seed to: " + str(seed));

// Get current seed
currentSeed = random.getSeed();
console.log("Current seed: " + str(currentSeed));

// ============================================
// Reproducible Sequences
// ============================================

console.log("\n=== Reproducible Sequences ===");

// First sequence with seed 100
console.log("Sequence 1 (seed=100):");
random.setSeed(100);
i = 0;
while (i < 5) {
    value = random.randomInt(1, 100);
    console.log("  " + str(value));
    i = i + 1;
}

// Different seed produces different sequence
console.log("\nSequence 2 (seed=200):");
random.setSeed(200);
i = 0;
while (i < 5) {
    value = random.randomInt(1, 100);
    console.log("  " + str(value));
    i = i + 1;
}

// Same seed reproduces first sequence
console.log("\nSequence 3 (seed=100 again):");
random.setSeed(100);
i = 0;
while (i < 5) {
    value = random.randomInt(1, 100);
    console.log("  " + str(value));
    i = i + 1;
}

// ============================================
// NextInt - Raw Random Integers
// ============================================

console.log("\n=== NextInt (Large Random Integers) ===");

random.setSeed(12345);
console.log("Generating 5 large random integers:");
i = 0;
while (i < 5) {
    large = random.nextInt();
    console.log("  " + str(large));
    i = i + 1;
}

// ============================================
// Practical Example: Reproducible Testing
// ============================================

console.log("\n=== Practical: Reproducible Testing ===");

function runSimulation(seed) {
    random.setSeed(seed);

    console.log("\nSimulation with seed " + str(seed) + ":");

    // Generate test data
    values = [];
    i = 0;
    while (i < 10) {
        value = random.randomInt(1, 100);
        values = values + [value];
        i = i + 1;
    }

    // Calculate statistics
    sum = 0;
    i = 0;
    while (i < len(values)) {
        sum = sum + values[i];
        i = i + 1;
    }

    avg = sum / len(values);
    console.log("  Values: " + str(values));
    console.log("  Average: " + str(round(avg, 1)));

    return avg;
}

// Run same simulation twice
result1 = runSimulation(999);
result2 = runSimulation(999);

console.log("\nResults match? " + str(result1 == result2));

// ============================================
// Practical Example: Deterministic Game
// ============================================

console.log("\n=== Practical: Deterministic Game Replay ===");

function playGame(gameSeed) {
    random.setSeed(gameSeed);

    console.log("Game with seed " + str(gameSeed) + ":");

    playerHealth = 100;
    enemyHealth = 80;
    turn = 1;

    while (playerHealth > 0 && enemyHealth > 0 && turn <= 5) {
        // Player attacks
        playerDamage = random.randomInt(10, 25);
        enemyHealth = enemyHealth - playerDamage;
        console.log("  Turn " + str(turn) + " - Player deals " + str(playerDamage) + " damage");

        if (enemyHealth > 0) {
            // Enemy attacks
            enemyDamage = random.randomInt(5, 15);
            playerHealth = playerHealth - enemyDamage;
            console.log("  Turn " + str(turn) + " - Enemy deals " + str(enemyDamage) + " damage");
        }

        turn = turn + 1;
    }

    console.log("  Final: Player HP=" + str(playerHealth) + ", Enemy HP=" + str(enemyHealth));

    if (enemyHealth <= 0) {
        return "Player wins!";
    } elif (playerHealth <= 0) {
        return "Enemy wins!";
    } else {
        return "Draw";
    }
}

// Play game twice with same seed
result1 = playGame(777);
console.log("Result: " + result1);

console.log("\nReplay with same seed:");
result2 = playGame(777);
console.log("Result: " + result2);

console.log("\nDifferent seed produces different outcome:");
result3 = playGame(888);
console.log("Result: " + result3);

// ============================================
// Practical Example: Random but Fair
// ============================================

console.log("\n=== Practical: Fair Tournament Brackets ===");

function generateBrackets(teams, tournamentSeed) {
    random.setSeed(tournamentSeed);

    console.log("Tournament seed: " + str(tournamentSeed));
    console.log("Teams: " + str(teams));

    // Shuffle teams
    shuffled = [];
    remaining = teams;

    while (len(remaining) > 0) {
        // Pick random team
        idx = random.randomInt(0, len(remaining));
        shuffled = shuffled + [remaining[idx]];

        // Remove from remaining
        newRemaining = [];
        i = 0;
        while (i < len(remaining)) {
            if (i != idx) {
                newRemaining = newRemaining + [remaining[i]];
            }
            i = i + 1;
        }
        remaining = newRemaining;
    }

    // Create matchups
    console.log("Matchups:");
    i = 0;
    while (i < len(shuffled) - 1) {
        console.log("  Match " + str(i / 2 + 1) + ": " + shuffled[i] + " vs " + shuffled[i + 1]);
        i = i + 2;
    }

    return shuffled;
}

teams = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta"];
brackets = generateBrackets(teams, 2024);

// Regenerate same brackets
console.log("\nRegenerate with same seed:");
brackets2 = generateBrackets(teams, 2024);

// ============================================
// Snapshot Testing Pattern
// ============================================

console.log("\n=== Pattern: Snapshot Testing ===");

function generateTestData(seed, count) {
    random.setSeed(seed);

    data = [];
    i = 0;
    while (i < count) {
        item = {
            value: random.randomInt(0, 1000),
            flag: random.randomBool()
        };
        data = data + [item];
        i = i + 1;
    }

    return data;
}

// Generate snapshot
testSeed = 54321;
snapshot = generateTestData(testSeed, 5);
console.log("Test snapshot (seed=" + str(testSeed) + "):");
console.log(str(snapshot));

// Verify reproducibility
console.log("\nVerify snapshot:");
verification = generateTestData(testSeed, 5);
console.log(str(verification));

// Check if they match
match = true;
if (len(snapshot) != len(verification)) {
    match = false;
} else {
    i = 0;
    while (i < len(snapshot)) {
        if (snapshot[i].value != verification[i].value) {
            match = false;
        }
        if (snapshot[i].flag != verification[i].flag) {
            match = false;
        }
        i = i + 1;
    }
}

console.log("Snapshots match? " + str(match));

console.log("\n=== Seeding and Reproducibility Complete ===");
