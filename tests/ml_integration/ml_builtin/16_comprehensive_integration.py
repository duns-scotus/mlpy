"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_data_processing_pipeline():
    results = {}
    raw_scores = [85, 92, 78, 95, 88, 73, 91, 82, 87, 94]
    total = _safe_call(builtin.sum, raw_scores)
    count = _safe_call(builtin.len, raw_scores)
    average = (total / count)
    results['total'] = total
    results['count'] = count
    results['average'] = _safe_call(builtin.round, average, 1)
    results['min_score'] = _safe_call(builtin.min, raw_scores)
    results['max_score'] = _safe_call(builtin.max, raw_scores)
    results['range'] = (_safe_call(builtin.max, raw_scores) - _safe_call(builtin.min, raw_scores))
    sorted_scores = _safe_call(builtin.sorted, raw_scores)
    results['sorted_first'] = sorted_scores[0]
    results['sorted_last'] = sorted_scores[(count - 1)]
    top_3 = _safe_call(builtin.reversed, _safe_call(builtin.sorted, raw_scores))
    results['rank_1'] = top_3[0]
    results['rank_2'] = top_3[1]
    results['rank_3'] = top_3[2]
    return results

def test_text_processing_pipeline():
    results = {}
    message = 'HELLO'
    results['msg_len'] = _safe_call(builtin.len, message)
    results['msg_type'] = _safe_call(builtin.typeof, message)
    char_codes = []
    for i in _safe_call(builtin.range, _safe_call(builtin.len, message)):
        char_codes = (char_codes + [_safe_call(builtin.ord, 'H')])
    results['code_count'] = _safe_call(builtin.len, char_codes)
    first_code = _safe_call(builtin.ord, 'H')
    results['first_char'] = _safe_call(builtin.chr, first_code)
    return results

def test_numerical_transformations():
    results = {}
    sequence = _safe_call(builtin.range, 1, 11)
    squares = []
    for n in sequence:
        squares = (squares + [(n * n)])
    results['sum_squares'] = _safe_call(builtin.sum, squares)
    results['min_square'] = _safe_call(builtin.min, squares)
    results['max_square'] = _safe_call(builtin.max, squares)
    sample = 42
    results['dec'] = sample
    results['hex'] = _safe_call(builtin.hex, sample)
    results['bin'] = _safe_call(builtin.bin, sample)
    results['oct'] = _safe_call(builtin.oct, sample)
    return results

def test_collection_operations():
    results = {}
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    letters = ['d', 'a', 'c', 'b']
    results['num_len'] = _safe_call(builtin.len, numbers)
    results['letter_len'] = _safe_call(builtin.len, letters)
    sorted_nums = _safe_call(builtin.sorted, numbers)
    sorted_letters = _safe_call(builtin.sorted, letters)
    results['nums_sorted'] = sorted_nums
    results['letters_sorted'] = sorted_letters
    results['nums_reversed'] = _safe_call(builtin.reversed, [1, 2, 3])
    enum_letters = _safe_call(builtin.enumerate, letters)
    results['enum_len'] = _safe_call(builtin.len, enum_letters)
    return results

def test_object_manipulation():
    results = {}
    person = {'name': 'Alice', 'age': 30, 'city': 'NYC', 'active': True}
    all_keys = _safe_call(builtin.keys, person)
    all_values = _safe_call(builtin.values, person)
    results['key_count'] = _safe_call(builtin.len, all_keys)
    results['value_count'] = _safe_call(builtin.len, all_values)
    results['obj_type'] = _safe_call(builtin.typeof, person)
    results['isinstance_obj'] = _safe_call(builtin.isinstance, person, 'object')
    return results

def test_mathematical_computations():
    results = {}
    values = [-5, 3, -2, 7, -1, 4, -3, 8]
    abs_values = []
    for v in values:
        abs_values = (abs_values + [_safe_call(builtin.abs, v)])
    results['sum_abs'] = _safe_call(builtin.sum, abs_values)
    results['min_abs'] = _safe_call(builtin.min, abs_values)
    results['max_abs'] = _safe_call(builtin.max, abs_values)
    pi = 3.14159
    results['pi_0'] = _safe_call(builtin.round, pi, 0)
    results['pi_2'] = _safe_call(builtin.round, pi, 2)
    results['pi_4'] = _safe_call(builtin.round, pi, 4)
    return results

def test_predicate_filtering():
    results = {}
    data = [1, 0, 5, 0, 3, 0, 7]
    checks = []
    for d in data:
        checks = (checks + [(d != 0)])
    results['all_nonzero'] = _safe_call(builtin.all, checks)
    results['any_nonzero'] = _safe_call(builtin.any, checks)
    nonzero_count = 0
    for d in data:
        if (d != 0):
            nonzero_count = (nonzero_count + 1)
    results['nonzero_count'] = nonzero_count
    return results

def test_string_formatting_pipeline():
    results = {}
    price = 99.99
    quantity = 5
    discount = 0.15
    results['price_fmt'] = _safe_call(builtin.format, price, '.2f')
    results['qty_fmt'] = _safe_call(builtin.format, quantity, '03d')
    subtotal = (price * quantity)
    discount_amount = (subtotal * discount)
    total = (subtotal - discount_amount)
    results['subtotal'] = _safe_call(builtin.round, subtotal, 2)
    results['discount'] = _safe_call(builtin.round, discount_amount, 2)
    results['total'] = _safe_call(builtin.round, total, 2)
    return results

def test_functional_composition():
    results = {}
    input = [1, 2, 3, 4, 5]
    squared = []
    for n in input:
        squared = (squared + [(n * n)])
    even_squared = []
    for s in squared:
        if ((s - ((s / 2) * 2)) == 0):
            even_squared = (even_squared + [s])
    total = _safe_call(builtin.sum, even_squared)
    results['squared'] = squared
    results['even_squared'] = even_squared
    results['total'] = total
    return results

def test_type_conversions_pipeline():
    results = {}
    start = '42'
    as_int = _safe_call(builtin.int, start)
    results['as_int'] = as_int
    as_float = _safe_call(builtin.float, as_int)
    results['as_float'] = as_float
    as_str = _safe_call(builtin.str, as_float)
    results['as_str'] = as_str
    as_bool = _safe_call(builtin.bool, as_str)
    results['as_bool'] = as_bool
    as_int2 = _safe_call(builtin.int, as_bool)
    results['as_int2'] = as_int2
    return results

def test_real_world_scenario():
    results = {}
    items = [{'name': 'Book', 'price': 19.99, 'qty': 2}, {'name': 'Pen', 'price': 2.5, 'qty': 5}, {'name': 'Notebook', 'price': 5.99, 'qty': 3}]
    prices = [19.99, 2.5, 5.99]
    quantities = [2, 5, 3]
    line_totals = []
    pairs = _safe_call(builtin.zip, prices, quantities)
    for pair in pairs:
        price = pair[0]
        qty = pair[1]
        line_totals = (line_totals + [(price * qty)])
    subtotal = _safe_call(builtin.sum, line_totals)
    tax_rate = 0.08
    tax = (subtotal * tax_rate)
    grand_total = (subtotal + tax)
    results['subtotal'] = _safe_call(builtin.round, subtotal, 2)
    results['tax'] = _safe_call(builtin.round, tax, 2)
    results['total'] = _safe_call(builtin.round, grand_total, 2)
    results['item_count'] = _safe_call(builtin.len, items)
    return results

def main():
    all_results = {}
    _safe_call(builtin.print, '=== Comprehensive Integration Tests ===')
    all_results['data_proc'] = test_data_processing_pipeline()
    all_results['text_proc'] = test_text_processing_pipeline()
    all_results['num_transform'] = test_numerical_transformations()
    all_results['collections'] = test_collection_operations()
    all_results['objects'] = test_object_manipulation()
    all_results['math'] = test_mathematical_computations()
    all_results['predicates'] = test_predicate_filtering()
    all_results['formatting'] = test_string_formatting_pipeline()
    all_results['functional'] = test_functional_composition()
    all_results['type_conv'] = test_type_conversions_pipeline()
    all_results['real_world'] = test_real_world_scenario()
    _safe_call(builtin.print, '=== All Integration Tests Complete ===')
    return all_results

test_results = main()

# End of generated code