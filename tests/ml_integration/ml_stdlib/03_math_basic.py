"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.math_bridge import math

def test_basic_functions():
    results = {}
    results['abs_positive'] = _safe_call(math.abs, 42)
    results['abs_negative'] = _safe_call(math.abs, -42)
    results['abs_zero'] = _safe_call(math.abs, 0)
    results['abs_float'] = _safe_call(math.abs, -3.14)
    results['ceil_positive'] = _safe_call(math.ceil, 3.2)
    results['ceil_negative'] = _safe_call(math.ceil, -3.2)
    results['ceil_whole'] = _safe_call(math.ceil, 5.0)
    results['floor_positive'] = _safe_call(math.floor, 3.8)
    results['floor_negative'] = _safe_call(math.floor, -3.8)
    results['floor_whole'] = _safe_call(math.floor, 5.0)
    results['round_up'] = _safe_call(math.round, 3.6)
    results['round_down'] = _safe_call(math.round, 3.4)
    results['round_half'] = _safe_call(math.round, 3.5)
    results['round_negative'] = _safe_call(math.round, -3.5)
    return results

def test_sqrt_function():
    results = {}
    results['sqrt_4'] = _safe_call(math.sqrt, 4.0)
    results['sqrt_9'] = _safe_call(math.sqrt, 9.0)
    results['sqrt_16'] = _safe_call(math.sqrt, 16.0)
    results['sqrt_2'] = _safe_call(math.sqrt, 2.0)
    return results

def test_pow_function():
    results = {}
    results['pow_2_3'] = _safe_call(math.pow, 2.0, 3.0)
    results['pow_3_2'] = _safe_call(math.pow, 3.0, 2.0)
    results['pow_5_0'] = _safe_call(math.pow, 5.0, 0.0)
    results['pow_2_neg'] = _safe_call(math.pow, 2.0, -1.0)
    results['pow_10_2'] = _safe_call(math.pow, 10.0, 2.0)
    return results

def test_constants():
    results = {}
    pi = math.pi
    e = math.e
    results['has_pi'] = ((pi > 3.14) and (pi < 3.15))
    results['has_e'] = ((e > 2.71) and (e < 2.72))
    results['pi_times_2'] = _safe_call(math.round, (pi * 2.0))
    results['e_squared'] = _safe_call(math.round, _safe_call(math.pow, e, 2.0))
    return results

def test_min_max():
    results = {}
    results['min_2_5'] = _safe_call(math.min, 2.0, 5.0)
    results['min_neg'] = _safe_call(math.min, -5.0, -2.0)
    results['max_2_5'] = _safe_call(math.max, 2.0, 5.0)
    results['max_neg'] = _safe_call(math.max, -5.0, -2.0)
    return results

def test_sign_function():
    results = {}
    results['sign_positive'] = _safe_call(math.sign, 42.0)
    results['sign_negative'] = _safe_call(math.sign, -42.0)
    results['sign_zero'] = _safe_call(math.sign, 0.0)
    return results

def test_practical_calculations():
    results = {}
    radius = 5.0
    area = (math.pi * _safe_call(math.pow, radius, 2.0))
    results['circle_area'] = _safe_call(math.round, area)
    a = 3.0
    b = 4.0
    c = _safe_call(math.sqrt, (_safe_call(math.pow, a, 2.0) + _safe_call(math.pow, b, 2.0)))
    results['hypotenuse'] = c
    x1 = 0.0
    y1 = 0.0
    x2 = 3.0
    y2 = 4.0
    dist = _safe_call(math.sqrt, (_safe_call(math.pow, (x2 - x1), 2.0) + _safe_call(math.pow, (y2 - y1), 2.0)))
    results['distance'] = dist
    return results

def main():
    all_results = {}
    all_results['basic'] = test_basic_functions()
    all_results['sqrt'] = test_sqrt_function()
    all_results['pow'] = test_pow_function()
    all_results['constants'] = test_constants()
    all_results['minmax'] = test_min_max()
    all_results['sign'] = test_sign_function()
    all_results['practical'] = test_practical_calculations()
    return all_results

test_results = main()

# End of generated code