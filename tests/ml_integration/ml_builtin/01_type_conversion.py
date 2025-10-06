"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_int_conversion():
    results = {}
    results['float_to_int'] = _safe_call(builtin.int, 3.14)
    results['float_to_int2'] = _safe_call(builtin.int, 9.99)
    results['str_to_int'] = _safe_call(builtin.int, '42')
    results['str_float_to_int'] = _safe_call(builtin.int, '3.14')
    results['true_to_int'] = _safe_call(builtin.int, True)
    results['false_to_int'] = _safe_call(builtin.int, False)
    results['int_to_int'] = _safe_call(builtin.int, 100)
    results['invalid_str'] = _safe_call(builtin.int, 'invalid')
    return results

def test_float_conversion():
    results = {}
    results['int_to_float'] = _safe_call(builtin.float, 42)
    results['int_to_float2'] = _safe_call(builtin.float, 0)
    results['str_to_float'] = _safe_call(builtin.float, '3.14')
    results['str_to_float2'] = _safe_call(builtin.float, '42')
    results['true_to_float'] = _safe_call(builtin.float, True)
    results['false_to_float'] = _safe_call(builtin.float, False)
    results['float_to_float'] = _safe_call(builtin.float, 3.14)
    results['invalid_str'] = _safe_call(builtin.float, 'invalid')
    return results

def test_str_conversion():
    results = {}
    results['int_to_str'] = _safe_call(builtin.str, 42)
    results['negative_int'] = _safe_call(builtin.str, -100)
    results['float_to_str'] = _safe_call(builtin.str, 3.14)
    results['true_to_str'] = _safe_call(builtin.str, True)
    results['false_to_str'] = _safe_call(builtin.str, False)
    results['str_to_str'] = _safe_call(builtin.str, 'hello')
    return results

def test_bool_conversion():
    results = {}
    results['one_to_bool'] = _safe_call(builtin.bool, 1)
    results['zero_to_bool'] = _safe_call(builtin.bool, 0)
    results['pos_to_bool'] = _safe_call(builtin.bool, 42)
    results['neg_to_bool'] = _safe_call(builtin.bool, -1)
    results['str_to_bool'] = _safe_call(builtin.bool, 'hello')
    results['empty_str_to_bool'] = _safe_call(builtin.bool, '')
    results['array_to_bool'] = _safe_call(builtin.bool, [1, 2, 3])
    results['empty_array'] = _safe_call(builtin.bool, [])
    results['true_to_bool'] = _safe_call(builtin.bool, True)
    results['false_to_bool'] = _safe_call(builtin.bool, False)
    return results

def test_round_trip_conversions():
    results = {}
    val1 = 42
    val1_str = _safe_call(builtin.str, val1)
    val1_back = _safe_call(builtin.int, val1_str)
    results['int_roundtrip'] = val1_back
    val2 = 3.14
    val2_str = _safe_call(builtin.str, val2)
    val2_back = _safe_call(builtin.float, val2_str)
    results['float_roundtrip'] = val2_back
    val3 = True
    val3_int = _safe_call(builtin.int, val3)
    val3_back = _safe_call(builtin.bool, val3_int)
    results['bool_roundtrip'] = val3_back
    return results

def main():
    all_results = {}
    all_results['int_tests'] = test_int_conversion()
    all_results['float_tests'] = test_float_conversion()
    all_results['str_tests'] = test_str_conversion()
    all_results['bool_tests'] = test_bool_conversion()
    all_results['roundtrip'] = test_round_trip_conversions()
    return all_results

test_results = main()

# End of generated code