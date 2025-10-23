// ============================================
// Example: Comprehensive HTTP API Client
// Category: standard-library/http
// Demonstrates: Complete API client with all HTTP features
// ============================================

import console;
import http;
import json;

console.log("=== Comprehensive HTTP API Client ===\n");

console.log("This example demonstrates a complete API client implementation.");
console.log("Note: This is an API demonstration. Network calls require capabilities.\n");

// ============================================
// API Client Configuration
// ============================================

console.log("=== API Client Configuration ===");

// API base configuration
apiBase = "https://api.example.com";
apiVersion = "v1";
apiTimeout = 30;

console.log("API Configuration:");
console.log("  Base URL: " + apiBase);
console.log("  Version: " + apiVersion);
console.log("  Timeout: " + str(apiTimeout) + "s");

// ============================================
// System 1: URL Builder
// ============================================

console.log("\n=== System 1: URL Builder ===");

function buildUrl(endpoint, params) {
    url = apiBase + "/" + apiVersion + endpoint;

    if (params != null) {
        queryStr = http.encodeQuery(params);
        if (len(queryStr) > 0) {
            url = url + "?" + queryStr;
        }
    }

    return url;
}

// Test URL builder
testUrls = [
    buildUrl("/users", null),
    buildUrl("/users", {page: "1", limit: "20"}),
    buildUrl("/posts", {author: "alice", status: "published"})
];

console.log("URL Builder examples:");
i = 0;
while (i < len(testUrls)) {
    console.log("  " + testUrls[i]);
    i = i + 1;
}

// ============================================
// System 2: Request Builder
// ============================================

console.log("\n=== System 2: Request Builder ===");

function buildHeaders(authToken, contentType) {
    headers = {};

    if (authToken != null) {
        headers = json.merge(headers, {"Authorization": "Bearer " + authToken});
    }

    if (contentType != null) {
        headers = json.merge(headers, {"Content-Type": contentType});
    }

    return headers;
}

// Test header builder
console.log("Header builder examples:");
headers1 = buildHeaders("sample_token", "application/json");
console.log("  With auth: " + str(headers1));

headers2 = buildHeaders(null, "application/json");
console.log("  No auth: " + str(headers2));

// ============================================
// System 3: Response Handler
// ============================================

console.log("\n=== System 3: Response Handler ===");

function handleResponse(response, description) {
    console.log("\nProcessing response: " + description);

    status = response.status();
    console.log("  Status: " + str(status) + " " + response.statusText());

    if (response.ok()) {
        console.log("  Result: SUCCESS");
        return response;
    } else {
        console.log("  Result: ERROR");
        console.log("  Body: " + response.body());
        return null;
    }
}

console.log("Response handler processes status and extracts data");

// ============================================
// System 4: User Resource Operations
// ============================================

console.log("\n=== System 4: User Resource Operations ===");

function getUser(userId) {
    console.log("\nGET User " + str(userId));
    url = buildUrl("/users/" + str(userId), null);
    console.log("  URL: " + url);
    console.log("  Method: GET");
    return url;
}

function createUser(userData) {
    console.log("\nCREATE User");
    url = buildUrl("/users", null);
    body = json.stringify(userData);
    console.log("  URL: " + url);
    console.log("  Method: POST");
    console.log("  Body: " + body);
    return url;
}

function updateUser(userId, userData) {
    console.log("\nUPDATE User " + str(userId));
    url = buildUrl("/users/" + str(userId), null);
    body = json.stringify(userData);
    console.log("  URL: " + url);
    console.log("  Method: PUT");
    console.log("  Body: " + body);
    return url;
}

function deleteUser(userId) {
    console.log("\nDELETE User " + str(userId));
    url = buildUrl("/users/" + str(userId), null);
    console.log("  URL: " + url);
    console.log("  Method: DELETE");
    return url;
}

// Demonstrate user operations
newUser = {name: "Alice", email: "alice@example.com", role: "developer"};
createUser(newUser);
getUser(123);
updateUser(123, {name: "Alice Smith", role: "senior-developer"});
deleteUser(123);

// ============================================
// System 5: Collection Operations
// ============================================

console.log("\n=== System 5: Collection Operations ===");

function listUsers(page, limit) {
    console.log("\nLIST Users");
    params = {page: str(page), limit: str(limit)};
    url = buildUrl("/users", params);
    console.log("  URL: " + url);
    console.log("  Method: GET");
    return url;
}

function searchUsers(query, filters) {
    console.log("\nSEARCH Users");
    params = json.merge(filters, {q: query});
    url = buildUrl("/users/search", params);
    console.log("  URL: " + url);
    console.log("  Method: GET");
    return url;
}

// Demonstrate collection operations
listUsers(1, 20);
searchFilters = {role: "developer", status: "active"};
searchUsers("alice", searchFilters);

// ============================================
// System 6: Batch Operations
// ============================================

console.log("\n=== System 6: Batch Operations ===");

function batchOperation(operation, ids) {
    console.log("\nBATCH " + operation);
    console.log("  Processing " + str(len(ids)) + " items");

    i = 0;
    while (i < len(ids)) {
        id = ids[i];
        url = buildUrl("/items/" + str(id), null);
        console.log("  " + str(i + 1) + ". " + operation + " " + str(id) + " -> " + url);
        i = i + 1;
    }

    console.log("  Batch complete");
}

// Demonstrate batch operations
batchIds = [101, 102, 103, 104, 105];
batchOperation("GET", batchIds);

// ============================================
// System 7: Error Recovery
// ============================================

console.log("\n=== System 7: Error Recovery ===");

function retryRequest(url, maxRetries) {
    console.log("\nRetry logic for: " + url);
    console.log("  Max retries: " + str(maxRetries));

    attempt = 0;
    while (attempt < maxRetries) {
        attempt = attempt + 1;
        console.log("  Attempt " + str(attempt) + "/" + str(maxRetries));

        // Simulate retry logic
        if (attempt == maxRetries) {
            console.log("  Final attempt - would execute request");
            return true;
        }

        console.log("  Would wait and retry...");
    }

    return false;
}

// Demonstrate retry logic
testUrl = buildUrl("/users", null);
retryRequest(testUrl, 3);

// ============================================
// System 8: Rate Limiting
// ============================================

console.log("\n=== System 8: Rate Limiting ===");

function checkRateLimit(headers) {
    console.log("\nRate limit check:");

    // Extract rate limit headers
    console.log("  X-RateLimit-Limit: 1000");
    console.log("  X-RateLimit-Remaining: 856");
    console.log("  X-RateLimit-Reset: 1640000000");

    remaining = 856;
    limit = 1000;
    percentage = (remaining * 100) / limit;

    console.log("  Usage: " + str(100 - percentage) + "%");

    if (remaining < 100) {
        console.log("  WARNING: Low rate limit");
        return false;
    }

    return true;
}

// Demonstrate rate limit check
checkRateLimit({});

// ============================================
// System 9: Request Queue
// ============================================

console.log("\n=== System 9: Request Queue ===");

requestQueue = [
    {method: "GET", endpoint: "/users/1"},
    {method: "POST", endpoint: "/posts"},
    {method: "PUT", endpoint: "/users/2"},
    {method: "DELETE", endpoint: "/posts/5"}
];

function processQueue(queue) {
    console.log("\nProcessing request queue");
    console.log("  Queue size: " + str(len(queue)));

    i = 0;
    while (i < len(queue)) {
        req = queue[i];
        url = buildUrl(req.endpoint, null);
        console.log("  " + str(i + 1) + ". " + req.method + " " + url);
        i = i + 1;
    }

    console.log("  Queue processed");
}

// Demonstrate queue processing
processQueue(requestQueue);

// ============================================
// System 10: API Client Wrapper
// ============================================

console.log("\n=== System 10: Complete API Client ===");

console.log("\nAPI Client Methods:");
console.log("  - buildUrl(endpoint, params)");
console.log("  - buildHeaders(authToken, contentType)");
console.log("  - handleResponse(response, description)");
console.log("  - getUser(userId)");
console.log("  - createUser(userData)");
console.log("  - updateUser(userId, userData)");
console.log("  - deleteUser(userId)");
console.log("  - listUsers(page, limit)");
console.log("  - searchUsers(query, filters)");
console.log("  - batchOperation(operation, ids)");
console.log("  - retryRequest(url, maxRetries)");
console.log("  - checkRateLimit(headers)");
console.log("  - processQueue(queue)");

// ============================================
// Usage Example: CRUD Workflow
// ============================================

console.log("\n=== Usage Example: CRUD Workflow ===");

console.log("\nComplete CRUD workflow:");

// 1. Create
console.log("\n1. CREATE new user");
newUserData = {
    name: "Bob Developer",
    email: "bob@example.com",
    role: "engineer",
    team: "backend"
};
createUserUrl = createUser(newUserData);

// 2. Read
console.log("\n2. READ user details");
getUserUrl = getUser(456);

// 3. Update
console.log("\n3. UPDATE user");
updateData = {
    role: "senior-engineer",
    team: "platform"
};
updateUserUrl = updateUser(456, updateData);

// 4. Delete
console.log("\n4. DELETE user");
deleteUserUrl = deleteUser(456);

// ============================================
// API Patterns Summary
// ============================================

console.log("\n=== API Patterns Summary ===");

console.log("\nResource patterns:");
console.log("  Collection: GET /users");
console.log("  Create: POST /users");
console.log("  Read: GET /users/123");
console.log("  Update: PUT /users/123");
console.log("  Partial: PATCH /users/123");
console.log("  Delete: DELETE /users/123");

console.log("\nQuery patterns:");
console.log("  Pagination: ?page=1&limit=20");
console.log("  Search: ?q=alice&type=user");
console.log("  Filtering: ?role=dev&status=active");
console.log("  Sorting: ?sort=name&order=asc");

console.log("\nHeader patterns:");
console.log("  Auth: Authorization: Bearer token");
console.log("  Content: Content-Type: application/json");
console.log("  Accept: Accept: application/json");
console.log("  Rate: X-RateLimit-Remaining: 856");

// ============================================
// Integration Features
// ============================================

console.log("\n=== Integration Features ===");

console.log("URL encoding:");
console.log("  - encodeURI() for path segments");
console.log("  - encodeQuery() for parameters");
console.log("  - decodeURI() for responses");

console.log("\nJSON handling:");
console.log("  - json.stringify() for request bodies");
console.log("  - response.json() for responses");
console.log("  - json.merge() for combining objects");

console.log("\nError handling:");
console.log("  - response.ok() for success check");
console.log("  - response.status() for status codes");
console.log("  - Retry logic for transient failures");
console.log("  - Rate limit awareness");

// ============================================
// Best Practices Applied
// ============================================

console.log("\n=== Best Practices Applied ===");

console.log("1. URL Builder: Consistent URL construction");
console.log("2. Header Builder: Reusable authentication");
console.log("3. Response Handler: Centralized error handling");
console.log("4. Resource Operations: CRUD encapsulation");
console.log("5. Collection Operations: Pagination support");
console.log("6. Batch Operations: Efficient bulk processing");
console.log("7. Error Recovery: Retry logic");
console.log("8. Rate Limiting: API quota management");
console.log("9. Request Queue: Sequential processing");
console.log("10. Complete Workflow: End-to-end examples");

// ============================================
// Configuration Summary
// ============================================

console.log("\n=== Configuration Summary ===");

console.log("API Settings:");
console.log("  Base URL: " + apiBase);
console.log("  Version: " + apiVersion);
console.log("  Timeout: " + str(apiTimeout) + "s");

console.log("\nSupported Operations:");
console.log("  GET - Retrieve data");
console.log("  POST - Create resources");
console.log("  PUT - Update resources");
console.log("  PATCH - Partial updates");
console.log("  DELETE - Remove resources");
console.log("  HEAD - Get metadata");

console.log("\nFeatures:");
console.log("  - URL encoding/decoding");
console.log("  - Query parameter handling");
console.log("  - JSON serialization");
console.log("  - Authentication headers");
console.log("  - Error recovery");
console.log("  - Rate limiting");
console.log("  - Batch operations");
console.log("  - Request queueing");

console.log("\n=== Comprehensive API Client Complete ===");
