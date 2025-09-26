def processPreyBehavior(prey_population, predator_population, environment, time_step):
    alive_prey = collections.filter(prey_population, lambda prey: (prey['energy'] > 0))
    processed_prey = collections.map(alive_prey, lambda prey_individual: None)
    return collections.filter(processed_prey, lambda prey: (prey['energy'] > 0))

print("Syntax OK")