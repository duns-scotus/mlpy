// Object-style programming test program (ML syntax - no classes)
function createAnimal(name, species) {
    animal = {};
    animal.name = name;
    animal.species = species;
    animal.energy = 100;
    return animal;
}

function animalSpeak(animal) {
    return animal.name + " makes a sound";
}

function animalMove(animal) {
    animal.energy = animal.energy - 10;
    return animal.name + " moves";
}

function createDog(name, breed) {
    dog = createAnimal(name, "Canis lupus");
    dog.breed = breed;
    dog.loyalty = 100;
    return dog;
}

function dogSpeak(dog) {
    return dog.name + " barks: Woof!";
}

function dogFetch(dog, item) {
    dog.energy = dog.energy - 15;
    dog.loyalty = dog.loyalty + 5;
    return dog.name + " fetches " + item;
}

// Test object-style operations
buddy = createDog("Buddy", "Golden Retriever");
speakResult = dogSpeak(buddy);
fetchResult = dogFetch(buddy, "ball");
moveResult = animalMove(buddy);