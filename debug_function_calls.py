#!/usr/bin/env python3
"""Debug script to understand function call resolution."""

from mlpy.ml.transpiler import transpile_ml_code
from mlpy.ml.grammar.parser import MLParser
from mlpy.ml.grammar.ast_nodes import *

def debug_function_calls():
    """Debug how function calls are parsed and generated."""
    ml_code = """
    import collections;

    function testFunction() {
        list = [1, 2, 3];
        result = collections.append(list, 4);
        return result;
    }
    """

    # Parse the code to see AST structure
    parser = MLParser()
    ast = parser.parse(ml_code, "debug.ml")

    print("=== AST STRUCTURE ===")
    print_ast(ast, 0)

    print("\n=== TRANSPILATION ===")
    result = transpile_ml_code(ml_code, "debug.ml")
    generated_code = result[0] if isinstance(result, tuple) else result
    print(generated_code)

def print_ast(node, indent=0):
    """Print AST structure for debugging."""
    prefix = "  " * indent
    if hasattr(node, '__class__'):
        print(f"{prefix}{node.__class__.__name__}", end="")

        if isinstance(node, FunctionCall):
            print(f" - function: {node.function} (type: {type(node.function)})")
        elif isinstance(node, MemberAccess):
            print(f" - object: {node.object}, member: {node.member}")
        elif isinstance(node, Identifier):
            print(f" - name: {node.name}")
        else:
            print()

        # Recurse through child nodes
        if hasattr(node, 'items') and node.items:
            for item in node.items:
                print_ast(item, indent + 1)

        if hasattr(node, 'body') and node.body:
            for stmt in node.body:
                print_ast(stmt, indent + 1)

        if hasattr(node, 'arguments') and node.arguments:
            for arg in node.arguments:
                print_ast(arg, indent + 1)

        if hasattr(node, 'function') and hasattr(node.function, '__class__'):
            print_ast(node.function, indent + 1)

        if hasattr(node, 'object') and hasattr(node.object, '__class__'):
            print_ast(node.object, indent + 1)

if __name__ == "__main__":
    debug_function_calls()