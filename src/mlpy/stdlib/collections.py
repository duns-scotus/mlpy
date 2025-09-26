"""ML Collections Standard Library - Python Implementation."""

from collections.abc import Callable
from typing import Any


class Collections:
    """ML collections operations implemented in Python."""

    @staticmethod
    def length(lst: list[Any]) -> int:
        """Get length of a list."""
        return len(lst)

    @staticmethod
    def append(lst: list[Any], element: Any) -> list[Any]:
        """Add element to end of list, returning new list."""
        return lst + [element]

    @staticmethod
    def prepend(lst: list[Any], element: Any) -> list[Any]:
        """Add element to beginning of list, returning new list."""
        return [element] + lst

    @staticmethod
    def concat(lst1: list[Any], lst2: list[Any]) -> list[Any]:
        """Concatenate two lists."""
        return lst1 + lst2

    @staticmethod
    def get(lst: list[Any], index: int) -> Any | None:
        """Get element at index, return None if out of bounds."""
        try:
            return lst[index]
        except IndexError:
            return None

    @staticmethod
    def first(lst: list[Any]) -> Any | None:
        """Get first element."""
        return lst[0] if lst else None

    @staticmethod
    def last(lst: list[Any]) -> Any | None:
        """Get last element."""
        return lst[-1] if lst else None

    @staticmethod
    def slice(lst: list[Any], start: int, end: int = None) -> list[Any]:
        """Create a slice of the list."""
        if end is None:
            return lst[start:]
        return lst[start:end]

    @staticmethod
    def reverse(lst: list[Any]) -> list[Any]:
        """Reverse a list."""
        return lst[::-1]

    @staticmethod
    def contains(lst: list[Any], element: Any) -> bool:
        """Check if list contains element."""
        return element in lst

    @staticmethod
    def indexOf(lst: list[Any], element: Any) -> int:
        """Find index of element, return -1 if not found."""
        try:
            return lst.index(element)
        except ValueError:
            return -1

    @staticmethod
    def filter(lst: list[Any], predicate: Callable[[Any], bool]) -> list[Any]:
        """Filter list elements matching predicate."""
        return [item for item in lst if predicate(item)]

    @staticmethod
    def map(lst: list[Any], transform: Callable[[Any], Any]) -> list[Any]:
        """Transform list elements with function."""
        return [transform(item) for item in lst]

    @staticmethod
    def find(lst: list[Any], predicate: Callable[[Any], bool]) -> Any | None:
        """Find first element matching predicate."""
        for item in lst:
            if predicate(item):
                return item
        return None

    @staticmethod
    def reduce(lst: list[Any], reducer: Callable[[Any, Any], Any], initial: Any) -> Any:
        """Reduce list to single value."""
        result = initial
        for item in lst:
            result = reducer(result, item)
        return result

    @staticmethod
    def removeAt(lst: list[Any], index: int) -> list[Any]:
        """Remove element at specific index."""
        if 0 <= index < len(lst):
            return lst[:index] + lst[index + 1 :]
        return lst


# Global collections instance for ML programs
collections = Collections()


# Additional helper functions for ML bridge
def list_append_helper(lst: list[Any], element: Any) -> list[Any]:
    """Helper function for list append operations."""
    return collections.append(lst, element)


def list_concat_helper(lst1: list[Any], lst2: list[Any]) -> list[Any]:
    """Helper function for list concatenation."""
    return collections.concat(lst1, lst2)
