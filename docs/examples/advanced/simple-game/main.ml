// Number Guessing Strategy Game - Advanced ML Demo
// Demonstrates ML's functional programming, state management, and game logic
// Using only currently implemented ML language features

import collections;
import random;
import math;

// Game configuration
function createGameConfig() {
    config = {};
    config.max_number = 100;
    config.max_guesses = 10;
    config.difficulty_levels = 3;
    config.points_per_game = 100;
    return config;
}

// Player stats tracking
function createPlayer(name) {
    player = {};
    player.name = name;
    player.total_score = 0;
    player.games_played = 0;
    player.games_won = 0;
    player.total_guesses = 0;
    player.best_score = 0;
    player.current_streak = 0;
    player.best_streak = 0;
    return player;
}

// Game session state
function createGameSession(player, config, difficulty) {
    session = {};
    session.player = player;
    session.config = config;
    session.difficulty = difficulty;
    session.target_number = generateTargetNumber(config.max_number, difficulty);
    session.guesses_made = [];
    session.guesses_remaining = config.max_guesses - difficulty;
    session.game_over = false;
    session.won = false;
    session.score = 0;
    session.hints_used = 0;
    session.start_time = 0;
    return session;
}

// Generate target number based on difficulty
function generateTargetNumber(max_number, difficulty) {
    if (difficulty == 1) {
        // Easy: 1-50
        return random.randomInt(1, 50);
    } elif (difficulty == 2) {
        // Medium: 1-75
        return random.randomInt(1, 75);
    } else {
        // Hard: 1-100
        return random.randomInt(1, max_number);
    }
}

// Core game logic
function makeGuess(session, guess_number) {
    // Validate guess
    max_for_difficulty = getDifficultyMaxNumber(session.difficulty);
    if (guess_number < 1 || guess_number > max_for_difficulty) {
        return createGuessResult(false, "Invalid guess! Must be between 1 and " + max_for_difficulty, session);
    }

    // Check if already guessed
    if (collections.contains(session.guesses_made, guess_number)) {
        return createGuessResult(false, "You already guessed " + guess_number + "!", session);
    }

    // Add guess to history
    session.guesses_made = collections.append(session.guesses_made, guess_number);
    session.guesses_remaining = session.guesses_remaining - 1;

    // Check if correct
    if (guess_number == session.target_number) {
        session.won = true;
        session.game_over = true;
        session.score = calculateScore(session);
        message = "Congratulations! You guessed " + session.target_number + " correctly!";
        return createGuessResult(true, message, session);
    }

    // Check if out of guesses
    if (session.guesses_remaining <= 0) {
        session.game_over = true;
        message = "Game over! The number was " + session.target_number;
        return createGuessResult(false, message, session);
    }

    // Provide hint
    hint = generateHint(session, guess_number);
    return createGuessResult(false, hint, session);
}

function getDifficultyMaxNumber(difficulty) {
    if (difficulty == 1) {
        return 50;
    } elif (difficulty == 2) {
        return 75;
    } else {
        return 100;
    }
}

function createGuessResult(correct, message, session) {
    result = {};
    result.correct = correct;
    result.message = message;
    result.session = session;
    result.guesses_remaining = session.guesses_remaining;
    result.game_over = session.game_over;
    return result;
}

// Hint generation system
function generateHint(session, guess_number) {
    target = session.target_number;
    difference = math.abs(guess_number - target);

    base_hint = "";
    if (guess_number < target) {
        base_hint = "Too low! ";
    } else {
        base_hint = "Too high! ";
    }

    // Distance-based hints
    if (difference <= 5) {
        base_hint = base_hint + "Very close!";
    } elif (difference <= 15) {
        base_hint = base_hint + "Getting warm!";
    } elif (difference <= 30) {
        base_hint = base_hint + "Getting warmer...";
    } else {
        base_hint = base_hint + "Way off!";
    }

    // Add remaining guesses info
    base_hint = base_hint + " (" + session.guesses_remaining + " guesses left)";

    // Advanced hint every few guesses
    if (collections.length(session.guesses_made) >= 3) {
        advanced_hint = generateAdvancedHint(session);
        base_hint = base_hint + " " + advanced_hint;
    }

    return base_hint;
}

function generateAdvancedHint(session) {
    target = session.target_number;

    // Range hint based on previous guesses
    low_guess = findClosestLowGuess(session.guesses_made, target);
    high_guess = findClosestHighGuess(session.guesses_made, target);

    if (low_guess != -1 && high_guess != -1) {
        return "Hint: Between " + low_guess + " and " + high_guess;
    } elif (low_guess != -1) {
        return "Hint: Higher than " + low_guess;
    } elif (high_guess != -1) {
        return "Hint: Lower than " + high_guess;
    }

    // Mathematical hint
    if (target % 2 == 0) {
        return "Hint: The number is even";
    } else {
        return "Hint: The number is odd";
    }
}

function findClosestLowGuess(guesses, target) {
    closest = -1;
    guesses_length = collections.length(guesses);

    i = 0;
    while (i < guesses_length) {
        guess = guesses[i];
        if (guess < target && guess > closest) {
            closest = guess;
        }
        i = i + 1;
    }

    return closest;
}

function findClosestHighGuess(guesses, target) {
    closest = 999;
    guesses_length = collections.length(guesses);

    i = 0;
    while (i < guesses_length) {
        guess = guesses[i];
        if (guess > target && guess < closest) {
            closest = guess;
        }
        i = i + 1;
    }

    return closest == 999 ? -1 : closest;
}

// Scoring system
function calculateScore(session) {
    base_score = 1000;

    // Bonus for fewer guesses
    guesses_made = collections.length(session.guesses_made);
    guess_bonus = (session.config.max_guesses - guesses_made) * 50;

    // Difficulty multiplier
    difficulty_multiplier = session.difficulty;

    // Penalty for hints
    hint_penalty = session.hints_used * 25;

    score = (base_score + guess_bonus) * difficulty_multiplier - hint_penalty;
    return math.max(0, score);
}

// Update player statistics
function updatePlayerStats(player, session) {
    player.games_played = player.games_played + 1;
    player.total_guesses = player.total_guesses + collections.length(session.guesses_made);

    if (session.won) {
        player.games_won = player.games_won + 1;
        player.current_streak = player.current_streak + 1;
        player.total_score = player.total_score + session.score;

        if (session.score > player.best_score) {
            player.best_score = session.score;
        }

        if (player.current_streak > player.best_streak) {
            player.best_streak = player.current_streak;
        }
    } else {
        player.current_streak = 0;
    }

    return player;
}

// Game strategy AI (for automated testing)
function createAIPlayer() {
    ai = {};
    ai.name = "AI Player";
    ai.strategy = "binary_search";
    ai.min_range = 1;
    ai.max_range = 100;
    ai.last_guess = -1;
    return ai;
}

function getAIGuess(ai, session, last_result) {
    if (ai.strategy == "binary_search") {
        return binarySearchGuess(ai, session, last_result);
    } else {
        return randomGuess(ai, session);
    }
}

function binarySearchGuess(ai, session, last_result) {
    if (last_result != null) {
        if (ai.last_guess < session.target_number) {
            ai.min_range = ai.last_guess + 1;
        } else {
            ai.max_range = ai.last_guess - 1;
        }
    }

    guess = math.floor((ai.min_range + ai.max_range) / 2);
    ai.last_guess = guess;
    return guess;
}

function randomGuess(ai, session) {
    max_num = getDifficultyMaxNumber(session.difficulty);
    return random.randomInt(1, max_num);
}

// Display functions
function displayGameStatus(session) {
    print("=== Number Guessing Game ===");
    print("Player: " + session.player.name);
    print("Difficulty: " + getDifficultyName(session.difficulty));
    print("Range: 1-" + getDifficultyMaxNumber(session.difficulty));
    print("Guesses remaining: " + session.guesses_remaining);
    print("Previous guesses: " + formatGuessList(session.guesses_made));
    print("");
}

function getDifficultyName(difficulty) {
    if (difficulty == 1) {
        return "Easy";
    } elif (difficulty == 2) {
        return "Medium";
    } else {
        return "Hard";
    }
}

function formatGuessList(guesses) {
    if (collections.length(guesses) == 0) {
        return "None";
    }

    result = "";
    guesses_length = collections.length(guesses);
    i = 0;
    while (i < guesses_length) {
        if (i > 0) {
            result = result + ", ";
        }
        result = result + guesses[i];
        i = i + 1;
    }

    return result;
}

function displayPlayerStats(player) {
    print("=== Player Statistics ===");
    print("Name: " + player.name);
    print("Games played: " + player.games_played);
    print("Games won: " + player.games_won);

    if (player.games_played > 0) {
        win_rate = math.floor(player.games_won * 100 / player.games_played);
        print("Win rate: " + win_rate + "%");
    }

    if (player.games_won > 0) {
        avg_guesses = math.floor(player.total_guesses / player.games_won);
        print("Average guesses per win: " + avg_guesses);
    }

    print("Total score: " + player.total_score);
    print("Best score: " + player.best_score);
    print("Current streak: " + player.current_streak);
    print("Best streak: " + player.best_streak);
    print("");
}

// AI tournament mode
function runAITournament() {
    print("Running AI Tournament...");

    config = createGameConfig();
    ai_player = createAIPlayer();

    total_games = 15;
    difficulties = [1, 2, 3];

    tournament_results = [];

    difficulty_index = 0;
    while (difficulty_index < collections.length(difficulties)) {
        difficulty = difficulties[difficulty_index];

        games_per_difficulty = 5;
        wins = 0;
        total_score = 0;

        game_num = 0;
        while (game_num < games_per_difficulty) {
            // Reset AI state
            ai_player.min_range = 1;
            ai_player.max_range = getDifficultyMaxNumber(difficulty);
            ai_player.last_guess = -1;

            session = createGameSession(ai_player, config, difficulty);
            last_result = null;

            while (!session.game_over) {
                guess = getAIGuess(ai_player, session, last_result);
                last_result = makeGuess(session, guess);
                session = last_result.session;
            }

            if (session.won) {
                wins = wins + 1;
                total_score = total_score + session.score;
            }

            game_num = game_num + 1;
        }

        result = {};
        result.difficulty = difficulty;
        result.wins = wins;
        result.games = games_per_difficulty;
        result.total_score = total_score;
        result.avg_score = wins > 0 ? total_score / wins : 0;
        tournament_results = collections.append(tournament_results, result);

        print("Difficulty " + getDifficultyName(difficulty) + ": " + wins + "/" + games_per_difficulty + " wins, Avg Score: " + result.avg_score);

        difficulty_index = difficulty_index + 1;
    }

    return tournament_results;
}

// Single player game simulation
function runSinglePlayerGame(difficulty) {
    config = createGameConfig();
    player = createPlayer("Demo Player");

    print("Starting single player game (Difficulty: " + getDifficultyName(difficulty) + ")");

    session = createGameSession(player, config, difficulty);
    displayGameStatus(session);

    // Simulate some intelligent guessing strategy
    guessing_strategy = createGuessingStrategy(difficulty);

    while (!session.game_over) {
        guess = getNextStrategicGuess(guessing_strategy, session);
        print("Guessing: " + guess);

        result = makeGuess(session, guess);
        session = result.session;

        print(result.message);

        if (!session.game_over) {
            updateGuessingStrategy(guessing_strategy, guess, result.message);
        }

        print("");
    }

    // Update player stats
    player = updatePlayerStats(player, session);

    print("Game completed!");
    if (session.won) {
        print("Final score: " + session.score);
    }

    displayPlayerStats(player);

    return session.won;
}

function createGuessingStrategy(difficulty) {
    strategy = {};
    strategy.min_bound = 1;
    strategy.max_bound = getDifficultyMaxNumber(difficulty);
    strategy.approach = "binary"; // or "random"
    strategy.eliminated_numbers = [];
    return strategy;
}

function getNextStrategicGuess(strategy, session) {
    if (strategy.approach == "binary") {
        return math.floor((strategy.min_bound + strategy.max_bound) / 2);
    } else {
        // Random approach
        return random.randomInt(strategy.min_bound, strategy.max_bound);
    }
}

function updateGuessingStrategy(strategy, last_guess, result_message) {
    if (collections.indexOf(result_message, "Too low") != -1) {
        strategy.min_bound = last_guess + 1;
    } elif (collections.indexOf(result_message, "Too high") != -1) {
        strategy.max_bound = last_guess - 1;
    }
}

// Main game runner
function runNumberGuessingGame() {
    print("Number Guessing Strategy Game - Advanced ML Demo");
    print("================================================");

    random.setSeed(123);

    print("Running demonstration games...");
    print("");

    // Run games at different difficulties
    difficulties = [1, 2, 3];
    wins = 0;
    total_games = collections.length(difficulties);

    i = 0;
    while (i < total_games) {
        difficulty = difficulties[i];
        won = runSinglePlayerGame(difficulty);

        if (won) {
            wins = wins + 1;
        }

        print("----------------------------------------");
        i = i + 1;
    }

    print("");
    print("Demo Results: " + wins + "/" + total_games + " games won");

    // Run AI tournament
    print("");
    print("Running AI tournament for comparison...");
    tournament_results = runAITournament();

    return wins;
}

// Entry point
function main() {
    print("Advanced Number Guessing Game");
    print("============================");

    result = runNumberGuessingGame();

    print("");
    print("Game demonstration completed successfully!");
    print("This showcases ML's object-oriented patterns, state management,");
    print("functional programming, and complex game logic implementation.");

    return 0;
}