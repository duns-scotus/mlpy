"""Python bridge implementations for ML functional programming module."""

from typing import Any, Callable, List, TypeVar, Iterable
from functools import reduce as py_reduce, partial

T = TypeVar('T')
U = TypeVar('U')


def compose(*functions: Callable) -> Callable:
    """Compose functions right to left."""
    def composed(x):
        result = x
        for func in reversed(functions):
            result = func(result)
        return result
    return composed


def pipe(*functions: Callable) -> Callable:
    """Pipe functions left to right."""
    def piped(x):
        result = x
        for func in functions:
            result = func(result)
        return result
    return piped


def curry(func: Callable, arity: int = None) -> Callable:
    """Curry a function."""
    if arity is None:
        arity = func.__code__.co_argcount

    def curried(*args):
        if len(args) >= arity:
            return func(*args[:arity])
        else:
            return lambda *more_args: curried(*(args + more_args))

    return curried


def partial_apply(func: Callable, *args) -> Callable:
    """Partially apply arguments to function."""
    return partial(func, *args)


def identity(x: Any) -> Any:
    """Identity function."""
    return x


def constant(value: Any) -> Callable[[], Any]:
    """Create constant function."""
    return lambda: value


def memoize(func: Callable) -> Callable:
    """Memoize function results."""
    cache = {}

    def memoized(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized


class Functional:
    """Functional programming module interface for ML compatibility."""

    @staticmethod
    def compose(*functions: Callable) -> Callable:
        """Compose functions right to left."""
        return compose(*functions)

    @staticmethod
    def composeAll(functions: List[Callable]) -> Callable:
        """Compose an array of functions right to left."""
        return compose(*functions)

    @staticmethod
    def pipe(*functions: Callable) -> Callable:
        """Pipe functions left to right."""
        return pipe(*functions)

    @staticmethod
    def pipeAll(functions: List[Callable]) -> Callable:
        """Pipe an array of functions left to right."""
        return pipe(*functions)

    @staticmethod
    def curry(func: Callable, arity: int = None) -> Callable:
        """Curry a function."""
        return curry(func, arity)

    @staticmethod
    def partial(func: Callable, *args) -> Callable:
        """Partially apply arguments to function."""
        return partial_apply(func, *args)

    @staticmethod
    def identity(x: Any) -> Any:
        """Identity function."""
        return identity(x)

    @staticmethod
    def constant(value: Any) -> Callable[[], Any]:
        """Create constant function."""
        return constant(value)

    @staticmethod
    def memoize(func: Callable) -> Callable:
        """Memoize function results."""
        return memoize(func)

    @staticmethod
    def map(func: Callable[[T], U], iterable: Iterable[T]) -> List[U]:
        """Map function over iterable."""
        return list(map(func, iterable))

    @staticmethod
    def filter(predicate: Callable[[T], bool], iterable: Iterable[T]) -> List[T]:
        """Filter iterable with predicate."""
        return list(filter(predicate, iterable))

    @staticmethod
    def reduce(func: Callable[[T, U], T], iterable: Iterable[U], initial: T = None) -> T:
        """Reduce iterable with function."""
        if initial is not None:
            return py_reduce(func, iterable, initial)
        else:
            return py_reduce(func, iterable)

    @staticmethod
    def forEach(func: Callable[[T], None], iterable: Iterable[T]) -> None:
        """Execute function for each element."""
        for item in iterable:
            func(item)

    @staticmethod
    def find(predicate: Callable[[T], bool], iterable: Iterable[T]) -> T:
        """Find first element matching predicate."""
        for item in iterable:
            if predicate(item):
                return item
        return None

    @staticmethod
    def some(predicate: Callable[[T], bool], iterable: Iterable[T]) -> bool:
        """Check if some elements match predicate."""
        return any(predicate(item) for item in iterable)

    @staticmethod
    def every(predicate: Callable[[T], bool], iterable: Iterable[T]) -> bool:
        """Check if all elements match predicate."""
        return all(predicate(item) for item in iterable)

    @staticmethod
    def zip(*iterables: Iterable) -> List[tuple]:
        """Zip iterables together."""
        return list(zip(*iterables))

    @staticmethod
    def range(start: int, end: int = None, step: int = 1) -> List[int]:
        """Create range of numbers."""
        if end is None:
            return list(range(start))
        return list(range(start, end, step))

    @staticmethod
    def repeat(value: T, times: int) -> List[T]:
        """Repeat value times."""
        return [value] * times

    @staticmethod
    def take(n: int, iterable: Iterable[T]) -> List[T]:
        """Take first n elements."""
        return list(iterable)[:n]

    @staticmethod
    def drop(n: int, iterable: Iterable[T]) -> List[T]:
        """Drop first n elements."""
        return list(iterable)[n:]

    @staticmethod
    def flatten(nested_list: List[List[T]]) -> List[T]:
        """Flatten nested list."""
        result = []
        for sublist in nested_list:
            if isinstance(sublist, list):
                result.extend(sublist)
            else:
                result.append(sublist)
        return result

    @staticmethod
    def chunk(iterable: Iterable[T], size: int) -> List[List[T]]:
        """Chunk iterable into groups of size."""
        items = list(iterable)
        return [items[i:i + size] for i in range(0, len(items), size)]

    @staticmethod
    def groupBy(key_func: Callable[[T], U], iterable: Iterable[T]) -> dict[U, List[T]]:
        """Group elements by key function."""
        groups = {}
        for item in iterable:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups

    @staticmethod
    def unique(iterable: Iterable[T]) -> List[T]:
        """Get unique elements preserving order."""
        seen = set()
        result = []
        for item in iterable:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    @staticmethod
    def reverse(iterable: Iterable[T]) -> List[T]:
        """Reverse iterable."""
        return list(reversed(iterable))

    # Snake_case aliases for ML compatibility
    @staticmethod
    def partial_apply(func: Callable, *args) -> Callable:
        """Partially apply arguments to function (snake_case alias)."""
        return partial_apply(func, *args)

    @staticmethod
    def for_each(func: Callable[[T], None], iterable: Iterable[T]) -> None:
        """Execute function for each element (snake_case alias)."""
        Functional.forEach(func, iterable)

    @staticmethod
    def group_by(key_func: Callable[[T], U], iterable: Iterable[T]) -> dict[U, List[T]]:
        """Group elements by key function (snake_case alias)."""
        return Functional.groupBy(key_func, iterable)

    @staticmethod
    def curry2(func: Callable) -> Callable:
        """Curry a function for exactly 2 arguments."""
        def curried(a):
            def inner(b):
                return func(a, b)
            return inner
        return curried

    @staticmethod
    def partition(predicate: Callable[[T], bool], iterable: Iterable[T]) -> List[List[T]]:
        """Partition iterable into two lists based on predicate."""
        truthy = []
        falsy = []
        for item in iterable:
            if predicate(item):
                truthy.append(item)
            else:
                falsy.append(item)
        return [truthy, falsy]

    @staticmethod
    def ifElse(predicate: Callable, true_fn: Callable, false_fn: Callable) -> Callable:
        """Create conditional function application."""
        def conditional(value):
            if predicate(value):
                return true_fn(value)
            else:
                return false_fn(value)
        return conditional

    @staticmethod
    def cond(conditions: List[List]) -> Callable:
        """Multi-condition function application (like switch/case)."""
        def conditional(value):
            for condition_pair in conditions:
                predicate, action = condition_pair[0], condition_pair[1]
                if predicate(value):
                    return action(value)
            return None  # No condition matched
        return conditional

    @staticmethod
    def times(func: Callable[[int], T], n: int) -> List[T]:
        """Execute function N times with index parameter."""
        return [func(i) for i in range(n)]

    @staticmethod
    def zipWith(combiner: Callable, iterable1: Iterable, iterable2: Iterable) -> List:
        """Zip two iterables with custom combiner function."""
        return [combiner(a, b) for a, b in zip(iterable1, iterable2)]

    @staticmethod
    def takeWhile(predicate: Callable[[T], bool], iterable: Iterable[T]) -> List[T]:
        """Take elements while predicate returns True."""
        result = []
        for item in iterable:
            if predicate(item):
                result.append(item)
            else:
                break
        return result

    @staticmethod
    def juxt(functions: List[Callable]) -> Callable:
        """Apply multiple functions to the same input and return results as list."""
        def apply_all(value):
            return [func(value) for func in functions]
        return apply_all


# Create global functional instance for ML compatibility
functional = Functional()

# Export all bridge functions and the functional object
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