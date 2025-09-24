"""Security analyzer for detecting dangerous operations in ML code."""

import re
from dataclasses import dataclass
from typing import Any

from mlpy.ml.errors.context import ErrorContext, create_error_context
from mlpy.ml.errors.exceptions import (
    CWECategory,
    MLSecurityError,
    create_code_injection_error,
    create_reflection_abuse_error,
    create_unsafe_import_error,
)
from mlpy.ml.grammar.ast_nodes import *
from mlpy.runtime.profiling.decorators import profile_security


@dataclass
class SecurityIssue:
    """Represents a security issue found during analysis."""

    severity: str  # "critical", "high", "medium", "low"
    category: str  # Type of security issue
    message: str
    line: int | None = None
    column: int | None = None
    node: ASTNode | None = None
    context: dict[str, Any] | None = None


class SecurityAnalyzer(ASTVisitor):
    """Security analyzer that traverses AST nodes to detect security issues."""

    def __init__(self, source_file: str | None = None) -> None:
        """Initialize security analyzer.

        Args:
            source_file: Source file path for error reporting
        """
        self.source_file = source_file
        self.issues: list[SecurityIssue] = []
        self.current_scope_imports: set[str] = set()
        self.dangerous_functions = {
            "eval",
            "exec",
            "compile",
            "__import__",
            "getattr",
            "setattr",
            "delattr",
            "hasattr",
            "globals",
            "locals",
            "vars",
            "dir",
            "open",
            "file",
            "input",
            "raw_input",
        }
        self.dangerous_modules = {
            "os",
            "sys",
            "subprocess",
            "shutil",
            "pickle",
            "marshal",
            "imp",
            "importlib",
            "types",
            "inspect",
            "gc",
            "ctypes",
            "__builtin__",
            "builtins",
        }
        self.reflection_patterns = {
            "__class__",
            "__bases__",
            "__subclasses__",
            "__mro__",
            "__globals__",
            "__dict__",
            "__code__",
            "__closure__",
            "__defaults__",
            "__kwdefaults__",
        }

    @profile_security
    def analyze(self, ast_node: Program) -> list[ErrorContext]:
        """Analyze AST for security issues.

        Args:
            ast_node: Root AST node to analyze

        Returns:
            List of ErrorContext objects for security issues found
        """
        self.issues.clear()
        self.current_scope_imports.clear()

        # Traverse the AST
        ast_node.accept(self)

        # Convert issues to ErrorContext objects
        error_contexts = []
        for issue in self.issues:
            error = self._create_security_error(issue)
            error_context = create_error_context(error, source_file=self.source_file)
            error_contexts.append(error_context)

        return error_contexts

    def _create_security_error(self, issue: SecurityIssue) -> MLSecurityError:
        """Create MLSecurityError from SecurityIssue."""
        if issue.category == "code_injection":
            return create_code_injection_error(
                issue.context.get("operation", "unknown"),
                source_file=self.source_file,
                line_number=issue.line,
                column=issue.column,
            )
        elif issue.category == "unsafe_import":
            return create_unsafe_import_error(
                issue.context.get("module", "unknown"),
                source_file=self.source_file,
                line_number=issue.line,
                column=issue.column,
            )
        elif issue.category == "reflection_abuse":
            return create_reflection_abuse_error(
                issue.context.get("operation", "unknown"),
                source_file=self.source_file,
                line_number=issue.line,
                column=issue.column,
            )
        else:
            # Generic security error
            return MLSecurityError(
                issue.message,
                cwe=CWECategory.IMPROPER_INPUT_VALIDATION,
                suggestions=[
                    "Review the security implications of this operation",
                    "Consider using safer alternatives",
                    "Ensure proper input validation and sanitization",
                ],
                context=issue.context or {},
                source_file=self.source_file,
                line_number=issue.line,
                column=issue.column,
            )

    def _add_issue(
        self,
        severity: str,
        category: str,
        message: str,
        node: ASTNode,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Add a security issue."""
        self.issues.append(
            SecurityIssue(
                severity=severity,
                category=category,
                message=message,
                line=node.line,
                column=node.column,
                node=node,
                context=context or {},
            )
        )

    # AST Visitor Methods
    def visit_program(self, node: Program):
        """Visit program node."""
        for item in node.items:
            if item:
                item.accept(self)

    def visit_capability_declaration(self, node: CapabilityDeclaration):
        """Visit capability declaration - Generally safe."""
        for item in node.items:
            if item:
                item.accept(self)

    def visit_resource_pattern(self, node: ResourcePattern):
        """Visit resource pattern - Check for overly broad patterns."""
        if node.pattern == "*" or node.pattern == "**":
            self._add_issue(
                "medium",
                "overly_broad_capability",
                f"Overly broad resource pattern '{node.pattern}' grants excessive access",
                node,
                {"pattern": node.pattern},
            )

    def visit_permission_grant(self, node: PermissionGrant):
        """Visit permission grant - Check for dangerous permissions."""
        dangerous_permissions = {"system", "execute"}
        if node.permission_type in dangerous_permissions:
            self._add_issue(
                "high",
                "dangerous_permission",
                f"Dangerous permission '{node.permission_type}' requires careful review",
                node,
                {"permission": node.permission_type, "target": node.target},
            )

    def visit_import_statement(self, node: ImportStatement):
        """Visit import statement - Check for dangerous modules."""
        module_path = ".".join(node.target)
        self.current_scope_imports.add(module_path)

        # Check for dangerous modules
        for dangerous_module in self.dangerous_modules:
            if module_path == dangerous_module or module_path.startswith(dangerous_module + "."):
                self._add_issue(
                    "high",
                    "unsafe_import",
                    f"Import of dangerous module '{module_path}' detected",
                    node,
                    {"module": module_path, "alias": node.alias},
                )

    def visit_function_definition(self, node: FunctionDefinition):
        """Visit function definition."""
        for param in node.parameters:
            if param:
                param.accept(self)

        for stmt in node.body:
            if stmt:
                stmt.accept(self)

    def visit_parameter(self, node: Parameter):
        """Visit parameter - Generally safe."""
        pass

    def visit_expression_statement(self, node: ExpressionStatement):
        """Visit expression statement."""
        if node.expression:
            node.expression.accept(self)

    def visit_assignment_statement(self, node: AssignmentStatement):
        """Visit assignment statement."""
        if node.value:
            node.value.accept(self)

    def visit_return_statement(self, node: ReturnStatement):
        """Visit return statement."""
        if node.value:
            node.value.accept(self)

    def visit_block_statement(self, node: BlockStatement):
        """Visit block statement."""
        for stmt in node.statements:
            if stmt:
                stmt.accept(self)

    def visit_if_statement(self, node: IfStatement):
        """Visit if statement."""
        if node.condition:
            node.condition.accept(self)
        if node.then_statement:
            node.then_statement.accept(self)
        if node.else_statement:
            node.else_statement.accept(self)

    def visit_while_statement(self, node: WhileStatement):
        """Visit while statement."""
        if node.condition:
            node.condition.accept(self)
        if node.body:
            node.body.accept(self)

    def visit_for_statement(self, node: ForStatement):
        """Visit for statement."""
        if node.iterable:
            node.iterable.accept(self)
        if node.body:
            node.body.accept(self)

    def visit_try_statement(self, node: TryStatement):
        """Visit try statement."""
        # Visit try body
        for stmt in node.try_body:
            if stmt:
                stmt.accept(self)

        # Visit except clauses
        for except_clause in node.except_clauses:
            if except_clause:
                except_clause.accept(self)

        # Visit finally body
        if node.finally_body:
            for stmt in node.finally_body:
                if stmt:
                    stmt.accept(self)

    def visit_except_clause(self, node: ExceptClause):
        """Visit except clause."""
        # Visit body statements
        for stmt in node.body:
            if stmt:
                stmt.accept(self)

    def visit_break_statement(self, node: BreakStatement):
        """Visit break statement - no security concerns."""
        pass

    def visit_continue_statement(self, node: ContinueStatement):
        """Visit continue statement - no security concerns."""
        pass

    def visit_binary_expression(self, node: BinaryExpression):
        """Visit binary expression."""
        if node.left:
            node.left.accept(self)
        if node.right:
            node.right.accept(self)

    def visit_unary_expression(self, node: UnaryExpression):
        """Visit unary expression."""
        if node.operand:
            node.operand.accept(self)

    def visit_identifier(self, node: Identifier):
        """Visit identifier - Check for dangerous variable names."""
        if node.name in self.dangerous_functions:
            self._add_issue(
                "high",
                "dangerous_identifier",
                f"Reference to dangerous function '{node.name}'",
                node,
                {"identifier": node.name},
            )

    def visit_function_call(self, node: FunctionCall):
        """Visit function call - CRITICAL SECURITY CHECK."""
        # Check for dangerous function calls
        if node.function in self.dangerous_functions:
            self._add_issue(
                "critical",
                "code_injection",
                f"Dangerous function call '{node.function}' detected",
                node,
                {"operation": node.function, "arguments": len(node.arguments)},
            )

        # Check arguments
        for arg in node.arguments:
            if arg:
                arg.accept(self)

    def visit_array_access(self, node: ArrayAccess):
        """Visit array access."""
        if node.array:
            node.array.accept(self)
        if node.index:
            node.index.accept(self)

    def visit_member_access(self, node: MemberAccess):
        """Visit member access - Check for reflection abuse."""
        if node.member in self.reflection_patterns:
            self._add_issue(
                "high",
                "reflection_abuse",
                f"Dangerous reflection operation '{node.member}' detected",
                node,
                {"operation": node.member},
            )

        if node.object:
            node.object.accept(self)

    def visit_literal(self, node: Literal):
        """Visit literal - Generally safe."""
        pass

    def visit_number_literal(self, node: NumberLiteral):
        """Visit number literal - Safe."""
        pass

    def visit_string_literal(self, node: StringLiteral):
        """Visit string literal - Check for dangerous content."""
        if isinstance(node.value, str):
            # Check for potential code injection patterns
            dangerous_patterns = [
                r"eval\s*\(",
                r"exec\s*\(",
                r"__import__\s*\(",
                r"open\s*\(",
                r"os\.system\s*\(",
                r"subprocess\.",
            ]

            for pattern in dangerous_patterns:
                if re.search(pattern, node.value, re.IGNORECASE):
                    self._add_issue(
                        "medium",
                        "suspicious_string",
                        "String contains potentially dangerous code pattern",
                        node,
                        {"pattern": pattern, "content": node.value[:100]},
                    )

    def visit_boolean_literal(self, node: BooleanLiteral):
        """Visit boolean literal - Safe."""
        pass

    def visit_array_literal(self, node: ArrayLiteral):
        """Visit array literal."""
        for element in node.elements:
            if element:
                element.accept(self)

    def visit_object_literal(self, node: ObjectLiteral):
        """Visit object literal."""
        for value in node.properties.values():
            if value:
                value.accept(self)


# Convenience functions
def analyze_security(ast_node: Program, source_file: str | None = None) -> list[ErrorContext]:
    """Analyze AST for security issues.

    Args:
        ast_node: Root AST node to analyze
        source_file: Optional source file path for error reporting

    Returns:
        List of ErrorContext objects for security issues found
    """
    analyzer = SecurityAnalyzer(source_file)
    return analyzer.analyze(ast_node)


def check_code_security(source_code: str, source_file: str | None = None) -> list[ErrorContext]:
    """Check ML source code for security issues.

    Args:
        source_code: ML source code to analyze
        source_file: Optional source file path for error reporting

    Returns:
        List of ErrorContext objects for security issues found
    """
    from mlpy.ml.grammar.parser import parse_ml_code

    try:
        ast_node = parse_ml_code(source_code, source_file)
        return analyze_security(ast_node, source_file)
    except Exception:
        # If parsing fails, we can't do security analysis
        return []
