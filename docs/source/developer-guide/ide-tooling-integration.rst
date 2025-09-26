========================
IDE and Tooling Integration
========================

This guide covers integrating mlpy with development environments, creating IDE plugins, and building development tools that enhance the ML programming experience.

Language Server Protocol (LSP) Integration
==========================================

mlpy provides comprehensive LSP support for modern editors and IDEs.

LSP Architecture
---------------

**File**: ``src/mlpy/tools/lsp/server.py``

.. code-block:: python

    class MLLanguageServer:
        """ML Language Server implementing LSP protocol."""

        def __init__(self):
            self.documents = {}
            self.analyzer = SecurityAnalyzer()
            self.parser = MLParser()
            self.workspace_config = None

        # Core LSP Methods
        async def initialize(self, params: InitializeParams) -> InitializeResult:
            """Initialize language server capabilities."""
            return InitializeResult(
                capabilities=ServerCapabilities(
                    text_document_sync=TextDocumentSyncOptions(
                        open_close=True,
                        change=TextDocumentSyncKind.INCREMENTAL
                    ),
                    completion_provider=CompletionOptions(
                        trigger_characters=['.', ':', '(']
                    ),
                    hover_provider=True,
                    signature_help_provider=SignatureHelpOptions(
                        trigger_characters=['(', ',']
                    ),
                    definition_provider=True,
                    references_provider=True,
                    document_highlight_provider=True,
                    document_symbol_provider=True,
                    workspace_symbol_provider=True,
                    code_action_provider=True,
                    code_lens_provider=True,
                    document_formatting_provider=True,
                    document_range_formatting_provider=True,
                    rename_provider=True,
                    folding_range_provider=True,
                    semantic_tokens_provider=SemanticTokensOptions(
                        legend=SemanticTokensLegend(
                            token_types=ML_TOKEN_TYPES,
                            token_modifiers=ML_TOKEN_MODIFIERS
                        )
                    )
                )
            )

        async def text_document_did_open(self, params: DidOpenTextDocumentParams):
            """Handle document open events."""
            document = params.text_document
            self.documents[document.uri] = document.text

            # Perform initial analysis
            await self.analyze_document(document.uri)

        async def text_document_did_change(self, params: DidChangeTextDocumentParams):
            """Handle document change events."""
            document = params.text_document
            changes = params.content_changes

            # Apply incremental changes
            current_text = self.documents.get(document.uri, "")
            updated_text = self.apply_changes(current_text, changes)
            self.documents[document.uri] = updated_text

            # Trigger incremental analysis
            await self.analyze_document_incremental(document.uri, changes)

IDE-Specific Integrations
=========================

Visual Studio Code Extension
----------------------------

**File**: ``tools/vscode-extension/src/extension.ts``

.. code-block:: typescript

    import * as vscode from 'vscode';
    import { LanguageClient, LanguageClientOptions, ServerOptions } from 'vscode-languageclient/node';

    export function activate(context: vscode.ExtensionContext) {
        // Language server configuration
        const serverOptions: ServerOptions = {
            command: 'mlpy',
            args: ['lsp'],
            options: {
                env: {
                    ...process.env,
                    MLPY_LSP_MODE: 'true'
                }
            }
        };

        const clientOptions: LanguageClientOptions = {
            documentSelector: [{ scheme: 'file', language: 'ml' }],
            synchronize: {
                fileEvents: vscode.workspace.createFileSystemWatcher('**/*.ml')
            }
        };

        // Create and start language client
        const client = new LanguageClient('mlLanguageServer', 'ML Language Server', serverOptions, clientOptions);

        // Register custom commands
        context.subscriptions.push(
            vscode.commands.registerCommand('ml.transpile', transpileCurrentFile),
            vscode.commands.registerCommand('ml.runWithSandbox', runFileInSandbox),
            vscode.commands.registerCommand('ml.analyzeSecurity', analyzeSecurityIssues),
            vscode.commands.registerCommand('ml.formatDocument', formatMLDocument)
        );

        // Start language server
        client.start();
    }

    async function transpileCurrentFile() {
        const editor = vscode.window.activeTextEditor;
        if (!editor || editor.document.languageId !== 'ml') {
            vscode.window.showErrorMessage('Please open an ML file');
            return;
        }

        const document = editor.document;
        const sourceCode = document.getText();

        try {
            // Call transpilation service
            const result = await vscode.commands.executeCommand(
                'ml.service.transpile',
                sourceCode,
                document.fileName
            );

            // Display result in new editor
            const pythonDoc = await vscode.workspace.openTextDocument({
                content: result.pythonCode,
                language: 'python'
            });

            await vscode.window.showTextDocument(pythonDoc, vscode.ViewColumn.Beside);

        } catch (error) {
            vscode.window.showErrorMessage(`Transpilation failed: ${error.message}`);
        }
    }

IntelliJ IDEA Plugin
-------------------

**File**: ``tools/intellij-plugin/src/main/kotlin/MLLanguagePlugin.kt``

.. code-block:: kotlin

    class MLLanguagePlugin : Plugin {
        override fun initPlugin() {
            // Register language support
            LanguageRegistry.registerLanguage(MLLanguage())

            // Register file type
            FileTypeRegistry.registerFileType(MLFileType())

            // Register syntax highlighting
            SyntaxHighlighterRegistry.registerHighlighter(
                MLLanguage(),
                MLSyntaxHighlighter()
            )

            // Register code completion
            CompletionContributorRegistry.register(MLCompletionContributor())

            // Register inspections
            InspectionRegistry.register(MLSecurityInspection())
            InspectionRegistry.register(MLPerformanceInspection())
        }
    }

    class MLSecurityInspection : LocalInspectionTool() {
        override fun buildVisitor(holder: ProblemsHolder, isOnTheFly: Boolean): PsiElementVisitor {
            return object : MLElementVisitor() {
                override fun visitFunctionCall(call: MLFunctionCall) {
                    super.visitFunctionCall(call)

                    if (isDangerousFunction(call.functionName)) {
                        holder.registerProblem(
                            call,
                            "Potentially dangerous function call: ${call.functionName}",
                            ProblemHighlightType.ERROR,
                            MLSecurityQuickFix()
                        )
                    }
                }
            }
        }
    }

Development Tools
================

CLI Tools Integration
--------------------

**File**: ``src/mlpy/tools/cli/main.py``

.. code-block:: python

    import click
    from rich.console import Console
    from rich.table import Table
    from rich.syntax import Syntax

    console = Console()

    @click.group()
    @click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
    @click.option('--config', '-c', help='Configuration file path')
    def cli(verbose, config):
        """ML Language Development Tools."""
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        if config:
            load_config(config)

    @cli.command()
    @click.argument('file', type=click.Path(exists=True))
    @click.option('--output', '-o', help='Output file path')
    @click.option('--strict-security', is_flag=True, default=True, help='Enable strict security analysis')
    @click.option('--generate-maps', is_flag=True, help='Generate source maps')
    def transpile(file, output, strict_security, generate_maps):
        """Transpile ML code to Python."""
        try:
            with open(file, 'r') as f:
                source_code = f.read()

            result = transpile_ml_code(
                source_code,
                source_file=file,
                strict_security=strict_security,
                generate_source_maps=generate_maps
            )

            if output:
                with open(output, 'w') as f:
                    f.write(result.python_code)
                console.print(f"✅ Transpiled to {output}")
            else:
                syntax = Syntax(result.python_code, "python", theme="monokai")
                console.print(syntax)

        except Exception as e:
            console.print(f"❌ Transpilation failed: {e}", style="red")

    @cli.command()
    @click.argument('file', type=click.Path(exists=True))
    @click.option('--format', 'output_format', default='table', help='Output format: table, json, sarif')
    def analyze(file, output_format):
        """Analyze ML code for security issues."""
        try:
            with open(file, 'r') as f:
                source_code = f.read()

            issues = analyze_security(source_code, file)

            if output_format == 'table':
                display_issues_table(issues)
            elif output_format == 'json':
                print(json.dumps([issue.to_dict() for issue in issues], indent=2))
            elif output_format == 'sarif':
                print(generate_sarif_report(issues))

        except Exception as e:
            console.print(f"❌ Analysis failed: {e}", style="red")

    def display_issues_table(issues):
        """Display security issues in formatted table."""
        table = Table(title="Security Analysis Results")

        table.add_column("Severity", style="red")
        table.add_column("Category", style="blue")
        table.add_column("Line", justify="right")
        table.add_column("Message", style="cyan")

        for issue in issues:
            severity_style = {
                'critical': 'bold red',
                'high': 'red',
                'medium': 'yellow',
                'low': 'green'
            }.get(issue.severity, 'white')

            table.add_row(
                f"[{severity_style}]{issue.severity.upper()}[/{severity_style}]",
                issue.category,
                str(issue.line) if issue.line else "-",
                issue.message
            )

        console.print(table)

Build System Integration
=======================

Webpack Plugin
-------------

**File**: ``tools/webpack-plugin/index.js``

.. code-block:: javascript

    const { execSync } = require('child_process');
    const path = require('path');

    class MLWebpackPlugin {
        constructor(options = {}) {
            this.options = {
                strictSecurity: true,
                generateSourceMaps: true,
                ...options
            };
        }

        apply(compiler) {
            compiler.hooks.compilation.tap('MLWebpackPlugin', (compilation) => {
                compilation.hooks.buildModule.tap('MLWebpackPlugin', (module) => {
                    if (module.resource && module.resource.endsWith('.ml')) {
                        this.transpileMLFile(module);
                    }
                });
            });
        }

        transpileMLFile(module) {
            const filePath = module.resource;
            const outputPath = filePath.replace('.ml', '.js');

            try {
                const command = `mlpy transpile "${filePath}" --output "${outputPath}" ${
                    this.options.strictSecurity ? '--strict-security' : ''
                } ${
                    this.options.generateSourceMaps ? '--generate-maps' : ''
                }`;

                execSync(command, { encoding: 'utf8' });

                // Update module to point to transpiled file
                module.resource = outputPath;
                module.type = 'javascript/auto';

            } catch (error) {
                throw new Error(`ML transpilation failed for ${filePath}: ${error.message}`);
            }
        }
    }

    module.exports = MLWebpackPlugin;

Rollup Plugin
------------

**File**: ``tools/rollup-plugin/index.js``

.. code-block:: javascript

    import { createFilter } from '@rollup/pluginutils';
    import { spawn } from 'child_process';
    import { promisify } from 'util';

    const execFile = promisify(spawn);

    export default function mlPlugin(options = {}) {
        const filter = createFilter(options.include || '**/*.ml', options.exclude);

        return {
            name: 'ml',

            async transform(code, id) {
                if (!filter(id)) return null;

                try {
                    const result = await this.transpileML(code, id, options);

                    return {
                        code: result.pythonCode,
                        map: result.sourceMap
                    };
                } catch (error) {
                    this.error(`ML transpilation failed: ${error.message}`, { id });
                }
            },

            async transpileML(code, filename, options) {
                const args = [
                    'transpile',
                    '--stdin',
                    '--source-file', filename
                ];

                if (options.strictSecurity !== false) {
                    args.push('--strict-security');
                }

                if (options.generateSourceMaps) {
                    args.push('--generate-maps');
                }

                const child = spawn('mlpy', args, {
                    stdio: ['pipe', 'pipe', 'pipe']
                });

                child.stdin.write(code);
                child.stdin.end();

                const [stdout, stderr] = await Promise.all([
                    this.streamToString(child.stdout),
                    this.streamToString(child.stderr)
                ]);

                const exitCode = await new Promise((resolve) => {
                    child.on('close', resolve);
                });

                if (exitCode !== 0) {
                    throw new Error(stderr);
                }

                return JSON.parse(stdout);
            },

            streamToString(stream) {
                const chunks = [];
                return new Promise((resolve, reject) => {
                    stream.on('data', chunk => chunks.push(chunk));
                    stream.on('error', reject);
                    stream.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
                });
            }
        };
    }

Testing and Debugging Tools
===========================

Test Framework Integration
--------------------------

**File**: ``src/mlpy/testing/framework.py``

.. code-block:: python

    import pytest
    from typing import Any, Optional
    from dataclasses import dataclass

    @dataclass
    class MLTestCase:
        """ML language test case definition."""
        name: str
        ml_code: str
        expected_result: Any = None
        expected_error: Optional[str] = None
        capabilities: Optional[list[str]] = None
        timeout_seconds: float = 5.0
        strict_security: bool = True

    class MLTestRunner:
        """Test runner for ML code."""

        def __init__(self):
            self.sandbox_config = SandboxConfig(
                max_memory_mb=100,
                max_cpu_time_seconds=10.0,
                allow_network=False
            )

        def run_test_case(self, test_case: MLTestCase) -> MLTestResult:
            """Run individual test case."""

            try:
                result = execute_ml_code_sandbox(
                    test_case.ml_code,
                    capabilities=test_case.capabilities,
                    sandbox_config=self.sandbox_config
                )

                if test_case.expected_error:
                    if result.success:
                        return MLTestResult(
                            name=test_case.name,
                            passed=False,
                            message=f"Expected error '{test_case.expected_error}' but execution succeeded"
                        )
                    else:
                        # Check if error matches expectation
                        error_matches = test_case.expected_error in str(result.error)
                        return MLTestResult(
                            name=test_case.name,
                            passed=error_matches,
                            message=f"Error matching: {error_matches}"
                        )
                else:
                    if not result.success:
                        return MLTestResult(
                            name=test_case.name,
                            passed=False,
                            message=f"Execution failed: {result.error}"
                        )

                    # Check result matches expectation
                    if test_case.expected_result is not None:
                        result_matches = result.return_value == test_case.expected_result
                        return MLTestResult(
                            name=test_case.name,
                            passed=result_matches,
                            message=f"Result: {result.return_value}, Expected: {test_case.expected_result}"
                        )

                return MLTestResult(
                    name=test_case.name,
                    passed=True,
                    message="Test passed"
                )

            except Exception as e:
                return MLTestResult(
                    name=test_case.name,
                    passed=False,
                    message=f"Test framework error: {e}"
                )

    # Pytest integration
    def pytest_collect_file(path, parent):
        """Collect ML test files for pytest."""
        if path.ext == ".mltest":
            return MLTestFile.from_parent(parent, fspath=path)

    class MLTestFile(pytest.File):
        """ML test file collector."""

        def collect(self):
            """Collect test cases from ML test file."""
            content = self.fspath.read()
            test_cases = parse_ml_test_file(content)

            for test_case in test_cases:
                yield MLTestItem.from_parent(self, name=test_case.name, test_case=test_case)

    class MLTestItem(pytest.Item):
        """Individual ML test case item."""

        def __init__(self, name, parent, test_case):
            super().__init__(name, parent)
            self.test_case = test_case

        def runtest(self):
            """Execute ML test case."""
            runner = MLTestRunner()
            result = runner.run_test_case(self.test_case)

            if not result.passed:
                raise MLTestFailure(result.message)

Debugging Tools
--------------

**File**: ``src/mlpy/tools/debugger/debugger.py``

.. code-block:: python

    class MLDebugger:
        """Interactive debugger for ML code."""

        def __init__(self):
            self.breakpoints: set[tuple[str, int]] = set()
            self.watch_expressions: list[str] = []
            self.call_stack: list[StackFrame] = []
            self.current_frame: Optional[StackFrame] = None

        def set_breakpoint(self, file_path: str, line_number: int):
            """Set breakpoint at specific location."""
            self.breakpoints.add((file_path, line_number))

        def add_watch(self, expression: str):
            """Add expression to watch list."""
            self.watch_expressions.append(expression)

        def debug_ml_code(self, source_code: str, source_file: str = None):
            """Debug ML code with interactive session."""

            # Parse and instrument code for debugging
            ast_tree = parse_ml_code(source_code, source_file)
            instrumented_ast = self.instrument_for_debugging(ast_tree)

            # Generate Python code with debug hooks
            generator = DebugInstrumentedGenerator()
            python_code = generator.generate(instrumented_ast)

            # Execute with debugging support
            debug_globals = {
                '__debugger__': self,
                '__breakpoint_check__': self.check_breakpoint,
                '__step_hook__': self.step_hook
            }

            try:
                exec(python_code, debug_globals)
            except DebuggerExit:
                print("Debugging session ended")

        def check_breakpoint(self, file_path: str, line_number: int):
            """Check if execution should stop at breakpoint."""
            if (file_path, line_number) in self.breakpoints:
                self.enter_debug_session(file_path, line_number)

        def enter_debug_session(self, file_path: str, line_number: int):
            """Enter interactive debugging session."""
            print(f"Breakpoint hit at {file_path}:{line_number}")

            while True:
                command = input("(mldb) ").strip().split()

                if not command:
                    continue

                cmd = command[0]

                if cmd in ['c', 'continue']:
                    break
                elif cmd in ['n', 'next']:
                    self.step_mode = 'next'
                    break
                elif cmd in ['s', 'step']:
                    self.step_mode = 'step'
                    break
                elif cmd in ['l', 'list']:
                    self.list_source(file_path, line_number)
                elif cmd in ['p', 'print']:
                    if len(command) > 1:
                        self.evaluate_expression(' '.join(command[1:]))
                elif cmd in ['w', 'watch']:
                    self.display_watch_expressions()
                elif cmd in ['bt', 'backtrace']:
                    self.display_call_stack()
                elif cmd in ['q', 'quit']:
                    raise DebuggerExit()
                else:
                    print(f"Unknown command: {cmd}")

Performance Profiling Tools
===========================

**File**: ``src/mlpy/tools/profiler/profiler.py``

.. code-block:: python

    class MLProfiler:
        """Performance profiler for ML code execution."""

        def __init__(self):
            self.call_stats: dict[str, CallStats] = {}
            self.memory_snapshots: list[MemorySnapshot] = []
            self.timeline_events: list[TimelineEvent] = []

        def profile_ml_execution(self, source_code: str, source_file: str = None) -> ProfileReport:
            """Profile ML code execution."""

            start_time = time.perf_counter()
            start_memory = self.get_memory_usage()

            try:
                # Instrument code for profiling
                result = execute_ml_code_sandbox(
                    source_code,
                    source_file=source_file,
                    profiler=self
                )

                end_time = time.perf_counter()
                end_memory = self.get_memory_usage()

                return ProfileReport(
                    total_time=end_time - start_time,
                    peak_memory=max(snapshot.usage for snapshot in self.memory_snapshots),
                    call_stats=self.call_stats,
                    timeline=self.timeline_events,
                    success=result.success
                )

            except Exception as e:
                return ProfileReport(
                    error=str(e),
                    success=False
                )

        def record_function_call(self, function_name: str, start_time: float, end_time: float):
            """Record function call statistics."""
            if function_name not in self.call_stats:
                self.call_stats[function_name] = CallStats(function_name)

            stats = self.call_stats[function_name]
            stats.call_count += 1
            stats.total_time += end_time - start_time
            stats.min_time = min(stats.min_time, end_time - start_time)
            stats.max_time = max(stats.max_time, end_time - start_time)

This comprehensive IDE and tooling integration guide provides the foundation for building sophisticated development tools that enhance the ML programming experience across different editors and build systems.