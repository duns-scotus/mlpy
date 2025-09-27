"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

person_data = {'name': 'Alice', 'age': 30, 'email': 'alice@example.com'}

def processValue(input, type_hint):
    if (type_hint == 'number'):
        if (input > 100):
            return (str('Large number: ') + str(input))
        elif (input > 0):
            return (str('Small number: ') + str(input))
        else:
            return (str('Zero or negative: ') + str(input))
    elif (type_hint == 'string'):
        return (str('Text: ') + str(input))
    else:
        return 'Unknown type'

def createSquares(numbers):
    squares = []
    i = 0
    while (i < numbers['length']()):
        value = numbers[i]
        if (value > 2):
            squares['push']((value * value))
        i = (i + 1)
    return squares

def divide(a, b):
    if (b == 0):
        return {'success': False, 'error': 'Division by zero error'}
    else:
        return {'success': True, 'value': (a / b)}

def complexCalculation(x, y):
    result1 = divide(x, 2)
    if result1['success']:
        return result1
    result2 = divide(y, 3)
    if result2['success']:
        return result2
    return {'success': True, 'value': (result1['value'] + result2['value'])}

def main_demo():
    print('Processing number 150:')
    print(processValue(150, 'number'))
    print("Processing string 'hello':")
    print(processValue('hello', 'string'))
    numbers = [1, 2, 3, 4, 5]
    squares = createSquares(numbers)
    print((str('Original numbers: ') + str(numbers)))
    print((str('Filtered squares: ') + str(squares)))
    print('Testing division:')
    safe_result = complexCalculation(10, 6)
    if safe_result['success']:
        print((str('Result: ') + str(safe_result['value'])))
    else:
        print((str('Error: ') + str(safe_result['error'])))
    print('Person data:')
    print((str('Name: ') + str(person_data['name'])))
    print((str('Age: ') + str(person_data['age'])))
    print((str('Email: ') + str(person_data['email'])))
    print('Advanced ML features demonstration complete!')

main_demo()

# End of generated code