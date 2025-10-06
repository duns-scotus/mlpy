"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

def add(a, b):
    return (a + b)

def subtract(a, b):
    return (a - b)

def multiply(a, b):
    return (a * b)

def divide(a, b):
    if (b == 0):
        return 0
    return (a / b)

def power(a, b):
    result = 1
    i = 0
    while (i < b):
        result = (result * a)
        i = (i + 1)
    return result

def dispatch_operation(op, a, b):
    if (op == 'add'):
        return add(a, b)
    elif (op == 'subtract'):
        return subtract(a, b)
    elif (op == 'multiply'):
        return multiply(a, b)
    elif (op == 'divide'):
        return divide(a, b)
    elif (op == 'power'):
        return power(a, b)
    else:
        return 0

def create_calculator():
    def calc_add(x, y):
        return (x + y)
    def calc_sub(x, y):
        return (x - y)
    def calc_mul(x, y):
        return (x * y)
    return {'add': calc_add, 'sub': calc_sub, 'mul': calc_mul}

def strategy_bubble(arr, len):
    i = 0
    while (i < len):
        j = 0
        while (j < ((len - i) - 1)):
            if (arr[j] > arr[(j + 1)]):
                temp = arr[j]
                arr[j] = arr[(j + 1)]
                arr[(j + 1)] = temp
            j = (j + 1)
        i = (i + 1)
    return arr

def strategy_insertion(arr, len):
    i = 1
    while (i < len):
        key = arr[i]
        j = (i - 1)
        while ((j >= 0) and (arr[j] > key)):
            arr[(j + 1)] = arr[j]
            j = (j - 1)
        arr[(j + 1)] = key
        i = (i + 1)
    return arr

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

def execute_strategy(strategy_name, arr):
    len = get_length(arr)
    result = []
    i = 0
    while (i < len):
        result = (result + [arr[i]])
        i = (i + 1)
    if (strategy_name == 'bubble'):
        return strategy_bubble(result, len)
    elif (strategy_name == 'insertion'):
        return strategy_insertion(result, len)
    else:
        return result

def create_command(action, value):
    return {'action': action, 'value': value}

def execute_command(state, command):
    if (_safe_attr_access(command, 'action') == 'increment'):
        state['counter'] = (_safe_attr_access(state, 'counter') + _safe_attr_access(command, 'value'))
    elif (_safe_attr_access(command, 'action') == 'decrement'):
        state['counter'] = (_safe_attr_access(state, 'counter') - _safe_attr_access(command, 'value'))
    elif (_safe_attr_access(command, 'action') == 'multiply'):
        state['counter'] = (_safe_attr_access(state, 'counter') * _safe_attr_access(command, 'value'))
    elif (_safe_attr_access(command, 'action') == 'reset'):
        state['counter'] = 0
    return state

def compose(f, g):
    def composed(x):
        return _safe_call(f, _safe_call(g, x))
    return composed

def double(x):
    return (x * 2)

def add_ten(x):
    return (x + 10)

def square(x):
    return (x * x)

def pipeline(value, functions):
    len = get_length(functions)
    result = value
    i = 0
    while (i < len):
        func = functions[i]
        result = _safe_call(func, result)
        i = (i + 1)
    return result

def main():
    results = {}
    results['add_5_3'] = dispatch_operation('add', 5, 3)
    results['mul_4_7'] = dispatch_operation('multiply', 4, 7)
    results['pow_2_5'] = dispatch_operation('power', 2, 5)
    calc = create_calculator()
    results['calc_add'] = _safe_method_call(calc, 'add', 10, 5)
    results['calc_sub'] = _safe_method_call(calc, 'sub', 10, 5)
    results['calc_mul'] = _safe_method_call(calc, 'mul', 10, 5)
    test_arr = [5, 2, 8, 1, 9]
    results['bubble_sorted'] = execute_strategy('bubble', test_arr)
    results['insertion_sorted'] = execute_strategy('insertion', test_arr)
    state = {'counter': 0}
    commands = [create_command('increment', 5), create_command('increment', 3), create_command('multiply', 2), create_command('decrement', 4)]
    i = 0
    cmd_len = get_length(commands)
    while (i < cmd_len):
        state = execute_command(state, commands[i])
        i = (i + 1)
    results['final_counter'] = _safe_attr_access(state, 'counter')
    double_then_add_ten = compose(add_ten, double)
    results['composed_5'] = _safe_call(double_then_add_ten, 5)
    pipeline_funcs = [double, add_ten, square]
    results['pipeline_3'] = pipeline(3, pipeline_funcs)
    operations = [{'op': 'add', 'a': 10, 'b': 5}, {'op': 'multiply', 'a': 3, 'b': 4}, {'op': 'power', 'a': 2, 'b': 3}, {'op': 'subtract', 'a': 20, 'b': 7}]
    batch_results = []
    i = 0
    op_len = get_length(operations)
    while (i < op_len):
        op = operations[i]
        batch_results = (batch_results + [dispatch_operation(_safe_attr_access(op, 'op'), _safe_attr_access(op, 'a'), _safe_attr_access(op, 'b'))])
        i = (i + 1)
    results['batch_operations'] = batch_results
    return results

test_results = main()

# End of generated code