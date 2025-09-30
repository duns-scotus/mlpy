// Test new arrow function grammar
add = fn(x) => x + 1;
result = add(5);
print("Result: " + str(result));

// Test arrow function in function call
numbers = [1, 2, 3];
doubled = map(fn(x) => x * 2, numbers);
print("Doubled: " + str(len(doubled)));