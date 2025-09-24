// Control flow structures test program (simplified ML syntax)
function processNumber(n) {
    if (n > 10) {
        result = n * 2;
        return result;
    } else {
        return n + 5;
    }
}

function countUp(start) {
    i = start;
    while (i < 5) {
        i = i + 1;
    }
    return i;
}

// Test the functions
result1 = processNumber(15);
result2 = processNumber(3);
count = countUp(0);