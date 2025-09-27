"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

def createMultiplier(factor):
    def multiply(value):
        return (value * factor)
    return multiply

def applyOperation(value, operation):
    return operation(value)

def processNumbers(numbers):
    double = createMultiplier(2)
    result1 = applyOperation(numbers[0], double)
    result2 = applyOperation(numbers[1], double)
    result3 = applyOperation(numbers[2], double)
    return [result1, result2, result3]

def recursiveSum(arr, index):
    if (index >= 3):
        return 0
    else:
        return (arr[index] + recursiveSum(arr, (index + 1)))

numbers = [5, 10, 15]

doubled = processNumbers(numbers)

sum = recursiveSum(numbers, 0)

# End of generated code