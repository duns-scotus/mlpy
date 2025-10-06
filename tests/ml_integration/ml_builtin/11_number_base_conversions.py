"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_hex_conversions():
    results = {}
    results['hex_0'] = _safe_call(builtin.hex, 0)
    results['hex_1'] = _safe_call(builtin.hex, 1)
    results['hex_10'] = _safe_call(builtin.hex, 10)
    results['hex_15'] = _safe_call(builtin.hex, 15)
    results['hex_16'] = _safe_call(builtin.hex, 16)
    results['hex_255'] = _safe_call(builtin.hex, 255)
    results['hex_256'] = _safe_call(builtin.hex, 256)
    results['hex_4096'] = _safe_call(builtin.hex, 4096)
    return results

def test_bin_conversions():
    results = {}
    results['bin_0'] = _safe_call(builtin.bin, 0)
    results['bin_1'] = _safe_call(builtin.bin, 1)
    results['bin_2'] = _safe_call(builtin.bin, 2)
    results['bin_3'] = _safe_call(builtin.bin, 3)
    results['bin_7'] = _safe_call(builtin.bin, 7)
    results['bin_8'] = _safe_call(builtin.bin, 8)
    results['bin_16'] = _safe_call(builtin.bin, 16)
    results['bin_32'] = _safe_call(builtin.bin, 32)
    results['bin_255'] = _safe_call(builtin.bin, 255)
    return results

def test_oct_conversions():
    results = {}
    results['oct_0'] = _safe_call(builtin.oct, 0)
    results['oct_1'] = _safe_call(builtin.oct, 1)
    results['oct_7'] = _safe_call(builtin.oct, 7)
    results['oct_8'] = _safe_call(builtin.oct, 8)
    results['oct_9'] = _safe_call(builtin.oct, 9)
    results['oct_64'] = _safe_call(builtin.oct, 64)
    results['oct_512'] = _safe_call(builtin.oct, 512)
    return results

def test_multiple_base_conversions():
    results = {}
    num = 42
    results['dec_42'] = num
    results['hex_42'] = _safe_call(builtin.hex, num)
    results['bin_42'] = _safe_call(builtin.bin, num)
    results['oct_42'] = _safe_call(builtin.oct, num)
    return results

def test_powers_of_two():
    results = {}
    pow2_8 = 256
    results['dec_256'] = pow2_8
    results['hex_256'] = _safe_call(builtin.hex, pow2_8)
    results['bin_256'] = _safe_call(builtin.bin, pow2_8)
    results['oct_256'] = _safe_call(builtin.oct, pow2_8)
    return results

def test_base_conversion_patterns():
    results = {}
    val_15 = 15
    results['bin_15'] = _safe_call(builtin.bin, val_15)
    results['hex_15'] = _safe_call(builtin.hex, val_15)
    val_31 = 31
    results['bin_31'] = _safe_call(builtin.bin, val_31)
    results['hex_31'] = _safe_call(builtin.hex, val_31)
    return results

def test_hexadecimal_digits():
    results = {}
    hex_vals = []
    for i in _safe_call(builtin.range, 16):
        hex_vals = (hex_vals + [_safe_call(builtin.hex, i)])
    results['hex_count'] = _safe_call(builtin.len, hex_vals)
    results['hex_0'] = hex_vals[0]
    results['hex_10'] = hex_vals[10]
    results['hex_15'] = hex_vals[15]
    return results

def test_large_number_conversions():
    results = {}
    large = 1000
    results['hex_1000'] = _safe_call(builtin.hex, large)
    results['bin_1000_len'] = _safe_call(builtin.len, _safe_call(builtin.bin, large))
    results['oct_1000'] = _safe_call(builtin.oct, large)
    return results

def test_conversion_in_calculations():
    results = {}
    flags = 255
    bin_repr = _safe_call(builtin.bin, flags)
    hex_repr = _safe_call(builtin.hex, flags)
    results['flags_bin'] = bin_repr
    results['flags_hex'] = hex_repr
    val = 12
    results['val_bin'] = _safe_call(builtin.bin, val)
    return results

def test_base_conversion_for_colors():
    results = {}
    red = 255
    green = 128
    blue = 64
    results['red_hex'] = _safe_call(builtin.hex, red)
    results['green_hex'] = _safe_call(builtin.hex, green)
    results['blue_hex'] = _safe_call(builtin.hex, blue)
    return results

def test_bit_representation():
    results = {}
    powers = [1, 2, 4, 8, 16, 32, 64, 128]
    bin_reps = []
    for p in powers:
        bin_reps = (bin_reps + [_safe_call(builtin.bin, p)])
    results['bin_count'] = _safe_call(builtin.len, bin_reps)
    results['bin_1'] = bin_reps[0]
    results['bin_128'] = bin_reps[7]
    return results

def main():
    all_results = {}
    all_results['hex_tests'] = test_hex_conversions()
    all_results['bin_tests'] = test_bin_conversions()
    all_results['oct_tests'] = test_oct_conversions()
    all_results['multi_base'] = test_multiple_base_conversions()
    all_results['powers_2'] = test_powers_of_two()
    all_results['patterns'] = test_base_conversion_patterns()
    all_results['hex_digits'] = test_hexadecimal_digits()
    all_results['large_nums'] = test_large_number_conversions()
    all_results['calculations'] = test_conversion_in_calculations()
    all_results['colors'] = test_base_conversion_for_colors()
    all_results['bit_repr'] = test_bit_representation()
    return all_results

test_results = main()

# End of generated code