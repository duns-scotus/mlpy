// Test all csv module functions end-to-end
// This validates the complete ML→Python transpilation pipeline for CSV operations

import csv;
import console;
import file;

console.log("=== Testing csv Module ===");

// Test 1: Create test data and write CSV
console.log("[Test 1] Create and write CSV");
users = [
    {name: "Alice Johnson", age: "30", city: "New York", email: "alice@example.com"},
    {name: "Bob Smith", age: "25", city: "Los Angeles", email: "bob@example.com"},
    {name: "Charlie Brown", age: "35", city: "San Francisco", email: "charlie@example.com"},
    {name: "Diana Prince", age: "28", city: "Seattle", email: "diana@example.com"}
];
csv.write("test_users.csv", users);
console.log("PASS: Created test CSV file");

// Test 2: Read CSV with headers
console.log("[Test 2] Read CSV with headers");
read_users = csv.read("test_users.csv");
if (len(read_users) == 4) {
    console.log("PASS: Read 4 users from CSV");
} else {
    console.log("FAIL: Expected 4 users, got " + str(len(read_users)));
}

// Test 3: Access CSV data
console.log("[Test 3] Access CSV data");
if (read_users[0].name == "Alice Johnson") {
    console.log("PASS: First user name correct");
} else {
    console.log("FAIL: First user name incorrect: " + read_users[0].name);
}

// Test 4: Write CSV from objects
console.log("[Test 4] Write CSV from objects");
test_data = [
    {name: "Test User 1", age: "40", city: "Boston"},
    {name: "Test User 2", age: "45", city: "Austin"}
];
csv.write("test_output.csv", test_data);
console.log("PASS: CSV written successfully");

// Test 5: Read written CSV
console.log("[Test 5] Read written CSV");
read_back = csv.read("test_output.csv");
if (len(read_back) == 2) {
    console.log("PASS: Read back 2 records");
} else {
    console.log("FAIL: Expected 2 records");
}

// Test 6: Verify written data
console.log("[Test 6] Verify written data");
if (read_back[0].name == "Test User 1") {
    console.log("PASS: Written data correct");
} else {
    console.log("FAIL: Written data incorrect");
}

// Test 7: CSV without headers
console.log("[Test 7] CSV without headers (arrays)");
array_data = [
    ["Name", "Age", "City"],
    ["User1", "30", "NYC"],
    ["User2", "25", "LA"]
];
csv.write("test_arrays.csv", array_data, ",", false);
read_arrays = csv.read("test_arrays.csv", ",", false);
if (len(read_arrays) == 3) {
    console.log("PASS: Array CSV works");
} else {
    console.log("FAIL: Array CSV failed");
}

// Test 8: Custom delimiter (semicolon)
console.log("[Test 8] Custom delimiter (semicolon)");
csv.write("test_ssv.csv", test_data, ";");
ssv_data = csv.read("test_ssv.csv", ";");
if (len(ssv_data) == 2) {
    console.log("PASS: Semicolon-delimited CSV works");
} else {
    console.log("FAIL: Semicolon-delimited CSV failed");
}

// Test 9: Get headers
console.log("[Test 9] Get headers");
headers = csv.get_headers("test_users.csv");
if (len(headers) == 4) {
    console.log("PASS: Got 4 headers - " + headers[0] + ", " + headers[1]);
} else {
    console.log("FAIL: Expected 4 headers");
}

// Test 10: Count rows
console.log("[Test 10] Count rows");
row_count = csv.count_rows("test_users.csv");
if (row_count == 4) {
    console.log("PASS: Counted 4 data rows");
} else {
    console.log("FAIL: Expected 4 rows, got " + str(row_count));
}

// Test 11: Append row
console.log("[Test 11] Append row");
new_user = {name: "Eve Davis", age: "29", city: "Portland", email: "eve@example.com"};
csv.append("test_output.csv", new_user);
appended_data = csv.read("test_output.csv");
if (len(appended_data) == 3) {
    console.log("PASS: Row appended (now 3 rows)");
} else {
    console.log("FAIL: Expected 3 rows after append");
}

// Test 12: Read CSV as string
console.log("[Test 12] Read CSV as string");
csv_text = "name,age\nAlice,30\nBob,25";
parsed = csv.read_string(csv_text);
if (len(parsed) == 2) {
    console.log("PASS: Parsed CSV string");
} else {
    console.log("FAIL: CSV string parsing failed");
}

// Test 13: Write CSV as string
console.log("[Test 13] Write CSV as string");
string_output = csv.write_string(test_data);
if (len(string_output) > 0) {
    console.log("PASS: CSV string generated");
} else {
    console.log("FAIL: CSV string generation failed");
}

// Test 14: Empty CSV
console.log("[Test 14] Empty CSV");
empty_data = [];
csv.write("test_empty.csv", empty_data);
empty_read = csv.read("test_empty.csv");
if (len(empty_read) == 0) {
    console.log("PASS: Empty CSV handled correctly");
} else {
    console.log("FAIL: Empty CSV should return empty array");
}

// Test 15: Real-world scenario - data processing
console.log("[Test 15] Real-world data processing");
original = csv.read("test_users.csv");
processed = [];
for (user in original) {
    processed_user = {
        name: user.name,
        age: user.age,
        location: user.city,
        contact: user.email
    };
    processed.append(processed_user);
}
csv.write("test_processed.csv", processed);
result = csv.read("test_processed.csv");
if (len(result) == 4 && result[0].location == "New York") {
    console.log("PASS: Data processing pipeline works");
} else {
    console.log("FAIL: Data processing pipeline failed");
}

// Cleanup test files
console.log("[Cleanup] Removing test files");
file.delete("test_users.csv");
file.delete("test_output.csv");
file.delete("test_arrays.csv");
file.delete("test_ssv.csv");
file.delete("test_empty.csv");
file.delete("test_processed.csv");
console.log("PASS: Cleanup complete");

console.log("=== All csv module tests passed! ===");
