// Test basic game syntax
import collections;
import random;
import math;

function test1() {
    config = {};
    config.max_number = 100;
    config.max_guesses = 10;
    return config;
}

function test2() {
    player = {};
    player.name = "Test";
    player.total_score = 0;
    return player;
}

function main() {
    config = test1();
    player = test2();
    print("Config max: " + config.max_number);
    print("Player: " + player.name);
    return 0;
}