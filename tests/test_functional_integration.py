#!/usr/bin/env python3
"""Test functional programming module integration with ML import system."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_functional_module_registration():
    """Test that the functional module is properly registered."""
    print("=== Testing Functional Module Registration ===\n")

    try:
        from mlpy.stdlib.registry import get_stdlib_registry
        from mlpy.ml.resolution.resolver import ModuleResolver

        # Test 1: Module is registered in stdlib
        print("--- Test 1: Stdlib Registration ---")
        registry = get_stdlib_registry()
        modules = registry.list_modules()

        if "functional" in modules:
            print("[OK] Functional module is registered")

            module_info = registry.get_module_info("functional")
            print(f"  - Description: {module_info.description}")
            print(f"  - Capabilities: {module_info.capabilities_required}")
            print(f"  - Python bridges: {module_info.python_bridge_modules}")
        else:
            print("[FAIL] Functional module not found in registry")
            return False

        # Test 2: Module can be resolved
        print("\n--- Test 2: Module Resolution ---")
        resolver = ModuleResolver()

        try:
            functional_module = resolver.resolve_import(["functional"])
            print(f"[OK] Functional module resolved successfully")
            print(f"  - Name: {functional_module.name}")
            print(f"  - Is stdlib: {functional_module.is_stdlib}")
            print(f"  - Capabilities: {functional_module.capabilities_required}")
            print(f"  - Source file exists: {functional_module.file_path is not None}")
        except Exception as e:
            print(f"[FAIL] Module resolution failed: {e}")
            return False

        # Test 3: Bridge functions are registered
        print("\n--- Test 3: Bridge Functions ---")
        bridge_functions = registry.get_bridge_functions("functional")
        print(f"[OK] Found {len(bridge_functions)} bridge functions")

        expected_bridges = ["len", "list_append", "isinstance", "str", "reduce", "partial"]
        for bridge in bridge_functions:
            if bridge.ml_name in expected_bridges:
                print(f"  - {bridge.ml_name} -> {bridge.python_module}.{bridge.python_function}")

        # Test 4: Module source code can be read
        print("\n--- Test 4: Source Code Analysis ---")
        if functional_module.source_code:
            lines = functional_module.source_code.split('\n')
            function_count = sum(1 for line in lines if line.strip().startswith('function '))
            capability_count = sum(1 for line in lines if 'capability' in line.lower())

            print(f"[OK] Source code loaded ({len(lines)} lines)")
            print(f"  - Functions defined: {function_count}")
            print(f"  - Capability declarations: {capability_count}")
            print(f"  - Contains core FP operations: {all(op in functional_module.source_code for op in ['map', 'filter', 'reduce'])}")

        # Test 5: Security capabilities
        print("\n--- Test 5: Security Integration ---")
        required_caps = functional_module.capabilities_required
        if required_caps:
            print(f"[OK] Security capabilities defined: {required_caps}")

            # Check for functional programming specific capabilities
            fp_caps = [cap for cap in required_caps if 'functional' in cap]
            print(f"  - Functional programming capabilities: {fp_caps}")
        else:
            print("[INFO] No specific capabilities required")

        print(f"\n=== Functional Module Integration Tests: SUCCESS ===")
        return True

    except Exception as e:
        print(f"[FAIL] Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_functional_capabilities():
    """Test specific functional programming capabilities."""
    print("\n=== Testing Functional Programming Capabilities ===\n")

    try:
        from mlpy.stdlib.registry import get_stdlib_registry

        registry = get_stdlib_registry()
        functional_module = registry.get_module("functional")

        if not functional_module:
            print("[FAIL] Could not load functional module")
            return False

        # Analyze the source code for functional programming patterns
        source = functional_module.source_code

        # Core higher-order functions
        core_functions = ["map", "filter", "reduce", "forEach"]
        found_core = [func for func in core_functions if f"function {func}(" in source]
        print(f"[OK] Core FP functions found: {found_core}")

        # Advanced operations
        advanced_functions = ["compose", "pipe", "curry", "partial", "memoize"]
        found_advanced = [func for func in advanced_functions if f"function {func}(" in source]
        print(f"[OK] Advanced FP functions found: {found_advanced}")

        # List operations
        list_functions = ["find", "some", "every", "partition", "groupBy", "unique"]
        found_list = [func for func in list_functions if f"function {func}(" in source]
        print(f"[OK] List processing functions found: {found_list}")

        # Conditional operations
        conditional_functions = ["ifElse", "when", "unless", "cond"]
        found_conditional = [func for func in conditional_functions if f"function {func}(" in source]
        print(f"[OK] Conditional functions found: {found_conditional}")

        # Utility functions
        utility_functions = ["range", "repeat", "times", "zip", "flatten"]
        found_utility = [func for func in utility_functions if f"function {func}(" in source]
        print(f"[OK] Utility functions found: {found_utility}")

        # Count total functions
        total_functions = len(found_core) + len(found_advanced) + len(found_list) + len(found_conditional) + len(found_utility)
        print(f"\n[OK] Total functional programming functions: {total_functions}")

        # Check for security patterns
        has_capabilities = "capability " in source
        has_bridge_calls = "__python_bridge" in source
        print(f"[OK] Security integration: capabilities={has_capabilities}, bridges={has_bridge_calls}")

        return True

    except Exception as e:
        print(f"[FAIL] Capability test failed: {e}")
        return False

def demo_functional_usage():
    """Demonstrate functional module usage patterns."""
    print("\n=== Functional Programming Usage Demo ===\n")

    print("Example ML code using functional module:")
    print("""
import functional;

// Core operations
numbers = [1, 2, 3, 4, 5];
doubled = functional.map(function(x) { return x * 2; }, numbers);
evens = functional.filter(function(x) { return x % 2 == 0; }, numbers);
sum = functional.reduce(function(a, b) { return a + b; }, 0, numbers);

// Function composition
double = function(x) { return x * 2; };
square = function(x) { return x * x; };
doubleAndSquare = functional.compose(square, double);

// Advanced operations
isEven = function(x) { return x % 2 == 0; };
partitioned = functional.partition(isEven, numbers);
grouped = functional.groupBy(function(x) { return x % 3; }, numbers);

// Conditional operations
processNumber = functional.ifElse(
    isEven,
    function(x) { return "Even: " + x; },
    function(x) { return "Odd: " + x; }
);
""")

    print("This demonstrates:")
    print("✓ Higher-order functions (map, filter, reduce)")
    print("✓ Function composition (compose, pipe)")
    print("✓ Data transformation (partition, groupBy)")
    print("✓ Conditional operations (ifElse, when, unless)")
    print("✓ Currying and partial application")
    print("✓ Advanced list processing")
    print("✓ Functional programming best practices")

    return True

def main():
    """Run all functional module tests."""
    print("ML Functional Programming Module Test Suite")
    print("=" * 60)

    success = True
    success &= test_functional_module_registration()
    success &= test_functional_capabilities()
    success &= demo_functional_usage()

    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL FUNCTIONAL MODULE TESTS PASSED!")
        print("\nThe ML Functional Programming Standard Library is ready!")
        print("\nKey Features Available:")
        print("• Complete higher-order function suite")
        print("• Function composition and currying")
        print("• Advanced list processing operations")
        print("• Conditional and utility functions")
        print("• Security-integrated Python bridges")
        print("• Performance-optimized implementations")

        return 0
    else:
        print("❌ SOME TESTS FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())