"""Python bridge implementations for ML Array module."""

from typing import Any, List, TypeVar, Callable

T = TypeVar('T')


def array_from(*args: Any) -> List[Any]:
    """Create array from arguments."""
    return list(args)


def array_of(*elements: Any) -> List[Any]:
    """Create array from elements."""
    return list(elements)


def array_fill(length: int, value: Any) -> List[Any]:
    """Create array filled with value."""
    return [value] * length


def array_range(start: int, end: int, step: int = 1) -> List[int]:
    """Create array with range of numbers."""
    return list(range(start, end, step))


class Array:
    """Array module interface for ML compatibility."""

    @staticmethod
    def from_(*args: Any) -> List[Any]:
        """Create array from arguments."""
        return array_from(*args)

    @staticmethod
    def of(*elements: Any) -> List[Any]:
        """Create array from elements."""
        return array_of(*elements)

    @staticmethod
    def fill(length: int, value: Any) -> List[Any]:
        """Create array filled with value."""
        return array_fill(length, value)

    @staticmethod
    def range(start: int, end: int, step: int = 1) -> List[int]:
        """Create array with range of numbers."""
        return array_range(start, end, step)

    @staticmethod
    def length(arr: List[Any]) -> int:
        """Get array length."""
        return len(arr)

    @staticmethod
    def isEmpty(arr: List[Any]) -> bool:
        """Check if array is empty."""
        return len(arr) == 0

    @staticmethod
    def first(arr: List[Any]) -> Any:
        """Get first element."""
        return arr[0] if arr else None

    @staticmethod
    def last(arr: List[Any]) -> Any:
        """Get last element."""
        return arr[-1] if arr else None

    @staticmethod
    def concat(*arrays: List[Any]) -> List[Any]:
        """Concatenate arrays."""
        result = []
        for arr in arrays:
            result.extend(arr)
        return result

    @staticmethod
    def slice(arr: List[Any], start: int, end: int = None) -> List[Any]:
        """Slice array."""
        if end is None:
            return arr[start:]
        return arr[start:end]

    @staticmethod
    def indexOf(arr: List[Any], element: Any) -> int:
        """Find index of element."""
        try:
            return arr.index(element)
        except ValueError:
            return -1

    @staticmethod
    def includes(arr: List[Any], element: Any) -> bool:
        """Check if array includes element."""
        return element in arr

    @staticmethod
    def reverse(arr: List[Any]) -> List[Any]:
        """Reverse array (returns new array)."""
        return arr[::-1]

    @staticmethod
    def sort(arr: List[Any], key_func: Callable = None) -> List[Any]:
        """Sort array (returns new array)."""
        return sorted(arr, key=key_func)

    @staticmethod
    def filter(arr: List[Any], predicate: Callable[[Any], bool]) -> List[Any]:
        """Filter array elements."""
        return [x for x in arr if predicate(x)]

    @staticmethod
    def map(arr: List[Any], transform: Callable[[Any], Any]) -> List[Any]:
        """Map array elements."""
        return [transform(x) for x in arr]

    @staticmethod
    def reduce(arr: List[Any], reducer: Callable[[Any, Any], Any], initial: Any = None) -> Any:
        """Reduce array to single value."""
        if not arr:
            return initial

        if initial is not None:
            result = initial
            start = 0
        else:
            result = arr[0]
            start = 1

        for i in range(start, len(arr)):
            result = reducer(result, arr[i])

        return result

    @staticmethod
    def forEach(arr: List[Any], callback: Callable[[Any], None]) -> None:
        """Execute callback for each element."""
        for element in arr:
            callback(element)

    @staticmethod
    def find(arr: List[Any], predicate: Callable[[Any], bool]) -> Any:
        """Find first element matching predicate."""
        for element in arr:
            if predicate(element):
                return element
        return None

    @staticmethod
    def some(arr: List[Any], predicate: Callable[[Any], bool]) -> bool:
        """Check if some elements match predicate."""
        return any(predicate(x) for x in arr)

    @staticmethod
    def every(arr: List[Any], predicate: Callable[[Any], bool]) -> bool:
        """Check if all elements match predicate."""
        return all(predicate(x) for x in arr)

    # Snake_case aliases for ML compatibility
    @staticmethod
    def from_args(*args: Any) -> List[Any]:
        """Create array from arguments (snake_case alias)."""
        return array_from(*args)

    @staticmethod
    def is_empty(arr: List[Any]) -> bool:
        """Check if array is empty (snake_case alias)."""
        return len(arr) == 0

    @staticmethod
    def index_of(arr: List[Any], element: Any) -> int:
        """Find index of element (snake_case alias)."""
        return Array.indexOf(arr, element)

    @staticmethod
    def for_each(arr: List[Any], callback: Callable[[Any], None]) -> None:
        """Execute callback for each element (snake_case alias)."""
        Array.forEach(arr, callback)

    # Properties
    @property
    def prototype(self):
        """Array prototype for ML compatibility."""
        return self

    # Static prototype methods for ML compatibility
    @staticmethod
    def shift(arr: List[Any]) -> Any:
        """Remove and return first element."""
        return arr.pop(0) if arr else None

    @staticmethod
    def unshift(arr: List[Any], *elements: Any) -> int:
        """Add elements to beginning of array."""
        for i, element in enumerate(elements):
            arr.insert(i, element)
        return len(arr)

    @staticmethod
    def push(arr: List[Any], *elements: Any) -> int:
        """Add elements to end of array."""
        arr.extend(elements)
        return len(arr)

    @staticmethod
    def pop(arr: List[Any]) -> Any:
        """Remove and return last element."""
        return arr.pop() if arr else None


# Create global array instance for ML compatibility
array = Array()

# Export all bridge functions and the array object
__all__ = [
    "Array",
    "array",
    "array_from",
    "array_of",
    "array_fill",
    "array_range",
]