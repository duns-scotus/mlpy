"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

# WARNING: Import 'functional' requires security review
# import functional

employees = [{'name': 'Alice', 'age': 28, 'department': 'Engineering', 'salary': 95000, 'experience': 5}, {'name': 'Bob', 'age': 35, 'department': 'Sales', 'salary': 75000, 'experience': 10}, {'name': 'Carol', 'age': 42, 'department': 'Engineering', 'salary': 120000, 'experience': 15}, {'name': 'Dave', 'age': 29, 'department': 'Marketing', 'salary': 65000, 'experience': 6}, {'name': 'Eve', 'age': 31, 'department': 'Engineering', 'salary': 88000, 'experience': 7}, {'name': 'Frank', 'age': 38, 'department': 'Sales', 'salary': 82000, 'experience': 12}, {'name': 'Grace', 'age': 26, 'department': 'Engineering', 'salary': 78000, 'experience': 3}, {'name': 'Henry', 'age': 45, 'department': 'Management', 'salary': 150000, 'experience': 20}]

transactions = [{'id': 1, 'amount': 1200, 'type': 'income', 'category': 'salary', 'date': '2024-01'}, {'id': 2, 'amount': 450, 'type': 'expense', 'category': 'rent', 'date': '2024-01'}, {'id': 3, 'amount': 200, 'type': 'expense', 'category': 'groceries', 'date': '2024-01'}, {'id': 4, 'amount': 1200, 'type': 'income', 'category': 'salary', 'date': '2024-02'}, {'id': 5, 'amount': 450, 'type': 'expense', 'category': 'rent', 'date': '2024-02'}, {'id': 6, 'amount': 180, 'type': 'expense', 'category': 'groceries', 'date': '2024-02'}, {'id': 7, 'amount': 300, 'type': 'expense', 'category': 'entertainment', 'date': '2024-02'}]

def demonstrateBasicOperations():
    console['log']('=== Basic Functional Operations ===')
    numbers = functional['range'](1, 21, 1)
    doubled = functional['map'](lambda x: (x * 2), numbers)
    evens = functional['filter'](lambda x: ((x % 2) == 0), numbers)
    sum = functional['reduce'](lambda a, b: (a + b), 0, evens)
    console['log']('Numbers 1-20:', numbers)
    console['log']('Doubled:', doubled)
    console['log']('Even numbers:', evens)
    console['log']('Sum of evens:', sum)
    firstBigNumber = functional['find'](lambda x: (x > 15), numbers)
    hasBigNumbers = functional['some'](lambda x: (x > 15), numbers)
    allPositive = functional['every'](lambda x: (x > 0), numbers)
    console['log']('First number > 15:', firstBigNumber)
    console['log']('Has numbers > 15:', hasBigNumbers)
    console['log']('All positive:', allPositive)
    console['log']()

def demonstrateComposition():
    console['log']('=== Function Composition Mastery ===')
    isEven = lambda x: ((x % 2) == 0)
    square = lambda x: (x * x)
    double = lambda x: (x * 2)
    sum = functional['partial'](functional['reduce'], lambda a, b: (a + b), 0)
    sumOfSquaredEvens = functional['pipe'](functional['partial'](functional['filter'], isEven), functional['partial'](functional['map'], square), sum)
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = sumOfSquaredEvens(numbers)
    console['log']('Sum of squared evens:', result)
    complexTransform = functional['composeAll']([lambda x: (x / 2), square, double])
    transformed = complexTransform(5)
    console['log']('Complex transform(5):', transformed)
    add = lambda a, b: (a + b)
    curriedAdd = functional['curry2'](add)
    add10 = curriedAdd(10)
    results = functional['map'](add10, [1, 2, 3, 4, 5])
    console['log']('Add 10 to each:', results)
    console['log']()

def demonstrateDataProcessing():
    console['log']('=== Advanced Data Processing ===')
    engineeringAnalysis = functional['pipe'](functional['partial'](functional['filter'], lambda emp: (emp['department'] == 'Engineering')), lambda engineers: {'count': functional['length'](engineers), 'avgAge': (functional['reduce'](lambda a, b: (a + b), 0, ages) / functional['length'](ages)), 'avgSalary': (functional['reduce'](lambda a, b: (a + b), 0, salaries) / functional['length'](salaries)), 'totalExperience': functional['reduce'](lambda a, b: (a + b), 0, experiences), 'names': functional['map'](lambda emp: emp['name'], engineers)})
    engStats = engineeringAnalysis(employees)
    console['log']('Engineering Department Analysis:', engStats)
    experienceLevels = functional['groupBy'](lambda emp: 'senior', employees)
    console['log']('Employees by experience level:', experienceLevels)
    salaryPartition = functional['partition'](lambda emp: (emp['salary'] > 80000), employees)
    console['log']('High/Low salary partition:')
    console['log']('  High earners:', functional['map'](lambda emp: emp['name'], salaryPartition[0]))
    console['log']('  Lower earners:', functional['map'](lambda emp: emp['name'], salaryPartition[1]))
    console['log']()

def demonstrateFinancialAnalysis():
    console['log']('=== Financial Data Analysis ===')
    monthlyAnalysis = functional['pipe'](functional['partial'](functional['groupBy'], lambda txn: txn['date']), lambda monthlyTxns: {})
    financialSummary = monthlyAnalysis(transactions)
    console['log']('Monthly Financial Analysis:', financialSummary)
    expensesByCategory = functional['pipe'](functional['partial'](functional['filter'], lambda txn: (txn['type'] == 'expense')), functional['partial'](functional['groupBy'], lambda txn: txn['category']), lambda categories: {})
    expenseAnalysis = expensesByCategory(transactions)
    console['log']('Expense Analysis by Category:', expenseAnalysis)
    console['log']()

def demonstrateConditionalLogic():
    console['log']('=== Conditional Logic Mastery ===')
    evaluateEmployee = functional['ifElse'](lambda emp: (emp['salary'] > 100000), lambda emp: (str(emp['name']) + str(' - Executive Level')), functional['ifElse'](lambda emp: (emp['experience'] > 10), lambda emp: (str(emp['name']) + str(' - Senior Level')), lambda emp: (str(emp['name']) + str(' - Standard Level'))))
    evaluations = functional['map'](evaluateEmployee, employees)
    console['log']('Employee Evaluations:', evaluations)
    adjustSalary = functional['cond']([[lambda emp: ((emp['department'] == 'Engineering') and (emp['experience'] > 10)), lambda emp: (emp['salary'] * 1.15)], [lambda emp: (emp['department'] == 'Engineering'), lambda emp: (emp['salary'] * 1.1)], [lambda emp: (emp['experience'] > 15), lambda emp: (emp['salary'] * 1.12)], [functional['constant'](True), lambda emp: (emp['salary'] * 1.05)]])
    salaryAdjustments = functional['map'](lambda emp: {'name': emp['name'], 'currentSalary': emp['salary'], 'adjustedSalary': adjustSalary(emp), 'increase': (adjustSalary(emp) - emp['salary'])}, employees)
    console['log']('Salary Adjustments:', salaryAdjustments)
    console['log']()

def demonstrateUtilityFunctions():
    console['log']('=== Utility Function Showcase ===')
    testRanges = [functional['range'](1, 11, 1), functional['range'](0, 101, 10), functional['range'](100, 0, 5)]
    console['log']('Generated ranges:', testRanges)
    greetings = functional['repeat']('Hello', 3)
    factorials = functional['times'](lambda n: functional['reduce'](lambda acc, x: (acc * x), 1, functional['range'](1, (n + 1), 1)), 6)
    console['log']('Repeated greetings:', greetings)
    console['log']('First 6 factorials:', factorials)
    letters = ['a', 'b', 'c', 'd', 'e']
    numbers = [1, 2, 3, 4, 5]
    zipped = functional['zip'](letters, numbers)
    zipSum = functional['zipWith'](lambda letter, num: (letter + num), letters, numbers)
    console['log']('Zipped pairs:', zipped)
    console['log']('Zip with concatenation:', zipSum)
    longList = functional['range'](1, 101, 1)
    first10 = functional['take'](10, longList)
    last10 = functional['take'](10, functional['drop'](90, longList))
    takeWhileSmall = functional['takeWhile'](lambda x: (x < 50), longList)
    console['log']('First 10:', first10)
    console['log']('Last 10:', last10)
    console['log']('Take while < 50 (length):', functional['length'](takeWhileSmall))
    console['log']()

def demonstrateAdvancedComposition():
    console['log']('=== Advanced Composition Patterns ===')
    createDataProcessor = lambda filterFn, transformFn, aggregateFn: functional['pipe'](functional['partial'](functional['filter'], filterFn), functional['partial'](functional['map'], transformFn), aggregateFn)
    sumSquaredEvens = createDataProcessor(lambda x: ((x % 2) == 0), lambda x: (x * x), functional['partial'](functional['reduce'], lambda a, b: (a + b), 0))
    productOddDoubles = createDataProcessor(lambda x: ((x % 2) == 1), lambda x: (x * 2), functional['partial'](functional['reduce'], lambda a, b: (a * b), 1))
    testNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    console['log']('Sum of squared evens:', sumSquaredEvens(testNumbers))
    console['log']('Product of doubled odds:', productOddDoubles(testNumbers))
    analyzeNumber = functional['juxt']([lambda x: 'even' if ((x % 2) == 0) else 'odd', lambda x: 'big' if (x > 5) else 'small', lambda x: (x * x), lambda x: (str(x) + str('!'))])
    analysis = analyzeNumber(7)
    console['log']('Multi-analysis of 7:', analysis)
    console['log']()

def runFunctionalProgrammingMasterclass():
    console['log']('===========================================================')
    console['log']('ML FUNCTIONAL PROGRAMMING MASTERCLASS')
    console['log']('Demonstrating the Full Power of Functional Programming in ML')
    console['log']('===========================================================')
    console['log']()
    demonstrateBasicOperations()
    demonstrateComposition()
    demonstrateDataProcessing()
    demonstrateFinancialAnalysis()
    demonstrateConditionalLogic()
    demonstrateUtilityFunctions()
    demonstrateAdvancedComposition()
    console['log']('===========================================================')
    console['log']('FUNCTIONAL PROGRAMMING MASTERCLASS COMPLETE!')
    console['log']('===========================================================')
    console['log']()
    console['log']('ML now provides:')
    console['log']('✓ Complete higher-order function suite')
    console['log']('✓ Advanced function composition capabilities')
    console['log']('✓ Powerful data transformation operations')
    console['log']('✓ Elegant conditional logic handling')
    console['log']('✓ Rich utility function library')
    console['log']('✓ Security-integrated Python bridges')
    console['log']('✓ Production-ready performance optimizations')
    console['log']()
    console['log']('ML functional programming is now on par with Haskell,')
    console['log']('Ramda, and other leading functional programming environments!')
    return {'masterclass': 'completed', 'functional_paradigm': 'fully_supported', 'operations_demonstrated': 50, 'complexity_level': 'enterprise_ready', 'ml_fp_status': 'production_ready'}

masterclassResults = runFunctionalProgrammingMasterclass()

def ultimateFunctionalDemo():
    console['log']('\\n=== ULTIMATE FUNCTIONAL PROGRAMMING DEMONSTRATION ===')
    ultimateProcessor = functional['composeAll']([lambda analysis: {'summary': 'Ultimate ML Functional Programming Demo', 'processed_employees': analysis['totalEmployees'], 'departments_analyzed': functional['length'](analysis['departmentBreakdown']), 'total_payroll': analysis['totalPayroll'], 'avg_departmental_salary': analysis['avgDepartmentalSalary'], 'top_department': analysis['topDepartment'], 'efficiency_score': analysis['efficiencyScore'], 'ml_fp_capability': 'enterprise_grade'}, lambda deptAnalysis: {'totalEmployees': deptAnalysis['totalEmployees'], 'departmentBreakdown': deptAnalysis['departments'], 'totalPayroll': totalPayroll, 'avgDepartmentalSalary': (totalPayroll / functional['length'](deptAnalysis['departments'])), 'topDepartment': topDept['name'], 'efficiencyScore': ((topDept['avgSalary'] / totalPayroll) * 100)}, lambda grouped: {'departments': departments, 'totalEmployees': totalEmployees}, functional['partial'](functional['groupBy'], lambda emp: emp['department']), functional['partial'](functional['filter'], lambda emp: ((emp['age'] < 50) and (emp['salary'] > 50000)))])
    ultimateResult = ultimateProcessor(employees)
    console['log']('ULTIMATE RESULT:', ultimateResult)
    console['log']('\\n🎉 ML FUNCTIONAL PROGRAMMING: MISSION ACCOMPLISHED! 🎉')

ultimateFunctionalDemo()

# End of generated code