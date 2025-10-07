// ============================================
// Example: Collections and Iteration
// Category: standard-library/builtin
// Demonstrates: len(), range(), enumerate(), keys(), values(), zip(), sorted()
// ============================================

print("=== Collections and Iteration ===\n");

// len() - Universal length function
print("Getting lengths:");
print("  len('hello') = " + str(len("hello")));               // 5
print("  len([1,2,3,4,5]) = " + str(len([1,2,3,4,5])));      // 5
print("  len({a:1, b:2, c:3}) = " + str(len({a:1, b:2, c:3})));  // 3

// range() - Generate number sequences
print("\n=== Range Generation ===");

// Single argument - from 0 to n
numbers = range(5);
print("range(5) = " + str(numbers));  // [0, 1, 2, 3, 4]

// Two arguments - from start to stop
numbers = range(2, 7);
print("range(2, 7) = " + str(numbers));  // [2, 3, 4, 5, 6]

// Three arguments - with step
numbers = range(0, 10, 2);
print("range(0, 10, 2) = " + str(numbers));  // [0, 2, 4, 6, 8]

// Practical: Sum first N numbers
print("\nSum first 10 numbers:");
total = sum(range(11));
print("sum(range(11)) = " + str(total));  // 55

// enumerate() - Index-value pairs
print("\n=== Enumerate Arrays ===");

fruits = ["apple", "banana", "cherry"];
indexed = enumerate(fruits);
print("Fruits with indices:");

i = 0;
while (i < len(indexed)) {
    pair = indexed[i];
    index = pair[0];
    fruit = pair[1];
    print("  [" + str(index) + "] " + fruit);
    i = i + 1;
}

// enumerate() with custom start
indexed = enumerate(fruits, 1);
print("\nFruits numbered from 1:");
i = 0;
while (i < len(indexed)) {
    pair = indexed[i];
    number = pair[0];
    fruit = pair[1];
    print("  " + str(number) + ". " + fruit);
    i = i + 1;
}

// keys() and values() - Object iteration
print("\n=== Object Keys and Values ===");

person = {name: "Alice", age: 30, city: "NYC", job: "Engineer"};

personKeys = keys(person);
print("Keys: " + str(personKeys));

personValues = values(person);
print("Values: " + str(personValues));

print("\nIterating over object:");
i = 0;
while (i < len(personKeys)) {
    key = personKeys[i];
    value = person[key];
    print("  " + key + " -> " + str(value));
    i = i + 1;
}

// zip() - Combine multiple arrays
print("\n=== Zipping Arrays ===");

names = ["Alice", "Bob", "Charlie"];
ages = [25, 30, 35];
cities = ["NYC", "LA", "Chicago"];

zipped = zip(names, ages, cities);
print("Combined data:");
i = 0;
while (i < len(zipped)) {
    record = zipped[i];
    name = record[0];
    age = record[1];
    city = record[2];
    print("  " + name + ", " + str(age) + ", " + city);
    i = i + 1;
}

// Practical: Create objects from parallel arrays
print("\nCreating person objects:");
people = [];
i = 0;
while (i < len(names)) {
    person = {
        name: names[i],
        age: ages[i],
        city: cities[i]
    };
    people = people + [person];
    i = i + 1;
}

i = 0;
while (i < len(people)) {
    p = people[i];
    print("  " + p.name + " (" + str(p.age) + ") from " + p.city);
    i = i + 1;
}

// sorted() - Sorting arrays
print("\n=== Sorting ===");

numbers = [42, 7, 23, 91, 15, 3];
print("Original: " + str(numbers));
print("Sorted (ascending): " + str(sorted(numbers)));
print("Sorted (descending): " + str(sorted(numbers, true)));

words = ["zebra", "apple", "mango", "banana"];
print("\nWords original: " + str(words));
print("Words sorted: " + str(sorted(words)));

// Practical example: Processing student data
print("\n=== Student Grade Processing ===");

students = ["Alice", "Bob", "Charlie", "David", "Eve"];
scores = [92, 78, 88, 95, 82];

print("Student scores:");
pairs = zip(students, scores);
i = 0;
while (i < len(pairs)) {
    student = pairs[i][0];
    score = pairs[i][1];
    print("  " + student + ": " + str(score));
    i = i + 1;
}

// Find top scorers
sortedScores = sorted(scores, true);
print("\nTop 3 scores: " + str([sortedScores[0], sortedScores[1], sortedScores[2]]));

// Average score
average = sum(scores) / len(scores);
print("Average score: " + str(round(average, 2)));

// Count above average
aboveAverage = 0;
i = 0;
while (i < len(scores)) {
    if (scores[i] > average) {
        aboveAverage = aboveAverage + 1;
    }
    i = i + 1;
}
print("Students above average: " + str(aboveAverage));

// Building a frequency map
print("\n=== Frequency Counting ===");

votes = ["apple", "banana", "apple", "cherry", "banana", "apple", "banana"];
counts = {};

i = 0;
while (i < len(votes)) {
    fruit = votes[i];
    if (hasattr(counts, fruit)) {
        counts[fruit] = counts[fruit] + 1;
    } else {
        counts[fruit] = 1;
    }
    i = i + 1;
}

print("Vote counts:");
countKeys = keys(counts);
i = 0;
while (i < len(countKeys)) {
    fruit = countKeys[i];
    count = counts[fruit];
    print("  " + fruit + ": " + str(count) + " votes");
    i = i + 1;
}

print("\n=== Collections Complete ===");
