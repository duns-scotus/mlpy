// ============================================
// Example: Application Logging
// Category: standard-library/console
// Demonstrates: Structured logging for application events
// ============================================

import console;

console.log("=== Application Logging Example ===\n");

// Application startup sequence
console.info("=== Application Startup ===");
console.info("Loading configuration...");
config = {port: 8080, debug: true};
console.debug("Config loaded:", config);
console.info("Configuration loaded");

console.info("Initializing database connection...");
console.debug("Database host: localhost");
console.debug("Database port: 5432");
console.info("Database connected");

console.info("Starting web server...");
console.debug("Listening on port:", config.port);
console.info("Server started successfully");
console.info("=== Ready ===\n");

// Processing requests
console.log("=== Processing Requests ===");

function processRequest(requestId, userId) {
    console.info("Processing request", requestId, "for user", userId);
    console.debug("Request ID:", requestId);
    console.debug("User ID:", userId);

    // Simulate processing
    if (userId > 0) {
        console.debug("User validation passed");
        console.info("Request", requestId, "completed successfully");
        return true;
    } else {
        console.warn("Invalid user ID:", userId);
        console.error("Request", requestId, "failed - invalid user");
        return false;
    }
}

// Process several requests
requests = [
    {id: 1, user: 101},
    {id: 2, user: 102},
    {id: 3, user: -1},
    {id: 4, user: 103}
];

successCount = 0;
failCount = 0;

for (req in requests) {
    success = processRequest(req.id, req.user);
    if (success) {
        successCount = successCount + 1;
    } else {
        failCount = failCount + 1;
    }
}

console.log("\n=== Processing Summary ===");
console.info("Total requests:", len(requests));
console.info("Successful:", successCount);
if (failCount > 0) {
    console.warn("Failed:", failCount);
}

// Application shutdown
console.log("\n=== Application Shutdown ===");
console.info("Shutting down gracefully...");
console.debug("Closing database connections");
console.info("Database disconnected");
console.debug("Stopping web server");
console.info("Server stopped");
console.info("=== Shutdown Complete ===");

console.log("\n=== Application Logging Complete ===");
