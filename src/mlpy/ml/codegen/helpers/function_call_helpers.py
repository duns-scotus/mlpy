"""Function call and lambda generation helper methods for Python code generation.

This module contains methods for:
1. Lambda generation from function definitions
2. Function call wrapping and security validation
3. Function call code generation (simple, member, wrapped, direct)
4. Error handling for unknown functions

Part of the modular code generator architecture (Phase 3e).
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mlpy.ml.grammar.ast_nodes import (
        FunctionCall,
        FunctionDefinition,
        MemberAccess,
        Identifier,
        ReturnStatement,
        AssignmentStatement,
    )


class FunctionCallHelpersMixin:
    """Mixin providing function call and lambda generation methods.

    This mixin handles all aspects of function call code generation:
    - Lambda expression generation from function definitions
    - Variable substitution in lambda bodies
    - Function call wrapping with security validation
    - Simple and member function calls
    - Error reporting for unknown functions

    Dependencies:
    - ExpressionHelpersMixin: For _generate_expression(), _safe_identifier()
    - GeneratorBase: For symbol_table, context, function_registry
    """

    # ============================================================================
    # Lambda Generation Methods
    # ============================================================================

    def _generate_lambda_from_function_def(self, func_def: "FunctionDefinition") -> str:
        """Generate a lambda expression from a FunctionDefinition used as an expression.

        Handles conversion of ML function definitions to Python lambda expressions.
        Supports single-expression lambdas and multi-statement functions with
        variable substitution.

        Args:
            func_def: FunctionDefinition AST node with parameters and body

        Returns:
            Python lambda expression string: "lambda x, y: x + y"

        Examples:
            ML: function(x) { return x + 1; }
            Python: lambda x: x + 1

            ML: function(a, b) { let sum = a + b; return sum * 2; }
            Python: lambda a, b: (a + b) * 2  # with substitution

        Note:
            Multi-statement functions undergo variable substitution to create
            valid lambda expressions. If substitution fails, falls back to
            direct expression generation which may reference undefined variables.
        """
        from mlpy.ml.grammar.ast_nodes import ReturnStatement

        # Build parameter list
        params = []
        param_names_set = set()
        for param in func_def.parameters:
            if hasattr(param, "name"):
                param_name = self._safe_identifier(param.name)
            else:
                param_name = self._safe_identifier(str(param))
            params.append(param_name)
            param_names_set.add(param_name)

        params_str = ", ".join(params)

        # Push parameters onto stack for lambda scope
        self.symbol_table['parameters'].append(param_names_set)

        try:
            # Handle function body - for lambda, we need a single expression
            if len(func_def.body) == 1 and isinstance(func_def.body[0], ReturnStatement):
                # Single return statement - extract the expression
                return_stmt = func_def.body[0]
                body_code = self._generate_expression(return_stmt.value)
                return f"lambda {params_str}: {body_code}"
            else:
                # Multiple statements - need to handle variable substitution
                # Find the return statement and substitute variables

                # Find the last return statement
                last_return = None
                for stmt in reversed(func_def.body):
                    if isinstance(stmt, ReturnStatement):
                        last_return = stmt
                        break

                if last_return and last_return.value:
                    # Try to substitute variables to create a valid lambda expression
                    substituted_expr = self._substitute_variables_in_lambda(
                        func_def.body, last_return.value, params
                    )
                    if substituted_expr:
                        return f"lambda {params_str}: {substituted_expr}"

                    # Fallback: generate the expression as-is (may have undefined variables)
                    body_code = self._generate_expression(last_return.value)
                    return f"lambda {params_str}: {body_code}"
                else:
                    # No return statement found, fall back to None
                    return f"lambda {params_str}: None"
        finally:
            # Pop parameters from stack
            self.symbol_table['parameters'].pop()

    def _substitute_variables_in_lambda(self, statements, return_expr, params):
        """Try to substitute variables in lambda to avoid undefined variable errors.

        Analyzes assignment statements in function body and inlines variable
        values into the return expression to create a valid single-expression lambda.

        Args:
            statements: List of statements in function body
            return_expr: Return expression AST node
            params: List of parameter names

        Returns:
            Substituted expression code string, or None if substitution fails

        Example:
            ML Function:
                function(x) {
                    let doubled = x * 2;
                    let squared = doubled * doubled;
                    return squared;
                }

            Substitution Process:
                doubled = x * 2
                squared = (x * 2) * (x * 2)
                return (x * 2) * (x * 2)

            Result:
                lambda x: (x * 2) * (x * 2)
        """
        from mlpy.ml.grammar.ast_nodes import AssignmentStatement

        # Build a map of variable assignments
        assignments = {}
        param_names = set()

        # Get parameter names
        for param in params:
            param_names.add(param)

        # Walk through statements to find assignments
        for stmt in statements:
            if isinstance(stmt, AssignmentStatement):
                if hasattr(stmt.target, "name"):
                    var_name = stmt.target.name
                    assignments[var_name] = stmt.value

        # Try to substitute the return expression
        try:
            substituted = self._substitute_expression(
                return_expr, assignments, param_names, depth=0
            )
            if substituted:
                return self._generate_expression(substituted)
        except:
            # If substitution fails, return None to use fallback
            pass

        return None

    def _substitute_expression(self, expr, assignments, param_names, depth=0):
        """Recursively substitute variables in an expression.

        Performs deep traversal of expression AST to inline variable values.
        Handles binary operations, function calls, member access, array access, etc.

        Args:
            expr: Expression AST node to substitute
            assignments: Dict mapping variable names to their assigned expressions
            param_names: Set of parameter names (don't substitute these)
            depth: Recursion depth (prevents infinite loops)

        Returns:
            New expression AST node with substitutions applied, or None if failed

        Supported Expression Types:
            - Identifier: Substitute if assigned, keep if parameter
            - BinaryExpression: Substitute both operands
            - UnaryExpression: Substitute operand
            - FunctionCall: Substitute arguments
            - MemberAccess: Substitute object
            - ArrayAccess: Substitute array and index
            - Literals: Return as-is

        Note:
            Recursion is limited to depth 10 to prevent infinite loops.
        """
        from mlpy.ml.grammar.ast_nodes import (
            ArrayAccess,
            BinaryExpression,
            FunctionCall,
            Identifier,
            MemberAccess,
            UnaryExpression,
        )

        # Prevent infinite recursion
        if depth > 10:
            return None

        if isinstance(expr, Identifier):
            var_name = expr.name
            # If it's a parameter, keep it as-is
            if var_name in param_names:
                return expr
            # If it's an assigned variable, substitute it
            elif var_name in assignments:
                # Recursively substitute the assigned expression
                return self._substitute_expression(
                    assignments[var_name], assignments, param_names, depth + 1
                )
            else:
                # Unknown variable - might be from outer scope, keep as-is
                return expr
        elif isinstance(expr, FunctionCall):
            # Substitute arguments in function calls
            new_args = []
            for arg in expr.arguments:
                substituted_arg = self._substitute_expression(
                    arg, assignments, param_names, depth + 1
                )
                if substituted_arg is None:
                    return None  # Failed to substitute
                new_args.append(substituted_arg)

            # Create new function call with substituted arguments
            new_call = FunctionCall(expr.function, new_args)
            return new_call
        elif isinstance(expr, BinaryExpression):
            # Substitute variables in both operands of binary expressions
            left_substituted = self._substitute_expression(
                expr.left, assignments, param_names, depth + 1
            )
            right_substituted = self._substitute_expression(
                expr.right, assignments, param_names, depth + 1
            )

            if left_substituted is None or right_substituted is None:
                return None  # Failed to substitute

            # Create new binary expression with substituted operands
            new_binary = BinaryExpression(left_substituted, expr.operator, right_substituted)
            return new_binary
        elif isinstance(expr, UnaryExpression):
            # Substitute variables in unary expressions
            operand_substituted = self._substitute_expression(
                expr.operand, assignments, param_names, depth + 1
            )

            if operand_substituted is None:
                return None  # Failed to substitute

            # Create new unary expression with substituted operand
            new_unary = UnaryExpression(expr.operator, operand_substituted)
            return new_unary
        elif isinstance(expr, MemberAccess):
            # Substitute variables in member access (obj.member)
            object_substituted = self._substitute_expression(
                expr.object, assignments, param_names, depth + 1
            )

            if object_substituted is None:
                return None  # Failed to substitute

            # Create new member access with substituted object
            new_member = MemberAccess(object_substituted, expr.member)
            return new_member
        elif isinstance(expr, ArrayAccess):
            # Substitute variables in array access (arr[index])
            array_substituted = self._substitute_expression(
                expr.array, assignments, param_names, depth + 1
            )
            index_substituted = self._substitute_expression(
                expr.index, assignments, param_names, depth + 1
            )

            if array_substituted is None or index_substituted is None:
                return None  # Failed to substitute

            # Create new array access with substituted parts
            new_array_access = ArrayAccess(array_substituted, index_substituted)
            return new_array_access
        else:
            # For other expression types (literals, etc.), return as-is
            return expr

    # ============================================================================
    # Function Call Wrapping Logic
    # ============================================================================

    def _should_wrap_call(self, func_expr) -> bool:
        """Determine if function call should be wrapped with _safe_call.

        Implements security policy for function calls:
        - User-defined functions: Trusted, no wrapping
        - ML builtins: Wrapped for validation
        - Module functions: Wrapped for validation
        - Dynamic expressions: Wrapped for safety

        Wrapping Rules:
        - User-defined functions: NO (trusted)
        - Everything else: YES (needs validation)

        Args:
            func_expr: Function expression (string for simple calls, MemberAccess for obj.method)

        Returns:
            True if call should be wrapped with _safe_call

        Examples:
            myFunc() -> False (user-defined, direct call)
            len() -> True (builtin, wrapped)
            math.sqrt() -> True (module function, wrapped)
            arr.map(f) -> True (method call, wrapped)
            someVar() -> True (dynamic, wrapped)
        """
        from mlpy.ml.grammar.ast_nodes import MemberAccess

        # Case 1: String function name (simple identifier call)
        if isinstance(func_expr, str):
            # Check if it's a known ML builtin function
            if self.function_registry.is_allowed_builtin(func_expr):
                return True  # ML builtin, needs wrapping for validation

            # Check if it's a user-defined function
            if self.function_registry.is_user_defined(func_expr):
                return False  # User-defined, don't wrap

            # Unknown function name (could be variable) - wrap it
            return True

        # Case 2: Member access (module.func or obj.method)
        elif isinstance(func_expr, MemberAccess):
            # Always wrap - validation will check decorator/safe type
            return True

        # Case 3: Any other expression type
        else:
            # Dynamic expression - wrap it
            return True

    def _generate_function_call_wrapped(self, node: "FunctionCall") -> str:
        """Generate function call with selective _safe_call wrapping.

        Main entry point for all function call generation. Determines whether
        to wrap the call based on function type and security policy.

        Args:
            node: FunctionCall AST node

        Returns:
            Generated Python code (wrapped or unwrapped)

        Flow:
            1. Determine if call needs wrapping (_should_wrap_call)
            2. If yes: Generate wrapped call (_generate_wrapped_call)
            3. If no: Generate direct call (_generate_direct_call)

        Examples:
            myFunc(1, 2) -> myFunc(1, 2)  # user-defined, direct
            len([1, 2]) -> _safe_call(builtin.len, [1, 2])  # builtin, wrapped
            text.upper() -> _safe_method_call(text, 'upper')  # method, wrapped
        """
        # Determine if this call needs wrapping
        needs_wrap = self._should_wrap_call(node.function)

        if needs_wrap:
            # Generate wrapped call: _safe_call(func, args)
            return self._generate_wrapped_call(node)
        else:
            # Generate direct call: func(args)
            return self._generate_direct_call(node)

    def _generate_direct_call(self, node: "FunctionCall") -> str:
        """Generate direct function call without _safe_call wrapper.

        Used for user-defined functions which are trusted. Generates simple
        function call syntax without security validation overhead.

        Args:
            node: FunctionCall AST node

        Returns:
            Generated code: func(arg1, arg2, ...)

        Example:
            ML: myFunc(1, 2, 3)
            Python: myFunc(1, 2, 3)
        """
        # node.function is a string for user-defined functions
        if isinstance(node.function, str):
            func_name = node.function
        else:
            # Fallback (shouldn't happen for user functions, but be safe)
            func_name = str(node.function)

        safe_name = self._safe_identifier(func_name)

        args = [self._generate_expression(arg) for arg in node.arguments]
        args_str = ', '.join(args)

        return f"{safe_name}({args_str})"

    def _generate_wrapped_call(self, node: "FunctionCall") -> str:
        """Generate function call wrapped with _safe_call.

        Handles all non-user-defined function calls with security validation:
        - ML builtins: Routed through builtin module
        - Module functions: Wrapped with _safe_call
        - Method calls: Wrapped with _safe_method_call
        - Dynamic calls: Wrapped with _safe_call

        Args:
            node: FunctionCall AST node

        Returns:
            Generated code: _safe_call(func, args...) or _safe_method_call(obj, 'method', args...)

        Examples:
            ML: len([1, 2, 3])
            Python: _safe_call(builtin.len, [1, 2, 3])

            ML: math.sqrt(16)
            Python: _safe_call(math.sqrt, 16)

            ML: text.upper()
            Python: _safe_method_call(text, 'upper')

            ML: someVar(42)
            Python: _safe_call(someVar, 42)
        """
        from mlpy.ml.grammar.ast_nodes import MemberAccess, Identifier

        # Special handling for MemberAccess: distinguish module vs method calls
        if isinstance(node.function, MemberAccess):
            # Check if this is a module function call (e.g., builtin.len) or method call (e.g., text.upper)
            is_module_call = False
            if isinstance(node.function.object, Identifier):
                # Check if the object is an imported module (including 'builtin')
                obj_name = node.function.object.name
                if obj_name in self.context.imported_modules or obj_name == "builtin":
                    is_module_call = True

            if is_module_call:
                # Module function call: builtin.len(), collections.append(), etc.
                # Generate as: _safe_call(module.func, args...)
                func_code = self._generate_expression(node.function)
                args = [self._generate_expression(arg) for arg in node.arguments]
                all_args = [func_code] + args
                args_str = ', '.join(all_args)
                return f"_safe_call({args_str})"
            else:
                # Method call on an object: text.upper(), arr.append(), etc.
                # Generate as: _safe_method_call(obj, 'method', args...)
                obj_code = self._generate_expression(node.function.object)
                member_name = node.function.member if isinstance(node.function.member, str) else str(node.function.member)
                args = [self._generate_expression(arg) for arg in node.arguments]

                # Ensure runtime helpers are imported
                self._ensure_runtime_helpers_imported()

                # Combine as _safe_method_call
                args_str = ', '.join([obj_code, repr(member_name)] + args)
                return f"_safe_method_call({args_str})"

        # For non-MemberAccess: use _safe_call wrapper
        if isinstance(node.function, str):
            func_name = node.function

            # Check if this is a known ML builtin function name
            if self.function_registry.is_allowed_builtin(func_name):
                # Route to builtin module: sum(...) → builtin.sum(...)
                self.context.builtin_functions_used.add(func_name)
                func_code = f"builtin.{func_name}"
            else:
                # Variable or unknown function
                func_code = self._safe_identifier(func_name)
        else:
            # Fallback for any other type
            func_code = self._generate_expression(node.function)

        # Generate arguments
        args = [self._generate_expression(arg) for arg in node.arguments]

        # Combine function and arguments for _safe_call
        all_args = [func_code] + args
        args_str = ', '.join(all_args)

        return f"_safe_call({args_str})"

    # ============================================================================
    # Whitelist Enforcement Methods (Legacy - kept for compatibility)
    # ============================================================================

    def _generate_simple_function_call(self, func_name: str, arguments: list) -> str:
        """Generate simple function call with whitelist enforcement.

        Legacy method kept for compatibility. Routes function calls based on
        whitelist category.

        Args:
            func_name: Function name (e.g., "len", "print", "myFunc")
            arguments: List of argument expressions

        Returns:
            Generated Python code for function call

        Raises:
            CodeGenError: If function is not in whitelist

        Categories:
            1. ML Builtin Functions: Routed to builtin module
            2. User-Defined Functions: Direct call
            3. Unknown Functions: Blocked with error
        """
        args = [self._generate_expression(arg) for arg in arguments]
        args_str = ', '.join(args)

        # Category 1: ML Builtin Functions -> route to builtin module
        if self.function_registry.is_allowed_builtin(func_name):
            self.context.builtin_functions_used.add(func_name)
            return f"builtin.{func_name}({args_str})"

        # Category 2: User-Defined Functions -> direct call
        elif self.function_registry.is_user_defined(func_name):
            safe_name = self._safe_identifier(func_name)
            return f"{safe_name}({args_str})"

        # Category 3: BLOCKED - Unknown function (not in whitelist)
        else:
            self._raise_unknown_function_error(func_name, arguments)

    def _generate_member_function_call(self, member_access: "MemberAccess", arguments: list) -> str:
        """Generate member function call with whitelist enforcement.

        Legacy method kept for compatibility. Handles both module function calls
        and object method calls.

        Args:
            member_access: MemberAccess node (e.g., math.sqrt)
            arguments: List of argument expressions

        Returns:
            Generated Python code for member function call

        Handles:
            - Imported module functions: math.sqrt() -> math.sqrt()
            - Object methods: obj.method() -> obj.method()

        Raises:
            CodeGenError: If module function is not in whitelist
        """
        from mlpy.ml.grammar.ast_nodes import Identifier

        args = [self._generate_expression(arg) for arg in arguments]
        args_str = ', '.join(args)

        # Check if this is an imported module function call
        if isinstance(member_access.object, Identifier):
            module_name = member_access.object.name
            func_name = member_access.member if isinstance(member_access.member, str) else str(member_access.member)

            # Check if this is an imported module
            if self.function_registry.is_imported_module(module_name):
                # Verify function exists in module
                if self.function_registry.is_imported_function(module_name, func_name):
                    # Generate module.function() call
                    safe_module = self._safe_identifier(module_name)
                    return f"{safe_module}.{func_name}({args_str})"
                else:
                    # Function not in module - block it
                    self._raise_unknown_module_function_error(module_name, func_name, arguments)

        # Not a module call - treat as object method call
        # Use existing member access generation logic
        obj_code = self._generate_expression(member_access.object)
        if isinstance(member_access.member, str):
            member_code = member_access.member
        else:
            member_code = self._generate_expression(member_access.member)

        return f"{obj_code}.{member_code}({args_str})"

    # ============================================================================
    # Error Handling Methods
    # ============================================================================

    def _raise_unknown_function_error(self, func_name: str, arguments: list) -> None:
        """Raise MLTranspilationError for unknown function call.

        Provides helpful error message with suggestions for similar function names.

        Args:
            func_name: Unknown function name
            arguments: Function arguments

        Raises:
            MLTranspilationError: Always raised with detailed error message

        Error Message Includes:
            - Function name and whitelist status
            - Allowed function categories explanation
            - Similar function name suggestions
            - Registry status information
        """
        from mlpy.ml.errors.exceptions import MLTranspilationError

        # Build helpful error message
        message = f"Unknown function '{func_name}()' - not in whitelist.\n\n"
        message += "Allowed function categories:\n"
        message += "  1. ML builtin functions (from stdlib.builtin module)\n"
        message += "  2. User-defined functions (defined in current ML program)\n"
        message += "  3. Imported module functions (from stdlib modules)\n\n"

        # Suggest similar function names
        all_allowed = self.function_registry.get_all_allowed_functions()
        similar = [f for f in all_allowed if func_name.lower() in f.lower() or f.lower() in func_name.lower()]

        if similar:
            message += f"Did you mean one of these?\n"
            for suggestion in sorted(similar)[:5]:
                category = self.function_registry.get_call_category(suggestion)
                message += f"  - {suggestion}() [{category}]\n"

        message += f"\nRegistry status: {self.function_registry}"

        raise MLTranspilationError(message)

    def _raise_unknown_module_function_error(self, module_name: str, func_name: str, arguments: list) -> None:
        """Raise MLTranspilationError for unknown module function.

        Provides helpful error message listing available functions in the module.

        Args:
            module_name: Module name
            func_name: Unknown function name
            arguments: Function arguments

        Raises:
            MLTranspilationError: Always raised with detailed error message

        Error Message Includes:
            - Module and function name
            - List of available functions in module (up to 10)
            - Total count if more than 10 functions available
        """
        from mlpy.ml.errors.exceptions import MLTranspilationError

        message = f"Unknown function '{module_name}.{func_name}()' - not found in module.\n\n"

        # Get module metadata
        metadata = self.function_registry.imported_modules.get(module_name)
        if metadata:
            available_functions = sorted(metadata.functions.keys())
            message += f"Available functions in '{module_name}' module:\n"
            for available_func in available_functions[:10]:
                message += f"  - {module_name}.{available_func}()\n"
            if len(available_functions) > 10:
                message += f"  ... and {len(available_functions) - 10} more\n"

        raise MLTranspilationError(message)
