// Tower Defense Strategy Game - Advanced ML Demo
// Demonstrates ML's object-oriented patterns, state management, and game logic
// Using only currently implemented ML language features

import collections;
import random;
import math;

// Game configuration
function createGameConfig() {
    config = {};
    config.board_width = 15;
    config.board_height = 10;
    config.initial_gold = 100;
    config.initial_lives = 20;
    config.wave_count = 10;
    config.base_enemy_health = 50;
    config.base_enemy_speed = 1.0;
    config.base_enemy_reward = 10;
    return config;
}

// Tower types and stats
function createTowerTypes() {
    types = [];

    // Basic Tower
    basic = {};
    basic.name = "Basic Tower";
    basic.cost = 25;
    basic.damage = 15;
    basic.range = 2.5;
    basic.fire_rate = 1.0;
    basic.upgrade_cost = 40;
    types = collections.append(types, basic);

    // Sniper Tower
    sniper = {};
    sniper.name = "Sniper Tower";
    sniper.cost = 60;
    sniper.damage = 45;
    sniper.range = 4.0;
    sniper.fire_rate = 0.4;
    sniper.upgrade_cost = 80;
    types = collections.append(types, sniper);

    // Rapid Fire Tower
    rapid = {};
    rapid.name = "Rapid Tower";
    rapid.cost = 40;
    rapid.damage = 8;
    rapid.range = 2.0;
    rapid.fire_rate = 2.5;
    rapid.upgrade_cost = 60;
    types = collections.append(types, rapid);

    // Splash Tower
    splash = {};
    splash.name = "Splash Tower";
    splash.cost = 80;
    splash.damage = 25;
    splash.range = 2.2;
    splash.fire_rate = 0.8;
    splash.upgrade_cost = 120;
    types = collections.append(types, splash);

    return types;
}

// Game state management
function createGameState(config) {
    state = {};
    state.config = config;
    state.tower_types = createTowerTypes();
    state.board = createBoard(config.board_width, config.board_height);
    state.path = generatePath(config.board_width, config.board_height);
    state.towers = [];
    state.enemies = [];
    state.projectiles = [];
    state.gold = config.initial_gold;
    state.lives = config.initial_lives;
    state.score = 0;
    state.current_wave = 0;
    state.wave_timer = 0;
    state.game_time = 0;
    state.game_over = false;
    state.victory = false;
    return state;
}

// Create game board
function createBoard(width, height) {
    board = [];

    y = 0;
    while (y < height) {
        row = [];
        x = 0;
        while (x < width) {
            cell = {};
            cell.x = x;
            cell.y = y;
            cell.type = "empty";
            cell.tower = null;
            row = collections.append(row, cell);
            x = x + 1;
        }
        board = collections.append(board, row);
        y = y + 1;
    }

    return board;
}

// Generate enemy path
function generatePath(width, height) {
    path = [];

    // Create S-shaped path for interesting gameplay
    // Start from left side
    start_y = math.floor(height / 2);

    // First segment: left to right, slight curve
    x = 0;
    while (x < width / 3) {
        pos = {};
        pos.x = x;
        pos.y = start_y + math.floor(math.sin(x * 0.5) * 1.5);
        pos.y = math.max(1, math.min(height - 2, pos.y));
        path = collections.append(path, pos);
        x = x + 1;
    }

    // Second segment: curve down
    while (x < 2 * width / 3) {
        pos = {};
        pos.x = x;
        pos.y = start_y + math.floor(math.sin(x * 0.3) * 2) + 2;
        pos.y = math.max(1, math.min(height - 2, pos.y));
        path = collections.append(path, pos);
        x = x + 1;
    }

    // Third segment: to exit
    while (x < width) {
        pos = {};
        pos.x = x;
        pos.y = start_y - 1;
        pos.y = math.max(1, math.min(height - 2, pos.y));
        path = collections.append(path, pos);
        x = x + 1;
    }

    return path;
}

// Enemy creation and management
function createEnemy(wave_number, path) {
    enemy = {};
    enemy.type = selectEnemyType(wave_number);
    enemy.health = enemy.type.base_health * (1 + wave_number * 0.2);
    enemy.max_health = enemy.health;
    enemy.speed = enemy.type.base_speed * (1 + wave_number * 0.1);
    enemy.reward = enemy.type.base_reward + wave_number * 2;
    enemy.path_position = 0;
    enemy.x = path[0].x;
    enemy.y = path[0].y;
    enemy.alive = true;
    return enemy;
}

function selectEnemyType(wave_number) {
    // Different enemy types based on wave progression
    if (wave_number < 3) {
        // Basic enemies
        type = {};
        type.name = "Scout";
        type.base_health = 40;
        type.base_speed = 1.2;
        type.base_reward = 8;
        return type;
    } else if (wave_number < 6) {
        // Stronger enemies
        if (random.randomFloat(0, 1) < 0.3) {
            type = {};
            type.name = "Tank";
            type.base_health = 120;
            type.base_speed = 0.8;
            type.base_reward = 20;
            return type;
        } else {
            type = {};
            type.name = "Runner";
            type.base_health = 30;
            type.base_speed = 2.0;
            type.base_reward = 12;
            return type;
        }
    } else {
        // Boss-like enemies
        if (random.randomFloat(0, 1) < 0.2) {
            type = {};
            type.name = "Boss";
            type.base_health = 300;
            type.base_speed = 0.6;
            type.base_reward = 50;
            return type;
        } else {
            type = {};
            type.name = "Elite";
            type.base_health = 80;
            type.base_speed = 1.5;
            type.base_reward = 25;
            return type;
        }
    }
}

// Tower creation and management
function createTower(tower_type, x, y) {
    tower = {};
    tower.type = tower_type;
    tower.x = x;
    tower.y = y;
    tower.damage = tower_type.damage;
    tower.range = tower_type.range;
    tower.fire_rate = tower_type.fire_rate;
    tower.last_shot = 0;
    tower.level = 1;
    tower.total_damage = 0;
    tower.kills = 0;
    return tower;
}

// Combat system
function createProjectile(tower, target_enemy) {
    projectile = {};
    projectile.start_x = tower.x;
    projectile.start_y = tower.y;
    projectile.target_x = target_enemy.x;
    projectile.target_y = target_enemy.y;
    projectile.damage = tower.damage;
    projectile.speed = 5.0;
    projectile.travel_time = 0;
    projectile.active = true;
    projectile.tower_type = tower.type.name;
    return projectile;
}

function calculateDistance(x1, y1, x2, y2) {
    dx = x1 - x2;
    dy = y1 - y2;
    return math.sqrt(dx * dx + dy * dy);
}

// Main game loop
function gameStep(state, time_delta) {
    state.game_time = state.game_time + time_delta;

    // Check for game over conditions
    if (state.lives <= 0) {
        state.game_over = true;
        return state;
    }

    if (state.current_wave >= state.config.wave_count && collections.length(state.enemies) == 0) {
        state.victory = true;
        state.game_over = true;
        return state;
    }

    // Wave management
    state = updateWaves(state, time_delta);

    // Update enemies
    state = updateEnemies(state, time_delta);

    // Update towers and combat
    state = updateTowers(state, time_delta);

    // Update projectiles
    state = updateProjectiles(state, time_delta);

    return state;
}

function updateWaves(state, time_delta) {
    state.wave_timer = state.wave_timer + time_delta;

    // Start new wave every 15 seconds if current wave is clear
    if (state.wave_timer > 15 && collections.length(state.enemies) == 0 && state.current_wave < state.config.wave_count) {
        state.current_wave = state.current_wave + 1;
        state.wave_timer = 0;

        // Spawn enemies for this wave
        enemy_count = 5 + state.current_wave * 2;
        spawn_delay = 1.0;

        i = 0;
        while (i < enemy_count) {
            enemy = createEnemy(state.current_wave, state.path);
            // Stagger enemy spawning
            enemy.spawn_delay = i * spawn_delay;
            state.enemies = collections.append(state.enemies, enemy);
            i = i + 1;
        }

        print("Wave " + state.current_wave + " spawned with " + enemy_count + " enemies!");
    }

    return state;
}

function updateEnemies(state, time_delta) {
    updated_enemies = [];

    enemies_length = collections.length(state.enemies);
    i = 0;
    while (i < enemies_length) {
        enemy = state.enemies[i];

        // Check spawn delay
        if (enemy.spawn_delay > 0) {
            enemy.spawn_delay = enemy.spawn_delay - time_delta;
            updated_enemies = collections.append(updated_enemies, enemy);
            i = i + 1;
            continue;
        }

        // Move enemy along path
        if (enemy.alive && enemy.path_position < collections.length(state.path) - 1) {
            enemy.path_position = enemy.path_position + enemy.speed * time_delta;
            path_index = math.floor(enemy.path_position);

            if (path_index < collections.length(state.path)) {
                current_pos = state.path[path_index];
                enemy.x = current_pos.x;
                enemy.y = current_pos.y;
                updated_enemies = collections.append(updated_enemies, enemy);
            } else {
                // Enemy reached end - lose life
                state.lives = state.lives - 1;
                print("Enemy escaped! Lives remaining: " + state.lives);
            }
        } else if (enemy.alive) {
            updated_enemies = collections.append(updated_enemies, enemy);
        } else {
            // Enemy died - award gold and score
            state.gold = state.gold + enemy.reward;
            state.score = state.score + enemy.reward;
        }

        i = i + 1;
    }

    state.enemies = updated_enemies;
    return state;
}

function updateTowers(state, time_delta) {
    towers_length = collections.length(state.towers);
    i = 0;
    while (i < towers_length) {
        tower = state.towers[i];
        tower.last_shot = tower.last_shot + time_delta;

        // Check if tower can fire
        if (tower.last_shot >= 1.0 / tower.fire_rate) {
            target = findEnemyInRange(tower, state.enemies);

            if (target != null) {
                projectile = createProjectile(tower, target);
                state.projectiles = collections.append(state.projectiles, projectile);
                tower.last_shot = 0;
            }
        }

        i = i + 1;
    }

    return state;
}

function findEnemyInRange(tower, enemies) {
    enemies_length = collections.length(enemies);
    i = 0;
    while (i < enemies_length) {
        enemy = enemies[i];

        if (enemy.alive && enemy.spawn_delay <= 0) {
            distance = calculateDistance(tower.x, tower.y, enemy.x, enemy.y);
            if (distance <= tower.range) {
                return enemy;
            }
        }

        i = i + 1;
    }

    return null;
}

function updateProjectiles(state, time_delta) {
    updated_projectiles = [];

    projectiles_length = collections.length(state.projectiles);
    i = 0;
    while (i < projectiles_length) {
        projectile = state.projectiles[i];

        if (projectile.active) {
            projectile.travel_time = projectile.travel_time + time_delta;

            // Simple projectile hit after short delay
            if (projectile.travel_time > 0.2) {
                // Find enemy to damage
                target = findNearestEnemy(projectile.target_x, projectile.target_y, state.enemies);

                if (target != null) {
                    target.health = target.health - projectile.damage;

                    if (target.health <= 0) {
                        target.alive = false;
                    }
                }

                projectile.active = false;
            } else {
                updated_projectiles = collections.append(updated_projectiles, projectile);
            }
        }

        i = i + 1;
    }

    state.projectiles = updated_projectiles;
    return state;
}

function findNearestEnemy(x, y, enemies) {
    nearest = null;
    nearest_distance = 999;

    enemies_length = collections.length(enemies);
    i = 0;
    while (i < enemies_length) {
        enemy = enemies[i];

        if (enemy.alive) {
            distance = calculateDistance(x, y, enemy.x, enemy.y);
            if (distance < nearest_distance) {
                nearest = enemy;
                nearest_distance = distance;
            }
        }

        i = i + 1;
    }

    return nearest;
}

// Player actions
function buildTower(state, tower_type_index, x, y) {
    tower_type = state.tower_types[tower_type_index];

    // Check if player has enough gold
    if (state.gold < tower_type.cost) {
        print("Not enough gold! Need " + tower_type.cost + ", have " + state.gold);
        return state;
    }

    // Check if position is valid (not on path, not occupied)
    if (!isValidBuildLocation(state, x, y)) {
        print("Cannot build here!");
        return state;
    }

    // Build tower
    tower = createTower(tower_type, x, y);
    state.towers = collections.append(state.towers, tower);
    state.gold = state.gold - tower_type.cost;

    print("Built " + tower_type.name + " at (" + x + ", " + y + ")");
    return state;
}

function isValidBuildLocation(state, x, y) {
    // Check bounds
    if (x < 0 || x >= state.config.board_width || y < 0 || y >= state.config.board_height) {
        return false;
    }

    // Check if on path
    path_length = collections.length(state.path);
    i = 0;
    while (i < path_length) {
        pos = state.path[i];
        if (pos.x == x && pos.y == y) {
            return false;
        }
        i = i + 1;
    }

    // Check if tower already exists here
    towers_length = collections.length(state.towers);
    i = 0;
    while (i < towers_length) {
        tower = state.towers[i];
        if (tower.x == x && tower.y == y) {
            return false;
        }
        i = i + 1;
    }

    return true;
}

// Game display and status
function displayGameStatus(state) {
    print("=== Tower Defense Game ===");
    print("Gold: " + state.gold + " | Lives: " + state.lives + " | Score: " + state.score);
    print("Wave: " + state.current_wave + "/" + state.config.wave_count);
    print("Enemies: " + collections.length(state.enemies) + " | Towers: " + collections.length(state.towers));

    if (state.game_over) {
        if (state.victory) {
            print("*** VICTORY! You defended successfully! ***");
        } else {
            print("*** GAME OVER - Base destroyed! ***");
        }
    }

    print("");
}

function displayTowerOptions(state) {
    print("Available Towers:");
    types_length = collections.length(state.tower_types);
    i = 0;
    while (i < types_length) {
        tower_type = state.tower_types[i];
        print(i + ": " + tower_type.name + " - Cost: " + tower_type.cost +
              " | Damage: " + tower_type.damage + " | Range: " + tower_type.range);
        i = i + 1;
    }
    print("");
}

// AI Strategy Helper (simple automated play for demo)
function autoPlay(state, time_delta) {
    // Simple AI: build towers at strategic locations when we have enough gold
    if (state.gold >= 60 && collections.length(state.towers) < 8) {
        // Try to build towers near the path
        path_length = collections.length(state.path);
        build_x = -1;
        build_y = -1;

        // Look for good positions near middle of path
        mid_path = math.floor(path_length / 2);
        center_pos = state.path[mid_path];

        // Try positions around the center
        offsets = [-2, -1, 1, 2];
        offset_length = collections.length(offsets);

        i = 0;
        while (i < offset_length && build_x == -1) {
            j = 0;
            while (j < offset_length && build_x == -1) {
                test_x = center_pos.x + offsets[i];
                test_y = center_pos.y + offsets[j];

                if (isValidBuildLocation(state, test_x, test_y)) {
                    build_x = test_x;
                    build_y = test_y;
                }

                j = j + 1;
            }
            i = i + 1;
        }

        // Build tower if we found a spot
        if (build_x != -1) {
            tower_type = 1; // Sniper tower for demo
            if (state.gold < 60) {
                tower_type = 0; // Basic tower
            }
            state = buildTower(state, tower_type, build_x, build_y);
        }
    }

    return state;
}

// Main game runner
function runTowerDefenseGame() {
    print("Starting Tower Defense Game!");
    print("=============================");

    random.setSeed(42);
    config = createGameConfig();
    state = createGameState(config);

    print("Game initialized!");
    print("Board size: " + config.board_width + "x" + config.board_height);
    print("Path length: " + collections.length(state.path));
    print("");

    displayTowerOptions(state);

    // Game simulation loop
    simulation_time = 0;
    time_delta = 0.5; // Half-second steps
    max_simulation_time = 180; // 3 minutes max

    while (!state.game_over && simulation_time < max_simulation_time) {
        state = gameStep(state, time_delta);
        state = autoPlay(state, time_delta); // AI plays automatically for demo

        simulation_time = simulation_time + time_delta;

        // Display status every 10 seconds
        if (math.floor(simulation_time) % 10 == 0 && math.floor(simulation_time) != math.floor(simulation_time - time_delta)) {
            displayGameStatus(state);
        }
    }

    // Final game status
    displayGameStatus(state);

    // Game statistics
    print("=== Final Statistics ===");
    print("Total game time: " + math.floor(simulation_time) + " seconds");
    print("Waves completed: " + state.current_wave + "/" + state.config.wave_count);
    print("Towers built: " + collections.length(state.towers));
    print("Final gold: " + state.gold);
    print("Final score: " + state.score);

    if (state.victory) {
        return 1; // Success
    } else {
        return 0; // Defeat
    }
}

// Entry point
function main() {
    print("Tower Defense Strategy Game - Advanced ML Demo");
    print("==============================================");

    result = runTowerDefenseGame();

    if (result == 1) {
        print("\nCongratulations on defending your base!");
    } else {
        print("\nBetter luck next time, commander!");
    }

    return result;
}