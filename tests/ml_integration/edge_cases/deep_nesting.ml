// Deep nesting structures test program (corrected ML syntax)
function createNestedData(depth) {
    if (depth <= 0) {
        return 42;
    }

    nested = createNestedData(depth - 1);
    result = nested + 1;
    return result;
}

function processDeepStructure(level) {
    if (level > 10) {
        innerValue = processDeepStructure(level - 1);
        return innerValue * 2;
    } else {
        if (level > 5) {
            return level + 100;
        } else {
            return level;
        }
    }
}

// Test deep nesting without malicious patterns
deepResult = createNestedData(20);
processed = processDeepStructure(15);