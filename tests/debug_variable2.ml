// More complex test case matching control_flow.ml pattern
function processNumber(n) {
    if (n > 10) {
        result = n * 2;
    } else {
        return result;  // ERROR: result not defined in else branch
        return n + 5;   // unreachable
    }
}

output = processNumber(3);