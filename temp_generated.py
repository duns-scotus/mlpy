"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData, typeof

from mlpy.ml.errors.exceptions import MLUserException

def test_basic_throw():
    result = None
    try:
        raise MLUserException(None)
    except Exception as e:
        result = 'caught'
    return result

def test_detailed_throw():
    result = None
    try:
        raise MLUserException(None)
    except Exception as e:
        result = 'error_caught'
    return result

def test_finally_basic():
    executed = False
    try:
        x = 10
    finally:
        executed = True
    return executed

def test_finally_with_exception():
    cleanup = False
    try:
        raise MLUserException(None)
    except Exception as e:
        pass
    finally:
        cleanup = True
    return cleanup

def test_complete_exception():
    results = {}
    results['caught'] = False
    results['finally_run'] = False
    try:
        raise MLUserException(None)
    except Exception as e:
        results['caught'] = True
    finally:
        results['finally_run'] = True
    return results

def test_finally_no_exception():
    count = 0
    try:
        count = (count + 1)
    finally:
        count = (count + 10)
    return count

def test_nested_finally():
    outer = False
    inner = False
    try:
        try:
            x = 5
        finally:
            inner = True
    finally:
        outer = True
    results = {}
    results['inner'] = inner
    results['outer'] = outer
    return results

def divide(a, b):
    if (b == 0):
        raise MLUserException(None)
    return (a / b)

def test_conditional_throw():
    result = None
    try:
        result = divide(10, 0)
    except Exception as e:
        result = 'error'
    return result

def test_finally_with_return():
    value = 0
    try:
        value = 10
        return value
    finally:
        value = 20
    return value

def test_multiple_operations():
    results = []
    try:
        x = 10
    except Exception as e:
        results = (results + ['error1'])
    finally:
        results = (results + ['finally1'])
    try:
        raise MLUserException(None)
    except Exception as e:
        results = (results + ['error2'])
    finally:
        results = (results + ['finally2'])
    return results

def test_finally_variable_update():
    counter = 0
    status = 'initial'
    try:
        counter = (counter + 5)
        status = 'try'
    finally:
        counter = (counter + 3)
        status = 'finally'
    results = {}
    results['counter'] = counter
    results['status'] = status
    return results

def test_throw_in_loop():
    results = []
    i = 0
    while (i < 5):
        try:
            if (i == 3):
                raise MLUserException(None)
            results = (results + [i])
        except Exception as e:
            results = (results + ['error'])
        i = (i + 1)
    return results

def test_finally_cleanup():
    resource_open = False
    resource_closed = False
    try:
        resource_open = True
        raise MLUserException(None)
    except Exception as e:
        pass
    finally:
        resource_closed = True
    results = {}
    results['opened'] = resource_open
    results['closed'] = resource_closed
    return results

def test_empty_finally():
    value = 10
    try:
        value = (value + 5)
    return value

def test_complex_error():
    result = None
    try:
        raise MLUserException(None)
    except Exception as e:
        result = 'caught_complex'
    return result

def main():
    results = {}
    results['basic_throw'] = test_basic_throw()
    results['detailed_throw'] = test_detailed_throw()
    results['finally_basic'] = test_finally_basic()
    results['finally_exception'] = test_finally_with_exception()
    results['complete'] = test_complete_exception()
    results['finally_no_exc'] = test_finally_no_exception()
    results['nested_finally'] = test_nested_finally()
    results['conditional_throw'] = test_conditional_throw()
    results['finally_return'] = test_finally_with_return()
    results['multiple_ops'] = test_multiple_operations()
    results['var_update'] = test_finally_variable_update()
    results['throw_loop'] = test_throw_in_loop()
    results['cleanup'] = test_finally_cleanup()
    results['empty_finally'] = test_empty_finally()
    results['complex_error'] = test_complex_error()
    return results

test_results = main()

# End of generated code