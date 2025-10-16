"""ML Integration Toolkit for production-ready Python-ML integration.

This module provides tools for integrating ML code into Python applications:

- **AsyncMLExecutor**: Non-blocking ML execution with async/await
- **async_ml_execute()**: Convenience function for async ML execution
- **MLCallbackWrapper**: Wrap ML functions as Python callbacks
- **MLCallbackRegistry**: Manage ML callbacks for event-driven applications

Example - Async Execution:
    ```python
    from mlpy.integration import async_ml_execute

    result = await async_ml_execute('result = 2 + 2;')
    print(result.value)  # 4
    ```

Example - ML as Callback:
    ```python
    from mlpy.integration import MLCallbackWrapper

    wrapper = MLCallbackWrapper('validate_input(data);')
    button.config(command=wrapper)
    ```
"""

from mlpy.integration.async_executor import (
    AsyncMLExecutor,
    AsyncMLResult,
    async_ml_execute,
)

__all__ = [
    "AsyncMLExecutor",
    "AsyncMLResult",
    "async_ml_execute",
]

__version__ = "1.0.0"
