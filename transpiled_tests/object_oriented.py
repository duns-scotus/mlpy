"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

def createAnimal(name, species):
    animal = {}
    animal['name'] = name
    animal['species'] = species
    animal['energy'] = 100
    return animal

def animalSpeak(animal):
    return (str(animal['name']) + str(' makes a sound'))

def animalMove(animal):
    animal['energy'] = (animal['energy'] - 10)
    return (str(animal['name']) + str(' moves'))

def createDog(name, breed):
    dog = createAnimal(name, 'Canis lupus')
    dog['breed'] = breed
    dog['loyalty'] = 100
    return dog

def dogSpeak(dog):
    return (str(dog['name']) + str(' barks: Woof!'))

def dogFetch(dog, item):
    dog['energy'] = (dog['energy'] - 15)
    dog['loyalty'] = (dog['loyalty'] + 5)
    return (str((str(dog['name']) + str(' fetches '))) + str(item))

buddy = createDog('Buddy', 'Golden Retriever')

speakResult = dogSpeak(buddy)

fetchResult = dogFetch(buddy, 'ball')

moveResult = animalMove(buddy)

# End of generated code