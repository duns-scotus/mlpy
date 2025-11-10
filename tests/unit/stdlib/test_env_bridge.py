"""Unit tests for env_bridge module."""

import os
import pytest

from mlpy.stdlib.env_bridge import Env


class TestEnvModule:
    """Test suite for environment variable operations."""

    def setup_method(self):
        """Setup for each test method."""
        self.env = Env()
        # Clean up any test variables
        self.cleanup_vars = []

    def teardown_method(self):
        """Cleanup after each test method."""
        for var in self.cleanup_vars:
            os.environ.pop(var, None)

    def test_get_existing_variable(self):
        """Test getting an existing environment variable."""
        os.environ["TEST_VAR"] = "test_value"
        self.cleanup_vars.append("TEST_VAR")

        result = self.env.get("TEST_VAR")
        assert result == "test_value"

    def test_get_missing_variable_no_default(self):
        """Test getting missing variable without default returns None."""
        result = self.env.get("NONEXISTENT_VAR")
        assert result is None

    def test_get_missing_variable_with_default(self):
        """Test getting missing variable with default returns default."""
        result = self.env.get("NONEXISTENT_VAR", "default_value")
        assert result == "default_value"

    def test_require_existing_variable(self):
        """Test requiring an existing variable returns its value."""
        os.environ["REQUIRED_VAR"] = "required_value"
        self.cleanup_vars.append("REQUIRED_VAR")

        result = self.env.require("REQUIRED_VAR")
        assert result == "required_value"

    def test_require_missing_variable_raises_error(self):
        """Test requiring missing variable raises RuntimeError."""
        with pytest.raises(RuntimeError, match="Required environment variable not set: MISSING_VAR"):
            self.env.require("MISSING_VAR")

    def test_set_variable(self):
        """Test setting environment variable."""
        self.cleanup_vars.append("NEW_VAR")

        self.env.set("NEW_VAR", "new_value")
        assert os.environ["NEW_VAR"] == "new_value"

    def test_set_variable_converts_to_string(self):
        """Test that set converts value to string."""
        self.cleanup_vars.append("INT_VAR")

        self.env.set("INT_VAR", 123)
        assert os.environ["INT_VAR"] == "123"

    def test_has_existing_variable(self):
        """Test has() returns True for existing variable."""
        os.environ["EXISTING_VAR"] = "value"
        self.cleanup_vars.append("EXISTING_VAR")

        assert self.env.has("EXISTING_VAR") is True

    def test_has_missing_variable(self):
        """Test has() returns False for missing variable."""
        assert self.env.has("NONEXISTENT_VAR") is False

    def test_delete_existing_variable(self):
        """Test deleting existing variable."""
        os.environ["DELETE_VAR"] = "value"
        self.cleanup_vars.append("DELETE_VAR")

        self.env.delete("DELETE_VAR")
        assert "DELETE_VAR" not in os.environ

    def test_delete_missing_variable(self):
        """Test deleting missing variable does not raise error."""
        # Should not raise
        self.env.delete("NONEXISTENT_VAR")

    def test_all_returns_dict(self):
        """Test all() returns dictionary of all variables."""
        result = self.env.all()
        assert isinstance(result, dict)
        # Should contain at least PATH or similar system variable
        assert len(result) > 0

    def test_all_includes_test_variable(self):
        """Test all() includes our test variable."""
        os.environ["ALL_TEST_VAR"] = "test_value"
        self.cleanup_vars.append("ALL_TEST_VAR")

        result = self.env.all()
        assert "ALL_TEST_VAR" in result
        assert result["ALL_TEST_VAR"] == "test_value"

    def test_get_int_valid_integer(self):
        """Test get_int with valid integer string."""
        os.environ["INT_VAR"] = "42"
        self.cleanup_vars.append("INT_VAR")

        result = self.env.get_int("INT_VAR")
        assert result == 42
        assert isinstance(result, int)

    def test_get_int_missing_variable_uses_default(self):
        """Test get_int with missing variable returns default."""
        result = self.env.get_int("MISSING_INT", 100)
        assert result == 100

    def test_get_int_invalid_value_uses_default(self):
        """Test get_int with invalid value returns default."""
        os.environ["INVALID_INT"] = "not_a_number"
        self.cleanup_vars.append("INVALID_INT")

        result = self.env.get_int("INVALID_INT", 50)
        assert result == 50

    def test_get_int_negative_number(self):
        """Test get_int with negative number."""
        os.environ["NEG_INT"] = "-42"
        self.cleanup_vars.append("NEG_INT")

        result = self.env.get_int("NEG_INT")
        assert result == -42

    def test_get_bool_true_values(self):
        """Test get_bool recognizes true values."""
        true_values = ["true", "True", "TRUE", "1", "yes", "YES", "on", "ON"]

        for i, value in enumerate(true_values):
            var_name = f"BOOL_VAR_{i}"
            os.environ[var_name] = value
            self.cleanup_vars.append(var_name)

            result = self.env.get_bool(var_name)
            assert result is True, f"Failed for value: {value}"

    def test_get_bool_false_values(self):
        """Test get_bool treats non-true values as false."""
        false_values = ["false", "False", "0", "no", "off", "anything"]

        for i, value in enumerate(false_values):
            var_name = f"BOOL_FALSE_VAR_{i}"
            os.environ[var_name] = value
            self.cleanup_vars.append(var_name)

            result = self.env.get_bool(var_name)
            assert result is False, f"Failed for value: {value}"

    def test_get_bool_missing_variable_uses_default(self):
        """Test get_bool with missing variable returns default."""
        result = self.env.get_bool("MISSING_BOOL", True)
        assert result is True

        result = self.env.get_bool("MISSING_BOOL", False)
        assert result is False

    def test_get_float_valid_float(self):
        """Test get_float with valid float string."""
        os.environ["FLOAT_VAR"] = "3.14"
        self.cleanup_vars.append("FLOAT_VAR")

        result = self.env.get_float("FLOAT_VAR")
        assert result == 3.14
        assert isinstance(result, float)

    def test_get_float_integer_string(self):
        """Test get_float with integer string."""
        os.environ["FLOAT_INT"] = "42"
        self.cleanup_vars.append("FLOAT_INT")

        result = self.env.get_float("FLOAT_INT")
        assert result == 42.0

    def test_get_float_missing_variable_uses_default(self):
        """Test get_float with missing variable returns default."""
        result = self.env.get_float("MISSING_FLOAT", 1.5)
        assert result == 1.5

    def test_get_float_invalid_value_uses_default(self):
        """Test get_float with invalid value returns default."""
        os.environ["INVALID_FLOAT"] = "not_a_float"
        self.cleanup_vars.append("INVALID_FLOAT")

        result = self.env.get_float("INVALID_FLOAT", 2.5)
        assert result == 2.5

    def test_get_float_scientific_notation(self):
        """Test get_float with scientific notation."""
        os.environ["SCI_FLOAT"] = "1.5e-3"
        self.cleanup_vars.append("SCI_FLOAT")

        result = self.env.get_float("SCI_FLOAT")
        assert result == 0.0015

    def test_integration_scenario(self):
        """Test realistic configuration scenario."""
        # Setup configuration
        os.environ["API_URL"] = "https://api.example.com"
        os.environ["API_PORT"] = "8080"
        os.environ["DEBUG"] = "true"
        os.environ["TIMEOUT"] = "30.5"

        self.cleanup_vars.extend(["API_URL", "API_PORT", "DEBUG", "TIMEOUT"])

        # Read configuration
        api_url = self.env.get("API_URL")
        api_port = self.env.get_int("API_PORT")
        debug = self.env.get_bool("DEBUG")
        timeout = self.env.get_float("TIMEOUT")

        # Verify
        assert api_url == "https://api.example.com"
        assert api_port == 8080
        assert debug is True
        assert timeout == 30.5


class TestEnvModuleMetadata:
    """Test module metadata and decorators."""

    def test_module_has_metadata(self):
        """Test that module has required metadata."""
        assert hasattr(Env, '_ml_module_metadata')
        metadata = Env._ml_module_metadata

        assert metadata.name == "env"
        assert metadata.description == "Environment variable access and management"
        assert "env.read" in metadata.capabilities
        assert "env.write" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_function_capabilities(self):
        """Test that functions have correct capability metadata."""
        env = Env()

        # Read operations
        assert hasattr(env.get, '_ml_function_metadata')
        assert "env.read" in env.get._ml_function_metadata.capabilities

        assert hasattr(env.require, '_ml_function_metadata')
        assert "env.read" in env.require._ml_function_metadata.capabilities

        # Write operations
        assert hasattr(env.set, '_ml_function_metadata')
        assert "env.write" in env.set._ml_function_metadata.capabilities

        assert hasattr(env.delete, '_ml_function_metadata')
        assert "env.write" in env.delete._ml_function_metadata.capabilities
