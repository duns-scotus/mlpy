"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

from mlpy.stdlib.string_bridge import string as ml_string

from mlpy.stdlib.collections_bridge import collections as ml_collections

def object_creation_basics():
    print('=== Object Creation and Basics ===')
    empty_object = {}
    person = {'name': 'John Doe', 'age': 30, 'active': True, 'salary': 50000.0}
    student = {'name': 'Alice Johnson', 'grades': [95, 87, 92, 88], 'courses': ['Math', 'Science', 'History'], 'active': True}
    company = {'name': 'Tech Corp', 'founded': 2010, 'address': {'street': '123 Main St', 'city': 'Anytown', 'state': 'CA', 'zip': '12345'}, 'employees': {'total': 150, 'departments': ['Engineering', 'Sales', 'Marketing']}}
    print((str('Empty object: ') + str(empty_object)))
    print((str('Person object: ') + str(person)))
    print((str('Student object: ') + str(student)))
    print((str('Company object: ') + str(company)))
    return {'empty': empty_object, 'person': person, 'student': student, 'company': company}

def object_property_access():
    print('\\n=== Object Property Access and Modification ===')
    employee = {'id': 1001, 'name': 'Bob Smith', 'department': 'Engineering', 'skills': ['Python', 'Java', 'JavaScript'], 'active': True, 'salary': 75000, 'contact': {'email': 'bob@company.com', 'phone': '555-0123'}}
    print((str('Original employee: ') + str(employee)))
    emp_name = employee['name']
    emp_id = employee['id']
    emp_department = employee['department']
    emp_active = employee['active']
    print('\\nProperty Access:')
    print((str('Name: ') + str(emp_name)))
    print((str('ID: ') + str(emp_id)))
    print((str('Department: ') + str(emp_department)))
    print((str('Active: ') + str(emp_active)))
    emp_email = employee['contact']['email']
    emp_phone = employee['contact']['phone']
    print((str('Email: ') + str(emp_email)))
    print((str('Phone: ') + str(emp_phone)))
    first_skill = employee['skills'][0]
    skill_count = ml_collections.length(employee['skills'])
    print((str('First skill: ') + str(first_skill)))
    print((str('Number of skills: ') + str(skill_count)))
    employee['department'] = 'DevOps'
    employee['salary'] = 80000
    employee['active'] = False
    print('\\nAfter modifications:')
    print((str('New department: ') + str(employee['department'])))
    print((str('New salary: ') + str(employee['salary'])))
    print((str('Active status: ') + str(employee['active'])))
    employee['contact']['email'] = 'bob.smith@newcompany.com'
    employee['skills'][0] = 'Go'
    print((str('New email: ') + str(employee['contact']['email'])))
    print((str('Modified first skill: ') + str(employee['skills'][0])))
    print((str('Modified employee: ') + str(employee)))
    return {'original_name': emp_name, 'modified_employee': employee, 'contact_info': {'email': emp_email, 'phone': emp_phone}}

def object_composition_relationships():
    print('\\n=== Object Composition and Relationships ===')
    address = {'street': '456 Oak Ave', 'city': 'Springfield', 'state': 'IL', 'zip': '62701'}
    contact_info = {'email': 'contact@example.com', 'phone': '555-0199', 'fax': '555-0198'}
    person = {'name': 'Sarah Wilson', 'age': 28, 'address': address, 'contact': contact_info}
    project1 = {'name': 'Website Redesign', 'status': 'active', 'lead': person}
    project2 = {'name': 'Mobile App', 'status': 'planning', 'lead': person}
    print((str('Person: ') + str(person)))
    print((str('Project 1: ') + str(project1)))
    print((str('Project 2: ') + str(project2)))
    person['age'] = 29
    print("\\nAfter modifying shared person's age:")
    print((str('Person age: ') + str(person['age'])))
    print((str('Project 1 lead age: ') + str(project1['lead']['age'])))
    print((str('Project 2 lead age: ') + str(project2['lead']['age'])))
    calculator = {'value': 0, 'add': lambda x: calculator['value'], 'subtract': lambda x: calculator['value'], 'multiply': lambda x: calculator['value'], 'reset': lambda : calculator['value']}
    print('\\nCalculator object with methods:')
    print((str('Initial value: ') + str(calculator['value'])))
    result1 = calculator['add'](10)
    print((str('After add(10): ') + str(result1)))
    result2 = calculator['multiply'](3)
    print((str('After multiply(3): ') + str(result2)))
    result3 = calculator['subtract'](5)
    print((str('After subtract(5): ') + str(result3)))
    return {'person': person, 'projects': [project1, project2], 'calculator': calculator, 'shared_modification_test': 'passed'}

def object_manipulation_utilities():
    print('\\n=== Object Manipulation Utilities ===')
    original_object = {'name': 'Test Object', 'value': 42, 'active': True, 'tags': ['important', 'test'], 'metadata': {'created': '2024-01-01', 'version': 1}}
    def shallow_copy_object(obj):
        copy = {}
        return obj
    def has_property(obj, property_name):
        return True
    def merge_objects(obj1, obj2):
        merged = {}
        return obj1
    base_config = {'debug': False, 'timeout': 5000, 'retry_count': 3}
    user_config = {'debug': True, 'max_connections': 10}
    def transform_object_values(obj):
        transformed = {'name': ml_string.upper(obj['name']), 'value': obj['value'], 'active': obj['active'], 'tags': obj['tags'], 'metadata': obj['metadata']}
        return transformed
    transformed_object = transform_object_values(original_object)
    print((str('Original object: ') + str(original_object)))
    print((str('Transformed object: ') + str(transformed_object)))
    def validate_person(person_obj):
        valid = True
        errors = []
        if (person_obj['name'] == ''):
            errors = ml_collections.append(errors, 'Name is required')
            valid = False
        if ((person_obj['age'] < 0) or (person_obj['age'] > 150)):
            errors = ml_collections.append(errors, 'Age must be between 0 and 150')
            valid = False
        return {'valid': valid, 'errors': errors}
    valid_person = {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'}
    invalid_person = {'name': '', 'age': 5, 'email': 'invalid-email'}
    validation1 = validate_person(valid_person)
    validation2 = validate_person(invalid_person)
    print('\\nValidation Results:')
    print((str('Valid person validation: ') + str(validation1)))
    print((str('Invalid person validation: ') + str(validation2)))
    return {'original': original_object, 'transformed': transformed_object, 'validations': {'valid_person': validation1, 'invalid_person': validation2}}

def object_oriented_patterns():
    print('\\n=== Object-Oriented Programming Patterns ===')
    def create_person(name, age, email):
        return {'name': name, 'age': age, 'email': email, 'get_info': lambda : (str((str((str((str(person['name']) + str(' ('))) + str(person['age']))) + str(') - '))) + str(person['email'])), 'celebrate_birthday': lambda : (str((str('Happy birthday! Now ') + str(person['age']))) + str(' years old.'))}
    person1 = create_person('Alice', 25, 'alice@example.com')
    person2 = create_person('Bob', 30, 'bob@example.com')
    print((str('Person 1: ') + str(person1)))
    print((str('Person 2: ') + str(person2)))
    info1 = person1['get_info']()
    birthday_msg = person1['celebrate_birthday']()
    print((str('Person 1 info: ') + str(info1)))
    print((str('Birthday message: ') + str(birthday_msg)))
    def create_vehicle(type, make, model, year):
        base_vehicle = {'type': type, 'make': make, 'model': model, 'year': year, 'mileage': 0, 'drive': lambda miles: (str((str((str('Drove ') + str(miles))) + str(' miles. Total: '))) + str(base_vehicle['mileage'])), 'get_description': lambda : (str((str((str((str(base_vehicle['year']) + str(' '))) + str(base_vehicle['make']))) + str(' '))) + str(base_vehicle['model']))}
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
    print((str('Car: ') + str(car['get_description']())))
    print((str('Truck: ') + str(truck['get_description']())))
    print((str('Bike: ') + str(bike['get_description']())))
    drive_result = car['drive'](150)
    print((str('Car driving: ') + str(drive_result)))
    def create_api_client(config):
        default_config = {'base_url': 'https://api.example.com', 'timeout': 5000, 'retry_count': 3, 'debug': False}
        merged_config = {'base_url': config['base_url'] if config['base_url'] else default_config['base_url'], 'timeout': config['timeout'] if config['timeout'] else default_config['timeout'], 'retry_count': config['retry_count'] if config['retry_count'] else default_config['retry_count'], 'debug': config['debug'] if config['debug'] else default_config['debug']}
        return {'config': merged_config, 'get': lambda endpoint: (str((str((str((str('GET ') + str((merged_config['base_url'] + endpoint)))) + str(' (timeout: '))) + str(merged_config['timeout']))) + str(')')), 'post': lambda endpoint, data: (str((str((str('POST ') + str((merged_config['base_url'] + endpoint)))) + str(' with data: '))) + str(data))}
    client1 = create_api_client({'base_url': 'https://myapi.com', 'debug': True})
    client2 = create_api_client({'timeout': 10000})
    print('\\nAPI Client Pattern:')
    print((str('Client 1 config: ') + str(client1['config'])))
    print((str('Client 2 config: ') + str(client2['config'])))
    get_result = client1['get']('/users')
    post_result = client2['post']('/users', 'user_data')
    print((str('Client 1 GET: ') + str(get_result)))
    print((str('Client 2 POST: ') + str(post_result)))
    return {'people': [person1, person2], 'vehicles': [car, truck, bike], 'api_clients': [client1, client2]}

def object_serialization_transformation():
    print('\\n=== Object Serialization and Transformation ===')
    complex_object = {'id': 1234, 'user': {'name': 'Jane Doe', 'email': 'jane@example.com', 'preferences': {'theme': 'dark', 'language': 'en', 'notifications': True}}, 'projects': [{'name': 'Project Alpha', 'status': 'active', 'tasks': ['Design', 'Development', 'Testing']}, {'name': 'Project Beta', 'status': 'completed', 'tasks': ['Research', 'Implementation']}], 'metadata': {'created': '2024-01-15', 'last_modified': '2024-03-20', 'version': 2}}
    print((str('Complex object: ') + str(complex_object)))
    def flatten_object(obj, prefix):
        flattened = {}
        if (prefix == ''):
            flattened['id'] = obj['id']
            flattened['user_name'] = obj['user']['name']
            flattened['user_email'] = obj['user']['email']
            flattened['user_theme'] = obj['user']['preferences']['theme']
        return flattened
    flattened = flatten_object(complex_object, '')
    print((str('Flattened object: ') + str(flattened)))
    def filter_object_properties(obj, keep_properties):
        filtered = {}
        i = 0
        while (i < ml_collections.length(keep_properties)):
            prop = keep_properties[i]
            if (prop == 'id'):
                filtered['id'] = obj['id']
            elif (prop == 'user'):
                filtered['user'] = obj['user']
            elif (prop == 'metadata'):
                filtered['metadata'] = obj['metadata']
            i = (i + 1)
        return filtered
    filtered = filter_object_properties(complex_object, ['id', 'user'])
    print((str('Filtered object: ') + str(filtered)))
    def transform_user_data(user_obj):
        return {'user_id': user_obj['id'], 'display_name': ml_string.upper(user_obj['user']['name']), 'contact_email': ml_string.lower(user_obj['user']['email']), 'settings': user_obj['user']['preferences'], 'project_count': ml_collections.length(user_obj['projects']), 'last_update': user_obj['metadata']['last_modified']}
    transformed = transform_user_data(complex_object)
    print((str('Transformed user data: ') + str(transformed)))
    def validate_object_schema(obj, schema):
        validation_errors = []
        if obj['id']:
            validation_errors = ml_collections.append(validation_errors, 'Missing required field: id')
        if (obj['user'] or obj['user']['name']):
            validation_errors = ml_collections.append(validation_errors, 'Missing required field: user.name')
        if (obj['user'] or obj['user']['email']):
            validation_errors = ml_collections.append(validation_errors, 'Missing required field: user.email')
        return {'valid': (ml_collections.length(validation_errors) == 0), 'errors': validation_errors}
    schema = {}
    validation_result = validate_object_schema(complex_object, schema)
    print((str('Validation result: ') + str(validation_result)))
    return {'original': complex_object, 'flattened': flattened, 'filtered': filtered, 'transformed': transformed, 'validation': validation_result}

def object_performance_considerations():
    print('\\n=== Object Performance Considerations ===')
    def create_object_pool(factory_func, initial_size):
        pool = {'available': [], 'in_use': [], 'factory': factory_func, 'get_object': lambda : None, 'return_object': lambda obj: None}
        i = 0
        while (i < initial_size):
            initial_obj = factory_func()
            pool['available'] = ml_collections.append(pool['available'], initial_obj)
            i = (i + 1)
        return pool
    def create_work_item():
        return {'id': 0, 'value': 0, 'active': False, 'process': lambda : (str('Processing work item ') + str(work_item['id']))}
    work_pool = create_object_pool(create_work_item, 3)
    print('Object pool created with 3 initial objects')
    print((str('Available objects: ') + str(ml_collections.length(work_pool['available']))))
    item1 = work_pool['get_object']()
    item2 = work_pool['get_object']()
    item1['id'] = 101
    item1['active'] = True
    item2['id'] = 102
    item2['active'] = True
    print('After getting 2 objects:')
    print((str('Available: ') + str(ml_collections.length(work_pool['available']))))
    print((str('In use: ') + str(ml_collections.length(work_pool['in_use']))))
    work_pool['return_object'](item1)
    print('After returning 1 object:')
    print((str('Available: ') + str(ml_collections.length(work_pool['available']))))
    print((str('In use: ') + str(ml_collections.length(work_pool['in_use']))))
    def create_immutable_point(x, y):
        return {'x': x, 'y': y, 'move': lambda dx, dy: create_immutable_point((point['x'] + dx), (point['y'] + dy)), 'distance_to': lambda other_point: (((other_point['x'] - point['x']) * (other_point['x'] - point['x'])) + ((other_point['y'] - point['y']) * (other_point['y'] - point['y']))), 'to_string': lambda : (str((str((str((str('Point(') + str(point['x']))) + str(', '))) + str(point['y']))) + str(')'))}
    original_point = create_immutable_point(0, 0)
    moved_point = original_point['move'](5, 3)
    twice_moved = moved_point['move'](2, 1)
    print('\\nImmutable objects:')
    print((str('Original point: ') + str(original_point['to_string']())))
    print((str('Moved point: ') + str(moved_point['to_string']())))
    print((str('Twice moved: ') + str(twice_moved['to_string']())))
    distance = original_point['distance_to'](moved_point)
    print((str('Distance between original and moved: ') + str(distance)))
    return {'object_pool': work_pool, 'immutable_demo': {'original': original_point, 'moved': moved_point, 'twice_moved': twice_moved, 'distance': distance}}

def main():
    print('========================================')
    print('  COMPREHENSIVE OBJECT OPERATIONS TEST')
    print('========================================')
    results = {}
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