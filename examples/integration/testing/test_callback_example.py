"""Example: Testing ML Callbacks with IntegrationTestHelper.

This example demonstrates how to test Python-to-ML callbacks using
the Integration Toolkit testing utilities.
"""

import pytest
from mlpy.integration.testing import IntegrationTestHelper


class TestCallbackExamples:
    """Examples of testing ML callbacks."""

    @pytest.fixture
    def helper(self):
        """Create a test helper and clean up after each test."""
        helper = IntegrationTestHelper()
        yield helper
        helper.cleanup()

    def test_simple_callback(self, helper):
        """Test a simple callback with one argument."""
        # Create REPL session and define ML function
        session = helper.create_test_repl()
        session.execute_ml_line("function double(x) { return x * 2; }")

        # Test the callback
        helper.assert_callback_works(
            session=session,
            function_name="double",
            args=(5,),
            expected_result=10
        )

    def test_callback_with_multiple_args(self, helper):
        """Test callback with multiple arguments."""
        session = helper.create_test_repl()
        session.execute_ml_line("function add(a, b) { return a + b; }")

        helper.assert_callback_works(
            session=session,
            function_name="add",
            args=(3, 7),
            expected_result=10
        )

    def test_callback_with_string_operations(self, helper):
        """Test callback with string manipulation."""
        session = helper.create_test_repl()
        ml_code = """
        import string;
        function greet(name) {
            return "Hello, " + name + "!";
        }
        """
        session.execute_ml_line(ml_code)

        helper.assert_callback_works(
            session=session,
            function_name="greet",
            args=("Alice",),
            expected_result="Hello, Alice!"
        )

    def test_callback_with_array_processing(self, helper):
        """Test callback that processes arrays."""
        session = helper.create_test_repl()
        ml_code = """
        function sum_array(arr) {
            total = 0;
            for (i = 0; i < len(arr); i = i + 1) {
                total = total + arr[i];
            }
            return total;
        }
        """
        session.execute_ml_line(ml_code)

        helper.assert_callback_works(
            session=session,
            function_name="sum_array",
            args=([1, 2, 3, 4, 5],),
            expected_result=15
        )

    def test_callback_with_object_manipulation(self, helper):
        """Test callback that works with objects."""
        session = helper.create_test_repl()
        ml_code = """
        function get_full_name(person) {
            return person.first_name + " " + person.last_name;
        }
        """
        session.execute_ml_line(ml_code)

        person_data = {
            "first_name": "John",
            "last_name": "Doe"
        }

        helper.assert_callback_works(
            session=session,
            function_name="get_full_name",
            args=(person_data,),
            expected_result="John Doe"
        )

    def test_callback_with_validation_logic(self, helper):
        """Test callback with complex validation logic."""
        session = helper.create_test_repl()
        ml_code = """
        function validate_email(email) {
            import regex;
            pattern = regex.compile("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$");
            return regex.test(pattern, email);
        }
        """
        session.execute_ml_line(ml_code)

        # Test valid email
        helper.assert_callback_works(
            session=session,
            function_name="validate_email",
            args=("user@example.com",),
            expected_result=True
        )

    def test_callback_with_mathematical_computation(self, helper):
        """Test callback with mathematical computation."""
        session = helper.create_test_repl()
        ml_code = """
        import math;
        function calculate_circle_area(radius) {
            return math.pi * radius * radius;
        }
        """
        session.execute_ml_line(ml_code)

        helper.assert_callback_works(
            session=session,
            function_name="calculate_circle_area",
            args=(5,),
            expected_result=78.53981633974483  # math.pi * 5 * 5
        )

    def test_multiple_callbacks_same_session(self, helper):
        """Test multiple callbacks in the same REPL session."""
        session = helper.create_test_repl()

        # Define multiple functions
        session.execute_ml_line("function add(a, b) { return a + b; }")
        session.execute_ml_line("function multiply(a, b) { return a * b; }")
        session.execute_ml_line("function subtract(a, b) { return a - b; }")

        # Test each callback
        helper.assert_callback_works(session, "add", (10, 5), expected_result=15)
        helper.assert_callback_works(session, "multiply", (10, 5), expected_result=50)
        helper.assert_callback_works(session, "subtract", (10, 5), expected_result=5)


def test_direct_callback_usage():
    """Example: Using ml_callback directly without helper."""
    from mlpy.cli.repl import MLREPLSession
    from mlpy.integration.ml_callback import ml_callback

    # Create REPL and define function
    session = MLREPLSession(security_enabled=False)
    session.execute_ml_line("function triple(x) { return x * 3; }")

    # Create callback
    triple_callback = ml_callback(session, "triple")

    # Use callback
    result = triple_callback(7)
    assert result == 21

    # Cleanup
    session.cleanup()


def test_callback_in_application_context():
    """Example: Testing callback in application context."""
    from mlpy.cli.repl import MLREPLSession
    from mlpy.integration.ml_callback import ml_callback

    # Simulate application initialization
    session = MLREPLSession(security_enabled=False)

    # Load ML business logic
    ml_code = """
    function calculate_discount(price, customer_type) {
        if (customer_type == "premium") {
            return price * 0.20;
        } elif (customer_type == "regular") {
            return price * 0.10;
        } else {
            return 0;
        }
    }
    """
    session.execute_ml_line(ml_code)

    # Create callback for business logic
    calculate_discount = ml_callback(session, "calculate_discount")

    # Test different scenarios
    assert calculate_discount(100, "premium") == 20.0
    assert calculate_discount(100, "regular") == 10.0
    assert calculate_discount(100, "guest") == 0

    # Cleanup
    session.cleanup()


if __name__ == "__main__":
    # Run with: pytest test_callback_example.py -v
    pytest.main([__file__, "-v"])
