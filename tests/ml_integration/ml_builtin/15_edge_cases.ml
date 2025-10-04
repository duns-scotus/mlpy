// Test builtin module: Edge cases and error handling
// Features tested: Error handling, boundary conditions, edge cases
// NO imports needed - builtin functions are auto-imported

function test_empty_collections() {
    results = {};

    // Empty arrays
    results.len_empty = len([]);                                // 0
    results.sum_empty = sum([]);                                // 0
    results.all_empty = all([]);                                // true (vacuous truth)
    results.any_empty = any([]);                                // false
    results.sorted_empty = sorted([]);                          // []
    results.reversed_empty = reversed([]);                      // []

    // Empty strings
    results.len_empty_str = len("");                            // 0

    // Empty objects
    results.keys_empty = keys({});                              // []
    results.values_empty = values({});                          // []

    return results;
}

function test_single_element_collections() {
    results = {};

    // Single element arrays
    results.len_single = len([42]);                             // 1
    results.sum_single = sum([42]);                             // 42
    results.all_single = all([true]);                           // true
    results.any_single = any([true]);                           // true
    results.sorted_single = sorted([42]);                       // [42]
    results.reversed_single = reversed([42]);                   // [42]
    results.min_single = min([42]);                             // 42
    results.max_single = max([42]);                             // 42

    return results;
}

function test_type_conversion_edge_cases() {
    results = {};

    // Zero conversions
    results.int_zero = int(0);                                  // 0
    results.float_zero = float(0);                              // 0.0
    results.bool_zero = bool(0);                                // false

    // Boolean conversions
    results.int_true = int(true);                               // 1
    results.int_false = int(false);                             // 0
    results.float_true = float(true);                           // 1.0
    results.float_false = float(false);                         // 0.0

    // String conversions
    results.str_true = str(true);                               // "true"
    results.str_false = str(false);                             // "false"
    results.str_zero = str(0);                                  // "0"

    return results;
}

function test_math_operations_edge_cases() {
    results = {};

    // Absolute value of zero
    results.abs_zero = abs(0);                                  // 0
    results.abs_zero_float = abs(0.0);                          // 0.0

    // Min/Max with duplicates
    results.min_dups = min([3, 1, 1, 2, 3]);                    // 1
    results.max_dups = max([3, 1, 1, 2, 3]);                    // 3

    // Round of integers
    results.round_int = round(42);                              // 42.0
    results.round_zero = round(0);                              // 0.0

    return results;
}

function test_range_edge_cases() {
    results = {};

    // Range with zero
    results.range_zero = range(0);                              // []

    // Range with one
    results.range_one = range(1);                               // [0]

    // Range with equal start and stop
    results.range_equal = range(5, 5);                          // []

    return results;
}

function test_boundary_values() {
    results = {};

    // Very large numbers
    large = 1000000;
    results.large_int = int(large);                             // 1000000
    results.large_str = len(str(large));                        // 7 (length of "1000000")

    // Very small numbers (near zero)
    small = 0.0001;
    results.small_float = float(small);                         // 0.0001

    return results;
}

function test_typeof_edge_cases() {
    results = {};

    // Type of zero
    results.typeof_zero = typeof(0);                            // "number"

    // Type of empty string
    results.typeof_empty_str = typeof("");                      // "string"

    // Type of empty array
    results.typeof_empty_arr = typeof([]);                      // "array"

    // Type of empty object
    results.typeof_empty_obj = typeof({});                      // "object"

    // Type of false
    results.typeof_false = typeof(false);                       // "boolean"

    return results;
}

function test_comparison_edge_cases() {
    results = {};

    // Zero comparisons
    results.zero_eq_false = (0 == false);                       // false (different types)
    results.zero_bool = bool(0);                                // false

    // Empty string comparisons
    results.empty_bool = bool("");                              // false

    return results;
}

function test_array_operations_edge_cases() {
    results = {};

    // Zip with mismatched lengths
    short = [1, 2];
    long = [10, 20, 30, 40];
    results.zip_mismatch = zip(short, long);                    // [(1,10), (2,20)]

    // Sorted with duplicates
    dups = [3, 1, 2, 3, 1, 2];
    results.sorted_dups = sorted(dups);                         // [1, 1, 2, 2, 3, 3]

    // Enumerate empty array
    results.enum_empty = enumerate([]);                         // []

    return results;
}

function test_string_edge_cases() {
    results = {};

    // Character conversions at boundaries
    results.chr_0 = len(chr(0));                                // 1 (null character)
    results.ord_space = ord(" ");                               // 32

    // Empty string operations
    results.reversed_empty_str = reversed("");                  // []

    return results;
}

function test_mixed_type_operations() {
    results = {};

    // All with mixed types
    results.all_mixed = all([1, "hello", true]);                // true
    results.any_mixed = any([0, "", 1]);                        // true

    // Sum with mixed int/float
    results.sum_mixed = sum([1, 2.5, 3]);                       // 6.5

    return results;
}

function test_predicate_edge_cases() {
    results = {};

    // All with single false
    results.all_one_false = all([true, true, false]);           // false

    // Any with single true
    results.any_one_true = any([false, false, true]);           // true

    // Callable with various types
    results.callable_int = callable(42);                        // false
    results.callable_str = callable("hello");                   // false

    return results;
}

function test_format_edge_cases() {
    results = {};

    // Format with zero padding
    results.format_zero = format(0, "05d");                     // "00000"

    // Format with precision 0
    results.format_prec_0 = format(3.14, ".0f");                // "3"

    // Format with empty spec
    results.format_empty = format(42, "");                      // "42"

    return results;
}

function test_combined_edge_cases() {
    results = {};

    // Empty array statistics
    empty_arr = [];
    if (len(empty_arr) == 0) {
        results.empty_handled = true;                           // true
    }

    // Single value statistics
    single = [42];
    results.single_sum = sum(single);                           // 42
    results.single_min = min(single);                           // 42
    results.single_max = min(single);                           // 42

    // All zeros
    zeros = [0, 0, 0];
    results.sum_zeros = sum(zeros);                             // 0
    results.any_zeros = any(zeros);                             // false
    results.all_zeros = all(zeros);                             // false

    return results;
}

function main() {
    all_results = {};

    all_results.empty = test_empty_collections();
    all_results.single = test_single_element_collections();
    all_results.type_conv = test_type_conversion_edge_cases();
    all_results.math = test_math_operations_edge_cases();
    all_results.range = test_range_edge_cases();
    all_results.boundaries = test_boundary_values();
    all_results.typeof = test_typeof_edge_cases();
    all_results.comparisons = test_comparison_edge_cases();
    all_results.arrays = test_array_operations_edge_cases();
    all_results.strings = test_string_edge_cases();
    all_results.mixed_types = test_mixed_type_operations();
    all_results.predicates = test_predicate_edge_cases();
    all_results.format = test_format_edge_cases();
    all_results.combined = test_combined_edge_cases();

    return all_results;
}

// Run tests
test_results = main();
