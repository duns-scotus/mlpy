"""Python bridge implementations for ML functional programming module.

The functional module provides comprehensive functional programming utilities.
When imported in ML code as 'import functional;', it creates a 'functional' object
with methods for functional composition, higher-order functions, and FP patterns.

Usage in ML:
    import functional;

    // Composition
    addTen = fn(x) => x + 10;
    double = fn(x) => x * 2;
    combined = functional.compose(double, addTen);

    // Higher-order functions
    numbers = [1, 2, 3, 4, 5];
    doubled = functional.map(fn(x) => x * 2, numbers);
    evens = functional.filter(fn(x) => x % 2 == 0, numbers);
"""

from collections.abc import Callable, Iterable
from functools import partial
from functools import reduce as py_reduce
from typing import Any, TypeVar
from mlpy.stdlib.decorators import ml_module, ml_function, FunctionMetadata

T = TypeVar("T")
U = TypeVar("U")


def _mark_as_ml_safe(func: Callable, description: str = "Dynamically created function") -> Callable:
    """Mark a dynamically created function as ML-safe by adding metadata.

    This allows the whitelist validator to accept the function without blocking it.
    """
    func._ml_function_metadata = FunctionMetadata(
        name=getattr(func, '__name__', '<lambda>'),
        description=description,
        capabilities=[],
        params=[],
        returns=None
    )
    return func


# Module-level helper functions
def compose(*functions: Callable) -> Callable:
    """Compose functions right to left."""
    def composed(x):
        result = x
        for func in reversed(functions):
            result = func(result)
        return result
    return _mark_as_ml_safe(composed, "Composed function (right to left)")


def pipe(*functions: Callable) -> Callable:
    """Pipe functions left to right."""
    def piped(x):
        result = x
        for func in functions:
            result = func(result)
        return result
    return _mark_as_ml_safe(piped, "Piped function (left to right)")


def curry(func: Callable, arity: int = None) -> Callable:
    """Curry a function."""
    if arity is None:
        arity = func.__code__.co_argcount

    def curried(*args):
        if len(args) >= arity:
            return func(*args[:arity])
        else:
            inner = lambda *more_args: curried(*(args + more_args))
            return _mark_as_ml_safe(inner, "Curried function (partial)")
    return _mark_as_ml_safe(curried, "Curried function")


def partial_apply(func: Callable, *args) -> Callable:
    """Partially apply arguments to function."""
    result = partial(func, *args)
    return _mark_as_ml_safe(result, "Partially applied function")


def identity(x: Any) -> Any:
    """Identity function."""
    return x


def constant(value: Any) -> Callable[[], Any]:
    """Create constant function."""
    const_func = lambda: value
    return _mark_as_ml_safe(const_func, "Constant function")


def memoize(func: Callable) -> Callable:
    """Memoize function results."""
    cache = {}

    def memoized(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return _mark_as_ml_safe(memoized, "Memoized function")


@ml_module(
    name="functional",
    description="Functional programming composition and higher-order functions",
    capabilities=["functional.compose", "functional.transform"],
    version="1.0.0"
)
class Functional:
    """Functional programming module interface for ML code.

    This class provides comprehensive functional programming utilities including
    composition, higher-order functions, and advanced FP patterns.
    """

    @ml_function(description="Compose functions right to left", capabilities=["functional.compose"])
    def compose(self, *functions: Callable) -> Callable:
        """Compose functions right to left.

        Args:
            *functions: Functions to compose

        Returns:
            Composed function that applies functions right to left
        """
        return compose(*functions)

    @ml_function(description="Compose array of functions", capabilities=["functional.compose"])
    def composeAll(self, functions: list[Callable]) -> Callable:
        """Compose an array of functions right to left.

        Args:
            functions: List of functions to compose

        Returns:
            Composed function
        """
        return compose(*functions)

    @ml_function(description="Pipe functions left to right", capabilities=["functional.compose"])
    def pipe(self, *functions: Callable) -> Callable:
        """Pipe functions left to right.

        Args:
            *functions: Functions to pipe

        Returns:
            Piped function that applies functions left to right
        """
        return pipe(*functions)

    @ml_function(description="Pipe array of functions", capabilities=["functional.compose"])
    def pipeAll(self, functions: list[Callable]) -> Callable:
        """Pipe an array of functions left to right.

        Args:
            functions: List of functions to pipe

        Returns:
            Piped function
        """
        return pipe(*functions)

    @ml_function(description="Curry a function", capabilities=["functional.compose"])
    def curry(self, func: Callable, arity: int = None) -> Callable:
        """Curry a function.

        Args:
            func: Function to curry
            arity: Number of arguments (default: auto-detect)

        Returns:
            Curried function
        """
        return curry(func, arity)

    @ml_function(description="Partially apply arguments", capabilities=["functional.compose"])
    def partial(self, func: Callable, *args) -> Callable:
        """Partially apply arguments to function.

        Args:
            func: Function to partially apply
            *args: Arguments to apply

        Returns:
            Partially applied function
        """
        return partial_apply(func, *args)

    @ml_function(description="Identity function")
    def identity(self, x: Any) -> Any:
        """Identity function.

        Args:
            x: Value to return

        Returns:
            The same value
        """
        return identity(x)

    @ml_function(description="Create constant function", capabilities=["functional.compose"])
    def constant(self, value: Any) -> Callable[[], Any]:
        """Create constant function.

        Args:
            value: Value to return

        Returns:
            Function that always returns value
        """
        return constant(value)

    @ml_function(description="Memoize function", capabilities=["functional.compose"])
    def memoize(self, func: Callable) -> Callable:
        """Memoize function results.

        Args:
            func: Function to memoize

        Returns:
            Memoized function with caching
        """
        return memoize(func)

    @ml_function(description="Map function over iterable", capabilities=["functional.transform"])
    def map(self, func: Callable[[T], U], iterable: Iterable[T]) -> list[U]:
        """Map function over iterable.

        Args:
            func: Transform function
            iterable: Iterable to map over

        Returns:
            List of transformed values
        """
        return list(map(func, iterable))

    @ml_function(description="Filter iterable with predicate", capabilities=["functional.transform"])
    def filter(self, predicate: Callable[[T], bool], iterable: Iterable[T]) -> list[T]:
        """Filter iterable with predicate.

        Args:
            predicate: Filter function
            iterable: Iterable to filter

        Returns:
            List of matching elements
        """
        return list(filter(predicate, iterable))

    @ml_function(description="Reduce iterable with function", capabilities=["functional.transform"])
    def reduce(self, func: Callable[[T, U], T], iterable: Iterable[U], initial: T = None) -> T:
        """Reduce iterable with function.

        Args:
            func: Reducer function
            iterable: Iterable to reduce
            initial: Initial value (optional)

        Returns:
            Reduced value
        """
        if initial is not None:
            return py_reduce(func, iterable, initial)
        else:
            return py_reduce(func, iterable)

    @ml_function(description="Execute function for each element", capabilities=["functional.transform"])
    def forEach(self, func: Callable[[T], None], iterable: Iterable[T]) -> None:
        """Execute function for each element.

        Args:
            func: Function to execute
            iterable: Iterable to process
        """
        for item in iterable:
            func(item)

    @ml_function(description="Find first matching element", capabilities=["functional.transform"])
    def find(self, predicate: Callable[[T], bool], iterable: Iterable[T]) -> T:
        """Find first element matching predicate.

        Args:
            predicate: Match function
            iterable: Iterable to search

        Returns:
            First matching element, or None if not found
        """
        for item in iterable:
            if predicate(item):
                return item
        return None

    @ml_function(description="Check if some elements match", capabilities=["functional.transform"])
    def some(self, predicate: Callable[[T], bool], iterable: Iterable[T]) -> bool:
        """Check if some elements match predicate.

        Args:
            predicate: Test function
            iterable: Iterable to check

        Returns:
            True if at least one element matches
        """
        return any(predicate(item) for item in iterable)

    @ml_function(description="Check if all elements match", capabilities=["functional.transform"])
    def every(self, predicate: Callable[[T], bool], iterable: Iterable[T]) -> bool:
        """Check if all elements match predicate.

        Args:
            predicate: Test function
            iterable: Iterable to check

        Returns:
            True if all elements match
        """
        return all(predicate(item) for item in iterable)

    @ml_function(description="Zip iterables together", capabilities=["functional.transform"])
    def zip(self, *iterables: Iterable) -> list[tuple]:
        """Zip iterables together.

        Args:
            *iterables: Iterables to zip

        Returns:
            List of tuples
        """
        return list(zip(*iterables, strict=False))

    @ml_function(description="Create range of numbers")
    def range(self, start: int, end: int = None, step: int = 1) -> list[int]:
        """Create range of numbers.

        Args:
            start: Start value (or end if end is None)
            end: End value (optional)
            step: Step size (default 1)

        Returns:
            List of numbers
        """
        if end is None:
            return list(range(start))
        return list(range(start, end, step))

    @ml_function(description="Repeat value N times")
    def repeat(self, value: T, times: int) -> list[T]:
        """Repeat value N times.

        Args:
            value: Value to repeat
            times: Number of repetitions

        Returns:
            List of repeated values
        """
        return [value] * times

    @ml_function(description="Take first N elements", capabilities=["functional.transform"])
    def take(self, n: int, iterable: Iterable[T]) -> list[T]:
        """Take first N elements.

        Args:
            n: Number of elements to take
            iterable: Iterable to take from

        Returns:
            List of first N elements
        """
        return list(iterable)[:n]

    @ml_function(description="Drop first N elements", capabilities=["functional.transform"])
    def drop(self, n: int, iterable: Iterable[T]) -> list[T]:
        """Drop first N elements.

        Args:
            n: Number of elements to drop
            iterable: Iterable to drop from

        Returns:
            List without first N elements
        """
        return list(iterable)[n:]

    @ml_function(description="Flatten nested list", capabilities=["functional.transform"])
    def flatten(self, nested_list: list[list[T]]) -> list[T]:
        """Flatten nested list one level.

        Args:
            nested_list: Nested list to flatten

        Returns:
            Flattened list
        """
        result = []
        for sublist in nested_list:
            if isinstance(sublist, list):
                result.extend(sublist)
            else:
                result.append(sublist)
        return result

    @ml_function(description="Chunk iterable into groups", capabilities=["functional.transform"])
    def chunk(self, size: int, iterable: Iterable[T]) -> list[list[T]]:
        """Chunk iterable into groups of size.

        Args:
            size: Chunk size
            iterable: Iterable to chunk

        Returns:
            List of chunks
        """
        items = list(iterable)
        return [items[i:i + size] for i in range(0, len(items), size)]

    @ml_function(description="Group elements by key", capabilities=["functional.transform"])
    def groupBy(self, key_func: Callable[[T], U], iterable: Iterable[T]) -> dict[U, list[T]]:
        """Group elements by key function.

        Args:
            key_func: Function to extract group key
            iterable: Iterable to group

        Returns:
            Dictionary of groups
        """
        groups = {}
        for item in iterable:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups

    @ml_function(description="Get unique elements", capabilities=["functional.transform"])
    def unique(self, iterable: Iterable[T]) -> list[T]:
        """Get unique elements preserving order.

        Args:
            iterable: Iterable to deduplicate

        Returns:
            List of unique elements
        """
        seen = set()
        result = []
        for item in iterable:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    @ml_function(description="Reverse iterable", capabilities=["functional.transform"])
    def reverse(self, iterable: Iterable[T]) -> list[T]:
        """Reverse iterable.

        Args:
            iterable: Iterable to reverse

        Returns:
            Reversed list
        """
        return list(reversed(iterable))

    # Advanced FP functions
    @ml_function(description="Curry function for 2 arguments", capabilities=["functional.compose"])
    def curry2(self, func: Callable) -> Callable:
        """Curry a function for exactly 2 arguments.

        Args:
            func: Function with 2 arguments

        Returns:
            Curried function
        """
        def curried(a):
            def inner(b):
                return func(a, b)
            return _mark_as_ml_safe(inner, "Curried function (inner)")
        return _mark_as_ml_safe(curried, "Curried function (curry2)")

    @ml_function(description="Partition by predicate", capabilities=["functional.transform"])
    def partition(self, predicate: Callable[[T], bool], iterable: Iterable[T]) -> list[list[T]]:
        """Partition iterable into two lists based on predicate.

        Args:
            predicate: Test function
            iterable: Iterable to partition

        Returns:
            List containing [matching, non-matching] lists
        """
        truthy = []
        falsy = []
        for item in iterable:
            if predicate(item):
                truthy.append(item)
            else:
                falsy.append(item)
        return [truthy, falsy]

    @ml_function(description="Conditional function application", capabilities=["functional.compose"])
    def ifElse(self, predicate: Callable, true_fn: Callable, false_fn: Callable) -> Callable:
        """Create conditional function application.

        Args:
            predicate: Condition function
            true_fn: Function to apply if true
            false_fn: Function to apply if false

        Returns:
            Conditional function
        """
        def conditional(value):
            if predicate(value):
                return true_fn(value)
            else:
                return false_fn(value)
        return _mark_as_ml_safe(conditional, "Conditional function (ifElse)")

    @ml_function(description="Multi-condition function", capabilities=["functional.compose"])
    def cond(self, conditions: list[list]) -> Callable:
        """Multi-condition function application (like switch/case).

        Args:
            conditions: List of [predicate, action] pairs

        Returns:
            Conditional function that applies first matching action
        """
        def conditional(value):
            for condition_pair in conditions:
                predicate, action = condition_pair[0], condition_pair[1]
                if predicate(value):
                    return action(value)
            return None  # No condition matched
        return _mark_as_ml_safe(conditional, "Multi-conditional function (cond)")

    @ml_function(description="Execute function N times", capabilities=["functional.transform"])
    def times(self, n: int, func: Callable[[int], T]) -> list[T]:
        """Execute function N times with index parameter.

        Args:
            n: Number of times to execute
            func: Function receiving index

        Returns:
            List of results
        """
        return [func(i) for i in range(n)]

    @ml_function(description="Zip with custom combiner", capabilities=["functional.transform"])
    def zipWith(self, combiner: Callable, iterable1: Iterable, iterable2: Iterable) -> list:
        """Zip two iterables with custom combiner function.

        Args:
            combiner: Function to combine pairs
            iterable1: First iterable
            iterable2: Second iterable

        Returns:
            List of combined values
        """
        return [combiner(a, b) for a, b in zip(iterable1, iterable2, strict=False)]

    @ml_function(description="Take while predicate true", capabilities=["functional.transform"])
    def takeWhile(self, predicate: Callable[[T], bool], iterable: Iterable[T]) -> list[T]:
        """Take elements while predicate returns True.

        Args:
            predicate: Test function
            iterable: Iterable to take from

        Returns:
            List of elements until predicate fails
        """
        result = []
        for item in iterable:
            if predicate(item):
                result.append(item)
            else:
                break
        return result

    @ml_function(description="Apply multiple functions to same input", capabilities=["functional.compose"])
    def juxt(self, functions: list[Callable]) -> Callable:
        """Apply multiple functions to the same input and return results as list.

        Args:
            functions: List of functions to apply

        Returns:
            Function that applies all functions and returns list of results
        """
        def apply_all(value):
            return [func(value) for func in functions]
        return _mark_as_ml_safe(apply_all, "Juxted function")

    # Snake_case aliases for convenience
    @ml_function(description="Partially apply (snake_case alias)", capabilities=["functional.compose"])
    def partial_apply(self, func: Callable, *args) -> Callable:
        """Alias for partial()."""
        return self.partial(func, *args)

    @ml_function(description="For each (snake_case alias)", capabilities=["functional.transform"])
    def for_each(self, func: Callable[[T], None], iterable: Iterable[T]) -> None:
        """Alias for forEach()."""
        self.forEach(func, iterable)

    @ml_function(description="Group by (snake_case alias)", capabilities=["functional.transform"])
    def group_by(self, key_func: Callable[[T], U], iterable: Iterable[T]) -> dict[U, list[T]]:
        """Alias for groupBy()."""
        return self.groupBy(key_func, iterable)


# Create global functional instance for ML import
# When ML code does 'import functional;', this creates the 'functional' object
functional = Functional()


# Export public API
__all__ = [
    "Functional",
    "functional",
    "compose",
    "pipe",
    "curry",
    "partial_apply",
    "identity",
    "constant",
    "memoize",
]
