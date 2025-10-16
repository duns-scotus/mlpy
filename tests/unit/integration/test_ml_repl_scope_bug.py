"""Test suite documenting REPL scope/closure bug.

BUG DESCRIPTION:
    ML functions cannot access variables from outer scopes when executed in the REPL.
    Variables ARE stored in the session namespace, but function execution doesn't have
    access to that namespace.

EXPECTED BEHAVIOR:
    Functions should be able to access variables defined in the same REPL session,
    similar to how Python closures work.

ACTUAL BEHAVIOR:
    When a function tries to access an outer-scope variable, it fails with:
    "Runtime Error: Variable 'X' is not defined"

IMPACT:
    - Callbacks that maintain state across calls don't work
    - Event handlers with shared state fail
    - Stateful applications (calculators, games, etc.) cannot be implemented

FIX LOCATION:
    This is a bug in the ML transpiler's code generation or the REPL's namespace
    handling. The fix likely needs to be in:
    - src/mlpy/ml/codegen/python_generator.py (closure handling)
    - src/mlpy/cli/repl.py (namespace injection into functions)
    - src/mlpy/ml/transpiler.py (REPL mode execution context)

WORKAROUND:
    Functions can only use their parameters and cannot reference external state.
    Any state must be passed as function parameters.
"""

import pytest
import textwrap
from mlpy.cli.repl import MLREPLSession


def ml(code):
    """Helper to dedent multiline ML code."""
    return textwrap.dedent(code).strip()


class TestMLREPLScopeBug:
    """Tests that document the REPL scope/closure bug."""

    @pytest.fixture
    def session(self):
        """Create test REPL session."""
        session = MLREPLSession(security_enabled=False)
        yield session

    @pytest.mark.xfail(reason="BUG: ML functions cannot access outer scope variables in REPL")
    def test_function_cannot_access_outer_variable(self, session):
        """Document that functions can't access variables from outer scope."""
        # Define variable
        result1 = session.execute_ml_line("counter = 0;")
        assert result1.success

        # Define function that references counter
        result2 = session.execute_ml_line(ml("""
            function increment() {
                counter = counter + 1;
                return counter;
            }
        """))
        assert result2.success

        # Try to call function - THIS FAILS
        result3 = session.execute_ml_line("increment();")
        assert result3.success, f"Expected success but got: {result3.error}"
        assert result3.value == 1

    @pytest.mark.xfail(reason="BUG: ML functions cannot access outer scope variables in REPL")
    def test_function_cannot_read_outer_variable(self, session):
        """Document that functions can't even READ outer scope variables."""
        # Define variable
        session.execute_ml_line("message = \"Hello\";")

        # Define function that just reads (doesn't modify) message
        session.execute_ml_line("function get_message() { return message; }")

        # Try to call function - THIS FAILS
        result = session.execute_ml_line("get_message();")
        assert result.success, f"Expected success but got: {result.error}"
        assert result.value == "Hello"

    @pytest.mark.xfail(reason="BUG: ML functions cannot access outer scope objects in REPL")
    def test_function_cannot_access_outer_object(self, session):
        """Document that functions can't access objects from outer scope."""
        # Define object
        session.execute_ml_line('state = {count: 0};')

        # Define function that modifies state
        session.execute_ml_line(ml("""
            function increment_state() {
                state.count = state.count + 1;
                return state.count;
            }
        """))

        # Try to call function - THIS FAILS
        result = session.execute_ml_line("increment_state();")
        assert result.success, f"Expected success but got: {result.error}"
        assert result.value == 1

    @pytest.mark.xfail(reason="BUG: ML functions cannot access outer scope arrays in REPL")
    def test_function_cannot_access_outer_array(self, session):
        """Document that functions can't access arrays from outer scope."""
        # Define array
        session.execute_ml_line('items = [];')

        # Define function that modifies array
        session.execute_ml_line(ml("""
            function add_item(item) {
                items = items + [item];
                return len(items);
            }
        """))

        # Try to call function - THIS FAILS
        result = session.execute_ml_line('add_item("test");')
        assert result.success, f"Expected success but got: {result.error}"
        assert result.value == 1

    def test_function_CAN_use_parameters(self, session):
        """Document that functions DO work with parameters (no outer scope access)."""
        # This should work - function only uses its parameters
        session.execute_ml_line("function add(a, b) { return a + b; }")

        result = session.execute_ml_line("add(10, 20);")
        assert result.success
        assert result.value == 30

    def test_variable_persistence_works(self, session):
        """Document that variables ARE persisted in the namespace."""
        # Variables do persist
        session.execute_ml_line("x = 42;")
        result = session.execute_ml_line("x;")

        assert result.success
        assert result.value == 42

        # Variables can be modified
        session.execute_ml_line("x = x + 1;")
        result = session.execute_ml_line("x;")

        assert result.success
        assert result.value == 43


class TestMultiStatementBlockBug:
    """Tests that document the multi-statement block parsing bug."""

    @pytest.fixture
    def session(self):
        """Create test REPL session."""
        session = MLREPLSession(security_enabled=False)
        yield session

    @pytest.mark.xfail(reason="BUG: REPL cannot parse variable + function in single block")
    def test_cannot_mix_variable_and_function_definitions(self, session):
        """Document that REPL can't parse variable + function in one call."""
        result = session.execute_ml_line(ml("""
            counter = 0;

            function increment() {
                return counter + 1;
            }
        """))

        assert result.success, f"Expected success but got: {result.error}"
        assert 'counter' in session.python_namespace
        assert 'increment' in session.python_namespace

    def test_multiple_functions_work(self, session):
        """Document that multiple functions in one block DO work."""
        result = session.execute_ml_line(ml("""
            function add(a, b) {
                return a + b;
            }

            function multiply(a, b) {
                return a * b;
            }
        """))

        assert result.success
        assert 'add' in session.python_namespace
        assert 'multiply' in session.python_namespace

    def test_separate_statements_work(self, session):
        """Document that separate execute_ml_line() calls DO work."""
        # Variable first
        result1 = session.execute_ml_line("counter = 0;")
        assert result1.success

        # Function second
        result2 = session.execute_ml_line("function get_counter() { return 42; }")
        assert result2.success

        assert 'counter' in session.python_namespace
        assert 'get_counter' in session.python_namespace
