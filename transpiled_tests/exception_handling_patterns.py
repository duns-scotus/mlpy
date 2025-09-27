"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

import from mlpy.ml.errors.exceptions import MLUserException

from mlpy.stdlib.string_bridge import string as ml_string

from mlpy.stdlib.datetime_bridge import datetime as ml_datetime

# WARNING: Import 'regex' requires security review
# import regex

def basic_exception_handling():
    print('=== Basic Exception Handling Patterns ===')
    def safe_division(a, b):
        try:
            if (b == 0):
                raise MLUserException(None)
            result = (a / b)
            return {'success': True, 'value': result, 'error': None}
        except error:
            return {'success': False, 'value': None, 'error': (str('Caught exception: ') + str(error))}
    print('Testing safe division:')
    result1 = safe_division(10, 2)
    result2 = safe_division(15, 3)
    result3 = safe_division(8, 0)
    result4 = safe_division(20, 4)
    print((str('10 / 2: ') + str(result1['value'] if result1['success'] else result1['error'])))
    print((str('15 / 3: ') + str(result2['value'] if result2['success'] else result2['error'])))
    print((str('8 / 0: ') + str(result3['value'] if result3['success'] else result3['error'])))
    print((str('20 / 4: ') + str(result4['value'] if result4['success'] else result4['error'])))
    return [result1, result2, result3, result4]

def try_catch_finally_patterns():
    print('\\n=== Try-Catch-Finally Patterns ===')
    def process_file_data(filename, data):
        resource_opened = False
        processing_log = []
        try:
            processing_log[processing_log['length']()] = (str('Opening file: ') + str(filename))
            if (ml_string.length(filename) == 0):
                raise MLUserException(None)
            resource_opened = True
            processing_log[processing_log['length']()] = 'File opened successfully'
            if ((data == None) or (data['length']() == 0)):
                raise MLUserException(None)
            processed_count = 0
            i = 0
            while (i < data['length']()):
                item = data[i]
                if ((typeof(item) == 'string') and (ml_string.length(item) > 0)):
                    processed_count = (processed_count + 1)
                elif ((typeof(item) == 'number') and (item > 0)):
                    processed_count = (processed_count + 1)
                else:
                    raise MLUserException(None)
                i = (i + 1)
            processing_log[processing_log['length']()] = (str((str('Processed ') + str(processed_count))) + str(' items successfully'))
            return {'success': True, 'processed_items': processed_count, 'log': processing_log, 'error': None}
        except error:
            processing_log[processing_log['length']()] = (str('Error occurred: ') + str(error))
            return {'success': False, 'processed_items': 0, 'log': processing_log, 'error': error}
    print('Testing file processing with various scenarios:')
    valid_data = ['item1', 'item2', 42, 'item3', 17]
    invalid_data = ['valid', None, 'another']
    empty_data = []
    scenario1 = process_file_data('data.txt', valid_data)
    scenario2 = process_file_data('', valid_data)
    scenario3 = process_file_data('test.txt', invalid_data)
    scenario4 = process_file_data('empty.txt', empty_data)
    scenarios = [scenario1, scenario2, scenario3, scenario4]
    scenario_names = ['Valid data', 'Empty filename', 'Invalid data', 'Empty data']
    j = 0
    while (j < scenarios['length']()):
        scenario = scenarios[j]
        name = scenario_names[j]
        print((str('\\nScenario: ') + str(name)))
        print((str('  Success: ') + str(scenario['success'])))
        if (scenario['error'] != None):
            print((str('  Error: ') + str(scenario['error'])))
        print((str('  Log entries: ') + str(scenario['log']['length']())))
        k = 0
        while (k < scenario['log']['length']()):
            print((str('    ') + str(scenario['log'][k])))
            k = (k + 1)
        j = (j + 1)
    return scenarios

def nested_exception_handling():
    print('\\n=== Nested Exception Handling ===')
    def complex_data_processor(input_data):
        main_log = []
        processed_results = []
        total_errors = 0
        try:
            main_log[main_log['length']()] = 'Starting complex data processing'
            if (input_data == None):
                raise MLUserException(None)
            i = 0
            while (i < input_data['length']()):
                section = input_data[i]
                section_result = None
                try:
                    main_log[main_log['length']()] = (str('Processing section ') + str(i))
                    if (section['type'] == 'numeric'):
                        section_result = process_numeric_section(section)
                    elif (section['type'] == 'text'):
                        section_result = process_text_section(section)
                    elif (section['type'] == 'mixed'):
                        section_result = process_mixed_section(section)
                    else:
                        raise MLUserException(None)
                    processed_results[processed_results['length']()] = section_result
                    main_log[main_log['length']()] = (str((str('Section ') + str(i))) + str(' processed successfully'))
                except section_error:
                    main_log[main_log['length']()] = (str((str((str('Error in section ') + str(i))) + str(': '))) + str(section_error))
                    total_errors = (total_errors + 1)
                    processed_results[processed_results['length']()] = {'success': False, 'error': section_error, 'section_index': i}
                i = (i + 1)
            main_log[main_log['length']()] = (str('Processing completed. Errors: ') + str(total_errors))
            return {'success': (total_errors == 0), 'results': processed_results, 'error_count': total_errors, 'log': main_log, 'error': None}
        except main_error:
            main_log[main_log['length']()] = (str('Main processing error: ') + str(main_error))
            return {'success': False, 'results': processed_results, 'error_count': (total_errors + 1), 'log': main_log, 'error': main_error}
    def process_numeric_section(section):
        try:
            if ((section['data'] == None) or (section['data']['length']() == 0)):
                raise MLUserException(None)
            sum = 0
            count = 0
            l = 0
            while (l < section['data']['length']()):
                item = section['data'][l]
                if (typeof(item) != 'number'):
                    raise MLUserException(None)
                sum = (sum + item)
                count = (count + 1)
                l = (l + 1)
            average = (sum / count)
            return {'success': True, 'type': 'numeric', 'sum': sum, 'count': count, 'average': average}
        except error:
            raise MLUserException(None)
    def process_text_section(section):
        try:
            if ((section['data'] == None) or (section['data']['length']() == 0)):
                raise MLUserException(None)
            total_length = 0
            word_count = 0
            m = 0
            while (m < section['data']['length']()):
                item = section['data'][m]
                if (typeof(item) != 'string'):
                    raise MLUserException(None)
                total_length = (total_length + ml_string.length(item))
                words = ml_string.split(item, ' ')
                word_count = (word_count + words['length']())
                m = (m + 1)
            return {'success': True, 'type': 'text', 'total_length': total_length, 'word_count': word_count, 'item_count': section['data']['length']()}
        except error:
            raise MLUserException(None)
    def process_mixed_section(section):
        try:
            if ((section['data'] == None) or (section['data']['length']() == 0)):
                raise MLUserException(None)
            string_count = 0
            number_count = 0
            other_count = 0
            n = 0
            while (n < section['data']['length']()):
                item = section['data'][n]
                item_type = typeof(item)
                if (item_type == 'string'):
                    string_count = (string_count + 1)
                elif (item_type == 'number'):
                    number_count = (number_count + 1)
                else:
                    other_count = (other_count + 1)
                n = (n + 1)
            return {'success': True, 'type': 'mixed', 'string_count': string_count, 'number_count': number_count, 'other_count': other_count, 'total_items': section['data']['length']()}
        except error:
            raise MLUserException(None)
    test_data = [{'type': 'numeric', 'data': [1, 2, 3, 4, 5]}, {'type': 'text', 'data': ['hello world', 'foo bar', 'test string']}, {'type': 'mixed', 'data': ['text', 42, 'more text', 17, True]}, {'type': 'numeric', 'data': [10, 'invalid', 30]}, {'type': 'unknown', 'data': ['should', 'fail']}, {'type': 'text', 'data': []}]
    print('Testing complex nested exception handling:')
    result = complex_data_processor(test_data)
    print((str('Overall success: ') + str(result['success'])))
    print((str('Error count: ') + str(result['error_count'])))
    print((str('Results processed: ') + str(result['results']['length']())))
    print('\\nProcessing log:')
    o = 0
    while (o < result['log']['length']()):
        print((str('  ') + str(result['log'][o])))
        o = (o + 1)
    return result

def exception_propagation_chaining():
    print('\\n=== Exception Propagation and Chaining ===')
    def level1_function(input):
        try:
            print('Level 1: Processing input')
            result = level2_function(input)
            print('Level 1: Completed successfully')
            return result
        except error:
            enhanced_error = (str('Level 1 error: ') + str(error))
            print((str('Level 1: Caught and re-throwing - ') + str(enhanced_error)))
            raise MLUserException(None)
    def level2_function(input):
        try:
            print('Level 2: Validating input')
            if (input == None):
                raise MLUserException(None)
            result = level3_function(input)
            print('Level 2: Validation passed')
            return result
        except error:
            enhanced_error = (str('Level 2 error: ') + str(error))
            print((str('Level 2: Caught and re-throwing - ') + str(enhanced_error)))
            raise MLUserException(None)
    def level3_function(input):
        try:
            print('Level 3: Core processing')
            if (typeof(input) != 'object'):
                raise MLUserException(None)
            if (input['value'] == None):
                raise MLUserException(None)
            result = level4_function(input['value'])
            print('Level 3: Core processing completed')
            return {'level3_result': result, 'processed_by': 'level3'}
        except error:
            enhanced_error = (str('Level 3 error: ') + str(error))
            print((str('Level 3: Caught and re-throwing - ') + str(enhanced_error)))
            raise MLUserException(None)
    def level4_function(value):
        print('Level 4: Final processing')
        if (value < 0):
            raise MLUserException(None)
        if (value > 1000):
            raise MLUserException(None)
        result = ((value * value) + 10)
        print((str('Level 4: Final result calculated: ') + str(result)))
        return result
    test_inputs = [{'value': 5}, {'value': 3}, {'value': 1500}, {'missing': 42}, 'not_object', None]
    input_descriptions = ['Valid input (value: 5)', 'Negative value (-3)', 'Large value (1500)', 'Missing value property', 'String instead of object', 'Null input']
    print('Testing exception propagation chain:')
    p = 0
    while (p < test_inputs['length']()):
        input = test_inputs[p]
        description = input_descriptions[p]
        print((str((str((str((str('\\n--- Test ') + str((p + 1)))) + str(': '))) + str(description))) + str(' ---')))
        try:
            result = level1_function(input)
            print((str('SUCCESS: Final result = ') + str(result['level3_result'])))
        except final_error:
            print((str('FINAL ERROR: ') + str(final_error)))
        p = (p + 1)
    return test_inputs

def custom_exception_types():
    print('\\n=== Custom Exception Types and Error Handling ===')
    def create_error(type, message, code, context):
        return {'error_type': type, 'message': message, 'error_code': code, 'context': context, 'timestamp': ml_datetime.now()}
    def handle_user_registration(user_data):
        validation_errors = []
        try:
            if (user_data == None):
                raise MLUserException(None)
            if ((user_data['username'] == None) or (ml_string.length(user_data['username']) == 0)):
                validation_errors[validation_errors['length']()] = create_error('ValidationError', 'Username is required', 'USER_002', {'field': 'username'})
            elif (ml_string.length(user_data['username']) < 3):
                validation_errors[validation_errors['length']()] = create_error('ValidationError', 'Username must be at least 3 characters', 'USER_003', {'field': 'username', 'min_length': 3})
            elif regex['is_alphanumeric_underscore'](user_data['username']):
                validation_errors[validation_errors['length']()] = create_error('ValidationError', 'Username can only contain letters, numbers, and underscores', 'USER_004', {'field': 'username'})
            if ((user_data['email'] == None) or (ml_string.length(user_data['email']) == 0)):
                validation_errors[validation_errors['length']()] = create_error('ValidationError', 'Email is required', 'USER_005', {'field': 'email'})
            elif regex['is_email'](user_data['email']):
                validation_errors[validation_errors['length']()] = create_error('ValidationError', 'Invalid email format', 'USER_006', {'field': 'email', 'value': user_data['email']})
            if ((user_data['password'] == None) or (ml_string.length(user_data['password']) == 0)):
                validation_errors[validation_errors['length']()] = create_error('ValidationError', 'Password is required', 'USER_007', {'field': 'password'})
            elif (ml_string.length(user_data['password']) < 8):
                validation_errors[validation_errors['length']()] = create_error('ValidationError', 'Password must be at least 8 characters', 'USER_008', {'field': 'password', 'min_length': 8})
            if (user_data['age'] != None):
                if (typeof(user_data['age']) != 'number'):
                    validation_errors[validation_errors['length']()] = create_error('ValidationError', 'Age must be a number', 'USER_009', {'field': 'age', 'value': user_data['age']})
                elif (user_data['age'] < 13):
                    validation_errors[validation_errors['length']()] = create_error('BusinessLogicError', 'Users must be at least 13 years old', 'USER_010', {'field': 'age', 'min_age': 13})
                elif (user_data['age'] > 120):
                    validation_errors[validation_errors['length']()] = create_error('ValidationError', 'Invalid age value', 'USER_011', {'field': 'age', 'max_age': 120})
            if (validation_errors['length']() > 0):
                raise MLUserException(None)
            if ((user_data['username'] == 'admin') or (user_data['username'] == 'root')):
                raise MLUserException(None)
            if (user_data['email'] == 'blacklisted@example.com'):
                raise MLUserException(None)
            user_id = (str('USER_') + str(ml_datetime.timestamp()))
            return {'success': True, 'user_id': user_id, 'username': user_data['username'], 'email': user_data['email'], 'created_at': ml_datetime.now()}
        except error:
            return {'success': False, 'error': error, 'user_id': None}
    test_users = [{'username': 'john_doe', 'email': 'john@example.com', 'password': 'securepass123', 'age': 25}, {'username': 'x', 'email': 'invalid-email', 'password': 'short', 'age': 12}, {'username': 'admin', 'email': 'admin@example.com', 'password': 'adminpass123', 'age': 30}, {'username': 'jane_smith', 'email': 'blacklisted@example.com', 'password': 'password123', 'age': 28}, {'email': 'missing@username.com', 'password': 'password123', 'age': 22}, None]
    user_descriptions = ['Valid user data', 'Multiple validation errors', 'Reserved username', 'Blacklisted email', 'Missing username', 'Null user data']
    print('Testing custom exception handling:')
    q = 0
    while (q < test_users['length']()):
        user = test_users[q]
        description = user_descriptions[q]
        print((str((str((str((str('\\n--- Registration Test ') + str((q + 1)))) + str(': '))) + str(description))) + str(' ---')))
        result = handle_user_registration(user)
        if result['success']:
            print((str('SUCCESS: User created with ID ') + str(result['user_id'])))
        else:
            error = result['error']
            print((str((str((str((str((str((str('FAILED: ') + str(error['error_type']))) + str(' - '))) + str(error['message']))) + str(' (Code: '))) + str(error['error_code']))) + str(')')))
            if (error['error_type'] == 'MultipleValidationErrors'):
                print('Validation Errors:')
                r = 0
                while (r < error['context']['errors']['length']()):
                    val_error = error['context']['errors'][r]
                    print((str((str((str((str('  - ') + str(val_error['message']))) + str(' (Code: '))) + str(val_error['error_code']))) + str(')')))
                    r = (r + 1)
        q = (q + 1)
    return test_users

def error_recovery_fallback():
    print('\\n=== Error Recovery and Fallback Strategies ===')
    def resilient_data_service(request):
        attempts_log = []
        max_retries = 3
        try:
            attempts_log[attempts_log['length']()] = 'Attempting primary service'
            result = call_primary_service(request)
            attempts_log[attempts_log['length']()] = 'Primary service succeeded'
            return {'success': True, 'data': result, 'service_used': 'primary', 'attempts': attempts_log}
        except primary_error:
            attempts_log[attempts_log['length']()] = (str('Primary service failed: ') + str(primary_error))
        try:
            attempts_log[attempts_log['length']()] = 'Attempting secondary service'
            result = call_secondary_service(request)
            attempts_log[attempts_log['length']()] = 'Secondary service succeeded'
            return {'success': True, 'data': result, 'service_used': 'secondary', 'attempts': attempts_log}
        except secondary_error:
            attempts_log[attempts_log['length']()] = (str('Secondary service failed: ') + str(secondary_error))
        try:
            attempts_log[attempts_log['length']()] = 'Attempting cached data'
            result = get_cached_data(request)
            if (result != None):
                attempts_log[attempts_log['length']()] = 'Cached data found'
                return {'success': True, 'data': result, 'service_used': 'cache', 'attempts': attempts_log}
            else:
                attempts_log[attempts_log['length']()] = 'No cached data available'
        except cache_error:
            attempts_log[attempts_log['length']()] = (str('Cache access failed: ') + str(cache_error))
        attempts_log[attempts_log['length']()] = 'Using default fallback data'
        return {'success': True, 'data': get_default_data(request), 'service_used': 'default', 'attempts': attempts_log}
    def call_primary_service(request):
        if (request['id'] == 'fail_primary'):
            raise MLUserException(None)
        if (request['id'] == 'fail_all'):
            raise MLUserException(None)
        return {'source': 'primary', 'data': (str('Primary data for ') + str(request['id'])), 'quality': 'high'}
    def call_secondary_service(request):
        if (request['id'] == 'fail_all'):
            raise MLUserException(None)
        if (request['id'] == 'fail_secondary'):
            raise MLUserException(None)
        return {'source': 'secondary', 'data': (str('Secondary data for ') + str(request['id'])), 'quality': 'medium'}
    def get_cached_data(request):
        if (request['id'] == 'fail_all'):
            return None
        if (request['id'] == 'cached_only'):
            return {'source': 'cache', 'data': (str('Cached data for ') + str(request['id'])), 'quality': 'cached'}
        return None
    def get_default_data(request):
        return {'source': 'default', 'data': (str('Default data for ') + str(request['id'])), 'quality': 'low'}
    test_requests = [{'id': 'normal_request'}, {'id': 'fail_primary'}, {'id': 'fail_secondary'}, {'id': 'cached_only'}, {'id': 'fail_all'}]
    request_descriptions = ['Normal request (should use primary)', 'Primary fails (should use secondary)', 'Secondary fails (should use primary)', 'Only cached data available', 'All services fail (should use default)']
    print('Testing resilient data service:')
    s = 0
    while (s < test_requests['length']()):
        request = test_requests[s]
        description = request_descriptions[s]
        print((str((str((str((str('\\n--- Request ') + str((s + 1)))) + str(': '))) + str(description))) + str(' ---')))
        result = resilient_data_service(request)
        print((str('Service used: ') + str(result['service_used'])))
        print((str('Data quality: ') + str(result['data']['quality'])))
        print('Attempts made:')
        t = 0
        while (t < result['attempts']['length']()):
            print((str('  ') + str(result['attempts'][t])))
            t = (t + 1)
        s = (s + 1)
    return test_requests

def main():
    print('==============================================')
    print('  EXCEPTION HANDLING PATTERNS TEST')
    print('==============================================')
    results = {}
    results['basic'] = basic_exception_handling()
    results['try_catch_finally'] = try_catch_finally_patterns()
    results['nested'] = nested_exception_handling()
    results['propagation'] = exception_propagation_chaining()
    results['custom_types'] = custom_exception_types()
    results['recovery'] = error_recovery_fallback()
    print('\\n==============================================')
    print('  ALL EXCEPTION HANDLING TESTS COMPLETED')
    print('==============================================')
    return results

main()

# End of generated code