// Test stdlib module: regex - Flags and advanced matching
// Features tested: IGNORECASE, MULTILINE, DOTALL, flag combinations
// Module: regex (version 2.0)

import regex;

function test_ignore_case() {
    results = {};

    // Case-insensitive matching
    pattern = regex.compile('hello', regex.IGNORECASE());

    match1 = pattern.search("hello world");
    match2 = pattern.search("HELLO WORLD");
    match3 = pattern.search("Hello World");
    match4 = pattern.search("HeLLo WoRLd");

    results.lower = match1 != null;             // true
    results.upper = match2 != null;             // true
    results.title = match3 != null;             // true
    results.mixed = match4 != null;             // true

    return results;
}

function test_multiline() {
    results = {};

    text = "INFO: Starting\nERROR: Failed\nWARN: Retry\nERROR: Timeout";

    // Without MULTILINE, ^ only matches at string start
    pattern_normal = regex.compile('^ERROR');
    matches_normal = pattern_normal.findall(text);
    results.normal_count = len(matches_normal);  // 0 or 1

    // With MULTILINE, ^ matches at line boundaries
    pattern_multi = regex.compile('^ERROR', regex.MULTILINE());
    matches_multi = pattern_multi.findall(text);
    results.multi_count = len(matches_multi);    // 2

    return results;
}

function test_dotall() {
    results = {};

    html = "<div>\nContent\nHere\n</div>";

    // Without DOTALL, . doesn't match newlines
    pattern_normal = regex.compile('<div>.*</div>');
    match_normal = pattern_normal.search(html);
    results.normal_match = match_normal == null;  // true (no match)

    // With DOTALL, . matches everything including newlines
    pattern_dotall = regex.compile('<div>.*</div>', regex.DOTALL());
    match_dotall = pattern_dotall.search(html);
    results.dotall_match = match_dotall != null;  // true

    return results;
}

function test_combined_flags() {
    results = {};

    text = "error: failed\nERROR: timeout\nWarn: retry";

    // Combine IGNORECASE and MULTILINE
    flags = regex.IGNORECASE() | regex.MULTILINE();
    pattern = regex.compile('^erro', flags);

    matches = pattern.findall(text);
    results.match_count = len(matches);          // 2 (both error lines)

    return results;
}

function test_pattern_operations() {
    results = {};

    pattern = regex.compile('\d+');

    // Test
    results.test_true = pattern.test("Number 42");   // true
    results.test_false = pattern.test("No digits");  // false

    // Count
    results.count = pattern.count("I have 5 apples and 3 oranges");  // 2

    // Get pattern string
    results.pattern_str = pattern.getPattern();      // '\d+'

    return results;
}

function test_findall_vs_finditer() {
    results = {};

    text = "Numbers: 10, 20, 30";
    pattern = regex.compile('\d+');

    // findall returns strings
    strings = pattern.findall(text);
    results.findall_count = len(strings);            // 3
    results.findall_first = strings[0];              // "10"

    // finditer returns Match objects
    matches = pattern.finditer(text);
    results.finditer_count = len(matches);           // 3

    if (len(matches) > 0) {
        first_match = matches[0];
        results.finditer_value = first_match.group(0);  // "10"
        results.finditer_start = first_match.start();   // 9
    }

    return results;
}

function test_split() {
    results = {};

    pattern = regex.compile('[,;]');

    // Split by comma or semicolon
    parts = pattern.split("a,b;c,d");
    results.split_count = len(parts);            // 4
    results.split_first = parts[0];              // "a"
    results.split_last = parts[3];               // "d"

    // Split with maxsplit
    parts2 = pattern.split("a,b,c,d", 2);
    results.maxsplit_count = len(parts2);        // 3

    return results;
}

function test_sub_and_subn() {
    results = {};

    pattern = regex.compile('\d+');

    // sub - replace all matches
    text1 = "I have 5 apples and 3 oranges";
    replaced = pattern.sub("X", text1);
    results.sub_result = replaced;               // "I have X apples and X oranges"

    // subn - replace with count
    result_obj = pattern.subn("X", text1);
    results.subn_text = result_obj.result;       // "I have X apples and X oranges"
    results.subn_count = result_obj.count;       // 2

    // sub with count limit
    replaced2 = pattern.sub("X", text1, 1);
    results.sub_limited = replaced2;             // "I have X apples and 3 oranges"

    return results;
}

function main() {
    all_results = {};

    all_results.ignorecase = test_ignore_case();
    all_results.multiline = test_multiline();
    all_results.dotall = test_dotall();
    all_results.combined = test_combined_flags();
    all_results.operations = test_pattern_operations();
    all_results.find_methods = test_findall_vs_finditer();
    all_results.split = test_split();
    all_results.substitution = test_sub_and_subn();

    return all_results;
}

// Run tests
test_results = main();
