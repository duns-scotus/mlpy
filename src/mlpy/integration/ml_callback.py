"""ML-as-Callback Bridge - Use ML functions as Python callables.

Enables ML functions to be used as native Python callbacks for:
- GUI event handlers (Tkinter, PyQt, etc.)
- Web framework routes (Flask, FastAPI)
- Event-driven systems
- Any Python code expecting callables

The bridge handles argument marshaling, error handling, and state management
automatically, making ML functions behave like native Python functions.
"""

from typing import Any, Optional, Callable, Dict
import json
import logging

from mlpy.cli.repl import MLREPLSession, REPLResult

logger = logging.getLogger(__name__)


class MLCallbackWrapper:
    """Wrapper that makes ML functions callable as Python callbacks.

    This class creates a Python callable from an ML function, handling all the
    complexity of argument marshaling, execution, and error handling.

    Example:
        ```python
        # Create REPL session and load ML function
        session = MLREPLSession(security_enabled=False)
        session.execute_ml_line('''
            function validate_email(email) {
                if (typeof(email) != "string") {
                    return {valid: false, error: "Email must be a string"};
                }

                // Simple validation
                has_at = false;
                i = 0;
                while (i < len(email)) {
                    if (email[i] == "@") {
                        has_at = true;
                    }
                    i = i + 1;
                }

                return {valid: has_at, error: has_at ? null : "Missing @"};
            }
        ''')

        # Create callback wrapper
        validator = MLCallbackWrapper(session, "validate_email")

        # Use as Python function
        result = validator("test@example.com")
        print(result)  # {'valid': True, 'error': None}
        ```
    """

    def __init__(
        self,
        ml_session: MLREPLSession,
        function_name: str,
        error_handler: Optional[Callable[[Exception], Any]] = None,
        default_return: Any = None
    ):
        """Create ML callback wrapper.

        Args:
            ml_session: MLREPLSession instance with ML function loaded
            function_name: Name of ML function to call
            error_handler: Optional error handler function (receives Exception, returns fallback value)
            default_return: Default value to return on error if no error_handler provided

        Example:
            ```python
            def on_error(exc):
                logger.error(f"ML callback failed: {exc}")
                return {"error": str(exc)}

            callback = MLCallbackWrapper(session, "my_function", error_handler=on_error)
            ```
        """
        self.ml_session = ml_session
        self.function_name = function_name
        self.error_handler = error_handler
        self.default_return = default_return

        # Verify function exists
        if function_name not in self.ml_session.python_namespace:
            logger.warning(
                f"Function '{function_name}' not found in session namespace. "
                "Make sure the function is defined before creating the callback."
            )

    def __call__(self, *args, **kwargs) -> Any:
        """Call the ML function with Python arguments.

        Args:
            *args: Positional arguments to pass to ML function
            **kwargs: Keyword arguments (converted to object if ML function expects one)

        Returns:
            Return value from ML function

        Raises:
            RuntimeError: If ML function execution fails and no error_handler provided

        Example:
            ```python
            # Positional arguments
            result = callback(10, 20)

            # Keyword arguments (converted to object)
            result = callback(x=10, y=20)

            # Mixed
            result = callback(10, multiplier=2)
            ```
        """
        try:
            # Marshal arguments to ML format
            ml_args = self._marshal_arguments(*args, **kwargs)

            # Build ML function call (without assignment to get return value)
            ml_code = f"{self.function_name}({ml_args});"

            logger.debug(f"Executing ML callback: {ml_code}")

            # Execute via REPL session
            result = self.ml_session.execute_ml_line(ml_code)

            if result.success:
                return result.value
            else:
                raise RuntimeError(f"ML function failed: {result.error}")

        except Exception as e:
            logger.exception(f"ML callback error in '{self.function_name}': {e}")

            if self.error_handler:
                return self.error_handler(e)
            elif self.default_return is not None:
                return self.default_return
            else:
                raise

    def _marshal_arguments(self, *args, **kwargs) -> str:
        """Convert Python arguments to ML format.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            ML argument string

        Example:
            _marshal_arguments(42, "hello")          → '42, "hello"'
            _marshal_arguments(x=10, y=20)           → '{"x": 10, "y": 20}'
            _marshal_arguments(10, options={'a': 1}) → '10, {"a": 1}'
        """
        ml_args = []

        # Convert positional args
        for arg in args:
            ml_args.append(self._python_to_ml(arg))

        # Handle keyword arguments
        # If there are kwargs, append them as a final object argument
        if kwargs:
            ml_args.append(self._python_to_ml(kwargs))

        return ", ".join(ml_args)

    def _python_to_ml(self, value: Any) -> str:
        """Convert Python value to ML representation.

        Args:
            value: Python value to convert

        Returns:
            ML-compatible string representation

        Example:
            _python_to_ml("hello")    → '"hello"'
            _python_to_ml(True)       → 'true'
            _python_to_ml(42)         → '42'
            _python_to_ml([1, 2, 3])  → '[1, 2, 3]'
            _python_to_ml({'x': 10})  → '{"x": 10}'
        """
        if isinstance(value, str):
            return json.dumps(value)  # Handles escaping
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, dict):
            return json.dumps(value)  # ML objects use JSON syntax
        elif isinstance(value, list):
            return json.dumps(value)  # ML arrays use JSON syntax
        elif value is None:
            return "null"
        else:
            # Try JSON serialization for other types
            try:
                return json.dumps(value)
            except (TypeError, ValueError):
                # Fallback: convert to string and quote
                return json.dumps(str(value))


class MLCallbackRegistry:
    """Registry for managing multiple ML callbacks.

    Provides convenient storage and retrieval of ML callbacks by name,
    making it easy to manage multiple event handlers in one place.

    Example:
        ```python
        # Create registry
        session = MLREPLSession(security_enabled=False)
        registry = MLCallbackRegistry(session)

        # Load ML event handlers
        session.execute_ml_line('''
            function on_click(data) {
                print("Button clicked:", data);
                return {status: "handled"};
            }

            function on_submit(form_data) {
                // Validate form
                if (!form_data.name) {
                    return {valid: false, error: "Name required"};
                }
                return {valid: true};
            }

            function on_validate(text) {
                return {valid: len(text) >= 3};
            }
        ''')

        # Register callbacks
        registry.register("click", "on_click")
        registry.register("submit", "on_submit")
        registry.register("validate", "on_validate")

        # Use callbacks
        button.config(command=lambda: registry["click"]({"button": "OK"}))
        form.bind("<Submit>", lambda e: registry["submit"](form.get_data()))
        ```
    """

    def __init__(self, ml_session: MLREPLSession):
        """Create callback registry.

        Args:
            ml_session: MLREPLSession instance with ML functions loaded

        Example:
            ```python
            session = MLREPLSession(security_enabled=False)
            registry = MLCallbackRegistry(session)
            ```
        """
        self.ml_session = ml_session
        self._callbacks: Dict[str, MLCallbackWrapper] = {}

    def register(
        self,
        name: str,
        function_name: str,
        error_handler: Optional[Callable[[Exception], Any]] = None,
        default_return: Any = None
    ) -> MLCallbackWrapper:
        """Register a named callback.

        Args:
            name: Registry name for this callback (for retrieval)
            function_name: ML function name to wrap
            error_handler: Optional error handler
            default_return: Default return value on error

        Returns:
            The created MLCallbackWrapper

        Example:
            ```python
            # Register with custom error handler
            def handle_error(exc):
                logger.error(f"Validation failed: {exc}")
                return {"valid": False, "error": str(exc)}

            registry.register(
                "validate",
                "validate_input",
                error_handler=handle_error
            )

            # Register with default return
            registry.register(
                "calculate",
                "calculate_result",
                default_return=0
            )
            ```
        """
        callback = MLCallbackWrapper(
            self.ml_session,
            function_name,
            error_handler=error_handler,
            default_return=default_return
        )
        self._callbacks[name] = callback

        logger.debug(f"Registered ML callback: '{name}' -> '{function_name}'")

        return callback

    def get(self, name: str) -> Optional[MLCallbackWrapper]:
        """Get registered callback by name.

        Args:
            name: Callback name

        Returns:
            MLCallbackWrapper if found, None otherwise

        Example:
            ```python
            callback = registry.get("validate")
            if callback:
                result = callback("test@example.com")
            ```
        """
        return self._callbacks.get(name)

    def __getitem__(self, name: str) -> MLCallbackWrapper:
        """Dictionary-style access to callbacks.

        Args:
            name: Callback name

        Returns:
            MLCallbackWrapper

        Raises:
            KeyError: If callback not found

        Example:
            ```python
            # Direct access
            result = registry["validate"]("test@example.com")

            # Use in button command
            button.config(command=registry["on_click"])
            ```
        """
        if name not in self._callbacks:
            raise KeyError(f"Callback '{name}' not found in registry")
        return self._callbacks[name]

    def __contains__(self, name: str) -> bool:
        """Check if callback is registered.

        Args:
            name: Callback name

        Returns:
            True if callback exists

        Example:
            ```python
            if "validate" in registry:
                result = registry["validate"](data)
            ```
        """
        return name in self._callbacks

    def list_callbacks(self) -> list[str]:
        """Get list of all registered callback names.

        Returns:
            List of callback names (sorted alphabetically)

        Example:
            ```python
            print("Available callbacks:", registry.list_callbacks())
            # Output: Available callbacks: ['click', 'submit', 'validate']
            ```
        """
        return sorted(self._callbacks.keys())

    def remove(self, name: str) -> bool:
        """Remove a registered callback.

        Args:
            name: Callback name to remove

        Returns:
            True if callback was removed, False if not found

        Example:
            ```python
            if registry.remove("old_callback"):
                print("Callback removed")
            ```
        """
        if name in self._callbacks:
            del self._callbacks[name]
            logger.debug(f"Removed ML callback: '{name}'")
            return True
        return False

    def clear(self):
        """Remove all registered callbacks.

        Example:
            ```python
            registry.clear()
            ```
        """
        self._callbacks.clear()
        logger.debug("Cleared all ML callbacks")


# Convenience function
def ml_callback(
    ml_session: MLREPLSession,
    function_name: str,
    error_handler: Optional[Callable[[Exception], Any]] = None,
    default_return: Any = None
) -> MLCallbackWrapper:
    """Create a Python callable from ML function.

    Convenience function for quick callback creation without a registry.

    Args:
        ml_session: REPL session with ML function loaded
        function_name: Name of ML function
        error_handler: Optional error handler
        default_return: Default return value on error

    Returns:
        Callable wrapper for ML function

    Example:
        ```python
        from mlpy.cli.repl import MLREPLSession
        from mlpy.integration.ml_callback import ml_callback

        # Create session and load ML function
        session = MLREPLSession(security_enabled=False)
        session.execute_ml_line('''
            function validate_email(email) {
                // Validation logic
                return email.includes("@");
            }
        ''')

        # Create callback
        validator = ml_callback(session, "validate_email")

        # Use as Python function
        is_valid = validator("test@example.com")  # Returns true/false
        ```
    """
    return MLCallbackWrapper(
        ml_session,
        function_name,
        error_handler=error_handler,
        default_return=default_return
    )
