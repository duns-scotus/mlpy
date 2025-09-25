// Pattern Matching Examples
// Demonstrates advanced pattern matching capabilities

// Basic pattern matching
function processValue(input) {
    match input {
        n when n > 100 => "Large number: " + n;
        n when n > 0 => "Small number: " + n;
        0 => "Zero";
        _ => "Negative or invalid";
    }
}

// Test pattern matching
result1 = processValue(150)
result2 = processValue(5)
result3 = processValue(0)
result4 = processValue(-10)

print("Result 1: " + result1)
print("Result 2: " + result2)
print("Result 3: " + result3)
print("Result 4: " + result4)

// Array pattern matching
function processArray(data) {
    match data {
        [] => "Empty array";
        [x] => "Single element: " + x;
        [first, ...rest] => "First: " + first + ", Rest length: " + rest.length;
        _ => "Complex array";
    }
}

// Test array patterns
empty_result = processArray([])
single_result = processArray([42])
multi_result = processArray([1, 2, 3, 4, 5])

print("Empty: " + empty_result)
print("Single: " + single_result)
print("Multi: " + multi_result)