"""
Tests for simple_bridge module - simplified callback bridge for capability testing.
"""

import pytest
import time
from mlpy.runtime.capabilities.simple_bridge import (
    MessageType,
    BridgeMessage,
    SimpleBridge,
)


class TestMessageType:
    """Test MessageType enum."""

    def test_function_call_type(self):
        """Test FUNCTION_CALL message type."""
        assert MessageType.FUNCTION_CALL.value == "function_call"

    def test_function_response_type(self):
        """Test FUNCTION_RESPONSE message type."""
        assert MessageType.FUNCTION_RESPONSE.value == "function_response"

    def test_error_type(self):
        """Test ERROR message type."""
        assert MessageType.ERROR.value == "error"


class TestBridgeMessage:
    """Test BridgeMessage dataclass."""

    def test_default_message_creation(self):
        """Test creating message with defaults."""
        msg = BridgeMessage()
        assert msg.message_id  # Should have auto-generated UUID
        assert msg.message_type == MessageType.FUNCTION_CALL
        assert msg.sender_id == ""
        assert msg.recipient_id == ""
        assert msg.payload == {}
        assert msg.capabilities == []
        assert isinstance(msg.timestamp, float)

    def test_message_with_custom_values(self):
        """Test creating message with custom values."""
        msg = BridgeMessage(
            message_type=MessageType.FUNCTION_RESPONSE,
            sender_id="sender123",
            recipient_id="recipient456",
            payload={"result": 42},
            capabilities=["file:read", "net:http"],
        )
        assert msg.message_type == MessageType.FUNCTION_RESPONSE
        assert msg.sender_id == "sender123"
        assert msg.recipient_id == "recipient456"
        assert msg.payload == {"result": 42}
        assert msg.capabilities == ["file:read", "net:http"]

    def test_message_id_uniqueness(self):
        """Test that message IDs are unique."""
        msg1 = BridgeMessage()
        msg2 = BridgeMessage()
        assert msg1.message_id != msg2.message_id

    def test_timestamp_is_recent(self):
        """Test that timestamp is set to current time."""
        before = time.time()
        msg = BridgeMessage()
        after = time.time()
        assert before <= msg.timestamp <= after


class TestSimpleBridge:
    """Test SimpleBridge functionality."""

    @pytest.fixture
    def bridge(self):
        """Create a SimpleBridge instance."""
        return SimpleBridge()

    def test_bridge_initialization(self, bridge):
        """Test bridge initialization."""
        assert bridge.ml_handlers == {}
        assert bridge.system_handlers == {}
        assert hasattr(bridge, "_lock")

    def test_register_ml_handler(self, bridge):
        """Test registering an ML handler."""

        def test_handler(x):
            return x * 2

        bridge.register_ml_handler("double", test_handler)
        assert "double" in bridge.ml_handlers
        assert bridge.ml_handlers["double"] == test_handler

    def test_register_system_handler(self, bridge):
        """Test registering a system handler."""

        def test_handler(x):
            return x + 1

        bridge.register_system_handler("increment", test_handler)
        assert "increment" in bridge.system_handlers
        assert bridge.system_handlers["increment"] == test_handler

    def test_register_multiple_handlers(self, bridge):
        """Test registering multiple handlers."""

        def handler1():
            return 1

        def handler2():
            return 2

        def handler3():
            return 3

        bridge.register_ml_handler("func1", handler1)
        bridge.register_ml_handler("func2", handler2)
        bridge.register_system_handler("func3", handler3)

        assert len(bridge.ml_handlers) == 2
        assert len(bridge.system_handlers) == 1

    def test_call_ml_function_with_args(self, bridge):
        """Test calling ML function with arguments."""

        def multiply(x, y):
            return x * y

        bridge.register_ml_handler("multiply", multiply)
        result = bridge.call_ml_function("multiply", {"x": 3, "y": 4})
        assert result == 12

    def test_call_ml_function_without_args(self, bridge):
        """Test calling ML function without arguments."""

        def get_value():
            return 42

        bridge.register_ml_handler("get_value", get_value)
        result = bridge.call_ml_function("get_value")
        assert result == 42

    def test_call_ml_function_not_found(self, bridge):
        """Test calling non-existent ML function raises error."""
        with pytest.raises(ValueError, match="No handler for function: nonexistent"):
            bridge.call_ml_function("nonexistent")

    def test_call_system_function_with_args(self, bridge):
        """Test calling system function with arguments."""

        def add(a, b):
            return a + b

        bridge.register_system_handler("add", add)
        result = bridge.call_system_function("add", {"a": 5, "b": 7})
        assert result == 12

    def test_call_system_function_without_args(self, bridge):
        """Test calling system function without arguments."""

        def get_status():
            return "ok"

        bridge.register_system_handler("get_status", get_status)
        result = bridge.call_system_function("get_status")
        assert result == "ok"

    def test_call_system_function_not_found(self, bridge):
        """Test calling non-existent system function raises error."""
        with pytest.raises(ValueError, match="No handler for function: unknown"):
            bridge.call_system_function("unknown")

    def test_start_method(self, bridge):
        """Test start method (no-op)."""
        bridge.start()  # Should not raise

    def test_stop_method(self, bridge):
        """Test stop method (no-op)."""
        bridge.stop()  # Should not raise

    def test_context_manager(self, bridge):
        """Test using bridge as context manager."""
        with bridge as b:
            assert b is bridge
            assert isinstance(b, SimpleBridge)

    def test_context_manager_with_operations(self, bridge):
        """Test context manager with actual operations."""
        with bridge as b:
            b.register_ml_handler("test", lambda: "result")
            result = b.call_ml_function("test")
            assert result == "result"

    def test_handler_override(self, bridge):
        """Test overriding an existing handler."""

        def handler1():
            return "first"

        def handler2():
            return "second"

        bridge.register_ml_handler("func", handler1)
        assert bridge.call_ml_function("func") == "first"

        bridge.register_ml_handler("func", handler2)
        assert bridge.call_ml_function("func") == "second"

    def test_ml_and_system_handlers_independent(self, bridge):
        """Test ML and system handlers are independent."""

        def ml_func():
            return "ml"

        def system_func():
            return "system"

        bridge.register_ml_handler("func", ml_func)
        bridge.register_system_handler("func", system_func)

        assert bridge.call_ml_function("func") == "ml"
        assert bridge.call_system_function("func") == "system"

    def test_call_with_kwargs(self, bridge):
        """Test calling function with kwargs parameter."""

        def func_with_defaults(x, y=10):
            return x + y

        bridge.register_ml_handler("func", func_with_defaults)
        # The kwargs parameter exists but isn't used in current implementation
        result = bridge.call_ml_function("func", {"x": 5})
        assert result == 15

    def test_thread_safety_with_lock(self, bridge):
        """Test that lock is used for thread safety."""
        import threading

        results = []

        def register_and_call():
            for i in range(10):
                handler_name = f"handler_{threading.get_ident()}_{i}"
                bridge.register_ml_handler(handler_name, lambda i=i: i)
                results.append(bridge.call_ml_function(handler_name))

        threads = [threading.Thread(target=register_and_call) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Should have 50 results (5 threads * 10 calls)
        assert len(results) == 50


class TestBridgeIntegration:
    """Integration tests for bridge functionality."""

    def test_complete_workflow(self):
        """Test complete workflow with bridge."""
        bridge = SimpleBridge()

        # Register handlers
        bridge.register_ml_handler("calculate", lambda x, y: x * y)
        bridge.register_system_handler("validate", lambda x: x > 0)

        # Use bridge
        with bridge:
            result = bridge.call_ml_function("calculate", {"x": 3, "y": 4})
            assert result == 12

            valid = bridge.call_system_function("validate", {"x": result})
            assert valid is True

    def test_error_handling_workflow(self):
        """Test error handling in workflow."""
        bridge = SimpleBridge()

        with pytest.raises(ValueError):
            bridge.call_ml_function("nonexistent")

        with pytest.raises(ValueError):
            bridge.call_system_function("unknown")
