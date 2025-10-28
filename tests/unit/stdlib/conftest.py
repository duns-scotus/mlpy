"""Pytest configuration and fixtures for stdlib unit tests."""

import pytest
import sys
from mlpy.stdlib.decorators import _MODULE_REGISTRY

# IMPORTANT: Import all stdlib modules to ensure they're registered in _MODULE_REGISTRY
# before any tests run. This prevents test pollution issues when running full test suite.
import mlpy.stdlib.builtin
import mlpy.stdlib.console_bridge
import mlpy.stdlib.datetime_bridge
import mlpy.stdlib.file_bridge
import mlpy.stdlib.functional_bridge
import mlpy.stdlib.http_bridge
import mlpy.stdlib.json_bridge
import mlpy.stdlib.math_bridge
import mlpy.stdlib.path_bridge
import mlpy.stdlib.random_bridge
import mlpy.stdlib.regex_bridge
import mlpy.stdlib.collections_bridge


@pytest.fixture(autouse=True)
def restore_module_registry():
    """Save and restore _MODULE_REGISTRY after each test to prevent pollution.

    This fixture automatically runs for every test in the stdlib test suite,
    ensuring that tests which modify _MODULE_REGISTRY (like test_decorators.py)
    don't affect other tests.

    Also cleans up sys.modules to prevent Python's module caching from
    interfering with module reload tests.

    NOTE: Standard library modules (console, math, etc.) are NOT cleaned up
    because their registration tests expect them to remain registered.
    """
    # Save original registry
    original_registry = _MODULE_REGISTRY.copy()

    # Save modules we might need to clean up
    test_module_patterns = ['test', 'testmod', 'secure', 'mixed', 'registered_mod',
                            'funcmod', 'classmod', 'mixedmod', 'getmod']
    original_modules = {name: sys.modules.get(name) for name in test_module_patterns
                       if name in sys.modules}

    yield  # Run the test

    # Restore original registry
    # Extract stdlib modules from the ORIGINAL registry (before test ran)
    # Standard library modules: builtin, console, datetime, functional, math, random, regex, etc.
    stdlib_modules = {name: cls for name, cls in original_registry.items()
                     if not any(name.startswith(pattern) for pattern in test_module_patterns)}

    _MODULE_REGISTRY.clear()
    _MODULE_REGISTRY.update(stdlib_modules)

    # Also restore any test modules that were there originally
    for name, cls in original_registry.items():
        if any(name.startswith(pattern) for pattern in test_module_patterns):
            _MODULE_REGISTRY[name] = cls

    # Clean up test modules from sys.modules
    for name in test_module_patterns:
        if name in sys.modules:
            # Only remove if it wasn't there originally or has changed
            if name not in original_modules:
                del sys.modules[name]
