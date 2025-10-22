// ML Integration Test: Capability Introspection Functions
// Tests: hasCapability(), getCapabilities(), getCapabilityInfo()

print("=== Capability Introspection Integration Test ===");
print("");

// Test 1: hasCapability() - Basic usage
print("Test 1: hasCapability() - Check individual capabilities");
hasFileRead = hasCapability("file.read");
hasFileWrite = hasCapability("file.write");
hasNetwork = hasCapability("network.http");
hasGui = hasCapability("gui.create");

print("  hasCapability('file.read'): " + str(hasFileRead));
print("  hasCapability('file.write'): " + str(hasFileWrite));
print("  hasCapability('network.http'): " + str(hasNetwork));
print("  hasCapability('gui.create'): " + str(hasGui));
print("");

// Test 2: getCapabilities() - List all capabilities
print("Test 2: getCapabilities() - List all available capabilities");
caps = getCapabilities();
print("  Total capabilities: " + str(len(caps)));
print("  Capabilities:");
if (len(caps) == 0) {
    print("    (none - running in restricted mode)");
} else {
    for (cap in caps) {
        print("    - " + cap);
    }
}
print("");

// Test 3: getCapabilityInfo() - Get detailed info
print("Test 3: getCapabilityInfo() - Detailed capability information");

// Try file.read capability
fileReadInfo = getCapabilityInfo("file.read");
if (fileReadInfo != null) {
    print("  file.read capability:");
    print("    Type: " + fileReadInfo.type);
    print("    Available: " + str(fileReadInfo.available));
    print("    Usage count: " + str(fileReadInfo.usage_count));

    if (fileReadInfo.patterns != null) {
        print("    Patterns: " + str(fileReadInfo.patterns));
    } else {
        print("    Patterns: (no restrictions)");
    }

    if (fileReadInfo.max_usage != null) {
        remaining = fileReadInfo.max_usage - fileReadInfo.usage_count;
        print("    Max usage: " + str(fileReadInfo.max_usage));
        print("    Remaining: " + str(remaining));
    } else {
        print("    Max usage: (unlimited)");
    }
} else {
    print("  file.read: Not available");
}
print("");

// Try network.http capability
networkInfo = getCapabilityInfo("network.http");
if (networkInfo != null) {
    print("  network.http capability:");
    print("    Type: " + networkInfo.type);
    print("    Available: " + str(networkInfo.available));
} else {
    print("  network.http: Not available");
}
print("");

// Test 4: Defensive Programming Pattern
print("Test 4: Defensive Programming - Check before use");

function loadData() {
    if (hasCapability("file.read")) {
        print("  File reading permitted - would load from file");
        return "file_data";
    } elif (hasCapability("network.http")) {
        print("  Network access permitted - would load from network");
        return "network_data";
    } else {
        print("  No data loading capabilities - using defaults");
        return "default_data";
    }
}

result = loadData();
print("  Result: " + result);
print("");

// Test 5: Feature Detection Pattern
print("Test 5: Feature Detection - Configure based on capabilities");

features = [];

if (hasCapability("file.read")) {
    features = features + ["load-files"];
}

if (hasCapability("file.write")) {
    features = features + ["save-files"];
}

if (hasCapability("network.http")) {
    features = features + ["sync-cloud"];
}

if (hasCapability("gui.create")) {
    features = features + ["gui-mode"];
}

print("  Available features: " + str(features));
print("");

// Test 6: Startup Validation Pattern
print("Test 6: Startup Validation - Check required capabilities");

required = ["file.read", "file.write"];
missing = [];

for (cap in required) {
    if (!hasCapability(cap)) {
        missing = missing + [cap];
    }
}

if (len(missing) == 0) {
    print("  All required capabilities available");
} else {
    print("  WARNING: Missing required capabilities:");
    for (cap in missing) {
        print("    - " + cap);
    }
}
print("");

// Test 7: Debug Environment Information
print("Test 7: Debug Environment - Print execution context");

function debugEnvironment() {
    print("  === Execution Environment ===");

    caps = getCapabilities();
    print("  Capabilities (" + str(len(caps)) + "):");

    if (len(caps) == 0) {
        print("    (none)");
    } else {
        for (cap in caps) {
            info = getCapabilityInfo(cap);
            if (info != null) {
                status = info.available ? "valid" : "expired";
                print("    - " + cap + " (" + status + ")");

                if (info.patterns != null) {
                    print("      Patterns: " + str(info.patterns));
                }
                if (info.max_usage != null) {
                    remaining = info.max_usage - info.usage_count;
                    print("      Usage: " + str(info.usage_count) + "/" + str(info.max_usage) + " (remaining: " + str(remaining) + ")");
                }
            }
        }
    }
}

debugEnvironment();
print("");

// Test 8: Combined Pattern - Smart Feature Configuration
print("Test 8: Smart Configuration - Adapt to available capabilities");

function configureApp() {
    config = {
        mode: "unknown",
        features: [],
        dataSource: "none"
    };

    // Determine mode based on capabilities
    if (hasCapability("gui.create")) {
        config.mode = "gui";
    } elif (hasCapability("network.http")) {
        config.mode = "networked";
    } else {
        config.mode = "minimal";
    }

    // Configure data source
    if (hasCapability("file.read")) {
        config.dataSource = "file";
        config.features = config.features + ["load-config"];
    } elif (hasCapability("network.http")) {
        config.dataSource = "network";
        config.features = config.features + ["fetch-remote"];
    }

    // Add persistence if available
    if (hasCapability("file.write")) {
        config.features = config.features + ["save-data"];
    }

    return config;
}

appConfig = configureApp();
print("  Application mode: " + appConfig.mode);
print("  Data source: " + appConfig.dataSource);
print("  Features: " + str(appConfig.features));
print("");

print("=== All Tests Complete ===");
