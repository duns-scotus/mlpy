"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

import from mlpy.ml.errors.exceptions import MLUserException

def add_numbers(a, b):
    return (a + b)

def concatenate_strings(s1, s2):
    return (s1 + s2)

def process_array(arr):
    length = arr['length']
    first = arr[0]
    return first

number_var = 42

string_var = 'hello'

boolean_var = True

array_var = [1, 2, 3, 4]

object_var = {'name': 'test', 'value': 100, 'active': True}

sum_result = add_numbers(10, 20)

concat_result = concatenate_strings('hello', ' world')

array_result = process_array([1, 2, 3])

numbers = [1, 2, 3]

first_number = numbers[0]

numbers[1] = 999

obj = {'id': 1, 'name': 'item', 'properties': {'color': 'blue', 'size': 'large'}}

item_id = obj['id']

item_name = obj['name']

item_color = obj['properties']['color']

if (number_var > 0):
    console['log']('Positive number')
else:
    console['log']('Non-positive number')

for ml_unknown_identifier_2231962371280 in array_var:
    console['log'](item)

while (number_var > 0):
    number_var = (number_var - 1)

def calculate_area(width, height):
    area = (width * height)
    return area

def get_user_info():
    return {'id': 123, 'username': 'testuser', 'active': True}

mixed_addition = (str(5) + str('text'))

comparison = (number_var < 100)

logical_op = (boolean_var and (number_var > 0))

def double_value(x):
    return (x * 2)

def apply_operation(value):
    return (double_value(value) + 10)

final_result = apply_operation(15)

string_array = ['apple', 'banana', 'cherry']

mixed_array = [1, 'two', True]

complex_object = {'user': {'profile': {'name': 'John Doe', 'age': 30, 'preferences': {'theme': 'dark', 'notifications': True}}, 'settings': {'privacy': 'private', 'language': 'en'}}, 'data': [{'key': 'item1', 'value': 100}, {'key': 'item2', 'value': 200}]}

user_name = complex_object['user']['profile']['name']

user_theme = complex_object['user']['profile']['preferences']['theme']

first_data_item = complex_object['data'][0]

first_item_value = complex_object['data'][0]['value']

try:
    risky_operation = divide_numbers(10, 0)
except error:
    console['log']((str('Error occurred: ') + str(error)))

def divide_numbers(a, b):
    if (b == 0):
        raise MLUserException(None)
    return (a / b)

pi_value = Math['PI']

sqrt_result = Math['sqrt'](16)

power_result = Math['pow'](2, 8)

message = 'Hello World'

message_length = message['length']

uppercase_message = message['toUpperCase']()

console['log']('Type checking demo completed successfully')

# End of generated code