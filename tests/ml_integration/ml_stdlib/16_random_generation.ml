// Test stdlib module: random - Random number generation
// Features tested: seed, random, randomInt, randomFloat, randomBool, choice
// Module: random

import random;

function test_seed() {
    results = {};

    // Set seed for reproducibility
    random.setSeed(42);
    val1 = random.randomInt(1, 100);

    random.setSeed(42);
    val2 = random.randomInt(1, 100);

    // Same seed should produce same results
    results.reproducible = val1 == val2;    // true

    return results;
}

function test_randomInt() {
    results = {};

    // Generate random integers in range
    val1 = random.randomInt(1, 10);
    val2 = random.randomInt(1, 10);
    val3 = random.randomInt(1, 10);

    results.in_range1 = val1 >= 1 && val1 <= 10;
    results.in_range2 = val2 >= 1 && val2 <= 10;
    results.in_range3 = val3 >= 1 && val3 <= 10;

    return results;
}

function test_randomFloat() {
    results = {};

    // Generate random floats
    val = random.randomFloat(0.0, 1.0);

    results.in_range = val >= 0.0 && val <= 1.0;

    return results;
}

function test_randomBool() {
    results = {};

    // Generate random booleans
    val1 = random.randomBool();
    val2 = random.randomBool();

    results.is_bool1 = typeof(val1) == "boolean";
    results.is_bool2 = typeof(val2) == "boolean";

    return results;
}

function test_choice() {
    results = {};

    // Random choice from array
    arr = ["apple", "banana", "cherry"];
    choice = random.choice(arr);

    results.is_valid = (choice == "apple" || choice == "banana" || choice == "cherry");

    return results;
}

function test_sample() {
    results = {};

    // Random sample without replacement
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    sample = random.sample(arr, 3);

    results.sample_size = len(sample);      // 3
    results.from_original = sample[0] >= 1 && sample[0] <= 10;

    return results;
}

function test_shuffle() {
    results = {};

    // Shuffle array
    arr = [1, 2, 3, 4, 5];
    shuffled = random.shuffle(arr);

    results.same_size = len(shuffled) == len(arr);
    results.has_elements = len(shuffled) == 5;

    return results;
}

function main() {
    all_results = {};

    all_results.seed = test_seed();
    all_results.int = test_randomInt();
    all_results.float = test_randomFloat();
    all_results.bool = test_randomBool();
    all_results.choice = test_choice();
    all_results.sample = test_sample();
    all_results.shuffle = test_shuffle();

    return all_results;
}

// Run tests
test_results = main();
