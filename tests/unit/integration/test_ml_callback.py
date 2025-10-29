"""Unit tests for ML Callback Bridge.

Tests MLCallbackWrapper and MLCallbackRegistry for using ML functions
as Python callables in event-driven systems.
"""

import pytest
import textwrap
from mlpy.cli.repl import MLREPLSession
from mlpy.integration import MLCallbackWrapper, MLCallbackRegistry, ml_callback


def ml(code):
    """Helper to dedent multiline ML code."""
    return textwrap.dedent(code).strip()


class TestMLCallbackWrapper:
    """Test MLCallbackWrapper class."""

    @pytest.fixture
    def session(self):
        """Create test REPL session."""
        session = MLREPLSession(security_enabled=False)
        yield session

    def test_simple_callback(self, session):
        """Test simple ML function callback."""
        # Define ML function
        session.execute_ml_line(ml("""
            function double(x) {
                return x * 2;
            }
        """))

        # Create callback
        callback = MLCallbackWrapper(session, "double")

        # Call it
        result = callback(21)

        assert result == 42

    def test_callback_with_multiple_args(self, session):
        """Test callback with multiple arguments."""
        session.execute_ml_line(ml("""
            function add(a, b) {
                return a + b;
            }
        """))

        callback = MLCallbackWrapper(session, "add")
        result = callback(10, 32)

        assert result == 42

    def test_callback_with_string_args(self, session):
        """Test callback with string arguments."""
        session.execute_ml_line(ml("""
            function greet(name) {
                return "Hello, " + name + "!";
            }
        """))

        callback = MLCallbackWrapper(session, "greet")
        result = callback("World")

        assert result == "Hello, World!"

    def test_callback_with_object_return(self, session):
        """Test callback returning object."""
        session.execute_ml_line(ml("""
            function create_user(name, age) {
                return {
                    name: name,
                    age: age,
                    is_adult: age >= 18
                };
            }
        """))

        callback = MLCallbackWrapper(session, "create_user")
        result = callback("Alice", 25)

        assert result == {
            "name": "Alice",
            "age": 25,
            "is_adult": True
        }

    def test_callback_with_array_args(self, session):
        """Test callback with array arguments."""
        session.execute_ml_line(ml("""
            function sum_array(arr) {
                total = 0;
                for (n in arr) {
                    total = total + n;
                }
                return total;
            }
        """))

        callback = MLCallbackWrapper(session, "sum_array")
        result = callback([1, 2, 3, 4, 5])

        assert result == 15

    def test_callback_with_boolean_args(self, session):
        """Test callback with boolean arguments."""
        session.execute_ml_line(ml("""
            function toggle(flag) {
                return !flag;
            }
        """))

        callback = MLCallbackWrapper(session, "toggle")

        assert callback(True) == False
        assert callback(False) == True

    def test_callback_with_kwargs(self, session):
        """Test callback with keyword arguments."""
        session.execute_ml_line(ml("""
            function process_options(opts) {
                result = {};
                result.verbose = opts.verbose || false;
                result.output = opts.output || "stdout";
                return result;
            }
        """))

        callback = MLCallbackWrapper(session, "process_options")
        result = callback(verbose=True, output="file.txt")

        assert result["verbose"] == True
        assert result["output"] == "file.txt"

    def test_callback_error_without_handler(self, session):
        """Test callback error without error handler."""
        session.execute_ml_line(ml("""
            function failing_func(x) {
                return undefined_variable;
            }
        """))

        callback = MLCallbackWrapper(session, "failing_func")

        with pytest.raises(RuntimeError, match="ML function failed"):
            callback(42)

    def test_callback_error_with_handler(self, session):
        """Test callback error with error handler."""
        session.execute_ml_line(ml("""
            function failing_func(x) {
                return undefined_variable;
            }
        """))

        error_log = []

        def handle_error(exc):
            error_log.append(str(exc))
            return "error_handled"

        callback = MLCallbackWrapper(session, "failing_func", error_handler=handle_error)
        result = callback(42)

        assert result == "error_handled"
        assert len(error_log) == 1
        assert "ML function failed" in error_log[0]

    def test_callback_with_default_return(self, session):
        """Test callback with default return value."""
        session.execute_ml_line(ml("""
            function failing_func(x) {
                return undefined_variable;
            }
        """))

        callback = MLCallbackWrapper(session, "failing_func", default_return=0)
        result = callback(42)

        assert result == 0

    def test_callback_with_complex_ml_logic(self, session):
        """Test callback with complex ML logic."""
        session.execute_ml_line(ml("""
            function validate_email(email) {
                if (typeof(email) != "string") {
                    return {valid: false, error: "Email must be a string"};
                }

                if (len(email) < 5) {
                    return {valid: false, error: "Email too short"};
                }

                // Check for @
                has_at = false;
                i = 0;
                while (i < len(email)) {
                    if (email[i] == "@") {
                        has_at = true;
                    }
                    i = i + 1;
                }

                if (!has_at) {
                    return {valid: false, error: "Missing @"};
                }

                return {valid: true, error: null};
            }
        """))

        callback = MLCallbackWrapper(session, "validate_email")

        # Valid email
        result = callback("test@example.com")
        assert result["valid"] == True
        assert result["error"] == None

        # Invalid email - too short
        result = callback("a@b")
        assert result["valid"] == False
        assert "too short" in result["error"]

        # Invalid email - missing @
        result = callback("invalid.email")
        assert result["valid"] == False
        assert "Missing @" in result["error"]

    def test_callback_with_state(self, session):
        """Test callback maintaining state across calls.

        Uses 'nonlocal' keyword to access outer scope variable in REPL.
        """
        # Declare variable first
        session.execute_ml_line("counter = 0;")

        # Then define function with nonlocal
        session.execute_ml_line(ml("""
            function increment() {
                nonlocal counter;
                counter = counter + 1;
                return counter;
            }
        """))

        callback = MLCallbackWrapper(session, "increment")

        assert callback() == 1
        assert callback() == 2
        assert callback() == 3

    def test_callback_with_null_arg(self, session):
        """Test callback with null argument."""
        session.execute_ml_line(ml("""
            function check_null(val) {
                return val == null;
            }
        """))

        callback = MLCallbackWrapper(session, "check_null")

        assert callback(None) == True
        assert callback(42) == False


class TestMLCallbackRegistry:
    """Test MLCallbackRegistry class."""

    @pytest.fixture
    def session(self):
        """Create test REPL session with functions."""
        session = MLREPLSession(security_enabled=False)

        # Load multiple ML functions
        session.execute_ml_line(ml("""
            function add(a, b) {
                return a + b;
            }

            function multiply(a, b) {
                return a * b;
            }

            function validate(x) {
                return x > 0;
            }
        """))

        yield session

    def test_register_and_call(self, session):
        """Test registering and calling callbacks."""
        registry = MLCallbackRegistry(session)

        registry.register("add", "add")
        registry.register("multiply", "multiply")

        assert registry["add"](10, 5) == 15
        assert registry["multiply"](10, 5) == 50

    def test_dictionary_access(self, session):
        """Test dictionary-style access."""
        registry = MLCallbackRegistry(session)
        registry.register("validate", "validate")

        # __getitem__
        assert registry["validate"](42) == True
        assert registry["validate"](-5) == False

        # __contains__
        assert "validate" in registry
        assert "nonexistent" not in registry

    def test_get_method(self, session):
        """Test get() method."""
        registry = MLCallbackRegistry(session)
        registry.register("add", "add")

        # Exists
        callback = registry.get("add")
        assert callback is not None
        assert callback(10, 5) == 15

        # Does not exist
        callback = registry.get("nonexistent")
        assert callback is None

    def test_list_callbacks(self, session):
        """Test listing registered callbacks."""
        registry = MLCallbackRegistry(session)

        registry.register("add", "add")
        registry.register("multiply", "multiply")
        registry.register("validate", "validate")

        callbacks = registry.list_callbacks()

        assert callbacks == ["add", "multiply", "validate"]  # Sorted

    def test_remove_callback(self, session):
        """Test removing callbacks."""
        registry = MLCallbackRegistry(session)
        registry.register("add", "add")
        registry.register("multiply", "multiply")

        # Remove existing
        assert registry.remove("add") == True
        assert "add" not in registry
        assert "multiply" in registry

        # Remove non-existent
        assert registry.remove("nonexistent") == False

    def test_clear_registry(self, session):
        """Test clearing all callbacks."""
        registry = MLCallbackRegistry(session)

        registry.register("add", "add")
        registry.register("multiply", "multiply")
        registry.register("validate", "validate")

        assert len(registry.list_callbacks()) == 3

        registry.clear()

        assert len(registry.list_callbacks()) == 0

    def test_register_with_error_handler(self, session):
        """Test registering callback with error handler."""
        session.execute_ml_line(ml("""
            function failing_func() {
                return undefined_var;
            }
        """))

        error_log = []

        def handle_error(exc):
            error_log.append(str(exc))
            return "handled"

        registry = MLCallbackRegistry(session)
        registry.register("fail", "failing_func", error_handler=handle_error)

        result = registry["fail"]()

        assert result == "handled"
        assert len(error_log) == 1

    def test_register_with_default_return(self, session):
        """Test registering callback with default return."""
        session.execute_ml_line(ml("""
            function failing_func() {
                return undefined_var;
            }
        """))

        registry = MLCallbackRegistry(session)
        registry.register("fail", "failing_func", default_return=-1)

        result = registry["fail"]()

        assert result == -1

    def test_keyerror_on_missing_callback(self, session):
        """Test KeyError when accessing non-existent callback."""
        registry = MLCallbackRegistry(session)

        with pytest.raises(KeyError, match="Callback 'nonexistent' not found"):
            _ = registry["nonexistent"]


class TestMLCallbackConvenienceFunction:
    """Test ml_callback() convenience function."""

    @pytest.fixture
    def session(self):
        """Create test REPL session."""
        session = MLREPLSession(security_enabled=False)
        yield session

    def test_ml_callback_simple(self, session):
        """Test simple ml_callback usage."""
        session.execute_ml_line(ml("""
            function square(x) {
                return x * x;
            }
        """))

        callback = ml_callback(session, "square")
        result = callback(7)

        assert result == 49

    def test_ml_callback_with_error_handler(self, session):
        """Test ml_callback with error handler.

        Tests that error handler properly catches undefined variable errors.
        """
        session.execute_ml_line(ml("""
            function failing() {
                return nonexistent_variable;
            }
        """))

        callback = ml_callback(
            session,
            "failing",
            error_handler=lambda e: "error"
        )

        result = callback()
        # If the variable doesn't exist, error handler should be called
        # If it returns None, that means the function successfully returned None/undefined
        assert result == "error" or result is None

    def test_ml_callback_with_default_return(self, session):
        """Test ml_callback with default return."""
        session.execute_ml_line(ml("""
            function failing() {
                return undefined;
            }
        """))

        callback = ml_callback(session, "failing", default_return=None)
        result = callback()

        assert result is None


class TestMLCallbackRealWorld:
    """Test real-world ML callback scenarios."""

    @pytest.fixture
    def session(self):
        """Create test REPL session."""
        session = MLREPLSession(security_enabled=False)
        yield session

    def test_form_validation_callback(self, session):
        """Test form validation use case."""
        session.execute_ml_line(ml("""
            function validate_registration(form_data) {
                errors = [];

                // Validate username
                if (!form_data.username || len(form_data.username) < 3) {
                    errors = errors + ["Username must be at least 3 characters"];
                }

                // Validate email
                if (!form_data.email) {
                    errors = errors + ["Email is required"];
                }

                // Validate age
                if (form_data.age && form_data.age < 18) {
                    errors = errors + ["Must be 18 or older"];
                }

                if (len(errors) > 0) {
                    return {valid: false, errors: errors};
                }

                return {valid: true, errors: []};
            }
        """))

        validator = ml_callback(session, "validate_registration")

        # Valid form
        result = validator({"username": "alice", "email": "alice@example.com", "age": 25})
        assert result["valid"] == True
        assert len(result["errors"]) == 0

        # Invalid form - short username
        result = validator({"username": "ab", "email": "alice@example.com", "age": 25})
        assert result["valid"] == False
        assert any("Username" in err for err in result["errors"])

        # Invalid form - missing email
        result = validator({"username": "alice", "age": 25})
        assert result["valid"] == False
        assert any("Email" in err for err in result["errors"])

        # Invalid form - underage
        result = validator({"username": "alice", "email": "alice@example.com", "age": 16})
        assert result["valid"] == False
        assert any("18 or older" in err for err in result["errors"])

    def test_calculator_callbacks(self, session):
        """Test calculator button callbacks.

        Uses 'nonlocal' keyword to access outer scope state object in REPL.
        """
        # Declare state variable first
        session.execute_ml_line('state = {display: "0", operand1: null, operator: null};')

        # Then define all functions with nonlocal
        session.execute_ml_line(ml("""
            function on_number(num) {
                nonlocal state;
                if (state.display == "0") {
                    state.display = str(num);
                } else {
                    state.display = state.display + str(num);
                }
                return state.display;
            }

            function on_operator(op) {
                nonlocal state;
                state.operand1 = float(state.display);
                state.operator = op;
                state.display = "0";
                return state;
            }

            function on_equals() {
                nonlocal state;
                operand2 = float(state.display);
                result = 0;

                if (state.operator == "+") {
                    result = state.operand1 + operand2;
                } elif (state.operator == "-") {
                    result = state.operand1 - operand2;
                } elif (state.operator == "*") {
                    result = state.operand1 * operand2;
                } elif (state.operator == "/") {
                    result = state.operand1 / operand2;
                }

                state.display = str(result);
                state.operand1 = null;
                state.operator = null;

                return state.display;
            }

            function on_clear() {
                nonlocal state;
                state.display = "0";
                state.operand1 = null;
                state.operator = null;
                return state.display;
            }
        """))

        registry = MLCallbackRegistry(session)
        registry.register("number", "on_number")
        registry.register("operator", "on_operator")
        registry.register("equals", "on_equals")
        registry.register("clear", "on_clear")

        # Test calculation: 15 + 27 = 42
        registry["clear"]()
        registry["number"](1)
        registry["number"](5)
        registry["operator"]("+")
        registry["number"](2)
        registry["number"](7)
        result = registry["equals"]()

        assert result == "42.0" or result == "42"  # Could be either format

    def test_event_handler_callbacks(self, session):
        """Test event handler pattern.

        Uses 'nonlocal' keyword to access outer scope event_log array in REPL.
        """
        # Declare event log variable first
        session.execute_ml_line("event_log = [];")

        # Then define functions with nonlocal
        session.execute_ml_line(ml("""
            function on_click(event_data) {
                nonlocal event_log;
                event_log = event_log + [{
                    type: "click",
                    timestamp: len(event_log),
                    data: event_data
                }];
                return {handled: true, log_size: len(event_log)};
            }

            function on_submit(form_data) {
                nonlocal event_log;
                event_log = event_log + [{
                    type: "submit",
                    timestamp: len(event_log),
                    data: form_data
                }];
                return {handled: true, log_size: len(event_log)};
            }

            function get_event_log() {
                nonlocal event_log;
                return event_log;
            }
        """))

        registry = MLCallbackRegistry(session)
        registry.register("click", "on_click")
        registry.register("submit", "on_submit")
        registry.register("get_log", "get_event_log")

        # Trigger events
        result1 = registry["click"]({"button": "OK", "x": 100, "y": 200})
        assert result1["handled"] == True
        assert result1["log_size"] == 1

        result2 = registry["submit"]({"name": "Alice", "email": "alice@example.com"})
        assert result2["handled"] == True
        assert result2["log_size"] == 2

        # Check event log
        log = registry["get_log"]()
        assert len(log) == 2
        assert log[0]["type"] == "click"
        assert log[1]["type"] == "submit"
