// Test builtin module: Type conversion functions
// Features tested: int(), float(), str(), bool()
// NO imports needed - builtin functions are auto-imported

function test_int_conversion() {
    results = {};

    // Integer from float
    results.float_to_int = int(3.14);       // 3
    results.float_to_int2 = int(9.99);      // 9

    // Integer from string
    results.str_to_int = int("42");         // 42
    results.str_float_to_int = int("3.14"); // 3

    // Integer from boolean
    results.true_to_int = int(true);        // 1
    results.false_to_int = int(false);      // 0

    // Integer from integer
    results.int_to_int = int(100);          // 100

    // Error cases (should return 0)
    results.invalid_str = int("invalid");   // 0

    return results;
}

function test_float_conversion() {
    results = {};

    // Float from integer
    results.int_to_float = float(42);       // 42.0
    results.int_to_float2 = float(0);       // 0.0

    // Float from string
    results.str_to_float = float("3.14");   // 3.14
    results.str_to_float2 = float("42");    // 42.0

    // Float from boolean
    results.true_to_float = float(true);    // 1.0
    results.false_to_float = float(false);  // 0.0

    // Float from float
    results.float_to_float = float(3.14);   // 3.14

    // Error cases (should return 0.0)
    results.invalid_str = float("invalid"); // 0.0

    return results;
}

function test_str_conversion() {
    results = {};

    // String from integer
    results.int_to_str = str(42);           // "42"
    results.negative_int = str(-100);       // "-100"

    // String from float
    results.float_to_str = str(3.14);       // "3.14"

    // String from boolean (ML-compatible: lowercase)
    results.true_to_str = str(true);        // "true"
    results.false_to_str = str(false);      // "false"

    // String from string
    results.str_to_str = str("hello");      // "hello"

    return results;
}

function test_bool_conversion() {
    results = {};

    // Boolean from integer
    results.one_to_bool = bool(1);          // true
    results.zero_to_bool = bool(0);         // false
    results.pos_to_bool = bool(42);         // true
    results.neg_to_bool = bool(-1);         // true

    // Boolean from string
    results.str_to_bool = bool("hello");    // true
    results.empty_str_to_bool = bool("");   // false

    // Boolean from array
    results.array_to_bool = bool([1,2,3]);  // true
    results.empty_array = bool([]);         // false

    // Boolean from boolean
    results.true_to_bool = bool(true);      // true
    results.false_to_bool = bool(false);    // false

    return results;
}

function test_round_trip_conversions() {
    results = {};

    // int -> str -> int
    val1 = 42;
    val1_str = str(val1);
    val1_back = int(val1_str);
    results.int_roundtrip = val1_back;      // 42

    // float -> str -> float
    val2 = 3.14;
    val2_str = str(val2);
    val2_back = float(val2_str);
    results.float_roundtrip = val2_back;    // 3.14

    // bool -> int -> bool
    val3 = true;
    val3_int = int(val3);
    val3_back = bool(val3_int);
    results.bool_roundtrip = val3_back;     // true

    return results;
}

function main() {
    all_results = {};

    all_results.int_tests = test_int_conversion();
    all_results.float_tests = test_float_conversion();
    all_results.str_tests = test_str_conversion();
    all_results.bool_tests = test_bool_conversion();
    all_results.roundtrip = test_round_trip_conversions();

    return all_results;
}

// Run tests
test_results = main();
