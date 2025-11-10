"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

from mlpy.stdlib import args

from mlpy.stdlib import console

_safe_call(console.log, '=== Testing args Module ===')

_safe_call(console.log, '[Test 1] Create parser')

parser = _safe_call(args.create_parser, 'Test Tool', 'A test command-line tool')

if (_safe_call(builtin.typeof, parser) == 'object'):
    _safe_call(console.log, 'PASS: create_parser() returns object')
else:
    _safe_call(console.log, 'FAIL: create_parser() should return object')

_safe_call(console.log, '[Test 2] Add flag')

_safe_method_call(parser, 'add_flag', 'verbose', 'v', 'Enable verbose output')

_safe_call(console.log, 'PASS: add_flag() completed')

_safe_call(console.log, '[Test 3] Add flag without short name')

_safe_method_call(parser, 'add_flag', 'debug', None, 'Enable debug mode')

_safe_call(console.log, 'PASS: add_flag() with null short name completed')

_safe_call(console.log, '[Test 4] Add option')

_safe_method_call(parser, 'add_option', 'output', 'o', 'Output file', 'output.txt')

_safe_call(console.log, 'PASS: add_option() completed')

_safe_call(console.log, '[Test 5] Add option with null default')

_safe_method_call(parser, 'add_option', 'config', 'c', 'Config file', None)

_safe_call(console.log, 'PASS: add_option() with null default completed')

_safe_call(console.log, '[Test 6] Add required positional')

_safe_method_call(parser, 'add_positional', 'input', 'Input file', True)

_safe_call(console.log, 'PASS: add_positional() with required=true completed')

_safe_call(console.log, '[Test 7] Add optional positional')

_safe_method_call(parser, 'add_positional', 'extra', 'Extra files', False)

_safe_call(console.log, 'PASS: add_positional() with required=false completed')

_safe_call(console.log, '[Test 8] Parse long flag')

parser2 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser2, 'add_flag', 'verbose', 'v', 'Verbose')

parsed = _safe_method_call(parser2, 'parse', ['--verbose'])

if (_safe_method_call(parsed, 'get_bool', 'verbose') == True):
    _safe_call(console.log, 'PASS: Parsing long flag works')
else:
    _safe_call(console.log, 'FAIL: Long flag should be true')

_safe_call(console.log, '[Test 9] Parse short flag')

parser3 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser3, 'add_flag', 'verbose', 'v', 'Verbose')

parsed2 = _safe_method_call(parser3, 'parse', ['-v'])

if (_safe_method_call(parsed2, 'get_bool', 'verbose') == True):
    _safe_call(console.log, 'PASS: Parsing short flag works')
else:
    _safe_call(console.log, 'FAIL: Short flag should be true')

_safe_call(console.log, '[Test 10] Parse multiple short flags combined')

parser4 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser4, 'add_flag', 'verbose', 'v', 'Verbose')

_safe_method_call(parser4, 'add_flag', 'force', 'f', 'Force')

parsed3 = _safe_method_call(parser4, 'parse', ['-vf'])

if (_safe_method_call(parsed3, 'get_bool', 'verbose') == True):
    if (_safe_method_call(parsed3, 'get_bool', 'force') == True):
        _safe_call(console.log, 'PASS: Parsing combined short flags works')
    else:
        _safe_call(console.log, 'FAIL: Force flag should be true')
else:
    _safe_call(console.log, 'FAIL: Verbose flag should be true')

_safe_call(console.log, '[Test 11] Parse long option with value')

parser5 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser5, 'add_option', 'output', 'o', 'Output', 'default.txt')

parsed4 = _safe_method_call(parser5, 'parse', ['--output', 'custom.txt'])

if (_safe_method_call(parsed4, 'get', 'output') == 'custom.txt'):
    _safe_call(console.log, 'PASS: Parsing long option with value works')
else:
    _safe_call(console.log, 'FAIL: Output should be custom.txt')

_safe_call(console.log, '[Test 12] Parse short option with value')

parser6 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser6, 'add_option', 'output', 'o', 'Output', 'default.txt')

parsed5 = _safe_method_call(parser6, 'parse', ['-o', 'custom.txt'])

if (_safe_method_call(parsed5, 'get', 'output') == 'custom.txt'):
    _safe_call(console.log, 'PASS: Parsing short option with value works')
else:
    _safe_call(console.log, 'FAIL: Output should be custom.txt')

_safe_call(console.log, '[Test 13] Option uses default value')

parser7 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser7, 'add_option', 'output', 'o', 'Output', 'default.txt')

parsed6 = _safe_method_call(parser7, 'parse', [])

if (_safe_method_call(parsed6, 'get', 'output') == 'default.txt'):
    _safe_call(console.log, 'PASS: Default value used correctly')
else:
    _safe_call(console.log, 'FAIL: Output should be default.txt')

_safe_call(console.log, '[Test 14] Parse positional argument')

parser8 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser8, 'add_positional', 'input', 'Input file', True)

parsed7 = _safe_method_call(parser8, 'parse', ['file.txt'])

if (_safe_method_call(parsed7, 'get', 'input') == 'file.txt'):
    _safe_call(console.log, 'PASS: Parsing positional argument works')
else:
    _safe_call(console.log, 'FAIL: Input should be file.txt')

_safe_call(console.log, '[Test 15] Parse multiple positional arguments')

parser9 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser9, 'add_positional', 'input', 'Input file', True)

_safe_method_call(parser9, 'add_positional', 'output', 'Output file', False)

parsed8 = _safe_method_call(parser9, 'parse', ['input.txt', 'output.txt'])

if (_safe_method_call(parsed8, 'get', 'input') == 'input.txt'):
    if (_safe_method_call(parsed8, 'get', 'output') == 'output.txt'):
        _safe_call(console.log, 'PASS: Parsing multiple positionals works')
    else:
        _safe_call(console.log, 'FAIL: Output should be output.txt')
else:
    _safe_call(console.log, 'FAIL: Input should be input.txt')

_safe_call(console.log, '[Test 16] Missing optional positional')

parser10 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser10, 'add_positional', 'input', 'Input', True)

_safe_method_call(parser10, 'add_positional', 'output', 'Output', False)

parsed9 = _safe_method_call(parser10, 'parse', ['input.txt'])

if (_safe_method_call(parsed9, 'get', 'input') == 'input.txt'):
    if (_safe_method_call(parsed9, 'get', 'output') == None):
        _safe_call(console.log, 'PASS: Missing optional positional is null')
    else:
        _safe_call(console.log, 'FAIL: Optional positional should be null')
else:
    _safe_call(console.log, 'FAIL: Input should be input.txt')

_safe_call(console.log, '[Test 17] has() method')

parser11 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser11, 'add_flag', 'verbose', 'v', 'Verbose')

_safe_method_call(parser11, 'add_option', 'output', 'o', 'Output', 'out.txt')

parsed10 = _safe_method_call(parser11, 'parse', ['-v'])

if (_safe_method_call(parsed10, 'has', 'verbose') == True):
    if (_safe_method_call(parsed10, 'has', 'missing') == False):
        _safe_call(console.log, 'PASS: has() method works correctly')
    else:
        _safe_call(console.log, 'FAIL: has() should return false for missing')
else:
    _safe_call(console.log, 'FAIL: has() should return true for verbose')

_safe_call(console.log, '[Test 18] get() with default value')

parser12 = _safe_call(args.create_parser, 'Tool', 'Desc')

parsed11 = _safe_method_call(parser12, 'parse', [])

result = _safe_method_call(parsed11, 'get', 'missing', 'default_value')

if (result == 'default_value'):
    _safe_call(console.log, 'PASS: get() with default works')
else:
    _safe_call(console.log, 'FAIL: get() should return default_value')

_safe_call(console.log, '[Test 19] flags() method')

parser13 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser13, 'add_flag', 'verbose', 'v', 'Verbose')

_safe_method_call(parser13, 'add_flag', 'force', 'f', 'Force')

parsed12 = _safe_method_call(parser13, 'parse', ['-vf'])

all_flags = _safe_method_call(parsed12, 'flags')

if (_safe_call(builtin.typeof, all_flags) == 'object'):
    _safe_call(console.log, 'PASS: flags() returns dictionary')
else:
    _safe_call(console.log, 'FAIL: flags() should return object')

_safe_call(console.log, '[Test 20] options() method')

parser14 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser14, 'add_option', 'output', 'o', 'Output', 'out.txt')

_safe_method_call(parser14, 'add_option', 'format', 'f', 'Format', 'json')

parsed13 = _safe_method_call(parser14, 'parse', ['--output', 'custom.txt'])

all_options = _safe_method_call(parsed13, 'options')

if (_safe_call(builtin.typeof, all_options) == 'object'):
    _safe_call(console.log, 'PASS: options() returns dictionary')
else:
    _safe_call(console.log, 'FAIL: options() should return object')

_safe_call(console.log, '[Test 21] positionals() method')

parser15 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser15, 'add_positional', 'input', 'Input', True)

_safe_method_call(parser15, 'add_positional', 'output', 'Output', False)

parsed14 = _safe_method_call(parser15, 'parse', ['file1.txt', 'file2.txt'])

all_positionals = _safe_method_call(parsed14, 'positionals')

if (_safe_call(builtin.typeof, all_positionals) == 'array'):
    if (_safe_call(builtin.len, all_positionals) == 2):
        _safe_call(console.log, 'PASS: positionals() returns array with 2 elements')
    else:
        _safe_call(console.log, 'FAIL: positionals() should have 2 elements')
else:
    _safe_call(console.log, 'FAIL: positionals() should return array')

_safe_call(console.log, '[Test 22] help() generates help text')

parser16 = _safe_call(args.create_parser, 'My Tool', 'Does cool things')

_safe_method_call(parser16, 'add_flag', 'verbose', 'v', 'Verbose output')

_safe_method_call(parser16, 'add_option', 'output', 'o', 'Output file', 'out.txt')

_safe_method_call(parser16, 'add_positional', 'input', 'Input file', True)

help_text = _safe_method_call(parser16, 'help')

if (_safe_call(builtin.typeof, help_text) == 'string'):
    _safe_call(console.log, 'PASS: help() returns string')
else:
    _safe_call(console.log, 'FAIL: help() should return string')

_safe_call(console.log, '[Test 23] Help flag detection')

parser17 = _safe_call(args.create_parser, 'Tool', 'Desc')

parsed15 = _safe_method_call(parser17, 'parse', ['--help'])

if (_safe_method_call(parsed15, 'has', 'help') == True):
    _safe_call(console.log, 'PASS: --help flag detected')
else:
    _safe_call(console.log, 'FAIL: --help flag should be detected')

_safe_call(console.log, '[Test 24] Short help flag detection')

parser18 = _safe_call(args.create_parser, 'Tool', 'Desc')

parsed16 = _safe_method_call(parser18, 'parse', ['-h'])

if (_safe_method_call(parsed16, 'has', 'help') == True):
    _safe_call(console.log, 'PASS: -h flag detected')
else:
    _safe_call(console.log, 'FAIL: -h flag should be detected')

_safe_call(console.log, '[Test 25] Complex argument parsing')

parser19 = _safe_call(args.create_parser, 'Data Processor', 'Process CSV files')

_safe_method_call(parser19, 'add_flag', 'verbose', 'v', 'Verbose output')

_safe_method_call(parser19, 'add_flag', 'force', 'f', 'Force overwrite')

_safe_method_call(parser19, 'add_option', 'output', 'o', 'Output file', 'output.csv')

_safe_method_call(parser19, 'add_option', 'format', None, 'Format', 'csv')

_safe_method_call(parser19, 'add_positional', 'input', 'Input file', True)

parsed17 = _safe_method_call(parser19, 'parse', ['-vf', '--output', 'result.csv', '--format', 'json', 'data.csv'])

all_passed = True

if (_safe_method_call(parsed17, 'get_bool', 'verbose') != True):
    _safe_call(console.log, 'FAIL: verbose should be true')
    all_passed = False

if (_safe_method_call(parsed17, 'get_bool', 'force') != True):
    _safe_call(console.log, 'FAIL: force should be true')
    all_passed = False

if (_safe_method_call(parsed17, 'get', 'output') != 'result.csv'):
    _safe_call(console.log, 'FAIL: output should be result.csv')
    all_passed = False

if (_safe_method_call(parsed17, 'get', 'format') != 'json'):
    _safe_call(console.log, 'FAIL: format should be json')
    all_passed = False

if (_safe_method_call(parsed17, 'get', 'input') != 'data.csv'):
    _safe_call(console.log, 'FAIL: input should be data.csv')
    all_passed = False

if all_passed:
    _safe_call(console.log, 'PASS: Complex argument parsing works')

_safe_call(console.log, '[Test 26] Error handling - missing required positional')

parser20 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser20, 'add_positional', 'input', 'Input file', True)

try:
    _safe_method_call(parser20, 'parse', [])
    _safe_call(console.log, 'FAIL: Should have thrown error for missing required positional')
except Exception as error:
    _safe_call(console.log, 'PASS: Error thrown for missing required positional')
finally:
    pass

_safe_call(console.log, '[Test 27] Error handling - unknown option')

parser21 = _safe_call(args.create_parser, 'Tool', 'Desc')

try:
    _safe_method_call(parser21, 'parse', ['--unknown'])
    _safe_call(console.log, 'FAIL: Should have thrown error for unknown option')
except Exception as error:
    _safe_call(console.log, 'PASS: Error thrown for unknown option')
finally:
    pass

_safe_call(console.log, '[Test 28] Error handling - option without value')

parser22 = _safe_call(args.create_parser, 'Tool', 'Desc')

_safe_method_call(parser22, 'add_option', 'output', 'o', 'Output', 'out.txt')

try:
    _safe_method_call(parser22, 'parse', ['--output'])
    _safe_call(console.log, 'FAIL: Should have thrown error for option without value')
except Exception as error:
    _safe_call(console.log, 'PASS: Error thrown for option without value')
finally:
    pass

_safe_call(console.log, '=== All args module tests passed! ===')

# End of generated code