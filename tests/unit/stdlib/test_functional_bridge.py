"""Unit tests for functional_bridge module migration."""

import pytest
from mlpy.stdlib.functional_bridge import Functional, functional
from mlpy.stdlib.decorators import get_module_metadata, _MODULE_REGISTRY


class TestFunctionalModuleRegistration:
    """Test that Functional module is properly registered with decorators."""

    def test_functional_module_registered(self):
        """Test that functional module is in global registry."""
        assert "functional" in _MODULE_REGISTRY
        assert _MODULE_REGISTRY["functional"] == Functional

    def test_functional_module_metadata(self):
        """Test functional module metadata is correct."""
        metadata = get_module_metadata("functional")
        assert metadata is not None
        assert metadata.name == "functional"
        assert metadata.description == "Functional programming composition and higher-order functions"
        assert "functional.compose" in metadata.capabilities
        assert "functional.transform" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_functional_has_function_metadata(self):
        """Test that functional module has registered functions."""
        metadata = get_module_metadata("functional")

        # Check key methods are registered
        assert "compose" in metadata.functions
        assert "pipe" in metadata.functions
        assert "curry" in metadata.functions
        assert "map" in metadata.functions
        assert "filter" in metadata.functions
        assert "reduce" in metadata.functions

        # Should have many functions (35+)
        assert len(metadata.functions) >= 35


class TestFunctionalComposition:
    """Test function composition utilities."""

    def test_compose(self):
        """Test compose() function - right to left."""
        add_ten = lambda x: x + 10
        double = lambda x: x * 2
        composed = functional.compose(double, add_ten)

        # add_ten first (right), then double (left)
        assert composed(5) == 30  # (5 + 10) * 2

    def test_composeAll(self):
        """Test composeAll() with list of functions."""
        add_ten = lambda x: x + 10
        double = lambda x: x * 2
        composed = functional.composeAll([double, add_ten])

        assert composed(5) == 30

    def test_pipe(self):
        """Test pipe() function - left to right."""
        add_ten = lambda x: x + 10
        double = lambda x: x * 2
        piped = functional.pipe(add_ten, double)

        # add_ten first (left), then double (right)
        assert piped(5) == 30  # (5 + 10) * 2

    def test_pipeAll(self):
        """Test pipeAll() with list of functions."""
        add_ten = lambda x: x + 10
        double = lambda x: x * 2
        piped = functional.pipeAll([add_ten, double])

        assert piped(5) == 30

    def test_curry(self):
        """Test curry() function."""
        add = lambda a, b: a + b
        curried_add = functional.curry(add)

        add_five = curried_add(5)
        assert add_five(3) == 8

    def test_partial(self):
        """Test partial() application."""
        multiply = lambda a, b, c: a * b * c
        partial_multiply = functional.partial(multiply, 2)

        assert partial_multiply(3, 4) == 24  # 2 * 3 * 4


class TestFunctionalBasicFunctions:
    """Test basic functional utilities."""

    def test_identity(self):
        """Test identity() function."""
        assert functional.identity(42) == 42
        assert functional.identity("hello") == "hello"
        assert functional.identity([1, 2, 3]) == [1, 2, 3]

    def test_constant(self):
        """Test constant() function."""
        const_42 = functional.constant(42)
        assert const_42() == 42
        assert const_42() == 42  # Always returns same value

    def test_memoize(self):
        """Test memoize() function."""
        call_count = [0]

        def expensive_func(x):
            call_count[0] += 1
            return x * 2

        memoized = functional.memoize(expensive_func)

        assert memoized(5) == 10
        assert call_count[0] == 1

        assert memoized(5) == 10  # Cached result
        assert call_count[0] == 1  # Not called again

        assert memoized(3) == 6  # New value
        assert call_count[0] == 2


class TestFunctionalHigherOrder:
    """Test higher-order functions."""

    def test_map(self):
        """Test map() function."""
        result = functional.map(lambda x: x * 2, [1, 2, 3])
        assert result == [2, 4, 6]

    def test_filter(self):
        """Test filter() function."""
        result = functional.filter(lambda x: x > 2, [1, 2, 3, 4, 5])
        assert result == [3, 4, 5]

    def test_reduce(self):
        """Test reduce() function."""
        result = functional.reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0)
        assert result == 10

    def test_reduce_without_initial(self):
        """Test reduce() without initial value."""
        result = functional.reduce(lambda acc, x: acc * x, [1, 2, 3, 4])
        assert result == 24

    def test_forEach(self):
        """Test forEach() function."""
        results = []
        functional.forEach(lambda x: results.append(x * 2), [1, 2, 3])
        assert results == [2, 4, 6]

    def test_find(self):
        """Test find() function."""
        result = functional.find(lambda x: x > 3, [1, 2, 3, 4, 5])
        assert result == 4

        result = functional.find(lambda x: x > 10, [1, 2, 3])
        assert result is None

    def test_some(self):
        """Test some() predicate."""
        assert functional.some(lambda x: x > 3, [1, 2, 3, 4]) is True
        assert functional.some(lambda x: x > 10, [1, 2, 3]) is False

    def test_every(self):
        """Test every() predicate."""
        assert functional.every(lambda x: x > 0, [1, 2, 3]) is True
        assert functional.every(lambda x: x > 2, [1, 2, 3]) is False


class TestFunctionalListUtilities:
    """Test list utility functions."""

    def test_zip(self):
        """Test zip() function."""
        result = functional.zip([1, 2, 3], ['a', 'b', 'c'])
        assert result == [(1, 'a'), (2, 'b'), (3, 'c')]

    def test_range(self):
        """Test range() function."""
        assert functional.range(5) == [0, 1, 2, 3, 4]
        assert functional.range(1, 5) == [1, 2, 3, 4]
        assert functional.range(0, 10, 2) == [0, 2, 4, 6, 8]

    def test_repeat(self):
        """Test repeat() function."""
        assert functional.repeat(5, 3) == [5, 5, 5]
        assert functional.repeat('x', 4) == ['x', 'x', 'x', 'x']

    def test_take(self):
        """Test take() function."""
        assert functional.take(3, [1, 2, 3, 4, 5]) == [1, 2, 3]
        assert functional.take(2, [1, 2]) == [1, 2]
        assert functional.take(5, [1, 2]) == [1, 2]  # Takes all available

    def test_drop(self):
        """Test drop() function."""
        assert functional.drop(2, [1, 2, 3, 4, 5]) == [3, 4, 5]
        assert functional.drop(3, [1, 2, 3]) == []
        assert functional.drop(0, [1, 2, 3]) == [1, 2, 3]

    def test_flatten(self):
        """Test flatten() function."""
        result = functional.flatten([[1, 2], [3, 4], [5]])
        assert result == [1, 2, 3, 4, 5]

    def test_chunk(self):
        """Test chunk() function."""
        result = functional.chunk([1, 2, 3, 4, 5], 2)
        assert result == [[1, 2], [3, 4], [5]]

    def test_groupBy(self):
        """Test groupBy() function."""
        data = [1, 2, 3, 4, 5, 6]
        result = functional.groupBy(lambda x: x % 2, data)
        assert result == {1: [1, 3, 5], 0: [2, 4, 6]}

    def test_unique(self):
        """Test unique() function."""
        result = functional.unique([1, 2, 2, 3, 3, 3, 4])
        assert result == [1, 2, 3, 4]

    def test_reverse(self):
        """Test reverse() function."""
        result = functional.reverse([1, 2, 3, 4])
        assert result == [4, 3, 2, 1]


class TestFunctionalAdvanced:
    """Test advanced FP functions."""

    def test_curry2(self):
        """Test curry2() for exactly 2 arguments."""
        add = lambda a, b: a + b
        curried = functional.curry2(add)

        add_five = curried(5)
        assert add_five(3) == 8

    def test_partition(self):
        """Test partition() function."""
        data = [1, 2, 3, 4, 5, 6]
        result = functional.partition(lambda x: x % 2 == 0, data)
        assert result == [[2, 4, 6], [1, 3, 5]]

    def test_ifElse(self):
        """Test ifElse() conditional function."""
        conditional = functional.ifElse(
            lambda x: x > 5,
            lambda x: x * 2,
            lambda x: x + 10
        )

        assert conditional(7) == 14  # > 5, so doubled
        assert conditional(3) == 13  # <= 5, so + 10

    def test_cond(self):
        """Test cond() multi-condition function."""
        categorize = functional.cond([
            [lambda x: x < 0, lambda x: "negative"],
            [lambda x: x == 0, lambda x: "zero"],
            [lambda x: x > 0, lambda x: "positive"]
        ])

        assert categorize(-5) == "negative"
        assert categorize(0) == "zero"
        assert categorize(5) == "positive"

    def test_times(self):
        """Test times() function."""
        result = functional.times(lambda i: i * 2, 5)
        assert result == [0, 2, 4, 6, 8]

    def test_zipWith(self):
        """Test zipWith() with custom combiner."""
        result = functional.zipWith(
            lambda a, b: a + b,
            [1, 2, 3],
            [10, 20, 30]
        )
        assert result == [11, 22, 33]

    def test_takeWhile(self):
        """Test takeWhile() function."""
        result = functional.takeWhile(lambda x: x < 4, [1, 2, 3, 4, 5, 6])
        assert result == [1, 2, 3]

    def test_juxt(self):
        """Test juxt() - apply multiple functions."""
        multi_fn = functional.juxt([
            lambda x: x + 1,
            lambda x: x * 2,
            lambda x: x ** 2
        ])

        assert multi_fn(3) == [4, 6, 9]


class TestFunctionalSnakeCaseAliases:
    """Test snake_case aliases for methods."""

    def test_partial_apply_alias(self):
        """Test partial_apply() alias."""
        multiply = lambda a, b, c: a * b * c
        partial_multiply = functional.partial_apply(multiply, 2)

        assert partial_multiply(3, 4) == 24

    def test_for_each_alias(self):
        """Test for_each() alias."""
        results = []
        functional.for_each(lambda x: results.append(x * 2), [1, 2, 3])
        assert results == [2, 4, 6]

    def test_group_by_alias(self):
        """Test group_by() alias."""
        data = [1, 2, 3, 4, 5, 6]
        result = functional.group_by(lambda x: x % 2, data)
        assert result == {1: [1, 3, 5], 0: [2, 4, 6]}


class TestFunctionalInstance:
    """Test global functional instance."""

    def test_functional_is_instance_of_functional_class(self):
        """Test that functional is an instance of Functional."""
        assert isinstance(functional, Functional)

    def test_functional_has_decorated_methods(self):
        """Test that functional instance has decorated methods with metadata."""
        assert hasattr(functional, "compose")
        assert hasattr(functional, "map")
        assert hasattr(functional, "filter")

        # Check they have metadata
        assert hasattr(functional.compose, "_ml_function_metadata")
        assert hasattr(functional.map, "_ml_function_metadata")
        assert hasattr(functional.filter, "_ml_function_metadata")


class TestFunctionalComplexScenarios:
    """Test complex functional programming scenarios."""

    def test_compose_pipe_combination(self):
        """Test combining compose and pipe."""
        add_ten = lambda x: x + 10
        double = lambda x: x * 2
        subtract_five = lambda x: x - 5

        # compose: right to left
        composed = functional.compose(subtract_five, double, add_ten)
        assert composed(5) == 25  # (5 + 10) * 2 - 5 = 25

        # pipe: left to right (same result, different order)
        piped = functional.pipe(add_ten, double, subtract_five)
        assert piped(5) == 25

    def test_curried_composition(self):
        """Test currying with composition."""
        add = lambda a, b: a + b
        curried_add = functional.curry(add)

        add_five = curried_add(5)
        composed = functional.compose(lambda x: x * 2, add_five)

        assert composed(3) == 16  # (3 + 5) * 2

    def test_map_filter_reduce_chain(self):
        """Test chaining map, filter, reduce."""
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # Map: square numbers
        squared = functional.map(lambda x: x ** 2, numbers)
        # Filter: only even squares
        even_squares = functional.filter(lambda x: x % 2 == 0, squared)
        # Reduce: sum them
        result = functional.reduce(lambda acc, x: acc + x, even_squares, 0)

        # 4, 16, 36, 64, 100 => 220
        assert result == 220

    def test_memoized_composition(self):
        """Test memoizing composed functions."""
        call_count = [0]

        def expensive(x):
            call_count[0] += 1
            return x * 2

        composed = functional.compose(
            lambda x: x + 1,
            functional.memoize(expensive)
        )

        composed(5)
        composed(5)  # Should use cached expensive(5)
        assert call_count[0] == 1
