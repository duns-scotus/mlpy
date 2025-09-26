"""Simplified CallbackBridge for testing capability integration."""

import threading
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MessageType(Enum):
    """Types of messages that can be sent through the bridge."""

    FUNCTION_CALL = "function_call"
    FUNCTION_RESPONSE = "function_response"
    ERROR = "error"


@dataclass
class BridgeMessage:
    """Message structure for bridge communication."""

    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_type: MessageType = MessageType.FUNCTION_CALL
    sender_id: str = ""
    recipient_id: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    capabilities: list[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)


class SimpleBridge:
    """Simplified bridge for testing."""

    def __init__(self) -> None:
        self.ml_handlers: dict[str, Callable] = {}
        self.system_handlers: dict[str, Callable] = {}
        self._lock = threading.RLock()

    def register_ml_handler(self, function_name: str, handler: Callable) -> None:
        """Register ML handler."""
        with self._lock:
            self.ml_handlers[function_name] = handler

    def register_system_handler(self, function_name: str, handler: Callable) -> None:
        """Register system handler."""
        with self._lock:
            self.system_handlers[function_name] = handler

    def call_ml_function(
        self, function_name: str, args: dict[str, Any] | None = None, **kwargs: Any
    ) -> Any:
        """Call ML function directly."""
        if function_name not in self.ml_handlers:
            raise ValueError(f"No handler for function: {function_name}")

        return self.ml_handlers[function_name](**(args or {}))

    def call_system_function(
        self, function_name: str, args: dict[str, Any] | None = None, **kwargs: Any
    ) -> Any:
        """Call system function directly."""
        if function_name not in self.system_handlers:
            raise ValueError(f"No handler for function: {function_name}")

        return self.system_handlers[function_name](**(args or {}))

    def start(self) -> None:
        """Start bridge (no-op for simple bridge)."""
        pass

    def stop(self) -> None:
        """Stop bridge (no-op for simple bridge)."""
        pass

    def __enter__(self) -> "SimpleBridge":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop()
