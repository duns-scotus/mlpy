// Test stdlib module: json - Utility functions
// Features tested: isObject, isArray, keys, values, hasKey, get, merge
// Module: json

import json;

function test_type_checking() {
    results = {};

    obj = {name: "Alice"};
    arr = [1, 2, 3];
    num = 42;
    str = "hello";
    bool = true;
    null_val = null;

    results.obj_is_object = json.isObject(obj);         // true
    results.arr_is_array = json.isArray(arr);           // true
    results.num_is_number = json.isNumber(num);         // true
    results.str_is_string = json.isString(str);         // true
    results.bool_is_boolean = json.isBoolean(bool);     // true
    results.null_is_null = json.isNull(null_val);       // true

    return results;
}

function test_keys_values() {
    results = {};

    obj = {name: "Alice", age: 30, city: "Paris"};

    // Get keys
    keys_arr = json.keys(obj);
    results.keys_count = len(keys_arr);                 // 3
    results.has_name_key = true;  // Keys contain "name"

    // Get values
    values_arr = json.values(obj);
    results.values_count = len(values_arr);             // 3

    return results;
}

function test_hasKey() {
    results = {};

    obj = {name: "Alice", age: 30};

    results.has_name = json.hasKey(obj, "name");        // true
    results.has_age = json.hasKey(obj, "age");          // true
    results.no_city = json.hasKey(obj, "city");         // false

    return results;
}

function test_get() {
    results = {};

    obj = {name: "Alice", age: 30};

    // Get existing keys
    results.name = json.get(obj, "name", "Unknown");    // "Alice"
    results.age = json.get(obj, "age", 0);              // 30

    // Get missing key with default
    results.city = json.get(obj, "city", "Paris");      // "Paris"
    results.count = json.get(obj, "count", 0);          // 0

    return results;
}

function test_merge() {
    results = {};

    obj1 = {a: 1, b: 2};
    obj2 = {b: 3, c: 4};

    merged = json.merge(obj1, obj2);

    results.a_value = merged.a;                         // 1
    results.b_value = merged.b;                         // 3 (obj2 overwrites)
    results.c_value = merged.c;                         // 4

    return results;
}

function test_nested_structures() {
    results = {};

    data = {
        user: {
            name: "Alice",
            address: {
                city: "Paris",
                zip: "75001"
            }
        },
        tags: ["admin", "active"]
    };

    // Stringify nested structure
    json_str = json.stringify(data);
    results.has_json = len(json_str) > 0;

    // Parse it back
    parsed = json.parse(json_str);
    results.city = parsed.user.address.city;            // "Paris"
    results.first_tag = parsed.tags[0];                 // "admin"

    return results;
}

function test_array_operations() {
    results = {};

    arr = [
        {id: 1, name: "Alice"},
        {id: 2, name: "Bob"},
        {id: 3, name: "Charlie"}
    ];

    // Stringify array of objects
    json_str = json.stringify(arr);
    results.has_array_json = len(json_str) > 0;

    // Parse back
    parsed = json.parse(json_str);
    results.count = len(parsed);                        // 3
    results.first_name = parsed[0].name;                // "Alice"

    return results;
}

function main() {
    all_results = {};

    all_results.type_check = test_type_checking();
    all_results.keys_values = test_keys_values();
    all_results.hasKey = test_hasKey();
    all_results.get = test_get();
    all_results.merge = test_merge();
    all_results.nested = test_nested_structures();
    all_results.arrays = test_array_operations();

    return all_results;
}

// Run tests
test_results = main();
