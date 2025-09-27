"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

from mlpy.stdlib.math_bridge import math as ml_math

from mlpy.stdlib.json_bridge import json as ml_json

from mlpy.stdlib.random_bridge import random as ml_random

def mathOperations():
    radius = 5.0
    area = ((ml_math.pi * radius) * radius)
    sqrt_result = ml_math.sqrt(25.0)
    power_result = ml_math.pow(2.0, 8.0)
    return {'area': area, 'sqrt': sqrt_result, 'power': power_result, 'pi': ml_math.pi, 'e': ml_math.e}

def randomOperations():
    random_float = ml_random.random()
    random_choice = ml_random.choice([1, 2, 3, 4, 5])
    return {'random_float': random_float, 'choice': random_choice}

def jsonOperations():
    data = {'name': 'ML Program', 'version': 1.0, 'active': True}
    json_string = ml_json.dumps(data)
    return {'original': data, 'serialized': json_string}

def combinedOperations():
    math_result = mathOperations()
    random_result = randomOperations()
    json_result = jsonOperations()
    final_result = {'math': math_result, 'random': random_result, 'json': json_result, 'timestamp': 'generated_by_ml'}
    return final_result

# End of generated code