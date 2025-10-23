"""Unit tests for new builtin module functions (Phase 4B enhancements).

Tests for:
- Dynamic introspection: hasattr(), getattr(), call()
- Safe utilities: callable(), all(), any(), sum(), chr(), ord(),
  hex(), bin(), oct(), repr(), format(), reversed()
"""

import pytest
from mlpy.stdlib.builtin import Builtin, builtin


class TestDynamicIntrospection:
    """Test dynamic introspection functions (hasattr, getattr, call)."""

    def test_hasattr_safe_attribute(self):
        """Test hasattr() with safe attributes."""
        assert builtin.hasattr("hello", "upper") is True
        assert builtin.hasattr([1, 2, 3], "append") is True
        assert builtin.hasattr({}, "keys") is True

    def test_hasattr_unsafe_attribute(self):
        """Test hasattr() blocks unsafe attributes."""
        assert builtin.hasattr("test", "__class__") is False
        assert builtin.hasattr([], "__dict__") is False

    def test_hasattr_nonexistent_attribute(self):
        """Test hasattr() with nonexistent attributes."""
        assert builtin.hasattr("test", "nonexistent") is False

    def test_getattr_safe_attribute(self):
        """Test getattr() with safe attributes."""
        upper_method = builtin.getattr("hello", "upper")
        assert callable(upper_method)
        assert upper_method() == "HELLO"

    def test_getattr_with_default(self):
        """Test getattr() returns default value."""
        result = builtin.getattr("test", "nonexistent", "default")
        assert result == "default"

    def test_getattr_blocks_dangerous_attributes(self):
        """Test getattr() blocks dangerous attributes."""
        result = builtin.getattr("test", "__class__", "BLOCKED")
        assert result == "BLOCKED"

    def test_call_with_function(self):
        """Test call() invokes functions."""
        result = builtin.call(builtin.abs, -5)
        assert result == 5

    def test_call_with_lambda(self):
        """Test call() with lambda functions."""
        result = builtin.call(lambda x, y: x + y, 3, 4)
        assert result == 7

    def test_call_with_method(self):
        """Test call() with methods from getattr."""
        upper = builtin.getattr("hello", "upper")
        result = builtin.call(upper)
        assert result == "HELLO"

    def test_call_rejects_non_callable(self):
        """Test call() raises TypeError for non-callable."""
        with pytest.raises(TypeError):
            builtin.call(42)


class TestSafeUtilityFunctions:
    """Test safe utility functions."""

    def test_callable_with_function(self):
        """Test callable() returns True for functions."""
        assert builtin.callable(builtin.print) is True
        assert builtin.callable(lambda x: x) is True

    def test_callable_with_non_callable(self):
        """Test callable() returns False for non-callable."""
        assert builtin.callable(42) is False
        assert builtin.callable("string") is False

    def test_all_truthy_values(self):
        """Test all() with all truthy values."""
        assert builtin.all([True, True, True]) is True
        assert builtin.all([1, 2, 3]) is True

    def test_all_with_falsy_value(self):
        """Test all() with falsy value."""
        assert builtin.all([True, False, True]) is False
        assert builtin.all([1, 0, 3]) is False

    def test_all_empty_list(self):
        """Test all() with empty list."""
        assert builtin.all([]) is True

    def test_any_with_truthy_value(self):
        """Test any() with truthy value."""
        assert builtin.any([False, False, True]) is True
        assert builtin.any([0, 0, 1]) is True

    def test_any_all_falsy(self):
        """Test any() with all falsy values."""
        assert builtin.any([False, False, False]) is False
        assert builtin.any([0, 0, 0]) is False

    def test_any_empty_list(self):
        """Test any() with empty list."""
        assert builtin.any([]) is False

    def test_sum_integers(self):
        """Test sum() with integers."""
        assert builtin.sum([1, 2, 3, 4]) == 10

    def test_sum_floats(self):
        """Test sum() with floats."""
        assert builtin.sum([1.5, 2.5, 3.0]) == 7.0

    def test_sum_with_start(self):
        """Test sum() with start value."""
        assert builtin.sum([1, 2, 3], 10) == 16

    def test_sum_empty_list(self):
        """Test sum() with empty list."""
        assert builtin.sum([]) == 0

    def test_chr_ascii(self):
        """Test chr() with ASCII values."""
        assert builtin.chr(65) == "A"
        assert builtin.chr(97) == "a"

    def test_chr_unicode(self):
        """Test chr() with Unicode values."""
        assert builtin.chr(8364) == "€"
        assert builtin.chr(9728) == "☀"

    def test_ord_ascii(self):
        """Test ord() with ASCII characters."""
        assert builtin.ord("A") == 65
        assert builtin.ord("a") == 97

    def test_ord_unicode(self):
        """Test ord() with Unicode characters."""
        assert builtin.ord("€") == 8364
        assert builtin.ord("☀") == 9728

    def test_chr_ord_roundtrip(self):
        """Test chr() and ord() are inverse operations."""
        for i in [65, 97, 128, 8364]:
            assert builtin.ord(builtin.chr(i)) == i

    def test_hex_conversion(self):
        """Test hex() converts to hexadecimal."""
        assert builtin.hex(255) == "0xff"
        assert builtin.hex(16) == "0x10"
        assert builtin.hex(0) == "0x0"

    def test_bin_conversion(self):
        """Test bin() converts to binary."""
        assert builtin.bin(10) == "0b1010"
        assert builtin.bin(255) == "0b11111111"
        assert builtin.bin(0) == "0b0"

    def test_oct_conversion(self):
        """Test oct() converts to octal."""
        assert builtin.oct(8) == "0o10"
        assert builtin.oct(64) == "0o100"
        assert builtin.oct(0) == "0o0"

    def test_repr_numbers(self):
        """Test repr() with numbers."""
        assert builtin.repr(42) == "42"
        assert builtin.repr(3.14) == "3.14"

    def test_repr_booleans(self):
        """Test repr() with ML-compatible boolean formatting."""
        assert builtin.repr(True) == "true"
        assert builtin.repr(False) == "false"

    def test_repr_strings(self):
        """Test repr() with strings."""
        assert builtin.repr("hello") == "'hello'"

    def test_format_float(self):
        """Test format() with float precision."""
        assert builtin.format(3.14159, ".2f") == "3.14"
        assert builtin.format(2.5, ".1f") == "2.5"

    def test_format_integer_padding(self):
        """Test format() with integer padding."""
        assert builtin.format(42, "05d") == "00042"
        assert builtin.format(7, "03d") == "007"

    def test_format_hex(self):
        """Test format() with hexadecimal."""
        assert builtin.format(255, "x") == "ff"
        assert builtin.format(255, "X") == "FF"

    def test_reversed_list(self):
        """Test reversed() with list."""
        assert builtin.reversed([1, 2, 3, 4]) == [4, 3, 2, 1]

    def test_reversed_string(self):
        """Test reversed() with string."""
        result = builtin.reversed("hello")
        assert result == ['o', 'l', 'l', 'e', 'h']

    def test_reversed_empty(self):
        """Test reversed() with empty list."""
        assert builtin.reversed([]) == []


class TestDynamicIntrospectionUseCases:
    """Test real-world use cases for dynamic introspection."""

    def test_dynamic_method_dispatch(self):
        """Test dynamic method dispatch pattern."""
        operations = {
            "upper": builtin.getattr("hello", "upper"),
            "lower": builtin.getattr("WORLD", "lower")
        }

        assert builtin.call(operations["upper"]) == "HELLO"
        assert builtin.call(operations["lower"]) == "world"

    def test_configuration_with_fallbacks(self):
        """Test configuration pattern with getattr defaults."""
        config = {"timeout": 30, "retries": 3}

        # Use getattr to access dictionary with default
        get_method = builtin.getattr(config, "get", None)
        if get_method:
            timeout = get_method("timeout", 10)
            assert timeout == 30

    def test_functional_programming_pipeline(self):
        """Test functional programming with call()."""
        operations = [
            lambda x: x + 10,
            lambda x: x * 2,
            lambda x: x - 5
        ]

        result = 5
        for op in operations:
            result = builtin.call(op, result)

        assert result == 25  # (5 + 10) * 2 - 5


class TestUtilityFunctionEdgeCases:
    """Test edge cases for utility functions."""

    def test_all_mixed_types(self):
        """Test all() with mixed types."""
        assert builtin.all([1, "hello", True, [1]]) is True
        assert builtin.all([1, "", True]) is False  # Empty string is falsy

    def test_any_mixed_types(self):
        """Test any() with mixed types."""
        assert builtin.any([0, "", False, 1]) is True
        assert builtin.any([0, "", False, []]) is False

    def test_sum_negative_numbers(self):
        """Test sum() with negative numbers."""
        assert builtin.sum([1, -2, 3, -4]) == -2

    def test_sum_mixed_int_float(self):
        """Test sum() with mixed int and float."""
        result = builtin.sum([1, 2.5, 3])
        assert result == 6.5

    def test_chr_boundary_values(self):
        """Test chr() with boundary values."""
        assert builtin.chr(0) == "\x00"
        assert builtin.chr(127) == "\x7f"

    def test_format_empty_spec(self):
        """Test format() with empty format spec."""
        assert builtin.format(42, "") == "42"
        assert builtin.format(3.14, "") == "3.14"

    def test_reversed_single_element(self):
        """Test reversed() with single element."""
        assert builtin.reversed([42]) == [42]

    def test_callable_with_builtin_types(self):
        """Test callable() with builtin types."""
        assert builtin.callable(int) is True
        assert builtin.callable(str) is True
        assert builtin.callable(list) is True


class TestNewFunctionsModuleRegistration:
    """Test that new functions are properly registered."""

    def test_new_functions_have_metadata(self):
        """Test new functions have @ml_function metadata."""
        new_functions = [
            "hasattr", "getattr", "call",
            "callable", "all", "any", "sum",
            "chr", "ord", "hex", "bin", "oct",
            "repr", "format", "reversed"
        ]

        for func_name in new_functions:
            func = getattr(builtin, func_name)
            assert hasattr(func, "_ml_function_metadata"), \
                f"{func_name} should have metadata"

    def test_module_metadata_updated(self):
        """Test module metadata includes new functions."""
        from mlpy.stdlib.decorators import get_module_metadata

        metadata = get_module_metadata("builtin")
        assert metadata is not None

        # Should have original 22 + 3 dynamic + 13 utilities = 38 functions
        assert len(metadata.functions) >= 38
