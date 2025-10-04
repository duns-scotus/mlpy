// Test builtin module: String representation functions
// Features tested: repr(), format()
// NO imports needed - builtin functions are auto-imported

function test_repr_numbers() {
    results = {};

    // Integers
    results.repr_42 = repr(42);                      // "42"
    results.repr_0 = repr(0);                        // "0"
    results.repr_neg = repr(-100);                   // "-100"

    // Floats
    results.repr_float = repr(3.14);                 // "3.14"
    results.repr_float2 = repr(2.71828);             // "2.71828"

    return results;
}

function test_repr_booleans() {
    results = {};

    // ML-compatible boolean formatting (lowercase)
    results.repr_true = repr(true);                  // "true"
    results.repr_false = repr(false);                // "false"

    return results;
}

function test_repr_strings() {
    results = {};

    // String representation (with quotes)
    results.repr_hello = repr("hello");              // "'hello'"
    results.repr_empty = repr("");                   // "''"

    return results;
}

function test_format_floats() {
    results = {};

    // Format with precision
    results.format_pi_2 = format(3.14159, ".2f");    // "3.14"
    results.format_pi_3 = format(3.14159, ".3f");    // "3.142"
    results.format_e_4 = format(2.71828, ".4f");     // "2.7183"

    // Format with different precisions
    val = 123.456789;
    results.format_0 = format(val, ".0f");           // "123"
    results.format_1 = format(val, ".1f");           // "123.5"
    results.format_2 = format(val, ".2f");           // "123.46"

    return results;
}

function test_format_integers() {
    results = {};

    // Format with padding
    results.format_pad_5 = format(42, "05d");        // "00042"
    results.format_pad_3 = format(7, "03d");         // "007"
    results.format_pad_8 = format(123, "08d");       // "00000123"

    return results;
}

function test_format_hexadecimal() {
    results = {};

    // Format as hexadecimal
    results.format_hex_lower = format(255, "x");     // "ff"
    results.format_hex_upper = format(255, "X");     // "FF"

    results.format_hex_16 = format(16, "x");         // "10"
    results.format_hex_256 = format(256, "x");       // "100"

    return results;
}

function test_format_empty_spec() {
    results = {};

    // Empty format spec (default formatting)
    results.format_int_empty = format(42, "");       // "42"
    results.format_float_empty = format(3.14, "");   // "3.14"

    return results;
}

function test_repr_for_debugging() {
    results = {};

    // Use repr for debug output
    x = 42;
    y = 3.14;
    z = true;

    debug_info = {
        x_repr: repr(x),
        y_repr: repr(y),
        z_repr: repr(z)
    };

    results.x_repr = debug_info.x_repr;              // "42"
    results.y_repr = debug_info.y_repr;              // "3.14"
    results.z_repr = debug_info.z_repr;              // "true"

    return results;
}

function test_format_for_tables() {
    results = {};

    // Format numbers for table display
    prices = [9.99, 123.45, 1.50, 99.99];

    formatted = [];
    for (price in prices) {
        formatted = formatted + [format(price, ".2f")];
    }

    results.formatted_count = len(formatted);        // 4
    results.price_0 = formatted[0];                  // "9.99"
    results.price_1 = formatted[1];                  // "123.45"
    results.price_2 = formatted[2];                  // "1.50"

    return results;
}

function test_format_for_percentages() {
    results = {};

    // Format as percentages
    ratios = [0.75, 0.925, 0.333];

    percentages = [];
    for (r in ratios) {
        pct = r * 100;
        percentages = percentages + [format(pct, ".1f")];
    }

    results.pct_count = len(percentages);            // 3
    results.pct_0 = percentages[0];                  // "75.0"
    results.pct_1 = percentages[1];                  // "92.5"
    results.pct_2 = percentages[2];                  // "33.3"

    return results;
}

function test_format_scientific_display() {
    results = {};

    // Format large numbers with grouping (simulated)
    large = 1234567;

    // Format with different widths
    results.format_default = format(large, "");      // "1234567"

    return results;
}

function test_repr_and_format_combinations() {
    results = {};

    // Combine repr and format
    value = 3.14159;

    results.repr_val = repr(value);                  // "3.14159"
    results.format_2 = format(value, ".2f");         // "3.14"
    results.format_4 = format(value, ".4f");         // "3.1416"

    // Different representations of same number
    num = 42;
    results.repr_num = repr(num);                    // "42"
    results.format_padded = format(num, "05d");      // "00042"
    results.format_hex = format(num, "x");           // "2a"

    return results;
}

function test_format_for_alignment() {
    results = {};

    // Right-align numbers (simulated with padding)
    numbers = [5, 42, 123, 7];

    padded = [];
    for (n in numbers) {
        padded = padded + [format(n, "04d")];
    }

    results.padded_0 = padded[0];                    // "0005"
    results.padded_1 = padded[1];                    // "0042"
    results.padded_2 = padded[2];                    // "0123"
    results.padded_3 = padded[3];                    // "0007"

    return results;
}

function test_practical_formatting() {
    results = {};

    // Invoice formatting
    subtotal = 99.99;
    tax_rate = 0.08;
    tax = subtotal * tax_rate;
    total = subtotal + tax;

    results.subtotal_fmt = format(subtotal, ".2f");  // "99.99"
    results.tax_fmt = format(tax, ".2f");            // "8.00"
    results.total_fmt = format(total, ".2f");        // "107.99"

    // Temperature display
    temp_c = 23.456;
    results.temp_1 = format(temp_c, ".1f");          // "23.5"

    // Score display
    score = 0.875;
    score_pct = score * 100;
    results.score_fmt = format(score_pct, ".1f");    // "87.5"

    return results;
}

function main() {
    all_results = {};

    all_results.repr_numbers = test_repr_numbers();
    all_results.repr_booleans = test_repr_booleans();
    all_results.repr_strings = test_repr_strings();
    all_results.format_floats = test_format_floats();
    all_results.format_integers = test_format_integers();
    all_results.format_hex = test_format_hexadecimal();
    all_results.format_empty = test_format_empty_spec();
    all_results.repr_debug = test_repr_for_debugging();
    all_results.format_tables = test_format_for_tables();
    all_results.format_pct = test_format_for_percentages();
    all_results.scientific = test_format_scientific_display();
    all_results.combinations = test_repr_and_format_combinations();
    all_results.alignment = test_format_for_alignment();
    all_results.practical = test_practical_formatting();

    return all_results;
}

// Run tests
test_results = main();
