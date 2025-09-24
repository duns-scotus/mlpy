"""CallbackBridge for secure system ↔ ML communication with capability forwarding."""

import queue
import threading
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .context import CapabilityContext, get_current_context
from .exceptions import CapabilityError, CapabilityNotFoundError
from .manager import get_capability_manager


class MessageType(Enum):
    """Types of messages that can be sent through the bridge."""

    FUNCTION_CALL = "function_call"
    FUNCTION_RESPONSE = "function_response"
    CAPABILITY_REQUEST = "capability_request"
    CAPABILITY_GRANT = "capability_grant"
    ERROR = "error"
    HEARTBEAT = "heartbeat"


@dataclass
class BridgeMessage:
    """Message structure for bridge communication."""

    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_type: MessageType = MessageType.FUNCTION_CALL
    sender_id: str = ""
    recipient_id: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    capabilities: list[str] = field(default_factory=list)  # Required capabilities
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "message_id": self.message_id,
            "message_type": self.message_type.value,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "payload": self.payload,
            "capabilities": self.capabilities,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BridgeMessage":
        """Create message from dictionary."""
        return cls(
            message_id=data["message_id"],
            message_type=MessageType(data["message_type"]),
            sender_id=data["sender_id"],
            recipient_id=data["recipient_id"],
            payload=data["payload"],
            capabilities=data["capabilities"],
            timestamp=data["timestamp"],
        )


class CallbackBridge:
    """Secure communication bridge between system and ML code with capability forwarding."""

    def __init__(self, bridge_id: str = None):
        """Initialize the callback bridge."""
        self.bridge_id = bridge_id or str(uuid.uuid4())

        # Message queues for bidirectional communication
        self._system_to_ml_queue: queue.Queue = queue.Queue()
        self._ml_to_system_queue: queue.Queue = queue.Queue()

        # Registered handlers
        self._ml_handlers: dict[str, Callable] = {}
        self._system_handlers: dict[str, Callable] = {}

        # Capability forwarding
        self._capability_context_stack: list[CapabilityContext] = []

        # Thread safety
        self._lock = threading.RLock()
        self._running = False
        self._processor_thread: threading.Thread | None = None

        # Statistics
        self._stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "capability_requests": 0,
            "capability_grants": 0,
            "errors": 0,
        }

    def start(self) -> None:
        """Start the bridge message processor."""
        with self._lock:
            if self._running:
                return

            self._running = True
            self._processor_thread = threading.Thread(
                target=self._message_processor, name=f"CallbackBridge-{self.bridge_id[:8]}"
            )
            self._processor_thread.daemon = True
            self._processor_thread.start()

    def stop(self) -> None:
        """Stop the bridge message processor."""
        with self._lock:
            if not self._running:
                return

            self._running = False

            # Send stop signal
            self._system_to_ml_queue.put(None)

            if self._processor_thread:
                self._processor_thread.join(timeout=5.0)

    def _message_processor(self) -> None:
        """Process messages in background thread."""
        while self._running:
            try:
                # Process system → ML messages
                try:
                    message = self._system_to_ml_queue.get(timeout=0.1)
                    if message is None:  # Stop signal
                        break
                    self._process_message(message, direction="system_to_ml")
                except queue.Empty:
                    pass

                # Process ML → system messages
                try:
                    message = self._ml_to_system_queue.get(timeout=0.1)
                    if message is None:  # Stop signal
                        break
                    self._process_message(message, direction="ml_to_system")
                except queue.Empty:
                    pass

            except Exception as e:
                self._stats["errors"] += 1
                print(f"CallbackBridge error: {e}")

    def _process_message(self, message: BridgeMessage, direction: str) -> None:
        """Process a single message."""
        try:
            # Validate capabilities
            if message.capabilities:
                self._validate_message_capabilities(message)

            # Route message to appropriate handler
            if direction == "system_to_ml":
                self._handle_ml_message(message)
            else:
                self._handle_system_message(message)

            self._stats["messages_received"] += 1

        except Exception as e:
            error_message = BridgeMessage(
                message_type=MessageType.ERROR,
                sender_id=self.bridge_id,
                recipient_id=message.sender_id,
                payload={"error": str(e), "original_message_id": message.message_id},
            )
            self._send_error(error_message)

    def _validate_message_capabilities(self, message: BridgeMessage) -> None:
        """Validate that required capabilities are available."""
        current_context = get_current_context()
        if not current_context:
            raise CapabilityNotFoundError("No capability context available")

        for capability_type in message.capabilities:
            if not current_context.has_capability(capability_type):
                raise CapabilityNotFoundError(capability_type)

    def _handle_ml_message(self, message: BridgeMessage) -> None:
        """Handle message from system to ML."""
        if message.message_type == MessageType.FUNCTION_CALL:
            function_name = message.payload.get("function")
            if function_name in self._ml_handlers:
                try:
                    # Execute function
                    result = self._ml_handlers[function_name](**message.payload.get("args", {}))

                    response = BridgeMessage(
                        message_type=MessageType.FUNCTION_RESPONSE,
                        sender_id=self.bridge_id,
                        recipient_id=message.sender_id,
                        payload={"result": result, "original_message_id": message.message_id},
                    )
                    self._ml_to_system_queue.put(response)
                except Exception as e:
                    error_response = BridgeMessage(
                        message_type=MessageType.ERROR,
                        sender_id=self.bridge_id,
                        recipient_id=message.sender_id,
                        payload={"error": str(e), "original_message_id": message.message_id},
                    )
                    self._ml_to_system_queue.put(error_response)

    def _handle_system_message(self, message: BridgeMessage) -> None:
        """Handle message from ML to system."""
        if message.message_type == MessageType.FUNCTION_CALL:
            function_name = message.payload.get("function")
            if function_name in self._system_handlers:
                try:
                    result = self._system_handlers[function_name](**message.payload.get("args", {}))

                    response = BridgeMessage(
                        message_type=MessageType.FUNCTION_RESPONSE,
                        sender_id=self.bridge_id,
                        recipient_id=message.sender_id,
                        payload={"result": result, "original_message_id": message.message_id},
                    )
                    self._system_to_ml_queue.put(response)
                except Exception as e:
                    error_response = BridgeMessage(
                        message_type=MessageType.ERROR,
                        sender_id=self.bridge_id,
                        recipient_id=message.sender_id,
                        payload={"error": str(e), "original_message_id": message.message_id},
                    )
                    self._system_to_ml_queue.put(error_response)

    def _create_capability_context(self, capability_types: list[str]) -> CapabilityContext:
        """Create capability context for message execution."""
        current_context = get_current_context()
        if not current_context:
            # If no current context, create a minimal context for bridge operations
            manager = get_capability_manager()
            bridge_context = manager.create_context("bridge_minimal")
            return bridge_context

        # Create child context with forwarded capabilities
        child_context = current_context.create_child_context("bridge_forwarded")

        # Forward relevant capabilities
        for capability_type in capability_types:
            try:
                token = current_context.get_capability(capability_type)
                child_context.add_capability(token)
            except CapabilityNotFoundError:
                pass  # Skip unavailable capabilities

        return child_context

    def register_ml_handler(self, function_name: str, handler: Callable) -> None:
        """Register a handler for ML function calls."""
        with self._lock:
            self._ml_handlers[function_name] = handler

    def register_system_handler(self, function_name: str, handler: Callable) -> None:
        """Register a handler for system function calls."""
        with self._lock:
            self._system_handlers[function_name] = handler

    def call_ml_function(
        self,
        function_name: str,
        args: dict[str, Any] = None,
        required_capabilities: list[str] = None,
        timeout: float = 30.0,
    ) -> Any:
        """Call an ML function from system side."""
        if not self._running:
            raise RuntimeError("Bridge is not running")

        message = BridgeMessage(
            message_type=MessageType.FUNCTION_CALL,
            sender_id="system",
            recipient_id="ml",
            payload={"function": function_name, "args": args or {}},
            capabilities=required_capabilities or [],
        )

        # Send message to ML side
        self._system_to_ml_queue.put(message)
        self._stats["messages_sent"] += 1

        # Wait for response from ML side
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = self._ml_to_system_queue.get(timeout=0.1)
                if (
                    response.message_type == MessageType.FUNCTION_RESPONSE
                    and response.payload.get("original_message_id") == message.message_id
                ):
                    return response.payload.get("result")
                elif response.message_type == MessageType.ERROR:
                    raise CapabilityError(
                        f"ML function call failed: {response.payload.get('error')}"
                    )
            except queue.Empty:
                continue

        raise TimeoutError(f"ML function call timed out: {function_name}")

    def call_system_function(
        self, function_name: str, args: dict[str, Any] = None, timeout: float = 30.0
    ) -> Any:
        """Call a system function from ML side."""
        if not self._running:
            raise RuntimeError("Bridge is not running")

        message = BridgeMessage(
            message_type=MessageType.FUNCTION_CALL,
            sender_id="ml",
            recipient_id="system",
            payload={"function": function_name, "args": args or {}},
        )

        # Send message to system side
        self._ml_to_system_queue.put(message)
        self._stats["messages_sent"] += 1

        # Wait for response from system side
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = self._system_to_ml_queue.get(timeout=0.1)
                if (
                    response.message_type == MessageType.FUNCTION_RESPONSE
                    and response.payload.get("original_message_id") == message.message_id
                ):
                    return response.payload.get("result")
                elif response.message_type == MessageType.ERROR:
                    raise CapabilityError(
                        f"System function call failed: {response.payload.get('error')}"
                    )
            except queue.Empty:
                continue

        raise TimeoutError(f"System function call timed out: {function_name}")

    def _send_error(self, error_message: BridgeMessage) -> None:
        """Send error message."""
        self._stats["errors"] += 1
        # In a real implementation, this would route to appropriate queue
        print(f"Bridge Error: {error_message.payload}")

    def get_statistics(self) -> dict[str, Any]:
        """Get bridge statistics."""
        with self._lock:
            return {
                **self._stats,
                "bridge_id": self.bridge_id,
                "running": self._running,
                "ml_handlers": len(self._ml_handlers),
                "system_handlers": len(self._system_handlers),
            }

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


# Global bridge instance
_global_bridge: CallbackBridge | None = None
_bridge_lock = threading.Lock()


def get_callback_bridge() -> CallbackBridge:
    """Get the global callback bridge instance."""
    global _global_bridge

    if _global_bridge is None:
        with _bridge_lock:
            if _global_bridge is None:
                _global_bridge = CallbackBridge()
                _global_bridge.start()

    return _global_bridge


def reset_callback_bridge() -> None:
    """Reset the global callback bridge (for testing)."""
    global _global_bridge
    with _bridge_lock:
        if _global_bridge:
            _global_bridge.stop()
        _global_bridge = None


# Convenience functions
def register_ml_handler(function_name: str, handler: Callable) -> None:
    """Register ML handler with global bridge."""
    get_callback_bridge().register_ml_handler(function_name, handler)


def register_system_handler(function_name: str, handler: Callable) -> None:
    """Register system handler with global bridge."""
    get_callback_bridge().register_system_handler(function_name, handler)


def call_ml_function(function_name: str, args: dict[str, Any] = None, **kwargs) -> Any:
    """Call ML function via global bridge."""
    return get_callback_bridge().call_ml_function(function_name, args, **kwargs)


def call_system_function(function_name: str, args: dict[str, Any] = None, **kwargs) -> Any:
    """Call system function via global bridge."""
    return get_callback_bridge().call_system_function(function_name, args, **kwargs)
