"""Async ML executor for non-blocking ML code execution.

Provides async/await interface for ML code execution using thread pool,
enabling integration with async frameworks like FastAPI, Flask, and GUI
applications without blocking the main thread.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from typing import Any, Optional, Dict
from dataclasses import dataclass
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class AsyncMLResult:
    """Result from async ML execution.

    Attributes:
        success: True if execution succeeded, False if error occurred
        value: Return value from ML code (None if no return value)
        error: Error message if execution failed (None if success)
        execution_time: Total execution time in seconds
        transpile_time: Time spent transpiling ML to Python
    """
    success: bool
    value: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    transpile_time: float = 0.0


class AsyncMLExecutor:
    """Async executor for ML code with thread pool.

    Enables non-blocking ML execution using Python's async/await syntax.
    ML code is transpiled and executed in background threads, allowing
    the main thread to continue processing other tasks.

    Example:
        ```python
        executor = AsyncMLExecutor(max_workers=4)

        # Execute ML code asynchronously
        result = await executor.execute('result = 2 + 2;')
        print(result.value)  # 4

        # With timeout
        result = await executor.execute(
            'result = expensive_calculation();',
            timeout=5.0
        )

        # Cleanup
        executor.shutdown()
        ```

    Args:
        max_workers: Maximum number of concurrent ML execution threads
        strict_security: Enable strict security analysis (default: False for flexibility)
        python_extension_paths: List of directories to search for custom modules
    """

    def __init__(
        self,
        max_workers: int = 4,
        strict_security: bool = False,  # Default to False for flexible integration
        python_extension_paths: Optional[list[str]] = None
    ):
        self.max_workers = max_workers
        self.strict_security = strict_security
        self.python_extension_paths = python_extension_paths or []

        # Thread pool for ML execution
        self._executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="ml_executor"
        )

        # Transpiler instance (reused for performance)
        # Use REPL mode to allow external context variables
        from mlpy.ml.transpiler import MLTranspiler
        self._transpiler = MLTranspiler(
            repl_mode=True,  # Allow variables from context
            python_extension_paths=self.python_extension_paths
        )

        logger.info(
            f"AsyncMLExecutor initialized with {max_workers} workers, "
            f"strict_security={strict_security}"
        )

    async def execute(
        self,
        ml_code: str,
        timeout: Optional[float] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> AsyncMLResult:
        """Execute ML code asynchronously.

        Transpiles and executes ML code in a background thread, returning
        an awaitable future that resolves when execution completes.

        Args:
            ml_code: ML source code to execute
            timeout: Timeout in seconds (None = no timeout)
            context: Additional context variables for ML namespace

        Returns:
            AsyncMLResult with execution results

        Example:
            ```python
            result = await executor.execute('result = 2 + 2;')
            if result.success:
                print(f"Result: {result.value}")
            else:
                print(f"Error: {result.error}")
            ```
        """
        loop = asyncio.get_event_loop()

        # Submit to thread pool
        future = loop.run_in_executor(
            self._executor,
            self._execute_sync,
            ml_code,
            context
        )

        try:
            # Wait with timeout
            if timeout:
                result = await asyncio.wait_for(future, timeout=timeout)
            else:
                result = await future

            return result

        except asyncio.TimeoutError:
            logger.error(f"ML execution timeout after {timeout}s")
            return AsyncMLResult(
                success=False,
                error=f"Execution timeout after {timeout} seconds"
            )
        except Exception as e:
            logger.exception(f"Async ML execution error: {e}")
            return AsyncMLResult(
                success=False,
                error=f"Async execution error: {str(e)}"
            )

    def _execute_sync(
        self,
        ml_code: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AsyncMLResult:
        """Synchronous execution in background thread.

        This method runs in a background thread and performs the actual
        transpilation and execution of ML code.

        Args:
            ml_code: ML source code to execute
            context: Additional context variables for ML namespace

        Returns:
            AsyncMLResult with execution results
        """
        start_time = time.perf_counter()

        try:
            # Transpile ML code
            transpile_start = time.perf_counter()
            python_code, issues, source_map = self._transpiler.transpile_to_python(
                ml_code,
                strict_security=self.strict_security,
                generate_source_maps=True
            )
            transpile_time = time.perf_counter() - transpile_start

            # Check for critical security issues (only fail on ERROR level)
            critical_issues = [issue for issue in issues if hasattr(issue, 'severity') and issue.severity == 'ERROR']
            if critical_issues:
                error_messages = [str(issue) for issue in critical_issues]
                return AsyncMLResult(
                    success=False,
                    error=f"Security issues: {'; '.join(error_messages)}",
                    transpile_time=transpile_time
                )

            if not python_code:
                # Log issues for debugging
                if issues:
                    issue_details = [f"{issue.severity}: {issue.message}" if hasattr(issue, 'severity') else str(issue) for issue in issues]
                    logger.warning(f"Transpilation produced no code. Issues: {'; '.join(issue_details)}")

                return AsyncMLResult(
                    success=False,
                    error="Transpilation failed: no Python code generated",
                    transpile_time=transpile_time
                )

            # Execute in isolated namespace
            namespace = context.copy() if context else {}
            exec(python_code, namespace)

            execution_time = time.perf_counter() - start_time

            # Extract return value (convention: use 'result' variable)
            return_value = namespace.get('result', None)

            return AsyncMLResult(
                success=True,
                value=return_value,
                execution_time=execution_time,
                transpile_time=transpile_time
            )

        except Exception as e:
            execution_time = time.perf_counter() - start_time
            logger.exception(f"ML execution error: {e}")

            return AsyncMLResult(
                success=False,
                error=str(e),
                execution_time=execution_time
            )

    def shutdown(self, wait: bool = True):
        """Shutdown the executor.

        Args:
            wait: If True, wait for pending tasks to complete before shutdown
        """
        logger.info("Shutting down AsyncMLExecutor")
        self._executor.shutdown(wait=wait)


# Convenience function for simple async execution
async def async_ml_execute(
    ml_code: str,
    timeout: Optional[float] = None,
    context: Optional[Dict[str, Any]] = None,
    strict_security: bool = False,
    python_extension_paths: Optional[list[str]] = None
) -> AsyncMLResult:
    """Convenience function for async ML execution.

    Creates a single-use AsyncMLExecutor and executes the ML code.
    For repeated executions, create an AsyncMLExecutor instance directly
    for better performance.

    Args:
        ml_code: ML source code to execute
        timeout: Timeout in seconds (None = no timeout)
        context: Additional context variables for ML namespace
        strict_security: Enable strict security analysis (default: False)
        python_extension_paths: List of directories to search for custom modules

    Returns:
        AsyncMLResult with execution results

    Example:
        ```python
        from mlpy.integration import async_ml_execute

        # Simple execution
        result = await async_ml_execute('result = 2 + 2;')
        print(result.value)  # 4

        # With timeout
        result = await async_ml_execute(
            'result = expensive_calculation();',
            timeout=5.0
        )

        # With custom modules
        result = await async_ml_execute(
            'import custom; result = custom.process(data);',
            python_extension_paths=['/path/to/modules']
        )
        ```
    """
    executor = AsyncMLExecutor(
        max_workers=1,
        strict_security=strict_security,
        python_extension_paths=python_extension_paths
    )

    try:
        result = await executor.execute(ml_code, timeout=timeout, context=context)
        return result
    finally:
        executor.shutdown(wait=False)
