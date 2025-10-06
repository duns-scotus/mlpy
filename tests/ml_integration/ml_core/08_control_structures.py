"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.ml.errors.exceptions import MLUserException
from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

def get_length(arr):
    len = 0
    try:
        i = 0
        while True:
            temp = arr[i]
            i = (i + 1)
            len = (len + 1)
    except Exception as e:
        pass
    finally:
        pass
    return len

def test_conditionals(value):
    if (value < 0):
        return 'negative'
    elif (value == 0):
        return 'zero'
    elif (value < 10):
        return 'small'
    elif (value < 100):
        return 'medium'
    else:
        return 'large'

def test_nested_if(a, b):
    if (a > 0):
        if (b > 0):
            return 'both positive'
        else:
            return 'a positive, b non-positive'
    else:
        if (b > 0):
            return 'a non-positive, b positive'
        else:
            return 'both non-positive'

def test_while_loop(n):
    sum = 0
    i = 1
    while (i <= n):
        sum = (sum + i)
        i = (i + 1)
    return sum

def test_while_break(limit):
    sum = 0
    i = 0
    found = False
    while ((i < 1000) and (not found)):
        sum = (sum + i)
        if (sum >= limit):
            found = True
        i = (i + 1)
    return {'sum': sum, 'iterations': i}

def test_while_continue(n):
    sum = 0
    i = 0
    while (i < n):
        i = (i + 1)
        remainder = (i - ((i / 2) * 2))
        if (remainder == 1):
            pass
        else:
            sum = (sum + i)
    return sum

def test_for_loop(arr):
    sum = 0
    for val in arr:
        sum = (sum + val)
    return sum

def test_nested_loops(rows, cols):
    count = 0
    i = 0
    while (i < rows):
        j = 0
        while (j < cols):
            count = (count + 1)
            j = (j + 1)
        i = (i + 1)
    return count

def test_try_except(value):
    result = {'success': False, 'value': 0, 'error': None}
    try:
        if (value == 0):
            raise MLUserException({'message': 'Zero not allowed', 'code': 100})
        result['value'] = (100 / value)
        result['success'] = True
    except Exception as e:
        result['error'] = e
        result['value'] = -1
    finally:
        pass
    return result

def test_try_finally():
    result = {'steps': [], 'final_value': 0}
    try:
        result['steps'] = (_safe_attr_access(result, 'steps') + ['try block'])
        x = 10
        result['final_value'] = (x * 2)
    except Exception as e:
        result['steps'] = (_safe_attr_access(result, 'steps') + ['except block'])
        result['final_value'] = -1
    finally:
        result['steps'] = (_safe_attr_access(result, 'steps') + ['finally block'])
        result['final_value'] = (_safe_attr_access(result, 'final_value') + 1)
    return result

def test_nested_try():
    result = {'outer': None, 'inner': None}
    try:
        result['outer'] = 'outer try'
        try:
            result['inner'] = 'inner try'
            x = (1 / 0)
            result['inner'] = 'inner success'
        except Exception as inner_error:
            result['inner'] = 'inner caught'
        finally:
            pass
        result['outer'] = 'outer success'
    except Exception as outer_error:
        result['outer'] = 'outer caught'
    finally:
        pass
    return result

def test_complex_flow(arr):
    len = get_length(arr)
    positive_count = 0
    negative_count = 0
    zero_count = 0
    sum = 0
    i = 0
    while (i < len):
        value = arr[i]
        if (value > 0):
            positive_count = (positive_count + 1)
            sum = (sum + value)
        elif (value < 0):
            negative_count = (negative_count + 1)
        else:
            zero_count = (zero_count + 1)
        i = (i + 1)
    return {'positive': positive_count, 'negative': negative_count, 'zeros': zero_count, 'sum': sum}

def test_early_return(arr, target):
    len = get_length(arr)
    i = 0
    while (i < len):
        if (arr[i] == target):
            return {'found': True, 'index': i}
        i = (i + 1)
    return {'found': False, 'index': -1}

def test_ternary(a, b):
    max = a if (a > b) else b
    min = a if (a < b) else b
    return {'max': max, 'min': min}

def test_switch(day):
    if (day == 1):
        return 'Monday'
    elif (day == 2):
        return 'Tuesday'
    elif (day == 3):
        return 'Wednesday'
    elif (day == 4):
        return 'Thursday'
    elif (day == 5):
        return 'Friday'
    elif (day == 6):
        return 'Saturday'
    elif (day == 7):
        return 'Sunday'
    else:
        return 'Invalid'

def main():
    results = {}
    results['cond_neg'] = test_conditionals(-5)
    results['cond_zero'] = test_conditionals(0)
    results['cond_small'] = test_conditionals(7)
    results['cond_medium'] = test_conditionals(50)
    results['cond_large'] = test_conditionals(200)
    results['nested_pp'] = test_nested_if(5, 3)
    results['nested_pn'] = test_nested_if(5, -3)
    results['nested_np'] = test_nested_if(-5, 3)
    results['nested_nn'] = test_nested_if(-5, -3)
    results['while_10'] = test_while_loop(10)
    results['while_100'] = test_while_loop(100)
    results['break_50'] = test_while_break(50)
    results['break_200'] = test_while_break(200)
    results['continue_10'] = test_while_continue(10)
    results['continue_20'] = test_while_continue(20)
    for_arr1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for_arr2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    results['for_10'] = test_for_loop(for_arr1)
    results['for_20'] = test_for_loop(for_arr2)
    results['nested_3x3'] = test_nested_loops(3, 3)
    results['nested_5x4'] = test_nested_loops(5, 4)
    results['try_normal'] = test_try_except(5)
    results['try_zero'] = test_try_except(0)
    results['try_finally'] = test_try_finally()
    results['nested_try'] = test_nested_try()
    test_arr = [5, -3, 0, 8, -1, 0, 12]
    results['complex'] = test_complex_flow(test_arr)
    search_arr = [10, 20, 30, 40, 50]
    results['found'] = test_early_return(search_arr, 30)
    results['not_found'] = test_early_return(search_arr, 99)
    results['ternary_5_3'] = test_ternary(5, 3)
    results['ternary_2_8'] = test_ternary(2, 8)
    results['day_1'] = test_switch(1)
    results['day_5'] = test_switch(5)
    results['day_7'] = test_switch(7)
    results['day_invalid'] = test_switch(99)
    return results

test_results = main()

# End of generated code