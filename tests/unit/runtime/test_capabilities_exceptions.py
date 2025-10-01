"""
Comprehensive test suite for capabilities/exceptions.py

Tests exception classes for the capability system including:
- CapabilityError base exception
- CapabilityNotFoundError
- CapabilityExpiredError
- CapabilityValidationError
- InsufficientCapabilityError
- CapabilityContextError
"""

import pytest

from mlpy.runtime.capabilities.exceptions import (
    CapabilityContextError,
    CapabilityError,
    CapabilityExpiredError,
    CapabilityNotFoundError,
    CapabilityValidationError,
    InsufficientCapabilityError,
)


class TestCapabilityError:
    """Test CapabilityError base exception."""

    def test_creation_with_message(self):
        """Test creating exception with message."""
        error = CapabilityError("Test error")
        assert str(error) == "Test error"
        assert error.context == {}

    def test_creation_with_context(self):
        """Test creating exception with context."""
        context = {"key": "value", "code": 123}
        error = CapabilityError("Test error", context)
        assert error.context == context

    def test_is_exception(self):
        """Test that CapabilityError is an Exception."""
        error = CapabilityError("Test")
        assert isinstance(error, Exception)

    def test_can_be_raised(self):
        """Test that exception can be raised and caught."""
        with pytest.raises(CapabilityError) as exc_info:
            raise CapabilityError("Test error")
        assert "Test error" in str(exc_info.value)


class TestCapabilityNotFoundError:
    """Test CapabilityNotFoundError exception."""

    def test_creation_with_capability_type(self):
        """Test creating with capability type."""
        error = CapabilityNotFoundError("file_system")
        assert "file_system" in str(error)
        assert "not found" in str(error)

    def test_creation_with_pattern(self):
        """Test creating with pattern."""
        error = CapabilityNotFoundError("file_system", "*.txt")
        assert "file_system" in str(error)
        assert "*.txt" in str(error)

    def test_context_includes_capability_type(self):
        """Test context includes capability type."""
        error = CapabilityNotFoundError("file_system")
        assert error.context["capability_type"] == "file_system"

    def test_context_includes_pattern(self):
        """Test context includes pattern when provided."""
        error = CapabilityNotFoundError("file_system", "*.txt")
        assert error.context["pattern"] == "*.txt"

    def test_context_includes_error_code(self):
        """Test context includes error code."""
        error = CapabilityNotFoundError("file_system")
        assert error.context["error_code"] == "CAPABILITY_NOT_FOUND"

    def test_is_capability_error(self):
        """Test that it inherits from CapabilityError."""
        error = CapabilityNotFoundError("file_system")
        assert isinstance(error, CapabilityError)

    def test_can_be_raised_and_caught(self):
        """Test raising and catching."""
        with pytest.raises(CapabilityNotFoundError):
            raise CapabilityNotFoundError("test")


class TestCapabilityExpiredError:
    """Test CapabilityExpiredError exception."""

    def test_creation_with_expiry_time(self):
        """Test creating with capability type and expiry time."""
        error = CapabilityExpiredError("file_system", "2024-01-01 12:00:00")
        assert "file_system" in str(error)
        assert "expired" in str(error)
        assert "2024-01-01 12:00:00" in str(error)

    def test_context_includes_capability_type(self):
        """Test context includes capability type."""
        error = CapabilityExpiredError("file_system", "2024-01-01")
        assert error.context["capability_type"] == "file_system"

    def test_context_includes_expired_at(self):
        """Test context includes expiration time."""
        error = CapabilityExpiredError("file_system", "2024-01-01 12:00:00")
        assert error.context["expired_at"] == "2024-01-01 12:00:00"

    def test_context_includes_error_code(self):
        """Test context includes error code."""
        error = CapabilityExpiredError("file_system", "2024-01-01")
        assert error.context["error_code"] == "CAPABILITY_EXPIRED"

    def test_is_capability_error(self):
        """Test that it inherits from CapabilityError."""
        error = CapabilityExpiredError("test", "2024-01-01")
        assert isinstance(error, CapabilityError)

    def test_can_be_raised_and_caught(self):
        """Test raising and catching."""
        with pytest.raises(CapabilityExpiredError):
            raise CapabilityExpiredError("test", "2024-01-01")


class TestCapabilityValidationError:
    """Test CapabilityValidationError exception."""

    def test_creation_with_reason(self):
        """Test creating with validation reason."""
        error = CapabilityValidationError("Invalid token signature")
        assert "validation failed" in str(error)
        assert "Invalid token signature" in str(error)

    def test_creation_with_token_id(self):
        """Test creating with token ID."""
        error = CapabilityValidationError("Invalid signature", "token-123")
        assert error.context["token_id"] == "token-123"

    def test_context_includes_reason(self):
        """Test context includes validation reason."""
        error = CapabilityValidationError("Invalid signature")
        assert error.context["reason"] == "Invalid signature"

    def test_context_includes_error_code(self):
        """Test context includes error code."""
        error = CapabilityValidationError("test")
        assert error.context["error_code"] == "CAPABILITY_VALIDATION_FAILED"

    def test_is_capability_error(self):
        """Test that it inherits from CapabilityError."""
        error = CapabilityValidationError("test")
        assert isinstance(error, CapabilityError)

    def test_can_be_raised_and_caught(self):
        """Test raising and catching."""
        with pytest.raises(CapabilityValidationError):
            raise CapabilityValidationError("test")


class TestInsufficientCapabilityError:
    """Test InsufficientCapabilityError exception."""

    def test_creation_with_permissions(self):
        """Test creating with required and current permissions."""
        error = InsufficientCapabilityError("write", "read")
        assert "Insufficient capability" in str(error)
        assert "write" in str(error)
        assert "read" in str(error)

    def test_context_includes_required_permission(self):
        """Test context includes required permission."""
        error = InsufficientCapabilityError("write", "read")
        assert error.context["required_permission"] == "write"

    def test_context_includes_current_permission(self):
        """Test context includes current permission."""
        error = InsufficientCapabilityError("write", "read")
        assert error.context["current_permission"] == "read"

    def test_context_includes_error_code(self):
        """Test context includes error code."""
        error = InsufficientCapabilityError("write", "read")
        assert error.context["error_code"] == "INSUFFICIENT_CAPABILITY"

    def test_is_capability_error(self):
        """Test that it inherits from CapabilityError."""
        error = InsufficientCapabilityError("write", "read")
        assert isinstance(error, CapabilityError)

    def test_can_be_raised_and_caught(self):
        """Test raising and catching."""
        with pytest.raises(InsufficientCapabilityError):
            raise InsufficientCapabilityError("write", "read")


class TestCapabilityContextError:
    """Test CapabilityContextError exception."""

    def test_creation_with_message(self):
        """Test creating with message."""
        error = CapabilityContextError("Context stack empty")
        assert "Capability context error" in str(error)
        assert "Context stack empty" in str(error)

    def test_creation_with_context_id(self):
        """Test creating with context ID."""
        error = CapabilityContextError("Invalid context", "ctx-123")
        assert error.context["context_id"] == "ctx-123"

    def test_context_includes_error_code(self):
        """Test context includes error code."""
        error = CapabilityContextError("test")
        assert error.context["error_code"] == "CAPABILITY_CONTEXT_ERROR"

    def test_is_capability_error(self):
        """Test that it inherits from CapabilityError."""
        error = CapabilityContextError("test")
        assert isinstance(error, CapabilityError)

    def test_can_be_raised_and_caught(self):
        """Test raising and catching."""
        with pytest.raises(CapabilityContextError):
            raise CapabilityContextError("test")


class TestExceptionHierarchy:
    """Test exception inheritance hierarchy."""

    def test_all_inherit_from_capability_error(self):
        """Test all exceptions inherit from CapabilityError."""
        exceptions = [
            CapabilityNotFoundError("test"),
            CapabilityExpiredError("test", "2024-01-01"),
            CapabilityValidationError("test"),
            InsufficientCapabilityError("write", "read"),
            CapabilityContextError("test"),
        ]
        for exc in exceptions:
            assert isinstance(exc, CapabilityError)

    def test_all_inherit_from_exception(self):
        """Test all exceptions inherit from Exception."""
        exceptions = [
            CapabilityError("test"),
            CapabilityNotFoundError("test"),
            CapabilityExpiredError("test", "2024-01-01"),
            CapabilityValidationError("test"),
            InsufficientCapabilityError("write", "read"),
            CapabilityContextError("test"),
        ]
        for exc in exceptions:
            assert isinstance(exc, Exception)

    def test_can_catch_all_with_capability_error(self):
        """Test catching all capability exceptions with base class."""
        with pytest.raises(CapabilityError):
            raise CapabilityNotFoundError("test")

        with pytest.raises(CapabilityError):
            raise CapabilityExpiredError("test", "2024-01-01")

        with pytest.raises(CapabilityError):
            raise CapabilityValidationError("test")

    def test_specific_exceptions_can_be_caught_separately(self):
        """Test specific exceptions can be caught individually."""
        with pytest.raises(CapabilityNotFoundError):
            raise CapabilityNotFoundError("test")

        with pytest.raises(CapabilityExpiredError):
            raise CapabilityExpiredError("test", "2024-01-01")

        with pytest.raises(CapabilityValidationError):
            raise CapabilityValidationError("test")
