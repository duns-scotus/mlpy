"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

def create_counter(initial):
    count = initial
    def increment():
        nonlocal count
        count = (count + 1)
        return count
    return increment

def create_account(initial_balance):
    balance = initial_balance
    def deposit(amount):
        nonlocal balance
        balance = (balance + amount)
        return balance
    def withdraw(amount):
        nonlocal balance
        if (balance >= amount):
            balance = (balance - amount)
            return balance
        else:
            return balance
    def get_balance():
        return balance
    return {'deposit': deposit, 'withdraw': withdraw, 'balance': get_balance}

def create_multiplier(factor):
    def multiply(value):
        return (value * factor)
    return multiply

def create_adder(amount):
    def add(value):
        return (value + amount)
    return add

def curry_add(a):
    def add_to_a(b):
        return (a + b)
    return add_to_a

def curry_multiply(a):
    def multiply_by_a(b):
        return (a * b)
    return multiply_by_a

def partial_power(base):
    def raise_to(exponent):
        result = 1
        i = 0
        while (i < exponent):
            result = (result * base)
            i = (i + 1)
        return result
    return raise_to

def get_operation(op_type):
    def add_op(a, b):
        return (a + b)
    def mul_op(a, b):
        return (a * b)
    def sub_op(a, b):
        return (a - b)
    if (op_type == 'add'):
        return add_op
    elif (op_type == 'mul'):
        return mul_op
    else:
        return sub_op

def create_sequence():
    current = 0
    def next():
        nonlocal current
        current = (current + 1)
        return current
    def reset():
        nonlocal current
        current = 0
        return current
    def get_current():
        return current
    return {'next': next, 'reset': reset, 'current': get_current}

def create_person(name, age):
    person_name = name
    person_age = age
    def get_name():
        return person_name
    def get_age():
        return person_age
    def have_birthday():
        nonlocal person_age
        person_age = (person_age + 1)
        return person_age
    return {'name': get_name, 'age': get_age, 'birthday': have_birthday}

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

def apply_to_array(arr, func):
    len = get_length(arr)
    result = []
    i = 0
    while (i < len):
        result = (result + [_safe_call(func, arr[i])])
        i = (i + 1)
    return result

def main():
    results = {}
    counter = create_counter(10)
    results['count1'] = _safe_call(counter)
    results['count2'] = _safe_call(counter)
    results['count3'] = _safe_call(counter)
    account = create_account(100)
    results['initial'] = _safe_method_call(account, 'balance')
    results['after_deposit'] = _safe_method_call(account, 'deposit', 50)
    results['after_withdraw'] = _safe_method_call(account, 'withdraw', 30)
    results['final_balance'] = _safe_method_call(account, 'balance')
    double = create_multiplier(2)
    triple = create_multiplier(3)
    add_five = create_adder(5)
    results['double_10'] = _safe_call(double, 10)
    results['triple_10'] = _safe_call(triple, 10)
    results['add_five_10'] = _safe_call(add_five, 10)
    add_5 = curry_add(5)
    mul_3 = curry_multiply(3)
    results['curried_add'] = _safe_call(add_5, 10)
    results['curried_mul'] = _safe_call(mul_3, 7)
    power_of_2 = partial_power(2)
    power_of_3 = partial_power(3)
    results['two_pow_5'] = _safe_call(power_of_2, 5)
    results['three_pow_3'] = _safe_call(power_of_3, 3)
    add_func = get_operation('add')
    mul_func = get_operation('mul')
    results['dynamic_add'] = _safe_call(add_func, 8, 7)
    results['dynamic_mul'] = _safe_call(mul_func, 8, 7)
    seq = create_sequence()
    results['seq1'] = _safe_method_call(seq, 'next')
    results['seq2'] = _safe_method_call(seq, 'next')
    results['seq3'] = _safe_method_call(seq, 'next')
    _safe_method_call(seq, 'reset')
    results['seq_after_reset'] = _safe_method_call(seq, 'next')
    person = create_person('Alice', 25)
    results['person_name'] = _safe_method_call(person, 'name')
    results['person_age'] = _safe_method_call(person, 'age')
    results['age_after_birthday'] = _safe_method_call(person, 'birthday')
    results['person_age_final'] = _safe_method_call(person, 'age')
    test_array = [1, 2, 3, 4, 5]
    square_func = create_multiplier(1)
    def square(x):
        return (x * x)
    results['squared_array'] = apply_to_array(test_array, square)
    counter_a = create_counter(0)
    counter_b = create_counter(100)
    results['counter_a1'] = _safe_call(counter_a)
    results['counter_b1'] = _safe_call(counter_b)
    results['counter_a2'] = _safe_call(counter_a)
    results['counter_b2'] = _safe_call(counter_b)
    return results

test_results = main()

# End of generated code