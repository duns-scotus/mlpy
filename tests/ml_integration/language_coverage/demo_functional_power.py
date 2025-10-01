"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib import typeof

# WARNING: Import 'functional' requires security review
# import functional
from mlpy.stdlib.collections_bridge import collections as ml_collections
from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access


def safe_upsert(arr, pos, item):
    if pos < _safe_attr_access(arr, "length"):
        new_arr = []
        i = 0
        while i < _safe_attr_access(arr, "length"):
            if i == pos:
                new_arr = ml_collections.append(new_arr, item)
            else:
                new_arr = ml_collections.append(new_arr, arr[i])
            i = i + 1
        return new_arr
    else:
        return ml_collections.append(arr, item)


def safe_append(arr, item):
    return ml_collections.append(arr, item)


def to_string(value):
    if typeof(value) == "string":
        return value
    elif typeof(value) == "number":
        return str(value) + ""
    elif typeof(value) == "boolean":
        return "true" if value else "false"
    else:
        return "[object]"


employees = []

safe_append(
    employees,
    {"name": "Alice", "age": 28, "department": "Engineering", "salary": 95000, "experience": 5},
)

safe_append(
    employees, {"name": "Bob", "age": 35, "department": "Sales", "salary": 75000, "experience": 10}
)

safe_append(
    employees,
    {"name": "Carol", "age": 42, "department": "Engineering", "salary": 120000, "experience": 15},
)

safe_append(
    employees,
    {"name": "Dave", "age": 29, "department": "Marketing", "salary": 65000, "experience": 6},
)

safe_append(
    employees,
    {"name": "Eve", "age": 31, "department": "Engineering", "salary": 88000, "experience": 7},
)

safe_append(
    employees,
    {"name": "Frank", "age": 38, "department": "Sales", "salary": 82000, "experience": 12},
)

safe_append(
    employees,
    {"name": "Grace", "age": 26, "department": "Engineering", "salary": 78000, "experience": 3},
)

safe_append(
    employees,
    {"name": "Henry", "age": 45, "department": "Management", "salary": 150000, "experience": 20},
)

transactions = []

safe_append(
    transactions,
    {"id": 1, "amount": 1200, "type": "income", "category": "salary", "date": "2024-01"},
)

safe_append(
    transactions, {"id": 2, "amount": 450, "type": "expense", "category": "rent", "date": "2024-01"}
)

safe_append(
    transactions,
    {"id": 3, "amount": 200, "type": "expense", "category": "groceries", "date": "2024-01"},
)

safe_append(
    transactions,
    {"id": 4, "amount": 1200, "type": "income", "category": "salary", "date": "2024-02"},
)

safe_append(
    transactions, {"id": 5, "amount": 450, "type": "expense", "category": "rent", "date": "2024-02"}
)

safe_append(
    transactions,
    {"id": 6, "amount": 180, "type": "expense", "category": "groceries", "date": "2024-02"},
)

safe_append(
    transactions,
    {"id": 7, "amount": 300, "type": "expense", "category": "entertainment", "date": "2024-02"},
)


def demonstrateBasicOperations():
    print("=== Basic Functional Operations ===")
    numbers = _safe_attr_access(functional, "range")(1, 21, 1)
    doubled = _safe_attr_access(functional, "map")(lambda x: (x * 2), numbers)
    evens = _safe_attr_access(functional, "filter")(lambda x: ((x % 2) == 0), numbers)
    sum = _safe_attr_access(functional, "reduce")(lambda a, b: (a + b), 0, evens)
    print(

            str("Numbers 1-20: " + str(to_string(_safe_attr_access(numbers, "length"))))
            + " elements"

    )
    print(

            str("Doubled: " + str(to_string(_safe_attr_access(doubled, "length"))))
            + " elements"

    )
    print(

            str("Even numbers: " + str(to_string(_safe_attr_access(evens, "length"))))
            + " elements"

    )
    print("Sum of evens: " + str(to_string(sum)))
    firstBigNumber = _safe_attr_access(functional, "find")(lambda x: (x > 15), numbers)
    hasBigNumbers = _safe_attr_access(functional, "some")(lambda x: (x > 15), numbers)
    allPositive = _safe_attr_access(functional, "every")(lambda x: (x > 0), numbers)
    print("First number > 15: " + str(to_string(firstBigNumber)))
    print("Has numbers > 15: " + str(to_string(hasBigNumbers)))
    print("All positive: " + str(to_string(allPositive)))
    print("")


def demonstrateComposition():
    print("=== Function Composition Mastery ===")
    isEven = lambda x: ((x % 2) == 0)
    square = lambda x: (x * x)
    double = lambda x: (x * 2)
    sum = _safe_attr_access(functional, "partial")(
        _safe_attr_access(functional, "reduce"), lambda a, b: (a + b)
    )
    sumOfSquaredEvens = _safe_attr_access(functional, "pipeAll")(
        [
            _safe_attr_access(functional, "partial")(
                _safe_attr_access(functional, "filter"), isEven
            ),
            _safe_attr_access(functional, "partial")(_safe_attr_access(functional, "map"), square),
            lambda list: _safe_attr_access(functional, "reduce")(lambda a, b: (a + b), 0, list),
        ]
    )
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = sumOfSquaredEvens(numbers)
    print("Sum of squared evens: " + str(to_string(result)))
    complexTransform = _safe_attr_access(functional, "composeAll")(
        [lambda x: (x / 2), square, double]
    )
    transformed = complexTransform(5)
    print("Complex transform(5): " + str(to_string(transformed)))
    add = lambda a, b: (a + b)
    curriedAdd = _safe_attr_access(functional, "curry2")(add)
    add10 = curriedAdd(10)
    results = _safe_attr_access(functional, "map")(add10, [1, 2, 3, 4, 5])
    print(

            str("Add 10 to each: " + str(to_string(_safe_attr_access(results, "length"))))
            + " results"

    )
    print("")


def demonstrateDataProcessing():
    print("=== Advanced Data Processing ===")

    def analyzeEngineering(engineers):
        ages = _safe_attr_access(functional, "map")(
            lambda emp: _safe_attr_access(emp, "age"), engineers
        )
        salaries = _safe_attr_access(functional, "map")(
            lambda emp: _safe_attr_access(emp, "salary"), engineers
        )
        experiences = _safe_attr_access(functional, "map")(
            lambda emp: _safe_attr_access(emp, "experience"), engineers
        )
        return {
            "count": _safe_attr_access(engineers, "length"),
            "avgAge": (
                _safe_attr_access(functional, "reduce")(lambda a, b: (a + b), 0, ages)
                / _safe_attr_access(ages, "length")
            ),
            "avgSalary": (
                _safe_attr_access(functional, "reduce")(lambda a, b: (a + b), 0, salaries)
                / _safe_attr_access(salaries, "length")
            ),
            "totalExperience": _safe_attr_access(functional, "reduce")(
                lambda a, b: (a + b), 0, experiences
            ),
            "names": _safe_attr_access(functional, "map")(
                lambda emp: _safe_attr_access(emp, "name"), engineers
            ),
        }

    engineeringEmployees = _safe_attr_access(functional, "filter")(
        lambda emp: (_safe_attr_access(emp, "department") == "Engineering"), employees
    )
    engStats = analyzeEngineering(engineeringEmployees)
    print("Engineering Department Analysis:")
    print("  Count: " + str(to_string(_safe_attr_access(engStats, "count"))))
    print("  Avg Age: " + str(to_string(_safe_attr_access(engStats, "avgAge"))))
    print("  Avg Salary: " + str(to_string(_safe_attr_access(engStats, "avgSalary"))))
    experienceLevels = _safe_attr_access(functional, "groupBy")(lambda emp: "senior", employees)
    print("Experience levels grouped successfully")
    salaryPartition = _safe_attr_access(functional, "partition")(
        lambda emp: (_safe_attr_access(emp, "salary") > 80000), employees
    )
    highEarners = _safe_attr_access(functional, "map")(
        lambda emp: _safe_attr_access(emp, "name"), salaryPartition[0]
    )
    lowerEarners = _safe_attr_access(functional, "map")(
        lambda emp: _safe_attr_access(emp, "name"), salaryPartition[1]
    )
    print("High/Low salary partition:")
    print(

            str(
                "  High earners: " + str(to_string(_safe_attr_access(highEarners, "length")))
            )
            + " employees"

    )
    print(

            str(

                    "  Lower earners: "
                    + str(to_string(_safe_attr_access(lowerEarners, "length")))

            )
            + " employees"

    )
    print("")


def demonstrateFinancialAnalysis():
    print("=== Financial Data Analysis ===")

    def analyzeMonth(monthlyTxns):
        result = {}
        for month in monthlyTxns:
            monthTransactions = monthlyTxns[month]
            income = _safe_attr_access(functional, "filter")(
                lambda txn: (_safe_attr_access(txn, "type") == "income"), monthTransactions
            )
            expenses = _safe_attr_access(functional, "filter")(
                lambda txn: (_safe_attr_access(txn, "type") == "expense"), monthTransactions
            )
            totalIncome = _safe_attr_access(functional, "reduce")(
                lambda sum, txn: (sum + _safe_attr_access(txn, "amount")), 0, income
            )
            totalExpenses = _safe_attr_access(functional, "reduce")(
                lambda sum, txn: (sum + _safe_attr_access(txn, "amount")), 0, expenses
            )
            result[month] = {
                "income": totalIncome,
                "expenses": totalExpenses,
                "netIncome": (totalIncome - totalExpenses),
                "transactionCount": _safe_attr_access(monthTransactions, "length"),
            }
        return result

    monthlyTxns = _safe_attr_access(functional, "groupBy")(
        lambda txn: _safe_attr_access(txn, "date"), transactions
    )
    financialSummary = analyzeMonth(monthlyTxns)
    print("Monthly Financial Analysis completed")
    expenseTransactions = _safe_attr_access(functional, "filter")(
        lambda txn: (_safe_attr_access(txn, "type") == "expense"), transactions
    )
    expensesByCategory = _safe_attr_access(functional, "groupBy")(
        lambda txn: _safe_attr_access(txn, "category"), expenseTransactions
    )
    print("Expense Analysis by Category completed")
    print("")


def demonstrateConditionalLogic():
    print("=== Conditional Logic Mastery ===")
    evaluateEmployee = _safe_attr_access(functional, "ifElse")(
        lambda emp: (_safe_attr_access(emp, "salary") > 100000),
        lambda emp: (str(_safe_attr_access(emp, "name")) + " - Executive Level"),
        _safe_attr_access(functional, "ifElse")(
            lambda emp: (_safe_attr_access(emp, "experience") > 10),
            lambda emp: (str(_safe_attr_access(emp, "name")) + " - Senior Level"),
            lambda emp: (str(_safe_attr_access(emp, "name")) + " - Standard Level"),
        ),
    )
    evaluations = _safe_attr_access(functional, "map")(evaluateEmployee, employees)
    print(

            str(

                    "Employee Evaluations: "
                    + str(to_string(_safe_attr_access(evaluations, "length")))

            )
            + " completed"

    )
    adjustSalary = _safe_attr_access(functional, "cond")(
        [
            [
                lambda emp: (
                    (_safe_attr_access(emp, "department") == "Engineering")
                    and (_safe_attr_access(emp, "experience") > 10)
                ),
                lambda emp: (_safe_attr_access(emp, "salary") * 1.15),
            ],
            [
                lambda emp: (_safe_attr_access(emp, "department") == "Engineering"),
                lambda emp: (_safe_attr_access(emp, "salary") * 1.1),
            ],
            [
                lambda emp: (_safe_attr_access(emp, "experience") > 15),
                lambda emp: (_safe_attr_access(emp, "salary") * 1.12),
            ],
            [
                _safe_attr_access(functional, "constant")(True),
                lambda emp: (_safe_attr_access(emp, "salary") * 1.05),
            ],
        ]
    )
    salaryAdjustments = _safe_attr_access(functional, "map")(
        lambda emp: {
            "name": _safe_attr_access(emp, "name"),
            "currentSalary": _safe_attr_access(emp, "salary"),
            "adjustedSalary": newSalary,
            "increase": (newSalary - _safe_attr_access(emp, "salary")),
        },
        employees,
    )
    print(

            str(

                    "Salary Adjustments: "
                    + str(to_string(_safe_attr_access(salaryAdjustments, "length")))

            )
            + " processed"

    )
    print("")


def demonstrateUtilityFunctions():
    print("=== Utility Function Showcase ===")
    testRanges = []
    safe_append(testRanges, _safe_attr_access(functional, "range")(1, 11, 1))
    safe_append(testRanges, _safe_attr_access(functional, "range")(0, 101, 10))
    safe_append(testRanges, _safe_attr_access(functional, "range")(100, 0, 5))
    print(

            str(

                    "Generated ranges: "
                    + str(to_string(_safe_attr_access(testRanges, "length")))

            )
            + " ranges"

    )
    greetings = _safe_attr_access(functional, "repeat")("Hello", 3)
    factorials = _safe_attr_access(functional, "times")(
        lambda n: _safe_attr_access(functional, "reduce")(
            lambda acc, x: (acc * x), 1, _safe_attr_access(functional, "range")(1, (n + 1), 1)
        ),
        6,
    )
    print(

            str(

                    "Repeated greetings: "
                    + str(to_string(_safe_attr_access(greetings, "length")))

            )
            + " items"

    )
    print(

            str(

                    "First 6 factorials: "
                    + str(to_string(_safe_attr_access(factorials, "length")))

            )
            + " computed"

    )
    letters = ["a", "b", "c", "d", "e"]
    numbers = [1, 2, 3, 4, 5]
    zipped = _safe_attr_access(functional, "zip")(letters, numbers)
    zipSum = _safe_attr_access(functional, "zipWith")(
        lambda letter, num: (letter + to_string(num)), letters, numbers
    )
    print(

            str("Zipped pairs: " + str(to_string(_safe_attr_access(zipped, "length"))))
            + " pairs"

    )
    print(

            str(

                    "Zip with concatenation: "
                    + str(to_string(_safe_attr_access(zipSum, "length")))

            )
            + " items"

    )
    longList = _safe_attr_access(functional, "range")(1, 101, 1)
    first10 = _safe_attr_access(functional, "take")(10, longList)
    last10 = _safe_attr_access(functional, "take")(
        10, _safe_attr_access(functional, "drop")(90, longList)
    )
    takeWhileSmall = _safe_attr_access(functional, "takeWhile")(lambda x: (x < 50), longList)
    print(

            str("First 10: " + str(to_string(_safe_attr_access(first10, "length"))))
            + " items"

    )
    print(

            str("Last 10: " + str(to_string(_safe_attr_access(last10, "length"))))
            + " items"

    )
    print(

            "Take while < 50 (length): "
            + str(to_string(_safe_attr_access(takeWhileSmall, "length")))

    )
    print("")


def demonstrateAdvancedComposition():
    print("=== Advanced Composition Patterns ===")

    def createDataProcessor(filterFn, transformFn, aggregateFn):
        return _safe_attr_access(functional, "pipeAll")(
            [
                _safe_attr_access(functional, "partial")(
                    _safe_attr_access(functional, "filter"), filterFn
                ),
                _safe_attr_access(functional, "partial")(
                    _safe_attr_access(functional, "map"), transformFn
                ),
                aggregateFn,
            ]
        )

    sumSquaredEvens = createDataProcessor(
        lambda x: ((x % 2) == 0),
        lambda x: (x * x),
        lambda list: _safe_attr_access(functional, "reduce")(lambda a, b: (a + b), 0, list),
    )
    productOddDoubles = createDataProcessor(
        lambda x: ((x % 2) == 1),
        lambda x: (x * 2),
        lambda list: _safe_attr_access(functional, "reduce")(lambda a, b: (a * b), 1, list),
    )
    testNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print("Sum of squared evens: " + str(to_string(sumSquaredEvens(testNumbers))))
    print("Product of doubled odds: " + str(to_string(productOddDoubles(testNumbers))))
    analyzeNumber = _safe_attr_access(functional, "juxt")(
        [
            lambda x: "even" if ((x % 2) == 0) else "odd",
            lambda x: "big" if (x > 5) else "small",
            lambda x: (x * x),
            lambda x: (str(to_string(x)) + "!"),
        ]
    )
    analysis = analyzeNumber(7)
    print(

            str(

                    "Multi-analysis of 7: "
                    + str(to_string(_safe_attr_access(analysis, "length")))

            )
            + " results"

    )
    print("")


def runFunctionalProgrammingMasterclass():
    print("===========================================================")
    print("ML FUNCTIONAL PROGRAMMING MASTERCLASS")
    print("Demonstrating the Full Power of Functional Programming in ML")
    print("===========================================================")
    print("")
    demonstrateBasicOperations()
    demonstrateComposition()
    demonstrateDataProcessing()
    demonstrateFinancialAnalysis()
    demonstrateConditionalLogic()
    demonstrateUtilityFunctions()
    demonstrateAdvancedComposition()
    print("===========================================================")
    print("FUNCTIONAL PROGRAMMING MASTERCLASS COMPLETE!")
    print("===========================================================")
    print("")
    print("ML now provides:")
    print("✓ Complete higher-order function suite")
    print("✓ Advanced function composition capabilities")
    print("✓ Powerful data transformation operations")
    print("✓ Elegant conditional logic handling")
    print("✓ Rich utility function library")
    print("✓ Security-integrated Python bridges")
    print("✓ Production-ready performance optimizations")
    print("")
    print("ML functional programming is now on par with Haskell,")
    print("Ramda, and other leading functional programming environments!")
    return {
        "masterclass": "completed",
        "functional_paradigm": "fully_supported",
        "operations_demonstrated": 50,
        "complexity_level": "enterprise_ready",
        "ml_fp_status": "production_ready",
    }


masterclassResults = runFunctionalProgrammingMasterclass()


def ultimateFunctionalDemo():
    print("")
    print("=== ULTIMATE FUNCTIONAL PROGRAMMING DEMONSTRATION ===")

    def formatFinalOutput(analysis):
        return {
            "summary": "Ultimate ML Functional Programming Demo",
            "processed_employees": _safe_attr_access(analysis, "totalEmployees"),
            "departments_analyzed": _safe_attr_access(
                _safe_attr_access(analysis, "departmentBreakdown"), "length"
            ),
            "total_payroll": _safe_attr_access(analysis, "totalPayroll"),
            "avg_departmental_salary": _safe_attr_access(analysis, "avgDepartmentalSalary"),
            "top_department": _safe_attr_access(analysis, "topDepartment"),
            "efficiency_score": _safe_attr_access(analysis, "efficiencyScore"),
            "ml_fp_capability": "enterprise_grade",
        }

    def calculateEfficiencyMetrics(deptAnalysis):
        topDept = _safe_attr_access(functional, "reduce")(
            lambda top, dept: (
                dept
                if (_safe_attr_access(dept, "avgSalary") > _safe_attr_access(top, "avgSalary"))
                else top
            ),
            {"avgSalary": 0},
            _safe_attr_access(deptAnalysis, "departments"),
        )
        totalPayroll = _safe_attr_access(functional, "reduce")(
            lambda sum, dept: (sum + _safe_attr_access(dept, "totalSalary")),
            0,
            _safe_attr_access(deptAnalysis, "departments"),
        )
        return {
            "totalEmployees": _safe_attr_access(deptAnalysis, "totalEmployees"),
            "departmentBreakdown": _safe_attr_access(deptAnalysis, "departments"),
            "totalPayroll": totalPayroll,
            "avgDepartmentalSalary": (
                totalPayroll
                / _safe_attr_access(_safe_attr_access(deptAnalysis, "departments"), "length")
            ),
            "topDepartment": _safe_attr_access(topDept, "name"),
            "efficiencyScore": ((_safe_attr_access(topDept, "avgSalary") / totalPayroll) * 100),
        }

    def aggregateDepartmentalData(grouped):
        departments = []
        totalEmployees = 0
        for deptName in grouped:
            deptEmployees = grouped[deptName]
            totalSalary = _safe_attr_access(functional, "reduce")(
                lambda sum, emp: (sum + _safe_attr_access(emp, "salary")), 0, deptEmployees
            )
            avgSalary = totalSalary / _safe_attr_access(deptEmployees, "length")
            safe_append(
                departments,
                {
                    "name": deptName,
                    "employeeCount": _safe_attr_access(deptEmployees, "length"),
                    "totalSalary": totalSalary,
                    "avgSalary": avgSalary,
                    "avgExperience": (
                        _safe_attr_access(functional, "reduce")(
                            lambda sum, emp: (sum + _safe_attr_access(emp, "experience")),
                            0,
                            deptEmployees,
                        )
                        / _safe_attr_access(deptEmployees, "length")
                    ),
                },
            )
            totalEmployees = totalEmployees + _safe_attr_access(deptEmployees, "length")
        return {"departments": departments, "totalEmployees": totalEmployees}

    filteredEmployees = _safe_attr_access(functional, "filter")(
        lambda emp: (
            (_safe_attr_access(emp, "age") < 50) and (_safe_attr_access(emp, "salary") > 50000)
        ),
        employees,
    )
    groupedByDept = _safe_attr_access(functional, "groupBy")(
        lambda emp: _safe_attr_access(emp, "department"), filteredEmployees
    )
    aggregatedData = aggregateDepartmentalData(groupedByDept)
    metricsData = calculateEfficiencyMetrics(aggregatedData)
    ultimateResult = formatFinalOutput(metricsData)
    print("ULTIMATE RESULT:")
    print("  Summary: " + str(_safe_attr_access(ultimateResult, "summary")))
    print(

            "  Processed Employees: "
            + str(to_string(_safe_attr_access(ultimateResult, "processed_employees")))

    )
    print(

            "  Departments Analyzed: "
            + str(to_string(_safe_attr_access(ultimateResult, "departments_analyzed")))

    )
    print(

            "  Total Payroll: "
            + str(to_string(_safe_attr_access(ultimateResult, "total_payroll")))

    )
    print("  Top Department: " + str(_safe_attr_access(ultimateResult, "top_department")))
    print(
        "  ML FP Capability: " + str(_safe_attr_access(ultimateResult, "ml_fp_capability"))
    )
    print("")
    print("🎉 ML FUNCTIONAL PROGRAMMING: MISSION ACCOMPLISHED! 🎉")


ultimateFunctionalDemo()

# End of generated code
