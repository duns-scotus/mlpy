// Ecosystem Simulation - Predator-Prey Dynamics
// Demonstrates ML's object-oriented patterns, state management, and functional programming
// Using only currently implemented ML language features and proper standard library

import collections;
import random;
import math;

// Simulation configuration factory
function createSimulationConfig(duration, time_step, initial_predators, initial_prey, environment_size, resource_capacity) {
    config = {};
    config.duration = duration;
    config.time_step = time_step;
    config.initial_predators = initial_predators;
    config.initial_prey = initial_prey;
    config.environment_size = environment_size;
    config.resource_capacity = resource_capacity;
    return config;
}

// Main simulation state management
function createSimulation(config) {
    simulation = {};
    simulation.config = config;
    simulation.environment = createEnvironment(config.environment_size, config.resource_capacity);
    simulation.predators = createPredatorPopulation(config.initial_predators, config.environment_size);
    simulation.prey = createPreyPopulation(config.initial_prey, config.environment_size);
    simulation.current_time = 0;
    simulation.statistics = createStatistics();
    return simulation;
}

// Create predator population with diversity
function createPredatorPopulation(count, environment_size) {
    predators = [];

    i = 0;
    while (i < count) {
        position = createRandomPosition(environment_size);
        energy = 100 + random.randomFloat(0, 50);  // energy 100-150
        speed = 1.2 + random.randomFloat(0, 0.6);  // speed 1.2-1.8
        hunting_efficiency = 0.3 + random.randomFloat(0, 0.2); // efficiency 0.3-0.5
        detection_range = 25 + random.randomFloat(0, 15);      // range 25-40

        predator = createPredator(position, energy, speed, hunting_efficiency, detection_range);
        predators = collections.append(predators, predator);
        i = i + 1;
    }

    return predators;
}

// Create prey population with diversity
function createPreyPopulation(count, environment_size) {
    prey = [];

    i = 0;
    while (i < count) {
        position = createRandomPosition(environment_size);
        energy = 50 + random.randomFloat(0, 30);       // energy 50-80
        speed = 0.8 + random.randomFloat(0, 0.4);      // speed 0.8-1.2
        reproduction_rate = 0.02 + random.randomFloat(0, 0.01); // rate 0.02-0.03
        detection_range = 15 + random.randomFloat(0, 10);       // range 15-25

        individual = createPrey(position, energy, speed, reproduction_rate, detection_range);
        prey = collections.append(prey, individual);
        i = i + 1;
    }

    return prey;
}

// Generate random position within bounds
function createRandomPosition(environment_size) {
    pos = {};
    pos.x = random.randomFloat(0, environment_size);
    pos.y = random.randomFloat(0, environment_size);
    return pos;
}

// Core simulation step
function simulationStep(sim) {
    // Update environment
    updated_environment = updateEnvironment(sim.environment, sim.config.time_step);

    // Process prey behavior
    updated_prey = processPreyBehavior(sim.prey, sim.predators, updated_environment, sim.config.time_step);

    // Handle prey reproduction
    new_prey = handlePreyReproduction(updated_prey, sim.config.time_step);
    all_prey = collections.concat(updated_prey, new_prey);

    // Process predator behavior
    updated_predators = processPredatorBehavior(sim.predators, all_prey, sim.config.time_step);

    // Collect statistics
    stats_data = createStatsData(
        sim.current_time,
        collections.length(updated_predators),
        collections.length(all_prey),
        calculateAverageEnergy(updated_predators),
        calculateAverageEnergy(all_prey),
        getTotalResources(updated_environment)
    );
    updated_statistics = recordDataPoint(sim.statistics, stats_data);

    // Create updated simulation state
    new_sim = {};
    new_sim.config = sim.config;
    new_sim.environment = updated_environment;
    new_sim.predators = updated_predators;
    new_sim.prey = all_prey;
    new_sim.current_time = sim.current_time + sim.config.time_step;
    new_sim.statistics = updated_statistics;

    return new_sim;
}

// Process all prey behavior using functional approach
function processPreyBehavior(prey_population, predator_population, environment, time_step) {
    // Filter alive prey and process their behavior
    alive_prey = collections.filter(prey_population, function(prey) {
        return prey.energy > 0;
    });

    // Transform each prey through behavior pipeline
    processed_prey = collections.map(alive_prey, function(prey_individual) {
        // Behavior pipeline: find food -> avoid predators -> move -> update energy
        prey_with_food = preyFindFood(prey_individual, environment);
        prey_avoiding = preyAvoidPredators(prey_with_food, predator_population);
        prey_moved = preyMove(prey_avoiding, time_step);
        prey_updated = preyUpdateEnergy(prey_moved, time_step);

        return prey_updated;
    });

    // Return only still-alive prey
    return collections.filter(processed_prey, function(prey) {
        return prey.energy > 0;
    });
}

// Handle prey reproduction
function handlePreyReproduction(prey_population, time_step) {
    offspring = [];

    len = collections.length(prey_population);
    i = 0;
    while (i < len) {
        prey_individual = prey_population[i];
        new_offspring = preyTryReproduce(prey_individual, time_step);

        if (new_offspring != null) {
            offspring = collections.append(offspring, new_offspring);
        }

        i = i + 1;
    }

    return offspring;
}

// Process predator behavior
function processPredatorBehavior(predator_population, prey_population, time_step) {
    // Filter alive predators and process their behavior
    alive_predators = collections.filter(predator_population, function(predator) {
        return predator.energy > 0;
    });

    // Transform each predator through behavior pipeline
    processed_predators = collections.map(alive_predators, function(predator) {
        // Process behavior by state -> update energy
        updated_predator = processPredatorByState(predator, prey_population, time_step);
        energy_updated = predatorUpdateEnergy(updated_predator, time_step);

        return energy_updated;
    });

    // Return only still-alive predators
    return collections.filter(processed_predators, function(predator) {
        return predator.energy > 0;
    });
}

// Calculate average energy of a population
function calculateAverageEnergy(population) {
    len = collections.length(population);
    if (len == 0) {
        return 0;
    }

    total_energy = collections.reduce(population, function(sum, individual) {
        return sum + individual.energy;
    }, 0);

    return total_energy / len;
}

// Main simulation runner
function runSimulation(config) {
    print("Starting ecosystem simulation...");
    print("Initial conditions:");
    print("  Predators: " + config.initial_predators);
    print("  Prey: " + config.initial_prey);
    print("  Duration: " + config.duration + " time units");
    print("  Environment size: " + config.environment_size);

    // Initialize simulation
    simulation = createSimulation(config);

    // Run simulation loop
    step_count = 0;
    max_steps = config.duration / config.time_step;

    while (step_count < max_steps) {
        // Update simulation state
        simulation = simulationStep(simulation);
        step_count = step_count + 1;

        // Progress reporting
        if (step_count % 100 == 0) {
            progress = step_count / max_steps * 100;
            predator_count = collections.length(simulation.predators);
            prey_count = collections.length(simulation.prey);

            print("Progress: " + progress + "% (Time: " + simulation.current_time + ")");
            print("  Populations - Predators: " + predator_count + ", Prey: " + prey_count);
        }

        // Check for extinction events
        predator_count = collections.length(simulation.predators);
        prey_count = collections.length(simulation.prey);

        if (predator_count == 0 && prey_count == 0) {
            print("Simulation ended: Complete extinction at time " + simulation.current_time);
            return true;
        }

        if (predator_count == 0) {
            print("Simulation note: Predators extinct at time " + simulation.current_time);
        }

        if (prey_count == 0) {
            print("Simulation note: Prey extinct at time " + simulation.current_time);
        }
    }

    // Generate final report
    print("");
    print("Simulation completed!");
    print("Final populations:");
    print("  Predators: " + collections.length(simulation.predators));
    print("  Prey: " + collections.length(simulation.prey));

    return true;
}

// Example usage with different scenarios
function runExampleScenarios() {
    // Scenario 1: Balanced ecosystem
    balanced_config = createSimulationConfig(500, 0.1, 10, 50, 200, 500);

    print("Running balanced ecosystem scenario...");
    success1 = runSimulation(balanced_config);

    // Scenario 2: Predator-heavy ecosystem
    predator_heavy_config = createSimulationConfig(500, 0.1, 20, 40, 150, 400);

    print("");
    print("Running predator-heavy ecosystem scenario...");
    success2 = runSimulation(predator_heavy_config);

    return success1 && success2;
}

// Entry point
function main() {
    print("Ecosystem Simulation - Advanced ML Demo");
    print("=====================================");

    // Set random seed for reproducible results
    random.setSeed(42);

    success = runExampleScenarios();

    if (success) {
        print("");
        print("All scenarios completed successfully!");
        return 0;
    } else {
        print("");
        print("Some scenarios failed to complete");
        return 1;
    }
}

// Placeholder functions for environment, species, and statistics
// These would be implemented in separate modules

function createEnvironment(size, capacity) {
    env = {};
    env.size = size;
    env.resources = createResourceList(capacity);
    return env;
}

function createResourceList(capacity) {
    // Simplified resource creation
    resources = [];
    resource_count = 10; // Fixed number of resources for simplicity

    i = 0;
    while (i < resource_count) {
        resource = {};
        resource.position = createRandomPosition(100); // Simplified
        resource.amount = capacity / resource_count;
        resources = collections.append(resources, resource);
        i = i + 1;
    }

    return resources;
}

function updateEnvironment(environment, time_step) {
    // Simplified environment update
    return environment;
}

function getTotalResources(environment) {
    return collections.reduce(environment.resources, function(sum, resource) {
        return sum + resource.amount;
    }, 0);
}

function createPrey(position, energy, speed, reproduction_rate, detection_range) {
    prey = {};
    prey.position = position;
    prey.energy = energy;
    prey.speed = speed;
    prey.reproduction_rate = reproduction_rate;
    prey.detection_range = detection_range;
    prey.state = "grazing";
    prey.age = 0;
    prey.last_reproduction = 0;
    prey.fear_level = 0;
    return prey;
}

function createPredator(position, energy, speed, hunting_efficiency, detection_range) {
    predator = {};
    predator.position = position;
    predator.energy = energy;
    predator.speed = speed;
    predator.hunting_efficiency = hunting_efficiency;
    predator.detection_range = detection_range;
    predator.state = "patrolling";
    predator.age = 0;
    predator.last_meal = 0;
    predator.target = null;
    return predator;
}

// Simplified behavior functions (placeholder implementations)
function preyFindFood(prey, environment) {
    // Simplified: always find some food
    updated_prey = clonePrey(prey);
    updated_prey.state = "grazing";
    return updated_prey;
}

function preyAvoidPredators(prey, predators) {
    // Check if any predators are nearby
    nearby_predators = collections.filter(predators, function(predator) {
        distance = calculateDistance(prey.position, predator.position);
        return distance <= prey.detection_range;
    });

    updated_prey = clonePrey(prey);

    if (collections.length(nearby_predators) > 0) {
        updated_prey.state = "fleeing";
        updated_prey.fear_level = math.min(1.0, updated_prey.fear_level + 0.3);
    }

    return updated_prey;
}

function preyMove(prey, time_step) {
    new_position = {};
    new_position.x = prey.position.x;
    new_position.y = prey.position.y;

    // Simple random movement
    angle = random.randomFloat(0, 2 * math.pi);
    speed_multiplier = prey.state == "fleeing" ? 2.0 : 1.0;
    distance = prey.speed * speed_multiplier * time_step;

    new_position.x = new_position.x + math.cos(angle) * distance;
    new_position.y = new_position.y + math.sin(angle) * distance;

    updated_prey = clonePrey(prey);
    updated_prey.position = new_position;
    return updated_prey;
}

function preyUpdateEnergy(prey, time_step) {
    energy_cost = prey.state == "fleeing" ? 3.0 : 1.0;
    new_energy = prey.energy - energy_cost * time_step;
    new_age = prey.age + time_step;

    updated_prey = clonePrey(prey);
    updated_prey.energy = math.max(0, new_energy);
    updated_prey.age = new_age;

    return updated_prey;
}

function preyTryReproduce(prey, time_step) {
    if (prey.energy > 60 && prey.age > 20 && random.randomBoolWeighted(prey.reproduction_rate)) {
        offspring_pos = {};
        offspring_pos.x = prey.position.x + random.randomFloat(-5, 5);
        offspring_pos.y = prey.position.y + random.randomFloat(-5, 5);

        return createPrey(offspring_pos, 40, prey.speed, prey.reproduction_rate, prey.detection_range);
    }

    return null;
}

function processPredatorByState(predator, prey_population, time_step) {
    if (predator.state == "hunting") {
        return predatorHunt(predator, prey_population, time_step);
    } else {
        return predatorPatrol(predator, time_step);
    }
}

function predatorHunt(predator, prey_population, time_step) {
    // Find nearby prey
    nearby_prey = collections.filter(prey_population, function(prey) {
        distance = calculateDistance(predator.position, prey.position);
        return distance <= predator.detection_range;
    });

    updated_predator = clonePredator(predator);

    if (collections.length(nearby_prey) > 0 && random.randomBoolWeighted(predator.hunting_efficiency)) {
        // Successful hunt
        updated_predator.energy = updated_predator.energy + 30;
        updated_predator.last_meal = updated_predator.age;
        updated_predator.state = "patrolling";
    }

    return updated_predator;
}

function predatorPatrol(predator, time_step) {
    // Random patrol movement
    angle = random.randomFloat(0, 2 * math.pi);
    distance = predator.speed * time_step;

    new_position = {};
    new_position.x = predator.position.x + math.cos(angle) * distance;
    new_position.y = predator.position.y + math.sin(angle) * distance;

    updated_predator = clonePredator(predator);
    updated_predator.position = new_position;

    // Switch to hunting if hungry
    if (predator.energy < 50) {
        updated_predator.state = "hunting";
    }

    return updated_predator;
}

function predatorUpdateEnergy(predator, time_step) {
    energy_cost = predator.state == "hunting" ? 2.0 : 1.0;
    new_energy = predator.energy - energy_cost * time_step;
    new_age = predator.age + time_step;

    updated_predator = clonePredator(predator);
    updated_predator.energy = math.max(0, new_energy);
    updated_predator.age = new_age;

    return updated_predator;
}

// Utility functions
function calculateDistance(pos1, pos2) {
    dx = pos1.x - pos2.x;
    dy = pos1.y - pos2.y;
    return math.sqrt(dx * dx + dy * dy);
}

function clonePrey(prey) {
    clone = {};
    clone.position = clonePosition(prey.position);
    clone.energy = prey.energy;
    clone.speed = prey.speed;
    clone.reproduction_rate = prey.reproduction_rate;
    clone.detection_range = prey.detection_range;
    clone.state = prey.state;
    clone.age = prey.age;
    clone.last_reproduction = prey.last_reproduction;
    clone.fear_level = prey.fear_level;
    return clone;
}

function clonePredator(predator) {
    clone = {};
    clone.position = clonePosition(predator.position);
    clone.energy = predator.energy;
    clone.speed = predator.speed;
    clone.hunting_efficiency = predator.hunting_efficiency;
    clone.detection_range = predator.detection_range;
    clone.state = predator.state;
    clone.age = predator.age;
    clone.last_meal = predator.last_meal;
    clone.target = predator.target;
    return clone;
}

function clonePosition(pos) {
    clone = {};
    clone.x = pos.x;
    clone.y = pos.y;
    return clone;
}

function createStatistics() {
    stats = {};
    stats.data_points = [];
    return stats;
}

function createStatsData(time, predator_count, prey_count, avg_predator_energy, avg_prey_energy, resources) {
    data = {};
    data.time = time;
    data.predator_count = predator_count;
    data.prey_count = prey_count;
    data.avg_predator_energy = avg_predator_energy;
    data.avg_prey_energy = avg_prey_energy;
    data.resources = resources;
    return data;
}

function recordDataPoint(stats, data) {
    updated_stats = {};
    updated_stats.data_points = collections.append(stats.data_points, data);
    return updated_stats;
}

// Run the simulation
exit_code = main();