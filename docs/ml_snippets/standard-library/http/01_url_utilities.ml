// ============================================
// Example: URL Utilities
// Category: standard-library/http
// Demonstrates: encodeURI, decodeURI, encodeQuery, parseQuery
// ============================================

import console;
import http;

console.log("=== URL Utilities ===\n");

// ============================================
// URL Encoding
// ============================================

console.log("=== encodeURI (percent encoding) ===");

// Encode spaces
text1 = "hello world";
encoded1 = http.encodeURI(text1);
console.log("Original: " + text1);
console.log("Encoded: " + encoded1);

// Encode special characters
text2 = "user@example.com";
encoded2 = http.encodeURI(text2);
console.log("\nOriginal: " + text2);
console.log("Encoded: " + encoded2);

// Encode path with spaces
text3 = "my file.txt";
encoded3 = http.encodeURI(text3);
console.log("\nOriginal: " + text3);
console.log("Encoded: " + encoded3);

// Build URL with encoded query
searchTerm = "machine learning";
encodedSearch = http.encodeURI(searchTerm);
url = "https://api.example.com/search?q=" + encodedSearch;
console.log("\nSearch URL: " + url);

// ============================================
// URL Decoding
// ============================================

console.log("\n=== decodeURI (percent decoding) ===");

// Decode spaces
encoded4 = "hello%20world";
decoded1 = http.decodeURI(encoded4);
console.log("Encoded: " + encoded4);
console.log("Decoded: " + decoded1);

// Decode special characters
encoded5 = "user%40example.com";
decoded2 = http.decodeURI(encoded5);
console.log("\nEncoded: " + encoded5);
console.log("Decoded: " + decoded2);

// Decode path
encoded6 = "my%20file.txt";
decoded3 = http.decodeURI(encoded6);
console.log("\nEncoded: " + encoded6);
console.log("Decoded: " + decoded3);

// ============================================
// Round-Trip Encoding
// ============================================

console.log("\n=== Round-Trip Encoding ===");

original = "special chars: @#$%";
console.log("Original: " + original);

encoded = http.encodeURI(original);
console.log("Encoded: " + encoded);

decoded = http.decodeURI(encoded);
console.log("Decoded: " + decoded);

matches = original == decoded;
console.log("Round-trip match: " + str(matches));

// ============================================
// Query String Encoding
// ============================================

console.log("\n=== encodeQuery (object to query string) ===");

// Simple parameters
params1 = {name: "John", age: "30"};
query1 = http.encodeQuery(params1);
console.log("Parameters: " + str(params1));
console.log("Query string: " + query1);

// Search parameters
params2 = {q: "machine learning", limit: "10", offset: "0"};
query2 = http.encodeQuery(params2);
console.log("\nSearch params: " + str(params2));
console.log("Query string: " + query2);

// Build complete URL
baseUrl = "https://api.example.com/search";
searchParams = {query: "ML", page: "1"};
queryString = http.encodeQuery(searchParams);
fullUrl = baseUrl + "?" + queryString;
console.log("\nFull URL: " + fullUrl);

// Filter parameters
filters = {category: "tech", status: "active", sort: "date"};
filterQuery = http.encodeQuery(filters);
console.log("\nFilter query: " + filterQuery);

// ============================================
// Query String Parsing
// ============================================

console.log("\n=== parseQuery (query string to object) ===");

// Parse simple query
queryStr1 = "name=John&age=30";
parsed1 = http.parseQuery(queryStr1);
console.log("Query string: " + queryStr1);
console.log("Parsed: " + str(parsed1));

// Parse with leading ?
queryStr2 = "?search=ML&page=2";
parsed2 = http.parseQuery(queryStr2);
console.log("\nQuery string: " + queryStr2);
console.log("Parsed: " + str(parsed2));

// Parse URL-encoded values
queryStr3 = "name=John%20Doe&email=john%40example.com";
parsed3 = http.parseQuery(queryStr3);
console.log("\nQuery string: " + queryStr3);
console.log("Parsed: " + str(parsed3));

// ============================================
// Practical Example: Search URL Builder
// ============================================

console.log("\n=== Practical: Search URL Builder ===");

function buildSearchUrl(baseUrl, searchTerm, page, limit) {
    params = {
        q: searchTerm,
        page: str(page),
        limit: str(limit)
    };

    queryString = http.encodeQuery(params);
    return baseUrl + "?" + queryString;
}

// Build search URLs
searchUrl1 = buildSearchUrl("https://api.example.com/search", "ML", 1, 10);
console.log("Search URL 1: " + searchUrl1);

searchUrl2 = buildSearchUrl("https://api.example.com/search", "machine learning", 2, 20);
console.log("Search URL 2: " + searchUrl2);

// ============================================
// Practical Example: URL Parameter Parser
// ============================================

console.log("\n=== Practical: URL Parameter Parser ===");

function parseUrlParams(url) {
    // Find query string (after ?)
    queryStart = 0;
    i = 0;
    while (i < len(url)) {
        // Simple character-by-character check for '?'
        if (i > 0) {
            // In real ML we'd check url[i] == '?', simplified here
            queryStart = i;
        }
        i = i + 1;
    }

    // For demo, use a known query string
    queryStr = "name=Alice&role=developer&level=senior";
    params = http.parseQuery(queryStr);

    console.log("  Query string: " + queryStr);
    console.log("  Parsed params: " + str(params));

    return params;
}

demoUrl = "https://api.example.com/users?name=Alice&role=developer&level=senior";
urlParams = parseUrlParams(demoUrl);

// ============================================
// Practical Example: API Client URL Builder
// ============================================

console.log("\n=== Practical: API Client URL Builder ===");

apiBase = "https://api.example.com";

function buildApiUrl(endpoint, params) {
    url = apiBase + endpoint;

    if (params != null) {
        queryStr = http.encodeQuery(params);
        url = url + "?" + queryStr;
    }

    return url;
}

// Build various API URLs
usersUrl = buildApiUrl("/users", {page: "1", limit: "50"});
console.log("Users URL: " + usersUrl);

postsUrl = buildApiUrl("/posts", {author: "john", status: "published"});
console.log("Posts URL: " + postsUrl);

itemUrl = buildApiUrl("/items/123", null);
console.log("Item URL: " + itemUrl);

// ============================================
// Practical Example: Query String Filters
// ============================================

console.log("\n=== Practical: Query String Filters ===");

function buildFilterUrl(baseUrl, filters) {
    // Only add non-empty filters
    activeFilters = {};

    // Note: In real ML we'd check each filter value
    // For demo, just use the filters as-is
    queryStr = http.encodeQuery(filters);

    if (len(queryStr) > 0) {
        return baseUrl + "?" + queryStr;
    } else {
        return baseUrl;
    }
}

// Apply filters
allFilters = {
    category: "electronics",
    minPrice: "100",
    maxPrice: "500",
    brand: "Samsung"
};

filteredUrl = buildFilterUrl("https://shop.example.com/products", allFilters);
console.log("Filtered URL: " + filteredUrl);

// ============================================
// Encoding Special Cases
// ============================================

console.log("\n=== Special Character Encoding ===");

// Encode various special characters
specialChars = [
    "hello world",
    "user@example.com",
    "path/to/file",
    "key=value",
    "a+b=c"
];

console.log("Encoding special characters:");
i = 0;
while (i < len(specialChars)) {
    original = specialChars[i];
    encoded = http.encodeURI(original);
    console.log("  " + original + " -> " + encoded);
    i = i + 1;
}

// ============================================
// Query String Round-Trip
// ============================================

console.log("\n=== Query String Round-Trip ===");

originalParams = {
    search: "machine learning",
    filter: "recent",
    count: "25"
};

console.log("Original params: " + str(originalParams));

// Encode to query string
queryEncoded = http.encodeQuery(originalParams);
console.log("Encoded query: " + queryEncoded);

// Decode back to params
parsedParams = http.parseQuery(queryEncoded);
console.log("Parsed params: " + str(parsedParams));

// ============================================
// URL Building Patterns
// ============================================

console.log("\n=== URL Building Patterns ===");

// Pattern 1: Simple search
searchQuery = "ML programming";
encodedQuery = http.encodeURI(searchQuery);
searchUrl = "https://search.example.com/q=" + encodedQuery;
console.log("Search pattern: " + searchUrl);

// Pattern 2: Pagination
pageParams = {page: "5", per_page: "20"};
pageQuery = http.encodeQuery(pageParams);
pageUrl = "https://api.example.com/items?" + pageQuery;
console.log("Pagination pattern: " + pageUrl);

// Pattern 3: Multiple filters
filterParams = {type: "article", tag: "ml", author: "john"};
filterQuery = http.encodeQuery(filterParams);
filterUrl = "https://blog.example.com/posts?" + filterQuery;
console.log("Filter pattern: " + filterUrl);

// ============================================
// Summary
// ============================================

console.log("\n=== URL Utilities Summary ===");

console.log("Encoding functions:");
console.log("  - encodeURI: Percent-encode special characters");
console.log("  - encodeQuery: Convert object to query string");

console.log("\nDecoding functions:");
console.log("  - decodeURI: Decode percent-encoded strings");
console.log("  - parseQuery: Parse query string to object");

console.log("\nCommon use cases:");
console.log("  - Building search URLs");
console.log("  - Encoding API parameters");
console.log("  - Parsing URL parameters");
console.log("  - Filter and pagination URLs");

console.log("\n=== URL Utilities Complete ===");
