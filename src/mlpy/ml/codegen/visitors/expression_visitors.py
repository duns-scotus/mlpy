"""Expression visitor methods for Python code generation.

This module contains all visitor methods for ML expression AST nodes,
including binary/unary expressions, identifiers, function calls, arrow functions,
ternary expressions, and advanced language constructs.

Part of the modularized code generation system introduced in the
codegen refactoring (Phase 3c).
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mlpy.ml.grammar.ast_nodes import (
        BinaryExpression,
        UnaryExpression,
        Identifier,
        FunctionCall,
        ArrayAccess,
        SliceExpression,
        MemberAccess,
        TernaryExpression,
        ArrayDestructuring,
        ObjectDestructuring,
    )


class ExpressionVisitorsMixin:
    """Mixin providing expression visitor methods for code generation.

    This mixin contains visitor methods for all expression-related AST nodes:
    - Binary/unary expressions (handled by _generate_expression)
    - Identifiers and member access (handled by _generate_expression)
    - Function calls and arrow functions
    - Ternary expressions (condition ? true : false)
    - Advanced constructs (match, pipeline - stubs for future)
    - Destructuring patterns (array and object destructuring)

    Most visitor methods are stubs that delegate to _generate_expression(),
    which is defined in ExpressionHelpersMixin. The actual implementations
    (arrow_function, ternary_expression, destructuring) are included here.

    Inheritance chain: ExpressionVisitorsMixin → ExpressionHelpersMixin → GeneratorBase
    """

    # ============================================================================
    # Expression visitor stubs (delegated to _generate_expression)
    # ============================================================================

    def visit_binary_expression(self, node: "BinaryExpression"):
        """Visit binary expression node (e.g., a + b, x * y).

        Actual implementation is in _generate_expression() from ExpressionHelpersMixin.
        """
        pass  # Handled by _generate_expression

    def visit_unary_expression(self, node: "UnaryExpression"):
        """Visit unary expression node (e.g., -x, !flag).

        Actual implementation is in _generate_expression() from ExpressionHelpersMixin.
        """
        pass  # Handled by _generate_expression

    def visit_identifier(self, node: "Identifier"):
        """Visit identifier node (e.g., variable_name).

        Actual implementation is in _generate_expression() from ExpressionHelpersMixin.
        """
        pass  # Handled by _generate_expression

    def visit_function_call(self, node: "FunctionCall"):
        """Visit function call node (e.g., foo(arg1, arg2)).

        Actual implementation is in _generate_expression() from ExpressionHelpersMixin.
        """
        pass  # Handled by _generate_expression

    def visit_array_access(self, node: "ArrayAccess"):
        """Visit array access node (e.g., arr[0], arr[i]).

        Actual implementation is in _generate_expression() from ExpressionHelpersMixin.
        """
        pass  # Handled by _generate_expression

    def visit_slice_expression(self, node: "SliceExpression"):
        """Visit slice expression node (e.g., arr[1:5], arr[:10]).

        Actual implementation is in _generate_expression() from ExpressionHelpersMixin.
        """
        pass  # Handled by _generate_expression

    def visit_member_access(self, node: "MemberAccess"):
        """Visit member access node (e.g., obj.property, obj.method).

        Actual implementation is in _generate_expression() from ExpressionHelpersMixin.
        """
        pass  # Handled by _generate_expression

    # ============================================================================
    # Implemented expression visitors
    # ============================================================================

    def visit_arrow_function(self, node):
        """Generate Python code for arrow function (lambda expression).

        ML syntax: (x, y) => x + y
        Python output: lambda x, y: x + y

        Handles:
        - Parameter extraction from various parameter node types
        - Parameter scope tracking in symbol table
        - Body expression generation
        - Proper lambda syntax generation

        Args:
            node: ArrowFunction AST node with parameters and body

        Returns:
            str: Python lambda expression code
        """
        # Generate parameter list
        param_names = []
        param_names_set = set()
        for param in node.parameters:
            if hasattr(param, "name"):
                param_names.append(param.name)
                param_names_set.add(param.name)
            elif hasattr(param, "value"):
                param_names.append(param.value)
                param_names_set.add(param.value)
            else:
                param_name = str(param)
                param_names.append(param_name)
                param_names_set.add(param_name)

        # Push lambda parameters onto stack for body scope
        self.symbol_table['parameters'].append(param_names_set)

        params_str = ", ".join(param_names)
        body_code = self._generate_expression(node.body)

        # Pop lambda parameters from stack
        self.symbol_table['parameters'].pop()

        # Generate lambda function
        return f"lambda {params_str}: {body_code}"

    def visit_ternary_expression(self, node: "TernaryExpression"):
        """Generate Python code for ternary expression.

        ML syntax: condition ? true_value : false_value
        Python output: (true_value if condition else false_value)

        Args:
            node: TernaryExpression AST node with condition, true_value, false_value

        Returns:
            str: Python ternary expression code with parentheses
        """
        # Convert to Python ternary: true_value if condition else false_value
        condition_code = self._generate_expression(node.condition)
        true_code = self._generate_expression(node.true_value)
        false_code = self._generate_expression(node.false_value)

        return f"({true_code} if {condition_code} else {false_code})"

    # ============================================================================
    # Advanced language constructs (stubs for future implementation)
    # ============================================================================

    def visit_match_expression(self, node):
        """Stub implementation for match expression (pattern matching).

        Future ML syntax:
            match value {
                pattern1 => result1,
                pattern2 => result2,
                _ => default
            }

        Currently returns a comment indicating the feature is not implemented.
        """
        return "# Match expression not yet implemented"

    def visit_match_case(self, node):
        """Stub implementation for match case (individual pattern case).

        Part of match expression syntax. Will be implemented when
        pattern matching feature is added to the language.

        Currently returns a comment indicating the feature is not implemented.
        """
        return "# Match case not yet implemented"

    def visit_pipeline_expression(self, node):
        """Stub implementation for pipeline expression (function chaining).

        Future ML syntax:
            value |> func1 |> func2 |> func3

        Would generate nested function calls or comprehension-style code.
        Currently returns a comment indicating the feature is not implemented.
        """
        return "# Pipeline expression not yet implemented"

    # ============================================================================
    # Destructuring patterns
    # ============================================================================

    def visit_array_destructuring(self, node: "ArrayDestructuring"):
        """Generate Python code for array destructuring pattern.

        ML syntax: [a, b, c] = [1, 2, 3]
        Python output: (a, b, c)

        Returns a tuple of variable names for unpacking. The actual assignment
        is handled by visit_destructuring_assignment.

        Args:
            node: ArrayDestructuring AST node with elements list

        Returns:
            str: Python tuple pattern for unpacking
        """
        # Return tuple of variable names for unpacking
        return f"({', '.join(node.elements)})"

    def visit_object_destructuring(self, node: "ObjectDestructuring"):
        """Generate Python code for object destructuring pattern.

        ML syntax: {x, y, z} = obj

        For object destructuring, we need to generate separate assignment statements.
        This method returns the pattern info that visit_destructuring_assignment will use.

        Args:
            node: ObjectDestructuring AST node with properties dict

        Returns:
            dict: Properties dictionary for generating individual assignments
        """
        # For object destructuring, we need to generate separate assignment statements
        # This method returns the pattern info that visit_destructuring_assignment will use
        return node.properties

    def visit_destructuring_assignment(self, node):
        """Generate Python code for destructuring assignment.

        Handles both array and object destructuring patterns:

        Array destructuring:
            ML: [a, b, c] = [1, 2, 3]
            Python: a, b, c = [1, 2, 3]

        Object destructuring:
            ML: {x, y, z} = obj
            Python:
                x = obj['x']
                y = obj['y']
                z = obj['z']

        Args:
            node: DestructuringAssignment AST node with pattern and value
        """
        from mlpy.ml.grammar.ast_nodes import ArrayDestructuring, ObjectDestructuring

        if isinstance(node.pattern, ArrayDestructuring):
            # Array destructuring: [a, b, c] = [1, 2, 3] -> a, b, c = [1, 2, 3]
            # Track all destructured variables in symbol table
            for element in node.pattern.elements:
                self.symbol_table['variables'].add(element)

            pattern_code = ", ".join(node.pattern.elements)
            value_code = self._generate_expression(node.value)
            self._emit_line(f"{pattern_code} = {value_code}", node)

        elif isinstance(node.pattern, ObjectDestructuring):
            # Object destructuring: {x, y, z} = obj -> separate assignments
            value_code = self._generate_expression(node.value)
            for key, var_name in node.pattern.properties.items():
                # Track each destructured variable in symbol table
                self.symbol_table['variables'].add(var_name)
                self._emit_line(f"{var_name} = {value_code}['{key}']", node)

        else:
            self._emit_line("# Unknown destructuring pattern", node)

    def visit_spread_element(self, node):
        """Stub implementation for spread element (...array).

        Future ML syntax:
            new_array = [...array1, ...array2]
            func(...args)

        Would generate Python unpacking syntax (*args, **kwargs).
        Currently returns a comment indicating the feature is not implemented.
        """
        return "# Spread element not yet implemented"
