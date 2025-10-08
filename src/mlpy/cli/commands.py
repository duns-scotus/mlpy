"""
CLI command implementations for mlpy.
Each command provides functionality through execute() and register_parser() methods.
"""

from pathlib import Path
from typing import Any


class BaseCommand:
    """Base class for all CLI commands."""

    def __init__(self, project_manager):
        self.project_manager = project_manager

    def execute(self, args: Any) -> int:
        """Execute the command. Return 0 for success, non-zero for error."""
        raise NotImplementedError

    def register_parser(self, subparsers) -> None:
        """Register argument parser for this command."""
        raise NotImplementedError


class InitCommand(BaseCommand):
    """Initialize a new ML project."""

    def register_parser(self, subparsers) -> None:
        parser = subparsers.add_parser(
            "init",
            help="Initialize a new ML project",
            description="Create a new ML project with the specified template and configuration.",
        )
        parser.add_argument("project_name", help="Name of the project to create")
        parser.add_argument(
            "--template",
            choices=["basic", "web", "cli", "library"],
            default="basic",
            help="Project template to use",
        )
        parser.add_argument("--dir", type=Path, default=".", help="Directory to create project in")
        parser.add_argument("--description", help="Project description")
        parser.add_argument("--author", help="Project author")
        parser.add_argument("--license", default="MIT", help="Project license")

    def execute(self, args: Any) -> int:
        """Execute project initialization."""
        try:
            success = self.project_manager.init_project(
                project_name=args.project_name, project_dir=args.dir, template=args.template
            )
            return 0 if success else 1
        except Exception as e:
            print(f"Error initializing project: {e}")
            return 1


class CompileCommand(BaseCommand):
    """Compile ML source files to Python."""

    def register_parser(self, subparsers) -> None:
        parser = subparsers.add_parser(
            "compile",
            help="Compile ML source files to Python",
            description="Transpile ML source files to Python with optimization and security analysis.",
        )
        parser.add_argument("source", help="Source file or directory to compile")
        parser.add_argument("-o", "--output", help="Output file or directory")
        parser.add_argument(
            "-O", "--optimize", type=int, choices=[0, 1, 2, 3], default=1, help="Optimization level"
        )
        parser.add_argument("--source-maps", action="store_true", help="Generate source maps")
        parser.add_argument(
            "--security-level",
            choices=["strict", "normal", "permissive"],
            default="strict",
            help="Security analysis level",
        )
        parser.add_argument("--capabilities", help="Required capabilities (comma-separated)")
        parser.add_argument(
            "--emit-code",
            choices=["silent", "single-file", "multi-file"],
            default="multi-file",
            help="Code emission mode: silent (no files), single-file (one .py with inlined modules), multi-file (separate .py files with caching)",
        )

    def execute(self, args: Any) -> int:
        """Execute compilation."""
        from mlpy.ml.transpiler import MLTranspiler

        source_path = Path(args.source)
        if not source_path.exists():
            print(f"Error: Source file not found: {args.source}")
            return 1

        # Read source code
        try:
            source_code = source_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading source file: {e}")
            return 1

        # Determine emit mode
        if args.emit_code == "silent":
            # Silent mode: inline everything, no file output
            module_output_mode = "inline"
            write_file = False
        elif args.emit_code == "single-file":
            # Single-file mode: inline everything, write one file
            module_output_mode = "inline"
            write_file = True
        else:  # multi-file
            # Multi-file mode: separate files with caching
            module_output_mode = "separate"
            write_file = True

        # Prepare import paths for user modules
        import_paths = [str(source_path.parent)]

        # Transpile
        transpiler = MLTranspiler()
        python_code, issues, source_map = transpiler.transpile_to_python(
            source_code,
            source_file=str(source_path),
            strict_security=(args.security_level == "strict"),
            generate_source_maps=args.source_maps,
            import_paths=import_paths,
            allow_current_dir=True,
            module_output_mode=module_output_mode,
        )

        # Check for errors
        if python_code is None or issues:
            print(f"Compilation failed with {len(issues)} issue(s):")
            for issue in issues[:5]:  # Show first 5 issues
                print(f"  {issue}")
            return 1

        # Output handling
        if write_file:
            if args.output:
                output_path = Path(args.output)
            else:
                output_path = source_path.with_suffix('.py')

            try:
                output_path.write_text(python_code, encoding='utf-8')
                print(f"[OK] Compiled {args.source} -> {output_path}")

                # Save source map if generated
                if source_map and args.source_maps:
                    from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap
                    import json

                    # Determine source map file path: example.py -> example.ml.map
                    map_path = output_path.with_suffix('.ml.map')

                    # Convert source_map dict to EnhancedSourceMap and save
                    # source_map is already a dict from transpile_to_python
                    try:
                        map_path.write_text(json.dumps(source_map, indent=2), encoding='utf-8')
                        print(f"  Source map: {map_path}")
                    except Exception as map_err:
                        print(f"  Warning: Could not save source map: {map_err}")

                if module_output_mode == "separate":
                    print(f"  Mode: multi-file (user modules cached as separate .py files)")
                else:
                    print(f"  Mode: single-file (all modules inlined)")
            except Exception as e:
                print(f"Error writing output file: {e}")
                return 1
        else:
            # Silent mode: just verify compilation succeeded
            print(f"[OK] Compiled {args.source} (silent mode - no files written)")

        return 0


class RunCommand(BaseCommand):
    """Compile and execute ML programs."""

    def register_parser(self, subparsers) -> None:
        parser = subparsers.add_parser(
            "run",
            help="Compile and execute ML programs",
            description="Compile and execute ML programs in a secure sandbox environment.",
        )
        parser.add_argument("source", help="ML source file to run")
        parser.add_argument("args", nargs="*", help="Arguments to pass to the program")
        parser.add_argument("--sandbox", action="store_true", default=True, help="Run in sandbox")
        parser.add_argument("--timeout", type=int, default=30, help="Execution timeout in seconds")
        parser.add_argument("--memory-limit", type=int, default=100, help="Memory limit in MB")
        parser.add_argument("--no-network", action="store_true", help="Disable network access")
        parser.add_argument(
            "--emit-code",
            choices=["silent", "single-file", "multi-file"],
            default="silent",
            help="Code emission mode: silent (no files, inline execution), single-file (one .py with inlined modules), multi-file (separate .py files with caching)",
        )

    def execute(self, args: Any) -> int:
        """Execute program."""
        from mlpy.ml.transpiler import MLTranspiler
        from mlpy.runtime.sandbox.sandbox import MLSandbox, SandboxConfig

        source_path = Path(args.source)
        if not source_path.exists():
            print(f"Error: Source file not found: {args.source}")
            return 1

        # Read source code
        try:
            source_code = source_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading source file: {e}")
            return 1

        # Determine emit mode
        if args.emit_code == "silent":
            # Silent mode: inline everything, no file output (best for direct execution)
            module_output_mode = "inline"
        elif args.emit_code == "single-file":
            # Single-file mode: inline everything, write one file
            module_output_mode = "inline"
        else:  # multi-file
            # Multi-file mode: separate files with caching
            module_output_mode = "separate"

        # Prepare import paths for user modules
        import_paths = [str(source_path.parent)]

        # Transpile (enable source maps when writing files for debugging support)
        transpiler = MLTranspiler()
        generate_maps = args.emit_code != "silent"  # Generate maps when writing files
        python_code, issues, source_map = transpiler.transpile_to_python(
            source_code,
            source_file=str(source_path),
            strict_security=True,
            generate_source_maps=generate_maps,
            import_paths=import_paths,
            allow_current_dir=True,
            module_output_mode=module_output_mode,
        )

        # Check for errors
        if python_code is None or issues:
            print(f"Compilation failed with {len(issues)} issue(s):")
            for issue in issues[:5]:
                print(f"  {issue}")
            return 1

        # Write file if not silent mode
        if args.emit_code != "silent":
            output_path = source_path.with_suffix('.py')
            try:
                output_path.write_text(python_code, encoding='utf-8')
                if module_output_mode == "separate":
                    print(f"[OK] Compiled {args.source} -> {output_path} (multi-file mode)")
                else:
                    print(f"[OK] Compiled {args.source} -> {output_path} (single-file mode)")

                # Save source map for debugging support
                if source_map:
                    import json
                    map_path = output_path.with_suffix('.ml.map')
                    try:
                        map_path.write_text(json.dumps(source_map, indent=2), encoding='utf-8')
                        print(f"  Source map: {map_path}")
                    except Exception as map_err:
                        print(f"  Warning: Could not save source map: {map_err}")

            except Exception as e:
                print(f"Warning: Could not write output file: {e}")

        # Execute in sandbox
        if args.sandbox:
            config = SandboxConfig(cpu_timeout=args.timeout)

            try:
                with MLSandbox(config) as sandbox:
                    result = sandbox._execute_python_code(python_code)

                    if result.success:
                        if result.stdout:
                            # Filter out internal __MLPY_RESULT__ marker
                            stdout_lines = result.stdout.split('\n')
                            filtered_stdout = '\n'.join(
                                line for line in stdout_lines
                                if not line.strip().startswith('__MLPY_RESULT__')
                            )
                            if filtered_stdout.strip():
                                print(filtered_stdout)
                        return 0
                    else:
                        if result.stderr:
                            print(result.stderr, end='', file=__import__('sys').stderr)
                        if result.error:
                            print(f"Error: {result.error}", file=__import__('sys').stderr)
                        return 1
            except Exception as e:
                print(f"Execution failed: {e}", file=__import__('sys').stderr)
                return 1
        else:
            # Direct execution (not recommended - bypasses sandbox)
            print("Warning: Running without sandbox (not recommended)")
            try:
                exec(python_code)
                return 0
            except Exception as e:
                print(f"Execution error: {e}", file=__import__('sys').stderr)
                return 1


class TestCommand(BaseCommand):
    """Run project tests."""

    def register_parser(self, subparsers) -> None:
        parser = subparsers.add_parser(
            "test",
            help="Run project tests",
            description="Execute project tests with coverage reporting and security validation.",
        )
        parser.add_argument("pattern", nargs="?", help="Test pattern to match")
        parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
        parser.add_argument("--security", action="store_true", help="Include security tests")
        parser.add_argument("--timeout", type=int, default=30, help="Test timeout in seconds")
        parser.add_argument("-j", "--parallel", type=int, help="Run tests in parallel")

    def execute(self, args: Any) -> int:
        """Execute tests."""
        print("Running tests...")
        print("Note: Full testing not yet implemented in CLI")
        return 0


class AnalyzeCommand(BaseCommand):
    """Perform security analysis."""

    def register_parser(self, subparsers) -> None:
        parser = subparsers.add_parser(
            "analyze",
            help="Perform security analysis",
            description="Perform comprehensive security analysis on ML code.",
        )
        parser.add_argument("path", nargs="?", default=".", help="Path to analyze")
        parser.add_argument(
            "--security", action="store_true", default=True, help="Run security analysis"
        )
        parser.add_argument(
            "--performance", action="store_true", help="Include performance analysis"
        )
        parser.add_argument(
            "--format", choices=["text", "json", "html"], default="text", help="Output format"
        )
        parser.add_argument("-o", "--output", help="Output file")

    def execute(self, args: Any) -> int:
        """Execute analysis."""
        print(f"Analyzing {args.path}...")
        print("Note: Full analysis not yet implemented in CLI")
        return 0


class WatchCommand(BaseCommand):
    """Watch files for changes."""

    def register_parser(self, subparsers) -> None:
        parser = subparsers.add_parser(
            "watch",
            help="Watch files for changes",
            description="Watch files for changes and automatically recompile/test.",
        )
        parser.add_argument("path", nargs="?", default=".", help="Path to watch")
        parser.add_argument("--pattern", default="**/*.ml", help="File patterns to watch")
        parser.add_argument("--ignore", help="Patterns to ignore")
        parser.add_argument("--command", default="compile", help="Command to run on changes")

    def execute(self, args: Any) -> int:
        """Execute watch mode."""
        print(f"Watching {args.path} for changes...")
        print("Note: Full watch mode not yet implemented in CLI")
        return 0


class ServeCommand(BaseCommand):
    """Start development servers."""

    def register_parser(self, subparsers) -> None:
        parser = subparsers.add_parser(
            "serve",
            help="Start development servers",
            description="Start development servers for various purposes.",
        )
        parser.add_argument("service", choices=["lsp", "docs", "api"], help="Service to start")
        parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
        parser.add_argument("--port", type=int, help="Port to bind to")
        parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    def execute(self, args: Any) -> int:
        """Execute service."""
        if args.service == "lsp":
            print("Starting Language Server...")
            # Import here to avoid dependency issues
            try:
                from ..lsp.server import MLLanguageServer

                server = MLLanguageServer()
                if args.port:
                    server.start_server(args.host, args.port)
                else:
                    server.start_stdio_server()
                return 0
            except ImportError:
                print("LSP server dependencies not available")
                return 1
            except Exception as e:
                print(f"Error starting LSP server: {e}")
                return 1
        else:
            print(f"Starting {args.service} service...")
            print("Note: Service not yet fully implemented in CLI")
            return 0


class FormatCommand(BaseCommand):
    """Format ML code."""

    def register_parser(self, subparsers) -> None:
        parser = subparsers.add_parser(
            "format",
            help="Format ML code",
            description="Format ML code according to style guidelines.",
        )
        parser.add_argument("path", nargs="?", default=".", help="Path to format")
        parser.add_argument("--check", action="store_true", help="Check if files are formatted")
        parser.add_argument("--diff", action="store_true", help="Show formatting changes")
        parser.add_argument("--line-length", type=int, default=100, help="Maximum line length")

    def execute(self, args: Any) -> int:
        """Execute formatting."""
        print(f"Formatting {args.path}...")
        print("Note: Full formatting not yet implemented in CLI")
        return 0


class DocCommand(BaseCommand):
    """Build and manage documentation."""

    def register_parser(self, subparsers) -> None:
        parser = subparsers.add_parser(
            "doc",
            help="Build and manage documentation",
            description="Build and manage project documentation.",
        )
        subcommands = parser.add_subparsers(dest="doc_command", help="Documentation commands")

        # Build command
        build_parser = subcommands.add_parser("build", help="Build documentation")

        # Serve command
        serve_parser = subcommands.add_parser("serve", help="Serve documentation locally")
        serve_parser.add_argument("--port", type=int, default=8000, help="Port to serve on")

        # Clean command
        clean_parser = subcommands.add_parser("clean", help="Clean documentation build")

    def execute(self, args: Any) -> int:
        """Execute documentation command."""
        if args.doc_command == "build":
            print("Building documentation...")
            # Try to build with sphinx
            try:
                import subprocess

                result = subprocess.run(["sphinx-build", "-b", "html", "docs/source", "docs/build"])
                return result.returncode
            except FileNotFoundError:
                print("Sphinx not found. Install with: pip install sphinx")
                return 1
        elif args.doc_command == "serve":
            print(f"Serving documentation on port {args.port}...")
            print("Note: Doc serving not yet implemented in CLI")
            return 0
        elif args.doc_command == "clean":
            print("Cleaning documentation build...")
            print("Note: Doc cleaning not yet implemented in CLI")
            return 0
        else:
            print("No documentation command specified")
            return 1


class LSPCommand(BaseCommand):
    """Start Language Server."""

    def register_parser(self, subparsers) -> None:
        parser = subparsers.add_parser(
            "lsp",
            help="Start Language Server",
            description="Start the ML Language Server for IDE integration.",
        )
        parser.add_argument(
            "--stdio", action="store_true", default=True, help="Use stdio communication"
        )
        parser.add_argument("--tcp", action="store_true", help="Use TCP communication")
        parser.add_argument("--host", default="127.0.0.1", help="TCP host")
        parser.add_argument("--port", type=int, default=2087, help="TCP port")

    def execute(self, args: Any) -> int:
        """Execute LSP server."""
        try:
            from ..lsp.server import MLLanguageServer

            server = MLLanguageServer()

            if args.tcp:
                print(f"Starting Language Server on {args.host}:{args.port}")
                server.start_server(args.host, args.port)
            else:
                print("Starting Language Server with stdio")
                server.start_stdio_server()

            return 0
        except ImportError:
            print("LSP server dependencies not available")
            return 1
        except Exception as e:
            print(f"Error starting Language Server: {e}")
            return 1


class DebugCommand(BaseCommand):
    """Debug ML programs interactively."""

    def register_parser(self, subparsers) -> None:
        parser = subparsers.add_parser(
            "debug",
            help="Debug ML programs interactively",
            description="Launch interactive debugging session for ML programs with breakpoints and step execution.",
        )
        parser.add_argument("source", help="ML source file to debug")
        parser.add_argument("args", nargs="*", help="Arguments to pass to the ML program")
        parser.add_argument(
            "--break-on-entry",
            action="store_true",
            help="Stop execution at program entry (first line)",
        )

    def execute(self, args: Any) -> int:
        """Execute interactive debugger."""
        try:
            from mlpy.debugging.debugger import MLDebugger
            from mlpy.debugging.source_map_index import SourceMapIndex
            from mlpy.debugging.repl import DebuggerREPL
            from mlpy.ml.transpiler import MLTranspiler

            # Check if source file exists
            source_path = Path(args.source)
            if not source_path.exists():
                print(f"Error: Source file not found: {args.source}")
                return 1

            # Transpile ML to Python
            print(f"Transpiling {args.source}...")

            transpiler = MLTranspiler()
            ml_source = source_path.read_text(encoding="utf-8")

            python_code, issues, source_map_data = transpiler.transpile_to_python(
                ml_source, source_file=str(source_path), generate_source_maps=True, strict_security=False
            )

            if python_code is None:
                print("Transpilation failed!")
                for issue in issues:
                    print(f"  - {issue.error.message}")
                return 1

            # Show security issues if any
            if issues:
                print(f"\nWarning: {len(issues)} security issues found:")
                for issue in issues:
                    print(f"  - {issue.error.message}")
                print()

            # Build source map index from transpiler's enhanced source maps
            from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap
            import json

            if source_map_data:
                # Use real source map from transpiler
                # Convert dict to EnhancedSourceMap
                source_map = EnhancedSourceMap()

                # Load mappings from source_map_data
                if "debugInfo" in source_map_data and "detailedMappings" in source_map_data["debugInfo"]:
                    for mapping_dict in source_map_data["debugInfo"]["detailedMappings"]:
                        gen = mapping_dict.get("generated", {})
                        orig = mapping_dict.get("original", {})

                        if orig:
                            source_map.add_mapping(
                                generated_line=gen.get("line", 1),
                                generated_column=gen.get("column", 0),
                                original_line=orig.get("line"),
                                original_column=orig.get("column"),
                                source_file=mapping_dict.get("source_file", str(source_path)),
                                name=mapping_dict.get("name"),
                                node_type=mapping_dict.get("node_type")
                            )

                # Save .py and .ml.map to disk for future debugging sessions
                output_path = source_path.with_suffix('.py')
                try:
                    output_path.write_text(python_code, encoding='utf-8')
                    map_path = output_path.with_suffix('.ml.map')
                    map_path.write_text(json.dumps(source_map_data, indent=2), encoding='utf-8')
                    print(f"Cached: {output_path} + {map_path}")
                except Exception as e:
                    print(f"Warning: Could not cache transpiled files: {e}")

                source_index = SourceMapIndex.from_source_map(source_map, str(output_path))
            else:
                print("Warning: No source map generated, debugging may be limited")
                source_index = SourceMapIndex(ml_to_py={}, py_to_ml={}, py_file="<generated>")

            # Create debugger
            debugger = MLDebugger(str(source_path), source_index, python_code)

            # Create REPL
            repl = DebuggerREPL(debugger)

            # Set up pause callback
            def on_pause():
                """Called when execution pauses at breakpoint."""
                debugger.show_source_context()
                repl.should_continue = False
                repl.cmdloop()

                # After REPL exits, check if should continue
                if not repl.should_continue and not debugger.finished:
                    debugger.stop()
                    sys.exit(0)

            debugger.on_pause = on_pause

            # Show intro
            print("\n" + repl.intro)
            print("Set breakpoints with 'break <line>', then 'continue' to start\n")

            # Initial REPL (to set breakpoints before running)
            repl.cmdloop()

            # If user exited without continuing, don't run
            if not repl.should_continue:
                return 0

            # Run the program
            print("\nStarting ML program...\n")
            debugger.run()

            if debugger.finished:
                print("\n\nProgram completed successfully")

            return 0

        except KeyboardInterrupt:
            print("\n\nDebugging interrupted")
            return 130
        except Exception as e:
            print(f"Debug error: {e}")
            import traceback

            traceback.print_exc()
            return 1
