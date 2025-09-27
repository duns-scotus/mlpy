"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

def add_numbers(a, b):
    return (a + b)

wrong_call1 = add_numbers('hello', 42)

wrong_call2 = add_numbers(10, True)

wrong_call3 = add_numbers([1, 2], 42)

undefined_result = (some_undefined_variable + 10)

not_array = 'hello'

invalid_access = not_array[0]

not_object = 42

invalid_property = not_object['name']

def get_string():
    return 'hello'

number_var = get_string()

def three_params(a, b, c):
    return ((a + b) + c)

wrong_args1 = three_params(1, 2)

wrong_args2 = three_params(1, 2, 3, 4)

text = 'hello'

number = 42

invalid_math = (text * number)

invalid_division = (text / 2)

invalid_subtraction = (text - 10)

array_comparison = ([1, 2, 3] < 5)

object_comparison = ({'a': 1} > 10)

def should_return_number():
    return 'not a number'

def should_return_string():
    return 42

numbers = [1, 2, 3]

numbers[0] = 'string'

numbers['invalid'] = 42

user = {'name': 'John', 'age': 30, 'active': True}

user['age'] = 'thirty'

user['active'] = 'yes'

maybe_object = None

nested_access = maybe_object['property']['subproperty']

not_function = 42

invalid_call = not_function()

string_array = ['a', 'b', 'c']

for ml_unknown_identifier_2145182723696 in string_array:
    math_result = (item * 2)

mixed = [1, 'two', True]

for ml_unknown_identifier_2145182727824 in mixed:
    length = element['length']

console['log']('Type error demo - many errors should be detected')

# End of generated code