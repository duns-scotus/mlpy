"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

number_int = 42

number_float = 3.14159

number_scientific = 1500000.0

number_negative = 273.15

string_double = 'Hello, World!'

string_single = 'Single quotes work too'

string_escape = 'Line 1\\nLine 2\\tTabbed'

string_empty = ''

boolean_true = True

boolean_false = False

empty_array = []

number_array = [1, 2, 3, 4, 5]

string_array = ['apple', 'banana', 'cherry', 'date']

mixed_array = [1, 'two', True, 4.0, False]

nested_array = [[1, 2], [3, 4], [5, 6]]

empty_object = {}

person = {'name': 'Alice Johnson', 'age': 30, 'active': True, 'salary': 75000.0, 'skills': ['JavaScript', 'Python', 'ML']}

complex_object = {'id': 1001, 'metadata': {'created': '2024-01-01', 'updated': '2024-03-15', 'version': 1.2}, 'settings': {'theme': 'dark', 'notifications': True, 'preferences': {'language': 'en', 'timezone': 'UTC'}}}

def arithmetic_operations():
    a = 20
    b = 8
    addition = (a + b)
    subtraction = (a - b)
    multiplication = (a * b)
    division = (a / b)
    modulo = (a % b)
    print('Arithmetic Results:')
    print((str('Addition: ') + str(addition)))
    print((str('Subtraction: ') + str(subtraction)))
    print((str('Multiplication: ') + str(multiplication)))
    print((str('Division: ') + str(division)))
    print((str('Modulo: ') + str(modulo)))
    negative = a
    positive = b
    print((str('Negative: ') + str(negative)))
    print((str('Positive: ') + str(positive)))
    return {'add': addition, 'sub': subtraction, 'mul': multiplication, 'div': division, 'mod': modulo}

def comparison_operations():
    x = 10
    y = 20
    z = 10
    equal = (x == z)
    not_equal = (x != y)
    less_than = (x < y)
    greater_than = (y > x)
    less_equal = (x <= z)
    greater_equal = (y >= x)
    print('Comparison Results:')
    print((str('Equal (10 == 10): ') + str(equal)))
    print((str('Not Equal (10 != 20): ') + str(not_equal)))
    print((str('Less Than (10 < 20): ') + str(less_than)))
    print((str('Greater Than (20 > 10): ') + str(greater_than)))
    print((str('Less or Equal (10 <= 10): ') + str(less_equal)))
    print((str('Greater or Equal (20 >= 10): ') + str(greater_equal)))
    return {'eq': equal, 'ne': not_equal, 'lt': less_than, 'gt': greater_than, 'le': less_equal, 'ge': greater_equal}

def logical_operations():
    p = True
    q = False
    r = True
    and_result = (p and q)
    or_result = (p or q)
    not_result = p
    complex_and = ((p and r) and q)
    complex_or = ((p or q) and r)
    print('Logical Operations:')
    print((str('AND (true && false): ') + str(and_result)))
    print((str('OR (true || false): ') + str(or_result)))
    print((str('NOT (!true): ') + str(not_result)))
    print((str('Complex AND: ') + str(complex_and)))
    print((str('Complex OR: ') + str(complex_or)))
    return {'and': and_result, 'or': or_result, 'not': not_result, 'complex_and': complex_and, 'complex_or': complex_or}

def ternary_operations():
    age = 25
    is_adult = 'adult' if (age >= 18) else 'minor'
    score = 85
    grade = 'A' if (score >= 90) else 'B' if (score >= 80) else 'C' if (score >= 70) else 'D' if (score >= 60) else 'F'
    weather = 'sunny'
    activity = 'go to beach' if (weather == 'sunny') else 'stay inside' if (weather == 'rainy') else 'go for a walk'
    print('Ternary Results:')
    print((str('Age status: ') + str(is_adult)))
    print((str('Grade: ') + str(grade)))
    print((str('Activity: ') + str(activity)))
    return {'status': is_adult, 'grade': grade, 'activity': activity}

def variable_scoping():
    global_var = "I'm global"
    def inner_function():
        local_var = "I'm local"
        modified_global = (str(global_var) + str(' (modified in function)'))
        return local_var
    function_result = inner_function()
    print('Scoping Test:')
    print((str('Global variable: ') + str(global_var)))
    print((str('Function result: ') + str(function_result)))
    return {'global': global_var, 'local': function_result}

def access_patterns():
    numbers = [10, 20, 30, 40, 50]
    employee = {'name': 'Bob Smith', 'department': 'Engineering', 'skills': ['Java', 'Python', 'Go']}
    first_number = numbers[0]
    last_number = numbers[4]
    emp_name = employee['name']
    emp_dept = employee['department']
    first_skill = employee['skills'][0]
    print('Access Patterns:')
    print((str('First number: ') + str(first_number)))
    print((str('Last number: ') + str(last_number)))
    print((str('Employee name: ') + str(emp_name)))
    print((str('Employee department: ') + str(emp_dept)))
    print((str('First skill: ') + str(first_skill)))
    numbers[2] = 999
    employee['department'] = 'DevOps'
    print('After modifications:')
    print((str('Modified number: ') + str(numbers[2])))
    print((str('Modified department: ') + str(employee['department'])))
    return {'numbers': numbers, 'employee': employee}

def higher_order_functions():
    multiply = lambda a, b: (a * b)
    def apply_operation(x, y, operation):
        return operation(x, y)
    result1 = apply_operation(5, 3, multiply)
    def create_adder(n):
        return lambda x: (x + n)
    add_ten = create_adder(10)
    result2 = add_ten(5)
    print('Higher-order functions:')
    print((str('Apply operation result: ') + str(result1)))
    print((str('Created adder result: ') + str(result2)))
    return {'multiply_result': result1, 'adder_result': result2}

def complex_expressions():
    x = 5
    y = 10
    z = 15
    complex1 = (((x + y) * z) - (x * y))
    complex2 = ((x * (y + z)) / (x + 1))
    complex3 = (x + z) if (x > y) else (y + z)
    complex4 = (((x < y) and (y < z)) or (x == 5))
    complex5 = ((x > y) and (z > y))
    complex6 = 'high' if ((x + y) > 10) else 'low'
    complex7 = (((x * 2) + (y / 2)) - (z % 4))
    print('Complex Expressions:')
    print((str('Complex arithmetic 1: ') + str(complex1)))
    print((str('Complex arithmetic 2: ') + str(complex2)))
    print((str('Complex conditional: ') + str(complex3)))
    print((str('Complex logical 1: ') + str(complex4)))
    print((str('Complex logical 2: ') + str(complex5)))
    print((str('Mixed conditional: ') + str(complex6)))
    print((str('Mixed arithmetic: ') + str(complex7)))
    return {'c1': complex1, 'c2': complex2, 'c3': complex3, 'c4': complex4, 'c5': complex5, 'c6': complex6, 'c7': complex7}

def main():
    print('=== ML Language Fundamentals Test ===')
    print('')
    print('Testing arithmetic operations:')
    arith_results = arithmetic_operations()
    print('')
    print('Testing comparison operations:')
    comp_results = comparison_operations()
    print('')
    print('Testing logical operations:')
    logic_results = logical_operations()
    print('')
    print('Testing ternary operations:')
    ternary_results = ternary_operations()
    print('')
    print('Testing variable scoping:')
    scope_results = variable_scoping()
    print('')
    print('Testing access patterns:')
    access_results = access_patterns()
    print('')
    print('Testing higher-order functions:')
    hof_results = higher_order_functions()
    print('')
    print('Testing complex expressions:')
    complex_results = complex_expressions()
    print('')
    print('=== All Fundamental Tests Complete ===')
    return {'arithmetic': arith_results, 'comparisons': comp_results, 'logical': logic_results, 'ternary': ternary_results, 'scoping': scope_results, 'access': access_results, 'functions': hof_results, 'complex': complex_results}

main()

# End of generated code