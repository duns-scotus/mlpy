// Test stdlib module: regex - Match objects and group capturing
// Features tested: search(), match(), group(), groups(), groupDict(), position info
// Module: regex (version 2.0)

import regex;

function test_basic_matching() {
    results = {};

    // Basic search
    match = regex.search('\d+', "The answer is 42");
    if (match != null) {
        results.value = match.group(0);         // "42"
        results.start = match.start();          // 14
        results.end = match.end();              // 16
    }

    // Pattern not found
    no_match = regex.search('\d+', "No numbers here");
    results.no_match = no_match == null;        // true

    return results;
}

function test_group_capturing() {
    results = {};

    // Phone number pattern with groups
    pattern = regex.compile('(\d{3})-(\d{4})');
    match = pattern.search("Call 555-1234");

    if (match != null) {
        results.full = match.group(0);          // "555-1234"
        results.area = match.group(1);          // "555"
        results.number = match.group(2);        // "1234"
        results.all_groups = match.groups();    // ["555", "1234"]
        results.count = match.groupCount();     // 2
    }

    return results;
}

function test_named_groups() {
    results = {};

    // Date pattern with named groups
    pattern = regex.compile('(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})');
    match = pattern.search("Date: 2025-10-05");

    if (match != null) {
        results.year = match.group("yea");     // "2025"
        results.month = match.group("month");   // "10"
        results.day = match.group("day");       // "05"
        results.dict = match.groupDict();       // {year: "2025", month: "10", day: "05"}
    }

    return results;
}

function test_multiple_matches() {
    results = {};

    // Find all phone numbers
    pattern = regex.compile('(\d{3})-(\d{4})');
    matches = pattern.finditer("Call 555-1234 or 800-5678");

    results.match_count = len(matches);         // 2

    // First match
    if (len(matches) > 0) {
        match1 = matches[0];
        results.first_area = match1.group(1);   // "555"
        results.first_num = match1.group(2);    // "1234"
    }

    // Second match
    if (len(matches) > 1) {
        match2 = matches[1];
        results.second_area = match2.group(1);  // "800"
        results.second_num = match2.group(2);   // "5678"
    }

    return results;
}

function test_position_info() {
    results = {};

    // Multiple occurrences with position tracking
    pattern = regex.compile('\d+');
    matches = pattern.finditer("Item 10 costs 25 dollars");

    if (len(matches) >= 2) {
        match1 = matches[0];
        match2 = matches[1];

        results.first_value = match1.group(0);  // "10"
        results.first_start = match1.start();   // 5
        results.first_end = match1.end();       // 7
        results.first_span = match1.span();     // [5, 7]

        results.second_value = match2.group(0); // "25"
        results.second_start = match2.start();  // 14
        results.second_end = match2.end();      // 16
    }

    return results;
}

function test_match_vs_search() {
    results = {};

    // search() finds anywhere
    search_result = regex.search('\d+', "Text 42");
    results.search_found = search_result != null;   // true

    // match() only from start
    match_result = regex.match('\d+', "Text 42");
    results.match_found = match_result == null;     // true (no match at start)

    match_result2 = regex.match('\d+', "42 text");
    results.match_found2 = match_result2 != null;   // true (match at start)

    return results;
}

function test_fullmatch() {
    results = {};

    // fullmatch() requires entire string to match
    pattern = regex.compile('\d+');

    full1 = pattern.fullmatch("42");
    results.full_exact = full1 != null;             // true

    full2 = pattern.fullmatch("42 extra");
    results.full_partial = full2 == null;           // true

    full3 = pattern.fullmatch("text 42");
    results.full_prefix = full3 == null;            // true

    return results;
}

function test_nested_groups() {
    results = {};

    // Nested capturing groups
    pattern = regex.compile('((\\d{2})-(\\d{2}))-(\\d{4})');
    match = pattern.search("Date: 10-05-2025");

    if (match != null) {
        results.group0 = match.group(0);        // "10-05-2025"
        results.group1 = match.group(1);        // "10-05"
        results.group2 = match.group(2);        // "10"
        results.group3 = match.group(3);        // "05"
        results.group4 = match.group(4);        // "2025"
    }

    return results;
}

function main() {
    all_results = {};

    all_results.basic = test_basic_matching();
    all_results.groups = test_group_capturing();
    all_results.named = test_named_groups();
    all_results.multiple = test_multiple_matches();
    all_results.positions = test_position_info();
    all_results.match_search = test_match_vs_search();
    all_results.fullmatch = test_fullmatch();
    all_results.nested = test_nested_groups();

    return all_results;
}

// Run tests
test_results = main();
