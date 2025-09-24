// Unicode handling test program (corrected ML syntax - safe version)
function processText(input) {
    // Test Unicode string handling without malicious patterns
    cleaned = input + "_processed";
    return cleaned;
}

function normalizeString(text) {
    // Simple string normalization simulation
    if (text == "test") {
        return "normalized_test";
    } else {
        return text + "_normalized";
    }
}

// Test Unicode handling safely
result1 = processText("hello_world");
result2 = normalizeString("test");
result3 = normalizeString("unicode_text");