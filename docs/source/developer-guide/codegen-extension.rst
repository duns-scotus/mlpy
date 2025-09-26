====================
Code Generation Extension
====================

This guide covers extending mlpy's code generation pipeline to support new language features, target platforms, and optimization strategies. The code generator transforms ML AST nodes into executable Python code while maintaining security guarantees and performance characteristics.

Code Generation Architecture
============================

The code generation system consists of several interconnected components:

.. code-block:: text

    ┌─────────────────────┐    ┌─────────────────────┐
    │   AST Traversal     │────│   Python AST        │
    │   (Visitor Pattern) │    │   Generation        │
    └─────────────────────┘    └─────────────────────┘
             │                          │
             ▼                          ▼
    ┌─────────────────────┐    ┌─────────────────────┐
    │   Source Map        │────│   Optimization      │
    │   Generation        │    │   Passes            │
    └─────────────────────┘    └─────────────────────┘

Core Extension Points
====================

**File**: ``src/mlpy/ml/codegen/python_generator.py``

The PythonGenerator class provides several extension mechanisms:

1. **Visitor Methods** - Handle new AST node types
2. **Code Templates** - Reusable code generation patterns
3. **Optimization Passes** - Transform generated code
4. **Target Specialization** - Platform-specific generation
5. **Runtime Integration** - Capability and security instrumentation

Adding Support for New Language Features
========================================

Example: Implementing Async/Await Code Generation
-------------------------------------------------

Let's extend the code generator to support async/await syntax:

**AST Nodes** (already defined in grammar extension):

.. code-block:: python

    @dataclass
    class AsyncFunctionDefinition(ASTNode):
        """Async function definition."""
        name: str
        parameters: list[Parameter]
        body: list[Statement]
        return_type: Optional[TypeAnnotation] = None

    @dataclass
    class AwaitExpression(ASTNode):
        """Await expression."""
        expression: Expression

**Code Generation Implementation**:

.. code-block:: python

    class EnhancedPythonGenerator(PythonGenerator):
        """Extended Python generator with async/await support."""

        def visit_async_function_definition(self, node: AsyncFunctionDefinition) -> ast.AsyncFunctionDef:
            """Generate Python async function definition."""

            # Generate parameters
            params = self.generate_parameters(node.parameters)

            # Generate function body with capability checks
            body_stmts = []

            # Add capability validation at function start
            if self.requires_capabilities(node):
                capability_check = self.generate_capability_validation(node)
                body_stmts.append(capability_check)

            # Generate async body statements
            for stmt in node.body:
                body_stmt = self.visit(stmt)
                body_stmts.append(body_stmt)

            # Ensure async function has return statement
            if not self.has_return_statement(body_stmts):
                body_stmts.append(ast.Return(value=ast.Constant(value=None)))

            return ast.AsyncFunctionDef(
                name=node.name,
                args=params,
                body=body_stmts,
                decorator_list=self.generate_async_decorators(node),
                returns=self.generate_return_annotation(node.return_type),
                type_comment=None
            )

        def visit_await_expression(self, node: AwaitExpression) -> ast.Await:
            """Generate Python await expression."""

            # Generate the awaited expression
            awaited_expr = self.visit(node.expression)

            # Add timeout wrapper if configured
            if self.config.async_timeout:
                awaited_expr = self.wrap_with_timeout(awaited_expr, self.config.async_timeout)

            # Add capability check for async operations
            if self.requires_async_capability(node.expression):
                capability_check = self.generate_async_capability_check(node.expression)

                # Wrap in conditional await
                return ast.IfExp(
                    test=capability_check,
                    body=ast.Await(value=awaited_expr),
                    orelse=self.generate_capability_error("async_operation")
                )

            return ast.Await(value=awaited_expr)

        def generate_async_decorators(self, node: AsyncFunctionDefinition) -> list[ast.expr]:
            """Generate decorators for async functions."""
            decorators = []

            # Add profiling decorator for async functions
            if self.config.enable_profiling:
                decorators.append(
                    ast.Name(id='profile_async', ctx=ast.Load())
                )

            # Add timeout decorator
            if hasattr(node, 'timeout') and node.timeout:
                decorators.append(
                    ast.Call(
                        func=ast.Name(id='async_timeout', ctx=ast.Load()),
                        args=[ast.Constant(value=node.timeout)],
                        keywords=[]
                    )
                )

            return decorators

        def wrap_with_timeout(self, expr: ast.expr, timeout: float) -> ast.Call:
            """Wrap async expression with timeout."""
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='asyncio', ctx=ast.Load()),
                    attr='wait_for',
                    ctx=ast.Load()
                ),
                args=[
                    expr,
                    ast.Constant(value=timeout)
                ],
                keywords=[]
            )

Advanced Code Generation Patterns
=================================

Template-Based Generation
-------------------------

Use templates for complex code patterns:

.. code-block:: python

    class TemplateBasedGenerator(PythonGenerator):
        """Code generator using templates for complex patterns."""

        def __init__(self):
            super().__init__()
            self.templates = self.load_code_templates()

        def load_code_templates(self) -> dict[str, CodeTemplate]:
            """Load code generation templates."""
            return {
                'error_handling': CodeTemplate("""
                    try:
                        {main_code}
                    except {exception_types} as e:
                        {error_handler}
                    finally:
                        {cleanup_code}
                """),

                'capability_wrapper': CodeTemplate("""
                    if not _capability_context.check("{capability}", "execute"):
                        raise CapabilityError("Missing capability: {capability}")

                    {wrapped_code}
                """),

                'async_pattern': CodeTemplate("""
                    async def {function_name}({parameters}):
                        {capability_checks}

                        async with {resource_manager}:
                            {function_body}

                        return {return_expression}
                """),

                'batch_operation': CodeTemplate("""
                    def {function_name}_batch({batch_parameters}):
                        results = []

                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            futures = []
                            for item in {batch_items}:
                                future = executor.submit({single_function}, item)
                                futures.append(future)

                            for future in concurrent.futures.as_completed(futures):
                                results.append(future.result())

                        return results
                """)
            }

        def generate_with_template(self,
                                 template_name: str,
                                 **kwargs) -> ast.Module:
            """Generate code using template."""

            template = self.templates[template_name]
            generated_code = template.render(**kwargs)

            # Parse generated code into AST
            try:
                return ast.parse(generated_code)
            except SyntaxError as e:
                raise CodeGenerationError(f"Template generated invalid code: {e}")

        def visit_try_statement(self, node: TryStatement) -> ast.Try:
            """Generate try statement using error handling template."""

            # Extract components
            main_code = [self.visit(stmt) for stmt in node.try_body]
            exception_handlers = []

            for except_clause in node.except_clauses:
                handler = ast.ExceptHandler(
                    type=self.generate_exception_type(except_clause.exception_type),
                    name=except_clause.variable_name,
                    body=[self.visit(stmt) for stmt in except_clause.body]
                )
                exception_handlers.append(handler)

            finally_body = []
            if node.finally_body:
                finally_body = [self.visit(stmt) for stmt in node.finally_body]

            return ast.Try(
                body=main_code,
                handlers=exception_handlers,
                orelse=[],  # ML doesn't have else clause for try
                finalbody=finally_body
            )

Optimization Passes
===================

Post-Generation Optimization
----------------------------

.. code-block:: python

    class CodeOptimizer:
        """Post-generation code optimization."""

        def __init__(self):
            self.optimization_passes = [
                DeadCodeElimination(),
                ConstantFolding(),
                CommonSubexpressionElimination(),
                CapabilityOptimization(),
                LoopOptimization()
            ]

        def optimize(self, ast_module: ast.Module) -> ast.Module:
            """Apply optimization passes to generated code."""

            optimized_ast = ast_module

            for pass_instance in self.optimization_passes:
                try:
                    optimized_ast = pass_instance.optimize(optimized_ast)
                except Exception as e:
                    logger.warning(f"Optimization pass {pass_instance.__class__.__name__} failed: {e}")

            return optimized_ast

    class DeadCodeElimination(ast.NodeTransformer):
        """Remove unreachable code."""

        def visit_If(self, node: ast.If) -> ast.If:
            """Optimize if statements with constant conditions."""

            self.generic_visit(node)  # Visit children first

            if isinstance(node.test, ast.Constant):
                if node.test.value:
                    # Condition is always true - return body
                    return node.body[0] if len(node.body) == 1 else ast.Module(body=node.body)
                else:
                    # Condition is always false - return else clause or remove
                    if node.orelse:
                        return node.orelse[0] if len(node.orelse) == 1 else ast.Module(body=node.orelse)
                    else:
                        return None  # Remove entire if statement

            return node

    class ConstantFolding(ast.NodeTransformer):
        """Fold constant expressions at compile time."""

        def visit_BinOp(self, node: ast.BinOp) -> ast.expr:
            """Fold binary operations on constants."""

            self.generic_visit(node)

            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                left_val = node.left.value
                right_val = node.right.value

                try:
                    if isinstance(node.op, ast.Add):
                        result = left_val + right_val
                    elif isinstance(node.op, ast.Sub):
                        result = left_val - right_val
                    elif isinstance(node.op, ast.Mult):
                        result = left_val * right_val
                    elif isinstance(node.op, ast.Div):
                        if right_val != 0:
                            result = left_val / right_val
                        else:
                            return node  # Keep division by zero for runtime error
                    else:
                        return node

                    return ast.Constant(value=result)

                except (TypeError, ValueError, ZeroDivisionError):
                    # Can't fold this operation
                    return node

            return node

    class CapabilityOptimization(ast.NodeTransformer):
        """Optimize capability checks."""

        def __init__(self):
            self.capability_cache = set()

        def visit_If(self, node: ast.If) -> ast.If:
            """Optimize redundant capability checks."""

            # Check if this is a capability check
            if self.is_capability_check(node.test):
                capability_name = self.extract_capability_name(node.test)

                if capability_name in self.capability_cache:
                    # Capability already checked - remove check
                    return ast.Module(body=node.body) if len(node.body) > 1 else node.body[0]
                else:
                    # Add to cache for future optimization
                    self.capability_cache.add(capability_name)

            return self.generic_visit(node)

Target Platform Specialization
==============================

Multi-Platform Code Generation
------------------------------

.. code-block:: python

    class MultiPlatformGenerator:
        """Generate code optimized for different target platforms."""

        def __init__(self, target_platform: str = "python3.12"):
            self.target_platform = target_platform
            self.platform_configs = {
                "python3.12": Python312Config(),
                "python3.11": Python311Config(),
                "pypy3.10": PyPy310Config(),
                "micropython": MicroPythonConfig()
            }

        def generate_for_platform(self, ast_node: ASTNode) -> str:
            """Generate platform-optimized code."""

            config = self.platform_configs[self.target_platform]
            generator = self.create_platform_generator(config)

            python_ast = generator.visit(ast_node)
            optimized_ast = self.apply_platform_optimizations(python_ast, config)

            return ast.unparse(optimized_ast)

        def create_platform_generator(self, config: PlatformConfig) -> PythonGenerator:
            """Create generator configured for target platform."""

            generator = PythonGenerator()
            generator.config = config

            # Add platform-specific visitor methods
            if config.supports_walrus_operator:
                generator.visit_assignment_expression = self.generate_walrus_operator
            else:
                generator.visit_assignment_expression = self.generate_assignment_fallback

            if config.supports_match_statement:
                generator.visit_match_expression = self.generate_native_match
            else:
                generator.visit_match_expression = self.generate_if_elif_chain

            return generator

        def apply_platform_optimizations(self,
                                       ast_module: ast.Module,
                                       config: PlatformConfig) -> ast.Module:
            """Apply platform-specific optimizations."""

            optimizations = []

            if config.optimize_for_memory:
                optimizations.append(MemoryOptimization())

            if config.optimize_for_speed:
                optimizations.append(SpeedOptimization())

            if config.minimal_runtime:
                optimizations.append(RuntimeMinimization())

            optimized_ast = ast_module
            for optimization in optimizations:
                optimized_ast = optimization.optimize(optimized_ast)

            return optimized_ast

    class Python312Config(PlatformConfig):
        """Configuration for Python 3.12 target."""
        supports_walrus_operator = True
        supports_match_statement = True
        supports_type_unions = True
        supports_exception_groups = True
        optimize_for_speed = True
        optimize_for_memory = False
        minimal_runtime = False

    class MicroPythonConfig(PlatformConfig):
        """Configuration for MicroPython target."""
        supports_walrus_operator = False
        supports_match_statement = False
        supports_type_unions = False
        supports_exception_groups = False
        optimize_for_speed = False
        optimize_for_memory = True
        minimal_runtime = True

Source Map Generation
====================

Enhanced Debugging Support
--------------------------

.. code-block:: python

    class EnhancedSourceMapGenerator:
        """Generate detailed source maps for debugging."""

        def __init__(self):
            self.source_mappings: list[SourceMapping] = []
            self.name_mappings: dict[str, str] = {}
            self.scope_mappings: dict[int, ScopeInfo] = {}

        def generate_source_map(self,
                               ml_ast: ASTNode,
                               python_ast: ast.Module,
                               source_code: str) -> EnhancedSourceMap:
            """Generate comprehensive source map."""

            # Generate basic mappings
            self.generate_basic_mappings(ml_ast, python_ast)

            # Generate scope information
            self.generate_scope_mappings(ml_ast, python_ast)

            # Generate variable mappings
            self.generate_variable_mappings(ml_ast, python_ast)

            # Generate capability mappings
            self.generate_capability_mappings(ml_ast, python_ast)

            return EnhancedSourceMap(
                version=3,
                sources=[source_code],
                mappings=self.encode_mappings(),
                names=list(self.name_mappings.keys()),
                scopes=self.scope_mappings,
                capabilities=self.extract_capability_info(ml_ast),
                debug_symbols=self.generate_debug_symbols(ml_ast, python_ast)
            )

        def generate_debug_symbols(self,
                                 ml_ast: ASTNode,
                                 python_ast: ast.Module) -> DebugSymbolTable:
            """Generate debug symbol table."""

            symbols = DebugSymbolTable()

            # Extract function information
            for node in ast.walk(python_ast):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    symbols.add_function(
                        name=node.name,
                        line_start=node.lineno,
                        line_end=node.end_lineno,
                        parameters=[arg.arg for arg in node.args.args],
                        local_variables=self.extract_local_variables(node)
                    )

                elif isinstance(node, ast.ClassDef):
                    symbols.add_class(
                        name=node.name,
                        line_start=node.lineno,
                        line_end=node.end_lineno,
                        methods=[n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    )

            return symbols

Runtime Integration
==================

Security Instrumentation
------------------------

.. code-block:: python

    class SecurityInstrumentedGenerator(PythonGenerator):
        """Generate code with security instrumentation."""

        def __init__(self):
            super().__init__()
            self.security_calls = []

        def visit_function_call(self, node: FunctionCall) -> ast.Call:
            """Generate function call with security instrumentation."""

            # Generate basic function call
            func_call = super().visit_function_call(node)

            # Add security instrumentation
            if self.is_security_sensitive(node):
                return self.wrap_with_security_monitoring(func_call, node)

            return func_call

        def wrap_with_security_monitoring(self,
                                        func_call: ast.Call,
                                        original_node: FunctionCall) -> ast.Call:
            """Wrap function call with security monitoring."""

            monitoring_call = ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='security_monitor', ctx=ast.Load()),
                    attr='monitor_call',
                    ctx=ast.Load()
                ),
                args=[
                    ast.Constant(value=original_node.function),  # Function name
                    func_call,  # Original call
                    ast.List(  # Capabilities required
                        elts=[ast.Constant(value=cap) for cap in self.get_required_capabilities(original_node)],
                        ctx=ast.Load()
                    )
                ],
                keywords=[]
            )

            return monitoring_call

        def generate_capability_validation(self, node: ASTNode) -> ast.If:
            """Generate runtime capability validation."""

            required_caps = self.get_required_capabilities(node)

            if not required_caps:
                return None

            # Generate validation condition
            validation_calls = []
            for cap in required_caps:
                validation_calls.append(
                    ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id='_capability_context', ctx=ast.Load()),
                            attr='check',
                            ctx=ast.Load()
                        ),
                        args=[
                            ast.Constant(value=cap),
                            ast.Constant(value='execute')
                        ],
                        keywords=[]
                    )
                )

            # Combine with AND
            condition = validation_calls[0]
            for call in validation_calls[1:]:
                condition = ast.BoolOp(op=ast.And(), values=[condition, call])

            # Generate capability error
            error_raise = ast.Raise(
                exc=ast.Call(
                    func=ast.Name(id='CapabilityError', ctx=ast.Load()),
                    args=[ast.Constant(value=f"Missing capabilities: {required_caps}")],
                    keywords=[]
                )
            )

            return ast.If(
                test=ast.UnaryOp(op=ast.Not(), operand=condition),
                body=[error_raise],
                orelse=[]
            )

Performance Monitoring Integration
---------------------------------

.. code-block:: python

    class PerformanceInstrumentedGenerator(PythonGenerator):
        """Generate code with performance monitoring."""

        def visit_function_definition(self, node: FunctionDefinition) -> ast.FunctionDef:
            """Generate function with performance profiling."""

            # Generate basic function
            func_def = super().visit_function_definition(node)

            # Add performance profiling decorator
            profiling_decorator = ast.Call(
                func=ast.Name(id='profile_function', ctx=ast.Load()),
                args=[ast.Constant(value=node.name)],
                keywords=[]
            )

            func_def.decorator_list.insert(0, profiling_decorator)

            return func_def

        def visit_loop_statement(self, node: LoopStatement) -> ast.stmt:
            """Generate loop with performance monitoring."""

            # Generate basic loop
            loop_stmt = super().visit_loop_statement(node)

            # Wrap with performance monitoring
            monitoring_context = ast.With(
                items=[
                    ast.withitem(
                        context_expr=ast.Call(
                            func=ast.Name(id='performance_monitor', ctx=ast.Load()),
                            args=[ast.Constant(value='loop_execution')],
                            keywords=[]
                        ),
                        optional_vars=None
                    )
                ],
                body=[loop_stmt]
            )

            return monitoring_context

This comprehensive code generation extension guide provides the foundation for building sophisticated, platform-aware, and security-conscious code generators that can adapt to new language features and target environments while maintaining performance and safety guarantees.