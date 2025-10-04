// Test builtin module: Comprehensive integration test
// Features tested: ALL builtin functions working together
// NO imports needed - builtin functions are auto-imported

function test_data_processing_pipeline() {
    results = {};

    // Raw data
    raw_scores = [85, 92, 78, 95, 88, 73, 91, 82, 87, 94];

    // Statistics
    total = sum(raw_scores);
    count = len(raw_scores);
    average = total / count;

    results.total = total;                                      // 865
    results.count = count;                                      // 10
    results.average = round(average, 1);                        // 86.5

    // Min and Max
    results.min_score = min(raw_scores);                        // 73
    results.max_score = max(raw_scores);                        // 95
    results.range = max(raw_scores) - min(raw_scores);          // 22

    // Sorted scores
    sorted_scores = sorted(raw_scores);
    results.sorted_first = sorted_scores[0];                    // 73
    results.sorted_last = sorted_scores[count - 1];             // 95

    // Top 3 scores
    top_3 = reversed(sorted(raw_scores));
    results.rank_1 = top_3[0];                                  // 95
    results.rank_2 = top_3[1];                                  // 94
    results.rank_3 = top_3[2];                                  // 92

    return results;
}

function test_text_processing_pipeline() {
    results = {};

    // Process text data
    message = "HELLO";

    // Length and type
    results.msg_len = len(message);                             // 5
    results.msg_type = typeof(message);                         // "string"

    // Convert to array of char codes
    char_codes = [];
    for (i in range(len(message))) {
        // Manually get character at position (simplified)
        char_codes = char_codes + [ord("H")];  // Simplified
    }

    results.code_count = len(char_codes);                       // 5

    // Build string from codes
    first_code = ord("H");
    results.first_char = chr(first_code);                       // "H"

    return results;
}

function test_numerical_transformations() {
    results = {};

    // Generate sequence
    sequence = range(1, 11);  // [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    // Transform: square each number
    squares = [];
    for (n in sequence) {
        squares = squares + [(n * n)];
    }

    // Statistics on squares
    results.sum_squares = sum(squares);                         // 385
    results.min_square = min(squares);                          // 1
    results.max_square = max(squares);                          // 100

    // Convert to different representations
    sample = 42;
    results.dec = sample;                                       // 42
    results.hex = hex(sample);                                  // "0x2a"
    results.bin = bin(sample);                                  // "0b101010"
    results.oct = oct(sample);                                  // "0o52"

    return results;
}

function test_collection_operations() {
    results = {};

    // Create collections
    numbers = [3, 1, 4, 1, 5, 9, 2, 6];
    letters = ["d", "a", "c", "b"];

    // Array operations
    results.num_len = len(numbers);                             // 8
    results.letter_len = len(letters);                          // 4

    // Sort both
    sorted_nums = sorted(numbers);
    sorted_letters = sorted(letters);

    results.nums_sorted = sorted_nums;                          // [1, 1, 2, 3, 4, 5, 6, 9]
    results.letters_sorted = sorted_letters;                    // ["a", "b", "c", "d"]

    // Reverse
    results.nums_reversed = reversed([1, 2, 3]);                // [3, 2, 1]

    // Enumerate
    enum_letters = enumerate(letters);
    results.enum_len = len(enum_letters);                       // 4

    return results;
}

function test_object_manipulation() {
    results = {};

    // Create object
    person = {
        name: "Alice",
        age: 30,
        city: "NYC",
        active: true
    };

    // Object operations
    all_keys = keys(person);
    all_values = values(person);

    results.key_count = len(all_keys);                          // 4
    results.value_count = len(all_values);                      // 4

    // Type checking
    results.obj_type = typeof(person);                          // "object"
    results.isinstance_obj = isinstance(person, "object");      // true

    return results;
}

function test_mathematical_computations() {
    results = {};

    // Complex calculations
    values = [-5, 3, -2, 7, -1, 4, -3, 8];

    // Absolute values
    abs_values = [];
    for (v in values) {
        abs_values = abs_values + [abs(v)];
    }

    // Statistics
    results.sum_abs = sum(abs_values);                          // 33
    results.min_abs = min(abs_values);                          // 1
    results.max_abs = max(abs_values);                          // 8

    // Rounding
    pi = 3.14159;
    results.pi_0 = round(pi, 0);                                // 3.0
    results.pi_2 = round(pi, 2);                                // 3.14
    results.pi_4 = round(pi, 4);                                // 3.1416

    return results;
}

function test_predicate_filtering() {
    results = {};

    // Filter with predicates
    data = [1, 0, 5, 0, 3, 0, 7];

    // Check if all non-zero
    checks = [];
    for (d in data) {
        checks = checks + [d != 0];
    }
    results.all_nonzero = all(checks);                          // false

    // Check if any non-zero
    results.any_nonzero = any(checks);                          // true

    // Count non-zero
    nonzero_count = 0;
    for (d in data) {
        if (d != 0) {
            nonzero_count = nonzero_count + 1;
        }
    }
    results.nonzero_count = nonzero_count;                      // 4

    return results;
}

function test_string_formatting_pipeline() {
    results = {};

    // Format various values
    price = 99.99;
    quantity = 5;
    discount = 0.15;

    // Format for display
    results.price_fmt = format(price, ".2f");                   // "99.99"
    results.qty_fmt = format(quantity, "03d");                  // "005"

    // Calculate with rounding
    subtotal = price * quantity;
    discount_amount = subtotal * discount;
    total = subtotal - discount_amount;

    results.subtotal = round(subtotal, 2);                      // 499.95
    results.discount = round(discount_amount, 2);               // 75.00 (approx)
    results.total = round(total, 2);                            // 424.96 (approx)

    return results;
}

function test_functional_composition() {
    results = {};

    // Compose operations
    input = [1, 2, 3, 4, 5];

    // Map: square each
    squared = [];
    for (n in input) {
        squared = squared + [(n * n)];
    }

    // Filter: only even
    even_squared = [];
    for (s in squared) {
        if ((s - (s / 2) * 2) == 0) {
            even_squared = even_squared + [s];
        }
    }

    // Reduce: sum
    total = sum(even_squared);

    results.squared = squared;                                  // [1, 4, 9, 16, 25]
    results.even_squared = even_squared;                        // [4, 16]
    results.total = total;                                      // 20

    return results;
}

function test_type_conversions_pipeline() {
    results = {};

    // Convert through various types
    start = "42";

    // String -> Int
    as_int = int(start);
    results.as_int = as_int;                                    // 42

    // Int -> Float
    as_float = float(as_int);
    results.as_float = as_float;                                // 42.0

    // Float -> String
    as_str = str(as_float);
    results.as_str = as_str;                                    // "42.0"

    // String -> Bool (non-empty)
    as_bool = bool(as_str);
    results.as_bool = as_bool;                                  // true

    // Bool -> Int
    as_int2 = int(as_bool);
    results.as_int2 = as_int2;                                  // 1

    return results;
}

function test_real_world_scenario() {
    results = {};

    // Shopping cart scenario
    items = [
        {name: "Book", price: 19.99, qty: 2},
        {name: "Pen", price: 2.50, qty: 5},
        {name: "Notebook", price: 5.99, qty: 3}
    ];

    // Extract prices
    prices = [19.99, 2.50, 5.99];
    quantities = [2, 5, 3];

    // Calculate line totals
    line_totals = [];
    pairs = zip(prices, quantities);
    for (pair in pairs) {
        price = pair[0];
        qty = pair[1];
        line_totals = line_totals + [(price * qty)];
    }

    // Calculate totals
    subtotal = sum(line_totals);
    tax_rate = 0.08;
    tax = subtotal * tax_rate;
    grand_total = subtotal + tax;

    results.subtotal = round(subtotal, 2);                      // 70.43
    results.tax = round(tax, 2);                                // 5.63
    results.total = round(grand_total, 2);                      // 76.06
    results.item_count = len(items);                            // 3

    return results;
}

function main() {
    all_results = {};

    print("=== Comprehensive Integration Tests ===");

    all_results.data_proc = test_data_processing_pipeline();
    all_results.text_proc = test_text_processing_pipeline();
    all_results.num_transform = test_numerical_transformations();
    all_results.collections = test_collection_operations();
    all_results.objects = test_object_manipulation();
    all_results.math = test_mathematical_computations();
    all_results.predicates = test_predicate_filtering();
    all_results.formatting = test_string_formatting_pipeline();
    all_results.functional = test_functional_composition();
    all_results.type_conv = test_type_conversions_pipeline();
    all_results.real_world = test_real_world_scenario();

    print("=== All Integration Tests Complete ===");

    return all_results;
}

// Run tests
test_results = main();
