// Species Definitions and Behaviors
// Demonstrates object-oriented patterns and behavioral modeling in ML
// Using only currently implemented ML language features

import math;

// Utility functions for distance calculations
function calculateDistance(pos1, pos2) {
    dx = pos1.x - pos2.x;
    dy = pos1.y - pos2.y;
    return math.sqrt(dx * dx + dy * dy);
}

function normalizeVector(x, y) {
    magnitude = math.sqrt(x * x + y * y);
    if (magnitude == 0) {
        result = {};
        result.x = 0;
        result.y = 0;
        return result;
    }

    normalized = {};
    normalized.x = x / magnitude;
    normalized.y = y / magnitude;
    return normalized;
}

// Prey factory and behavior functions
function createPrey(position, energy, speed, reproduction_rate, detection_range) {
    prey = {};
    prey.position = position;
    prey.energy = energy;
    prey.speed = speed;
    prey.detection_range = detection_range;
    prey.reproduction_rate = reproduction_rate;
    prey.state = "grazing";
    prey.age = 0;
    prey.last_reproduction = 0;
    prey.fear_level = 0;
    return prey;
}

// Prey food seeking behavior
function preyFindFood(prey, environment) {
    // Find nearby resources
    nearby_resources = [];
    resource_count = 0;

    i = 0;
    while (i < getResourceCount(environment)) {
        resource = getResourceAt(environment, i);
        distance = calculateDistance(prey.position, resource.position);

        if (distance <= prey.detection_range && resource.amount > 0) {
            nearby_resources[resource_count] = resource;
            resource_count = resource_count + 1;
        }
        i = i + 1;
    }

    updated_prey = copyPrey(prey);

    if (resource_count > 0) {
        // Find closest resource
        closest = nearby_resources[0];
        closest_distance = calculateDistance(prey.position, closest.position);

        j = 1;
        while (j < resource_count) {
            current_distance = calculateDistance(prey.position, nearby_resources[j].position);
            if (current_distance < closest_distance) {
                closest = nearby_resources[j];
                closest_distance = current_distance;
            }
            j = j + 1;
        }

        updated_prey.state = "grazing";
        updated_prey.fear_level = math.max(0, updated_prey.fear_level - 0.1);
    } else {
        updated_prey.state = "resting";
        updated_prey.fear_level = math.max(0, updated_prey.fear_level - 0.05);
    }

    return updated_prey;
}

// Prey predator avoidance behavior
function preyAvoidPredators(prey, predators) {
    // Detect nearby predators
    nearby_predators = [];
    predator_count = 0;

    i = 0;
    while (i < getArrayLength(predators)) {
        predator = predators[i];
        distance = calculateDistance(prey.position, predator.position);

        if (distance <= prey.detection_range) {
            nearby_predators[predator_count] = predator;
            predator_count = predator_count + 1;
        }
        i = i + 1;
    }

    updated_prey = copyPrey(prey);

    if (predator_count == 0) {
        return updated_prey;
    }

    // Calculate escape vector
    escape_x = 0;
    escape_y = 0;

    i = 0;
    while (i < predator_count) {
        predator = nearby_predators[i];
        distance = calculateDistance(prey.position, predator.position);
        weight = prey.detection_range / (distance + 1);

        escape_x = escape_x + (prey.position.x - predator.position.x) * weight;
        escape_y = escape_y + (prey.position.y - predator.position.y) * weight;
        i = i + 1;
    }

    // Calculate fear level
    max_fear = 0;
    i = 0;
    while (i < predator_count) {
        predator = nearby_predators[i];
        distance = calculateDistance(prey.position, predator.position);
        fear_contribution = 1.0 - (distance / prey.detection_range);
        if (fear_contribution > max_fear) {
            max_fear = fear_contribution;
        }
        i = i + 1;
    }

    updated_prey.state = "fleeing";
    updated_prey.fear_level = math.min(1.0, updated_prey.fear_level + max_fear);

    return updated_prey;
}

// Prey movement based on state
function preyMove(prey, time_step) {
    new_position = {};
    new_position.x = prey.position.x;
    new_position.y = prey.position.y;

    movement_speed = 0;
    direction_x = 0;
    direction_y = 0;

    if (prey.state == "grazing") {
        // Slow, energy-conserving movement
        movement_speed = prey.speed * 0.3;
        angle = math.random() * 2 * math.pi;
        direction_x = math.cos(angle);
        direction_y = math.sin(angle);
    } else if (prey.state == "fleeing") {
        // Fast, energy-intensive movement
        movement_speed = prey.speed * (1.0 + prey.fear_level);
        angle = math.random() * 2 * math.pi;
        direction_x = math.cos(angle);
        direction_y = math.sin(angle);
    } else if (prey.state == "resting") {
        // Minimal movement
        movement_speed = 0;
    } else {
        // Default movement
        movement_speed = prey.speed * 0.5;
        angle = math.random() * 2 * math.pi;
        direction_x = math.cos(angle);
        direction_y = math.sin(angle);
    }

    new_position.x = new_position.x + direction_x * movement_speed * time_step;
    new_position.y = new_position.y + direction_y * movement_speed * time_step;

    updated_prey = copyPrey(prey);
    updated_prey.position = new_position;
    return updated_prey;
}

// Prey energy management
function preyUpdateEnergy(prey, time_step) {
    energy_cost = 1.5; // Default cost

    if (prey.state == "grazing") {
        energy_cost = 1.0;
    } else if (prey.state == "fleeing") {
        energy_cost = 3.0 * (1.0 + prey.fear_level);
    } else if (prey.state == "resting") {
        energy_cost = 0.3;
    }

    new_energy = prey.energy - energy_cost * time_step;
    new_age = prey.age + time_step;

    updated_prey = copyPrey(prey);
    updated_prey.energy = math.max(0, new_energy);
    updated_prey.age = new_age;

    return updated_prey;
}

// Prey reproduction
function preyTryReproduce(prey, time_step) {
    time_since_last = prey.age - prey.last_reproduction;
    energy_threshold = 80;
    age_threshold = 10;

    if (prey.energy < energy_threshold ||
        prey.age < age_threshold ||
        time_since_last < (1.0 / prey.reproduction_rate)) {
        return null;
    }

    // Create offspring position
    offspring_pos = {};
    offspring_pos.x = prey.position.x + (math.random() - 0.5) * 10;
    offspring_pos.y = prey.position.y + (math.random() - 0.5) * 10;

    offspring = createPrey(
        offspring_pos,
        30 + math.random() * 20,
        prey.speed * (0.8 + math.random() * 0.4),
        prey.reproduction_rate * (0.9 + math.random() * 0.2),
        prey.detection_range * (0.9 + math.random() * 0.2)
    );

    return offspring;
}

// Predator factory and behavior functions
function createPredator(position, energy, speed, hunting_efficiency, detection_range) {
    predator = {};
    predator.position = position;
    predator.energy = energy;
    predator.speed = speed;
    predator.detection_range = detection_range;
    predator.hunting_efficiency = hunting_efficiency;
    predator.state = "patrolling";
    predator.age = 0;
    predator.last_meal = 0;
    predator.target = null;
    return predator;
}

// Process predator behavior by state
function processPredatorByState(predator, prey_population, time_step) {
    if (predator.state == "hunting") {
        return predatorHunt(predator, prey_population, time_step);
    } else if (predator.state == "feeding") {
        return predatorFeed(predator, time_step);
    } else if (predator.state == "resting") {
        return predatorRest(predator, time_step);
    } else {
        return predatorPatrol(predator, time_step);
    }
}

// Predator hunting behavior
function predatorHunt(predator, prey_population, time_step) {
    // Find prey within detection range
    potential_targets = [];
    target_count = 0;

    i = 0;
    while (i < getArrayLength(prey_population)) {
        prey_individual = prey_population[i];
        distance = calculateDistance(predator.position, prey_individual.position);

        if (distance <= predator.detection_range) {
            potential_targets[target_count] = prey_individual;
            target_count = target_count + 1;
        }
        i = i + 1;
    }

    updated_predator = copyPredator(predator);

    if (target_count == 0) {
        updated_predator.state = "patrolling";
        updated_predator.target = null;
        return updated_predator;
    }

    // Select best target (closest and weakest)
    best_target = potential_targets[0];
    best_score = calculateHuntingScore(predator, best_target);

    i = 1;
    while (i < target_count) {
        current_target = potential_targets[i];
        current_score = calculateHuntingScore(predator, current_target);

        if (current_score > best_score) {
            best_target = current_target;
            best_score = current_score;
        }
        i = i + 1;
    }

    // Calculate hunting success
    distance_to_target = calculateDistance(predator.position, best_target.position);
    hunt_success_chance = predator.hunting_efficiency * (1.0 - distance_to_target / predator.detection_range);

    if (math.random() < hunt_success_chance && distance_to_target < 5) {
        // Successful hunt
        energy_gained = math.min(best_target.energy * 0.8, 50);
        updated_predator.state = "feeding";
        updated_predator.energy = updated_predator.energy + energy_gained;
        updated_predator.last_meal = updated_predator.age;
        updated_predator.target = null;
    } else {
        // Continue hunting
        updated_predator.state = "hunting";
        updated_predator.target = best_target;
    }

    return updated_predator;
}

// Calculate hunting score for target selection
function calculateHuntingScore(predator, prey) {
    distance = calculateDistance(predator.position, prey.position);
    distance_score = 1.0 / (distance + 1);
    weakness_score = 1.0 / (prey.energy + 1);
    return distance_score * weakness_score;
}

// Predator feeding behavior
function predatorFeed(predator, time_step) {
    feeding_time = 5;

    updated_predator = copyPredator(predator);

    if (predator.age - predator.last_meal < feeding_time) {
        // Still feeding
        updated_predator.energy = updated_predator.energy + 2 * time_step;
    } else {
        // Finished feeding
        updated_predator.state = "patrolling";
    }

    return updated_predator;
}

// Predator resting behavior
function predatorRest(predator, time_step) {
    updated_predator = copyPredator(predator);

    if (predator.energy > 60) {
        updated_predator.state = "patrolling";
    } else {
        updated_predator.energy = updated_predator.energy + 0.5 * time_step;
    }

    return updated_predator;
}

// Predator patrolling behavior
function predatorPatrol(predator, time_step) {
    angle = math.random() * 2 * math.pi;
    movement_speed = predator.speed * 0.6;

    new_position = {};
    new_position.x = predator.position.x + math.cos(angle) * movement_speed * time_step;
    new_position.y = predator.position.y + math.sin(angle) * movement_speed * time_step;

    updated_predator = copyPredator(predator);
    updated_predator.position = new_position;
    updated_predator.state = "patrolling";

    return updated_predator;
}

// Predator energy management
function predatorUpdateEnergy(predator, time_step) {
    energy_cost = 1.5; // Default

    if (predator.state == "hunting") {
        energy_cost = 2.5;
    } else if (predator.state == "feeding") {
        energy_cost = 0.5;
    } else if (predator.state == "resting") {
        energy_cost = 0.2;
    } else if (predator.state == "patrolling") {
        energy_cost = 1.0;
    }

    new_energy = predator.energy - energy_cost * time_step;
    new_age = predator.age + time_step;

    updated_predator = copyPredator(predator);
    updated_predator.energy = math.max(0, new_energy);
    updated_predator.age = new_age;

    // Switch to resting if energy is critically low
    if (new_energy < 30 && predator.state != "feeding") {
        updated_predator.state = "resting";
    }

    return updated_predator;
}

// Helper functions for copying objects (since ML doesn't have spread operator)
function copyPrey(prey) {
    copy = {};
    copy.position = copyPosition(prey.position);
    copy.energy = prey.energy;
    copy.speed = prey.speed;
    copy.detection_range = prey.detection_range;
    copy.reproduction_rate = prey.reproduction_rate;
    copy.state = prey.state;
    copy.age = prey.age;
    copy.last_reproduction = prey.last_reproduction;
    copy.fear_level = prey.fear_level;
    return copy;
}

function copyPredator(predator) {
    copy = {};
    copy.position = copyPosition(predator.position);
    copy.energy = predator.energy;
    copy.speed = predator.speed;
    copy.detection_range = predator.detection_range;
    copy.hunting_efficiency = predator.hunting_efficiency;
    copy.state = predator.state;
    copy.age = predator.age;
    copy.last_meal = predator.last_meal;
    copy.target = predator.target;
    return copy;
}

function copyPosition(position) {
    copy = {};
    copy.x = position.x;
    copy.y = position.y;
    return copy;
}

// Helper function to get array length (referenced in main.ml)
function getArrayLength(arr) {
    length = 0;
    i = 0;

    while (i >= 0) {
        if (arr[i] != null) {
            length = length + 1;
            i = i + 1;
        } else {
            return length;
        }
    }
    return length;
}