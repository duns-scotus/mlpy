def processPreyBehavior(prey_population, predator_population, environment, time_step):
    alive_prey = ml_collections.filter(prey_population, lambda prey: (prey['energy'] > 0))
    processed_prey = ml_collections.map(alive_prey, lambda prey_individual: None  # TODO: Complex function with 5 statements)
    return ml_collections.filter(processed_prey, lambda prey: (prey['energy'] > 0))

print('Function OK')
