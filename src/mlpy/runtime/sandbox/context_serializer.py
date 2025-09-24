"""Capability context serialization for subprocess communication."""

import base64
import json
import time
from typing import Any

from ..capabilities.context import CapabilityContext
from ..capabilities.tokens import CapabilityToken


class ContextSerializationError(Exception):
    """Exception raised for context serialization errors."""

    pass


class CapabilityContextSerializer:
    """Serializer for capability contexts and tokens."""

    def __init__(self):
        """Initialize the serializer."""
        self.supported_token_types = {
            "file": CapabilityToken,
            "network": CapabilityToken,
            # Add more token types as needed
        }

    def serialize(self, context: CapabilityContext) -> bytes:
        """Serialize a capability context to bytes."""
        try:
            context_data = self._context_to_dict(context)

            # Use JSON for cross-platform compatibility
            json_str = json.dumps(context_data, default=self._json_serializer)
            return json_str.encode("utf-8")

        except Exception as e:
            raise ContextSerializationError(f"Failed to serialize context: {e}")

    def deserialize(self, data: bytes) -> CapabilityContext:
        """Deserialize bytes to a capability context."""
        try:
            json_str = data.decode("utf-8")
            context_data = json.loads(json_str, object_hook=self._json_deserializer)

            return self._dict_to_context(context_data)

        except Exception as e:
            raise ContextSerializationError(f"Failed to deserialize context: {e}")

    def _context_to_dict(self, context: CapabilityContext) -> dict[str, Any]:
        """Convert capability context to dictionary."""
        # Get all valid capabilities
        capabilities = {}
        for cap_type, token in context.get_all_capabilities(include_parents=False).items():
            if token.is_valid():
                capabilities[cap_type] = self._token_to_dict(token)

        return {
            "context_id": context.context_id,
            "name": context.name,
            "capabilities": capabilities,
            "parent_context_id": (
                context.parent_context.context_id if context.parent_context else None
            ),
            "serialization_time": time.time(),
            "version": "1.0",
        }

    def _dict_to_context(self, data: dict[str, Any]) -> CapabilityContext:
        """Convert dictionary to capability context."""
        # Create context (without parent for now - parent contexts
        # would need to be handled at a higher level)
        context = CapabilityContext(context_id=data["context_id"], name=data["name"])

        # Add capabilities
        for cap_type, token_data in data.get("capabilities", {}).items():
            try:
                token = self._dict_to_token(token_data)
                if token.is_valid():
                    context.add_capability(token)
            except Exception:
                # Skip invalid tokens
                continue

        return context

    def _token_to_dict(self, token: CapabilityToken) -> dict[str, Any]:
        """Convert capability token to dictionary."""
        base_data = {
            "token_id": token.token_id,
            "capability_type": token.capability_type,
            "created_at": (
                token.created_at.isoformat()
                if hasattr(token.created_at, "isoformat")
                else str(token.created_at)
            ),
            "created_by": token.created_by,
            "description": token.description,
            "usage_count": token.usage_count,
            "last_used_at": token.last_used_at.isoformat() if token.last_used_at else None,
            "token_type": self._get_token_type_name(token),
        }

        # Add token-specific constraint data
        if hasattr(token, "constraints") and token.constraints:
            constraint_data = {
                "resource_patterns": token.constraints.resource_patterns,
                "allowed_operations": list(token.constraints.allowed_operations),
                "allowed_hosts": token.constraints.allowed_hosts,
                "allowed_ports": token.constraints.allowed_ports,
                "max_usage_count": token.constraints.max_usage_count,
                "max_file_size": token.constraints.max_file_size,
                "max_memory": token.constraints.max_memory,
                "max_cpu_time": token.constraints.max_cpu_time,
            }
            base_data["constraints"] = constraint_data

        return base_data

    def _dict_to_token(self, data: dict[str, Any]) -> CapabilityToken:
        """Convert dictionary to capability token."""
        token_type_name = data.get("token_type", "base")

        if token_type_name == "file":
            return self._create_file_token(data)
        elif token_type_name == "network":
            return self._create_network_token(data)
        else:
            return self._create_base_token(data)

    def _create_base_token(self, data: dict[str, Any]) -> CapabilityToken:
        """Create a base capability token from data."""
        from datetime import datetime

        # Parse datetime fields
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at)
            except ValueError:
                created_at = datetime.now()

        return CapabilityToken(
            capability_type=data["capability_type"],
            token_id=data.get("token_id"),
            created_by=data.get("created_by", "system"),
            description=data.get("description", ""),
        )

    def _create_file_token(self, data: dict[str, Any]) -> CapabilityToken:
        """Create a file capability token from data."""
        from ..capabilities.tokens import create_file_capability

        constraints_data = data.get("constraints", {})
        patterns = constraints_data.get("resource_patterns", [])
        operations = set(constraints_data.get("allowed_operations", ["read"]))

        # Note: create_file_capability may not support all these parameters
        # This is a simplified reconstruction
        try:
            return create_file_capability(patterns=patterns, operations=operations)
        except TypeError:
            # Fallback to basic token if creation fails
            return self._create_base_token(data)

    def _create_network_token(self, data: dict[str, Any]) -> CapabilityToken:
        """Create a network capability token from data."""
        from ..capabilities.tokens import create_network_capability

        constraints_data = data.get("constraints", {})
        hosts = constraints_data.get("allowed_hosts", [])
        ports = constraints_data.get("allowed_ports", [80, 443])

        # Note: create_network_capability may not support all these parameters
        # This is a simplified reconstruction
        try:
            return create_network_capability(hosts=hosts, ports=ports)
        except TypeError:
            # Fallback to basic token if creation fails
            return self._create_base_token(data)

    def _get_token_type_name(self, token: CapabilityToken) -> str:
        """Get the type name for a token based on its capability type."""
        return token.capability_type if token.capability_type else "base"

    def _json_serializer(self, obj: Any) -> Any:
        """Custom JSON serializer for special types."""
        if isinstance(obj, set):
            return list(obj)
        elif hasattr(obj, "isoformat"):  # datetime objects
            return obj.isoformat()
        else:
            return str(obj)

    def _json_deserializer(self, data: dict[str, Any]) -> dict[str, Any]:
        """Custom JSON deserializer for special types."""
        # This is called for each dictionary in the JSON
        # We don't need special handling here as we handle types
        # in _dict_to_token and _dict_to_context
        return data

    def serialize_for_subprocess(self, context: CapabilityContext) -> str:
        """Serialize context for subprocess execution (base64 encoded)."""
        serialized_bytes = self.serialize(context)
        return base64.b64encode(serialized_bytes).decode("ascii")

    def deserialize_from_subprocess(self, encoded_data: str) -> CapabilityContext:
        """Deserialize context from subprocess data (base64 encoded)."""
        serialized_bytes = base64.b64decode(encoded_data.encode("ascii"))
        return self.deserialize(serialized_bytes)

    def validate_serialization(self, context: CapabilityContext) -> bool:
        """Validate that context can be serialized and deserialized correctly."""
        try:
            # Serialize and deserialize
            serialized = self.serialize(context)
            deserialized = self.deserialize(serialized)

            # Check basic properties
            if deserialized.context_id != context.context_id:
                return False

            if deserialized.name != context.name:
                return False

            # Check capabilities count
            original_caps = context.get_all_capabilities(include_parents=False)
            deserialized_caps = deserialized.get_all_capabilities(include_parents=False)

            if len(original_caps) != len(deserialized_caps):
                return False

            # Check individual capabilities
            for cap_type in original_caps:
                if cap_type not in deserialized_caps:
                    return False

                orig_token = original_caps[cap_type]
                deser_token = deserialized_caps[cap_type]

                if orig_token.capability_type != deser_token.capability_type:
                    return False

            return True

        except Exception:
            return False

    def get_serialized_size(self, context: CapabilityContext) -> int:
        """Get the size of serialized context in bytes."""
        try:
            serialized = self.serialize(context)
            return len(serialized)
        except Exception:
            return 0

    def create_minimal_context(self, capabilities: list[CapabilityToken]) -> CapabilityContext:
        """Create a minimal context with only the specified capabilities."""
        context = CapabilityContext(name="minimal_sandbox_context")

        for token in capabilities:
            if token.is_valid():
                context.add_capability(token)

        return context

    def extract_capabilities(self, context: CapabilityContext) -> list[CapabilityToken]:
        """Extract all valid capabilities from a context."""
        capabilities = []

        for token in context.get_all_capabilities(include_parents=True).values():
            if token.is_valid():
                capabilities.append(token)

        return capabilities

    def merge_contexts(self, *contexts: CapabilityContext) -> CapabilityContext:
        """Merge multiple contexts into a single context."""
        merged = CapabilityContext(name="merged_context")

        for context in contexts:
            for cap_type, token in context.get_all_capabilities(include_parents=False).items():
                if token.is_valid() and not merged.has_capability(cap_type, check_parents=False):
                    merged.add_capability(token)

        return merged
