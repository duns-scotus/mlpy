"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

def test_array_destructuring():
    arr = [10, 20, 30]
    a, b, c = arr
    results = {}
    results['a'] = a
    results['b'] = b
    results['c'] = c
    return results

def test_array_exact():
    arr = [100, 200]
    x, y = arr
    results = {}
    results['x'] = x
    results['y'] = y
    return results

def test_object_destructuring():
    obj = {'x': 10, 'y': 20, 'z': 30}
    x = obj['x']
    y = obj['y']
    z = obj['z']
    results = {}
    results['x'] = x
    results['y'] = y
    results['z'] = z
    return results

def test_object_exact():
    obj = {'name': 'Alice', 'age': 25}
    name = obj['name']
    age = obj['age']
    results = {}
    results['name'] = name
    results['age'] = age
    return results

def swap(a, b):
    temp = [b, a]
    a, b = temp
    results = {}
    results['a'] = a
    results['b'] = b
    return results

def test_swap():
    return swap(10, 20)

def test_destructuring_expression():
    a, b = [(5 * 2), (10 + 5)]
    results = {}
    results['a'] = a
    results['b'] = b
    return results

def test_nested_destructuring():
    point = {'x': 100, 'y': 200}
    x = point['x']
    y = point['y']
    sum = (x + y)
    product = (x * y)
    results = {}
    results['sum'] = sum
    results['product'] = product
    return results

def test_destructuring_loop():
    pairs = [[1, 2], [3, 4], [5, 6]]
    sums = []
    i = 0
    while (i < 3):
        a, b = pairs[i]
        sums = (sums + [(a + b)])
        i = (i + 1)
    return sums

def test_multiple_destructuring():
    arr1 = [1, 2, 3]
    arr2 = [4, 5, 6]
    a, b, c = arr1
    d, e, f = arr2
    results = {}
    results['from_arr1'] = ((a + b) + c)
    results['from_arr2'] = ((d + e) + f)
    return results

def test_destructuring_build():
    source = [10, 20]
    first, second = source
    result = [(first * 2), (second * 2)]
    return result

def test_object_names():
    data = {'firstName': 'John', 'lastName': 'Doe', 'age': 30}
    firstName = data['firstName']
    lastName = data['lastName']
    age = data['age']
    results = {}
    results['firstName'] = firstName
    results['lastName'] = lastName
    results['age'] = age
    return results

def get_point():
    return {'x': 50, 'y': 100}

def test_destructuring_return():
    x = get_point()['x']
    y = get_point()['y']
    results = {}
    results['x'] = x
    results['y'] = y
    return results

def test_destructuring_calc():
    a, b, c = [5, 10, 15]
    min_val = a if (a < b) else b
    min_val = min_val if (min_val < c) else c
    max_val = a if (a > b) else b
    max_val = max_val if (max_val > c) else c
    results = {}
    results['min'] = min_val
    results['max'] = max_val
    results['sum'] = ((a + b) + c)
    return results

def main():
    results = {}
    results['array_basic'] = test_array_destructuring()
    results['array_exact'] = test_array_exact()
    results['object_basic'] = test_object_destructuring()
    results['object_exact'] = test_object_exact()
    results['swap'] = test_swap()
    results['expression'] = test_destructuring_expression()
    results['nested'] = test_nested_destructuring()
    results['loop'] = test_destructuring_loop()
    results['multiple'] = test_multiple_destructuring()
    results['build'] = test_destructuring_build()
    results['object_names'] = test_object_names()
    results['return_val'] = test_destructuring_return()
    results['calc'] = test_destructuring_calc()
    return results

test_results = main()

# End of generated code