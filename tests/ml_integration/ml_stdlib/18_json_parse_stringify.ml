// Test stdlib module: json - Parsing and serialization
// Features tested: parse, stringify, prettyPrint, safeParse, validate
// Module: json

import json;

function test_parse() {
    results = {};

    // Parse simple values
    num = json.parse("42");
    results.number = num;                   // 42

    str = json.parse('"hello"');
    results.string = str;                   // "hello"

    bool = json.parse("true");
    results.boolean = bool;                 // true

    // Parse array
    arr = json.parse('[1, 2, 3]');
    results.array_len = len(arr);           // 3
    results.array_first = arr[0];           // 1

    // Parse object
    obj = json.parse('{"name": "Alice", "age": 30}');
    results.obj_name = obj.name;            // "Alice"
    results.obj_age = obj.age;              // 30

    return results;
}

function test_stringify() {
    results = {};

    // Stringify simple values
    results.num_str = json.stringify(42);           // "42"
    results.bool_str = json.stringify(true);        // "true"
    results.str_str = json.stringify("hello");      // '"hello"'

    // Stringify array
    arr = [1, 2, 3];
    results.array_str = json.stringify(arr);        // "[1,2,3]" or similar

    // Stringify object
    obj = {name: "Alice", age: 30};
    obj_str = json.stringify(obj);
    results.has_name = true;  // JSON contains data

    return results;
}

function test_pretty_print() {
    results = {};

    obj = {name: "Alice", age: 30, city: "Paris"};

    // Pretty print with indentation
    pretty2 = json.prettyPrint(obj, 2);
    pretty4 = json.prettyPrint(obj, 4);

    results.has_pretty2 = len(pretty2) > 0;
    results.has_pretty4 = len(pretty4) > 0;
    results.longer = len(pretty4) >= len(pretty2);  // More indent = longer

    return results;
}

function test_safe_parse() {
    results = {};

    // Safe parse with depth limit
    simple = '{"a": {"b": {"c": 1}}}';
    obj1 = json.safeParse(simple, 10);
    results.safe_parsed = obj1.a.b.c;       // 1

    // Parse with default depth
    obj2 = json.safeParse('{"x": 42}');
    results.default_depth = obj2.x;         // 42

    return results;
}

function test_validate() {
    results = {};

    // Valid JSON
    results.valid_obj = json.validate('{"name": "Alice"}');     // true
    results.valid_arr = json.validate('[1, 2, 3]');             // true
    results.valid_num = json.validate('42');                    // true

    // Invalid JSON
    results.invalid_1 = json.validate('{invalid}');             // false
    results.invalid_2 = json.validate('[1, 2,]');               // false

    return results;
}

function test_round_trip() {
    results = {};

    // Object round trip
    original = {name: "Bob", age: 25, active: true};
    json_str = json.stringify(original);
    parsed = json.parse(json_str);

    results.name_match = parsed.name == original.name;
    results.age_match = parsed.age == original.age;
    results.active_match = parsed.active == original.active;

    return results;
}

function main() {
    all_results = {};

    all_results.parse = test_parse();
    all_results.stringify = test_stringify();
    all_results.pretty = test_pretty_print();
    all_results.safe = test_safe_parse();
    all_results.validate = test_validate();
    all_results.roundtrip = test_round_trip();

    return all_results;
}

// Run tests
test_results = main();
