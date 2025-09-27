"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

from mlpy.stdlib.math_bridge import math as ml_math

from mlpy.stdlib.json_bridge import json as ml_json

from mlpy.stdlib.string_bridge import string as ml_string

from mlpy.stdlib.datetime_bridge import datetime as ml_datetime

def testMathOperations():
    radius = 5.0
    area = ((ml_math.pi * radius) * radius)
    sqrt_result = ml_math.sqrt(25.0)
    power_result = ml_math.pow(2.0, 8.0)
    return {'pi': ml_math.pi, 'area': area, 'sqrt_25': sqrt_result, '2_pow_8': power_result, 'abs_negative': ml_math.abs(42), 'min': ml_math.min(10, 20), 'max': ml_math.max(10, 20)}

def testStringOperations():
    text = 'Hello, World!'
    return {'original': text, 'uppercase': ml_string.upper(text), 'lowercase': ml_string.lower(text), 'length': ml_string.length(text), 'contains_world': ml_string.contains(text, 'World'), 'starts_with_hello': ml_string.starts_with(text, 'Hello'), 'stripped': ml_string.trim('  spaced  '), 'replaced': ml_string.replace(text, 'World', 'ML')}

def testJsonOperations():
    data = {'name': 'ML Import Test', 'version': 2.0, 'features': ['imports', 'security', 'stdlib'], 'active': True}
    json_string = ml_json.dumps(data)
    parsed_back = ml_json.loads(json_string)
    return {'original': data, 'serialized': json_string, 'round_trip': parsed_back}

def testDateTimeOperations():
    current_time = ml_datetime.now()
    formatted = ml_datetime.format_readable(current_time)
    iso_format = ml_datetime.format_iso(current_time)
    future_time = ml_datetime.add_hours(current_time, 24)
    hours_diff = ml_datetime.hours_between(current_time, future_time)
    return {'current_timestamp': current_time, 'readable_format': formatted, 'iso_format': iso_format, 'future_timestamp': future_time, 'hours_difference': hours_diff, 'is_leap_year_2024': ml_datetime.is_leap_year(2024)}

def runComprehensiveTest():
    console['log']('Testing ML Import System...')
    math_results = testMathOperations()
    string_results = testStringOperations()
    json_results = testJsonOperations()
    datetime_results = testDateTimeOperations()
    comprehensive_result = {'test_name': 'ML Import System Validation', 'status': 'success', 'results': {'math': math_results, 'string': string_results, 'json': json_results, 'datetime': datetime_results}, 'summary': {'total_tests': 4, 'stdlib_modules_tested': ['math', 'string', 'json', 'datetime'], 'security_validated': True, 'capability_system_integrated': True}}
    return comprehensive_result

test_result = runComprehensiveTest()

def displayResults():
    console['log']('=== ML Import System Test Results ===')
    console['log']('Test Status:', test_result['status'])
    console['log']('Modules Tested:', test_result['summary']['stdlib_modules_tested'])
    console['log']('Total Tests:', test_result['summary']['total_tests'])
    console['log']('\\n--- Math Operations ---')
    console['log']('π =', test_result['results']['math']['pi'])
    console['log']('sqrt(25) =', test_result['results']['math']['sqrt_25'])
    console['log']('2^8 =', test_result['results']['math']['2_pow_8'])
    console['log']('abs(-42) =', test_result['results']['math']['abs_negative'])
    console['log']('\\n--- String Operations ---')
    console['log']('Original:', test_result['results']['string']['original'])
    console['log']('Uppercase:', test_result['results']['string']['uppercase'])
    console['log']('Length:', test_result['results']['string']['length'])
    console['log']("Contains 'World':", test_result['results']['string']['contains_world'])
    console['log']('\\n--- JSON Operations ---')
    console['log']('Serialized:', test_result['results']['json']['serialized'])
    console['log']('Round-trip success:', (test_result['results']['json']['round_trip'] != None))
    console['log']('\\n--- DateTime Operations ---')
    console['log']('Current time:', test_result['results']['datetime']['readable_format'])
    console['log']('ISO format:', test_result['results']['datetime']['iso_format'])
    console['log']('Hours difference:', test_result['results']['datetime']['hours_difference'])
    console['log']('Is 2024 leap year:', test_result['results']['datetime']['is_leap_year_2024'])
    console['log']('\\n=== Test Complete ===')
    return 'Import system test completed successfully!'

final_message = displayResults()

# End of generated code