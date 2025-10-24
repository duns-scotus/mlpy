"""Unit tests for collections_bridge module migration."""

import pytest
from mlpy.stdlib.collections_bridge import Collections, collections
from mlpy.stdlib.decorators import get_module_metadata, _MODULE_REGISTRY


class TestCollectionsModuleRegistration:
    """Test that Collections module is properly registered with decorators."""

    def test_collections_module_registered(self):
        """Test that collections module is in global registry."""
        assert "collections" in _MODULE_REGISTRY
        assert _MODULE_REGISTRY["collections"] == Collections

    def test_collections_module_metadata(self):
        """Test collections module metadata is correct."""
        metadata = get_module_metadata("collections")
        assert metadata is not None
        assert metadata.name == "collections"
        assert metadata.description == "Functional list and array manipulation utilities"
        assert "collections.read" in metadata.capabilities
        assert "collections.transform" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_collections_has_function_metadata(self):
        """Test that collections module has registered functions."""
        metadata = get_module_metadata("collections")

        # Check key methods are registered
        assert "length" in metadata.functions
        assert "append" in metadata.functions
        assert "prepend" in metadata.functions
        assert "concat" in metadata.functions
        assert "filter" in metadata.functions
        assert "map" in metadata.functions
        assert "reduce" in metadata.functions
        assert "find" in metadata.functions

        # Should have many functions (25+)
        assert len(metadata.functions) >= 25


class TestCollectionsBasicOperations:
    """Test basic collections operations."""

    def test_length(self):
        """Test length() method."""
        assert collections.length([1, 2, 3]) == 3
        assert collections.length([]) == 0
        assert collections.length([1]) == 1

    def test_append(self):
        """Test append() method."""
        result = collections.append([1, 2, 3], 4)
        assert result == [1, 2, 3, 4]
        assert result is not [1, 2, 3]  # Returns new list

    def test_prepend(self):
        """Test prepend() method."""
        result = collections.prepend([2, 3, 4], 1)
        assert result == [1, 2, 3, 4]
        assert result is not [2, 3, 4]  # Returns new list

    def test_concat(self):
        """Test concat() method."""
        result = collections.concat([1, 2], [3, 4])
        assert result == [1, 2, 3, 4]

    def test_get(self):
        """Test get() method."""
        lst = [10, 20, 30]
        assert collections.get(lst, 0) == 10
        assert collections.get(lst, 2) == 30
        assert collections.get(lst, 5) is None  # Out of bounds
        assert collections.get(lst, -1) == 30  # Negative index

    def test_first(self):
        """Test first() method."""
        assert collections.first([1, 2, 3]) == 1
        assert collections.first([10]) == 10
        assert collections.first([]) is None

    def test_last(self):
        """Test last() method."""
        assert collections.last([1, 2, 3]) == 3
        assert collections.last([10]) == 10
        assert collections.last([]) is None


class TestCollectionsTransformations:
    """Test collections transformation operations."""

    def test_slice(self):
        """Test slice() method."""
        lst = [1, 2, 3, 4, 5]
        assert collections.slice(lst, 1, 3) == [2, 3]
        assert collections.slice(lst, 2) == [3, 4, 5]
        assert collections.slice(lst, 0, 2) == [1, 2]

    def test_reverse(self):
        """Test reverse() method."""
        result = collections.reverse([1, 2, 3])
        assert result == [3, 2, 1]

    def test_contains(self):
        """Test contains() method."""
        lst = [1, 2, 3]
        assert collections.contains(lst, 2) is True
        assert collections.contains(lst, 5) is False

    def test_indexOf(self):
        """Test indexOf() method."""
        lst = [10, 20, 30]
        assert collections.indexOf(lst, 20) == 1
        assert collections.indexOf(lst, 10) == 0
        assert collections.indexOf(lst, 99) == -1  # Not found

    def test_filter(self):
        """Test filter() method."""
        lst = [1, 2, 3, 4, 5]
        result = collections.filter(lst, lambda x: x > 2)
        assert result == [3, 4, 5]

        result = collections.filter(lst, lambda x: x % 2 == 0)
        assert result == [2, 4]

    def test_map(self):
        """Test map() method."""
        lst = [1, 2, 3]
        result = collections.map(lst, lambda x: x * 2)
        assert result == [2, 4, 6]

        result = collections.map(lst, lambda x: x + 10)
        assert result == [11, 12, 13]

    def test_find(self):
        """Test find() method."""
        lst = [1, 2, 3, 4, 5]
        result = collections.find(lst, lambda x: x > 3)
        assert result == 4  # First element > 3

        result = collections.find(lst, lambda x: x > 10)
        assert result is None  # No match

    def test_reduce(self):
        """Test reduce() method."""
        lst = [1, 2, 3, 4]
        # Sum all elements
        result = collections.reduce(lst, lambda acc, x: acc + x, 0)
        assert result == 10

        # Multiply all elements
        result = collections.reduce(lst, lambda acc, x: acc * x, 1)
        assert result == 24

    def test_removeAt(self):
        """Test removeAt() method."""
        lst = [1, 2, 3, 4]
        result = collections.removeAt(lst, 1)
        assert result == [1, 3, 4]

        result = collections.removeAt(lst, 0)
        assert result == [2, 3, 4]

        result = collections.removeAt(lst, 10)  # Out of bounds
        assert result == lst


class TestCollectionsUtilities:
    """Test collections utility methods."""

    def test_isEmpty(self):
        """Test isEmpty() method."""
        assert collections.isEmpty([]) is True
        assert collections.isEmpty([1]) is False
        assert collections.isEmpty([1, 2, 3]) is False

    def test_take(self):
        """Test take() method."""
        lst = [1, 2, 3, 4, 5]
        assert collections.take(lst, 3) == [1, 2, 3]
        assert collections.take(lst, 1) == [1]
        assert collections.take(lst, 0) == []
        assert collections.take(lst, 10) == lst  # Takes all available

    def test_drop(self):
        """Test drop() method."""
        lst = [1, 2, 3, 4, 5]
        assert collections.drop(lst, 2) == [3, 4, 5]
        assert collections.drop(lst, 1) == [2, 3, 4, 5]
        assert collections.drop(lst, 0) == lst
        assert collections.drop(lst, 10) == []  # Drops all

    def test_unique(self):
        """Test unique() method."""
        lst = [1, 2, 2, 3, 3, 3, 4]
        result = collections.unique(lst)
        assert result == [1, 2, 3, 4]

        lst = [1, 1, 1, 1]
        result = collections.unique(lst)
        assert result == [1]

        lst = []
        result = collections.unique(lst)
        assert result == []

    def test_unique_preserves_order(self):
        """Test that unique() preserves original order."""
        lst = [3, 1, 2, 1, 3, 2]
        result = collections.unique(lst)
        assert result == [3, 1, 2]  # First occurrence order

    def test_flatten(self):
        """Test flatten() method."""
        lst = [[1, 2], [3, 4], [5]]
        result = collections.flatten(lst)
        assert result == [1, 2, 3, 4, 5]

        lst = [[1], [2, 3], [], [4, 5]]
        result = collections.flatten(lst)
        assert result == [1, 2, 3, 4, 5]

    def test_flatten_mixed_types(self):
        """Test flatten() with mixed types."""
        lst = [[1, 2], 3, [4, 5]]
        result = collections.flatten(lst)
        assert result == [1, 2, 3, 4, 5]

    def test_zip(self):
        """Test zip() method."""
        lst1 = [1, 2, 3]
        lst2 = ['a', 'b', 'c']
        result = collections.zip(lst1, lst2)
        assert result == [(1, 'a'), (2, 'b'), (3, 'c')]

    def test_zip_different_lengths(self):
        """Test zip() with different length lists."""
        lst1 = [1, 2, 3]
        lst2 = ['a', 'b']
        result = collections.zip(lst1, lst2)
        assert result == [(1, 'a'), (2, 'b')]  # Stops at shortest


class TestCollectionsSnakeCaseAliases:
    """Test snake_case aliases for methods."""

    def test_index_of_alias(self):
        """Test index_of() alias."""
        lst = [10, 20, 30]
        assert collections.index_of(lst, 20) == 1
        assert collections.index_of(lst, 99) == -1

    def test_remove_at_alias(self):
        """Test remove_at() alias."""
        lst = [1, 2, 3, 4]
        result = collections.remove_at(lst, 1)
        assert result == [1, 3, 4]

    def test_is_empty_alias(self):
        """Test is_empty() alias."""
        assert collections.is_empty([]) is True
        assert collections.is_empty([1]) is False


class TestCollectionsInstance:
    """Test global collections instance."""

    def test_collections_is_instance_of_collections_class(self):
        """Test that collections is an instance of Collections."""
        assert isinstance(collections, Collections)

    def test_collections_has_decorated_methods(self):
        """Test that collections instance has decorated methods with metadata."""
        assert hasattr(collections, "append")
        assert hasattr(collections, "filter")
        assert hasattr(collections, "map")

        # Check they have metadata
        assert hasattr(collections.append, "_ml_function_metadata")
        assert hasattr(collections.filter, "_ml_function_metadata")
        assert hasattr(collections.map, "_ml_function_metadata")


class TestCollectionsHelperFunctions:
    """Test helper functions for ML bridge."""

    def test_list_append_helper(self):
        """Test list_append_helper() function."""
        from mlpy.stdlib.collections_bridge import list_append_helper

        result = list_append_helper([1, 2], 3)
        assert result == [1, 2, 3]

    def test_list_concat_helper(self):
        """Test list_concat_helper() function."""
        from mlpy.stdlib.collections_bridge import list_concat_helper

        result = list_concat_helper([1, 2], [3, 4])
        assert result == [1, 2, 3, 4]


class TestCollectionsEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_list_operations(self):
        """Test operations on empty lists."""
        empty = []
        assert collections.length(empty) == 0
        assert collections.first(empty) is None
        assert collections.last(empty) is None
        assert collections.reverse(empty) == []
        assert collections.unique(empty) == []
        assert collections.flatten(empty) == []

    def test_single_element_operations(self):
        """Test operations on single-element lists."""
        single = [42]
        assert collections.length(single) == 1
        assert collections.first(single) == 42
        assert collections.last(single) == 42
        assert collections.reverse(single) == [42]
        assert collections.unique(single) == [42]

    def test_immutability(self):
        """Test that operations return new lists (immutable)."""
        original = [1, 2, 3]
        result = collections.append(original, 4)
        assert original == [1, 2, 3]  # Original unchanged
        assert result == [1, 2, 3, 4]

        result = collections.reverse(original)
        assert original == [1, 2, 3]  # Original unchanged
        assert result == [3, 2, 1]


class TestCollectionsMissingCoverage:
    """Test cases to cover missing lines."""

    def test_unique_with_unhashable_types(self):
        """Test unique() with unhashable types (lists/dicts)."""
        # Lists are unhashable - should trigger TypeError handling
        lst = [[1, 2], [3, 4], [1, 2], [5, 6]]
        result = collections.unique(lst)
        assert len(result) == 3
        assert [1, 2] in result
        assert [3, 4] in result
        assert [5, 6] in result

    def test_sort_reverse_order(self):
        """Test sort() with reverse=True."""
        lst = [3, 1, 4, 1, 5, 9, 2, 6]
        result = collections.sort(lst, reverse=True)
        assert result == [9, 6, 5, 4, 3, 2, 1, 1]

    def test_sort_by_reverse_order(self):
        """Test sortBy() with reverse=True and key function."""
        lst = ["apple", "pie", "a", "longer"]
        result = collections.sortBy(lst, lambda x: len(x), reverse=True)
        assert result == ["longer", "apple", "pie", "a"]

    def test_chunk_with_zero_size(self):
        """Test chunk() with size=0 returns empty list."""
        lst = [1, 2, 3, 4, 5]
        result = collections.chunk(lst, 0)
        assert result == []

    def test_chunk_with_negative_size(self):
        """Test chunk() with negative size returns empty list."""
        lst = [1, 2, 3, 4, 5]
        result = collections.chunk(lst, -5)
        assert result == []

    def test_every_predicate(self):
        """Test every() with predicate function."""
        # All elements match
        assert collections.every([2, 4, 6, 8], lambda x: x % 2 == 0) is True
        # Not all match
        assert collections.every([2, 3, 4, 6], lambda x: x % 2 == 0) is False
        # Empty list
        assert collections.every([], lambda x: x > 0) is True

    def test_some_predicate(self):
        """Test some() with predicate function."""
        # At least one matches
        assert collections.some([1, 3, 4, 7], lambda x: x % 2 == 0) is True
        # None match
        assert collections.some([1, 3, 5, 7], lambda x: x % 2 == 0) is False
        # Empty list
        assert collections.some([], lambda x: x > 0) is False
