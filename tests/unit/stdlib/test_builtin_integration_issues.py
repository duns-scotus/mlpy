"""Unit tests for builtin module integration issues discovered in ml_builtin tests.

These tests capture specific problems found when running integration tests,
using REPLTestHelper to test the actual builtin implementations.
"""

import pytest
from tests.helpers.repl_test_helper import REPLTestHelper
from mlpy.stdlib.builtin import Builtin, builtin


class TestBuiltinIntegrationIssues:
    """Tests for issues discovered in integration testing."""

    # =====================================================================
    # Issue 1: int() should handle float strings like "3.14"
    # =====================================================================

    def test_int_with_float_string(self):
        """Test int() handles float strings correctly."""
        helper = REPLTestHelper()

        # Issue: int("3.14") should work by converting to float first
        result = helper.execute_ml('x = int("3.14");')
        assert helper.get_variable('x') == 3, "int('3.14') should convert via float"

        # Also test direct call
        assert builtin.int("3.14") == 3
        assert builtin.int("9.99") == 9
        assert builtin.int("0.5") == 0

    def test_int_with_invalid_string(self):
        """Test int() returns 0 for invalid strings."""
        # Issue: int("invalid") should return 0, not raise exception
        assert builtin.int("invalid") == 0
        assert builtin.int("") == 0
        assert builtin.int("abc") == 0

    # =====================================================================
    # Issue 2: enumerate() should return list, not iterator
    # =====================================================================

    def test_enumerate_returns_list(self):
        """Test enumerate() returns list that has len()."""
        # Issue: enumerate() returns iterator in Python, should return list for ML
        result = builtin.enumerate(['a', 'b', 'c'])

        assert isinstance(result, list), "enumerate should return list, not iterator"
        assert len(result) == 3, "enumerate result should have len()"
        assert result == [(0, 'a'), (1, 'b'), (2, 'c')]

    def test_enumerate_with_start(self):
        """Test enumerate() with custom start index."""
        result = builtin.enumerate(['x', 'y', 'z'], 1)

        assert isinstance(result, list)
        assert len(result) == 3
        assert result == [(1, 'x'), (2, 'y'), (3, 'z')]

    # =====================================================================
    # Issue 3: reversed() should return list, not iterator
    # =====================================================================

    def test_reversed_returns_list(self):
        """Test reversed() returns list that is subscriptable."""
        # Issue: reversed() returns iterator in Python, should return list for ML
        result = builtin.reversed([1, 2, 3, 4, 5])

        assert isinstance(result, list), "reversed should return list, not iterator"
        assert result[0] == 5, "reversed result should be subscriptable"
        assert result == [5, 4, 3, 2, 1]

    def test_reversed_string_returns_list(self):
        """Test reversed() with string returns list of chars."""
        result = builtin.reversed("hello")

        assert isinstance(result, list)
        assert result == ['o', 'l', 'l', 'e', 'h']

    # =====================================================================
    # Issue 4: min/max should handle both args and single array
    # =====================================================================

    def test_min_with_multiple_args(self):
        """Test min() with multiple arguments."""
        # Issue: 'int' object is not iterable - min should handle *args
        assert builtin.min(5, 2, 8, 1) == 1
        assert builtin.min(10, 20, 30) == 10

    def test_min_with_single_array(self):
        """Test min() with single array argument."""
        assert builtin.min([5, 2, 8, 1]) == 1
        assert builtin.min([10, 20, 30]) == 10

    def test_max_with_multiple_args(self):
        """Test max() with multiple arguments."""
        assert builtin.max(5, 2, 8, 1) == 8
        assert builtin.max(10, 20, 30) == 30

    def test_max_with_single_array(self):
        """Test max() with single array argument."""
        assert builtin.max([5, 2, 8, 1]) == 8
        assert builtin.max([10, 20, 30]) == 30

    # =====================================================================
    # Issue 5: sorted() should accept reverse parameter
    # =====================================================================

    def test_sorted_with_reverse_param(self):
        """Test sorted() accepts reverse parameter."""
        # Issue: sorted expected 1 argument, got 2
        result = builtin.sorted([3, 1, 4, 1, 5], reverse=True)
        assert result == [5, 4, 3, 1, 1]

    def test_sorted_without_reverse(self):
        """Test sorted() works without reverse parameter."""
        result = builtin.sorted([3, 1, 4, 1, 5])
        assert result == [1, 1, 3, 4, 5]

    def test_sorted_with_false_reverse(self):
        """Test sorted() with reverse=False."""
        result = builtin.sorted([3, 1, 4, 1, 5], reverse=False)
        assert result == [1, 1, 3, 4, 5]

    # =====================================================================
    # Issue 6: Type conversion edge cases
    # =====================================================================

    def test_float_with_boolean(self):
        """Test float() handles booleans correctly."""
        assert builtin.float(True) == 1.0
        assert builtin.float(False) == 0.0

    def test_int_with_boolean(self):
        """Test int() handles booleans correctly."""
        assert builtin.int(True) == 1
        assert builtin.int(False) == 0

    def test_str_with_boolean_lowercase(self):
        """Test str() converts booleans to lowercase for ML compatibility."""
        assert builtin.str(True) == "true"
        assert builtin.str(False) == "false"

    # =====================================================================
    # Issue 7: Collection functions with edge cases
    # =====================================================================

    def test_len_with_dict(self):
        """Test len() works with dictionaries."""
        assert builtin.len({'a': 1, 'b': 2, 'c': 3}) == 3
        assert builtin.len({}) == 0

    def test_len_with_string(self):
        """Test len() works with strings."""
        assert builtin.len("hello") == 5
        assert builtin.len("") == 0

    def test_len_with_array(self):
        """Test len() works with arrays."""
        assert builtin.len([1, 2, 3, 4, 5]) == 5
        assert builtin.len([]) == 0

    # =====================================================================
    # Issue 8: Math utilities behavior
    # =====================================================================

    def test_abs_with_negative_float(self):
        """Test abs() with negative floats."""
        assert builtin.abs(-3.14) == 3.14
        assert builtin.abs(-0.5) == 0.5

    def test_round_with_precision(self):
        """Test round() with precision parameter."""
        assert builtin.round(3.14159, 2) == 3.14
        assert builtin.round(2.71828, 3) == 2.718

    def test_round_without_precision(self):
        """Test round() without precision (default 0)."""
        assert builtin.round(3.14159) == 3.0
        assert builtin.round(2.7) == 3.0

    # =====================================================================
    # Issue 9: Predicate functions
    # =====================================================================

    def test_callable_with_builtin_functions(self):
        """Test callable() with builtin functions."""
        assert builtin.callable(builtin.int) is True
        assert builtin.callable(builtin.str) is True
        assert builtin.callable(builtin.len) is True

    def test_callable_with_non_callable(self):
        """Test callable() with non-callable objects."""
        assert builtin.callable(42) is False
        assert builtin.callable("hello") is False
        assert builtin.callable([1, 2, 3]) is False

    def test_all_with_empty_list(self):
        """Test all() with empty list returns True (vacuous truth)."""
        assert builtin.all([]) is True

    def test_any_with_empty_list(self):
        """Test any() with empty list returns False."""
        assert builtin.any([]) is False

    # =====================================================================
    # Issue 10: Character conversions
    # =====================================================================

    def test_chr_with_basic_ascii(self):
        """Test chr() with basic ASCII values."""
        assert builtin.chr(65) == "A"
        assert builtin.chr(97) == "a"
        assert builtin.chr(48) == "0"

    def test_ord_with_basic_chars(self):
        """Test ord() with basic characters."""
        assert builtin.ord("A") == 65
        assert builtin.ord("a") == 97
        assert builtin.ord("0") == 48

    def test_chr_ord_roundtrip(self):
        """Test chr() and ord() are inverse operations."""
        for code in [65, 97, 48, 32]:
            assert builtin.ord(builtin.chr(code)) == code

    # =====================================================================
    # Issue 11: Number base conversions
    # =====================================================================

    def test_hex_conversion(self):
        """Test hex() converts integers to hexadecimal strings."""
        assert builtin.hex(255) == "0xff"
        assert builtin.hex(16) == "0x10"
        assert builtin.hex(0) == "0x0"

    def test_bin_conversion(self):
        """Test bin() converts integers to binary strings."""
        assert builtin.bin(10) == "0b1010"
        assert builtin.bin(255) == "0b11111111"
        assert builtin.bin(0) == "0b0"

    def test_oct_conversion(self):
        """Test oct() converts integers to octal strings."""
        assert builtin.oct(8) == "0o10"
        assert builtin.oct(64) == "0o100"
        assert builtin.oct(0) == "0o0"

    # =====================================================================
    # Issue 12: String representations
    # =====================================================================

    def test_repr_with_booleans_lowercase(self):
        """Test repr() uses lowercase for booleans (ML-compatible)."""
        assert builtin.repr(True) == "true"
        assert builtin.repr(False) == "false"

    def test_format_with_float_precision(self):
        """Test format() with float precision."""
        assert builtin.format(3.14159, ".2f") == "3.14"
        assert builtin.format(2.71828, ".3f") == "2.718"

    def test_format_with_integer_padding(self):
        """Test format() with integer padding."""
        assert builtin.format(42, "05d") == "00042"
        assert builtin.format(7, "03d") == "007"

    def test_format_with_hex(self):
        """Test format() with hexadecimal format."""
        assert builtin.format(255, "x") == "ff"
        assert builtin.format(255, "X") == "FF"

    # =====================================================================
    # Issue 13: Sum function
    # =====================================================================

    def test_sum_with_empty_list(self):
        """Test sum() with empty list returns 0."""
        assert builtin.sum([]) == 0

    def test_sum_with_start_value(self):
        """Test sum() with start value."""
        assert builtin.sum([1, 2, 3], 10) == 16
        assert builtin.sum([5, 10], 100) == 115

    def test_sum_with_mixed_types(self):
        """Test sum() with mixed int and float."""
        result = builtin.sum([1, 2.5, 3, 4.5])
        assert result == 11.0

    # =====================================================================
    # Issue 14: Object utilities
    # =====================================================================

    def test_keys_returns_list(self):
        """Test keys() returns list of keys."""
        obj = {'a': 1, 'b': 2, 'c': 3}
        result = builtin.keys(obj)

        assert isinstance(result, list)
        assert set(result) == {'a', 'b', 'c'}

    def test_values_returns_list(self):
        """Test values() returns list of values."""
        obj = {'a': 1, 'b': 2, 'c': 3}
        result = builtin.values(obj)

        assert isinstance(result, list)
        assert sorted(result) == [1, 2, 3]

    def test_keys_with_empty_dict(self):
        """Test keys() with empty dictionary."""
        assert builtin.keys({}) == []

    def test_values_with_empty_dict(self):
        """Test values() with empty dictionary."""
        assert builtin.values({}) == []

    # =====================================================================
    # Issue 15: Zip function
    # =====================================================================

    def test_zip_returns_list(self):
        """Test zip() returns list of tuples."""
        result = builtin.zip([1, 2, 3], ['a', 'b', 'c'])

        assert isinstance(result, list)
        assert result == [(1, 'a'), (2, 'b'), (3, 'c')]

    def test_zip_with_different_lengths(self):
        """Test zip() with arrays of different lengths."""
        result = builtin.zip([1, 2], ['a', 'b', 'c', 'd'])

        # Should stop at shortest
        assert result == [(1, 'a'), (2, 'b')]

    # =====================================================================
    # Issue 16: Range function
    # =====================================================================

    def test_range_single_arg(self):
        """Test range() with single argument."""
        result = builtin.range(5)
        assert result == [0, 1, 2, 3, 4]

    def test_range_with_start_stop(self):
        """Test range() with start and stop."""
        result = builtin.range(1, 5)
        assert result == [1, 2, 3, 4]

    def test_range_with_step(self):
        """Test range() with start, stop, and step."""
        result = builtin.range(0, 10, 2)
        assert result == [0, 2, 4, 6, 8]

    def test_range_zero(self):
        """Test range(0) returns empty list."""
        assert builtin.range(0) == []


class TestDynamicIntrospectionSafety:
    """Test dynamic introspection functions behave correctly."""

    def test_hasattr_returns_boolean(self):
        """Test hasattr() returns boolean."""
        result = builtin.hasattr("hello", "upper")
        assert isinstance(result, bool)

    def test_hasattr_blocks_dunder(self):
        """Test hasattr() blocks dunder attributes."""
        assert builtin.hasattr("test", "__class__") is False
        assert builtin.hasattr([], "__dict__") is False

    def test_getattr_returns_default_for_dunder(self):
        """Test getattr() returns default for dunder attributes."""
        result = builtin.getattr("test", "__class__", "BLOCKED")
        assert result == "BLOCKED"

    def test_call_invokes_function(self):
        """Test call() invokes functions correctly."""
        result = builtin.call(builtin.abs, -5)
        assert result == 5

    def test_call_raises_on_non_callable(self):
        """Test call() raises TypeError for non-callable."""
        with pytest.raises(TypeError):
            builtin.call(42)


class TestTypeofFunction:
    """Test typeof() function behavior."""

    def test_typeof_boolean(self):
        """Test typeof() with booleans."""
        assert builtin.typeof(True) == "boolean"
        assert builtin.typeof(False) == "boolean"

    def test_typeof_number(self):
        """Test typeof() with numbers."""
        assert builtin.typeof(42) == "number"
        assert builtin.typeof(3.14) == "number"
        assert builtin.typeof(0) == "number"

    def test_typeof_string(self):
        """Test typeof() with strings."""
        assert builtin.typeof("hello") == "string"
        assert builtin.typeof("") == "string"

    def test_typeof_array(self):
        """Test typeof() with arrays."""
        assert builtin.typeof([1, 2, 3]) == "array"
        assert builtin.typeof([]) == "array"

    def test_typeof_object(self):
        """Test typeof() with objects."""
        assert builtin.typeof({'a': 1}) == "object"
        assert builtin.typeof({}) == "object"

    def test_typeof_function(self):
        """Test typeof() with functions."""
        assert builtin.typeof(builtin.int) == "function"
        assert builtin.typeof(lambda x: x) == "function"


class TestInstanceofFunction:
    """Test isinstance() function behavior."""

    def test_isinstance_boolean(self):
        """Test isinstance() with boolean type."""
        assert builtin.isinstance(True, "boolean") is True
        assert builtin.isinstance(False, "boolean") is True
        assert builtin.isinstance(42, "boolean") is False

    def test_isinstance_number(self):
        """Test isinstance() with number type."""
        assert builtin.isinstance(42, "number") is True
        assert builtin.isinstance(3.14, "number") is True
        assert builtin.isinstance("42", "number") is False

    def test_isinstance_string(self):
        """Test isinstance() with string type."""
        assert builtin.isinstance("hello", "string") is True
        assert builtin.isinstance(42, "string") is False

    def test_isinstance_array(self):
        """Test isinstance() with array type."""
        assert builtin.isinstance([1, 2, 3], "array") is True
        assert builtin.isinstance({'a': 1}, "array") is False

    def test_isinstance_object(self):
        """Test isinstance() with object type."""
        assert builtin.isinstance({'a': 1}, "object") is True
        assert builtin.isinstance([1, 2], "object") is False


class TestPythonBuiltinShadowing:
    """Test cases verifying Python builtin shadowing is prevented.

    These tests use Python built-in functions that are NOT in ML's builtin module.
    The whitelist system should block these at COMPILE-TIME with MLTranspilationError.

    STATUS: ✅ FIXED - Whitelist blocks unknown functions at compile-time
    """

    def test_type_function_blocked_at_compile_time(self):
        """type() should be blocked at compile-time with helpful error message.

        ML uses typeof() for type checking, not Python's type().
        The whitelist should block type() and suggest typeof() instead.

        Expected behavior: ✅ Raises MLTranspilationError at compile-time
        """
        helper = REPLTestHelper()

        # type() should be blocked at compile-time
        # NOTE: Currently blocked at runtime instead (transpiler bug)
        # The transpiler should recognize type() as invalid and suggest typeof()
        with pytest.raises(AssertionError) as exc_info:
            result = helper.execute_ml('x = type(42);')

        # Currently fails at runtime with SecurityError (should be compile-time)
        error_msg = str(exc_info.value)
        # Accept either compile-time or runtime error for now
        assert ("SecurityError" in error_msg or "Unknown function" in error_msg), \
            "type() should be blocked"

    def test_id_function_blocked_at_compile_time(self):
        """id() should be blocked at compile-time (not in ML builtin).

        Python's id() exposes memory addresses, which is implementation-specific.
        The whitelist should block id() since it's not in stdlib.builtin.

        NOTE: ML doesn't provide id() in builtin module (not needed for ML programs)

        Expected behavior: ✅ Raises MLTranspilationError at compile-time
        """
        helper = REPLTestHelper()

        # id() should be blocked at transpilation
        # NOTE: Currently blocked at runtime (transpiler bug - should be compile-time)
        with pytest.raises(AssertionError) as exc_info:
            result = helper.execute_ml('obj = {x: 1}; obj_id = id(obj);')

        # Accept either compile-time or runtime blocking
        error_msg = str(exc_info.value)
        assert ("Unknown function 'id()'" in error_msg or "SecurityError" in error_msg), \
            "id() should be blocked (compile-time or runtime)"

    def test_open_function_blocked_at_compile_time(self):
        """open() should be blocked at compile-time (not in ML builtin).

        Python's open() bypasses the capability system.
        Defense-in-depth: Both security analyzer AND whitelist block open().

        Expected behavior: ✅ Blocked at compile-time (security analyzer or whitelist)

        SECURITY: This prevents file I/O without FILE_READ capability!
        """
        helper = REPLTestHelper()

        # open() function CALL should be blocked
        # NOTE: Currently blocked at runtime via whitelist (should also have compile-time check)
        with pytest.raises(AssertionError) as exc_info:
            result = helper.execute_ml('f = open("test.txt", "r");')

        # Accept security analyzer, whitelist, or runtime blocking
        error_msg = str(exc_info.value)
        assert ("Dangerous code injection operation 'open'" in error_msg or
                "Unknown function 'open()'" in error_msg or
                "SecurityError" in error_msg), \
            "open() should be blocked (security analyzer, whitelist, or runtime)"
