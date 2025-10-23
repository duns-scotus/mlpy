"""Pytest configuration and fixtures for stdlib unit tests."""

import pytest
from mlpy.stdlib.decorators import _MODULE_REGISTRY


@pytest.fixture(autouse=True)
def restore_module_registry():
    """Save and restore _MODULE_REGISTRY after each test to prevent pollution.

    This fixture automatically runs for every test in the stdlib test suite,
    ensuring that tests which modify _MODULE_REGISTRY (like test_decorators.py)
    don't affect other tests.
    """
    # Save original registry
    original_registry = _MODULE_REGISTRY.copy()

    yield  # Run the test

    # Restore original registry
    _MODULE_REGISTRY.clear()
    _MODULE_REGISTRY.update(original_registry)
