"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

def processNumber(n):
    if (n > 10):
        result = (n * 2)
        return result
    else:
        return (n + 5)

def countUp(start):
    i = start
    while (i < 5):
        i = (i + 1)
    return i

result1 = processNumber(15)

result2 = processNumber(3)

count = countUp(0)

# End of generated code