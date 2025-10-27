"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.builtin import builtin

from mlpy.stdlib import console

_safe_call(builtin.print, 'Test 1: requiredCapabilities with builtin functions')

caps = _safe_call(builtin.requiredCapabilities, builtin.print)

_safe_call(builtin.print, (str('print requires: ') + str(_safe_call(builtin.str, caps))))

if (_safe_call(builtin.len, caps) == 0):
    _safe_call(builtin.print, '  [PASS] print requires no capabilities')
else:
    _safe_call(builtin.print, '  [FAIL] Expected empty list')

caps = _safe_call(builtin.requiredCapabilities, builtin.typeof)

_safe_call(builtin.print, (str('typeof requires: ') + str(_safe_call(builtin.str, caps))))

if (_safe_call(builtin.len, caps) == 0):
    _safe_call(builtin.print, '  [PASS] typeof requires no capabilities')
else:
    _safe_call(builtin.print, '  [FAIL] Expected empty list')

caps = _safe_call(builtin.requiredCapabilities, builtin.len)

_safe_call(builtin.print, (str('len requires: ') + str(_safe_call(builtin.str, caps))))

if (_safe_call(builtin.len, caps) == 0):
    _safe_call(builtin.print, '  [PASS] len requires no capabilities')
else:
    _safe_call(builtin.print, '  [FAIL] Expected empty list')

_safe_call(builtin.print, '\\nTest 2: requiredCapabilities with console.log')

caps = _safe_call(builtin.requiredCapabilities, console.log)

_safe_call(builtin.print, (str('console.log requires: ') + str(_safe_call(builtin.str, caps))))

if (_safe_call(builtin.len, caps) == 0):
    _safe_call(builtin.print, '  [PASS] console.log requires no capabilities')
else:
    _safe_call(builtin.print, '  [FAIL] Expected empty list')

_safe_call(builtin.print, '\\nTest 3: help() includes capability information')

helpText = _safe_call(builtin.help, builtin.print)

_safe_call(builtin.print, 'help(print):')

_safe_call(builtin.print, helpText)

if (_safe_call(builtin.len, helpText) > 0):
    _safe_call(builtin.print, '  [PASS] help returns information for print')
else:
    _safe_call(builtin.print, '  [FAIL] Expected help text for print')

_safe_call(builtin.print, '\\nTest 4: help() for console.log')

helpText = _safe_call(builtin.help, console.log)

_safe_call(builtin.print, 'help(console.log):')

_safe_call(builtin.print, helpText)

if (_safe_call(builtin.len, helpText) > 0):
    _safe_call(builtin.print, '  [PASS] help returns information for console.log')
else:
    _safe_call(builtin.print, '  [FAIL] Expected help text for console.log')

_safe_call(builtin.print, '\\nTest 5: Defensive programming pattern')

def canCall(func):
    required = _safe_call(builtin.requiredCapabilities, func)
    for cap in required:
        if (not _safe_call(builtin.hasCapability, cap)):
            return False
    return True

if canCall(console.log):
    _safe_call(builtin.print, '  [PASS] canCall(console.log) returns true')
else:
    _safe_call(builtin.print, '  [FAIL] Expected canCall(console.log) to return true')

if canCall(builtin.print):
    _safe_call(builtin.print, '  [PASS] canCall(print) returns true')
else:
    _safe_call(builtin.print, '  [FAIL] Expected canCall(print) to return true')

_safe_call(builtin.print, '\\nTest 6: Combined usage pattern')

def checkFunctionAccess(func, funcName):
    required = _safe_call(builtin.requiredCapabilities, func)
    if (_safe_call(builtin.len, required) == 0):
        _safe_call(builtin.print, (str(funcName) + str(' requires no capabilities - always available')))
        return True
    _safe_call(builtin.print, (str((str(funcName) + str(' requires capabilities: '))) + str(_safe_call(builtin.str, required))))
    missing = []
    for cap in required:
        if _safe_call(builtin.hasCapability, cap):
            _safe_call(builtin.print, (str('  + Have ') + str(cap)))
        else:
            _safe_call(builtin.print, (str('  - Missing ') + str(cap)))
            missing = (missing + [cap])
    return (_safe_call(builtin.len, missing) == 0)

if checkFunctionAccess(console.log, 'console.log'):
    _safe_call(builtin.print, '  [PASS] console.log is accessible')
else:
    _safe_call(builtin.print, '  [FAIL] Expected console.log to be accessible')

if checkFunctionAccess(builtin.typeof, 'typeof'):
    _safe_call(builtin.print, '  [PASS] typeof is accessible')
else:
    _safe_call(builtin.print, '  [FAIL] Expected typeof to be accessible')

_safe_call(builtin.print, '\\nTest 7: Custom function capability check')

def myCustomFunc(x):
    return (x + 1)

caps = _safe_call(builtin.requiredCapabilities, myCustomFunc)

_safe_call(builtin.print, (str('myCustomFunc requires: ') + str(_safe_call(builtin.str, caps))))

if (_safe_call(builtin.len, caps) == 0):
    _safe_call(builtin.print, '  [PASS] Custom function has no declared capabilities')
else:
    _safe_call(builtin.print, '  [FAIL] Expected empty list for custom function')

_safe_call(builtin.print, '\\nTest 8: Feature detection pattern')

def checkAvailableFeatures():
    features = []
    if (_safe_call(builtin.len, _safe_call(builtin.requiredCapabilities, builtin.print)) == 0):
        features = (features + ['printing'])
    if (_safe_call(builtin.len, _safe_call(builtin.requiredCapabilities, builtin.typeof)) == 0):
        features = (features + ['type_checking'])
    if (_safe_call(builtin.len, _safe_call(builtin.requiredCapabilities, console.log)) == 0):
        features = (features + ['console_logging'])
    return features

available = checkAvailableFeatures()

_safe_call(builtin.print, (str('Available features: ') + str(_safe_call(builtin.str, available))))

if (_safe_call(builtin.len, available) >= 3):
    _safe_call(builtin.print, '  [PASS] Feature detection found expected features')
else:
    _safe_call(builtin.print, '  [FAIL] Expected at least 3 available features')

_safe_call(builtin.print, '\\n========================================')

_safe_call(builtin.print, 'All capability introspection tests completed!')

_safe_call(builtin.print, '========================================')

# End of generated code