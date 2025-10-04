"""Unit tests for builtin module migration."""

import pytest
from mlpy.stdlib.builtin import Builtin, builtin
from mlpy.stdlib.decorators import get_module_metadata, _MODULE_REGISTRY, ml_class


class TestBuiltinModuleRegistration:
    """Test that Builtin module is properly registered with decorators."""

    def test_builtin_module_registered(self):
        """Test that builtin module is in global registry."""
        assert "builtin" in _MODULE_REGISTRY
        assert _MODULE_REGISTRY["builtin"] == Builtin

    def test_builtin_module_metadata(self):
        """Test builtin module metadata is correct."""
        metadata = get_module_metadata("builtin")
        assert metadata is not None
        assert metadata.name == "builtin"
        assert metadata.description == "Core builtin functions always available without import"
        assert metadata.capabilities == []  # Builtin doesn't require capabilities
        assert metadata.version == "1.0.0"

    def test_builtin_has_function_metadata(self):
        """Test that builtin module has registered functions."""
        metadata = get_module_metadata("builtin")

        # Check key methods are registered
        assert "int" in metadata.functions
        assert "float" in metadata.functions
        assert "str" in metadata.functions
        assert "bool" in metadata.functions
        assert "typeof" in metadata.functions
        assert "isinstance" in metadata.functions
        assert "len" in metadata.functions
        assert "range" in metadata.functions
        assert "print" in metadata.functions
        assert "help" in metadata.functions
        assert "methods" in metadata.functions
        assert "modules" in metadata.functions
        assert "abs" in metadata.functions
        assert "min" in metadata.functions
        assert "max" in metadata.functions

        # Should have many functions (22+)
        assert len(metadata.functions) >= 22


class TestTypeConversionFunctions:
    """Test type conversion builtin functions."""

    def test_int_from_float(self):
        """Test int() converts float to int."""
        assert builtin.int(3.14) == 3
        assert builtin.int(9.99) == 9

    def test_int_from_string(self):
        """Test int() converts string to int."""
        assert builtin.int("42") == 42
        assert builtin.int("100") == 100

    def test_int_from_float_string(self):
        """Test int() converts float string to int."""
        assert builtin.int("3.14") == 3
        assert builtin.int("9.99") == 9

    def test_int_from_boolean(self):
        """Test int() converts boolean to int."""
        assert builtin.int(True) == 1
        assert builtin.int(False) == 0

    def test_int_error_handling(self):
        """Test int() returns 0 on error."""
        assert builtin.int("invalid") == 0
        assert builtin.int(None) == 0

    def test_float_from_int(self):
        """Test float() converts int to float."""
        assert builtin.float(42) == 42.0
        assert builtin.float(100) == 100.0

    def test_float_from_string(self):
        """Test float() converts string to float."""
        assert builtin.float("3.14") == 3.14
        assert builtin.float("2.5") == 2.5

    def test_float_from_boolean(self):
        """Test float() converts boolean to float."""
        assert builtin.float(True) == 1.0
        assert builtin.float(False) == 0.0

    def test_float_error_handling(self):
        """Test float() returns 0.0 on error."""
        assert builtin.float("invalid") == 0.0
        assert builtin.float(None) == 0.0

    def test_str_from_number(self):
        """Test str() converts numbers to string."""
        assert builtin.str(42) == "42"
        assert builtin.str(3.14) == "3.14"

    def test_str_from_boolean(self):
        """Test str() converts boolean to ML-compatible string."""
        # ML uses lowercase true/false
        assert builtin.str(True) == "true"
        assert builtin.str(False) == "false"

    def test_bool_conversion(self):
        """Test bool() converts values to boolean."""
        assert builtin.bool(1) is True
        assert builtin.bool(0) is False
        assert builtin.bool("hello") is True
        assert builtin.bool("") is False
        assert builtin.bool([1, 2, 3]) is True
        assert builtin.bool([]) is False


class TestTypeCheckingFunctions:
    """Test type checking builtin functions."""

    def test_typeof_boolean(self):
        """Test typeof() identifies boolean type."""
        assert builtin.typeof(True) == "boolean"
        assert builtin.typeof(False) == "boolean"

    def test_typeof_number(self):
        """Test typeof() identifies number type."""
        assert builtin.typeof(42) == "number"
        assert builtin.typeof(3.14) == "number"

    def test_typeof_string(self):
        """Test typeof() identifies string type."""
        assert builtin.typeof("hello") == "string"
        assert builtin.typeof("") == "string"

    def test_typeof_array(self):
        """Test typeof() identifies array type."""
        assert builtin.typeof([1, 2, 3]) == "array"
        assert builtin.typeof([]) == "array"

    def test_typeof_object(self):
        """Test typeof() identifies object type."""
        assert builtin.typeof({"a": 1, "b": 2}) == "object"
        assert builtin.typeof({}) == "object"

    def test_typeof_function(self):
        """Test typeof() identifies function type."""
        assert builtin.typeof(lambda x: x) == "function"
        assert builtin.typeof(builtin.typeof) == "function"

    def test_typeof_with_ml_class_metadata(self):
        """Test typeof() recognizes @ml_class decorated classes."""
        # Create a test class with @ml_class metadata
        @ml_class(description="Test class")
        class TestClass:
            pass

        instance = TestClass()
        # Should return "TestClass" not "object"
        assert builtin.typeof(instance) == "TestClass"

    def test_isinstance_primitive_types(self):
        """Test isinstance() with primitive types."""
        assert builtin.isinstance(42, "number") is True
        assert builtin.isinstance("hello", "string") is True
        assert builtin.isinstance(True, "boolean") is True
        assert builtin.isinstance([1, 2, 3], "array") is True
        assert builtin.isinstance({"a": 1}, "object") is True

    def test_isinstance_negative_cases(self):
        """Test isinstance() returns false for wrong types."""
        assert builtin.isinstance(42, "string") is False
        assert builtin.isinstance("hello", "number") is False
        assert builtin.isinstance([1, 2, 3], "object") is False

    def test_isinstance_with_custom_classes(self):
        """Test isinstance() with @ml_class decorated classes."""
        @ml_class(description="Custom class")
        class CustomClass:
            pass

        instance = CustomClass()
        assert builtin.isinstance(instance, "CustomClass") is True
        assert builtin.isinstance(instance, "object") is False


class TestCollectionFunctions:
    """Test collection builtin functions."""

    def test_len_string(self):
        """Test len() with strings."""
        assert builtin.len("hello") == 5
        assert builtin.len("") == 0

    def test_len_array(self):
        """Test len() with arrays."""
        assert builtin.len([1, 2, 3]) == 3
        assert builtin.len([]) == 0

    def test_len_object(self):
        """Test len() with objects."""
        assert builtin.len({"a": 1, "b": 2, "c": 3}) == 3
        assert builtin.len({}) == 0

    def test_len_error_handling(self):
        """Test len() returns 0 for non-collections."""
        assert builtin.len(42) == 0
        assert builtin.len(None) == 0

    def test_range_single_arg(self):
        """Test range() with single argument."""
        assert builtin.range(5) == [0, 1, 2, 3, 4]
        assert builtin.range(3) == [0, 1, 2]

    def test_range_two_args(self):
        """Test range() with start and stop."""
        assert builtin.range(1, 5) == [1, 2, 3, 4]
        assert builtin.range(2, 7) == [2, 3, 4, 5, 6]

    def test_range_three_args(self):
        """Test range() with start, stop, and step."""
        assert builtin.range(0, 10, 2) == [0, 2, 4, 6, 8]
        assert builtin.range(1, 10, 3) == [1, 4, 7]

    def test_enumerate_basic(self):
        """Test enumerate() with default start."""
        result = builtin.enumerate(['a', 'b', 'c'])
        assert result == [(0, 'a'), (1, 'b'), (2, 'c')]

    def test_enumerate_custom_start(self):
        """Test enumerate() with custom start index."""
        result = builtin.enumerate(['a', 'b', 'c'], 1)
        assert result == [(1, 'a'), (2, 'b'), (3, 'c')]

    def test_enumerate_empty_array(self):
        """Test enumerate() with empty array."""
        result = builtin.enumerate([])
        assert result == []


class TestIOFunctions:
    """Test I/O builtin functions."""

    def test_print_single_value(self, capsys):
        """Test print() with single value."""
        builtin.print("hello")
        captured = capsys.readouterr()
        assert captured.out == "hello\n"

    def test_print_multiple_values(self, capsys):
        """Test print() with multiple values."""
        builtin.print("hello", "world")
        captured = capsys.readouterr()
        assert captured.out == "hello world\n"

    def test_print_boolean_formatting(self, capsys):
        """Test print() uses ML boolean formatting."""
        builtin.print(True, False)
        captured = capsys.readouterr()
        assert captured.out == "true false\n"

    def test_input_with_prompt(self, monkeypatch):
        """Test input() with prompt."""
        monkeypatch.setattr('builtins.input', lambda x: "test input")
        result = builtin.input("Enter text: ")
        assert result == "test input"

    def test_input_without_prompt(self, monkeypatch):
        """Test input() without prompt."""
        monkeypatch.setattr('builtins.input', lambda x: "test")
        result = builtin.input()
        assert result == "test"


class TestIntrospectionFunctions:
    """Test introspection builtin functions."""

    def test_help_with_ml_function(self):
        """Test help() with @ml_function decorated function."""
        help_text = builtin.help(builtin.typeof)
        assert "type of value" in help_text.lower()

    def test_help_with_ml_module(self):
        """Test help() with @ml_module decorated module."""
        from mlpy.stdlib.console_bridge import Console
        help_text = builtin.help(Console)
        # Should return module description from metadata
        assert "console" in help_text.lower() or "no description" in help_text.lower()

    def test_help_with_no_metadata(self):
        """Test help() with object without metadata."""
        def plain_function():
            """Plain function docstring."""
            pass

        help_text = builtin.help(plain_function)
        assert "Plain function docstring" in help_text or "No help" in help_text

    def test_methods_returns_list(self):
        """Test methods() returns list of method names."""
        result = builtin.methods("hello")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_methods_for_string(self):
        """Test methods() for string includes expected methods."""
        result = builtin.methods("hello")
        # Should include common string methods
        assert any(method in result for method in ['upper', 'lower', 'split'])

    def test_methods_for_array(self):
        """Test methods() for array includes expected methods."""
        result = builtin.methods([1, 2, 3])
        # Should include common list methods
        assert any(method in result for method in ['append', 'pop', 'sort'])

    def test_modules_returns_list(self):
        """Test modules() returns list of module names."""
        result = builtin.modules()
        assert isinstance(result, list)
        assert "builtin" in result


class TestMathUtilityFunctions:
    """Test math utility builtin functions."""

    def test_abs_positive(self):
        """Test abs() with positive numbers."""
        assert builtin.abs(5) == 5
        assert builtin.abs(3.14) == 3.14

    def test_abs_negative(self):
        """Test abs() with negative numbers."""
        assert builtin.abs(-5) == 5
        assert builtin.abs(-3.14) == 3.14

    def test_abs_zero(self):
        """Test abs() with zero."""
        assert builtin.abs(0) == 0

    def test_min_multiple_args(self):
        """Test min() with multiple arguments."""
        assert builtin.min(5, 2, 8, 1, 9) == 1
        assert builtin.min(3.14, 2.5, 9.0) == 2.5

    def test_min_array_arg(self):
        """Test min() with array argument."""
        assert builtin.min([5, 2, 8, 1, 9]) == 1
        assert builtin.min([3.14, 2.5, 9.0]) == 2.5

    def test_min_empty(self):
        """Test min() with empty array."""
        assert builtin.min([]) is None

    def test_max_multiple_args(self):
        """Test max() with multiple arguments."""
        assert builtin.max(5, 2, 8, 1, 9) == 9
        assert builtin.max(3.14, 2.5, 9.0) == 9.0

    def test_max_array_arg(self):
        """Test max() with array argument."""
        assert builtin.max([5, 2, 8, 1, 9]) == 9
        assert builtin.max([3.14, 2.5, 9.0]) == 9.0

    def test_max_empty(self):
        """Test max() with empty array."""
        assert builtin.max([]) is None

    def test_round_no_precision(self):
        """Test round() without precision."""
        assert builtin.round(3.14159) == 3.0
        assert builtin.round(2.5) == 2.0

    def test_round_with_precision(self):
        """Test round() with precision."""
        assert builtin.round(3.14159, 2) == 3.14
        assert builtin.round(3.14159, 3) == 3.142


class TestAdditionalUtilities:
    """Test additional utility builtin functions."""

    def test_zip_two_arrays(self):
        """Test zip() with two arrays."""
        result = builtin.zip([1, 2, 3], ['a', 'b', 'c'])
        assert result == [(1, 'a'), (2, 'b'), (3, 'c')]

    def test_zip_three_arrays(self):
        """Test zip() with three arrays."""
        result = builtin.zip([1, 2], ['a', 'b'], [True, False])
        assert result == [(1, 'a', True), (2, 'b', False)]

    def test_zip_different_lengths(self):
        """Test zip() with different length arrays."""
        result = builtin.zip([1, 2, 3], ['a', 'b'])
        # Zip stops at shortest array
        assert result == [(1, 'a'), (2, 'b')]

    def test_sorted_ascending(self):
        """Test sorted() in ascending order."""
        result = builtin.sorted([3, 1, 4, 1, 5, 9, 2, 6])
        assert result == [1, 1, 2, 3, 4, 5, 6, 9]

    def test_sorted_descending(self):
        """Test sorted() in descending order."""
        result = builtin.sorted([3, 1, 4, 1, 5, 9, 2, 6], reverse=True)
        assert result == [9, 6, 5, 4, 3, 2, 1, 1]

    def test_sorted_strings(self):
        """Test sorted() with strings."""
        result = builtin.sorted(['banana', 'apple', 'cherry'])
        assert result == ['apple', 'banana', 'cherry']

    def test_keys_basic(self):
        """Test keys() returns object keys."""
        result = builtin.keys({"a": 1, "b": 2, "c": 3})
        assert sorted(result) == ["a", "b", "c"]

    def test_keys_empty_object(self):
        """Test keys() with empty object."""
        result = builtin.keys({})
        assert result == []

    def test_values_basic(self):
        """Test values() returns object values."""
        result = builtin.values({"a": 1, "b": 2, "c": 3})
        assert sorted(result) == [1, 2, 3]

    def test_values_empty_object(self):
        """Test values() with empty object."""
        result = builtin.values({})
        assert result == []


class TestBuiltinInstance:
    """Test global builtin instance."""

    def test_builtin_is_instance_of_builtin_class(self):
        """Test that builtin is an instance of Builtin."""
        assert isinstance(builtin, Builtin)

    def test_builtin_has_decorated_methods(self):
        """Test that builtin instance has decorated methods with metadata."""
        assert hasattr(builtin, "typeof")
        assert hasattr(builtin, "len")
        assert hasattr(builtin, "print")

        # Check they have metadata
        assert hasattr(builtin.typeof, "_ml_function_metadata")
        assert hasattr(builtin.len, "_ml_function_metadata")
        assert hasattr(builtin.print, "_ml_function_metadata")


class TestHelperFunctions:
    """Test helper functions for ML bridge."""

    def test_typeof_helper(self):
        """Test typeof_helper() function."""
        from mlpy.stdlib.builtin import typeof_helper

        assert typeof_helper(42) == "number"
        assert typeof_helper("hello") == "string"
        assert typeof_helper(True) == "boolean"

    def test_len_helper(self):
        """Test len_helper() function."""
        from mlpy.stdlib.builtin import len_helper

        assert len_helper("hello") == 5
        assert len_helper([1, 2, 3]) == 3

    def test_print_helper(self, capsys):
        """Test print_helper() function."""
        from mlpy.stdlib.builtin import print_helper

        print_helper("test", 42)
        captured = capsys.readouterr()
        assert "test" in captured.out
        assert "42" in captured.out


class TestMLCompatibility:
    """Test ML language compatibility and edge cases."""

    def test_boolean_formatting_consistency(self):
        """Test all boolean formatting is ML-compatible."""
        # str() should use lowercase
        assert builtin.str(True) == "true"
        assert builtin.str(False) == "false"

    def test_type_conversion_chaining(self):
        """Test type conversions can be chained."""
        # String -> Float -> Int
        result = builtin.int(builtin.float("3.14"))
        assert result == 3

        # Int -> Str -> Float (should fail gracefully)
        result = builtin.float(builtin.str(42))
        assert result == 42.0

    def test_typeof_comprehensive_coverage(self):
        """Test typeof() covers all ML types."""
        types_covered = {
            "boolean": True,
            "number": 42,
            "string": "hello",
            "array": [1, 2, 3],
            "object": {"a": 1},
            "function": lambda x: x
        }

        for expected_type, value in types_covered.items():
            assert builtin.typeof(value) == expected_type

    def test_error_recovery_robustness(self):
        """Test error handling doesn't raise exceptions."""
        # int() with invalid input
        assert builtin.int("not a number") == 0
        assert builtin.int(None) == 0

        # float() with invalid input
        assert builtin.float("not a number") == 0.0
        assert builtin.float(None) == 0.0

        # len() with non-collection
        assert builtin.len(42) == 0
        assert builtin.len(None) == 0
