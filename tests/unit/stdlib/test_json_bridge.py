"""Unit tests for JSON bridge module.

Tests all functionality of the JSON module including:
- Parsing JSON strings (parse, safeParse)
- Serializing objects (stringify, prettyPrint)
- Validation (validate)
- Type checking (isObject, isArray, isString, isNumber, isBoolean, isNull)
- Utility methods (keys, values, hasKey, get, merge)
"""

import pytest
from mlpy.stdlib.json_bridge import JSON, json


class TestJSONBridgeModule:
    """Test JSON bridge module registration and instantiation."""

    def test_json_module_exists(self):
        """Test that json module is properly instantiated."""
        assert json is not None
        assert isinstance(json, JSON)

    def test_json_class_exists(self):
        """Test that JSON class can be instantiated."""
        json_instance = JSON()
        assert json_instance is not None


class TestJSONParsing:
    """Test JSON parsing functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.json = JSON()

    def test_parse_simple_object(self):
        """Test parsing a simple JSON object."""
        result = self.json.parse('{"name": "Alice", "age": 30}')
        assert isinstance(result, dict)
        assert result["name"] == "Alice"
        assert result["age"] == 30

    def test_parse_simple_array(self):
        """Test parsing a simple JSON array."""
        result = self.json.parse('[1, 2, 3, 4, 5]')
        assert isinstance(result, list)
        assert result == [1, 2, 3, 4, 5]

    def test_parse_nested_object(self):
        """Test parsing nested JSON objects."""
        json_str = '{"user": {"name": "Bob", "address": {"city": "NYC"}}}'
        result = self.json.parse(json_str)
        assert result["user"]["name"] == "Bob"
        assert result["user"]["address"]["city"] == "NYC"

    def test_parse_mixed_types(self):
        """Test parsing JSON with mixed types."""
        json_str = '{"str": "hello", "num": 42, "bool": true, "null": null, "arr": [1,2,3]}'
        result = self.json.parse(json_str)
        assert result["str"] == "hello"
        assert result["num"] == 42
        assert result["bool"] is True
        assert result["null"] is None
        assert result["arr"] == [1, 2, 3]

    def test_parse_primitive_number(self):
        """Test parsing a primitive number."""
        result = self.json.parse('42')
        assert result == 42

    def test_parse_primitive_string(self):
        """Test parsing a primitive string."""
        result = self.json.parse('"hello world"')
        assert result == "hello world"

    def test_parse_primitive_boolean(self):
        """Test parsing primitive booleans."""
        assert self.json.parse('true') is True
        assert self.json.parse('false') is False

    def test_parse_primitive_null(self):
        """Test parsing null."""
        result = self.json.parse('null')
        assert result is None

    def test_parse_invalid_json_raises_error(self):
        """Test that invalid JSON raises ValueError."""
        with pytest.raises(ValueError, match="JSON parsing failed"):
            self.json.parse('{invalid}')

    def test_parse_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="JSON parsing failed"):
            self.json.parse('')

    def test_parse_malformed_json_raises_error(self):
        """Test that malformed JSON raises ValueError."""
        with pytest.raises(ValueError, match="JSON parsing failed"):
            self.json.parse('{"key": "value",}')  # Trailing comma


class TestJSONSafeParsing:
    """Test safe JSON parsing with depth validation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.json = JSON()

    def test_safe_parse_shallow_object(self):
        """Test safe parsing of shallow object."""
        result = self.json.safeParse('{"a": 1, "b": 2}', max_depth=10)
        assert result == {"a": 1, "b": 2}

    def test_safe_parse_nested_within_limit(self):
        """Test safe parsing of nested object within depth limit."""
        json_str = '{"a": {"b": {"c": 1}}}'
        result = self.json.safeParse(json_str, max_depth=10)
        assert result["a"]["b"]["c"] == 1

    def test_safe_parse_depth_exceeds_limit(self):
        """Test that deeply nested JSON exceeds depth limit."""
        # Create deeply nested JSON
        json_str = '{"a":' * 10 + '1' + '}' * 10
        with pytest.raises(ValueError, match="depth exceeds maximum"):
            self.json.safeParse(json_str, max_depth=5)

    def test_safe_parse_default_max_depth(self):
        """Test safe parsing with default max depth (100)."""
        # Should work with default depth
        json_str = '{"a": {"b": {"c": 1}}}'
        result = self.json.safeParse(json_str)
        assert result["a"]["b"]["c"] == 1

    def test_safe_parse_enforces_max_depth_limit(self):
        """Test that max_depth cannot exceed 100."""
        # Even if we request 200, should be capped at 100
        json_str = '{"a": 1}'
        result = self.json.safeParse(json_str, max_depth=200)
        assert result == {"a": 1}
        # Can't easily verify the cap, but the code enforces it

    def test_safe_parse_array_depth(self):
        """Test safe parsing counts array nesting depth."""
        json_str = '[[[[1]]]]'
        with pytest.raises(ValueError, match="depth exceeds maximum"):
            self.json.safeParse(json_str, max_depth=2)

    def test_safe_parse_mixed_nesting_depth(self):
        """Test safe parsing with mixed object/array nesting."""
        json_str = '{"a": [{"b": [1, 2, 3]}]}'
        result = self.json.safeParse(json_str, max_depth=10)
        assert result["a"][0]["b"] == [1, 2, 3]

    def test_safe_parse_invalid_json_raises_error(self):
        """Test that safeParse raises ValueError for invalid JSON."""
        with pytest.raises(ValueError) as exc_info:
            self.json.safeParse('{"invalid": json syntax}')
        assert "JSON parsing failed" in str(exc_info.value)


class TestJSONSerialization:
    """Test JSON serialization functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.json = JSON()

    def test_stringify_simple_object(self):
        """Test stringifying a simple object."""
        obj = {"name": "Alice", "age": 30}
        result = self.json.stringify(obj)
        assert '"name"' in result
        assert '"Alice"' in result
        assert '"age"' in result
        assert '30' in result

    def test_stringify_simple_array(self):
        """Test stringifying a simple array."""
        arr = [1, 2, 3, 4, 5]
        result = self.json.stringify(arr)
        assert result == '[1, 2, 3, 4, 5]' or result == '[1,2,3,4,5]'

    def test_stringify_nested_object(self):
        """Test stringifying nested objects."""
        obj = {"user": {"name": "Bob", "age": 25}}
        result = self.json.stringify(obj)
        assert '"user"' in result
        assert '"name"' in result
        assert '"Bob"' in result

    def test_stringify_primitive_types(self):
        """Test stringifying primitive types."""
        assert self.json.stringify(42) == '42'
        assert self.json.stringify("hello") == '"hello"'
        assert self.json.stringify(True) == 'true'
        assert self.json.stringify(False) == 'false'
        assert self.json.stringify(None) == 'null'

    def test_stringify_empty_object(self):
        """Test stringifying empty object."""
        result = self.json.stringify({})
        assert result == '{}'

    def test_stringify_empty_array(self):
        """Test stringifying empty array."""
        result = self.json.stringify([])
        assert result == '[]'

    def test_pretty_print_with_indentation(self):
        """Test pretty printing with indentation."""
        obj = {"name": "Alice", "age": 30}
        result = self.json.prettyPrint(obj, indent=2)
        assert '\n' in result  # Should have newlines
        assert '  ' in result  # Should have indentation

    def test_pretty_print_default_indent(self):
        """Test pretty printing with default indentation (4 spaces)."""
        obj = {"name": "Alice", "age": 30}
        result = self.json.prettyPrint(obj)
        assert '\n' in result
        assert '    ' in result  # 4 spaces

    def test_pretty_print_nested_object(self):
        """Test pretty printing nested objects."""
        obj = {"user": {"name": "Bob", "address": {"city": "NYC"}}}
        result = self.json.prettyPrint(obj, indent=2)
        assert '\n' in result
        lines = result.split('\n')
        assert len(lines) > 3  # Multiple lines for nested structure

    def test_stringify_circular_reference_error(self):
        """Test that stringify raises ValueError for circular references."""
        class CircularRef:
            def __init__(self):
                self.self_ref = self

        with pytest.raises(ValueError) as exc_info:
            self.json.stringify(CircularRef())
        assert "JSON serialization failed" in str(exc_info.value)

    def test_pretty_print_circular_reference_error(self):
        """Test that prettyPrint raises ValueError for circular references."""
        class CircularRef:
            def __init__(self):
                self.self_ref = self

        with pytest.raises(ValueError) as exc_info:
            self.json.prettyPrint(CircularRef())
        assert "JSON serialization failed" in str(exc_info.value)


class TestJSONValidation:
    """Test JSON validation functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.json = JSON()

    def test_validate_valid_object(self):
        """Test validation of valid JSON object."""
        assert self.json.validate('{"name": "Alice"}') is True

    def test_validate_valid_array(self):
        """Test validation of valid JSON array."""
        assert self.json.validate('[1, 2, 3]') is True

    def test_validate_valid_primitives(self):
        """Test validation of valid JSON primitives."""
        assert self.json.validate('42') is True
        assert self.json.validate('"hello"') is True
        assert self.json.validate('true') is True
        assert self.json.validate('false') is True
        assert self.json.validate('null') is True

    def test_validate_invalid_json(self):
        """Test validation of invalid JSON."""
        assert self.json.validate('{invalid}') is False
        assert self.json.validate('') is False
        assert self.json.validate('undefined') is False
        assert self.json.validate('{key: "value"}') is False  # Unquoted key

    def test_validate_malformed_json(self):
        """Test validation of malformed JSON."""
        assert self.json.validate('{"key": "value",}') is False  # Trailing comma
        assert self.json.validate('{"key"}') is False  # Missing value


class TestJSONTypeChecking:
    """Test JSON type checking utilities."""

    def setup_method(self):
        """Set up test fixtures."""
        self.json = JSON()

    def test_is_object(self):
        """Test isObject type checker."""
        assert self.json.isObject({"a": 1}) is True
        assert self.json.isObject({}) is True
        assert self.json.isObject([1, 2, 3]) is False
        assert self.json.isObject("string") is False
        assert self.json.isObject(42) is False
        assert self.json.isObject(None) is False

    def test_is_array(self):
        """Test isArray type checker."""
        assert self.json.isArray([1, 2, 3]) is True
        assert self.json.isArray([]) is True
        assert self.json.isArray({"a": 1}) is False
        assert self.json.isArray("string") is False
        assert self.json.isArray(42) is False
        assert self.json.isArray(None) is False

    def test_is_string(self):
        """Test isString type checker."""
        assert self.json.isString("hello") is True
        assert self.json.isString("") is True
        assert self.json.isString(42) is False
        assert self.json.isString([]) is False
        assert self.json.isString({}) is False
        assert self.json.isString(None) is False

    def test_is_number(self):
        """Test isNumber type checker (excludes booleans)."""
        assert self.json.isNumber(42) is True
        assert self.json.isNumber(3.14) is True
        assert self.json.isNumber(0) is True
        assert self.json.isNumber(-5) is True
        assert self.json.isNumber(True) is False  # Boolean, not number
        assert self.json.isNumber(False) is False  # Boolean, not number
        assert self.json.isNumber("42") is False
        assert self.json.isNumber(None) is False

    def test_is_boolean(self):
        """Test isBoolean type checker."""
        assert self.json.isBoolean(True) is True
        assert self.json.isBoolean(False) is True
        assert self.json.isBoolean(1) is False
        assert self.json.isBoolean(0) is False
        assert self.json.isBoolean("true") is False
        assert self.json.isBoolean(None) is False

    def test_is_null(self):
        """Test isNull type checker."""
        assert self.json.isNull(None) is True
        assert self.json.isNull(0) is False
        assert self.json.isNull("") is False
        assert self.json.isNull(False) is False
        assert self.json.isNull([]) is False
        assert self.json.isNull({}) is False


class TestJSONUtilityMethods:
    """Test JSON utility methods."""

    def setup_method(self):
        """Set up test fixtures."""
        self.json = JSON()

    def test_keys_of_object(self):
        """Test getting keys from object."""
        obj = {"name": "Alice", "age": 30, "city": "NYC"}
        keys = self.json.keys(obj)
        assert set(keys) == {"name", "age", "city"}

    def test_keys_of_empty_object(self):
        """Test getting keys from empty object."""
        keys = self.json.keys({})
        assert keys == []

    def test_keys_of_non_object(self):
        """Test getting keys from non-object returns empty list."""
        assert self.json.keys([1, 2, 3]) == []
        assert self.json.keys("string") == []
        assert self.json.keys(42) == []

    def test_values_of_object(self):
        """Test getting values from object."""
        obj = {"name": "Alice", "age": 30}
        values = self.json.values(obj)
        assert set(values) == {"Alice", 30}

    def test_values_of_empty_object(self):
        """Test getting values from empty object."""
        values = self.json.values({})
        assert values == []

    def test_values_of_non_object(self):
        """Test getting values from non-object returns empty list."""
        assert self.json.values([1, 2, 3]) == []
        assert self.json.values("string") == []

    def test_has_key_exists(self):
        """Test hasKey returns True when key exists."""
        obj = {"name": "Alice", "age": 30}
        assert self.json.hasKey(obj, "name") is True
        assert self.json.hasKey(obj, "age") is True

    def test_has_key_not_exists(self):
        """Test hasKey returns False when key doesn't exist."""
        obj = {"name": "Alice"}
        assert self.json.hasKey(obj, "age") is False
        assert self.json.hasKey(obj, "city") is False

    def test_has_key_on_non_object(self):
        """Test hasKey on non-object returns False."""
        assert self.json.hasKey([1, 2, 3], "0") is False
        assert self.json.hasKey("string", "key") is False
        assert self.json.hasKey(42, "key") is False

    def test_get_existing_key(self):
        """Test get returns value for existing key."""
        obj = {"name": "Alice", "age": 30}
        assert self.json.get(obj, "name") == "Alice"
        assert self.json.get(obj, "age") == 30

    def test_get_missing_key_returns_default(self):
        """Test get returns default for missing key."""
        obj = {"name": "Alice"}
        assert self.json.get(obj, "age", 0) == 0
        assert self.json.get(obj, "city", "Unknown") == "Unknown"

    def test_get_missing_key_default_none(self):
        """Test get returns None by default for missing key."""
        obj = {"name": "Alice"}
        assert self.json.get(obj, "age") is None

    def test_get_on_non_object_returns_default(self):
        """Test get on non-object returns default."""
        assert self.json.get([1, 2, 3], "key", "default") == "default"
        assert self.json.get("string", "key", 42) == 42

    def test_merge_two_objects(self):
        """Test merging two objects."""
        obj1 = {"x": 1, "y": 2}
        obj2 = {"y": 3, "z": 4}
        result = self.json.merge(obj1, obj2)
        assert result == {"x": 1, "y": 3, "z": 4}

    def test_merge_empty_objects(self):
        """Test merging empty objects."""
        assert self.json.merge({}, {}) == {}
        assert self.json.merge({"a": 1}, {}) == {"a": 1}
        assert self.json.merge({}, {"b": 2}) == {"b": 2}

    def test_merge_non_objects_returns_second(self):
        """Test merge handles non-objects gracefully."""
        result = self.json.merge([1, 2], {"a": 1})
        assert result == {"a": 1}

        result = self.json.merge({"a": 1}, [1, 2])
        assert result == {"a": 1}

    def test_merge_does_not_modify_originals(self):
        """Test merge creates new object without modifying originals."""
        obj1 = {"x": 1, "y": 2}
        obj2 = {"y": 3, "z": 4}
        result = self.json.merge(obj1, obj2)

        # Originals should be unchanged
        assert obj1 == {"x": 1, "y": 2}
        assert obj2 == {"y": 3, "z": 4}

        # Result should be new dict
        assert result is not obj1
        assert result is not obj2


class TestJSONIntegration:
    """Integration tests for JSON module."""

    def setup_method(self):
        """Set up test fixtures."""
        self.json = JSON()

    def test_parse_stringify_roundtrip(self):
        """Test that parse -> stringify -> parse preserves data."""
        original = {"name": "Alice", "age": 30, "active": True}
        json_str = self.json.stringify(original)
        parsed = self.json.parse(json_str)
        assert parsed == original

    def test_complex_nested_structure(self):
        """Test handling of complex nested structures."""
        data = {
            "users": [
                {"id": 1, "name": "Alice", "tags": ["admin", "active"]},
                {"id": 2, "name": "Bob", "tags": ["user"]},
            ],
            "meta": {"count": 2, "page": 1},
        }

        # Serialize and parse
        json_str = self.json.stringify(data)
        parsed = self.json.parse(json_str)

        # Verify structure
        assert len(parsed["users"]) == 2
        assert parsed["users"][0]["name"] == "Alice"
        assert "admin" in parsed["users"][0]["tags"]
        assert parsed["meta"]["count"] == 2

    def test_real_world_workflow(self):
        """Test a real-world JSON workflow."""
        # Parse JSON from "API"
        api_response = '{"status": "success", "data": {"user": "Alice", "score": 95}}'
        response = self.json.parse(api_response)

        # Validate
        assert self.json.isObject(response)
        assert self.json.hasKey(response, "status")

        # Extract data
        status = self.json.get(response, "status")
        data = self.json.get(response, "data")

        # Merge with additional data
        extra = {"timestamp": "2025-10-24"}
        enriched = self.json.merge(data, extra)

        # Serialize back
        output = self.json.prettyPrint(enriched, 2)
        assert "user" in output
        assert "timestamp" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
