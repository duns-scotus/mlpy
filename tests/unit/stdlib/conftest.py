"""Pytest configuration and fixtures for stdlib unit tests."""

import pytest
import sys
from mlpy.stdlib.decorators import _MODULE_REGISTRY


@pytest.fixture(autouse=True)
def restore_module_registry():
    """Save and restore _MODULE_REGISTRY after each test to prevent pollution.

    This fixture automatically runs for every test in the stdlib test suite,
    ensuring that tests which modify _MODULE_REGISTRY (like test_decorators.py)
    don't affect other tests.

    Also cleans up sys.modules to prevent Python's module caching from
    interfering with module reload tests.
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
    _MODULE_REGISTRY.clear()
    _MODULE_REGISTRY.update(original_registry)

    # Clean up test modules from sys.modules
    for name in test_module_patterns:
        if name in sys.modules:
            # Only remove if it wasn't there originally or has changed
            if name not in original_modules:
                del sys.modules[name]
