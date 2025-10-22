"""Test runner for ML capability introspection integration test.

This script executes the capability_introspection.ml test file with
proper capability context setup to demonstrate all three functions.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from mlpy.ml.transpiler import MLTranspiler
from mlpy.runtime.capabilities import CapabilityContext, CapabilityToken
from mlpy.runtime.capabilities.tokens import CapabilityConstraint
from mlpy.runtime.whitelist_validator import set_capability_context


def main():
    """Run the ML capability introspection integration test."""
    print("="* 80)
    print("ML CAPABILITY INTROSPECTION INTEGRATION TEST")
    print("="* 80)
    print()

    # Read ML test file
    ml_file = Path(__file__).parent / 'tests' / 'ml_integration' / 'capability_introspection.ml'
    if not ml_file.exists():
        print(f"ERROR: ML test file not found: {ml_file}")
        return 1

    ml_code = ml_file.read_text(encoding='utf-8')

    # Create transpiler
    transpiler = MLTranspiler()

    print("Transpiling ML code...")
    python_code, issues, source_map = transpiler.transpile_to_python(
        ml_code,
        strict_security=False
    )

    if not python_code:
        print("ERROR: Transpilation failed!")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("Transpilation successful!")
    print()

    # Create capability context with various capabilities for testing
    with CapabilityContext() as ctx:
        # Add basic file capabilities
        ctx.add_capability(CapabilityToken(capability_type='file.read'))
        ctx.add_capability(CapabilityToken(capability_type='file.write'))

        # Add file capability with constraints
        file_constraint = CapabilityConstraint(
            resource_patterns=['*.txt', 'data/*.json'],
            allowed_operations={'read'},
            max_usage_count=100
        )
        ctx.add_capability(CapabilityToken(
            capability_type='file.restricted',
            constraints=file_constraint
        ))

        # Add network capability (to show capability detection)
        # ctx.add_capability(CapabilityToken(capability_type='network.http'))

        # Set active context
        set_capability_context(ctx)

        # Execute transpiled code
        exec_globals = {
            '__name__': '__main__',
        }

        try:
            print("-" * 80)
            print("EXECUTING ML CODE:")
            print("-" * 80)
            print()

            exec(python_code, exec_globals)

            print()
            print("=" * 80)
            print("TEST COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            return 0

        except Exception as e:
            print()
            print("=" * 80)
            print("ERROR DURING EXECUTION!")
            print("=" * 80)
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return 1

        finally:
            # Clear context
            set_capability_context(None)


if __name__ == '__main__':
    sys.exit(main())
