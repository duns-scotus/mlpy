#!/usr/bin/env python3
"""Detailed AST debugging for function call resolution."""

from mlpy.ml.grammar.parser import MLParser
from mlpy.ml.grammar.ast_nodes import *

def debug_detailed():
    """Debug AST parsing in detail."""
    ml_code = """
    import collections;

    function testFunction() {
        result = collections.append([1, 2], 3);
        return result;
    }
    """

    parser = MLParser()
    ast = parser.parse(ml_code, "debug.ml")

    print("=== DETAILED AST ANALYSIS ===")

    # Find the function definition
    func_def = None
    for item in ast.items:
        if isinstance(item, FunctionDefinition):
            func_def = item
            break

    if func_def:
        print(f"Found function: {func_def.name}")
        print(f"Function body has {len(func_def.body)} statements")

        for i, stmt in enumerate(func_def.body):
            print(f"\nStatement {i}: {stmt.__class__.__name__}")

            if isinstance(stmt, AssignmentStatement):
                print(f"  Target: {stmt.target}")
                print(f"  Target type: {type(stmt.target)}")
                print(f"  Value type: {stmt.value.__class__.__name__}")

                if isinstance(stmt.value, FunctionCall):
                    print(f"  Function call:")
                    print(f"    function: {stmt.value.function}")
                    print(f"    function type: {type(stmt.value.function)}")
                    print(f"    arguments: {len(stmt.value.arguments)}")

                    # Check if function is a MemberAccess
                    if hasattr(stmt.value.function, '__class__'):
                        func_expr = stmt.value.function
                        print(f"    function expression: {func_expr.__class__.__name__}")

                        if isinstance(func_expr, MemberAccess):
                            print(f"      object: {func_expr.object}")
                            print(f"      object type: {type(func_expr.object)}")
                            print(f"      member: {func_expr.member}")
                            print(f"      member type: {type(func_expr.member)}")

                            if isinstance(func_expr.object, Identifier):
                                print(f"        object name: {func_expr.object.name}")
                        elif isinstance(func_expr, Identifier):
                            print(f"      simple function name: {func_expr.name}")

if __name__ == "__main__":
    debug_detailed()