// mlpy v2.0 Capability Integration Demo
// This demonstrates capability declarations in ML code

capability FileAccess {
    resource "*.txt";
    resource "data/*.json";
    allow read;
    allow write;
}

capability MathOperations {
    allow execute;
}

function processFile(filename) {
    // This function would require FileAccess capability at runtime
    return "Processing " + filename;
}

function calculateSum(a, b) {
    // This function would require MathOperations capability
    return a + b;
}

function main() {
    result1 = processFile("test.txt");
    result2 = calculateSum(10, 20);
    return result1 + " - Sum: " + result2;
}