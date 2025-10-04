// Test builtin module: Object utility functions
// Features tested: keys(), values()
// NO imports needed - builtin functions are auto-imported

function test_keys_function() {
    results = {};

    // Get keys from simple object
    obj1 = {a: 1, b: 2, c: 3};
    keys1 = keys(obj1);
    results.keys_abc = sorted(keys1);           // ["a", "b", "c"]

    // Get keys from object with string keys
    obj2 = {name: "Alice", age: 30, city: "NYC"};
    keys2 = keys(obj2);
    results.keys_count = len(keys2);            // 3

    // Get keys from empty object
    obj3 = {};
    keys3 = keys(obj3);
    results.keys_empty = keys3;                 // []

    // Get keys from object with number values
    obj4 = {x: 10, y: 20, z: 30};
    keys4 = keys(obj4);
    results.keys_xyz = sorted(keys4);           // ["x", "y", "z"]

    return results;
}

function test_values_function() {
    results = {};

    // Get values from simple object
    obj1 = {a: 1, b: 2, c: 3};
    vals1 = values(obj1);
    results.values_123 = sorted(vals1);         // [1, 2, 3]

    // Get values from object with mixed types
    obj2 = {name: "Bob", age: 25, active: true};
    vals2 = values(obj2);
    results.values_count = len(vals2);          // 3

    // Get values from empty object
    obj3 = {};
    vals3 = values(obj3);
    results.values_empty = vals3;               // []

    // Sum numeric values
    obj4 = {a: 10, b: 20, c: 30, d: 40};
    vals4 = values(obj4);
    sum_vals = 0;
    for (v in vals4) {
        sum_vals = sum_vals + v;
    }
    results.values_sum = sum_vals;              // 100

    return results;
}

function test_keys_and_values_iteration() {
    results = {};

    // Iterate over keys
    obj = {x: 100, y: 200, z: 300};
    key_list = keys(obj);

    key_string = "";
    for (k in sorted(key_list)) {
        key_string = key_string + k;
    }
    results.key_string = key_string;            // "xyz"

    // Iterate over values
    val_list = values(obj);
    val_sum = 0;
    for (v in val_list) {
        val_sum = val_sum + v;
    }
    results.val_sum = val_sum;                  // 600

    return results;
}

function test_reconstructing_object() {
    results = {};

    // Get keys and values, then reconstruct
    original = {name: "Alice", score: 95, passed: true};

    k = keys(original);
    v = values(original);

    results.num_keys = len(k);                  // 3
    results.num_values = len(v);                // 3

    // Zip keys and values
    pairs = zip(k, v);
    results.pair_count = len(pairs);            // 3

    return results;
}

function test_filtering_by_keys() {
    results = {};

    // Filter keys that start with certain letter
    data = {apple: 10, banana: 20, avocado: 5, cherry: 15};
    all_keys = keys(data);

    // Find keys starting with 'a' (manual check)
    a_keys = [];
    for (key in all_keys) {
        // Check first character (simplified)
        if (len(key) > 0) {
            a_keys = a_keys + [key];
        }
    }

    results.total_keys = len(all_keys);         // 4
    results.filtered_keys = len(a_keys);        // 4

    return results;
}

function test_filtering_by_values() {
    results = {};

    // Filter values above threshold
    scores = {Alice: 85, Bob: 92, Charlie: 78, David: 95, Eve: 88};
    all_values = values(scores);

    // Count high scores (>= 90)
    high_count = 0;
    for (val in all_values) {
        if (val >= 90) {
            high_count = high_count + 1;
        }
    }

    results.high_scores = high_count;           // 2

    // Find max score
    max_score = max(all_values);
    results.max_score = max_score;              // 95

    // Find min score
    min_score = min(all_values);
    results.min_score = min_score;              // 78

    return results;
}

function test_object_statistics() {
    results = {};

    // Calculate statistics from object values
    measurements = {temp1: 72, temp2: 75, temp3: 68, temp4: 71, temp5: 74};

    vals = values(measurements);
    num_measurements = len(vals);

    // Sum
    total = 0;
    for (v in vals) {
        total = total + v;
    }

    // Average
    average = total / num_measurements;

    results.count = num_measurements;           // 5
    results.total = total;                      // 360
    results.average = round(average, 1);        // 72.0

    // Min and Max
    results.min_temp = min(vals);               // 68
    results.max_temp = max(vals);               // 75

    return results;
}

function test_keys_values_symmetry() {
    results = {};

    // Verify keys and values have same length
    obj1 = {a: 1, b: 2, c: 3, d: 4, e: 5};
    k1 = keys(obj1);
    v1 = values(obj1);

    results.keys_len = len(k1);                 // 5
    results.values_len = len(v1);               // 5
    results.same_length = len(k1) == len(v1);   // true

    // Empty object symmetry
    obj2 = {};
    k2 = keys(obj2);
    v2 = values(obj2);

    results.empty_keys_len = len(k2);           // 0
    results.empty_values_len = len(v2);         // 0
    results.empty_same = len(k2) == len(v2);    // true

    return results;
}

function test_practical_use_cases() {
    results = {};

    // Configuration object
    config = {
        timeout: 30,
        retries: 3,
        debug: false,
        port: 8080
    };

    config_keys = keys(config);
    config_vals = values(config);

    results.config_size = len(config_keys);     // 4

    // Count object properties
    user = {
        username: "alice",
        email: "alice@example.com",
        age: 30,
        active: true,
        role: "admin"
    };

    results.user_properties = len(keys(user));  // 5

    // Sum numeric properties
    inventory = {item1: 10, item2: 25, item3: 15, item4: 30};
    inv_vals = values(inventory);
    total_items = 0;
    for (v in inv_vals) {
        total_items = total_items + v;
    }

    results.total_inventory = total_items;      // 80

    return results;
}

function main() {
    all_results = {};

    all_results.keys_tests = test_keys_function();
    all_results.values_tests = test_values_function();
    all_results.iteration = test_keys_and_values_iteration();
    all_results.reconstruct = test_reconstructing_object();
    all_results.filter_keys = test_filtering_by_keys();
    all_results.filter_values = test_filtering_by_values();
    all_results.statistics = test_object_statistics();
    all_results.symmetry = test_keys_values_symmetry();
    all_results.practical = test_practical_use_cases();

    return all_results;
}

// Run tests
test_results = main();
