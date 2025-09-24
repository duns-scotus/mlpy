"""Tests for CallbackBridge secure communication system."""

import pytest
import threading
import time
from datetime import datetime, timedelta
from src.mlpy.runtime.capabilities.simple_bridge import (
    SimpleBridge as CallbackBridge, BridgeMessage, MessageType
)
from src.mlpy.runtime.capabilities import (
    create_capability_token, get_capability_manager, CapabilityNotFoundError
)


class TestBridgeMessage:
    """Test bridge message functionality."""

    def test_message_creation(self):
        """Test basic message creation."""
        message = BridgeMessage(
            message_type=MessageType.FUNCTION_CALL,
            sender_id="test_sender",
            recipient_id="test_recipient",
            payload={"function": "test_func", "args": {"x": 42}}
        )

        assert message.message_id is not None
        assert message.message_type == MessageType.FUNCTION_CALL
        assert message.sender_id == "test_sender"
        assert message.recipient_id == "test_recipient"
        assert message.payload["function"] == "test_func"

    def test_message_serialization(self):
        """Test message serialization and deserialization."""
        original = BridgeMessage(
            message_type=MessageType.CAPABILITY_REQUEST,
            sender_id="sender",
            recipient_id="recipient",
            payload={"capability": "file"},
            capabilities=["file", "network"]
        )

        # Serialize to dict
        message_dict = original.to_dict()

        # Deserialize from dict
        restored = BridgeMessage.from_dict(message_dict)

        assert restored.message_id == original.message_id
        assert restored.message_type == original.message_type
        assert restored.sender_id == original.sender_id
        assert restored.recipient_id == original.recipient_id
        assert restored.payload == original.payload
        assert restored.capabilities == original.capabilities


class TestCallbackBridge:
    """Test CallbackBridge functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.bridge = CallbackBridge()
        self.manager = get_capability_manager()

    def teardown_method(self):
        """Clean up after tests."""
        if self.bridge._running:
            self.bridge.stop()

    def test_bridge_initialization(self):
        """Test bridge initialization."""
        assert self.bridge.bridge_id is not None
        assert not self.bridge._running
        assert len(self.bridge._ml_handlers) == 0
        assert len(self.bridge._system_handlers) == 0

    def test_bridge_start_stop(self):
        """Test bridge start and stop functionality."""
        # Start bridge
        self.bridge.start()
        assert self.bridge._running
        assert self.bridge._processor_thread is not None

        # Stop bridge
        self.bridge.stop()
        assert not self.bridge._running

    def test_handler_registration(self):
        """Test handler registration."""
        def test_ml_handler(x):
            return x * 2

        def test_system_handler(y):
            return y + 1

        # Register handlers
        self.bridge.register_ml_handler("double", test_ml_handler)
        self.bridge.register_system_handler("increment", test_system_handler)

        assert "double" in self.bridge._ml_handlers
        assert "increment" in self.bridge._system_handlers
        assert self.bridge._ml_handlers["double"] == test_ml_handler
        assert self.bridge._system_handlers["increment"] == test_system_handler

    def test_ml_function_call_without_capabilities(self):
        """Test ML function call without capability requirements."""
        def test_function(x, y=10):
            return x + y

        self.bridge.register_ml_handler("add", test_function)
        self.bridge.start()

        try:
            result = self.bridge.call_ml_function("add", {"x": 5, "y": 3})
            assert result == 8
        finally:
            self.bridge.stop()

    def test_system_function_call(self):
        """Test system function call."""
        def system_function(name):
            return f"Hello, {name}!"

        self.bridge.register_system_handler("greet", system_function)
        self.bridge.start()

        try:
            result = self.bridge.call_system_function("greet", {"name": "World"})
            assert result == "Hello, World!"
        finally:
            self.bridge.stop()

    def test_function_call_timeout(self):
        """Test function call timeout handling."""
        self.bridge.start()

        try:
            with pytest.raises(TimeoutError):
                # Call non-existent function with short timeout
                self.bridge.call_ml_function("nonexistent", timeout=0.1)
        finally:
            self.bridge.stop()

    def test_capability_validation_success(self):
        """Test successful capability validation."""
        def protected_function(x):
            return x ** 2

        # Create capability token
        math_token = create_capability_token(
            capability_type="math",
            description="Math operations"
        )

        self.bridge.register_ml_handler("square", protected_function)
        self.bridge.start()

        try:
            # Call with capability context
            with self.manager.capability_context("test_math", [math_token]):
                result = self.bridge.call_ml_function(
                    "square",
                    {"x": 4},
                    required_capabilities=["math"]
                )
                assert result == 16
        finally:
            self.bridge.stop()

    def test_capability_validation_failure(self):
        """Test capability validation failure."""
        def protected_function(x):
            return x ** 2

        self.bridge.register_ml_handler("square", protected_function)
        self.bridge.start()

        try:
            # Call without capability context - should fail
            with pytest.raises(Exception):  # Should raise capability error
                self.bridge.call_ml_function(
                    "square",
                    {"x": 4},
                    required_capabilities=["math"]
                )
        finally:
            self.bridge.stop()

    def test_context_manager(self):
        """Test bridge as context manager."""
        def test_handler():
            return "success"

        with CallbackBridge() as bridge:
            bridge.register_ml_handler("test", test_handler)
            assert bridge._running

            result = bridge.call_ml_function("test")
            assert result == "success"

        # Bridge should be stopped after context exit
        assert not bridge._running

    def test_statistics_tracking(self):
        """Test bridge statistics tracking."""
        def test_handler(x):
            return x

        self.bridge.register_ml_handler("echo", test_handler)
        self.bridge.start()

        try:
            # Make some calls
            self.bridge.call_ml_function("echo", {"x": 1})
            self.bridge.call_ml_function("echo", {"x": 2})

            stats = self.bridge.get_statistics()
            assert stats["messages_sent"] >= 2
            assert stats["bridge_id"] == self.bridge.bridge_id
            assert stats["running"] == True
            assert stats["ml_handlers"] == 1
            assert stats["system_handlers"] == 0
        finally:
            self.bridge.stop()

    def test_concurrent_operations(self):
        """Test concurrent bridge operations."""
        def slow_handler(delay):
            time.sleep(delay / 1000)  # Convert ms to seconds
            return f"Completed after {delay}ms"

        self.bridge.register_ml_handler("slow", slow_handler)
        self.bridge.start()

        results = []
        errors = []

        def call_function(delay):
            try:
                result = self.bridge.call_ml_function("slow", {"delay": delay})
                results.append(result)
            except Exception as e:
                errors.append(e)

        try:
            # Start multiple concurrent calls
            threads = []
            for i in range(5):
                thread = threading.Thread(target=call_function, args=(10 * (i + 1),))
                threads.append(thread)
                thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join(timeout=2.0)

            assert len(errors) == 0, f"Unexpected errors: {errors}"
            assert len(results) == 5
        finally:
            self.bridge.stop()


class TestGlobalBridge:
    """Test global bridge functionality."""

    def teardown_method(self):
        """Reset global bridge after each test."""
        reset_callback_bridge()

    def test_global_bridge_singleton(self):
        """Test global bridge singleton behavior."""
        bridge1 = get_callback_bridge()
        bridge2 = get_callback_bridge()

        assert bridge1 is bridge2
        assert bridge1._running  # Should auto-start

    def test_global_bridge_reset(self):
        """Test global bridge reset functionality."""
        bridge1 = get_callback_bridge()
        bridge1_id = bridge1.bridge_id

        reset_callback_bridge()

        bridge2 = get_callback_bridge()
        assert bridge2.bridge_id != bridge1_id


class TestSecurityExploitPrevention:
    """Test security exploit prevention in bridge system."""

    def setup_method(self):
        """Set up test fixtures."""
        self.bridge = CallbackBridge()
        self.manager = get_capability_manager()

    def teardown_method(self):
        """Clean up after tests."""
        if self.bridge._running:
            self.bridge.stop()

    def test_capability_bypass_attempt(self):
        """Test that capability requirements cannot be bypassed."""
        def sensitive_operation():
            # This should require capabilities
            return "SENSITIVE_DATA"

        self.bridge.register_ml_handler("sensitive", sensitive_operation)
        self.bridge.start()

        try:
            # Attempt to call without required capability
            with pytest.raises(Exception):
                self.bridge.call_ml_function(
                    "sensitive",
                    required_capabilities=["admin"]
                )
        finally:
            self.bridge.stop()

    def test_message_tampering_protection(self):
        """Test protection against message tampering."""
        def handler(data):
            return f"Processed: {data}"

        self.bridge.register_ml_handler("process", handler)
        self.bridge.start()

        try:
            # Normal operation should work
            result = self.bridge.call_ml_function("process", {"data": "safe_data"})
            assert "safe_data" in result

            # Test with potentially malicious data
            malicious_data = {"__class__": "exploit", "eval": "dangerous_code"}
            result = self.bridge.call_ml_function("process", {"data": malicious_data})
            assert "exploit" in str(result)  # Should be safely stringified
        finally:
            self.bridge.stop()

    def test_resource_exhaustion_protection(self):
        """Test protection against resource exhaustion attacks."""
        call_count = 0

        def counting_handler():
            nonlocal call_count
            call_count += 1
            return call_count

        self.bridge.register_ml_handler("count", counting_handler)
        self.bridge.start()

        try:
            # Make many rapid calls
            for i in range(100):
                result = self.bridge.call_ml_function("count", timeout=0.1)
                assert result == i + 1

            # Bridge should still be responsive
            stats = self.bridge.get_statistics()
            assert stats["running"]
        finally:
            self.bridge.stop()

    def test_capability_context_isolation(self):
        """Test that capability contexts are properly isolated."""
        def context_sensitive_operation():
            # This should only work with proper context
            from src.mlpy.runtime.capabilities.context import get_current_context
            context = get_current_context()
            if context and context.has_capability("test"):
                return "AUTHORIZED"
            else:
                raise CapabilityNotFoundError("test")

        self.bridge.register_ml_handler("check_context", context_sensitive_operation)
        self.bridge.start()

        try:
            # Create capability token
            test_token = create_capability_token(
                capability_type="test",
                description="Test capability"
            )

            # Should work with capability
            with self.manager.capability_context("test_context", [test_token]):
                result = self.bridge.call_ml_function(
                    "check_context",
                    required_capabilities=["test"]
                )
                assert result == "AUTHORIZED"

            # Should fail without capability
            with pytest.raises(Exception):
                self.bridge.call_ml_function("check_context")

        finally:
            self.bridge.stop()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])