#!/usr/bin/env python3
"""Unit tests for lambda variable scoping issues."""

import pytest

from tests.helpers.repl_test_helper import REPLTestHelper


class TestLambdaVariableScoping:
    """Test that lambda expressions handle variable scoping correctly."""

    def test_simple_variable_chain_in_lambda(self):
        """Test arrow function with simple expression (no variable chain needed)."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function test() { numbers = [1, 2, 3]; result = functional.map(fn(x) => x * 2, numbers); return result; }")

        result = repl.execute_ml("test()")

        assert result == [2, 4, 6], f"Expected [2, 4, 6], got {result}"

    def test_ecosystem_prey_processing_pattern(self):
        """Test the exact ecosystem prey processing pattern with helper function."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function preyFindFood(prey, environment) { return prey; }")
        repl.execute_ml("function preyAvoidPredators(prey, predators) { return prey; }")
        repl.execute_ml("function preyMove(prey, time_step) { return prey; }")
        repl.execute_ml("function preyUpdateEnergy(prey, time_step) { updated = {}; updated.energy = prey.energy - 1; return updated; }")
        repl.execute_ml("function processSinglePrey(prey_individual, predators, environment, time_step) { prey_with_food = preyFindFood(prey_individual, environment); prey_avoiding = preyAvoidPredators(prey_with_food, predators); prey_moved = preyMove(prey_avoiding, time_step); prey_updated = preyUpdateEnergy(prey_moved, time_step); return prey_updated; }")
        repl.execute_ml("function processPreyBehavior(prey_population, predators, environment, time_step) { alive_prey = functional.filter(fn(prey) => prey.energy > 0, prey_population); processed_prey = functional.map(fn(prey_individual) => processSinglePrey(prey_individual, predators, environment, time_step), alive_prey); return processed_prey; }")

        repl.set_variable('prey_data', [{'energy': 50}, {'energy': 30}, {'energy': 80}])

        result = repl.execute_ml("processPreyBehavior(prey_data, [], {}, 0.1)")

        # Should process all 3 prey successfully
        assert len(result) == 3, f"Expected 3 processed prey, got {len(result)}"

    def test_complex_expression_in_return(self):
        """Test arrow function with complex expression inlined."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function test() { numbers = [1, 2, 3, 4, 5]; result = functional.map(fn(x) => ((x * 2) + 1) * 3, numbers); return result; }")

        result = repl.execute_ml("test()")

        # Expected: [((1*2)+1)*3, ((2*2)+1)*3, ...] = [9, 15, 21, 27, 33]
        assert result == [9, 15, 21, 27, 33], f"Expected [9, 15, 21, 27, 33], got {result}"

    def test_function_call_chain_in_lambda(self):
        """Test arrow function with function call chain inlined."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function helper1(x) { return x + 1; }")
        repl.execute_ml("function helper2(x) { return x * 2; }")
        repl.execute_ml("function test() { numbers = [1, 2, 3]; result = functional.map(fn(x) => helper2(helper1(x)), numbers); return result; }")

        result = repl.execute_ml("test()")

        # Expected: [helper2(helper1(1)), ...] = [helper2(2), helper2(3), helper2(4)] = [4, 6, 8]
        assert result == [4, 6, 8], f"Expected [4, 6, 8], got {result}"

    def test_single_statement_lambda_works(self):
        """Test that single-statement arrow functions work correctly."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function test() { numbers = [1, 2, 3, 4, 5]; result = functional.map(fn(x) => x * 2, numbers); return result; }")

        result = repl.execute_ml("test()")

        assert result == [2, 4, 6, 8, 10], f"Expected [2, 4, 6, 8, 10], got {result}"

    def test_assignment_then_return_pattern(self):
        """Test arrow function calling helper function."""
        repl = REPLTestHelper()

        repl.execute_ml("import functional;")
        repl.execute_ml("function processItem(item) { doubled_item = item * 2; return doubled_item; }")
        repl.execute_ml("function test() { items = [1, 2, 3]; result = functional.map(fn(x) => processItem(x), items); return result; }")

        result = repl.execute_ml("test()")

        assert result == [2, 4, 6], f"Expected [2, 4, 6], got {result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
