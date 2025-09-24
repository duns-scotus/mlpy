"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib import console, getCurrentTime, processData

def createAnimal(name, species):
    animal = {}
    animal['name'] = name
    animal['species'] = species
    animal['energy'] = 100
    return animal

def animalSpeak(animal):
    return (animal['name'] + ' makes a sound')

def animalMove(animal):
    animal['energy'] = (animal['energy'] - 10)
    return (animal['name'] + ' moves')

def createDog(name, breed):
    dog = createAnimal(name, 'Canis lupus')
    dog['breed'] = breed
    dog['loyalty'] = 100
    return dog

def dogSpeak(dog):
    return (dog['name'] + ' barks: Woof!')

def dogFetch(dog, item):
    dog['energy'] = (dog['energy'] - 15)
    dog['loyalty'] = (dog['loyalty'] + 5)
    return ((dog['name'] + ' fetches ') + item)

buddy = createDog('Buddy', 'Golden Retriever')

speakResult = dogSpeak(buddy)

fetchResult = dogFetch(buddy, 'ball')

moveResult = animalMove(buddy)

# End of generated code