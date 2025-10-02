"""Lark transformer to convert parse trees to AST nodes."""

from lark import Token, Transformer

from .ast_nodes import *


class MLTransformer(Transformer):
    """Transform Lark parse trees into mlpy AST nodes."""

    def program(self, items):
        """Transform program node."""
        return Program(items=list(items))

    # Capability System
    def capability_declaration(self, items):
        """Transform capability declaration."""
        # Extract name from Token, Identifier, or other types
        if isinstance(items[0], Token):
            name = items[0].value
        elif hasattr(items[0], "name"):
            name = items[0].name
        else:
            name = str(items[0])

        # Filter out non-AST items (skip Trees and other Lark objects)
        capability_items = []
        for item in items[1:]:
            if hasattr(item, "accept"):  # Only include proper AST nodes
                capability_items.append(item)

        return CapabilityDeclaration(name=name, items=capability_items)

    def capability_item(self, items):
        """Transform capability item (resource_pattern or permission_grant)."""
        # Return the first (and should be only) item
        return items[0] if items else None

    def capability_name(self, items):
        """Transform capability name."""
        if not items:
            return ""
        if hasattr(items[0], "value"):
            return items[0].value
        elif hasattr(items[0], "name"):
            return items[0].name
        else:
            return str(items[0])

    def resource_pattern(self, items):
        """Transform resource pattern."""
        if items:
            if hasattr(items[0], "value"):
                pattern = items[0].value.strip("\"'")
            else:
                pattern = str(items[0]).strip("\"'")
        else:
            pattern = ""
        return ResourcePattern(pattern=pattern)

    def permission_type(self, items):
        """Transform permission type."""
        if items and hasattr(items[0], "value"):
            return items[0].value
        elif items:
            return str(items[0])
        return ""

    def permission_grant(self, items):
        """Transform permission grant."""
        permission_type = ""
        if items:
            if isinstance(items[0], str):
                permission_type = items[0]
            elif hasattr(items[0], "value"):
                permission_type = items[0].value
            else:
                permission_type = str(items[0])

        target = None
        if len(items) > 1:
            if hasattr(items[1], "value"):
                target = items[1].value.strip("\"'")
            elif hasattr(items[1], "children") and items[1].children:
                # Handle Tree object with StringLiteral child
                child = items[1].children[0]
                if hasattr(child, "value"):
                    target = child.value
                else:
                    target = str(child).strip("\"'")
            else:
                target = str(items[1]).strip("\"'")

        return PermissionGrant(permission_type=permission_type, target=target)

    # Imports
    def import_statement(self, items):
        """Transform import statement."""
        # The first item should be the import_target list
        target_parts = []
        alias = None

        for item in items:
            if isinstance(item, list):
                # This is the import_target result
                target_parts = item
            elif hasattr(item, "name"):
                # This could be an alias identifier
                alias = item.name
            elif isinstance(item, Token) and item.value not in ["import", "as"]:
                # Direct identifier token
                if alias is None:  # No alias set yet, this is part of target
                    target_parts.append(item.value)
                else:  # Alias already exists, this shouldn't happen
                    pass

        return ImportStatement(target=target_parts, alias=alias)

    def import_target(self, items):
        """Transform import target."""
        target_parts = []
        for item in items:
            if isinstance(item, Token):
                target_parts.append(item.value)
            elif hasattr(item, "name"):
                target_parts.append(item.name)
        return target_parts

    # Functions
    def function_definition(self, items):
        """Transform function definition."""
        name = items[0]

        # Find parameters and body
        parameters = []
        body = []

        for item in items[1:]:
            if isinstance(item, list):
                if all(isinstance(x, Parameter) for x in item):
                    parameters = item
                else:
                    body.extend(item)
            elif isinstance(item, Parameter):
                parameters.append(item)
            elif isinstance(item, Statement):
                body.append(item)
            elif isinstance(item, FunctionDefinition):
                body.append(item)

        return FunctionDefinition(name=name, parameters=parameters, body=body)

    # DEPRECATED: function_expression removed from grammar
    # Use arrow functions instead: fn(x) => expression
    # def function_expression(self, items):
    #     """Transform function expression (anonymous function) - DEPRECATED."""
    #     # This was removed because multi-statement function expressions
    #     # cannot be correctly transpiled to Python lambdas
    #     pass

    def parameter_list(self, items):
        """Transform parameter list."""
        return list(items)

    def parameter(self, items):
        """Transform parameter."""
        # Extract name from Identifier or Token
        if hasattr(items[0], "name"):
            name = items[0].name
        elif hasattr(items[0], "value"):
            name = items[0].value
        else:
            name = str(items[0])

        type_annotation = items[1] if len(items) > 1 else None
        return Parameter(name=name, type_annotation=type_annotation)

    def type_annotation(self, items):
        """Transform type annotation."""
        if not items:
            return None
        if isinstance(items[0], Token):
            return items[0].value
        elif hasattr(items[0], "name"):
            return items[0].name
        else:
            return str(items[0])

    # Statements
    def expression_statement(self, items):
        """Transform expression statement."""
        return ExpressionStatement(expression=items[0])

    def assignment_target(self, items):
        """Transform assignment target (LHS of assignment)."""
        return items[0]  # Return the target expression (Identifier, ArrayAccess, or MemberAccess)

    def assignment_statement(self, items):
        """Transform assignment statement."""
        target = items[0]  # This is now the result from assignment_target
        value = items[1]  # This is from assignment_expression
        return AssignmentStatement(target=target, value=value)

    def assignment_expression(self, items):
        """Transform assignment expression."""
        return items[0]  # Return the arrow function or regular expression

    def destructuring_statement(self, items):
        """Transform destructuring statement."""
        pattern = items[0]  # Destructuring pattern (array or object)
        value = items[1]  # Expression being destructured
        return DestructuringAssignment(pattern=pattern, value=value)

    def destructuring_pattern(self, items):
        """Transform destructuring pattern."""
        return items[0]  # Return the array or object destructuring pattern

    def array_destructuring(self, items):
        """Transform array destructuring pattern."""
        # Extract names from Identifier AST nodes
        element_names = []
        for item in items:
            if hasattr(item, "name"):
                element_names.append(item.name)
            elif hasattr(item, "value"):
                element_names.append(item.value)
            else:
                element_names.append(str(item))
        return ArrayDestructuring(elements=element_names)

    def object_destructuring(self, items):
        """Transform object destructuring pattern."""
        # Extract names from Identifier AST nodes - for simple cases, map name to name
        property_dict = {}
        for item in items:
            if hasattr(item, "name"):
                name = item.name
                property_dict[name] = name  # {key: variable_name}
            elif hasattr(item, "value"):
                name = item.value
                property_dict[name] = name
            else:
                name = str(item)
                property_dict[name] = name
        return ObjectDestructuring(properties=property_dict)

    def arrow_function(self, items):
        """Transform arrow function with FN keyword.

        Grammar: FN "(" parameter_list? ")" "=>" arrow_body
        """
        # Filter out FN token and other terminals
        # Keep only parameter_list and arrow_body (the non-terminals)
        non_terminals = [item for item in items if not isinstance(item, Token)]

        # Last non-terminal is the body
        body = non_terminals[-1] if non_terminals else None

        # First non-terminal (if exists and not the body) is parameters
        if len(non_terminals) > 1:
            params = non_terminals[0]
            if params and not isinstance(params, list):
                params = [params]
            elif not params:
                params = []
        else:
            params = []

        return ArrowFunction(parameters=params, body=body)

    def arrow_body(self, items):
        """Transform arrow body."""
        return items[0]  # Just return the expression

    def return_statement(self, items):
        """Transform return statement."""
        value = items[0] if items else None
        return ReturnStatement(value=value)

    def block_statement(self, items):
        """Transform block statement."""
        return BlockStatement(statements=list(items))

    def statement_block(self, items):
        """Transform statement block - handles {statement*} constructs."""
        # Filter out None items and return as BlockStatement
        statements = [item for item in items if item is not None]
        return BlockStatement(statements)

    def elif_clause(self, items):
        """Transform elif clause."""
        condition = items[0]
        statement = items[1]  # Already a BlockStatement from statement_block
        return ElifClause(condition=condition, statement=statement)

    def if_statement(self, items):
        """Transform if statement with elif clauses support."""
        condition = items[0]
        then_block = items[1]  # Always present

        # Separate elif clauses from else clause
        elif_clauses = []
        else_block = None

        # Process remaining items to identify elif clauses and else clause
        i = 2
        while i < len(items):
            item = items[i]
            if hasattr(item, "__class__") and item.__class__.__name__ == "ElifClause":
                elif_clauses.append(item)
            else:
                # This must be the else block (last item)
                else_block = item
                break
            i += 1

        return IfStatement(
            condition=condition,
            then_statement=then_block,
            elif_clauses=elif_clauses,
            else_statement=else_block,
        )

    def while_statement(self, items):
        """Transform while statement."""
        condition = items[0]
        body_statements = [item for item in items[1:] if not isinstance(item, str)]
        body = BlockStatement(body_statements) if body_statements else None
        return WhileStatement(condition=condition, body=body)

    def for_statement(self, items):
        """Transform for statement."""
        # Extract variable name and create Identifier object
        if isinstance(items[0], Token):
            variable_name = items[0].value
        elif hasattr(items[0], "name"):
            # Already an Identifier object
            variable_name = items[0].name
        else:
            variable_name = str(items[0])

        variable = Identifier(name=variable_name)
        iterable = items[1]
        body_statements = [item for item in items[2:] if not isinstance(item, str)]
        body = BlockStatement(body_statements) if body_statements else None
        return ForStatement(variable=variable, iterable=iterable, body=body)

    def try_statement(self, items):
        """Transform try statement."""
        # For now, simplified approach - just collect statements and except clauses
        try_body = []
        except_clauses = []
        finally_body = []

        collecting_try = True
        collecting_finally = False

        for item in items:
            if isinstance(item, ExceptClause):
                except_clauses.append(item)
                collecting_try = False
            elif collecting_try and not isinstance(item, (str, type(None))):
                try_body.append(item)

        return TryStatement(
            try_body=try_body,
            except_clauses=except_clauses,
            finally_body=finally_body if finally_body else None,
        )

    def except_clause(self, items):
        """Transform except clause."""
        exception_variable = None
        body = []

        # Debug: Enable to see what items are being parsed
        # print(f"DEBUG except_clause items: {[(type(item).__name__, str(item)) for item in items]}")

        for item in items:
            if isinstance(item, Token):
                # Handle both direct IDENTIFIER and tokens within parentheses
                if item.type == "IDENTIFIER":
                    exception_variable = item.value
            elif isinstance(item, Identifier):
                # Handle Identifier AST nodes (for parenthesized exception variables)
                exception_variable = item.name
            elif not isinstance(item, str):
                body.append(item)

        return ExceptClause(exception_variable=exception_variable, body=body)

    def finally_clause(self, items):
        """Transform finally clause - handled in try_statement."""
        return items  # Return statements for try_statement to process

    def break_statement(self, items):
        """Transform break statement."""
        return BreakStatement()

    def continue_statement(self, items):
        """Transform continue statement."""
        return ContinueStatement()

    def throw_statement(self, items):
        """Transform throw statement."""
        if not items or len(items) != 1:
            raise ValueError(
                f"Throw statement requires exactly 1 dictionary argument, got {len(items)}"
            )
        error_data = items[0]
        if not isinstance(error_data, ObjectLiteral):
            raise ValueError(f"Throw statement requires an object literal, got {type(error_data)}")
        return ThrowStatement(error_data=error_data)

    # Expressions
    def ternary_op(self, items):
        """Transform ternary conditional expression."""
        # ternary_op has: condition, true_value, false_value
        if len(items) != 3:
            raise ValueError(f"Ternary operator requires exactly 3 items, got {len(items)}")
        condition, true_value, false_value = items
        return TernaryExpression(
            condition=condition, true_value=true_value, false_value=false_value
        )

    def logical_or(self, items):
        """Transform logical OR expression."""
        return items[0] if len(items) == 1 else items[0]

    def or_op(self, items):
        """Transform logical OR operation."""
        return BinaryExpression(left=items[0], operator="||", right=items[1])

    def logical_and(self, items):
        """Transform logical AND expression."""
        return items[0] if len(items) == 1 else items[0]

    def and_op(self, items):
        """Transform logical AND operation."""
        return BinaryExpression(left=items[0], operator="&&", right=items[1])

    def equality(self, items):
        """Transform equality expression."""
        return items[0] if len(items) == 1 else items[0]

    def eq_op(self, items):
        """Transform equality operation."""
        return BinaryExpression(left=items[0], operator="==", right=items[1])

    def ne_op(self, items):
        """Transform not-equal operation."""
        return BinaryExpression(left=items[0], operator="!=", right=items[1])

    def comparison(self, items):
        """Transform comparison expression."""
        return items[0] if len(items) == 1 else items[0]

    def lt_op(self, items):
        """Transform less-than operation."""
        return BinaryExpression(left=items[0], operator="<", right=items[1])

    def gt_op(self, items):
        """Transform greater-than operation."""
        return BinaryExpression(left=items[0], operator=">", right=items[1])

    def le_op(self, items):
        """Transform less-than-or-equal operation."""
        return BinaryExpression(left=items[0], operator="<=", right=items[1])

    def ge_op(self, items):
        """Transform greater-than-or-equal operation."""
        return BinaryExpression(left=items[0], operator=">=", right=items[1])

    def addition(self, items):
        """Transform addition expression."""
        return items[0] if len(items) == 1 else items[0]

    def add_op(self, items):
        """Transform addition operation."""
        return BinaryExpression(left=items[0], operator="+", right=items[1])

    def sub_op(self, items):
        """Transform subtraction operation."""
        return BinaryExpression(left=items[0], operator="-", right=items[1])

    def multiplication(self, items):
        """Transform multiplication expression."""
        return items[0] if len(items) == 1 else items[0]

    def mul_op(self, items):
        """Transform multiplication operation."""
        return BinaryExpression(left=items[0], operator="*", right=items[1])

    def div_op(self, items):
        """Transform division operation."""
        return BinaryExpression(left=items[0], operator="/", right=items[1])

    def mod_op(self, items):
        """Transform modulo operation."""
        return BinaryExpression(left=items[0], operator="%", right=items[1])

    def unary_not(self, items):
        """Transform logical NOT unary expression."""
        return UnaryExpression(operator="!", operand=items[0])

    def unary_neg(self, items):
        """Transform numeric negation unary expression."""
        return UnaryExpression(operator="-", operand=items[0])

    def function_call(self, items):
        """Transform function call - Security Critical."""
        # Handle both simple identifiers and member access function calls
        function_ref = items[0]

        # Check if it's a MemberAccess or simple identifier
        if isinstance(function_ref, MemberAccess):
            # Member function call like math.sqrt()
            function = function_ref
        elif hasattr(function_ref, "name"):
            # Simple identifier function call
            function = function_ref.name
        elif hasattr(function_ref, "value"):
            # Token function call
            function = function_ref.value
        else:
            # Fallback
            function = str(function_ref)

        arguments = []

        # Handle argument lists properly
        for item in items[1:]:
            if isinstance(item, list):
                arguments.extend(item)
            else:
                arguments.append(item)

        return FunctionCall(function=function, arguments=arguments)

    def argument_list(self, items):
        """Transform argument list."""
        return list(items)

    def array_access(self, items):
        """Transform array access (both indexing and slicing)."""
        array = items[0]
        index_or_slice = items[1]
        return ArrayAccess(array=array, index=index_or_slice)

    def slice_expression(self, items):
        """Transform slice expression.

        The items come from Lark's transformation of the grammar rules.
        Since slice_start, slice_end, and slice_step are all optional and transformed
        separately, we need to identify which item is which based on the meta information.
        """
        start = None
        end = None
        step = None

        # Items arrive in order, but only the ones that were present in the source
        # We need to check the metadata to know which is which
        for item in items:
            if hasattr(item, '_slice_position'):
                if item._slice_position == 'start':
                    start = item
                elif item._slice_position == 'end':
                    end = item
                elif item._slice_position == 'step':
                    step = item
            else:
                # Fallback: if no metadata, assume order is start, end, step
                if start is None:
                    start = item
                elif end is None:
                    end = item
                elif step is None:
                    step = item

        return SliceExpression(start=start, end=end, step=step)

    def slice_start(self, items):
        """Transform slice start."""
        result = items[0] if items else None
        if result is not None:
            result._slice_position = 'start'
        return result

    def slice_end(self, items):
        """Transform slice end."""
        result = items[0] if items else None
        if result is not None:
            result._slice_position = 'end'
        return result

    def slice_step(self, items):
        """Transform slice step."""
        result = items[0] if items else None
        if result is not None:
            result._slice_position = 'step'
        return result

    def member_access(self, items):
        """Transform member access - Security Critical."""
        obj = items[0]
        # Extract member name from Token, Identifier, or other types
        if isinstance(items[1], Token):
            member = items[1].value
        elif hasattr(items[1], "name"):
            member = items[1].name
        else:
            member = str(items[1])
        return MemberAccess(object=obj, member=member)

    # Literals
    def array_literal(self, items):
        """Transform array literal."""
        return ArrayLiteral(elements=list(items))

    def object_literal(self, items):
        """Transform object literal."""
        properties = {}
        for item in items:
            if isinstance(item, list) and len(item) == 2:
                key, value = item
                # Extract key name
                if isinstance(key, Token):
                    key_name = key.value.strip("\"'")
                elif hasattr(key, "value"):
                    key_name = key.value.strip("\"'")
                elif hasattr(key, "name"):
                    key_name = key.name  # For Identifier objects
                else:
                    key_name = str(key)
                properties[key_name] = value

        return ObjectLiteral(properties=properties)

    def object_property(self, items):
        """Transform object property."""
        return items  # Pass through, handled by object_literal

    # Identifiers and Tokens
    def IDENTIFIER(self, token):
        """Transform identifier token."""
        return Identifier(name=token.value)

    def NUMBER(self, token):
        """Transform number token with scientific notation support."""
        token_str = token.value

        # Check for scientific notation (contains 'e' or 'E')
        if "e" in token_str.lower():
            # Always use float for scientific notation
            value = float(token_str)
        elif "." in token_str:
            # Decimal number
            value = float(token_str)
        else:
            # Integer
            value = int(token_str)

        return NumberLiteral(value=value)

    def STRING(self, token):
        """Transform string token."""
        # Remove quotes
        value = token.value[1:-1]
        return StringLiteral(value=value)

    def BOOLEAN(self, token):
        """Transform boolean token."""
        value = token.value == "true"
        return BooleanLiteral(value=value)

    # Helper methods for handling operators
    def _handle_binary_op(self, items, default_operator):
        """Helper to handle binary operations."""
        if len(items) == 1:
            return items[0]

        left = items[0]
        for i in range(1, len(items), 2):
            if i + 1 < len(items):
                op = items[i] if isinstance(items[i], str) else default_operator
                right = items[i + 1]
                left = BinaryExpression(left=left, operator=op, right=right)

        return left
