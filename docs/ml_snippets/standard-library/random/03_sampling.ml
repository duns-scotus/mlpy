// ============================================
// Example: List Sampling
// Category: standard-library/random
// Demonstrates: choice, shuffle, sample, randomIndices
// ============================================

import console;
import random;

console.log("=== List Sampling ===\n");

// ============================================
// Choice - Pick Random Element
// ============================================

console.log("=== Choice (pick one element) ===");

fruits = ["apple", "banana", "cherry", "date", "elderberry"];
console.log("Fruits: " + str(fruits));

console.log("\nRandom picks:");
i = 0;
while (i < 5) {
    picked = random.choice(fruits);
    console.log("  Pick " + str(i + 1) + ": " + picked);
    i = i + 1;
}

// Pick from numbers
numbers = [10, 20, 30, 40, 50];
console.log("\nNumbers: " + str(numbers));
console.log("Random number: " + str(random.choice(numbers)));

// ============================================
// Shuffle - Randomize Order
// ============================================

console.log("\n=== Shuffle (randomize order) ===");

deck = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"];
console.log("Original deck: " + str(deck));

shuffled = random.shuffle(deck);
console.log("Shuffled deck: " + str(shuffled));

// Original unchanged
console.log("Original unchanged: " + str(deck));

// Shuffle again
shuffled2 = random.shuffle(deck);
console.log("Another shuffle: " + str(shuffled2));

// ============================================
// Sample - Pick Multiple Elements
// ============================================

console.log("\n=== Sample (pick multiple) ===");

participants = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"];
console.log("Participants: " + str(participants));

// Pick 3 winners
winners = random.sample(participants, 3);
console.log("\nWinners (3 random): " + str(winners));

// Pick 5 for team
team = random.sample(participants, 5);
console.log("Team members (5 random): " + str(team));

// ============================================
// Random Indices
// ============================================

console.log("\n=== Random Indices ===");

dataSize = 100;
sampleSize = 5;

indices = random.randomIndices(dataSize, sampleSize);
console.log("Random indices from 0-99 (5 samples): " + str(indices));

// Use indices to sample from list
items = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
console.log("\nItems: " + str(items));

randomIdx = random.randomIndices(len(items), 3);
console.log("Random indices: " + str(randomIdx));

sampled = [];
i = 0;
while (i < len(randomIdx)) {
    idx = randomIdx[i];
    sampled = sampled + [items[idx]];
    i = i + 1;
}
console.log("Sampled items: " + str(sampled));

// ============================================
// Practical Example: Card Game
// ============================================

console.log("\n=== Practical: Card Dealing ===");

function createDeck() {
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"];
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"];

    deck = [];
    i = 0;
    while (i < len(suits)) {
        j = 0;
        while (j < len(ranks)) {
            card = ranks[j] + " of " + suits[i];
            deck = deck + [card];
            j = j + 1;
        }
        i = i + 1;
    }

    return deck;
}

fullDeck = createDeck();
console.log("Created deck with " + str(len(fullDeck)) + " cards");

// Shuffle and deal
shuffledDeck = random.shuffle(fullDeck);
console.log("Shuffled deck");

// Deal 5 cards to player
hand = random.sample(shuffledDeck, 5);
console.log("\nPlayer's hand:");
i = 0;
while (i < len(hand)) {
    console.log("  " + str(i + 1) + ". " + hand[i]);
    i = i + 1;
}

// ============================================
// Practical Example: Random Quiz
// ============================================

console.log("\n=== Practical: Random Quiz Generator ===");

questions = [
    {id: 1, question: "What is 2+2?", difficulty: "easy"},
    {id: 2, question: "What is the capital of France?", difficulty: "easy"},
    {id: 3, question: "Who wrote Hamlet?", difficulty: "medium"},
    {id: 4, question: "What is the speed of light?", difficulty: "hard"},
    {id: 5, question: "When was WW2?", difficulty: "medium"},
    {id: 6, question: "What is DNA?", difficulty: "hard"},
    {id: 7, question: "Name a primary color", difficulty: "easy"},
    {id: 8, question: "What is photosynthesis?", difficulty: "medium"}
];

console.log("Total questions available: " + str(len(questions)));

// Generate random quiz with 5 questions
quizSize = 5;
selectedQuestions = random.sample(questions, quizSize);

console.log("\nRandom Quiz (" + str(quizSize) + " questions):");
i = 0;
while (i < len(selectedQuestions)) {
    q = selectedQuestions[i];
    console.log("  Q" + str(i + 1) + ": " + q.question + " [" + q.difficulty + "]");
    i = i + 1;
}

// ============================================
// Practical Example: Team Assignment
// ============================================

console.log("\n=== Practical: Random Team Assignment ===");

students = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack"];
console.log("Students: " + str(students));

teamSize = 3;
console.log("Team size: " + str(teamSize));

// Shuffle students
shuffled = random.shuffle(students);

// Assign to teams
teamNum = 1;
i = 0;
while (i < len(shuffled)) {
    console.log("\nTeam " + str(teamNum) + ":");

    j = 0;
    while (j < teamSize && (i + j) < len(shuffled)) {
        console.log("  - " + shuffled[i + j]);
        j = j + 1;
    }

    i = i + teamSize;
    teamNum = teamNum + 1;
}

// ============================================
// Practical Example: Random Sampling Survey
// ============================================

console.log("\n=== Practical: Random Survey Sampling ===");

population = [];
i = 1;
while (i <= 1000) {
    population = population + [i];
    i = i + 1;
}

console.log("Population size: " + str(len(population)));

sampleSize = 50;
console.log("Sample size: " + str(sampleSize));

// Random sample for survey
surveyParticipants = random.sample(population, sampleSize);

console.log("\nFirst 10 participant IDs:");
i = 0;
while (i < 10) {
    console.log("  " + str(surveyParticipants[i]));
    i = i + 1;
}

// Calculate sample statistics
sum = 0;
i = 0;
while (i < len(surveyParticipants)) {
    sum = sum + surveyParticipants[i];
    i = i + 1;
}

avgId = sum / len(surveyParticipants);
console.log("\nSample statistics:");
console.log("  Average ID: " + str(round(avgId, 1)));
console.log("  Expected (random): ~500");

// ============================================
// Practical Example: Lottery System
// ============================================

console.log("\n=== Practical: Lottery Number Generator ===");

function generateLotteryNumbers(count, maxNum) {
    // Generate unique random numbers
    numbers = [];
    i = 1;
    while (i <= maxNum) {
        numbers = numbers + [i];
        i = i + 1;
    }

    // Pick random sample
    picked = random.sample(numbers, count);

    // Sort for display
    sorted = [];
    while (len(picked) > 0) {
        smallest = picked[0];
        smallestIdx = 0;

        i = 1;
        while (i < len(picked)) {
            if (picked[i] < smallest) {
                smallest = picked[i];
                smallestIdx = i;
            }
            i = i + 1;
        }

        sorted = sorted + [smallest];

        // Remove from picked
        newPicked = [];
        i = 0;
        while (i < len(picked)) {
            if (i != smallestIdx) {
                newPicked = newPicked + [picked[i]];
            }
            i = i + 1;
        }
        picked = newPicked;
    }

    return sorted;
}

console.log("Generating lottery tickets:");
i = 0;
while (i < 3) {
    ticket = generateLotteryNumbers(6, 49);
    console.log("  Ticket " + str(i + 1) + ": " + str(ticket));
    i = i + 1;
}

console.log("\n=== List Sampling Complete ===");
