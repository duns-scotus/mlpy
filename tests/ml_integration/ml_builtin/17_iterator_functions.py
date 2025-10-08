"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

def test_basic_iteration():
    results = {}
    arr = [1, 2, 3]
    it = _safe_call(builtin.iter, arr)
    results['first'] = _safe_call(builtin.next, it)
    results['second'] = _safe_call(builtin.next, it)
    results['third'] = _safe_call(builtin.next, it)
    return results

def test_next_with_default():
    results = {}
    arr = [10, 20]
    it = _safe_call(builtin.iter, arr)
    results['val1'] = _safe_call(builtin.next, it)
    results['val2'] = _safe_call(builtin.next, it)
    results['val3'] = _safe_call(builtin.next, it, 'done')
    results['val4'] = _safe_call(builtin.next, it, None)
    results['val5'] = _safe_call(builtin.next, it, -1)
    return results

def test_string_iteration():
    results = {}
    text = 'abc'
    it = _safe_call(builtin.iter, text)
    results['char1'] = _safe_call(builtin.next, it)
    results['char2'] = _safe_call(builtin.next, it)
    results['char3'] = _safe_call(builtin.next, it)
    results['char4'] = _safe_call(builtin.next, it, 'END')
    return results

def test_empty_iteration():
    results = {}
    empty = []
    it = _safe_call(builtin.iter, empty)
    results['first_attempt'] = _safe_call(builtin.next, it, 'empty')
    results['second_attempt'] = _safe_call(builtin.next, it, 'still_empty')
    return results

def test_manual_sum():
    results = {}
    numbers = [1, 2, 3, 4, 5]
    it = _safe_call(builtin.iter, numbers)
    total = 0
    val = _safe_call(builtin.next, it, None)
    while (val != None):
        total = (total + val)
        val = _safe_call(builtin.next, it, None)
    results['sum'] = total
    results['expected'] = _safe_call(builtin.sum, numbers)
    return results

def test_partial_consumption():
    results = {}
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    it = _safe_call(builtin.iter, data)
    first_three = []
    first_three = (first_three + [_safe_call(builtin.next, it)])
    first_three = (first_three + [_safe_call(builtin.next, it)])
    first_three = (first_three + [_safe_call(builtin.next, it)])
    results['first_three'] = first_three
    results['count'] = _safe_call(builtin.len, first_three)
    results['fourth'] = _safe_call(builtin.next, it)
    results['fifth'] = _safe_call(builtin.next, it)
    return results

def test_multiple_iterators():
    results = {}
    arr = [1, 2, 3]
    it1 = _safe_call(builtin.iter, arr)
    it2 = _safe_call(builtin.iter, arr)
    results['it1_first'] = _safe_call(builtin.next, it1)
    results['it2_first'] = _safe_call(builtin.next, it2)
    results['it1_second'] = _safe_call(builtin.next, it1)
    results['it2_second'] = _safe_call(builtin.next, it2)
    results['it1_third'] = _safe_call(builtin.next, it1)
    results['it1_done'] = _safe_call(builtin.next, it1, 'DONE')
    results['it2_third'] = _safe_call(builtin.next, it2)
    results['it2_done'] = _safe_call(builtin.next, it2, 'DONE')
    return results

def test_collect_from_iterator():
    results = {}
    source = [100, 200, 300, 400]
    it = _safe_call(builtin.iter, source)
    collected = []
    val = _safe_call(builtin.next, it, None)
    while (val != None):
        collected = (collected + [val])
        val = _safe_call(builtin.next, it, None)
    results['collected'] = collected
    results['length'] = _safe_call(builtin.len, collected)
    results['matches_source'] = (_safe_call(builtin.len, collected) == _safe_call(builtin.len, source))
    return results

def test_filter_with_iterator():
    results = {}
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    it = _safe_call(builtin.iter, numbers)
    evens = []
    val = _safe_call(builtin.next, it, None)
    while (val != None):
        if ((val % 2) == 0):
            evens = (evens + [val])
        val = _safe_call(builtin.next, it, None)
    results['evens'] = evens
    results['count'] = _safe_call(builtin.len, evens)
    return results

def test_transform_with_iterator():
    results = {}
    numbers = [1, 2, 3, 4, 5]
    it = _safe_call(builtin.iter, numbers)
    squared = []
    val = _safe_call(builtin.next, it, None)
    while (val != None):
        squared = (squared + [(val * val)])
        val = _safe_call(builtin.next, it, None)
    results['squared'] = squared
    results['first'] = squared[0]
    results['last'] = squared[(_safe_call(builtin.len, squared) - 1)]
    return results

def test_zip_with_iterators():
    results = {}
    arr1 = [1, 2, 3]
    arr2 = ['a', 'b', 'c']
    it1 = _safe_call(builtin.iter, arr1)
    it2 = _safe_call(builtin.iter, arr2)
    pairs = []
    val1 = _safe_call(builtin.next, it1, None)
    val2 = _safe_call(builtin.next, it2, None)
    while ((val1 != None) and (val2 != None)):
        pairs = (pairs + [[val1, val2]])
        val1 = _safe_call(builtin.next, it1, None)
        val2 = _safe_call(builtin.next, it2, None)
    results['pairs'] = pairs
    results['count'] = _safe_call(builtin.len, pairs)
    results['first_pair'] = pairs[0]
    return results

def test_take_while():
    results = {}
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    it = _safe_call(builtin.iter, numbers)
    less_than_5 = []
    val = _safe_call(builtin.next, it, None)
    while ((val != None) and (val < 5)):
        less_than_5 = (less_than_5 + [val])
        val = _safe_call(builtin.next, it, None)
    results['taken'] = less_than_5
    results['count'] = _safe_call(builtin.len, less_than_5)
    results['stopped_at'] = val
    return results

def test_find_first():
    results = {}
    numbers = [1, 3, 5, 8, 10, 11]
    it = _safe_call(builtin.iter, numbers)
    found = None
    val = _safe_call(builtin.next, it, None)
    while (val != None):
        if ((val % 2) == 0):
            found = val
            val = None
        elif (val != None):
            val = _safe_call(builtin.next, it, None)
    results['first_even'] = found
    return results

def test_enumerate_manual():
    results = {}
    items = ['a', 'b', 'c']
    it = _safe_call(builtin.iter, items)
    indexed = []
    index = 0
    val = _safe_call(builtin.next, it, None)
    while (val != None):
        indexed = (indexed + [[index, val]])
        index = (index + 1)
        val = _safe_call(builtin.next, it, None)
    results['indexed'] = indexed
    results['count'] = _safe_call(builtin.len, indexed)
    return results

def test_range_iteration():
    results = {}
    r = _safe_call(builtin.range, 5)
    it = _safe_call(builtin.iter, r)
    sum_val = 0
    count = 0
    val = _safe_call(builtin.next, it, None)
    while (val != None):
        sum_val = (sum_val + val)
        count = (count + 1)
        val = _safe_call(builtin.next, it, None)
    results['sum'] = sum_val
    results['count'] = count
    return results

def test_nested_iteration():
    results = {}
    nested = [[1, 2], [3, 4], [5, 6]]
    outer_it = _safe_call(builtin.iter, nested)
    flattened = []
    outer_val = _safe_call(builtin.next, outer_it, None)
    while (outer_val != None):
        inner_it = _safe_call(builtin.iter, outer_val)
        inner_val = _safe_call(builtin.next, inner_it, None)
        while (inner_val != None):
            flattened = (flattened + [inner_val])
            inner_val = _safe_call(builtin.next, inner_it, None)
        outer_val = _safe_call(builtin.next, outer_it, None)
    results['flattened'] = flattened
    results['count'] = _safe_call(builtin.len, flattened)
    return results

def test_iterator_state_persistence():
    results = {}
    numbers = [10, 20, 30, 40, 50]
    it = _safe_call(builtin.iter, numbers)
    batch1 = []
    batch1 = (batch1 + [_safe_call(builtin.next, it)])
    batch1 = (batch1 + [_safe_call(builtin.next, it)])
    results['batch1'] = batch1
    batch2 = []
    batch2 = (batch2 + [_safe_call(builtin.next, it)])
    batch2 = (batch2 + [_safe_call(builtin.next, it)])
    results['batch2'] = batch2
    results['remaining'] = _safe_call(builtin.next, it)
    results['exhausted'] = _safe_call(builtin.next, it, 'NONE')
    return results

def test_chunking_with_iterator():
    results = {}
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    it = _safe_call(builtin.iter, data)
    chunks = []
    val = _safe_call(builtin.next, it, None)
    while (val != None):
        chunk = [val]
        next_val = _safe_call(builtin.next, it, None)
        if (next_val != None):
            chunk = (chunk + [next_val])
        chunks = (chunks + [chunk])
        val = _safe_call(builtin.next, it, None)
    results['chunks'] = chunks
    results['chunk_count'] = _safe_call(builtin.len, chunks)
    results['first_chunk'] = chunks[0]
    return results

def main():
    all_results = {}
    all_results['basic'] = test_basic_iteration()
    all_results['with_default'] = test_next_with_default()
    all_results['string_iter'] = test_string_iteration()
    all_results['empty'] = test_empty_iteration()
    all_results['manual_sum'] = test_manual_sum()
    all_results['partial'] = test_partial_consumption()
    all_results['multiple'] = test_multiple_iterators()
    all_results['collect'] = test_collect_from_iterator()
    all_results['filter'] = test_filter_with_iterator()
    all_results['transform'] = test_transform_with_iterator()
    all_results['zip_manual'] = test_zip_with_iterators()
    all_results['take_while'] = test_take_while()
    all_results['find_first'] = test_find_first()
    all_results['enumerate'] = test_enumerate_manual()
    all_results['range_iter'] = test_range_iteration()
    all_results['nested'] = test_nested_iteration()
    all_results['state'] = test_iterator_state_persistence()
    all_results['chunking'] = test_chunking_with_iterator()
    return all_results

test_results = main()

# End of generated code