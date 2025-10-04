"""Python bridge implementations for ML collections module.

The collections module provides functional list/array manipulation utilities.
When imported in ML code as 'import collections;', it creates a 'collections' object
with methods for working with lists and arrays.

Usage in ML:
    import collections;

    // List operations
    result = collections.append([1, 2, 3], 4);  // [1, 2, 3, 4]
    first = collections.first([10, 20, 30]);    // 10
    filtered = collections.filter(numbers, fn(n) => n > 5);
"""

from collections.abc import Callable
from typing import Any
from mlpy.stdlib.decorators import ml_module, ml_function


@ml_module(
    name="collections",
    description="Functional list and array manipulation utilities",
    capabilities=["collections.read", "collections.transform"],
    version="1.0.0"
)
class Collections:
    """Collections module interface for ML code.

    This class provides functional utilities for list/array operations.
    All methods are pure functions that return new data structures.
    """

    @ml_function(description="Get length of list", capabilities=["collections.read"])
    def length(self, lst: list[Any]) -> int:
        """Get length of a list.

        Args:
            lst: List to measure

        Returns:
            Number of elements in list
        """
        return len(lst)

    @ml_function(description="Append element to list", capabilities=["collections.transform"])
    def append(self, lst: list[Any], element: Any) -> list[Any]:
        """Add element to end of list, returning new list.

        Args:
            lst: Original list
            element: Element to append

        Returns:
            New list with element added to end
        """
        return lst + [element]

    @ml_function(description="Prepend element to list", capabilities=["collections.transform"])
    def prepend(self, lst: list[Any], element: Any) -> list[Any]:
        """Add element to beginning of list, returning new list.

        Args:
            lst: Original list
            element: Element to prepend

        Returns:
            New list with element added to beginning
        """
        return [element] + lst

    @ml_function(description="Concatenate two lists", capabilities=["collections.transform"])
    def concat(self, lst1: list[Any], lst2: list[Any]) -> list[Any]:
        """Concatenate two lists.

        Args:
            lst1: First list
            lst2: Second list

        Returns:
            New list containing all elements from both lists
        """
        return lst1 + lst2

    @ml_function(description="Get element at index", capabilities=["collections.read"])
    def get(self, lst: list[Any], index: int) -> Any | None:
        """Get element at index, return None if out of bounds.

        Args:
            lst: List to access
            index: Index of element

        Returns:
            Element at index, or None if index is out of bounds
        """
        try:
            return lst[index]
        except IndexError:
            return None

    @ml_function(description="Get first element", capabilities=["collections.read"])
    def first(self, lst: list[Any]) -> Any | None:
        """Get first element of list.

        Args:
            lst: List to access

        Returns:
            First element, or None if list is empty
        """
        return lst[0] if lst else None

    @ml_function(description="Get last element", capabilities=["collections.read"])
    def last(self, lst: list[Any]) -> Any | None:
        """Get last element of list.

        Args:
            lst: List to access

        Returns:
            Last element, or None if list is empty
        """
        return lst[-1] if lst else None

    @ml_function(description="Create slice of list", capabilities=["collections.transform"])
    def slice(self, lst: list[Any], start: int, end: int = None) -> list[Any]:
        """Create a slice of the list.

        Args:
            lst: List to slice
            start: Start index (inclusive)
            end: End index (exclusive), None for end of list

        Returns:
            New list containing slice
        """
        if end is None:
            return lst[start:]
        return lst[start:end]

    @ml_function(description="Reverse list", capabilities=["collections.transform"])
    def reverse(self, lst: list[Any]) -> list[Any]:
        """Reverse a list.

        Args:
            lst: List to reverse

        Returns:
            New list with elements in reverse order
        """
        return lst[::-1]

    @ml_function(description="Check if list contains element", capabilities=["collections.read"])
    def contains(self, lst: list[Any], element: Any) -> bool:
        """Check if list contains element.

        Args:
            lst: List to search
            element: Element to find

        Returns:
            True if element is in list, False otherwise
        """
        return element in lst

    @ml_function(description="Find index of element", capabilities=["collections.read"])
    def indexOf(self, lst: list[Any], element: Any) -> int:
        """Find index of element, return -1 if not found.

        Args:
            lst: List to search
            element: Element to find

        Returns:
            Index of element, or -1 if not found
        """
        try:
            return lst.index(element)
        except ValueError:
            return -1

    @ml_function(description="Filter list elements", capabilities=["collections.transform"])
    def filter(self, lst: list[Any], predicate: Callable[[Any], bool]) -> list[Any]:
        """Filter list elements matching predicate.

        Args:
            lst: List to filter
            predicate: Function that returns True for elements to keep

        Returns:
            New list containing only elements matching predicate
        """
        return [item for item in lst if predicate(item)]

    @ml_function(description="Transform list elements", capabilities=["collections.transform"])
    def map(self, lst: list[Any], transform: Callable[[Any], Any]) -> list[Any]:
        """Transform list elements with function.

        Args:
            lst: List to transform
            transform: Function to apply to each element

        Returns:
            New list with transformed elements
        """
        return [transform(item) for item in lst]

    @ml_function(description="Find first matching element", capabilities=["collections.read"])
    def find(self, lst: list[Any], predicate: Callable[[Any], bool]) -> Any | None:
        """Find first element matching predicate.

        Args:
            lst: List to search
            predicate: Function that returns True for desired element

        Returns:
            First matching element, or None if not found
        """
        for item in lst:
            if predicate(item):
                return item
        return None

    @ml_function(description="Reduce list to single value", capabilities=["collections.transform"])
    def reduce(self, lst: list[Any], reducer: Callable[[Any, Any], Any], initial: Any) -> Any:
        """Reduce list to single value using reducer function.

        Args:
            lst: List to reduce
            reducer: Function that combines accumulator and current element
            initial: Initial value for accumulator

        Returns:
            Final reduced value
        """
        result = initial
        for item in lst:
            result = reducer(result, item)
        return result

    @ml_function(description="Remove element at index", capabilities=["collections.transform"])
    def removeAt(self, lst: list[Any], index: int) -> list[Any]:
        """Remove element at specific index.

        Args:
            lst: List to modify
            index: Index of element to remove

        Returns:
            New list with element removed, or original list if index invalid
        """
        if 0 <= index < len(lst):
            return lst[:index] + lst[index + 1:]
        return lst

    @ml_function(description="Check if list is empty", capabilities=["collections.read"])
    def isEmpty(self, lst: list[Any]) -> bool:
        """Check if list is empty.

        Args:
            lst: List to check

        Returns:
            True if list is empty, False otherwise
        """
        return len(lst) == 0

    @ml_function(description="Take first N elements", capabilities=["collections.transform"])
    def take(self, lst: list[Any], count: int) -> list[Any]:
        """Take first N elements from list.

        Args:
            lst: List to take from
            count: Number of elements to take

        Returns:
            New list containing first N elements
        """
        return lst[:count]

    @ml_function(description="Drop first N elements", capabilities=["collections.transform"])
    def drop(self, lst: list[Any], count: int) -> list[Any]:
        """Drop first N elements from list.

        Args:
            lst: List to drop from
            count: Number of elements to drop

        Returns:
            New list with first N elements removed
        """
        return lst[count:]

    @ml_function(description="Create list with unique elements", capabilities=["collections.transform"])
    def unique(self, lst: list[Any]) -> list[Any]:
        """Create list with unique elements (preserves order).

        Args:
            lst: List to deduplicate

        Returns:
            New list with duplicates removed
        """
        seen = set()
        result = []
        for item in lst:
            # Handle unhashable types by using a try-except
            try:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            except TypeError:
                # For unhashable types, use linear search
                if item not in result:
                    result.append(item)
        return result

    @ml_function(description="Flatten nested list one level", capabilities=["collections.transform"])
    def flatten(self, lst: list[Any]) -> list[Any]:
        """Flatten nested list one level deep.

        Args:
            lst: List to flatten

        Returns:
            New flattened list
        """
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(item)
            else:
                result.append(item)
        return result

    @ml_function(description="Zip two lists together", capabilities=["collections.transform"])
    def zip(self, lst1: list[Any], lst2: list[Any]) -> list[tuple[Any, Any]]:
        """Zip two lists together into list of tuples.

        Args:
            lst1: First list
            lst2: Second list

        Returns:
            New list of tuples (element1, element2)
        """
        return list(zip(lst1, lst2))

    # Snake_case aliases for convenience
    @ml_function(description="Get element at index (snake_case alias)", capabilities=["collections.read"])
    def index_of(self, lst: list[Any], element: Any) -> int:
        """Alias for indexOf()."""
        return self.indexOf(lst, element)

    @ml_function(description="Remove at index (snake_case alias)", capabilities=["collections.transform"])
    def remove_at(self, lst: list[Any], index: int) -> list[Any]:
        """Alias for removeAt()."""
        return self.removeAt(lst, index)

    @ml_function(description="Check if empty (snake_case alias)", capabilities=["collections.read"])
    def is_empty(self, lst: list[Any]) -> bool:
        """Alias for isEmpty()."""
        return self.isEmpty(lst)


# Global collections instance for ML import
# When ML code does 'import collections;', this creates the 'collections' object
collections = Collections()


# Additional helper functions for ML bridge
def list_append_helper(lst: list[Any], element: Any) -> list[Any]:
    """Helper function for list append operations."""
    return collections.append(lst, element)


def list_concat_helper(lst1: list[Any], lst2: list[Any]) -> list[Any]:
    """Helper function for list concatenation."""
    return collections.concat(lst1, lst2)


# Export public API
__all__ = [
    "Collections",
    "collections",
    "list_append_helper",
    "list_concat_helper",
]
