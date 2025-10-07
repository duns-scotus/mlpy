// ============================================
// Example: HTTP Response Handling
// Category: standard-library/http
// Demonstrates: Response object, status codes, headers, error handling
// ============================================

import console;
import http;
import json;

console.log("=== HTTP Response Handling ===\n");

// ============================================
// Response Object Methods
// ============================================

console.log("=== Response Object Methods ===");

console.log("Response object provides 7 methods:");
console.log("  1. status() - Get HTTP status code (200, 404, etc.)");
console.log("  2. statusText() - Get status message (\"OK\", \"Not Found\")");
console.log("  3. ok() - Check if status is 2xx (success)");
console.log("  4. body() - Get response body as string");
console.log("  5. text() - Alias for body()");
console.log("  6. json() - Parse body as JSON");
console.log("  7. headers() - Get headers dictionary");

// ============================================
// Status Code Checking
// ============================================

console.log("\n=== Status Code Checking ===");

console.log("Check exact status:");
console.log("  status = response.status();");
console.log("  if (status == 200) {");
console.log("    console.log(\"Success\");");
console.log("  } elif (status == 404) {");
console.log("    console.log(\"Not found\");");
console.log("  }");

console.log("\nCheck success range:");
console.log("  if (response.ok()) {");
console.log("    // Status is 200-299 (success)");
console.log("    data = response.json();");
console.log("  }");

// ============================================
// Status Code Categories
// ============================================

console.log("\n=== Status Code Categories ===");

console.log("1xx - Informational:");
console.log("  100 - Continue");
console.log("  101 - Switching Protocols");

console.log("\n2xx - Success:");
console.log("  200 - OK");
console.log("  201 - Created");
console.log("  202 - Accepted");
console.log("  204 - No Content");

console.log("\n3xx - Redirection:");
console.log("  301 - Moved Permanently");
console.log("  302 - Found (temporary redirect)");
console.log("  304 - Not Modified");

console.log("\n4xx - Client Errors:");
console.log("  400 - Bad Request");
console.log("  401 - Unauthorized");
console.log("  403 - Forbidden");
console.log("  404 - Not Found");
console.log("  405 - Method Not Allowed");
console.log("  409 - Conflict");
console.log("  422 - Unprocessable Entity");
console.log("  429 - Too Many Requests");

console.log("\n5xx - Server Errors:");
console.log("  500 - Internal Server Error");
console.log("  501 - Not Implemented");
console.log("  502 - Bad Gateway");
console.log("  503 - Service Unavailable");
console.log("  504 - Gateway Timeout");

// ============================================
// Response Body Access
// ============================================

console.log("\n=== Response Body Access ===");

console.log("Get response as text:");
console.log("  text = response.body();");
console.log("  text = response.text();  // Same as body()");
console.log("  console.log(\"Response: \" + text);");

console.log("\nParse response as JSON:");
console.log("  if (response.ok()) {");
console.log("    data = response.json();");
console.log("    name = data.name;");
console.log("    items = data.items;");
console.log("  }");

console.log("\nHandle JSON parsing errors:");
console.log("  if (response.ok()) {");
console.log("    // Check Content-Type before parsing");
console.log("    headers = response.headers();");
console.log("    contentType = headers[\"Content-Type\"];");
console.log("    ");
console.log("    if (contentType == \"application/json\") {");
console.log("      data = response.json();");
console.log("    } else {");
console.log("      text = response.text();");
console.log("    }");
console.log("  }");

// ============================================
// Header Access
// ============================================

console.log("\n=== Response Header Access ===");

console.log("Get all headers:");
console.log("  headers = response.headers();");
console.log("  console.log(\"Headers: \" + str(headers));");

console.log("\nGet specific headers:");
console.log("  headers = response.headers();");
console.log("  contentType = headers[\"Content-Type\"];");
console.log("  contentLength = headers[\"Content-Length\"];");
console.log("  server = headers[\"Server\"];");
console.log("  date = headers[\"Date\"];");

console.log("\nCommon response headers:");
console.log("  - Content-Type: Response body format");
console.log("  - Content-Length: Response body size");
console.log("  - Cache-Control: Caching directives");
console.log("  - ETag: Resource version identifier");
console.log("  - Last-Modified: Resource modification time");
console.log("  - Location: Redirect target (3xx responses)");
console.log("  - Set-Cookie: Cookie setting");
console.log("  - Server: Server software info");

// ============================================
// Error Handling Patterns
// ============================================

console.log("\n=== Error Handling Patterns ===");

console.log("Pattern 1: Simple success check");
console.log("  response = http.get(url);");
console.log("  if (response.ok()) {");
console.log("    data = response.json();");
console.log("  } else {");
console.log("    console.log(\"Error: \" + str(response.status()));");
console.log("  }");

console.log("\nPattern 2: Specific error handling");
console.log("  status = response.status();");
console.log("  if (status == 200) {");
console.log("    data = response.json();");
console.log("  } elif (status == 404) {");
console.log("    console.log(\"Resource not found\");");
console.log("  } elif (status == 429) {");
console.log("    console.log(\"Rate limit exceeded\");");
console.log("  } elif (status >= 500) {");
console.log("    console.log(\"Server error\");");
console.log("  }");

console.log("\nPattern 3: Error message extraction");
console.log("  if (!response.ok()) {");
console.log("    errorBody = response.text();");
console.log("    console.log(\"Error response: \" + errorBody);");
console.log("    ");
console.log("    // Try to parse error as JSON");
console.log("    errorData = response.json();");
console.log("    if (errorData.message) {");
console.log("      console.log(\"Error: \" + errorData.message);");
console.log("    }");
console.log("  }");

// ============================================
// Status-Based Logic
// ============================================

console.log("\n=== Status-Based Response Logic ===");

console.log("Handle different response types:");
console.log("  status = response.status();");
console.log("  ");
console.log("  if (status >= 200 && status < 300) {");
console.log("    // Success - process data");
console.log("    data = response.json();");
console.log("    console.log(\"Success: \" + str(data));");
console.log("  } elif (status >= 300 && status < 400) {");
console.log("    // Redirection");
console.log("    headers = response.headers();");
console.log("    location = headers[\"Location\"];");
console.log("    console.log(\"Redirect to: \" + location);");
console.log("  } elif (status >= 400 && status < 500) {");
console.log("    // Client error");
console.log("    console.log(\"Client error: \" + str(status));");
console.log("  } elif (status >= 500) {");
console.log("    // Server error");
console.log("    console.log(\"Server error: \" + str(status));");
console.log("  }");

// ============================================
// Response Processing Pipeline
// ============================================

console.log("\n=== Response Processing Pipeline ===");

console.log("Complete response handling:");
console.log("  response = http.get(url);");
console.log("  ");
console.log("  // 1. Check status");
console.log("  if (!response.ok()) {");
console.log("    console.log(\"Request failed: \" + str(response.status()));");
console.log("    return null;");
console.log("  }");
console.log("  ");
console.log("  // 2. Check Content-Type");
console.log("  headers = response.headers();");
console.log("  contentType = headers[\"Content-Type\"];");
console.log("  ");
console.log("  // 3. Parse response");
console.log("  if (contentType == \"application/json\") {");
console.log("    data = response.json();");
console.log("  } else {");
console.log("    data = response.text();");
console.log("  }");
console.log("  ");
console.log("  // 4. Process data");
console.log("  return data;");

// ============================================
// Pagination Response Handling
// ============================================

console.log("\n=== Pagination Response Handling ===");

console.log("Extract pagination info:");
console.log("  response = http.get(url);");
console.log("  if (response.ok()) {");
console.log("    data = response.json();");
console.log("    ");
console.log("    items = data.items;");
console.log("    totalPages = data.totalPages;");
console.log("    currentPage = data.page;");
console.log("    hasMore = data.hasMore;");
console.log("    ");
console.log("    console.log(\"Page \" + str(currentPage) + \"/\" + str(totalPages));");
console.log("    console.log(\"Items: \" + str(len(items)));");
console.log("  }");

// ============================================
// API Response Patterns
// ============================================

console.log("\n=== Common API Response Patterns ===");

console.log("Pattern 1: Success with data");
console.log("  {");
console.log("    \"success\": true,");
console.log("    \"data\": { ... }");
console.log("  }");

console.log("\nPattern 2: Error with message");
console.log("  {");
console.log("    \"success\": false,");
console.log("    \"error\": \"Error message\",");
console.log("    \"code\": \"ERROR_CODE\"");
console.log("  }");

console.log("\nPattern 3: Collection with metadata");
console.log("  {");
console.log("    \"items\": [...],");
console.log("    \"total\": 100,");
console.log("    \"page\": 1,");
console.log("    \"perPage\": 20");
console.log("  }");

console.log("\nPattern 4: Envelope format");
console.log("  {");
console.log("    \"status\": \"success\",");
console.log("    \"data\": { ... },");
console.log("    \"meta\": { ... }");
console.log("  }");

// ============================================
// Error Response Handling
// ============================================

console.log("\n=== Error Response Handling ===");

console.log("Extract error details:");
console.log("  if (!response.ok()) {");
console.log("    status = response.status();");
console.log("    statusText = response.statusText();");
console.log("    ");
console.log("    console.log(\"HTTP \" + str(status) + \": \" + statusText);");
console.log("    ");
console.log("    // Try to get error message from body");
console.log("    errorBody = response.text();");
console.log("    console.log(\"Response: \" + errorBody);");
console.log("    ");
console.log("    // Try JSON error format");
console.log("    errorData = response.json();");
console.log("    if (errorData.message) {");
console.log("      console.log(\"Error: \" + errorData.message);");
console.log("    }");
console.log("  }");

// ============================================
// Timeout Error Handling
// ============================================

console.log("\n=== Timeout Error Handling ===");

console.log("Handle timeout errors:");
console.log("  // Timeouts throw RuntimeError");
console.log("  // Default timeout: 30 seconds");
console.log("  // Set custom timeout in request options");
console.log("  ");
console.log("  response = http.get(url, null, 60);  // 60 second timeout");

// ============================================
// Response Validation
// ============================================

console.log("\n=== Response Validation ===");

console.log("Validate response structure:");
console.log("  response = http.get(url);");
console.log("  if (response.ok()) {");
console.log("    data = response.json();");
console.log("    ");
console.log("    // Validate required fields");
console.log("    if (json.hasKey(data, \"id\") &&");
console.log("        json.hasKey(data, \"name\")) {");
console.log("      console.log(\"Valid response\");");
console.log("      return data;");
console.log("    } else {");
console.log("      console.log(\"Invalid response structure\");");
console.log("      return null;");
console.log("    }");
console.log("  }");

// ============================================
// Best Practices
// ============================================

console.log("\n=== Response Handling Best Practices ===");

console.log("1. Always check response.ok() or status code");
console.log("2. Handle different error types appropriately");
console.log("3. Check Content-Type before parsing");
console.log("4. Extract error messages from response body");
console.log("5. Validate response structure");
console.log("6. Use statusText for debugging");
console.log("7. Log headers for troubleshooting");
console.log("8. Handle timeouts gracefully");
console.log("9. Implement retry logic for server errors");
console.log("10. Parse JSON safely (check content type first)");

// ============================================
// Success Check Methods
// ============================================

console.log("\n=== Success Check Methods ===");

console.log("Method 1: Using ok()");
console.log("  if (response.ok()) {");
console.log("    // Status is 2xx");
console.log("  }");

console.log("\nMethod 2: Exact status");
console.log("  if (response.status() == 200) {");
console.log("    // Exact match");
console.log("  }");

console.log("\nMethod 3: Status range");
console.log("  status = response.status();");
console.log("  if (status >= 200 && status < 300) {");
console.log("    // Success range");
console.log("  }");

// ============================================
// Summary
// ============================================

console.log("\n=== Response Handling Summary ===");

console.log("Key methods:");
console.log("  response.ok() - Check if 2xx status");
console.log("  response.status() - Get status code");
console.log("  response.statusText() - Get status message");
console.log("  response.body() - Get response text");
console.log("  response.json() - Parse as JSON");
console.log("  response.headers() - Get headers");

console.log("\nCommon patterns:");
console.log("  - Check status before processing");
console.log("  - Parse JSON for structured data");
console.log("  - Extract error messages");
console.log("  - Validate response structure");
console.log("  - Handle different status codes");

console.log("\nStatus code categories:");
console.log("  2xx - Success");
console.log("  3xx - Redirection");
console.log("  4xx - Client error");
console.log("  5xx - Server error");

console.log("\n=== Response Handling Complete ===");
