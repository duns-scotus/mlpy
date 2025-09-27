"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

# WARNING: Import 'functional' requires security review
# import functional

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

words = ['hello', 'world', 'functional', 'programming', 'ml']

people = [{'name': 'Alice', 'age': 25, 'department': 'Engineering'}, {'name': 'Bob', 'age': 30, 'department': 'Sales'}, {'name': 'Carol', 'age': 35, 'department': 'Engineering'}, {'name': 'Dave', 'age': 28, 'department': 'Marketing'}, {'name': 'Eve', 'age': 32, 'department': 'Engineering'}]

def isEven(n):
    return ((n % 2) == 0)

def isOdd(n):
    return ((n % 2) == 1)

def double(n):
    return (n * 2)

def square(n):
    return (n * n)

def add(a, b):
    return (a + b)

def multiply(a, b):
    return (a * b)

def isLongWord(word):
    return (functional['length'](word) > 5)

def getAge(person):
    return person['age']

def getDepartment(person):
    return person['department']

def isEngineer(person):
    return (person['department'] == 'Engineering')

def testCoreOperations():
    console['log']('=== Testing Core Functional Operations ===')
    doubled = functional['map'](double, numbers)
    console['log']('Doubled numbers:', doubled)
    squared = functional['map'](square, numbers)
    console['log']('Squared numbers:', squared)
    evens = functional['filter'](isEven, numbers)
    console['log']('Even numbers:', evens)
    odds = functional['filter'](isOdd, numbers)
    console['log']('Odd numbers:', odds)
    longWords = functional['filter'](isLongWord, words)
    console['log']('Long words:', longWords)
    sum = functional['reduce'](add, 0, numbers)
    console['log']('Sum of numbers:', sum)
    product = functional['reduce'](multiply, 1, numbers)
    console['log']('Product of numbers:', product)
    sumOfSquaredEvens = functional['reduce'](add, 0, functional['map'](square, functional['filter'](isEven, numbers)))
    console['log']('Sum of squared evens:', sumOfSquaredEvens)
    console['log']()

def testSearchOperations():
    console['log']('=== Testing Search and Selection Operations ===')
    firstEven = functional['find'](isEven, numbers)
    console['log']('First even number:', firstEven)
    firstEngineer = functional['find'](isEngineer, people)
    console['log']('First engineer:', firstEngineer['name'])
    firstEvenIndex = functional['findIndex'](isEven, numbers)
    console['log']('Index of first even:', firstEvenIndex)
    hasEvens = functional['some'](isEven, numbers)
    console['log']('Has even numbers:', hasEvens)
    hasLargeNumbers = functional['some'](lambda n: (n > 100), numbers)
    console['log']('Has numbers > 100:', hasLargeNumbers)
    allPositive = functional['every'](lambda n: (n > 0), numbers)
    console['log']('All numbers positive:', allPositive)
    allEven = functional['every'](isEven, numbers)
    console['log']('All numbers even:', allEven)
    noNegative = functional['none'](lambda n: (n < 0), numbers)
    console['log']('No negative numbers:', noNegative)
    console['log']()

def testFunctionComposition():
    console['log']('=== Testing Function Composition ===')
    doubleAndSquare = functional['compose'](square, double)
    result1 = doubleAndSquare(5)
    console['log']('Compose double then square (5):', result1)
    squareAndDouble = functional['pipe'](square, double)
    result2 = squareAndDouble(5)
    console['log']('Pipe square then double (5):', result2)
    identityResult = functional['identity'](42)
    console['log']('Identity(42):', identityResult)
    alwaysTrue = functional['constant'](True)
    constantResult = alwaysTrue(99)
    console['log']('Constant(true)(99):', constantResult)
    subtract = lambda a, b: (a - b)
    flippedSubtract = functional['flip'](subtract)
    normal = subtract(10, 3)
    flipped = flippedSubtract(10, 3)
    console['log']('Normal subtract(10, 3):', normal)
    console['log']('Flipped subtract(10, 3):', flipped)
    notEven = functional['negate'](isEven)
    result3 = notEven(4)
    result4 = notEven(5)
    console['log']('Not even(4):', result3)
    console['log']('Not even(5):', result4)
    console['log']()

def testListProcessing():
    console['log']('=== Testing List Processing Operations ===')
    duplicateAndSquare = lambda n: [n, (n * n)]
    flatMapped = functional['flatMap'](duplicateAndSquare, [2, 3, 4])
    console['log']('FlatMap duplicate and square:', flatMapped)
    letters = ['a', 'b', 'c']
    zipped = functional['zip'](numbers, letters)
    console['log']('Zipped numbers and letters:', zipped)
    addStrings = lambda n, s: (n + s)
    zippedWith = functional['zipWith'](addStrings, [1, 2, 3], ['a', 'b', 'c'])
    console['log']('ZipWith add:', zippedWith)
    partitioned = functional['partition'](isEven, numbers)
    console['log']('Partitioned evens/odds:', partitioned)
    peopleByDept = functional['groupBy'](getDepartment, people)
    console['log']('People by department:', peopleByDept)
    duplicates = [1, 2, 2, 3, 3, 3, 4, 5, 5]
    uniqueNumbers = functional['unique'](duplicates)
    console['log']('Unique numbers:', uniqueNumbers)
    console['log']()

def testListSlicing():
    console['log']('=== Testing List Slicing Operations ===')
    firstFive = functional['take'](5, numbers)
    console['log']('Take first 5:', firstFive)
    afterFive = functional['drop'](5, numbers)
    console['log']('Drop first 5:', afterFive)
    takeWhileSmall = functional['takeWhile'](lambda n: (n < 6), numbers)
    console['log']('Take while < 6:', takeWhileSmall)
    dropWhileSmall = functional['dropWhile'](lambda n: (n < 6), numbers)
    console['log']('Drop while < 6:', dropWhileSmall)
    console['log']()

def testConditionalOperations():
    console['log']('=== Testing Conditional Operations ===')
    evenOrOddMessage = functional['ifElse'](isEven, lambda n: (str('Even: ') + str(n)), lambda n: (str('Odd: ') + str(n)))
    console['log']('IfElse for 4:', evenOrOddMessage(4))
    console['log']('IfElse for 7:', evenOrOddMessage(7))
    doubleIfEven = functional['when'](isEven, double)
    console['log']('Double if even (4):', doubleIfEven(4))
    console['log']('Double if even (5):', doubleIfEven(5))
    doubleUnlessEven = functional['unless'](isEven, double)
    console['log']('Double unless even (4):', doubleUnlessEven(4))
    console['log']('Double unless even (5):', doubleUnlessEven(5))
    numberCategory = functional['cond']([[lambda n: (n < 0), lambda n: 'negative'], [lambda n: (n == 0), lambda n: 'zero'], [lambda n: (n < 10), lambda n: 'small'], [lambda n: (n < 100), lambda n: 'medium'], [functional['constant'](True), lambda n: 'large']])
    console['log']('Category of -5:', numberCategory(5))
    console['log']('Category of 0:', numberCategory(0))
    console['log']('Category of 5:', numberCategory(5))
    console['log']('Category of 50:', numberCategory(50))
    console['log']('Category of 500:', numberCategory(500))
    console['log']()

def testUtilities():
    console['log']('=== Testing Utility Functions ===')
    range1to5 = functional['range'](1, 6, 1)
    console['log']('Range 1 to 5:', range1to5)
    evenRange = functional['range'](0, 11, 2)
    console['log']('Even range 0 to 10:', evenRange)
    repeated = functional['repeat']('hello', 3)
    console['log']("Repeat 'hello' 3 times:", repeated)
    squares = functional['times'](square, 5)
    console['log']('Squares of indices 0-4:', squares)
    console['log']()

def advancedFunctionalDemo():
    console['log']('=== Advanced Functional Programming Demo ===')
    console['log']('Processing employee data with FP pipeline:')
    engineeringStats = functional['pipe'](functional['partial'](functional['filter'], isEngineer), functional['partial'](functional['map'], getAge), lambda ages: (functional['reduce'](add, 0, ages) / functional['length'](ages)))
    avgEngineerAge = engineeringStats(people)
    console['log']('Average engineer age:', avgEngineerAge)
    analyzeNumbers = functional['composeAll']([lambda data: {'original': data['numbers'], 'evens': data['evens'], 'odds': data['odds'], 'evenSum': data['evenSum'], 'oddSum': data['oddSum'], 'ratio': (data['evenSum'] / data['oddSum'])}, lambda data: {'numbers': data['numbers'], 'evens': data['evens'], 'odds': data['odds'], 'evenSum': functional['reduce'](add, 0, data['evens']), 'oddSum': functional['reduce'](add, 0, data['odds'])}, lambda nums: {'numbers': nums, 'evens': partitioned[0], 'odds': partitioned[1]}, functional['identity']])
    analysis = analyzeNumbers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    console['log']('Number analysis:', analysis)
    console['log']()

def runAllTests():
    console['log']('======================================================')
    console['log']('ML FUNCTIONAL PROGRAMMING STANDARD LIBRARY TESTS')
    console['log']('======================================================')
    console['log']()
    testCoreOperations()
    testSearchOperations()
    testFunctionComposition()
    testListProcessing()
    testListSlicing()
    testConditionalOperations()
    testUtilities()
    advancedFunctionalDemo()
    console['log']('======================================================')
    console['log']('ALL FUNCTIONAL PROGRAMMING TESTS COMPLETED!')
    console['log']('======================================================')
    return {'test_status': 'completed', 'module': 'functional', 'features_tested': ['map, filter, reduce', 'find, some, every, none', 'compose, pipe, curry', 'zip, partition, groupBy, unique', 'take, drop, takeWhile, dropWhile', 'ifElse, when, unless, cond', 'range, repeat, times', 'advanced composition and pipelines'], 'total_operations': 50, 'functional_paradigm': 'fully_supported'}

testResults = runAllTests()

def createDataPipeline():
    processEmployeeData = functional['pipeAll']([functional['partial'](functional['filter'], lambda p: ((p['department'] == 'Engineering') and (p['age'] < 40))), functional['partial'](functional['map'], lambda p: {'name': p['name'], 'experience_level': 'junior' if (p['age'] < 30) else 'senior', 'age_group': '20s' if (p['age'] < 30) else '30s'}), functional['partial'](functional['groupBy'], lambda p: p['experience_level']), lambda grouped: {'data': grouped, 'summary': {'junior_count': functional['length']((grouped['junior'] or [])), 'senior_count': functional['length']((grouped['senior'] or [])), 'total_processed': functional['length'](((grouped['junior'] or []) + (grouped['senior'] or [])))}}])
    result = processEmployeeData(people)
    console['log']('Employee processing pipeline result:', result)
    return result

finalDemo = createDataPipeline()

# End of generated code