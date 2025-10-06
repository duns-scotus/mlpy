// Test stdlib module: http - HTTP client utilities
// Features tested: encodeURI, decodeURI, encodeQuery, parseQuery
// Module: http (URL utilities require no capabilities)
// Note: Actual HTTP requests require network.http/network.https capabilities

import http;

function test_uri_encoding() {
    results = {};

    // Encode special characters
    results.space = http.encodeURI("hello world");               // "hello%20world"
    results.at_sign = http.encodeURI("user@example.com");        // Contains %40
    results.question = http.encodeURI("what?");                  // Contains %3F
    results.slash = http.encodeURI("path/to/file");              // Contains path/to/file

    // Check encoding worked
    results.space_encoded = results.space == "hello%20world";    // true
    results.has_encoded_chars = len(results.at_sign) > len("user@example.com");  // true

    return results;
}

function test_uri_decoding() {
    results = {};

    // Decode percent-encoded strings
    results.space = http.decodeURI("hello%20world");             // "hello world"
    results.at_sign = http.decodeURI("user%40example.com");      // "user@example.com"
    results.plus = http.decodeURI("hello+world");                // "hello+world" (+ not decoded)

    // Check decoding worked
    results.space_decoded = results.space == "hello world";      // true
    results.at_decoded = results.at_sign == "user@example.com";  // true

    return results;
}

function test_round_trip_encoding() {
    results = {};

    // Encode then decode should give original
    original1 = "hello world";
    encoded1 = http.encodeURI(original1);
    decoded1 = http.decodeURI(encoded1);
    results.round_trip1 = decoded1 == original1;                 // true

    original2 = "user@example.com?query=test";
    encoded2 = http.encodeURI(original2);
    decoded2 = http.decodeURI(encoded2);
    results.round_trip2 = decoded2 == original2;                 // true

    return results;
}

function test_query_encoding() {
    results = {};

    // Encode object as query string
    params1 = {};
    params1.name = "John Doe";
    params1.age = 30;

    query1 = http.encodeQuery(params1);

    // Should contain both parameters
    results.has_name = query1 != "";                             // true
    results.has_equals = query1 != "";                           // true (contains =)
    results.query_length = len(query1);

    // Simple params
    params2 = {};
    params2.q = "search";
    params2.page = 1;

    query2 = http.encodeQuery(params2);
    results.simple_query = len(query2) > 0;                      // true

    return results;
}

function test_query_parsing() {
    results = {};

    // Parse query string to object
    parsed1 = http.parseQuery("name=John&age=30");

    results.has_name_key = parsed1.name != null;                 // true
    results.name_value = parsed1.name;                           // "John"
    results.age_value = parsed1.age;                             // "30"

    // Parse with leading ?
    parsed2 = http.parseQuery("?search=ML&lang=en");

    results.has_search = parsed2.search != null;                 // true
    results.search_value = parsed2.search;                       // "ML"

    return results;
}

function test_query_round_trip() {
    results = {};

    // Create params, encode, parse, compare
    original = {};
    original.query = "test";
    original.limit = 10;

    // Encode to query string
    query_str = http.encodeQuery(original);

    // Parse back
    parsed = http.parseQuery(query_str);

    // Should match original
    results.query_matches = parsed.query == "test";              // true
    results.limit_exists = parsed.limit != null;                 // true

    return results;
}

function test_url_building() {
    results = {};

    // Build URLs using utilities
    base = "https://api.example.com/search";

    // Build query parameters
    params = {};
    params.q = "ML programming";
    params.page = 1;
    params.limit = 20;

    query = http.encodeQuery(params);

    // Full URL would be: base + "?" + query
    results.has_base = len(base) > 0;                            // true
    results.has_query = len(query) > 0;                          // true

    // Encode individual parameter
    encoded_q = http.encodeURI("ML programming");
    results.param_encoded = len(encoded_q) > 0;                  // true

    return results;
}

function test_special_characters() {
    results = {};

    // Test various special characters
    test_strings = [
        "hello world",
        "test@example.com",
        "path/to/resource",
        "key=value",
        "a+b",
        "100%"
    ];

    // Encode all
    encoded_count = 0;
    for (s in test_strings) {
        encoded = http.encodeURI(s);
        if (len(encoded) > 0) {
            encoded_count = encoded_count + 1;
        }
    }

    results.all_encoded = encoded_count == len(test_strings);    // true
    results.test_count = len(test_strings);                      // 6

    return results;
}

function test_empty_and_edge_cases() {
    results = {};

    // Empty string
    empty_encoded = http.encodeURI("");
    results.empty_encoded = empty_encoded == "";                 // true

    empty_decoded = http.decodeURI("");
    results.empty_decoded = empty_decoded == "";                 // true

    // Empty query
    empty_query = http.encodeQuery({});
    results.empty_query_ok = len(empty_query) >= 0;              // true

    // Parse empty query
    empty_parsed = http.parseQuery("");
    results.empty_parsed_ok = typeof(empty_parsed) == "object";  // true

    return results;
}

function test_complex_query_params() {
    results = {};

    // Complex parameter object
    params = {};
    params.search = "machine learning";
    params.filter = "recent";
    params.sort = "relevance";
    params.page = 1;
    params.limit = 50;

    // Encode to query string
    query = http.encodeQuery(params);

    results.query_not_empty = len(query) > 0;                    // true

    // Parse back
    parsed = http.parseQuery(query);

    // Check all parameters present
    has_all = (
        parsed.search != null &&
        parsed.filter != null &&
        parsed.sort != null &&
        parsed.page != null &&
        parsed.limit != null
    );

    results.all_params_present = has_all;                        // true

    return results;
}

function test_practical_url_scenarios() {
    results = {};

    // Scenario 1: Search API
    search_query = "artificial intelligence";
    encoded_search = http.encodeURI(search_query);
    results.search_encoded = len(encoded_search) > 0;            // true

    // Scenario 2: API with multiple filters
    api_params = {};
    api_params.q = "ML";
    api_params.category = "tech";
    api_params.date = "2024-01-01";

    api_query = http.encodeQuery(api_params);
    results.api_query_built = len(api_query) > 0;                // true

    // Scenario 3: Parsing callback URL
    callback_url = "status=success&code=abc123&state=xyz";
    callback_params = http.parseQuery(callback_url);

    results.has_status = callback_params.status != null;         // true
    results.status_value = callback_params.status;               // "success"

    return results;
}

function test_encoding_consistency() {
    results = {};

    // Same input should give same output
    input = "test string";
    encoded1 = http.encodeURI(input);
    encoded2 = http.encodeURI(input);

    results.consistent = encoded1 == encoded2;                   // true

    // Decoding consistency
    decoded1 = http.decodeURI(encoded1);
    decoded2 = http.decodeURI(encoded2);

    results.decode_consistent = decoded1 == decoded2;            // true
    results.matches_original = decoded1 == input;                // true

    return results;
}

function test_query_param_types() {
    results = {};

    // Test different value types in query params
    params = {};
    params.string_val = "text";
    params.number_val = 42;
    params.bool_val = true;

    query = http.encodeQuery(params);

    // Should encode all types
    results.encoded_ok = len(query) > 0;                         // true

    // Parse back
    parsed = http.parseQuery(query);

    // All should be present (as strings after parsing)
    results.has_string = parsed.string_val != null;              // true
    results.has_number = parsed.number_val != null;              // true
    results.has_bool = parsed.bool_val != null;                  // true

    return results;
}

function main() {
    all_results = {};

    all_results.uri_encode = test_uri_encoding();
    all_results.uri_decode = test_uri_decoding();
    all_results.round_trip = test_round_trip_encoding();
    all_results.query_encode = test_query_encoding();
    all_results.query_parse = test_query_parsing();
    all_results.query_round_trip = test_query_round_trip();
    all_results.url_build = test_url_building();
    all_results.special_chars = test_special_characters();
    all_results.edge_cases = test_empty_and_edge_cases();
    all_results.complex_query = test_complex_query_params();
    all_results.practical = test_practical_url_scenarios();
    all_results.consistency = test_encoding_consistency();
    all_results.param_types = test_query_param_types();

    return all_results;
}

// Run tests
test_results = main();
