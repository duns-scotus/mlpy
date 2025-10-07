// ============================================
// Example: HTTP GET Requests
// Category: standard-library/http
// Demonstrates: GET requests, response handling (API demonstration)
// Note: Actual network calls may not execute in sandbox
// ============================================

import console;
import http;

console.log("=== HTTP GET Requests ===\n");

console.log("This example demonstrates the HTTP GET API.");
console.log("Note: Actual network requests require network capabilities.\n");

// ============================================
// Basic GET Request Structure
// ============================================

console.log("=== Basic GET Request (API demonstration) ===");

console.log("Simple GET request syntax:");
console.log("  response = http.get(url);");
console.log("  response = http.get(url, headers);");
console.log("  response = http.get(url, headers, timeout);");

// ============================================
// Response Object Structure
// ============================================

console.log("\n=== Response Object (structure) ===");

console.log("Response object methods:");
console.log("  - response.status() -> HTTP status code (200, 404, etc.)");
console.log("  - response.statusText() -> Status message");
console.log("  - response.ok() -> true if 2xx status");
console.log("  - response.body() -> Response body as string");
console.log("  - response.text() -> Alias for body()");
console.log("  - response.json() -> Parse body as JSON");
console.log("  - response.headers() -> Response headers dictionary");

// ============================================
// GET Request Patterns
// ============================================

console.log("\n=== GET Request Patterns ===");

// Pattern 1: Simple GET
console.log("Pattern 1: Simple GET");
console.log("  url = \"https://api.example.com/data\";");
console.log("  response = http.get(url);");
console.log("  if (response.ok()) {");
console.log("    data = response.json();");
console.log("  }");

// Pattern 2: GET with headers
console.log("\nPattern 2: GET with custom headers");
console.log("  headers = {");
console.log("    \"Authorization\": \"Bearer token\",");
console.log("    \"Accept\": \"application/json\"");
console.log("  };");
console.log("  response = http.get(url, headers);");

// Pattern 3: GET with timeout
console.log("\nPattern 3: GET with timeout");
console.log("  response = http.get(url, null, 60);");
console.log("  // Timeout: 60 seconds");

// ============================================
// Response Status Checking
// ============================================

console.log("\n=== Response Status Checking ===");

console.log("Check response status:");
console.log("  if (response.status() == 200) {");
console.log("    console.log(\"Success\");");
console.log("  } elif (response.status() == 404) {");
console.log("    console.log(\"Not found\");");
console.log("  }");

console.log("\nOr use ok() helper:");
console.log("  if (response.ok()) {");
console.log("    // Status is 2xx (success)");
console.log("  }");

// ============================================
// Response Body Handling
// ============================================

console.log("\n=== Response Body Handling ===");

console.log("Get response as text:");
console.log("  text = response.body();");
console.log("  text = response.text();  // Alias");

console.log("\nParse response as JSON:");
console.log("  jsonData = response.json();");
console.log("  name = jsonData.name;");
console.log("  items = jsonData.items;");

// ============================================
// Header Access
// ============================================

console.log("\n=== Response Header Access ===");

console.log("Get response headers:");
console.log("  headers = response.headers();");
console.log("  contentType = headers[\"Content-Type\"];");
console.log("  contentLength = headers[\"Content-Length\"];");

// ============================================
// Query Parameters
// ============================================

console.log("\n=== Query Parameters with GET ===");

console.log("Build URL with query params:");
console.log("  params = {search: \"ML\", page: \"1\", limit: \"10\"};");
console.log("  queryStr = http.encodeQuery(params);");
console.log("  url = \"https://api.example.com/search?\" + queryStr;");
console.log("  response = http.get(url);");

// Demonstrate URL building
baseUrl = "https://api.example.com/search";
params = {query: "machine learning", limit: "50"};
queryStr = http.encodeQuery(params);
fullUrl = baseUrl + "?" + queryStr;
console.log("\nExample URL: " + fullUrl);

// ============================================
// Pagination Pattern
// ============================================

console.log("\n=== Pagination Pattern ===");

console.log("Fetch paginated data:");
console.log("  page = 1;");
console.log("  limit = 20;");
console.log("  params = {page: str(page), limit: str(limit)};");
console.log("  queryStr = http.encodeQuery(params);");
console.log("  url = baseUrl + \"?\" + queryStr;");
console.log("  response = http.get(url);");

// Demonstrate pagination URLs
console.log("\nPagination URL examples:");
i = 1;
while (i <= 3) {
    pageParams = {page: str(i), limit: "20"};
    pageQuery = http.encodeQuery(pageParams);
    pageUrl = "https://api.example.com/items?" + pageQuery;
    console.log("  Page " + str(i) + ": " + pageUrl);
    i = i + 1;
}

// ============================================
// Search Pattern
// ============================================

console.log("\n=== Search Pattern ===");

console.log("Build search request:");
console.log("  searchTerm = \"machine learning\";");
console.log("  encoded = http.encodeURI(searchTerm);");
console.log("  url = \"https://api.example.com/search?q=\" + encoded;");
console.log("  response = http.get(url);");

// Demonstrate search URL
searchTerm = "ML programming";
encodedSearch = http.encodeURI(searchTerm);
searchUrl = "https://api.example.com/search?q=" + encodedSearch;
console.log("\nSearch URL: " + searchUrl);

// ============================================
// Resource Fetching Pattern
// ============================================

console.log("\n=== Resource Fetching Pattern ===");

console.log("Fetch specific resource:");
console.log("  userId = 123;");
console.log("  url = \"https://api.example.com/users/\" + str(userId);");
console.log("  response = http.get(url);");
console.log("  if (response.ok()) {");
console.log("    user = response.json();");
console.log("    console.log(\"User: \" + user.name);");
console.log("  }");

// Demonstrate resource URLs
console.log("\nResource URL examples:");
resourceIds = [1, 42, 999];
i = 0;
while (i < len(resourceIds)) {
    id = resourceIds[i];
    resourceUrl = "https://api.example.com/items/" + str(id);
    console.log("  Item " + str(id) + ": " + resourceUrl);
    i = i + 1;
}

// ============================================
// Filtering Pattern
// ============================================

console.log("\n=== Filtering Pattern ===");

console.log("Apply filters:");
console.log("  filters = {");
console.log("    category: \"electronics\",");
console.log("    status: \"active\",");
console.log("    sort: \"price\"");
console.log("  };");
console.log("  queryStr = http.encodeQuery(filters);");
console.log("  url = baseUrl + \"?\" + queryStr;");

// Demonstrate filter URL
filters = {type: "article", status: "published", tag: "ml"};
filterQuery = http.encodeQuery(filters);
filterUrl = "https://api.example.com/posts?" + filterQuery;
console.log("\nFilter URL: " + filterUrl);

// ============================================
// Authentication Pattern
// ============================================

console.log("\n=== Authentication Pattern ===");

console.log("GET with authentication:");
console.log("  headers = {");
console.log("    \"Authorization\": \"Bearer your_token_here\",");
console.log("    \"Accept\": \"application/json\"");
console.log("  };");
console.log("  response = http.get(url, headers);");

console.log("\nOr with API key:");
console.log("  url = baseUrl + \"?api_key=your_key_here\";");
console.log("  response = http.get(url);");

// ============================================
// Error Handling Pattern
// ============================================

console.log("\n=== Error Handling Pattern ===");

console.log("Handle different status codes:");
console.log("  response = http.get(url);");
console.log("  status = response.status();");
console.log("  ");
console.log("  if (status == 200) {");
console.log("    data = response.json();");
console.log("  } elif (status == 404) {");
console.log("    console.log(\"Resource not found\");");
console.log("  } elif (status == 401) {");
console.log("    console.log(\"Unauthorized\");");
console.log("  } else {");
console.log("    console.log(\"Error: \" + str(status));");
console.log("  }");

// ============================================
// API Client Pattern
// ============================================

console.log("\n=== API Client Pattern ===");

apiBase = "https://api.example.com";

function buildApiUrl(endpoint, params) {
    url = apiBase + endpoint;
    if (params != null) {
        queryStr = http.encodeQuery(params);
        url = url + "?" + queryStr;
    }
    return url;
}

console.log("API client helper:");
console.log("  function buildApiUrl(endpoint, params) { ... }");

// Demonstrate API URLs
endpoints = [
    "/users",
    "/posts",
    "/comments"
];

console.log("\nAPI endpoint URLs:");
i = 0;
while (i < len(endpoints)) {
    endpoint = endpoints[i];
    apiUrl = buildApiUrl(endpoint, {limit: "10"});
    console.log("  " + endpoint + " -> " + apiUrl);
    i = i + 1;
}

// ============================================
// Best Practices
// ============================================

console.log("\n=== GET Request Best Practices ===");

console.log("1. Always check response.ok() or status code");
console.log("2. Set appropriate timeout for long requests");
console.log("3. Use headers for authentication");
console.log("4. URL-encode query parameters");
console.log("5. Handle errors gracefully");
console.log("6. Parse JSON responses with response.json()");
console.log("7. Include User-Agent header when needed");

// ============================================
// Common Status Codes
// ============================================

console.log("\n=== Common HTTP Status Codes ===");

console.log("Success (2xx):");
console.log("  200 - OK (request succeeded)");
console.log("  201 - Created (resource created)");
console.log("  204 - No Content (success, no body)");

console.log("\nClient Errors (4xx):");
console.log("  400 - Bad Request");
console.log("  401 - Unauthorized");
console.log("  403 - Forbidden");
console.log("  404 - Not Found");
console.log("  429 - Too Many Requests");

console.log("\nServer Errors (5xx):");
console.log("  500 - Internal Server Error");
console.log("  502 - Bad Gateway");
console.log("  503 - Service Unavailable");
console.log("  504 - Gateway Timeout");

// ============================================
// Summary
// ============================================

console.log("\n=== GET Request Summary ===");

console.log("GET request syntax:");
console.log("  response = http.get(url)");
console.log("  response = http.get(url, headers)");
console.log("  response = http.get(url, headers, timeout)");

console.log("\nResponse methods:");
console.log("  response.ok() - Check success");
console.log("  response.status() - Get status code");
console.log("  response.body() - Get response text");
console.log("  response.json() - Parse JSON");
console.log("  response.headers() - Get headers");

console.log("\nCommon patterns:");
console.log("  - Simple data fetching");
console.log("  - Pagination");
console.log("  - Search with query params");
console.log("  - Resource fetching by ID");
console.log("  - Filtering and sorting");

console.log("\n=== HTTP GET Requests Complete ===");
