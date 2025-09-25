// Control Flow Examples
// Demonstrates if/else, loops, and function definitions

// Basic conditional
age = 25
if (age >= 18) {
    status = "adult"
} else {
    status = "minor"
}
print("Status: " + status)

// Function definition
function greet(name) {
    return "Hello, " + name + "!"
}

// Function call
greeting = greet("Alice")
print(greeting)

// Loop example
numbers = [1, 2, 3, 4, 5]
sum = 0
for (i = 0; i < numbers.length; i = i + 1) {
    sum = sum + numbers[i]
}
print("Sum: " + sum)

// While loop
counter = 0
while (counter < 3) {
    print("Counter: " + counter)
    counter = counter + 1
}