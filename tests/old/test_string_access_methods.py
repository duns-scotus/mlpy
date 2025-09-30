"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData, typeof

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length

from mlpy.stdlib.string_bridge import string as ml_string

def main():
    print('=== Testing String Access Methods ===')
    test_text = 'Hello World'
    print('Testing direct property access:')
    try:
        direct_length = _safe_attr_access(test_text, 'length')
        print((str('Direct length access: ') + str(ml_string.toString(direct_length))))
    except error:
        print((str('Direct length access FAILED: ') + str(ml_string.toString(error))))
    print('Testing module function access:')
    try:
        module_length = ml_string.length(test_text)
        print((str('Module length access: ') + str(ml_string.toString(module_length))))
    except error:
        print((str('Module length access FAILED: ') + str(ml_string.toString(error))))
    print('Testing direct method calls:')
    try:
        direct_upper = _safe_attr_access(test_text, 'toUpperCase')()
        print((str('Direct toUpperCase: ') + str(direct_upper)))
    except error:
        print((str('Direct toUpperCase FAILED: ') + str(ml_string.toString(error))))
    print('Testing module method calls:')
    try:
        module_upper = ml_string.upper(test_text)
        print((str('Module upper: ') + str(module_upper)))
    except error:
        print((str('Module upper FAILED: ') + str(ml_string.toString(error))))
    print('Testing substring operations:')
    try:
        direct_sub = _safe_attr_access(test_text, 'substring')(0, 5)
        print((str('Direct substring: ') + str(direct_sub)))
    except error:
        print((str('Direct substring FAILED: ') + str(ml_string.toString(error))))
    try:
        module_sub = ml_string.substring(test_text, 0, 5)
        print((str('Module substring: ') + str(module_sub)))
    except error:
        print((str('Module substring FAILED: ') + str(ml_string.toString(error))))
    print('Testing indexOf operations:')
    try:
        direct_index = _safe_attr_access(test_text, 'indexOf')('o')
        print((str('Direct indexOf: ') + str(ml_string.toString(direct_index))))
    except error:
        print((str('Direct indexOf FAILED: ') + str(ml_string.toString(error))))
    try:
        module_index = ml_string.find(test_text, 'o')
        print((str('Module find: ') + str(ml_string.toString(module_index))))
    except error:
        print((str('Module find FAILED: ') + str(ml_string.toString(error))))
    print('=== String Access Methods Test Complete ===')

main()

# End of generated code