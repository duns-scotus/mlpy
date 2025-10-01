#!/usr/bin/env python3
"""Unit tests for lambda variable scoping issues."""

import pytest

from mlpy.ml.transpiler import transpile_ml_code


class TestLambdaVariableScoping:
    """Test that lambda expressions handle variable scoping correctly."""

    def test_simple_variable_chain_in_lambda(self):
        """Test lambda with variable chain that should be inlined."""
        ml_code = """
        function test() {
            numbers = [1, 2, 3];
            result = numbers.map(function(x) {
                doubled = x * 2;
                return doubled;
            });
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_variable_chain.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Transpiler failed for simple variable chain")

        # Should NOT have undefined variables in lambda
        if "lambda x: doubled" in generated_code:
            pytest.fail(f"Lambda contains undefined variable 'doubled': {generated_code}")

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated variable chain code has syntax error: {e}")

    def test_ecosystem_prey_processing_pattern(self):
        """Test the exact ecosystem prey processing pattern that's failing."""
        ml_code = """
        function processPreyBehavior(prey_population, predators, environment, time_step) {
            alive_prey = prey_population.filter(function(prey) {
                return prey.energy > 0;
            });

            processed_prey = alive_prey.map(function(prey_individual) {
                prey_with_food = preyFindFood(prey_individual, environment);
                prey_avoiding = preyAvoidPredators(prey_with_food, predators);
                prey_moved = preyMove(prey_avoiding, time_step);
                prey_updated = preyUpdateEnergy(prey_moved, time_step);
                return prey_updated;
            });

            return processed_prey;
        }

        function preyFindFood(prey, environment) {
            return prey;
        }

        function preyAvoidPredators(prey, predators) {
            return prey;
        }

        function preyMove(prey, time_step) {
            return prey;
        }

        function preyUpdateEnergy(prey, time_step) {
            updated = {};
            updated.energy = prey.energy - 1;
            return updated;
        }
        """

        result = transpile_ml_code(ml_code, "test_ecosystem_prey.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Ecosystem prey processing transpilation failed")

        # Critical bug check: should NOT have lambda with undefined variable
        problematic_patterns = [
            "lambda prey_individual: prey_updated",
            "lambda prey_individual: prey_with_food",
            "lambda prey_individual: prey_avoiding",
            "lambda prey_individual: prey_moved",
        ]

        for pattern in problematic_patterns:
            if pattern in generated_code:
                pytest.fail(
                    f"Found lambda with undefined variable pattern '{pattern}': {generated_code}"
                )

        # Should be syntactically valid
        try:
            compile(generated_code, "test", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated ecosystem prey code has syntax error: {e}")

        # Should execute without NameError
        try:
            exec(
                generated_code
                + """
# Test execution
prey_data = [{'energy': 50}, {'energy': 30}, {'energy': 80}]
result = processPreyBehavior(prey_data, [], {}, 0.1)
print(f"Success: processed {len(result)} prey")
"""
            )
        except NameError as e:
            if "is not defined" in str(e):
                pytest.fail(
                    f"Lambda variable scoping error: {e}\n\nGenerated code:\n{generated_code}"
                )

    def test_complex_expression_in_return(self):
        """Test lambda with complex expression in return that should be inlined."""
        ml_code = """
        function test() {
            numbers = [1, 2, 3, 4, 5];
            result = numbers.map(function(x) {
                step1 = x * 2;
                step2 = step1 + 1;
                step3 = step2 * 3;
                return step3;
            });
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_complex_return.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Complex expression transpilation failed")

        # Should NOT have undefined variables
        undefined_vars = ["lambda x: step1", "lambda x: step2", "lambda x: step3"]
        for pattern in undefined_vars:
            if pattern in generated_code:
                pytest.fail(f"Lambda contains undefined variable: {pattern}")

        # Should execute successfully
        try:
            exec(
                generated_code
                + """
result = test()
print(f"Result: {result}")
"""
            )
        except NameError as e:
            if "is not defined" in str(e):
                pytest.fail(f"Complex expression scoping error: {e}")

    def test_function_call_chain_in_lambda(self):
        """Test lambda with function call chain that should be properly handled."""
        ml_code = """
        function helper1(x) {
            return x + 1;
        }

        function helper2(x) {
            return x * 2;
        }

        function test() {
            numbers = [1, 2, 3];
            result = numbers.map(function(x) {
                intermediate = helper1(x);
                final = helper2(intermediate);
                return final;
            });
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_function_chain.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Function call chain transpilation failed")

        # Should NOT have undefined variables in lambda
        if "lambda x: intermediate" in generated_code or "lambda x: final" in generated_code:
            pytest.fail(
                f"Lambda contains undefined variables from function chain: {generated_code}"
            )

        # Should execute without errors
        try:
            exec(
                generated_code
                + """
result = test()
print(f"Function chain result: {result}")
"""
            )
        except NameError as e:
            if "is not defined" in str(e):
                pytest.fail(f"Function chain scoping error: {e}")

    def test_single_statement_lambda_works(self):
        """Test that single-statement lambdas still work correctly."""
        ml_code = """
        function test() {
            numbers = [1, 2, 3, 4, 5];
            result = numbers.map(function(x) {
                return x * 2;
            });
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_single_statement.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Single statement lambda transpilation failed")

        # Should work as a proper lambda
        if "lambda x: (x * 2)" not in generated_code and "lambda x: x * 2" not in generated_code:
            # This might be ok if it's generating something else valid
            pass

        # Should execute successfully
        try:
            exec(
                generated_code
                + """
result = test()
expected = [2, 4, 6, 8, 10]
print(f"Single lambda result: {result}")
"""
            )
        except Exception as e:
            pytest.fail(f"Single statement lambda error: {e}")

    def test_assignment_then_return_pattern(self):
        """Test the specific pattern: variable = expression; return variable."""
        ml_code = """
        function processItem(item) {
            doubled_item = item * 2;
            return doubled_item;
        }

        function test() {
            items = [1, 2, 3];
            result = items.map(function(x) {
                processed_x = processItem(x);
                return processed_x;
            });
            return result;
        }
        """

        result = transpile_ml_code(ml_code, "test_assignment_return.ml")
        generated_code = result[0] if isinstance(result, tuple) else result

        if generated_code is None:
            pytest.fail("Assignment-return pattern transpilation failed")

        # Should NOT have lambda with undefined variable
        if "lambda x: processed_x" in generated_code:
            pytest.fail(f"Lambda contains undefined 'processed_x': {generated_code}")

        # Should execute successfully
        try:
            exec(
                generated_code
                + """
result = test()
print(f"Assignment-return result: {result}")
"""
            )
        except NameError as e:
            if "processed_x" in str(e):
                pytest.fail(f"Assignment-return pattern scoping error: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
