"""Pytest configuration for integration testing tests."""
import pytest


@pytest.fixture
def anyio_backend():
    """Use asyncio backend only for tests.

    Our integration toolkit uses ThreadPoolExecutor which is incompatible
    with trio's strict async model. We only test with asyncio backend.
    """
    return "asyncio"
