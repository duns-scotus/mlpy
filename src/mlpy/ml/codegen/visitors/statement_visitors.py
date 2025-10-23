"""Statement visitor methods for code generation.

This mixin provides visitor methods for all ML statement types.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mlpy.ml.grammar.ast_nodes import (
        Program, CapabilityDeclaration, ResourcePattern, PermissionGrant,
        ImportStatement, FunctionDefinition, Parameter, ExpressionStatement,
        AssignmentStatement, ReturnStatement, BlockStatement, IfStatement,
        WhileStatement, ForStatement, TryStatement, ExceptClause,
        BreakStatement, ContinueStatement, NonlocalStatement, ThrowStatement
    )


class StatementVisitorsMixin:
    """Mixin providing statement visitor methods.

    This mixin contains visitor methods for:
    - Program and top-level structure
    - Function definitions
    - Control flow statements (if, while, for, try)
    - Assignment and expression statements
    - Import and capability statements
    """


    def visit_program(self, node: "Program"):
        """Generate code for program root."""
        for item in node.items:
            if item:
                item.accept(self)
                # Add spacing between top-level items
                if item != node.items[-1]:
                    self._emit_raw_line("")

    def visit_capability_declaration(self, node: "CapabilityDeclaration"):
        """Generate code for capability declaration."""
        # Add necessary imports for capability system
        self.context.imports_needed.add("contextlib")

        # Generate capability token creation
        capability_name = self._safe_identifier(node.name)

        self._emit_line(f"# Capability declaration: {node.name}", node)

        # Collect resource patterns and permissions from capability items
        resource_patterns = []
        permissions = set()

        for item in node.items:
            if hasattr(item, "pattern"):  # ResourcePattern
                resource_patterns.append(item.pattern.strip("\"'"))
            elif hasattr(item, "permission_type"):  # PermissionGrant
                permissions.add(item.permission_type)

        # Generate capability token creation function
        self._emit_line(f"def _create_{capability_name}_capability():")
        self._indent()
        self._emit_line(f'"""Create capability token for {node.name}."""')
        self._emit_line("from mlpy.runtime.capabilities import create_capability_token")
        self._emit_line("return create_capability_token(")
        self._indent()
        self._emit_line(f'capability_type="{node.name}",')
        if resource_patterns:
            patterns_str = ", ".join(f'"{p}"' for p in resource_patterns)
            self._emit_line(f"resource_patterns=[{patterns_str}],")
        if permissions:
            perms_str = ", ".join(f'"{p}"' for p in permissions)
            self._emit_line(f"allowed_operations={{{perms_str}}},")
        self._emit_line(f'description="Generated capability for {node.name}"')
        self._dedent()
        self._emit_line(")")
        self._dedent()
        self._emit_line("")

        # Generate context manager function
        self._emit_line("@contextlib.contextmanager")
        self._emit_line(f"def {capability_name}_context():")
        self._indent()
        self._emit_line(f'"""Capability context manager for {node.name}."""')
        self._emit_line("from mlpy.runtime.capabilities import get_capability_manager")
        self._emit_line("manager = get_capability_manager()")
        self._emit_line(f"token = _create_{capability_name}_capability()")
        self._emit_line(f'with manager.capability_context("{node.name}_context", [token]):')
        self._indent()
        self._emit_line("yield")
        self._dedent()
        self._dedent()
        self._emit_line("")

    def visit_resource_pattern(self, node: "ResourcePattern"):
        """Generate code for resource pattern."""
        self._emit_line(f"# Resource pattern: {node.pattern}", node)

    def visit_permission_grant(self, node: "PermissionGrant"):
        """Generate code for permission grant."""
        target_str = f" to {node.target}" if node.target else ""
        self._emit_line(f"# Grant {node.permission_type} permission{target_str}", node)

    def visit_import_statement(self, node: "ImportStatement"):
        """Generate code for import statement with ML source support."""
        module_path = ".".join(node.target)

        # Check registry for auto-discovered modules
        from mlpy.stdlib.module_registry import get_registry, ModuleType
        registry = get_registry()

        if registry.is_available(module_path):
            # Get module metadata to check type
            metadata = registry._discovered.get(module_path)

            if metadata and metadata.module_type == ModuleType.PYTHON_BRIDGE:
                # Python bridge module - import from mlpy.stdlib
                python_module_path = f"mlpy.stdlib"
                alias = node.alias if node.alias else None
                self.function_registry.register_import(module_path, alias)

                if node.alias:
                    alias_name = self._safe_identifier(node.alias)
                    self._emit_line(
                        f"from {python_module_path} import {module_path} as {alias_name}", node
                    )
                    self.context.imported_modules.add(alias_name)
                    self.symbol_table['imports'].add(alias_name)
                else:
                    self._emit_line(f"from {python_module_path} import {module_path}", node)
                    self.context.imported_modules.add(module_path)
                    self.symbol_table['imports'].add(module_path)

            elif metadata and metadata.module_type == ModuleType.ML_SOURCE:
                # ML source module - transpile and import
                module_info = self._get_ml_module_info(module_path, metadata)
                self._generate_user_module_import(module_info, node.alias, node)
            else:
                # Unknown module type
                self._emit_line(f"# WARNING: Unknown module type for '{module_path}'", node)

        else:
            # Not in registry - try filesystem resolution (legacy path)
            try:
                module_info = self._resolve_user_module(node.target)
                if module_info:
                    # User module found - transpile and import it
                    self._generate_user_module_import(module_info, node.alias, node)
                else:
                    # Unknown modules get a runtime import check with suggestions
                    available_modules = registry.get_all_module_names()
                    suggestions = self._find_similar_names(module_path, available_modules)

                    error_msg = f"# WARNING: Import '{module_path}' not found."
                    if suggestions:
                        error_msg += f" Did you mean: {', '.join(suggestions[:3])}?"

                    self._emit_line(error_msg, node)
                    self._emit_line(f"# import {module_path}", node)
            except Exception as e:
                # Module resolution failed
                self._emit_line(f"# ERROR: Failed to resolve module '{module_path}': {e}", node)
                self._emit_line(f"# import {module_path}", node)

    def _find_similar_names(self, target: str, available: set) -> list[str]:
        """Find similar module names using Levenshtein distance."""
        import difflib
        return difflib.get_close_matches(target, available, n=3, cutoff=0.6)

    def visit_function_definition(self, node: "FunctionDefinition"):
        """Generate code for function definition."""
        func_name = self._safe_identifier(
            node.name.name if hasattr(node.name, "name") else str(node.name)
        )

        # Register user-defined function in whitelist
        self.function_registry.register_user_function(func_name)

        # Track function in symbol table
        self.symbol_table['functions'].add(func_name)

        # Track function symbol in enhanced source map
        if self.generate_source_maps and self.context.enhanced_source_map_generator:
            self.context.enhanced_source_map_generator.track_symbol(
                name=func_name,
                node=node,
                symbol_type="function"
            )

        # Build parameter list and track parameters
        params = []
        param_names = set()
        for param in node.parameters:
            if hasattr(param, "name"):
                param_name = self._safe_identifier(param.name)
                param_names.add(param_name)
                if hasattr(param, "type_annotation") and param.type_annotation:
                    params.append(f"{param_name}: {param.type_annotation}")
                else:
                    params.append(param_name)
            else:
                # Fallback for malformed parameters
                params.append("param")

        # Push parameters onto stack for function scope
        self.symbol_table['parameters'].append(param_names)

        param_str = ", ".join(params)
        self._emit_line(f"def {func_name}({param_str}):", node)

        # Track function scope in enhanced source map
        if self.generate_source_maps and self.context.enhanced_source_map_generator:
            self.context.enhanced_source_map_generator.track_scope(
                scope_type="function",
                start_node=node,
                end_node=None  # Will be set when function body ends
            )

        self._indent()

        # Generate function body
        if node.body:
            for stmt in node.body:
                if stmt:
                    stmt.accept(self)
        else:
            self._emit_line("pass")

        self._dedent()

        # Pop parameters from stack when leaving function scope
        self.symbol_table['parameters'].pop()

    def visit_parameter(self, node: "Parameter"):
        """Visit parameter - handled by function definition."""
        pass

    def visit_expression_statement(self, node: "ExpressionStatement"):
        """Generate code for expression statement."""
        if node.expression:
            expr_code = self._generate_expression(node.expression)
            self._emit_line(expr_code, node)

    def visit_assignment_statement(self, node: "AssignmentStatement"):
        """Generate code for assignment statement."""
        # Handle different assignment target types
        var_name = None
        if isinstance(node.target, str):
            # Simple variable assignment (legacy support)
            target_code = self._safe_identifier(node.target)
            var_name = node.target
            # Track variable in symbol table
            self.symbol_table['variables'].add(node.target)
        elif hasattr(node.target, "name"):
            # Identifier node
            var_name = node.target.name
            target_code = self._safe_identifier(var_name)
            # Track variable in symbol table
            self.symbol_table['variables'].add(var_name)
        else:
            # ArrayAccess or MemberAccess - generate as assignment target (NOT expression)
            # Don't track these as new variables
            target_code = self._generate_assignment_target(node.target)

        # Track variable symbol in enhanced source map
        if var_name and self.generate_source_maps and self.context.enhanced_source_map_generator:
            self.context.enhanced_source_map_generator.track_symbol(
                name=var_name,
                node=node,
                symbol_type="variable"
            )

        value_code = self._generate_expression(node.value)
        self._emit_line(f"{target_code} = {value_code}", node)

    def visit_return_statement(self, node: "ReturnStatement"):
        """Generate code for return statement."""
        if node.value:
            value_code = self._generate_expression(node.value)
            self._emit_line(f"return {value_code}", node)
        else:
            self._emit_line("return", node)

    def visit_block_statement(self, node: "BlockStatement"):
        """Generate code for block statement."""
        # If block is empty, emit pass to avoid IndentationError
        if not node.statements:
            self._emit_line("pass")
        else:
            for stmt in node.statements:
                if stmt:
                    stmt.accept(self)

    def visit_if_statement(self, node: "IfStatement"):
        """Generate code for if statement."""
        condition_code = self._generate_expression(node.condition)
        self._emit_line(f"if {condition_code}:", node)

        self._indent()
        if node.then_statement:
            node.then_statement.accept(self)
        else:
            self._emit_line("pass")
        self._dedent()

        # Generate elif clauses
        if hasattr(node, "elif_clauses") and node.elif_clauses:
            for elif_clause in node.elif_clauses:
                elif_clause.accept(self)

        if node.else_statement:
            self._emit_line("else:")
            self._indent()
            node.else_statement.accept(self)
            self._dedent()

    def visit_elif_clause(self, node):
        """Generate code for elif clause."""
        condition_code = self._generate_expression(node.condition)
        self._emit_line(f"elif {condition_code}:", node)

        self._indent()
        if node.statement:
            node.statement.accept(self)
        else:
            self._emit_line("pass")
        self._dedent()

    def visit_while_statement(self, node: "WhileStatement"):
        """Generate code for while statement."""
        condition_code = self._generate_expression(node.condition)
        self._emit_line(f"while {condition_code}:", node)

        self._indent()
        if node.body:
            node.body.accept(self)
        else:
            self._emit_line("pass")
        self._dedent()

    def visit_for_statement(self, node: "ForStatement"):
        """Generate code for for statement."""
        # Handle variable name - could be string or Identifier node
        if isinstance(node.variable, str):
            var_name = self._safe_identifier(node.variable)
        elif hasattr(node.variable, "name"):
            var_name = self._safe_identifier(node.variable.name)
        else:
            var_name = self._safe_identifier(str(node.variable))

        # Track loop variable in symbol table
        self.symbol_table['variables'].add(var_name)

        iterable_code = self._generate_expression(node.iterable)
        self._emit_line(f"for {var_name} in {iterable_code}:", node)

        self._indent()
        if node.body:
            node.body.accept(self)
        else:
            self._emit_line("pass")
        self._dedent()

    def visit_try_statement(self, node: "TryStatement"):
        """Generate code for try/except/finally statement."""
        self._emit_line("try:", node)

        self._indent()
        if node.try_body:
            for stmt in node.try_body:
                stmt.accept(self)
        else:
            self._emit_line("pass")
        self._dedent()

        # Generate except clauses
        for except_clause in node.except_clauses:
            except_clause.accept(self)

        # Generate finally clause
        if node.finally_body is not None:
            self._emit_line("finally:", node)
            self._indent()
            if node.finally_body:
                for stmt in node.finally_body:
                    stmt.accept(self)
            else:
                self._emit_line("pass")
            self._dedent()

    def visit_except_clause(self, node: "ExceptClause"):
        """Generate code for except clause."""
        if node.exception_variable:
            # Track exception variable in symbol table
            self.symbol_table['variables'].add(node.exception_variable)
            # ML syntax: except (error) -> Python syntax: except Exception as error
            self._emit_line(f"except Exception as {node.exception_variable}:", node)
        else:
            self._emit_line("except:", node)

        self._indent()
        if node.body:
            for stmt in node.body:
                stmt.accept(self)
        else:
            self._emit_line("pass")
        self._dedent()

    def visit_break_statement(self, node: "BreakStatement"):
        """Generate code for break statement."""
        self._emit_line("break", node)

    def visit_continue_statement(self, node: "ContinueStatement"):
        """Generate code for continue statement."""
        self._emit_line("continue", node)

    def visit_nonlocal_statement(self, node: "NonlocalStatement"):
        """Generate code for nonlocal statement.

        IMPORTANT: Semantic adjustment for REPL mode.

        In ML, 'nonlocal' means "access variable from outer scope".
        In Python, 'nonlocal' means "access variable from enclosing function scope only".

        When executing in REPL mode at module level:
        - Outer scope = module/global scope
        - Python requires 'global' keyword for module-level variables
        - Python's 'nonlocal' would fail with "no binding for nonlocal 'x' found"

        This is an intelligent fix that detects function nesting depth:
        - Top-level functions in REPL: convert 'nonlocal' → 'global' (for module scope access)
        - Nested functions in REPL: keep 'nonlocal' (for proper closure semantics)
        - Normal mode: always use 'nonlocal' (Python will validate scope)

        See: docs/proposals/repl-scope-bug.md for full analysis and rationale.
        """
        variables = ", ".join(node.variables)

        # Detect function nesting depth using parameter stack
        # len == 1: top-level function (one level of parameters on stack)
        # len > 1: nested function (multiple levels on stack)
        nesting_depth = len(self.symbol_table['parameters'])

        # In REPL mode, emit 'global' for top-level functions, 'nonlocal' for nested functions
        # In normal mode, always emit 'nonlocal'
        if self.repl_mode and nesting_depth == 1:
            # Top-level function in REPL - accessing module-level variables
            keyword = "global"
        else:
            # Nested function (REPL or normal) or normal mode - accessing enclosing function scope
            keyword = "nonlocal"

        self._emit_line(f"{keyword} {variables}", node)

    def visit_throw_statement(self, node: "ThrowStatement"):
        """Generate code for throw statement."""
        # Import MLUserException if needed
        self.context.imports_needed.add("from mlpy.ml.errors.exceptions import MLUserException")

        # Generate the dictionary argument
        dict_code = self._generate_expression(node.error_data)

        # Emit the raise statement
        self._emit_line(f"raise MLUserException({dict_code})", node)

    # NOTE: _could_be_string_expression() moved to ExpressionHelpersMixin

    # NOTE: _generate_expression() moved to ExpressionHelpersMixin

    # NOTE: _generate_slice() moved to ExpressionHelpersMixin



__all__ = ['StatementVisitorsMixin']
