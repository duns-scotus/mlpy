// Test builtin module: Number base conversion functions
// Features tested: hex(), bin(), oct()
// NO imports needed - builtin functions are auto-imported

function test_hex_conversions() {
    results = {};

    // Basic hex conversions
    results.hex_0 = hex(0);                      // "0x0"
    results.hex_1 = hex(1);                      // "0x1"
    results.hex_10 = hex(10);                    // "0xa"
    results.hex_15 = hex(15);                    // "0xf"
    results.hex_16 = hex(16);                    // "0x10"
    results.hex_255 = hex(255);                  // "0xff"

    // Powers of 16
    results.hex_256 = hex(256);                  // "0x100"
    results.hex_4096 = hex(4096);                // "0x1000"

    return results;
}

function test_bin_conversions() {
    results = {};

    // Basic binary conversions
    results.bin_0 = bin(0);                      // "0b0"
    results.bin_1 = bin(1);                      // "0b1"
    results.bin_2 = bin(2);                      // "0b10"
    results.bin_3 = bin(3);                      // "0b11"
    results.bin_7 = bin(7);                      // "0b111"
    results.bin_8 = bin(8);                      // "0b1000"

    // Powers of 2
    results.bin_16 = bin(16);                    // "0b10000"
    results.bin_32 = bin(32);                    // "0b100000"
    results.bin_255 = bin(255);                  // "0b11111111"

    return results;
}

function test_oct_conversions() {
    results = {};

    // Basic octal conversions
    results.oct_0 = oct(0);                      // "0o0"
    results.oct_1 = oct(1);                      // "0o1"
    results.oct_7 = oct(7);                      // "0o7"
    results.oct_8 = oct(8);                      // "0o10"
    results.oct_9 = oct(9);                      // "0o11"
    results.oct_64 = oct(64);                    // "0o100"

    // Powers of 8
    results.oct_512 = oct(512);                  // "0o1000"

    return results;
}

function test_multiple_base_conversions() {
    results = {};

    // Same number in different bases
    num = 42;

    results.dec_42 = num;                        // 42
    results.hex_42 = hex(num);                   // "0x2a"
    results.bin_42 = bin(num);                   // "0b101010"
    results.oct_42 = oct(num);                   // "0o52"

    return results;
}

function test_powers_of_two() {
    results = {};

    // Powers of 2 in different bases
    pow2_8 = 256;  // 2^8

    results.dec_256 = pow2_8;                    // 256
    results.hex_256 = hex(pow2_8);               // "0x100"
    results.bin_256 = bin(pow2_8);               // "0b100000000"
    results.oct_256 = oct(pow2_8);               // "0o400"

    return results;
}

function test_base_conversion_patterns() {
    results = {};

    // All 1s in binary (2^n - 1)
    val_15 = 15;  // 1111 in binary
    results.bin_15 = bin(val_15);                // "0b1111"
    results.hex_15 = hex(val_15);                // "0xf"

    val_31 = 31;  // 11111 in binary
    results.bin_31 = bin(val_31);                // "0b11111"
    results.hex_31 = hex(val_31);                // "0x1f"

    return results;
}

function test_hexadecimal_digits() {
    results = {};

    // Test all hex digits (0-15)
    hex_vals = [];
    for (i in range(16)) {
        hex_vals = hex_vals + [hex(i)];
    }

    results.hex_count = len(hex_vals);           // 16
    results.hex_0 = hex_vals[0];                 // "0x0"
    results.hex_10 = hex_vals[10];               // "0xa"
    results.hex_15 = hex_vals[15];               // "0xf"

    return results;
}

function test_large_number_conversions() {
    results = {};

    // Larger numbers
    large = 1000;

    results.hex_1000 = hex(large);               // "0x3e8"
    results.bin_1000_len = len(bin(large));      // Should be > 10 ("0b" + digits)
    results.oct_1000 = oct(large);               // "0o1750"

    return results;
}

function test_conversion_in_calculations() {
    results = {};

    // Use base conversions for debugging/display
    flags = 255;  // All bits set for first byte

    bin_repr = bin(flags);
    hex_repr = hex(flags);

    results.flags_bin = bin_repr;                // "0b11111111"
    results.flags_hex = hex_repr;                // "0xff"

    // Bit manipulation example (visual)
    val = 12;  // 1100 in binary
    results.val_bin = bin(val);                  // "0b1100"

    return results;
}

function test_base_conversion_for_colors() {
    results = {};

    // RGB color components (0-255)
    red = 255;
    green = 128;
    blue = 64;

    results.red_hex = hex(red);                  // "0xff"
    results.green_hex = hex(green);              // "0x80"
    results.blue_hex = hex(blue);                // "0x40"

    // Full color would be "#FF8040" in web colors
    // (simplified demonstration)

    return results;
}

function test_bit_representation() {
    results = {};

    // Show bit patterns
    powers = [1, 2, 4, 8, 16, 32, 64, 128];

    bin_reps = [];
    for (p in powers) {
        bin_reps = bin_reps + [bin(p)];
    }

    results.bin_count = len(bin_reps);           // 8
    results.bin_1 = bin_reps[0];                 // "0b1"
    results.bin_128 = bin_reps[7];               // "0b10000000"

    return results;
}

function main() {
    all_results = {};

    all_results.hex_tests = test_hex_conversions();
    all_results.bin_tests = test_bin_conversions();
    all_results.oct_tests = test_oct_conversions();
    all_results.multi_base = test_multiple_base_conversions();
    all_results.powers_2 = test_powers_of_two();
    all_results.patterns = test_base_conversion_patterns();
    all_results.hex_digits = test_hexadecimal_digits();
    all_results.large_nums = test_large_number_conversions();
    all_results.calculations = test_conversion_in_calculations();
    all_results.colors = test_base_conversion_for_colors();
    all_results.bit_repr = test_bit_representation();

    return all_results;
}

// Run tests
test_results = main();
