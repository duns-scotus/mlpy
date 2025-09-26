==================
Compilation Pipeline
==================

The mlpy compilation pipeline transforms ML source code into secure, executable Python code through a series of well-defined stages. Understanding this pipeline is crucial for extending mlpy or debugging compilation issues.

Pipeline Overview
=================

.. code-block:: text

    ML Source Code
         |
    [1] Lexical Analysis (Lark)
         |
    [2] Syntax Analysis & AST Generation
         |
    [3] AST Transformation & Validation
         |
    [4] Security Analysis (Parallel)
         |
    [5] Intermediate Representation (IR)
         |
    [6] Optimization Passes
         |
    [7] Python AST Generation
         |
    [8] Source Map Generation
         |
    Python Code + Debugging Info

Stage 1: Lexical Analysis
=========================

**File**: ``src/mlpy/ml/grammar/ml.lark``

The Lark parser performs tokenization and initial syntax analysis using a context-free grammar.

Key Features:
- **Performance**: Sub-millisecond parsing for typical programs
- **Error Recovery**: Detailed syntax error reporting with suggestions
- **Extensibility**: Clean grammar rules for adding new language constructs

Example Grammar Rule::

    function_definition: "function" IDENTIFIER "(" parameter_list? ")" "{" statement* "}"
    parameter_list: parameter ("," parameter)*
    parameter: IDENTIFIER (":" type_annotation)?

Stage 2: AST Generation
=======================

**File**: ``src/mlpy/ml/grammar/transformer.py``

The transformer converts parse trees into strongly-typed AST nodes.

Core AST Node Types:

.. code-block:: python

    # Expression Nodes
    class BinaryExpression(ASTNode):
        left: Expression
        operator: str
        right: Expression

    # Statement Nodes
    class FunctionDefinition(ASTNode):
        name: str
        parameters: list[Parameter]
        body: list[Statement]

    # Control Flow
    class IfStatement(ASTNode):
        condition: Expression
        then_statement: Statement
        elif_clauses: list[ElifClause]
        else_statement: Statement | None

**Adding New AST Nodes**:

1. Define the node class in ``ast_nodes.py``::

    class MatchExpression(ASTNode):
        value: Expression
        cases: list[MatchCase]
        line: int
        column: int

2. Add visitor method::

    def visit_match_expression(self, node: MatchExpression):
        # Handle match expression logic
        pass

3. Implement in transformer::

    def match_expression(self, items):
        value = items[0]
        cases = items[1:]
        return MatchExpression(value=value, cases=cases)

Stage 3: AST Validation
=======================

**File**: ``src/mlpy/ml/grammar/transformer.py``

Post-parsing validation ensures semantic correctness:

- **Type Consistency**: Variable types match usage
- **Scope Resolution**: All identifiers are properly defined
- **Control Flow**: Unreachable code and missing returns detected
- **Capability Requirements**: Security annotations are validated

Example Validation::

    def validate_function_definition(self, node: FunctionDefinition):
        # Check for duplicate parameters
        param_names = [p.name for p in node.parameters]
        if len(param_names) != len(set(param_names)):
            raise SemanticError("Duplicate parameter names")

        # Validate return paths
        if not self.has_return_path(node.body):
            if node.return_type != "void":
                raise SemanticError("Missing return statement")

Stage 4: Security Analysis
==========================

**File**: ``src/mlpy/ml/analysis/security_analyzer.py``

Multi-threaded security analysis with comprehensive threat detection:

Security Checks:
- **Code Injection**: Detection of eval, exec, dangerous imports
- **Reflection Abuse**: __class__, __globals__ access patterns
- **File System**: Path traversal and unauthorized file access
- **Network**: Unsafe HTTP operations and data leakage

Parallel Analysis Architecture::

    class ParallelSecurityAnalyzer:
        def analyze(self, ast_nodes: list[ASTNode]) -> list[SecurityIssue]:
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                for node in ast_nodes:
                    future = executor.submit(self._analyze_node, node)
                    futures.append(future)

                results = []
                for future in as_completed(futures):
                    results.extend(future.result())

                return results

**Custom Security Rules**:

Add new security patterns by extending the analyzer::

    def visit_custom_node(self, node: CustomNode):
        if self.is_dangerous_pattern(node.operation):
            self._add_issue(
                severity="high",
                category="custom_vulnerability",
                message=f"Dangerous operation: {node.operation}",
                node=node,
                context={"operation": node.operation}
            )

Stage 5: Intermediate Representation
====================================

**File**: ``src/mlpy/ml/codegen/ir_generator.py`` (Future Implementation)

The IR stage provides platform-independent code representation:

- **Control Flow Graphs**: Optimized control flow representation
- **Data Dependency Analysis**: Variable lifetime and usage tracking
- **Capability Tracking**: Security requirements propagation
- **Optimization Metadata**: Performance improvement opportunities

Example IR Structure::

    class IRNode:
        opcode: str
        operands: list[str]
        result: str
        capabilities: set[str]
        metadata: dict

    # Example: Binary operation
    IRNode(
        opcode="ADD",
        operands=["x", "y"],
        result="temp_1",
        capabilities={"execute:arithmetic"},
        metadata={"source_line": 42}
    )

Stage 6: Optimization Passes
============================

**File**: ``src/mlpy/ml/optimization/`` (Future Implementation)

Multiple optimization passes improve performance and security:

**Dead Code Elimination**::

    def eliminate_dead_code(self, ir_nodes: list[IRNode]) -> list[IRNode]:
        live_vars = self.compute_live_variables(ir_nodes)
        return [node for node in ir_nodes if node.result in live_vars]

**Constant Folding**::

    def fold_constants(self, node: BinaryExpression) -> Expression:
        if isinstance(node.left, NumberLiteral) and isinstance(node.right, NumberLiteral):
            if node.operator == "+":
                return NumberLiteral(node.left.value + node.right.value)
        return node

**Security Optimization**::

    def optimize_capability_checks(self, nodes: list[IRNode]) -> list[IRNode]:
        # Combine multiple capability checks for same resource
        # Cache capability validation results
        pass

Stage 7: Python AST Generation
===============================

**File**: ``src/mlpy/ml/codegen/python_generator.py``

Generates Python AST nodes with security instrumentation:

Core Generation Patterns::

    def visit_function_call(self, node: FunctionCall) -> ast.Call:
        # Generate capability check
        capability_check = self.generate_capability_check(node.capabilities)

        # Generate actual function call
        func_call = ast.Call(
            func=ast.Name(id=node.function, ctx=ast.Load()),
            args=[self.visit(arg) for arg in node.arguments],
            keywords=[]
        )

        # Wrap with security validation
        return ast.If(
            test=capability_check,
            body=[ast.Return(value=func_call)],
            orelse=[self.generate_security_error()]
        )

**Assignment Handling**::

    def visit_assignment_statement(self, node: AssignmentStatement) -> ast.Assign:
        if isinstance(node.target, MemberAccess):
            # obj.prop = value -> obj['prop'] = value
            return ast.Assign(
                targets=[ast.Subscript(
                    value=self.visit(node.target.object),
                    slice=ast.Constant(value=node.target.member),
                    ctx=ast.Store()
                )],
                value=self.visit(node.value)
            )

Stage 8: Source Map Generation
==============================

**File**: ``src/mlpy/ml/codegen/enhanced_source_maps.py``

Enhanced source maps provide debugging support:

Source Map Structure::

    class SourceMap:
        mappings: list[SourceMapping]
        sources: list[str]
        names: list[str]
        source_root: str
        debug_info: DebugInfo

    class SourceMapping:
        generated_line: int
        generated_column: int
        source_line: int
        source_column: int
        source_file: str
        name: str | None

**IDE Integration**::

    def generate_vscode_source_map(self, mappings: list[SourceMapping]) -> dict:
        return {
            "version": 3,
            "sources": self.sources,
            "mappings": self.encode_vlq_mappings(mappings),
            "sourcesContent": self.load_source_files(),
            "debugInfo": {
                "capabilities": self.extract_capabilities(),
                "securityContext": self.get_security_context()
            }
        }

Error Handling and Recovery
===========================

Each pipeline stage implements comprehensive error handling:

**Parse Error Recovery**::

    def handle_parse_error(self, error: ParseError) -> RecoveryAction:
        if error.error_type == "missing_semicolon":
            return RecoveryAction.INSERT_TOKEN
        elif error.error_type == "unmatched_brace":
            return RecoveryAction.SKIP_TO_NEXT_STATEMENT
        else:
            return RecoveryAction.ABORT_WITH_DETAILS

**Security Error Reporting**::

    def report_security_issue(self, issue: SecurityIssue) -> None:
        error_context = create_error_context(
            error=issue.to_ml_error(),
            source_file=self.source_file,
            line=issue.line,
            column=issue.column
        )

        self.error_reporter.report(error_context)

Performance Characteristics
===========================

Pipeline stage performance targets:

================== ============== =====================
Stage              Target Time    Optimization Strategy
================== ============== =====================
Lexical Analysis   < 0.1ms        Optimized Lark grammar
AST Generation     < 0.5ms        Efficient transformations
Security Analysis  < 1.0ms        Parallel processing
IR Generation      < 0.2ms        Streamlined IR format
Optimization       < 2.0ms        Incremental passes
Python Generation  < 1.0ms        Template-based generation
Source Maps        < 0.3ms        Cached metadata
================== ============== =====================

**Total Pipeline**: < 5ms for typical programs

Debugging the Pipeline
======================

Enable detailed pipeline debugging::

    export MLPY_DEBUG_PIPELINE=true
    export MLPY_PROFILE_STAGES=true

    # Run compilation with debugging
    mlpy compile --debug-ast --profile program.ml

Debug output includes:
- AST structure at each transformation stage
- Security analysis results and timing
- Optimization pass effects
- Generated Python AST structure
- Source map generation details

Extension Points
================

The pipeline provides several extension points:

1. **Custom AST Nodes**: Add new language constructs
2. **Security Analyzers**: Implement domain-specific security checks
3. **Optimization Passes**: Add performance improvements
4. **Code Generators**: Support new target platforms
5. **Source Map Formats**: IDE-specific debugging support

Each extension point maintains security guarantees and performance characteristics of the overall pipeline.