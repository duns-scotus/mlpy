"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib import console, getCurrentTime, processData

def test():
    x = 15
    if (x < 10):
        return 'small'
    elif (x < 20):
        return 'medium'
    else:
        return 'large'

def main():
    result = test()
    print((str('Result: ') + str(result)))
    return 0

# End of generated code