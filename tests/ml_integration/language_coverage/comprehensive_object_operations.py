"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData, typeof

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length

from mlpy.stdlib.string_bridge import string as ml_string

from mlpy.stdlib.collections_bridge import collections as ml_collections

def safe_upsert(arr, pos, item):
    if (pos < _safe_attr_access(arr, 'length')):
        new_arr = []
        i = 0
        while (i < _safe_attr_access(arr, 'length')):
            if (i == pos):
                new_arr = ml_collections.append(new_arr, item)
            else:
                new_arr = ml_collections.append(new_arr, arr[i])
            i = (i + 1)
        return new_arr
    else:
        return ml_collections.append(arr, item)

def safe_append(arr, item):
    return ml_collections.append(arr, item)

def object_to_string(obj):
    if (obj == None):
        return 'null'
    return '[Object]'

def object_creation_basics():
    print('=== Object Creation and Basics ===')
    empty_object = {}
    person = {'name': 'John Doe', 'age': 30, 'active': True, 'salary': 50000.0}
    student = {'name': 'Alice Johnson', 'grades': [95, 87, 92, 88], 'courses': ['Math', 'Science', 'History'], 'active': True}
    company = {'name': 'Tech Corp', 'founded': 2010, 'address': {'street': '123 Main St', 'city': 'Anytown', 'state': 'CA', 'zip': '12345'}, 'employees': {'total': 150, 'departments': ['Engineering', 'Sales', 'Marketing']}}
    print((str('Empty object: ') + str(object_to_string(empty_object))))
    print((str((str((str('Person name: ') + str(_safe_attr_access(person, 'name')))) + str(', age: '))) + str(ml_string.toString(_safe_attr_access(person, 'age')))))
    print((str((str((str('Student name: ') + str(_safe_attr_access(student, 'name')))) + str(', grade count: '))) + str(ml_string.toString(_safe_attr_access(_safe_attr_access(student, 'grades'), 'length')))))
    print((str((str((str((str('Company: ') + str(_safe_attr_access(company, 'name')))) + str(' (founded '))) + str(ml_string.toString(_safe_attr_access(company, 'founded'))))) + str(')')))
    return {'empty': empty_object, 'person': person, 'student': student, 'company': company}

def object_property_access():
    print('\\n=== Object Property Access and Modification ===')
    employee = {'id': 1001, 'name': 'Bob Smith', 'department': 'Engineering', 'skills': ['Python', 'Java', 'JavaScript'], 'active': True, 'salary': 75000, 'contact': {'email': 'bob@company.com', 'phone': '555-0123'}}
    print((str((str((str((str('Original employee: ') + str(_safe_attr_access(employee, 'name')))) + str(' ('))) + str(ml_string.toString(_safe_attr_access(employee, 'id'))))) + str(')')))
    emp_name = _safe_attr_access(employee, 'name')
    emp_id = _safe_attr_access(employee, 'id')
    emp_department = _safe_attr_access(employee, 'department')
    emp_active = _safe_attr_access(employee, 'active')
    print('\\nProperty Access:')
    print((str('Name: ') + str(emp_name)))
    print((str('ID: ') + str(ml_string.toString(emp_id))))
    print((str('Department: ') + str(emp_department)))
    print((str('Active: ') + str(ml_string.toString(emp_active))))
    emp_email = _safe_attr_access(_safe_attr_access(employee, 'contact'), 'email')
    emp_phone = _safe_attr_access(_safe_attr_access(employee, 'contact'), 'phone')
    print((str('Email: ') + str(emp_email)))
    print((str('Phone: ') + str(emp_phone)))
    first_skill = _safe_attr_access(employee, 'skills')[0]
    skill_count = _safe_attr_access(_safe_attr_access(employee, 'skills'), 'length')
    print((str('First skill: ') + str(first_skill)))
    print((str('Number of skills: ') + str(ml_string.toString(skill_count))))
    employee['department'] = 'DevOps'
    employee['salary'] = 80000
    employee['active'] = False
    print('\\nAfter modifications:')
    print((str('New department: ') + str(_safe_attr_access(employee, 'department'))))
    print((str('New salary: ') + str(ml_string.toString(_safe_attr_access(employee, 'salary')))))
    print((str('Active status: ') + str(ml_string.toString(_safe_attr_access(employee, 'active')))))
    _safe_attr_access(employee, 'contact')['email'] = 'bob.smith@newcompany.com'
    _safe_attr_access(employee, 'skills')[0] = 'Go'
    print((str('New email: ') + str(_safe_attr_access(_safe_attr_access(employee, 'contact'), 'email'))))
    print((str('Modified first skill: ') + str(_safe_attr_access(employee, 'skills')[0])))
    return {'original_name': emp_name, 'modified_employee': employee, 'contact_info': {'email': emp_email, 'phone': emp_phone}}

def object_composition_relationships():
    print('\\n=== Object Composition and Relationships ===')
    address = {'street': '456 Oak Ave', 'city': 'Springfield', 'state': 'IL', 'zip': '62701'}
    contact_info = {'email': 'contact@example.com', 'phone': '555-0199', 'fax': '555-0198'}
    person = {'name': 'Sarah Wilson', 'age': 28, 'address': address, 'contact': contact_info}
    project1 = {'name': 'Website Redesign', 'status': 'active', 'lead': person}
    project2 = {'name': 'Mobile App', 'status': 'planning', 'lead': person}
    print((str((str((str((str('Person: ') + str(_safe_attr_access(person, 'name')))) + str(' (age '))) + str(ml_string.toString(_safe_attr_access(person, 'age'))))) + str(')')))
    print((str((str((str('Project 1: ') + str(_safe_attr_access(project1, 'name')))) + str(' - '))) + str(_safe_attr_access(project1, 'status'))))
    print((str((str((str('Project 2: ') + str(_safe_attr_access(project2, 'name')))) + str(' - '))) + str(_safe_attr_access(project2, 'status'))))
    person['age'] = 29
    print("\\nAfter modifying shared person's age:")
    print((str('Person age: ') + str(ml_string.toString(_safe_attr_access(person, 'age')))))
    print((str('Project 1 lead age: ') + str(ml_string.toString(_safe_attr_access(_safe_attr_access(project1, 'lead'), 'age')))))
    print((str('Project 2 lead age: ') + str(ml_string.toString(_safe_attr_access(_safe_attr_access(project2, 'lead'), 'age')))))
    calculator = {'value': 0, 'add': lambda x: _safe_attr_access(calculator, 'value'), 'subtract': lambda x: _safe_attr_access(calculator, 'value'), 'multiply': lambda x: _safe_attr_access(calculator, 'value'), 'reset': lambda : _safe_attr_access(calculator, 'value')}
    print('\\nCalculator object with methods:')
    print((str('Initial value: ') + str(ml_string.toString(_safe_attr_access(calculator, 'value')))))
    result1 = _safe_attr_access(calculator, 'add')(10)
    print((str('After add(10): ') + str(ml_string.toString(result1))))
    result2 = _safe_attr_access(calculator, 'multiply')(3)
    print((str('After multiply(3): ') + str(ml_string.toString(result2))))
    result3 = _safe_attr_access(calculator, 'subtract')(5)
    print((str('After subtract(5): ') + str(ml_string.toString(result3))))
    return {'person': person, 'projects': [project1, project2], 'calculator': calculator, 'shared_modification_test': 'passed'}

def object_manipulation_utilities():
    print('\\n=== Object Manipulation Utilities ===')
    original_object = {'name': 'Test Object', 'value': 42, 'active': True, 'tags': ['important', 'test'], 'metadata': {'created': '2024-01-01', 'version': 1}}
    def shallow_copy_object(obj):
        copy = {'name': _safe_attr_access(obj, 'name'), 'value': _safe_attr_access(obj, 'value'), 'active': _safe_attr_access(obj, 'active'), 'tags': _safe_attr_access(obj, 'tags'), 'metadata': _safe_attr_access(obj, 'metadata')}
        return copy
    def has_property(obj, property_name):
        if (property_name == 'name'):
            return (_safe_attr_access(obj, 'name') != None)
        elif (property_name == 'value'):
            return (_safe_attr_access(obj, 'value') != None)
        elif (property_name == 'active'):
            return (_safe_attr_access(obj, 'active') != None)
        return False
    def merge_objects(obj1, obj2):
        merged = {'name': _safe_attr_access(obj2, 'name') if (_safe_attr_access(obj2, 'name') != None) else _safe_attr_access(obj1, 'name'), 'value': _safe_attr_access(obj2, 'value') if (_safe_attr_access(obj2, 'value') != None) else _safe_attr_access(obj1, 'value'), 'active': _safe_attr_access(obj2, 'active') if (_safe_attr_access(obj2, 'active') != None) else _safe_attr_access(obj1, 'active'), 'debug': _safe_attr_access(obj2, 'debug') if (_safe_attr_access(obj2, 'debug') != None) else _safe_attr_access(obj1, 'debug') if (_safe_attr_access(obj1, 'debug') != None) else False, 'timeout': _safe_attr_access(obj2, 'timeout') if (_safe_attr_access(obj2, 'timeout') != None) else _safe_attr_access(obj1, 'timeout') if (_safe_attr_access(obj1, 'timeout') != None) else 5000}
        return merged
    base_config = {'debug': False, 'timeout': 5000, 'retry_count': 3}
    user_config = {'debug': True, 'max_connections': 10}
    def transform_object_values(obj):
        transformed = {'name': ml_string.upper(_safe_attr_access(obj, 'name')), 'value': _safe_attr_access(obj, 'value'), 'active': _safe_attr_access(obj, 'active'), 'tags': _safe_attr_access(obj, 'tags'), 'metadata': _safe_attr_access(obj, 'metadata')}
        return transformed
    transformed_object = transform_object_values(original_object)
    print((str('Original object name: ') + str(_safe_attr_access(original_object, 'name'))))
    print((str('Transformed object name: ') + str(_safe_attr_access(transformed_object, 'name'))))
    def validate_person(person_obj):
        valid = True
        errors = []
        if ((_safe_attr_access(person_obj, 'name') == '') or (_safe_attr_access(person_obj, 'name') == None)):
            errors = safe_append(errors, 'Name is required')
            valid = False
        if ((_safe_attr_access(person_obj, 'age') < 0) or (_safe_attr_access(person_obj, 'age') > 150)):
            errors = safe_append(errors, 'Age must be between 0 and 150')
            valid = False
        return {'valid': valid, 'errors': errors, 'error_count': _safe_attr_access(errors, 'length')}
    valid_person = {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'}
    invalid_person = {'name': '', 'age': 5, 'email': 'invalid-email'}
    validation1 = validate_person(valid_person)
    validation2 = validate_person(invalid_person)
    print('\\nValidation Results:')
    print((str((str((str((str('Valid person validation: ') + str(ml_string.toString(_safe_attr_access(validation1, 'valid'))))) + str(' (errors: '))) + str(ml_string.toString(_safe_attr_access(validation1, 'error_count'))))) + str(')')))
    print((str((str((str((str('Invalid person validation: ') + str(ml_string.toString(_safe_attr_access(validation2, 'valid'))))) + str(' (errors: '))) + str(ml_string.toString(_safe_attr_access(validation2, 'error_count'))))) + str(')')))
    return {'original': original_object, 'transformed': transformed_object, 'validations': {'valid_person': validation1, 'invalid_person': validation2}}

def object_oriented_patterns():
    print('\\n=== Object-Oriented Programming Patterns ===')
    def create_person(name, age, email):
        person_obj = {'name': name, 'age': age, 'email': email, 'get_info': lambda : (str((str((str((str(_safe_attr_access(person_obj, 'name')) + str(' ('))) + str(ml_string.toString(_safe_attr_access(person_obj, 'age'))))) + str(') - '))) + str(_safe_attr_access(person_obj, 'email'))), 'celebrate_birthday': lambda : (str((str('Happy birthday! Now ') + str(ml_string.toString(_safe_attr_access(person_obj, 'age'))))) + str(' years old.'))}
        return person_obj
    person1 = create_person('Alice', 25, 'alice@example.com')
    person2 = create_person('Bob', 30, 'bob@example.com')
    print((str('Person 1: ') + str(_safe_attr_access(person1, 'name'))))
    print((str('Person 2: ') + str(_safe_attr_access(person2, 'name'))))
    info1 = _safe_attr_access(person1, 'get_info')()
    birthday_msg = _safe_attr_access(person1, 'celebrate_birthday')()
    print((str('Person 1 info: ') + str(info1)))
    print((str('Birthday message: ') + str(birthday_msg)))
    def create_vehicle(type, make, model, year):
        base_vehicle = {'type': type, 'make': make, 'model': model, 'year': year, 'mileage': 0, 'drive': lambda miles: (str((str((str('Drove ') + str(ml_string.toString(miles)))) + str(' miles. Total: '))) + str(ml_string.toString(_safe_attr_access(base_vehicle, 'mileage')))), 'get_description': lambda : (str((str((str((str(ml_string.toString(_safe_attr_access(base_vehicle, 'year'))) + str(' '))) + str(_safe_attr_access(base_vehicle, 'make')))) + str(' '))) + str(_safe_attr_access(base_vehicle, 'model')))}
        if (type == 'car'):
            base_vehicle['doors'] = 4
        elif (type == 'truck'):
            base_vehicle['bed_length'] = 6
        elif (type == 'motorcycle'):
            base_vehicle['engine_size'] = '600cc'
        return base_vehicle
    car = create_vehicle('car', 'Toyota', 'Camry', 2022)
    truck = create_vehicle('truck', 'Ford', 'F-150', 2023)
    bike = create_vehicle('motorcycle', 'Honda', 'CBR600RR', 2021)
    print('\\nVehicle Factory Pattern:')
    print((str('Car: ') + str(_safe_attr_access(car, 'get_description')())))
    print((str('Truck: ') + str(_safe_attr_access(truck, 'get_description')())))
    print((str('Bike: ') + str(_safe_attr_access(bike, 'get_description')())))
    drive_result = _safe_attr_access(car, 'drive')(150)
    print((str('Car driving: ') + str(drive_result)))
    def create_api_client(config):
        default_config = {'base_url': 'https://api.example.com', 'timeout': 5000, 'retry_count': 3, 'debug': False}
        merged_config = {'base_url': _safe_attr_access(config, 'base_url') if (_safe_attr_access(config, 'base_url') != None) else _safe_attr_access(default_config, 'base_url'), 'timeout': _safe_attr_access(config, 'timeout') if (_safe_attr_access(config, 'timeout') != None) else _safe_attr_access(default_config, 'timeout'), 'retry_count': _safe_attr_access(config, 'retry_count') if (_safe_attr_access(config, 'retry_count') != None) else _safe_attr_access(default_config, 'retry_count'), 'debug': _safe_attr_access(config, 'debug') if (_safe_attr_access(config, 'debug') != None) else _safe_attr_access(default_config, 'debug')}
        return {'config': merged_config, 'get': lambda endpoint: (str((str((str((str('GET ') + str((_safe_attr_access(merged_config, 'base_url') + endpoint)))) + str(' (timeout: '))) + str(ml_string.toString(_safe_attr_access(merged_config, 'timeout'))))) + str(')')), 'post': lambda endpoint, data: (str((str((str('POST ') + str((_safe_attr_access(merged_config, 'base_url') + endpoint)))) + str(' with data: '))) + str(data))}
    client1 = create_api_client({'base_url': 'https://myapi.com', 'debug': True, 'timeout': 8000, 'retry_count': 2})
    client2 = create_api_client({'base_url': 'https://api.production.com', 'timeout': 10000, 'retry_count': 5, 'debug': False})
    print('\\nAPI Client Pattern:')
    print((str('Client 1 base URL: ') + str(_safe_attr_access(_safe_attr_access(client1, 'config'), 'base_url'))))
    print((str('Client 2 timeout: ') + str(ml_string.toString(_safe_attr_access(_safe_attr_access(client2, 'config'), 'timeout')))))
    get_result = _safe_attr_access(client1, 'get')('/users')
    post_result = _safe_attr_access(client2, 'post')('/users', 'user_data')
    print((str('Client 1 GET: ') + str(get_result)))
    print((str('Client 2 POST: ') + str(post_result)))
    return {'people': [person1, person2], 'vehicles': [car, truck, bike], 'api_clients': [client1, client2]}

def object_serialization_transformation():
    print('\\n=== Object Serialization and Transformation ===')
    complex_object = {'id': 1234, 'user': {'name': 'Jane Doe', 'email': 'jane@example.com', 'preferences': {'theme': 'dark', 'language': 'en', 'notifications': True}}, 'projects': [{'name': 'Project Alpha', 'status': 'active', 'tasks': ['Design', 'Development', 'Testing']}, {'name': 'Project Beta', 'status': 'completed', 'tasks': ['Research', 'Implementation']}], 'metadata': {'created': '2024-01-15', 'last_modified': '2024-03-20', 'version': 2}}
    print((str('Complex object ID: ') + str(ml_string.toString(_safe_attr_access(complex_object, 'id')))))
    print((str((str((str((str('User: ') + str(_safe_attr_access(_safe_attr_access(complex_object, 'user'), 'name')))) + str(' ('))) + str(_safe_attr_access(_safe_attr_access(complex_object, 'user'), 'email')))) + str(')')))
    def flatten_object(obj, prefix):
        flattened = {}
        if (prefix == ''):
            flattened['id'] = _safe_attr_access(obj, 'id')
            flattened['user_name'] = _safe_attr_access(_safe_attr_access(obj, 'user'), 'name')
            flattened['user_email'] = _safe_attr_access(_safe_attr_access(obj, 'user'), 'email')
            flattened['user_theme'] = _safe_attr_access(_safe_attr_access(_safe_attr_access(obj, 'user'), 'preferences'), 'theme')
            flattened['project_count'] = _safe_attr_access(_safe_attr_access(obj, 'projects'), 'length')
            flattened['version'] = _safe_attr_access(_safe_attr_access(obj, 'metadata'), 'version')
        return flattened
    flattened = flatten_object(complex_object, '')
    print((str((str((str('Flattened - User: ') + str(_safe_attr_access(flattened, 'user_name')))) + str(', Theme: '))) + str(_safe_attr_access(flattened, 'user_theme'))))
    def filter_object_properties(obj, keep_properties):
        filtered = {}
        i = 0
        while (i < _safe_attr_access(keep_properties, 'length')):
            prop = keep_properties[i]
            if (prop == 'id'):
                filtered['id'] = _safe_attr_access(obj, 'id')
            elif (prop == 'user'):
                filtered['user'] = _safe_attr_access(obj, 'user')
            elif (prop == 'metadata'):
                filtered['metadata'] = _safe_attr_access(obj, 'metadata')
            i = (i + 1)
        return filtered
    filtered = filter_object_properties(complex_object, ['id', 'user'])
    print((str((str((str('Filtered object ID: ') + str(ml_string.toString(_safe_attr_access(filtered, 'id'))))) + str(', User: '))) + str(_safe_attr_access(_safe_attr_access(filtered, 'user'), 'name'))))
    def transform_user_data(user_obj):
        return {'user_id': _safe_attr_access(user_obj, 'id'), 'display_name': ml_string.upper(_safe_attr_access(_safe_attr_access(user_obj, 'user'), 'name')), 'contact_email': ml_string.lower(_safe_attr_access(_safe_attr_access(user_obj, 'user'), 'email')), 'settings': _safe_attr_access(_safe_attr_access(user_obj, 'user'), 'preferences'), 'project_count': _safe_attr_access(_safe_attr_access(user_obj, 'projects'), 'length'), 'last_update': _safe_attr_access(_safe_attr_access(user_obj, 'metadata'), 'last_modified')}
    transformed = transform_user_data(complex_object)
    print((str('Transformed - Display name: ') + str(_safe_attr_access(transformed, 'display_name'))))
    print((str('Contact email: ') + str(_safe_attr_access(transformed, 'contact_email'))))
    print((str('Project count: ') + str(ml_string.toString(_safe_attr_access(transformed, 'project_count')))))
    def validate_object_schema(obj, schema):
        validation_errors = []
        if _safe_attr_access(obj, 'id'):
            validation_errors = safe_append(validation_errors, 'Missing required field: id')
        if (_safe_attr_access(obj, 'user') or _safe_attr_access(_safe_attr_access(obj, 'user'), 'name')):
            validation_errors = safe_append(validation_errors, 'Missing required field: user.name')
        if (_safe_attr_access(obj, 'user') or _safe_attr_access(_safe_attr_access(obj, 'user'), 'email')):
            validation_errors = safe_append(validation_errors, 'Missing required field: user.email')
        return {'valid': (_safe_attr_access(validation_errors, 'length') == 0), 'errors': validation_errors, 'error_count': _safe_attr_access(validation_errors, 'length')}
    schema = {}
    validation_result = validate_object_schema(complex_object, schema)
    print((str((str((str((str('Validation result: ') + str(ml_string.toString(_safe_attr_access(validation_result, 'valid'))))) + str(' (errors: '))) + str(ml_string.toString(_safe_attr_access(validation_result, 'error_count'))))) + str(')')))
    return {'original': complex_object, 'flattened': flattened, 'filtered': filtered, 'transformed': transformed, 'validation': validation_result}

def object_performance_considerations():
    print('\\n=== Object Performance Considerations ===')
    def create_object_pool(factory_func, initial_size):
        pool = {'available': [], 'in_use': [], 'factory': factory_func, 'get_object': lambda : None, 'return_object': lambda obj: None}
        i = 0
        while (i < initial_size):
            initial_obj = factory_func()
            pool['available'] = safe_append(_safe_attr_access(pool, 'available'), initial_obj)
            i = (i + 1)
        return pool
    def create_work_item():
        work_item = {'id': 0, 'value': 0, 'active': False, 'process': lambda : (str('Processing work item ') + str(ml_string.toString(_safe_attr_access(work_item, 'id'))))}
        return work_item
    work_pool = create_object_pool(create_work_item, 3)
    print('Object pool created with 3 initial objects')
    print((str('Available objects: ') + str(ml_string.toString(_safe_attr_access(_safe_attr_access(work_pool, 'available'), 'length')))))
    item1 = _safe_attr_access(work_pool, 'get_object')()
    item2 = _safe_attr_access(work_pool, 'get_object')()
    item1['id'] = 101
    item1['active'] = True
    item2['id'] = 102
    item2['active'] = True
    print('After getting 2 objects:')
    print((str('Available: ') + str(ml_string.toString(_safe_attr_access(_safe_attr_access(work_pool, 'available'), 'length')))))
    print((str('In use: ') + str(ml_string.toString(_safe_attr_access(_safe_attr_access(work_pool, 'in_use'), 'length')))))
    _safe_attr_access(work_pool, 'return_object')(item1)
    print('After returning 1 object:')
    print((str('Available: ') + str(ml_string.toString(_safe_attr_access(_safe_attr_access(work_pool, 'available'), 'length')))))
    print((str('In use: ') + str(ml_string.toString(_safe_attr_access(_safe_attr_access(work_pool, 'in_use'), 'length')))))
    def create_immutable_point(x, y):
        point = {'x': x, 'y': y, 'move': lambda dx, dy: create_immutable_point((_safe_attr_access(point, 'x') + dx), (_safe_attr_access(point, 'y') + dy)), 'distance_to': lambda other_point: (((_safe_attr_access(other_point, 'x') - _safe_attr_access(point, 'x')) * (_safe_attr_access(other_point, 'x') - _safe_attr_access(point, 'x'))) + ((_safe_attr_access(other_point, 'y') - _safe_attr_access(point, 'y')) * (_safe_attr_access(other_point, 'y') - _safe_attr_access(point, 'y')))), 'to_string': lambda : (str((str((str((str('Point(') + str(ml_string.toString(_safe_attr_access(point, 'x'))))) + str(', '))) + str(ml_string.toString(_safe_attr_access(point, 'y'))))) + str(')'))}
        return point
    original_point = create_immutable_point(0, 0)
    moved_point = _safe_attr_access(original_point, 'move')(5, 3)
    twice_moved = _safe_attr_access(moved_point, 'move')(2, 1)
    print('\\nImmutable objects:')
    print((str('Original point: ') + str(_safe_attr_access(original_point, 'to_string')())))
    print((str('Moved point: ') + str(_safe_attr_access(moved_point, 'to_string')())))
    print((str('Twice moved: ') + str(_safe_attr_access(twice_moved, 'to_string')())))
    distance = _safe_attr_access(original_point, 'distance_to')(moved_point)
    print((str('Distance between original and moved: ') + str(ml_string.toString(distance))))
    return {'object_pool': work_pool, 'immutable_demo': {'original': original_point, 'moved': moved_point, 'twice_moved': twice_moved, 'distance': distance}}

def main():
    print('========================================')
    print('  COMPREHENSIVE OBJECT OPERATIONS TEST')
    print('========================================')
    results = {'creation': None, 'access': None, 'composition': None, 'utilities': None, 'oop_patterns': None, 'serialization': None, 'performance': None}
    results['creation'] = object_creation_basics()
    results['access'] = object_property_access()
    results['composition'] = object_composition_relationships()
    results['utilities'] = object_manipulation_utilities()
    results['oop_patterns'] = object_oriented_patterns()
    results['serialization'] = object_serialization_transformation()
    results['performance'] = object_performance_considerations()
    print('\\n========================================')
    print('  ALL OBJECT TESTS COMPLETED')
    print('========================================')
    return results

main()

# End of generated code