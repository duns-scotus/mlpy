"""Integration testing utilities for the ML Integration Toolkit.

This module provides comprehensive testing infrastructure for ML integration:

- **IntegrationTestHelper**: Utilities for testing async execution and callbacks
- **MockAsyncExecutor**: Mock executor for testing
- **MockREPLSession**: Mock REPL session for testing
- **MockCapabilityManager**: Mock capability manager for testing
- **PerformanceTester**: Performance benchmarking utilities

Example - Testing Async Execution:
    ```python
    from mlpy.integration.testing import IntegrationTestHelper

    helper = IntegrationTestHelper()
    await helper.assert_async_execution(
        "result = 2 + 2;",
        expected_result=4
    )
    helper.cleanup()
    ```

Example - Testing Callbacks:
    ```python
    session = helper.create_test_repl()
    session.execute_ml_line('function double(x) { return x * 2; }')

    helper.assert_callback_works(
        session,
        'double',
        (5,),
        expected_result=10
    )
    ```
"""

from mlpy.integration.testing.test_utilities import IntegrationTestHelper
from mlpy.integration.testing.mocks import (
    MockAsyncExecutor,
    MockREPLSession,
    MockCapabilityManager,
)
from mlpy.integration.testing.performance import PerformanceTester

__all__ = [
    "IntegrationTestHelper",
    "MockAsyncExecutor",
    "MockREPLSession",
    "MockCapabilityManager",
    "PerformanceTester",
]
