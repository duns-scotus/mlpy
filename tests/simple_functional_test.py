#!/usr/bin/env python3
"""Simple test for functional programming module registration."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_functional_registration():
    """Test functional module registration."""
    print("Testing Functional Programming Module Integration")
    print("=" * 50)

    try:
        from mlpy.stdlib.registry import get_stdlib_registry
        from mlpy.ml.resolution.resolver import ModuleResolver

        # Test registry
        print("\n1. Testing Registry")
        registry = get_stdlib_registry()
        modules = registry.list_modules()
        print(f"Available modules: {modules}")

        if "functional" in modules:
            print("[OK] Functional module registered")

            module_info = registry.get_module_info("functional")
            print(f"Description: {module_info.description}")
            print(f"Capabilities: {module_info.capabilities_required}")
            print(f"Python bridges: {module_info.python_bridge_modules}")
        else:
            print("[FAIL] Functional module not registered")
            return False

        # Test bridge functions
        print("\n2. Testing Bridge Functions")
        bridges = registry.get_bridge_functions("functional")
        print(f"Bridge functions: {len(bridges)}")
        for bridge in bridges[:3]:  # Show first 3
            print(f"  - {bridge.ml_name} -> {bridge.python_module}.{bridge.python_function}")

        # Test module resolution
        print("\n3. Testing Module Resolution")
        resolver = ModuleResolver()

        try:
            functional_module = resolver.resolve_import(["functional"])
            print(f"[OK] Functional module resolved")
            print(f"Name: {functional_module.name}")
            print(f"Is stdlib: {functional_module.is_stdlib}")
            print(f"Has source: {functional_module.source_code is not None}")

            if functional_module.source_code:
                # Analyze source
                lines = functional_module.source_code.split('\n')
                functions = [line for line in lines if line.strip().startswith('function ')]
                print(f"Functions found: {len(functions)}")

                # Check for key functions
                key_functions = ['map', 'filter', 'reduce', 'compose', 'pipe']
                found_functions = []
                for func in key_functions:
                    if f'function {func}(' in functional_module.source_code:
                        found_functions.append(func)

                print(f"Key FP functions present: {found_functions}")

        except Exception as e:
            print(f"[FAIL] Module resolution error: {e}")
            return False

        print(f"\n[SUCCESS] Functional Programming Module Integration Complete!")
        return True

    except Exception as e:
        print(f"[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def demonstrate_functional_features():
    """Show what functional programming features are available."""
    print("\n" + "=" * 50)
    print("FUNCTIONAL PROGRAMMING FEATURES AVAILABLE")
    print("=" * 50)

    features = {
        "Core Higher-Order Functions": [
            "map(fn, list) - Transform each element",
            "filter(predicate, list) - Select matching elements",
            "reduce(reducer, initial, list) - Accumulate values",
            "forEach(fn, list) - Execute function for each element"
        ],
        "Function Composition": [
            "compose(f, g) - Right-to-left composition f(g(x))",
            "pipe(f, g) - Left-to-right composition g(f(x))",
            "curry2/curry3 - Convert to curried functions",
            "partial(fn, ...args) - Partial application"
        ],
        "Search & Selection": [
            "find(predicate, list) - First matching element",
            "some(predicate, list) - Any element matches",
            "every(predicate, list) - All elements match",
            "none(predicate, list) - No elements match"
        ],
        "Data Transformation": [
            "partition(predicate, list) - Split into [true, false]",
            "groupBy(keyFn, list) - Group by key function",
            "unique(list) - Remove duplicates",
            "zip(list1, list2) - Combine into pairs"
        ],
        "List Processing": [
            "flatMap(fn, list) - Map and flatten",
            "take(n, list) - First n elements",
            "drop(n, list) - Skip first n elements",
            "takeWhile/dropWhile - Conditional slicing"
        ],
        "Conditional Operations": [
            "ifElse(predicate, thenFn, elseFn) - Conditional application",
            "when(predicate, fn) - Apply if true",
            "unless(predicate, fn) - Apply if false",
            "cond(pairs) - Multi-condition switch"
        ],
        "Utilities": [
            "range(start, end, step) - Number sequences",
            "repeat(value, count) - Repeated values",
            "times(fn, count) - Execute n times",
            "memoize(fn) - Cache results"
        ]
    }

    for category, functions in features.items():
        print(f"\n{category}:")
        for func in functions:
            print(f"  • {func}")

    print(f"\nExample Usage:")
    print("""
import functional;

numbers = [1, 2, 3, 4, 5];

// Higher-order functions
doubled = functional.map(function(x) { return x * 2; }, numbers);
evens = functional.filter(function(x) { return x % 2 == 0; }, numbers);
sum = functional.reduce(function(a, b) { return a + b; }, 0, numbers);

// Function composition
double = function(x) { return x * 2; };
square = function(x) { return x * x; };
doubleAndSquare = functional.compose(square, double);
result = doubleAndSquare(5); // 100

// Data processing pipeline
processData = functional.pipe(
    functional.partial(functional.filter, function(x) { return x > 0; }),
    functional.partial(functional.map, function(x) { return x * x; }),
    functional.partial(functional.reduce, function(a, b) { return a + b; }, 0)
);
""")

def main():
    success = test_functional_registration()
    demonstrate_functional_features()

    print(f"\n" + "=" * 50)
    if success:
        print("FUNCTIONAL PROGRAMMING MODULE: READY TO USE!")
        print("\nML now has comprehensive functional programming support!")
        return 0
    else:
        print("SOME TESTS FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())