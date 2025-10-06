"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_empty_collections():
    results = {}
    results['len_empty'] = _safe_call(builtin.len, [])
    results['sum_empty'] = _safe_call(builtin.sum, [])
    results['all_empty'] = _safe_call(builtin.all, [])
    results['any_empty'] = _safe_call(builtin.any, [])
    results['sorted_empty'] = _safe_call(builtin.sorted, [])
    results['reversed_empty'] = _safe_call(builtin.reversed, [])
    results['len_empty_str'] = _safe_call(builtin.len, '')
    results['keys_empty'] = _safe_call(builtin.keys, {})
    results['values_empty'] = _safe_call(builtin.values, {})
    return results

def test_single_element_collections():
    results = {}
    results['len_single'] = _safe_call(builtin.len, [42])
    results['sum_single'] = _safe_call(builtin.sum, [42])
    results['all_single'] = _safe_call(builtin.all, [True])
    results['any_single'] = _safe_call(builtin.any, [True])
    results['sorted_single'] = _safe_call(builtin.sorted, [42])
    results['reversed_single'] = _safe_call(builtin.reversed, [42])
    results['min_single'] = _safe_call(builtin.min, [42])
    results['max_single'] = _safe_call(builtin.max, [42])
    return results

def test_type_conversion_edge_cases():
    results = {}
    results['int_zero'] = _safe_call(builtin.int, 0)
    results['float_zero'] = _safe_call(builtin.float, 0)
    results['bool_zero'] = _safe_call(builtin.bool, 0)
    results['int_true'] = _safe_call(builtin.int, True)
    results['int_false'] = _safe_call(builtin.int, False)
    results['float_true'] = _safe_call(builtin.float, True)
    results['float_false'] = _safe_call(builtin.float, False)
    results['str_true'] = _safe_call(builtin.str, True)
    results['str_false'] = _safe_call(builtin.str, False)
    results['str_zero'] = _safe_call(builtin.str, 0)
    return results

def test_math_operations_edge_cases():
    results = {}
    results['abs_zero'] = _safe_call(builtin.abs, 0)
    results['abs_zero_float'] = _safe_call(builtin.abs, 0.0)
    results['min_dups'] = _safe_call(builtin.min, [3, 1, 1, 2, 3])
    results['max_dups'] = _safe_call(builtin.max, [3, 1, 1, 2, 3])
    results['round_int'] = _safe_call(builtin.round, 42)
    results['round_zero'] = _safe_call(builtin.round, 0)
    return results

def test_range_edge_cases():
    results = {}
    results['range_zero'] = _safe_call(builtin.range, 0)
    results['range_one'] = _safe_call(builtin.range, 1)
    results['range_equal'] = _safe_call(builtin.range, 5, 5)
    return results

def test_boundary_values():
    results = {}
    large = 1000000
    results['large_int'] = _safe_call(builtin.int, large)
    results['large_str'] = _safe_call(builtin.len, _safe_call(builtin.str, large))
    small = 0.0001
    results['small_float'] = _safe_call(builtin.float, small)
    return results

def test_typeof_edge_cases():
    results = {}
    results['typeof_zero'] = _safe_call(builtin.typeof, 0)
    results['typeof_empty_str'] = _safe_call(builtin.typeof, '')
    results['typeof_empty_arr'] = _safe_call(builtin.typeof, [])
    results['typeof_empty_obj'] = _safe_call(builtin.typeof, {})
    results['typeof_false'] = _safe_call(builtin.typeof, False)
    return results

def test_comparison_edge_cases():
    results = {}
    results['zero_eq_false'] = (0 == False)
    results['zero_bool'] = _safe_call(builtin.bool, 0)
    results['empty_bool'] = _safe_call(builtin.bool, '')
    return results

def test_array_operations_edge_cases():
    results = {}
    short = [1, 2]
    long = [10, 20, 30, 40]
    results['zip_mismatch'] = _safe_call(builtin.zip, short, long)
    dups = [3, 1, 2, 3, 1, 2]
    results['sorted_dups'] = _safe_call(builtin.sorted, dups)
    results['enum_empty'] = _safe_call(builtin.enumerate, [])
    return results

def test_string_edge_cases():
    results = {}
    results['chr_0'] = _safe_call(builtin.len, _safe_call(builtin.chr, 0))
    results['ord_space'] = _safe_call(builtin.ord, ' ')
    results['reversed_empty_str'] = _safe_call(builtin.reversed, '')
    return results

def test_mixed_type_operations():
    results = {}
    results['all_mixed'] = _safe_call(builtin.all, [1, 'hello', True])
    results['any_mixed'] = _safe_call(builtin.any, [0, '', 1])
    results['sum_mixed'] = _safe_call(builtin.sum, [1, 2.5, 3])
    return results

def test_predicate_edge_cases():
    results = {}
    results['all_one_false'] = _safe_call(builtin.all, [True, True, False])
    results['any_one_true'] = _safe_call(builtin.any, [False, False, True])
    results['callable_int'] = _safe_call(builtin.callable, 42)
    results['callable_str'] = _safe_call(builtin.callable, 'hello')
    return results

def test_format_edge_cases():
    results = {}
    results['format_zero'] = _safe_call(builtin.format, 0, '05d')
    results['format_prec_0'] = _safe_call(builtin.format, 3.14, '.0f')
    results['format_empty'] = _safe_call(builtin.format, 42, '')
    return results

def test_combined_edge_cases():
    results = {}
    empty_arr = []
    if (_safe_call(builtin.len, empty_arr) == 0):
        results['empty_handled'] = True
    single = [42]
    results['single_sum'] = _safe_call(builtin.sum, single)
    results['single_min'] = _safe_call(builtin.min, single)
    results['single_max'] = _safe_call(builtin.min, single)
    zeros = [0, 0, 0]
    results['sum_zeros'] = _safe_call(builtin.sum, zeros)
    results['any_zeros'] = _safe_call(builtin.any, zeros)
    results['all_zeros'] = _safe_call(builtin.all, zeros)
    return results

def main():
    all_results = {}
    all_results['empty'] = test_empty_collections()
    all_results['single'] = test_single_element_collections()
    all_results['type_conv'] = test_type_conversion_edge_cases()
    all_results['math'] = test_math_operations_edge_cases()
    all_results['range'] = test_range_edge_cases()
    all_results['boundaries'] = test_boundary_values()
    all_results['typeof'] = test_typeof_edge_cases()
    all_results['comparisons'] = test_comparison_edge_cases()
    all_results['arrays'] = test_array_operations_edge_cases()
    all_results['strings'] = test_string_edge_cases()
    all_results['mixed_types'] = test_mixed_type_operations()
    all_results['predicates'] = test_predicate_edge_cases()
    all_results['format'] = test_format_edge_cases()
    all_results['combined'] = test_combined_edge_cases()
    return all_results

test_results = main()

# End of generated code