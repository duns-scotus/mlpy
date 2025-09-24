// Functional programming patterns test program (ML syntax)
function createMultiplier(factor) {
    function multiply(value) {
        return value * factor;
    }
    return multiply;
}

function applyOperation(value, operation) {
    return operation(value);
}

function processNumbers(numbers) {
    double = createMultiplier(2);
    result1 = applyOperation(numbers[0], double);
    result2 = applyOperation(numbers[1], double);
    result3 = applyOperation(numbers[2], double);
    return [result1, result2, result3];
}

function recursiveSum(arr, index) {
    if (index >= 3) {
        return 0;
    } else {
        return arr[index] + recursiveSum(arr, index + 1);
    }
}

// Test functional operations
numbers = [5, 10, 15];
doubled = processNumbers(numbers);
sum = recursiveSum(numbers, 0);