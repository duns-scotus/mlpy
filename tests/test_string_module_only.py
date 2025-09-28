"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData, typeof

from mlpy.stdlib.string_bridge import string as ml_string

def main():
    print('=== Testing String Module Functions ===')
    test_text = 'Hello World'
    length = ml_string.length(test_text)
    print((str('String length: ') + str(ml_string.toString(length))))
    upper = ml_string.upper(test_text)
    print((str('Uppercase: ') + str(upper)))
    lower = ml_string.lower(test_text)
    print((str('Lowercase: ') + str(lower)))
    substring = ml_string.substring(test_text, 0, 5)
    print((str('Substring: ') + str(substring)))
    find_result = ml_string.find(test_text, 'o')
    print((str("Find 'o': ") + str(ml_string.toString(find_result))))
    contains = ml_string.contains(test_text, 'World')
    print((str("Contains 'World': ") + str(ml_string.toString(contains))))
    print('=== All String Module Functions Work ===')

main()

# End of generated code