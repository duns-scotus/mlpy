"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib import console, getCurrentTime, processData

from mlpy.stdlib.collections import collections as ml_collections

from mlpy.stdlib.random import random as ml_random

from mlpy.stdlib.math import math as ml_math

def createSimulationConfig(duration, time_step, initial_predators, initial_prey, environment_size, resource_capacity):
    config = {}
    config['duration'] = duration
    config['time_step'] = time_step
    config['initial_predators'] = initial_predators
    config['initial_prey'] = initial_prey
    config['environment_size'] = environment_size
    config['resource_capacity'] = resource_capacity
    return config

def createSimulation(config):
    simulation = {}
    simulation['config'] = config
    simulation['environment'] = createEnvironment(config['environment_size'], config['resource_capacity'])
    simulation['predators'] = createPredatorPopulation(config['initial_predators'], config['environment_size'])
    simulation['prey'] = createPreyPopulation(config['initial_prey'], config['environment_size'])
    simulation['current_time'] = 0
    simulation['statistics'] = createStatistics()
    return simulation

def createPredatorPopulation(count, environment_size):
    predators = []
    i = 0
    while (i < count):
        position = createRandomPosition(environment_size)
        energy = (100 + ml_random.randomFloat(0, 50))
        speed = (1.2 + ml_random.randomFloat(0, 0.6))
        hunting_efficiency = (0.3 + ml_random.randomFloat(0, 0.2))
        detection_range = (25 + ml_random.randomFloat(0, 15))
        predator = createPredator(position, energy, speed, hunting_efficiency, detection_range)
        predators = ml_collections.append(predators, predator)
        i = (i + 1)
    return predators

def createPreyPopulation(count, environment_size):
    prey = []
    i = 0
    while (i < count):
        position = createRandomPosition(environment_size)
        energy = (50 + ml_random.randomFloat(0, 30))
        speed = (0.8 + ml_random.randomFloat(0, 0.4))
        reproduction_rate = (0.02 + ml_random.randomFloat(0, 0.01))
        detection_range = (15 + ml_random.randomFloat(0, 10))
        individual = createPrey(position, energy, speed, reproduction_rate, detection_range)
        prey = ml_collections.append(prey, individual)
        i = (i + 1)
    return prey

def createRandomPosition(environment_size):
    pos = {}
    pos['x'] = ml_random.randomFloat(0, environment_size)
    pos['y'] = ml_random.randomFloat(0, environment_size)
    return pos

def simulationStep(sim):
    updated_environment = updateEnvironment(sim['environment'], sim['config']['time_step'])
    updated_prey = processPreyBehavior(sim['prey'], sim['predators'], updated_environment, sim['config']['time_step'])
    new_prey = handlePreyReproduction(updated_prey, sim['config']['time_step'])
    all_prey = ml_collections.concat(updated_prey, new_prey)
    updated_predators = processPredatorBehavior(sim['predators'], all_prey, sim['config']['time_step'])
    stats_data = createStatsData(sim['current_time'], ml_collections.length(updated_predators), ml_collections.length(all_prey), calculateAverageEnergy(updated_predators), calculateAverageEnergy(all_prey), getTotalResources(updated_environment))
    updated_statistics = recordDataPoint(sim['statistics'], stats_data)
    new_sim = {}
    new_sim['config'] = sim['config']
    new_sim['environment'] = updated_environment
    new_sim['predators'] = updated_predators
    new_sim['prey'] = all_prey
    new_sim['current_time'] = (sim['current_time'] + sim['config']['time_step'])
    new_sim['statistics'] = updated_statistics
    return new_sim

def processPreyBehavior(prey_population, predator_population, environment, time_step):
    alive_prey = ml_collections.filter(prey_population, lambda prey: (prey['energy'] > 0))
    processed_prey = ml_collections.map(alive_prey, lambda prey_individual: preyUpdateEnergy(preyMove(preyAvoidPredators(preyFindFood(prey_individual, environment), predator_population), time_step), time_step))
    return ml_collections.filter(processed_prey, lambda prey: (prey['energy'] > 0))

def handlePreyReproduction(prey_population, time_step):
    offspring = []
    len = ml_collections.length(prey_population)
    i = 0
    while (i < len):
        prey_individual = prey_population[i]
        new_offspring = preyTryReproduce(prey_individual, time_step)
        if (new_offspring != None):
            offspring = ml_collections.append(offspring, new_offspring)
        i = (i + 1)
    return offspring

def processPredatorBehavior(predator_population, prey_population, time_step):
    alive_predators = ml_collections.filter(predator_population, lambda predator: (predator['energy'] > 0))
    processed_predators = ml_collections.map(alive_predators, lambda predator: predatorUpdateEnergy(processPredatorByState(predator, prey_population, time_step), time_step))
    return ml_collections.filter(processed_predators, lambda predator: (predator['energy'] > 0))

def calculateAverageEnergy(population):
    len = ml_collections.length(population)
    if (len == 0):
        return 0
    total_energy = ml_collections.reduce(population, lambda sum, individual: (sum + individual['energy']), 0)
    return (total_energy / len)

def runSimulation(config):
    print('Starting ecosystem simulation...')
    print('Initial conditions:')
    print((str('  Predators: ') + str(config['initial_predators'])))
    print((str('  Prey: ') + str(config['initial_prey'])))
    print((str((str('  Duration: ') + str(config['duration']))) + str(' time units')))
    print((str('  Environment size: ') + str(config['environment_size'])))
    simulation = createSimulation(config)
    step_count = 0
    max_steps = (config['duration'] / config['time_step'])
    while (step_count < max_steps):
        simulation = simulationStep(simulation)
        step_count = (step_count + 1)
        if ((step_count % 100) == 0):
            progress = ((step_count / max_steps) * 100)
            predator_count = ml_collections.length(simulation['predators'])
            prey_count = ml_collections.length(simulation['prey'])
            print((str((str((str((str('Progress: ') + str(progress))) + str('% (Time: '))) + str(simulation['current_time']))) + str(')')))
            print((str((str((str('  Populations - Predators: ') + str(predator_count))) + str(', Prey: '))) + str(prey_count)))
        predator_count = ml_collections.length(simulation['predators'])
        prey_count = ml_collections.length(simulation['prey'])
        if ((predator_count == 0) and (prey_count == 0)):
            print((str('Simulation ended: Complete extinction at time ') + str(simulation['current_time'])))
            return True
        if (predator_count == 0):
            print((str('Simulation note: Predators extinct at time ') + str(simulation['current_time'])))
        if (prey_count == 0):
            print((str('Simulation note: Prey extinct at time ') + str(simulation['current_time'])))
    print('')
    print('Simulation completed!')
    print('Final populations:')
    print((str('  Predators: ') + str(ml_collections.length(simulation['predators']))))
    print((str('  Prey: ') + str(ml_collections.length(simulation['prey']))))
    return True

def runExampleScenarios():
    balanced_config = createSimulationConfig(500, 0.1, 10, 50, 200, 500)
    print('Running balanced ecosystem scenario...')
    success1 = runSimulation(balanced_config)
    predator_heavy_config = createSimulationConfig(500, 0.1, 20, 40, 150, 400)
    print('')
    print('Running predator-heavy ecosystem scenario...')
    success2 = runSimulation(predator_heavy_config)
    return (success1 and success2)

def main():
    print('Ecosystem Simulation - Advanced ML Demo')
    print('=====================================')
    ml_random.setSeed(42)
    success = runExampleScenarios()
    if success:
        print('')
        print('All scenarios completed successfully!')
        return 0
    else:
        print('')
        print('Some scenarios failed to complete')
        return 1

def createEnvironment(size, capacity):
    env = {}
    env['size'] = size
    env['resources'] = createResourceList(capacity)
    return env

def createResourceList(capacity):
    resources = []
    resource_count = 10
    i = 0
    while (i < resource_count):
        resource = {}
        resource['position'] = createRandomPosition(100)
        resource['amount'] = (capacity / resource_count)
        resources = ml_collections.append(resources, resource)
        i = (i + 1)
    return resources

def updateEnvironment(environment, time_step):
    return environment

def getTotalResources(environment):
    return ml_collections.reduce(environment['resources'], lambda sum, resource: (sum + resource['amount']), 0)

def createPrey(position, energy, speed, reproduction_rate, detection_range):
    prey = {}
    prey['position'] = position
    prey['energy'] = energy
    prey['speed'] = speed
    prey['reproduction_rate'] = reproduction_rate
    prey['detection_range'] = detection_range
    prey['state'] = 'grazing'
    prey['age'] = 0
    prey['last_reproduction'] = 0
    prey['fear_level'] = 0
    return prey

def createPredator(position, energy, speed, hunting_efficiency, detection_range):
    predator = {}
    predator['position'] = position
    predator['energy'] = energy
    predator['speed'] = speed
    predator['hunting_efficiency'] = hunting_efficiency
    predator['detection_range'] = detection_range
    predator['state'] = 'patrolling'
    predator['age'] = 0
    predator['last_meal'] = 0
    predator['target'] = None
    return predator

def preyFindFood(prey, environment):
    updated_prey = clonePrey(prey)
    updated_prey['state'] = 'grazing'
    return updated_prey

def preyAvoidPredators(prey, predators):
    nearby_predators = ml_collections.filter(predators, lambda predator: (calculateDistance(prey['position'], predator['position']) <= prey['detection_range']))
    updated_prey = clonePrey(prey)
    if (ml_collections.length(nearby_predators) > 0):
        updated_prey['state'] = 'fleeing'
        updated_prey['fear_level'] = ml_math.min(1.0, (updated_prey['fear_level'] + 0.3))
    return updated_prey

def preyMove(prey, time_step):
    new_position = {}
    new_position['x'] = prey['position']['x']
    new_position['y'] = prey['position']['y']
    angle = ml_random.randomFloat(0, (2 * ml_math.pi))
    speed_multiplier = 2.0 if (prey['state'] == 'fleeing') else 1.0
    distance = ((prey['speed'] * speed_multiplier) * time_step)
    new_position['x'] = (new_position['x'] + (ml_math.cos(angle) * distance))
    new_position['y'] = (new_position['y'] + (ml_math.sin(angle) * distance))
    updated_prey = clonePrey(prey)
    updated_prey['position'] = new_position
    return updated_prey

def preyUpdateEnergy(prey, time_step):
    energy_cost = 3.0 if (prey['state'] == 'fleeing') else 1.0
    new_energy = (prey['energy'] - (energy_cost * time_step))
    new_age = (prey['age'] + time_step)
    updated_prey = clonePrey(prey)
    updated_prey['energy'] = ml_math.max(0, new_energy)
    updated_prey['age'] = new_age
    return updated_prey

def preyTryReproduce(prey, time_step):
    if (((prey['energy'] > 60) and (prey['age'] > 20)) and ml_random.randomBoolWeighted(prey['reproduction_rate'])):
        offspring_pos = {}
        offspring_pos['x'] = (prey['position']['x'] + ml_random.randomFloat(5, 5))
        offspring_pos['y'] = (prey['position']['y'] + ml_random.randomFloat(5, 5))
        return createPrey(offspring_pos, 40, prey['speed'], prey['reproduction_rate'], prey['detection_range'])
    return None

def processPredatorByState(predator, prey_population, time_step):
    if (predator['state'] == 'hunting'):
        return predatorHunt(predator, prey_population, time_step)
    else:
        return predatorPatrol(predator, time_step)

def predatorHunt(predator, prey_population, time_step):
    nearby_prey = ml_collections.filter(prey_population, lambda prey: (calculateDistance(predator['position'], prey['position']) <= predator['detection_range']))
    updated_predator = clonePredator(predator)
    if ((ml_collections.length(nearby_prey) > 0) and ml_random.randomBoolWeighted(predator['hunting_efficiency'])):
        updated_predator['energy'] = (updated_predator['energy'] + 30)
        updated_predator['last_meal'] = updated_predator['age']
        updated_predator['state'] = 'patrolling'
    return updated_predator

def predatorPatrol(predator, time_step):
    angle = ml_random.randomFloat(0, (2 * ml_math.pi))
    distance = (predator['speed'] * time_step)
    new_position = {}
    new_position['x'] = (predator['position']['x'] + (ml_math.cos(angle) * distance))
    new_position['y'] = (predator['position']['y'] + (ml_math.sin(angle) * distance))
    updated_predator = clonePredator(predator)
    updated_predator['position'] = new_position
    if (predator['energy'] < 50):
        updated_predator['state'] = 'hunting'
    return updated_predator

def predatorUpdateEnergy(predator, time_step):
    energy_cost = 2.0 if (predator['state'] == 'hunting') else 1.0
    new_energy = (predator['energy'] - (energy_cost * time_step))
    new_age = (predator['age'] + time_step)
    updated_predator = clonePredator(predator)
    updated_predator['energy'] = ml_math.max(0, new_energy)
    updated_predator['age'] = new_age
    return updated_predator

def calculateDistance(pos1, pos2):
    dx = (pos1['x'] - pos2['x'])
    dy = (pos1['y'] - pos2['y'])
    return ml_math.sqrt(((dx * dx) + (dy * dy)))

def clonePrey(prey):
    clone = {}
    clone['position'] = clonePosition(prey['position'])
    clone['energy'] = prey['energy']
    clone['speed'] = prey['speed']
    clone['reproduction_rate'] = prey['reproduction_rate']
    clone['detection_range'] = prey['detection_range']
    clone['state'] = prey['state']
    clone['age'] = prey['age']
    clone['last_reproduction'] = prey['last_reproduction']
    clone['fear_level'] = prey['fear_level']
    return clone

def clonePredator(predator):
    clone = {}
    clone['position'] = clonePosition(predator['position'])
    clone['energy'] = predator['energy']
    clone['speed'] = predator['speed']
    clone['hunting_efficiency'] = predator['hunting_efficiency']
    clone['detection_range'] = predator['detection_range']
    clone['state'] = predator['state']
    clone['age'] = predator['age']
    clone['last_meal'] = predator['last_meal']
    clone['target'] = predator['target']
    return clone

def clonePosition(pos):
    clone = {}
    clone['x'] = pos['x']
    clone['y'] = pos['y']
    return clone

def createStatistics():
    stats = {}
    stats['data_points'] = []
    return stats

def createStatsData(time, predator_count, prey_count, avg_predator_energy, avg_prey_energy, resources):
    data = {}
    data['time'] = time
    data['predator_count'] = predator_count
    data['prey_count'] = prey_count
    data['avg_predator_energy'] = avg_predator_energy
    data['avg_prey_energy'] = avg_prey_energy
    data['resources'] = resources
    return data

def recordDataPoint(stats, data):
    updated_stats = {}
    updated_stats['data_points'] = ml_collections.append(stats['data_points'], data)
    return updated_stats

exit_code = main()

# End of generated code