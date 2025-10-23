// ============================================
// Example: HTTP POST, PUT, DELETE, PATCH Requests
// Category: standard-library/http
// Demonstrates: POST, PUT, DELETE, PATCH, HEAD methods (API demonstration)
// ============================================

import console;
import http;
import json;

console.log("=== HTTP POST, PUT, DELETE, PATCH ===\n");

console.log("This example demonstrates HTTP method APIs.");
console.log("Note: Actual network requests require network capabilities.\n");

// ============================================
// POST Requests
// ============================================

console.log("=== POST Requests ===");

console.log("POST request syntax:");
console.log("  response = http.post(url, options);");
console.log("  ");
console.log("Options object:");
console.log("  {");
console.log("    body: json.stringify(data),");
console.log("    headers: {\"Content-Type\": \"application/json\"},");
console.log("    timeout: 30");
console.log("  }");

// ============================================
// POST with JSON
// ============================================

console.log("\n=== POST with JSON Body ===");

console.log("Create resource with JSON:");
console.log("  newUser = {name: \"Alice\", email: \"alice@example.com\"};");
console.log("  body = json.stringify(newUser);");
console.log("  ");
console.log("  options = {");
console.log("    body: body,");
console.log("    headers: {\"Content-Type\": \"application/json\"}");
console.log("  };");
console.log("  ");
console.log("  response = http.post(\"https://api.example.com/users\", options);");
console.log("  if (response.ok()) {");
console.log("    created = response.json();");
console.log("    console.log(\"Created ID: \" + str(created.id));");
console.log("  }");

// Demonstrate JSON body preparation
newItem = {name: "Item 1", price: 29.99, quantity: 10};
itemBody = json.stringify(newItem);
console.log("\nExample JSON body: " + itemBody);

// ============================================
// POST with Form Data
// ============================================

console.log("\n=== POST with Form Data ===");

console.log("Submit form data:");
console.log("  formData = {username: \"john\", password: \"secret\"};");
console.log("  body = http.encodeQuery(formData);");
console.log("  ");
console.log("  options = {");
console.log("    body: body,");
console.log("    headers: {\"Content-Type\": \"application/x-www-form-urlencoded\"}");
console.log("  };");
console.log("  ");
console.log("  response = http.post(loginUrl, options);");

// Demonstrate form encoding
formData = {username: "alice", action: "login"};
formBody = http.encodeQuery(formData);
console.log("\nForm-encoded body: " + formBody);

// ============================================
// PUT Requests
// ============================================

console.log("\n=== PUT Requests ===");

console.log("PUT request syntax:");
console.log("  response = http.put(url, options);");
console.log("  ");
console.log("Update resource:");
console.log("  updatedUser = {name: \"Alice Smith\", email: \"alice@example.com\"};");
console.log("  body = json.stringify(updatedUser);");
console.log("  ");
console.log("  options = {");
console.log("    body: body,");
console.log("    headers: {\"Content-Type\": \"application/json\"}");
console.log("  };");
console.log("  ");
console.log("  url = \"https://api.example.com/users/123\";");
console.log("  response = http.put(url, options);");

// Demonstrate PUT URL
userId = 42;
putUrl = "https://api.example.com/users/" + str(userId);
console.log("\nPUT URL example: " + putUrl);

// ============================================
// DELETE Requests
// ============================================

console.log("\n=== DELETE Requests ===");

console.log("DELETE request syntax:");
console.log("  response = http.delete(url);");
console.log("  response = http.delete(url, headers);");
console.log("  response = http.delete(url, headers, timeout);");
console.log("  ");
console.log("Delete resource:");
console.log("  url = \"https://api.example.com/items/456\";");
console.log("  response = http.delete(url);");
console.log("  ");
console.log("  if (response.ok()) {");
console.log("    console.log(\"Deleted successfully\");");
console.log("  }");

// Demonstrate DELETE URLs
console.log("\nDELETE URL examples:");
deleteIds = [1, 5, 99];
i = 0;
while (i < len(deleteIds)) {
    id = deleteIds[i];
    deleteUrl = "https://api.example.com/items/" + str(id);
    console.log("  Delete item " + str(id) + ": " + deleteUrl);
    i = i + 1;
}

// ============================================
// PATCH Requests
// ============================================

console.log("\n=== PATCH Requests ===");

console.log("PATCH request syntax:");
console.log("  response = http.patch(url, options);");
console.log("  ");
console.log("Partial update:");
console.log("  patch = {status: \"completed\"};");
console.log("  body = json.stringify(patch);");
console.log("  ");
console.log("  options = {");
console.log("    body: body,");
console.log("    headers: {\"Content-Type\": \"application/json\"}");
console.log("  };");
console.log("  ");
console.log("  response = http.patch(\"https://api.example.com/tasks/789\", options);");

// Demonstrate PATCH body
patchData = {status: "active", priority: "high"};
patchBody = json.stringify(patchData);
console.log("\nPATCH body example: " + patchBody);

// ============================================
// HEAD Requests
// ============================================

console.log("\n=== HEAD Requests ===");

console.log("HEAD request syntax:");
console.log("  response = http.head(url);");
console.log("  response = http.head(url, headers, timeout);");
console.log("  ");
console.log("Get metadata only:");
console.log("  response = http.head(\"https://example.com/large-file.zip\");");
console.log("  headers = response.headers();");
console.log("  fileSize = headers[\"Content-Length\"];");
console.log("  contentType = headers[\"Content-Type\"];");
console.log("  console.log(\"File size: \" + fileSize);");

// ============================================
// Custom Request Method
// ============================================

console.log("\n=== Custom Request Method ===");

console.log("Using http.request() for full control:");
console.log("  options = {");
console.log("    method: \"POST\",");
console.log("    url: \"https://api.example.com/data\",");
console.log("    headers: {");
console.log("      \"Authorization\": \"Bearer token\",");
console.log("      \"Content-Type\": \"application/json\"");
console.log("    },");
console.log("    body: json.stringify(data),");
console.log("    timeout: 60");
console.log("  };");
console.log("  ");
console.log("  response = http.request(options);");

// ============================================
// Authentication Patterns
// ============================================

console.log("\n=== Authentication Patterns ===");

console.log("Bearer token authentication:");
console.log("  headers = {");
console.log("    \"Authorization\": \"Bearer your_token_here\",");
console.log("    \"Content-Type\": \"application/json\"");
console.log("  };");
console.log("  ");
console.log("  options = {body: body, headers: headers};");
console.log("  response = http.post(url, options);");

console.log("\nAPI key authentication:");
console.log("  headers = {");
console.log("    \"X-API-Key\": \"your_api_key_here\"");
console.log("  };");

console.log("\nBasic authentication:");
console.log("  // Encode credentials as base64");
console.log("  headers = {");
console.log("    \"Authorization\": \"Basic base64_encoded_credentials\"");
console.log("  };");

// ============================================
// CRUD Operations Pattern
// ============================================

console.log("\n=== CRUD Operations Pattern ===");

apiBase = "https://api.example.com/items";

console.log("Create (POST):");
console.log("  url = \"" + apiBase + "\";");
console.log("  // POST to collection URL");

console.log("\nRead (GET):");
console.log("  url = \"" + apiBase + "/123\";");
console.log("  // GET specific resource");

console.log("\nUpdate (PUT):");
console.log("  url = \"" + apiBase + "/123\";");
console.log("  // PUT to specific resource");

console.log("\nPartial Update (PATCH):");
console.log("  url = \"" + apiBase + "/123\";");
console.log("  // PATCH specific resource");

console.log("\nDelete (DELETE):");
console.log("  url = \"" + apiBase + "/123\";");
console.log("  // DELETE specific resource");

// ============================================
// Error Handling
// ============================================

console.log("\n=== Error Handling ===");

console.log("Handle POST/PUT/DELETE errors:");
console.log("  response = http.post(url, options);");
console.log("  status = response.status();");
console.log("  ");
console.log("  if (status == 201) {");
console.log("    console.log(\"Created successfully\");");
console.log("  } elif (status == 400) {");
console.log("    console.log(\"Bad request\");");
console.log("  } elif (status == 401) {");
console.log("    console.log(\"Unauthorized\");");
console.log("  } elif (status == 409) {");
console.log("    console.log(\"Conflict - resource exists\");");
console.log("  } elif (status == 422) {");
console.log("    console.log(\"Validation error\");");
console.log("  }");

// ============================================
// Request Body Patterns
// ============================================

console.log("\n=== Request Body Patterns ===");

console.log("JSON body:");
console.log("  data = {field1: \"value1\", field2: 123};");
console.log("  body = json.stringify(data);");
console.log("  headers = {\"Content-Type\": \"application/json\"};");

console.log("\nForm-encoded body:");
console.log("  data = {username: \"alice\", email: \"alice@example.com\"};");
console.log("  body = http.encodeQuery(data);");
console.log("  headers = {\"Content-Type\": \"application/x-www-form-urlencoded\"};");

console.log("\nPlain text body:");
console.log("  body = \"Plain text content\";");
console.log("  headers = {\"Content-Type\": \"text/plain\"};");

// ============================================
// Response Status Checking
// ============================================

console.log("\n=== Response Status Checking ===");

console.log("POST/PUT success:");
console.log("  if (response.status() == 200) {");
console.log("    // Updated");
console.log("  } elif (response.status() == 201) {");
console.log("    // Created");
console.log("  }");

console.log("\nDELETE success:");
console.log("  if (response.status() == 204) {");
console.log("    // Deleted (no content)");
console.log("  } elif (response.status() == 200) {");
console.log("    // Deleted with response body");
console.log("  }");

// ============================================
// Timeout Configuration
// ============================================

console.log("\n=== Timeout Configuration ===");

console.log("Short timeout (fast operations):");
console.log("  options = {body: body, headers: headers, timeout: 10};");
console.log("  response = http.post(url, options);");

console.log("\nLong timeout (slow operations):");
console.log("  options = {body: body, headers: headers, timeout: 120};");
console.log("  response = http.post(url, options);");

console.log("\nDefault timeout:");
console.log("  // Default is 30 seconds");
console.log("  options = {body: body, headers: headers};");
console.log("  response = http.post(url, options);");

// ============================================
// Best Practices
// ============================================

console.log("\n=== Best Practices ===");

console.log("1. Always set Content-Type header for POST/PUT/PATCH");
console.log("2. Use json.stringify() for JSON bodies");
console.log("3. Check response status codes");
console.log("4. Handle authentication properly");
console.log("5. Set appropriate timeouts");
console.log("6. Use PUT for full updates, PATCH for partial");
console.log("7. Validate data before sending");
console.log("8. Handle errors gracefully");

// ============================================
// Common Patterns
// ============================================

console.log("\n=== Common Patterns ===");

console.log("Create new resource:");
console.log("  1. Prepare data object");
console.log("  2. Convert to JSON with json.stringify()");
console.log("  3. Set Content-Type header");
console.log("  4. POST to collection URL");
console.log("  5. Check for 201 Created status");
console.log("  6. Extract ID from response");

console.log("\nUpdate existing resource:");
console.log("  1. Fetch current data (GET)");
console.log("  2. Modify data");
console.log("  3. Convert to JSON");
console.log("  4. PUT to specific resource URL");
console.log("  5. Check for 200 OK status");

console.log("\nDelete resource:");
console.log("  1. Confirm deletion if needed");
console.log("  2. DELETE to specific resource URL");
console.log("  3. Check for 204 No Content or 200 OK");

// ============================================
// Summary
// ============================================

console.log("\n=== HTTP Methods Summary ===");

console.log("Method overview:");
console.log("  GET - Retrieve data (read-only)");
console.log("  POST - Create new resource");
console.log("  PUT - Update entire resource");
console.log("  PATCH - Partial resource update");
console.log("  DELETE - Remove resource");
console.log("  HEAD - Get metadata only");

console.log("\nRequest options:");
console.log("  body - Request body content");
console.log("  headers - Request headers dictionary");
console.log("  timeout - Request timeout in seconds");

console.log("\nSuccess status codes:");
console.log("  200 - OK (general success)");
console.log("  201 - Created (POST success)");
console.log("  204 - No Content (DELETE success)");

console.log("\n=== HTTP POST/PUT/DELETE Complete ===");
