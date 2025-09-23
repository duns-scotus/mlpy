"""Lark transformer to convert parse trees to AST nodes."""

from typing import List, Optional, Any, Dict
from lark import Transformer, Token
from .ast_nodes import *


class MLTransformer(Transformer):
    """Transform Lark parse trees into mlpy AST nodes."""

    def program(self, items):
        """Transform program node."""
        return Program(items=list(items))

    # Capability System
    def capability_declaration(self, items):
        """Transform capability declaration."""
        name = items[0].value if isinstance(items[0], Token) else str(items[0])
        capability_items = items[1:] if len(items) > 1 else []
        return CapabilityDeclaration(name=name, items=capability_items)

    def capability_name(self, items):
        """Transform capability name."""
        return items[0].value if items else ""

    def resource_pattern(self, items):
        """Transform resource pattern."""
        pattern = items[0].value.strip('"\'') if items else ""
        return ResourcePattern(pattern=pattern)

    def permission_grant(self, items):
        """Transform permission grant."""
        permission_type = items[0].value if items else ""
        target = items[1].value.strip('"\'') if len(items) > 1 else None
        return PermissionGrant(permission_type=permission_type, target=target)

    # Imports
    def import_statement(self, items):
        """Transform import statement."""
        target_parts = []
        alias = None

        i = 0
        while i < len(items):
            item = items[i]
            if isinstance(item, Token):
                if item.type == "IDENTIFIER":
                    if i > 0 and isinstance(items[i-1], Token) and items[i-1].value == "as":
                        alias = item.value
                    else:
                        target_parts.append(item.value)
            i += 1

        return ImportStatement(target=target_parts, alias=alias)

    def import_target(self, items):
        """Transform import target."""
        return [item.value for item in items if isinstance(item, Token)]

    # Functions
    def function_definition(self, items):
        """Transform function definition."""
        name = items[0].value if isinstance(items[0], Token) else str(items[0])

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

        return FunctionDefinition(name=name, parameters=parameters, body=body)

    def parameter_list(self, items):
        """Transform parameter list."""
        return list(items)

    def parameter(self, items):
        """Transform parameter."""
        name = items[0].value if isinstance(items[0], Token) else str(items[0])
        type_annotation = items[1] if len(items) > 1 else None
        return Parameter(name=name, type_annotation=type_annotation)

    def type_annotation(self, items):
        """Transform type annotation."""
        return items[0].value if items and isinstance(items[0], Token) else None

    # Statements
    def expression_statement(self, items):
        """Transform expression statement."""
        return ExpressionStatement(expression=items[0])

    def assignment_statement(self, items):
        """Transform assignment statement."""
        target = items[0].value if isinstance(items[0], Token) else str(items[0])
        value = items[1]
        return AssignmentStatement(target=target, value=value)

    def return_statement(self, items):
        """Transform return statement."""
        value = items[0] if items else None
        return ReturnStatement(value=value)

    def block_statement(self, items):
        """Transform block statement."""
        return BlockStatement(statements=list(items))

    def if_statement(self, items):
        """Transform if statement."""
        condition = items[0]
        then_statements = [item for item in items[1:-1] if not isinstance(item, str)]
        else_statements = []

        # Find else clause if present
        else_start = -1
        for i, item in enumerate(items):
            if isinstance(item, str) and item == "else":
                else_start = i + 1
                break

        if else_start > 0:
            then_statements = [item for item in items[1:else_start-1] if not isinstance(item, str)]
            else_statements = [item for item in items[else_start:] if not isinstance(item, str)]

        then_block = BlockStatement(then_statements) if then_statements else None
        else_block = BlockStatement(else_statements) if else_statements else None

        return IfStatement(
            condition=condition,
            then_statement=then_block,
            else_statement=else_block
        )

    def while_statement(self, items):
        """Transform while statement."""
        condition = items[0]
        body_statements = [item for item in items[1:] if not isinstance(item, str)]
        body = BlockStatement(body_statements) if body_statements else None
        return WhileStatement(condition=condition, body=body)

    def for_statement(self, items):
        """Transform for statement."""
        variable = items[0].value if isinstance(items[0], Token) else str(items[0])
        iterable = items[1]
        body_statements = [item for item in items[2:] if not isinstance(item, str)]
        body = BlockStatement(body_statements) if body_statements else None
        return ForStatement(variable=variable, iterable=iterable, body=body)

    # Expressions
    def logical_or(self, items):
        """Transform logical OR expression."""
        if len(items) == 1:
            return items[0]
        return BinaryExpression(left=items[0], operator="||", right=items[1])

    def logical_and(self, items):
        """Transform logical AND expression."""
        if len(items) == 1:
            return items[0]
        return BinaryExpression(left=items[0], operator="&&", right=items[1])

    def equality(self, items):
        """Transform equality expression."""
        if len(items) == 1:
            return items[0]
        return BinaryExpression(left=items[0], operator=items[1], right=items[2])

    def comparison(self, items):
        """Transform comparison expression."""
        if len(items) == 1:
            return items[0]
        return BinaryExpression(left=items[0], operator=items[1], right=items[2])

    def addition(self, items):
        """Transform addition expression."""
        if len(items) == 1:
            return items[0]
        return BinaryExpression(left=items[0], operator=items[1], right=items[2])

    def multiplication(self, items):
        """Transform multiplication expression."""
        if len(items) == 1:
            return items[0]
        return BinaryExpression(left=items[0], operator=items[1], right=items[2])

    def unary(self, items):
        """Transform unary expression."""
        if len(items) == 1:
            return items[0]
        return UnaryExpression(operator=items[0], operand=items[1])

    def function_call(self, items):
        """Transform function call - Security Critical."""
        function_name = items[0].value if isinstance(items[0], Token) else str(items[0])
        arguments = items[1:] if len(items) > 1 else []
        return FunctionCall(function=function_name, arguments=arguments)

    def argument_list(self, items):
        """Transform argument list."""
        return list(items)

    def array_access(self, items):
        """Transform array access."""
        array = items[0]
        index = items[1]
        return ArrayAccess(array=array, index=index)

    def member_access(self, items):
        """Transform member access - Security Critical."""
        obj = items[0]
        member = items[1].value if isinstance(items[1], Token) else str(items[1])
        return MemberAccess(object=obj, member=member)

    # Literals
    def array_literal(self, items):
        """Transform array literal."""
        return ArrayLiteral(elements=list(items))

    def object_literal(self, items):
        """Transform object literal."""
        properties = {}
        for i in range(0, len(items), 2):
            if i + 1 < len(items):
                key = items[i]
                value = items[i + 1]

                # Extract key name
                if isinstance(key, Token):
                    key_name = key.value.strip('"\'')
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
        """Transform number token."""
        value = float(token.value) if '.' in token.value else int(token.value)
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
    def _handle_binary_op(self, items, operator):
        """Helper to handle binary operations."""
        if len(items) == 1:
            return items[0]

        left = items[0]
        for i in range(1, len(items), 2):
            if i + 1 < len(items):
                op = items[i] if isinstance(items[i], str) else operator
                right = items[i + 1]
                left = BinaryExpression(left=left, operator=op, right=right)

        return left