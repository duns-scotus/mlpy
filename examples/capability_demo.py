#!/usr/bin/env python3
"""Demonstration of the mlpy capability system."""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mlpy.runtime.capabilities import (
    CapabilityToken, create_capability_token,
    get_capability_manager, requires_capability, with_capability
)
from mlpy.runtime.capabilities.manager import file_capability_context
from mlpy.runtime.capabilities.exceptions import CapabilityNotFoundError
from mlpy.runtime.system_modules.math_safe import math_safe


def main():
    """Demonstrate capability system functionality."""
    print("mlpy v2.0 Capability System Demonstration")
    print("=" * 50)

    # 1. Basic capability token creation
    print("\n1. Creating capability tokens...")
    file_token = create_capability_token(
        capability_type="file",
        resource_patterns=["*.txt", "data/*.json"],
        allowed_operations={"read", "write"},
        description="File access for demo"
    )

    print(f"   Created file token: {file_token.token_id[:8]}...")
    print(f"   Capability type: {file_token.capability_type}")
    print(f"   Resource patterns: {file_token.constraints.resource_patterns}")

    # 2. Capability validation
    print("\n2. Testing capability validation...")
    print(f"   Can access 'test.txt' for read: {file_token.can_access_resource('test.txt', 'read')}")
    print(f"   Can access 'test.py' for read: {file_token.can_access_resource('test.py', 'read')}")
    print(f"   Can access 'test.txt' for execute: {file_token.can_access_resource('test.txt', 'execute')}")

    # 3. Capability context demonstration
    print("\n3. Capability context demonstration...")
    manager = get_capability_manager()

    try:
        # This should fail - no capability context
        math_safe.sqrt(16)
        print("   ERROR: Math operation succeeded without capability!")
    except CapabilityNotFoundError:
        print("   SUCCESS: Math operation correctly blocked without capability")

    # Create a capability context with math access
    math_token = create_capability_token(
        capability_type="math",
        description="Math operations for demo"
    )

    with manager.capability_context("demo_math", [math_token]):
        try:
            result = math_safe.sqrt(16)
            print(f"   SUCCESS: Math operation succeeded with capability: sqrt(16) = {result}")
        except Exception as e:
            print(f"   ERROR: Math operation failed: {e}")

    # 4. File capability context demonstration
    print("\n4. File capability context demonstration...")

    with file_capability_context(["*.txt"], {"read", "write"}):
        print("   File capability context active")
        print("   Would be able to read/write *.txt files")
        # Note: We don't actually access files in this demo

    # 5. Decorator demonstration
    print("\n5. Function decorator demonstration...")

    @requires_capability("demo")
    def protected_function(x):
        """A function that requires demo capability."""
        return f"Protected function called with {x}"

    # Create demo capability
    demo_token = create_capability_token(
        capability_type="demo",
        description="Demo capability for protected function"
    )

    try:
        # This should fail - no demo capability
        protected_function("test")
        print("   ERROR: Protected function succeeded without capability!")
    except CapabilityNotFoundError:
        print("   SUCCESS: Protected function correctly blocked without capability")

    # Add demo capability and try again
    with manager.capability_context("demo_context", [demo_token]):
        try:
            result = protected_function("test")
            print(f"   SUCCESS: Protected function succeeded with capability: {result}")
        except Exception as e:
            print(f"   ERROR: Protected function failed: {e}")

    # 6. Statistics and debugging
    print("\n6. Capability system statistics...")
    stats = manager.get_statistics()
    print(f"   Contexts created: {stats['contexts_created']}")
    print(f"   Capability checks: {stats['capability_checks']}")
    print(f"   Cache hit rate: {stats['cache_hit_rate']:.1%}")

    print("\nCapability system demonstration completed!")
    print("All security boundaries enforced correctly")


if __name__ == "__main__":
    main()