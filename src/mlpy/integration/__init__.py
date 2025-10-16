"""ML Integration Toolkit for production-ready Python-ML integration.

This module provides tools for integrating ML code into Python applications:

- **AsyncMLExecutor**: Non-blocking ML execution with async/await
- **async_ml_execute()**: Convenience function for async ML execution
- **MLCallbackWrapper**: Wrap ML functions as Python callbacks
- **MLCallbackRegistry**: Manage ML callbacks for event-driven applications
- **ml_callback()**: Convenience function for creating ML callbacks

Example - Async Execution:
    ```python
    from mlpy.integration import async_ml_execute

    result = await async_ml_execute('result = 2 + 2;')
    print(result.value)  # 4
    ```

Example - ML as Callback:
    ```python
    from mlpy.integration import MLCallbackWrapper, ml_callback
    from mlpy.cli.repl import MLREPLSession

    session = MLREPLSession()
    session.execute_ml_line('function validate(x) { return x > 0; }')

    validator = ml_callback(session, 'validate')
    result = validator(42)  # true
    ```
"""

from mlpy.integration.async_executor import (
    AsyncMLExecutor,
    AsyncMLResult,
    async_ml_execute,
)

from mlpy.integration.ml_callback import (
    MLCallbackWrapper,
    MLCallbackRegistry,
    ml_callback,
)

__all__ = [
    "AsyncMLExecutor",
    "AsyncMLResult",
    "async_ml_execute",
    "MLCallbackWrapper",
    "MLCallbackRegistry",
    "ml_callback",
]

__version__ = "1.0.0"
