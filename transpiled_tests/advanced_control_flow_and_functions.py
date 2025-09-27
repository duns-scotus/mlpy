"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

from mlpy.stdlib.string_bridge import string as ml_string

from mlpy.stdlib.collections_bridge import collections as ml_collections

from mlpy.stdlib.math_bridge import math as ml_math

def basic_control_flow():
    print('=== Basic Control Flow Structures ===')
    age = 25
    if (age >= 18):
        print('You are an adult')
    temperature = 72
    if (temperature > 80):
        print("It's hot outside")
    else:
        print("It's comfortable outside")
    score = 85
    if (score >= 90):
        grade = 'A'
    elif (score >= 80):
        grade = 'B'
    elif (score >= 70):
        grade = 'C'
    elif (score >= 60):
        grade = 'D'
    else:
        grade = 'F'
    print((str((str((str('Grade for score ') + str(score))) + str(': '))) + str(grade)))
    weather = 'sunny'
    temperature = 75
    if (weather == 'sunny'):
        if (temperature > 70):
            activity = 'go to the beach'
        else:
            activity = 'take a walk'
    else:
        if (temperature > 60):
            activity = 'stay inside and read'
        else:
            activity = 'stay warm inside'
    print((str((str((str((str((str('Weather: ') + str(weather))) + str(', Temperature: '))) + str(temperature))) + str(' -> '))) + str(activity)))
    return {'age_check': (age >= 18), 'temperature_check': temperature, 'grade': grade, 'activity': activity}

def loop_constructs_patterns():
    print('\\n=== Loop Constructs and Patterns ===')
    print('While loop counting to 5:')
    count = 1
    while (count <= 5):
        print((str('Count: ') + str(count)))
        count = (count + 1)
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sum = 0
    i = 0
    while (i < ml_collections.length(numbers)):
        sum = (sum + numbers[i])
        i = (i + 1)
    print((str('Sum of numbers 1-10: ') + str(sum)))
    print('\\nFor-in loop with fruits:')
    fruits = ['apple', 'banana', 'cherry', 'date']
    for ml_unknown_identifier_2786171882000 in fruits:
        print((str('Fruit: ') + str(fruit)))
    print('\\nFor-in loop processing characters:')
    chars = ml_string.to_chars('Hello')
    word = ''
    for ml_unknown_identifier_2786171888336 in chars:
        word = (word + ml_string.upper(char))
    print((str('Uppercase word: ') + str(word)))
    print('\\nNested loops - 3x3 multiplication table:')
    i = 1
    while (i <= 3):
        row = ''
        j = 1
        while (j <= 3):
            product = (i * j)
            row = (str((row + product)) + str(' '))
            j = (j + 1)
        print((str((str((str('Row ') + str(i))) + str(': '))) + str(row)))
        i = (i + 1)
    print('\\nLoop with conditional processing:')
    test_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    even_sum = 0
    odd_count = 0
    k = 0
    while (k < ml_collections.length(test_numbers)):
        number = test_numbers[k]
        if ((number % 2) == 0):
            even_sum = (even_sum + number)
            print((str('Even number found: ') + str(number)))
        else:
            odd_count = (odd_count + 1)
            print((str('Odd number found: ') + str(number)))
        k = (k + 1)
    print((str('Even sum: ') + str(even_sum)))
    print((str('Odd count: ') + str(odd_count)))
    return {'sum_1_to_10': sum, 'even_sum': even_sum, 'odd_count': odd_count, 'uppercase_word': word}

def function_definition_patterns():
    print('\\n=== Function Definition Patterns ===')
    def greet(name, greeting):
        return (str((str((str(greeting) + str(', '))) + str(name))) + str('!'))
    message1 = greet('Alice', 'Hello')
    message2 = greet('Bob', 'Good morning')
    print((str('Greeting 1: ') + str(message1)))
    print((str('Greeting 2: ') + str(message2)))
    def calculate_area(length, width):
        if (width == 0):
            return (length * length)
        else:
            return (length * width)
    square_area = calculate_area(5, 0)
    rectangle_area = calculate_area(4, 6)
    print((str('Square area (5x5): ') + str(square_area)))
    print((str('Rectangle area (4x6): ') + str(rectangle_area)))
    def classify_number(n):
        if (n < 0):
            return 'negative'
        if (n == 0):
            return 'zero'
        if ((n > 0) and (n <= 100)):
            return 'small positive'
        return 'large positive'
    class1 = classify_number(5)
    class2 = classify_number(0)
    class3 = classify_number(50)
    class4 = classify_number(200)
    print('Number classifications:')
    print((str('-5: ') + str(class1)))
    print((str('0: ') + str(class2)))
    print((str('50: ') + str(class3)))
    print((str('200: ') + str(class4)))
    def find_prime_factors(n):
        factors = []
        divisor = 2
        while ((divisor * divisor) <= n):
            while ((n % divisor) == 0):
                factors = ml_collections.append(factors, divisor)
                n = (n / divisor)
            divisor = (divisor + 1)
        if (n > 1):
            factors = ml_collections.append(factors, n)
        return factors
    factors_12 = find_prime_factors(12)
    factors_17 = find_prime_factors(17)
    factors_24 = find_prime_factors(24)
    print('\\nPrime factorization:')
    print((str('12: ') + str(factors_12)))
    print((str('17: ') + str(factors_17)))
    print((str('24: ') + str(factors_24)))
    return {'greetings': [message1, message2], 'areas': {'square': square_area, 'rectangle': rectangle_area}, 'classifications': [class1, class2, class3, class4], 'prime_factors': {'twelve': factors_12, 'seventeen': factors_17, 'twenty_four': factors_24}}

def higher_order_functions():
    print('\\n=== Higher-Order Functions and Function Expressions ===')
    add = lambda a, b: (a + b)
    multiply = lambda a, b: (a * b)
    subtract = lambda a, b: (a - b)
    divide = lambda a, b: None
    def apply_binary_operation(x, y, operation):
        return operation(x, y)
    result1 = apply_binary_operation(10, 5, add)
    result2 = apply_binary_operation(10, 5, multiply)
    result3 = apply_binary_operation(10, 5, subtract)
    result4 = apply_binary_operation(10, 5, divide)
    print('Binary operations on 10 and 5:')
    print((str('Add: ') + str(result1)))
    print((str('Multiply: ') + str(result2)))
    print((str('Subtract: ') + str(result3)))
    print((str('Divide: ') + str(result4)))
    def create_multiplier(factor):
        return lambda x: (x * factor)
    double = create_multiplier(2)
    triple = create_multiplier(3)
    times_ten = create_multiplier(10)
    doubled = double(7)
    tripled = triple(4)
    times_ten_result = times_ten(6)
    print('\\nFunction factory results:')
    print((str('Double 7: ') + str(doubled)))
    print((str('Triple 4: ') + str(tripled)))
    print((str('Times 10 of 6: ') + str(times_ten_result)))
    def transform_array(arr, transformer):
        result = []
        i = 0
        while (i < ml_collections.length(arr)):
            element = arr[i]
            transformed = transformer(element)
            result = ml_collections.append(result, transformed)
            i = (i + 1)
        return result
    def square(x):
        return (x * x)
    def cube(x):
        return ((x * x) * x)
    numbers = [1, 2, 3, 4, 5]
    squared_numbers = transform_array(numbers, square)
    cubed_numbers = transform_array(numbers, cube)
    doubled_numbers = transform_array(numbers, double)
    print('\\nArray transformations:')
    print((str('Original: ') + str(numbers)))
    print((str('Squared: ') + str(squared_numbers)))
    print((str('Cubed: ') + str(cubed_numbers)))
    print((str('Doubled: ') + str(doubled_numbers)))
    def compose_functions(f, g):
        return lambda x: f(g(x))
    def add_one(x):
        return (x + 1)
    def multiply_by_two(x):
        return (x * 2)
    composed = compose_functions(add_one, multiply_by_two)
    composition_result = composed(5)
    print('\\nFunction composition:')
    print((str('Composed function on 5: ') + str(composition_result)))
    return {'binary_ops': [result1, result2, result3, result4], 'factory_results': [doubled, tripled, times_ten_result], 'transformations': {'squared': squared_numbers, 'cubed': cubed_numbers, 'doubled': doubled_numbers}, 'composition_result': composition_result}

def recursive_functions_algorithms():
    print('\\n=== Recursive Functions and Algorithms ===')
    def factorial(n):
        if (n <= 1):
            return 1
        else:
            return (n * factorial((n - 1)))
    fact_5 = factorial(5)
    fact_7 = factorial(7)
    fact_0 = factorial(0)
    print('Factorial calculations:')
    print((str('5! = ') + str(fact_5)))
    print((str('7! = ') + str(fact_7)))
    print((str('0! = ') + str(fact_0)))
    def fibonacci(n):
        if (n <= 1):
            return n
        else:
            return (fibonacci((n - 1)) + fibonacci((n - 2)))
    fib_sequence = []
    i = 0
    while (i < 10):
        fib_value = fibonacci(i)
        fib_sequence = ml_collections.append(fib_sequence, fib_value)
        i = (i + 1)
    print((str('Fibonacci sequence (first 10): ') + str(fib_sequence)))
    def recursive_sum(arr, index):
        if (index >= ml_collections.length(arr)):
            return 0
        else:
            return (arr[index] + recursive_sum(arr, (index + 1)))
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    recursive_total = recursive_sum(numbers, 0)
    print((str('Recursive sum of 1-10: ') + str(recursive_total)))
    def reverse_string_recursive(str, index):
        if (index >= ml_string.length(str)):
            return ''
        else:
            char = ml_string.char_at(str, index)
            return (reverse_string_recursive(str, (index + 1)) + char)
    original_string = 'Hello World'
    reversed_string = reverse_string_recursive(original_string, 0)
    print('String reversal:')
    print((str('Original: ') + str(original_string)))
    print((str('Reversed: ') + str(reversed_string)))
    def count_nodes(node):
        if (node == None):
            return 0
        left_count = 0
        right_count = 0
        if (node['left'] != None):
            left_count = count_nodes(node['left'])
        if (node['right'] != None):
            right_count = count_nodes(node['right'])
        return ((1 + left_count) + right_count)
    tree = {'value': 1, 'left': {'value': 2, 'left': {'value': 4, 'left': None, 'right': None}, 'right': {'value': 5, 'left': None, 'right': None}}, 'right': {'value': 3, 'left': None, 'right': {'value': 6, 'left': None, 'right': None}}}
    node_count = count_nodes(tree)
    print((str('Binary tree node count: ') + str(node_count)))
    return {'factorials': [fact_5, fact_7, fact_0], 'fibonacci': fib_sequence, 'recursive_sum': recursive_total, 'string_reversal': {'original': original_string, 'reversed': reversed_string}, 'tree_node_count': node_count}

def exception_handling_error_management():
    print('\\n=== Exception Handling and Error Management ===')
    def safe_divide(a, b):
        try:
            if (b == 0):
                return {'success': False, 'error': 'Division by zero', 'value': None}
            result = (a / b)
            return {'success': True, 'error': None, 'value': result}
        except error:
            return {'success': False, 'error': 'Unknown error occurred', 'value': None}
    result1 = safe_divide(10, 2)
    result2 = safe_divide(10, 0)
    result3 = safe_divide(15, 3)
    print('Safe division results:')
    print((str('10 / 2: ') + str(result1)))
    print((str('10 / 0: ') + str(result2)))
    print((str('15 / 3: ') + str(result3)))
    def validate_and_process(input):
        errors = []
        try:
            if ((input['name'] == '') or (input['name'] == None)):
                errors = ml_collections.append(errors, 'Name is required')
            if ((input['age'] < 0) or (input['age'] > 150)):
                errors = ml_collections.append(errors, 'Age must be between 0 and 150')
            if (ml_collections.length(errors) > 0):
                return {'success': False, 'errors': errors, 'data': None}
            processed_data = {'name': ml_string.upper(input['name']), 'age': input['age'], 'age_group': 'minor' if (input['age'] < 18) else 'adult', 'valid': True}
            return {'success': True, 'errors': [], 'data': processed_data}
        except error:
            return {'success': False, 'errors': ['Processing error occurred'], 'data': None}
    valid_input = {'name': 'John Doe', 'age': 30}
    invalid_input = {'name': '', 'age': 5}
    validation1 = validate_and_process(valid_input)
    validation2 = validate_and_process(invalid_input)
    print('Validation results:')
    print((str('Valid input result: ') + str(validation1)))
    print((str('Invalid input result: ') + str(validation2)))
    def chain_operations(start_value):
        def step1(value):
            if (value < 0):
                return {'success': False, 'error': 'Value cannot be negative', 'value': None}
            return {'success': True, 'error': None, 'value': (value * 2)}
        def step2(value):
            if (value > 100):
                return {'success': False, 'error': 'Value too large', 'value': None}
            return {'success': True, 'error': None, 'value': (value + 10)}
        def step3(value):
            if ((value % 2) != 0):
                return {'success': False, 'error': 'Value must be even', 'value': None}
            return {'success': True, 'error': None, 'value': (value / 2)}
        result1 = step1(start_value)
        if result1['success']:
            return result1
        result2 = step2(result1['value'])
        if result2['success']:
            return result2
        result3 = step3(result2['value'])
        return result3
    chain_result1 = chain_operations(5)
    chain_result2 = chain_operations(50)
    chain_result3 = chain_operations(1)
    print('\\nChained operations:')
    print((str('Chain with 5: ') + str(chain_result1)))
    print((str('Chain with 50: ') + str(chain_result2)))
    print((str('Chain with -1: ') + str(chain_result3)))
    return {'division_results': [result1, result2, result3], 'validation_results': [validation1, validation2], 'chain_results': [chain_result1, chain_result2, chain_result3]}

def advanced_algorithm_implementations():
    print('\\n=== Advanced Algorithm Implementations ===')
    def quick_sort(arr):
        if (ml_collections.length(arr) <= 1):
            return arr
        pivot = arr[0]
        less = []
        equal = []
        greater = []
        i = 0
        while (i < ml_collections.length(arr)):
            element = arr[i]
            if (element < pivot):
                less = ml_collections.append(less, element)
            elif (element == pivot):
                equal = ml_collections.append(equal, element)
            else:
                greater = ml_collections.append(greater, element)
            i = (i + 1)
        sorted_less = quick_sort(less)
        sorted_greater = quick_sort(greater)
        result = sorted_less
        j = 0
        while (j < ml_collections.length(equal)):
            result = ml_collections.append(result, equal[j])
            j = (j + 1)
        k = 0
        while (k < ml_collections.length(sorted_greater)):
            result = ml_collections.append(result, sorted_greater[k])
            k = (k + 1)
        return result
    unsorted = [64, 34, 25, 12, 22, 11, 90, 5]
    sorted_array = quick_sort(unsorted)
    print('Quick sort result:')
    print((str('Unsorted: ') + str(unsorted)))
    print((str('Sorted: ') + str(sorted_array)))
    def gcd(a, b):
        while (b != 0):
            temp = b
            b = (a % b)
            a = temp
        return a
    gcd_result1 = gcd(48, 18)
    gcd_result2 = gcd(17, 13)
    gcd_result3 = gcd(100, 25)
    print('\\nGCD calculations:')
    print((str('GCD(48, 18) = ') + str(gcd_result1)))
    print((str('GCD(17, 13) = ') + str(gcd_result2)))
    print((str('GCD(100, 25) = ') + str(gcd_result3)))
    def sieve_of_eratosthenes(limit):
        is_prime = []
        primes = []
        i = 0
        while (i <= limit):
            is_prime = ml_collections.append(is_prime, True)
            i = (i + 1)
        is_prime[0] = False
        is_prime[1] = False
        p = 2
        while ((p * p) <= limit):
            if is_prime[p]:
                multiple = (p * p)
                while (multiple <= limit):
                    is_prime[multiple] = False
                    multiple = (multiple + p)
            p = (p + 1)
        i = 2
        while (i <= limit):
            if is_prime[i]:
                primes = ml_collections.append(primes, i)
            i = (i + 1)
        return primes
    primes_30 = sieve_of_eratosthenes(30)
    print((str('Prime numbers up to 30: ') + str(primes_30)))
    def create_bst_node(value):
        return {'value': value, 'left': None, 'right': None}
    def insert_bst(root, value):
        if (root == None):
            return create_bst_node(value)
        if (value < root['value']):
            root['left'] = insert_bst(root['left'], value)
        elif (value > root['value']):
            root['right'] = insert_bst(root['right'], value)
        return root
    def search_bst(root, value):
        if ((root == None) or (root['value'] == value)):
            return root
        if (value < root['value']):
            return search_bst(root['left'], value)
        else:
            return search_bst(root['right'], value)
    def inorder_traversal(root, result):
        if (root != None):
            inorder_traversal(root['left'], result)
            result = ml_collections.append(result, root['value'])
            inorder_traversal(root['right'], result)
        return result
    bst_root = None
    bst_values = [50, 30, 70, 20, 40, 60, 80]
    i = 0
    while (i < ml_collections.length(bst_values)):
        bst_root = insert_bst(bst_root, bst_values[i])
        i = (i + 1)
    search_found = search_bst(bst_root, 40)
    search_missing = search_bst(bst_root, 90)
    traversal_result = inorder_traversal(bst_root, [])
    print('\\nBinary Search Tree:')
    print((str('Inserted values: ') + str(bst_values)))
    print((str('Search for 40: ') + str('found' if (search_found != None) else 'not found')))
    print((str('Search for 90: ') + str('found' if (search_missing != None) else 'not found')))
    print((str('Inorder traversal: ') + str(traversal_result)))
    return {'sorting': {'unsorted': unsorted, 'sorted': sorted_array}, 'gcd_results': [gcd_result1, gcd_result2, gcd_result3], 'primes': primes_30, 'bst': {'inserted': bst_values, 'traversal': traversal_result, 'search_results': {'found_40': (search_found != None), 'found_90': (search_missing != None)}}}

def main():
    print('==============================================')
    print('  ADVANCED CONTROL FLOW AND FUNCTIONS TEST')
    print('==============================================')
    results = {}
    results['basic_control'] = basic_control_flow()
    results['loops'] = loop_constructs_patterns()
    results['functions'] = function_definition_patterns()
    results['higher_order'] = higher_order_functions()
    results['recursion'] = recursive_functions_algorithms()
    results['exceptions'] = exception_handling_error_management()
    results['algorithms'] = advanced_algorithm_implementations()
    print('\\n==============================================')
    print('  ALL CONTROL FLOW AND FUNCTION TESTS COMPLETED')
    print('==============================================')
    return results

main()

# End of generated code