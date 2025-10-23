"""
Test script to verify the sys.modules fix works correctly.

This test verifies that:
1. Modules loaded via registry are registered in sys.modules
2. Direct imports return the same module instance
3. isinstance() checks work correctly
4. CapabilityContext works across import styles
"""

import sys
from pathlib import Path

# Add mlpy to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=" * 80)
print("TESTING sys.modules FIX")
print("=" * 80)

# Test 1: Module registry registration
print("\n[Test 1] Module Registry Registration")
print("-" * 80)

from mlpy.stdlib.module_registry import get_registry

registry = get_registry()
datetime_instance = registry.get_module('datetime')

print(f"[OK] Loaded datetime via registry: {datetime_instance}")
print(f"  Type: {type(datetime_instance).__name__}")

# Check sys.modules
module_name = "mlpy.stdlib.datetime_bridge"
in_sys_modules = module_name in sys.modules
print(f"  '{module_name}' in sys.modules: {in_sys_modules}")

if not in_sys_modules:
    print(f"  [FAIL] FAIL: Module not registered in sys.modules!")
    sys.exit(1)

print("  [OK] PASS: Module properly registered in sys.modules")

# Test 2: Direct import returns same instance
print("\n[Test 2] Direct Import Returns Same Instance")
print("-" * 80)

from mlpy.stdlib.datetime_bridge import DateTime

print(f"[OK] Direct import DateTime class: {DateTime}")
print(f"  Registry DateTime: {datetime_instance.__class__}")
print(f"  Are they the same class? {datetime_instance.__class__ is DateTime}")

if datetime_instance.__class__ is not DateTime:
    print(f"  [FAIL] FAIL: Classes are different instances!")
    print(f"    Registry class ID: {id(datetime_instance.__class__)}")
    print(f"    Direct import ID:  {id(DateTime)}")
    sys.exit(1)

print("  [OK] PASS: Same class instance returned")

# Test 3: isinstance() checks work
print("\n[Test 3] isinstance() Checks Work Correctly")
print("-" * 80)

from mlpy.stdlib.datetime_bridge import DateTimeObject
from mlpy.runtime.capabilities import CapabilityContext, create_capability_token
from mlpy.runtime.capabilities.context import capability_context

# Create a DateTimeObject
ctx = CapabilityContext(name='test')
token = create_capability_token('datetime.now')
ctx.add_capability(token)

with capability_context(ctx):
    dt_obj = datetime_instance.now()

print(f"[OK] Created datetime object: {dt_obj}")
print(f"  Type: {type(dt_obj).__name__}")
print(f"  isinstance(dt_obj, DateTimeObject)? {isinstance(dt_obj, DateTimeObject)}")

if not isinstance(dt_obj, DateTimeObject):
    print(f"  [FAIL] FAIL: isinstance() check failed!")
    print(f"    Object class: {type(dt_obj)}")
    print(f"    Expected class: {DateTimeObject}")
    print(f"    Object class ID: {id(type(dt_obj))}")
    print(f"    Expected ID:     {id(DateTimeObject)}")
    sys.exit(1)

print("  [OK] PASS: isinstance() check works correctly")

# Test 4: Capability Context works across import styles
print("\n[Test 4] CapabilityContext Works Across Import Styles")
print("-" * 80)

try:
    # Import via different paths
    from mlpy.runtime.capabilities import CapabilityContext as CapCtx1
    from mlpy.runtime.capabilities.context import CapabilityContext as CapCtx2

    print(f"[OK] Imported CapabilityContext via two different paths")
    print(f"  Path 1 (mlpy.runtime.capabilities): {CapCtx1}")
    print(f"  Path 2 (mlpy.runtime.capabilities.context): {CapCtx2}")
    print(f"  Are they the same class? {CapCtx1 is CapCtx2}")

    if CapCtx1 is not CapCtx2:
        print(f"  [FAIL] FAIL: Different CapabilityContext classes!")
        sys.exit(1)

    # Test that thread-local storage works
    ctx1 = CapCtx1(name='test1')
    token = create_capability_token('test.capability')
    ctx1.add_capability(token)

    with capability_context(ctx1):
        # This should work without AttributeError
        from mlpy.runtime.capabilities.context import get_current_context
        current = get_current_context()
        print(f"  [OK] Current context: {current.name if current else 'None'}")

        if current is None or current.name != 'test1':
            print(f"  [FAIL] FAIL: Thread-local context not working!")
            sys.exit(1)

    print("  [OK] PASS: CapabilityContext works correctly across imports")

except AttributeError as e:
    print(f"  [FAIL] FAIL: AttributeError occurred: {e}")
    sys.exit(1)

# Test 5: Multiple module loads
print("\n[Test 5] Multiple Module Loads Return Same Instance")
print("-" * 80)

# Load datetime again
datetime_instance2 = registry.get_module('datetime')

print(f"[OK] Loaded datetime a second time: {datetime_instance2}")
print(f"  First load:  {id(datetime_instance)}")
print(f"  Second load: {id(datetime_instance2)}")
print(f"  Are they the same instance? {datetime_instance is datetime_instance2}")

if datetime_instance is not datetime_instance2:
    print(f"  [FAIL] FAIL: Different instances returned!")
    sys.exit(1)

print("  [OK] PASS: Same instance returned on multiple loads")

# Test 6: Other modules also work
print("\n[Test 6] Other Standard Library Modules")
print("-" * 80)

test_modules = ['math', 'string', 'regex']
for mod_name in test_modules:
    if registry.is_available(mod_name):
        mod = registry.get_module(mod_name)
        sys_mod_name = f"mlpy.stdlib.{mod_name}_bridge"
        in_sys = sys_mod_name in sys.modules
        print(f"  {mod_name:10s}: loaded={str(mod is not None):5s}, in sys.modules={str(in_sys):5s}")

        if mod and not in_sys:
            print(f"    [FAIL] FAIL: {mod_name} not in sys.modules!")
            sys.exit(1)

print("  [OK] PASS: All tested modules properly registered")

# Final summary
print("\n" + "=" * 80)
print("ALL TESTS PASSED [OK]")
print("=" * 80)
print("\nThe sys.modules fix is working correctly:")
print("  [OK] Modules are registered in sys.modules")
print("  [OK] Direct imports return same instance")
print("  [OK] isinstance() checks work correctly")
print("  [OK] CapabilityContext works across import styles")
print("  [OK] Multiple loads return same instance")
print("  [OK] Other modules also work correctly")
print("\nThe fix resolves:")
print("  • isinstance() failures with DateTimeObject")
print("  • CapabilityContext AttributeError issues")
print("  • JSON serialization type checking")
print("  • Module identity inconsistencies")
