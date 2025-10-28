#!/usr/bin/env python3
"""Regression tests for functional method chaining bug.

These tests verify that functional.map and functional.filter work correctly
when chained together inside user-defined functions. Previously, AttributeError
exceptions from inside lambda functions were incorrectly caught and re-raised
with misleading error messages.

Bug fix: src/mlpy/stdlib/runtime_helpers.py - separated getattr exception
handling from method execution to prevent masking AttributeErrors from lambdas.
"""

import pytest
from tests.helpers.repl_test_helper import REPLTestHelper


class TestFunctionalChainingBug:
    """Regression tests for functional method chaining with proper error propagation."""

    def test_functional_map_works_alone(self):
        """Verify functional.map works in a user function."""
        repl = REPLTestHelper()
        repl.execute_ml("import functional;")
        repl.execute_ml("function testMap(data) { return functional.map(fn(x) => x * 2, data); }")

        result = repl.execute_ml("testMap([1, 2, 3])")
        assert result == [2, 4, 6], f"Expected [2, 4, 6], got {result}"

    def test_functional_filter_works_alone(self):
        """Verify functional.filter works in a user function."""
        repl = REPLTestHelper()
        repl.execute_ml("import functional;")
        repl.execute_ml("function testFilter(data) { return functional.filter(fn(x) => x > 2, data); }")

        result = repl.execute_ml("testFilter([1, 2, 3, 4])")
        assert result == [3, 4], f"Expected [3, 4], got {result}"

    def test_functional_map_then_filter_separate_statements(self):
        """Verify map and filter work when in separate statements."""
        repl = REPLTestHelper()
        repl.execute_ml("import functional;")
        repl.execute_ml("function testChaining(data) { step1 = functional.map(fn(x) => x * 2, data); step2 = functional.filter(fn(x) => x > 2, step1); return step2; }")

        result = repl.execute_ml("testChaining([1, 2, 3])")
        assert result == [4, 6], f"Expected [4, 6], got {result}"

    def test_functional_map_then_filter_in_return(self):
        """Verify chaining map and filter in return statement works.

        Regression test for bug where chaining functional methods in a return
        statement incorrectly raised: 'Functional' object has no method 'filter'
        """
        repl = REPLTestHelper()
        repl.execute_ml("import functional;")

        # This function definition should work
        repl.execute_ml("function testChaining(data) { mapped = functional.map(fn(x) => x * 2, data); return functional.filter(fn(x) => x > 2, mapped); }")

        # But execution fails with 'Functional' object has no method 'filter'
        result = repl.execute_ml("testChaining([1, 2, 3])")
        assert result == [4, 6], f"Expected [4, 6], got {result}"

    def test_functional_filter_then_map(self):
        """Verify filter followed by map works.

        Regression test confirming the bug fix works in both directions.
        """
        repl = REPLTestHelper()
        repl.execute_ml("import functional;")

        repl.execute_ml("function testChaining(data) { filtered = functional.filter(fn(x) => x > 1, data); return functional.map(fn(x) => x * 2, filtered); }")

        result = repl.execute_ml("testChaining([1, 2, 3])")
        assert result == [4, 6], f"Expected [4, 6], got {result}"

    def test_minimal_two_method_calls(self):
        """Absolute minimal case: just two functional method calls in sequence.

        This is the simplest possible reproduction.
        """
        repl = REPLTestHelper()
        repl.execute_ml("import functional;")

        repl.execute_ml("function test(data) { a = functional.map(fn(x) => x, data); b = functional.filter(fn(x) => x > 0, a); return b; }")

        result = repl.execute_ml("test([1, 2, 3])")
        assert result == [1, 2, 3], f"Expected [1, 2, 3], got {result}"

    def test_with_property_access(self):
        """Verify chaining with property access in lambdas works correctly.

        Regression test for the exact pattern that triggered the bug.
        When lambdas access object properties and encounter AttributeError,
        it should propagate the correct error message, not mask it.
        """
        repl = REPLTestHelper()
        repl.execute_ml("import functional;")

        # Function with property access in lambdas
        repl.execute_ml("function processBuggyPattern(prey_population) { processed = functional.map(fn(prey) => prey.energy < 10 ? null : prey, prey_population); return functional.filter(fn(prey) => prey.energy > 0, processed); }")

        # Set test data
        repl.set_variable('prey_data', [
            {'energy': 15, 'name': 'prey1'},
            {'energy': 5, 'name': 'prey2'},
            {'energy': 20, 'name': 'prey3'}
        ])

        # This should fail with NoneType error (accessing .energy on None)
        # Previously the bug caused it to fail with wrong error message
        try:
            result = repl.execute_ml("processBuggyPattern(prey_data)")
            # If we get here, check if it's the expected error
            assert False, f"Expected error but got result: {result}"
        except AssertionError as e:
            error_msg = str(e)
            # Verify we get the CORRECT error message (NoneType attribute error)
            # not the buggy message ('Functional' object has no method 'filter')
            if "'Functional' object has no method 'filter'" in error_msg:
                pytest.fail(f"BUG RETURNED: Got wrong error message: {error_msg}")
            elif "NoneType" in error_msg and ("energy" in error_msg or "accessible attribute" in error_msg):
                pass  # This is the expected/correct behavior
            else:
                raise


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
