#!/usr/bin/env python3
"""
Unified ML Test Runner - Complete Pipeline Testing and Validation

Integrates parsing validation and end-to-end integration testing with a
comprehensive CLI interface and result matrix for debugging pipeline stages.

Usage:
    python ml_test_runner.py --help
    python ml_test_runner.py --parse           # Parse validation only
    python ml_test_runner.py --full            # Complete pipeline with result matrix
    python ml_test_runner.py --full --matrix   # Show detailed result matrix
"""

import io
import sys

# Set UTF-8 encoding for stdout/stderr on Windows
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
import argparse
import json
import textwrap
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import ML pipeline components
from mlpy.ml.analysis.ast_transformer import ASTTransformer
from mlpy.ml.analysis.ast_validator import ASTValidator
from mlpy.ml.analysis.information_collector import MLInformationCollector
from mlpy.ml.analysis.optimizer import MLOptimizer
from mlpy.ml.analysis.parallel_analyzer import ParallelSecurityAnalyzer
from mlpy.ml.analysis.security_deep import SecurityDeepAnalyzer
from mlpy.ml.grammar.parser import MLParser
from mlpy.ml.transpiler import MLTranspiler
from mlpy.runtime.sandbox.sandbox import MLSandbox, SandboxConfig


class StageResult(Enum):
    """Result of a pipeline stage."""

    PASS = "+"
    FAIL = "X"
    SKIP = "-"
    ERROR = "E"


@dataclass
class PipelineStageResults:
    """Results for each stage of the ML processing pipeline."""

    parse: StageResult = StageResult.SKIP
    ast: StageResult = StageResult.SKIP
    ast_valid: StageResult = StageResult.SKIP
    transform: StageResult = StageResult.SKIP
    typecheck: StageResult = StageResult.SKIP
    security_deep: StageResult = StageResult.SKIP
    optimize: StageResult = StageResult.SKIP
    security: StageResult = StageResult.SKIP
    codegen: StageResult = StageResult.SKIP
    execution: StageResult = StageResult.SKIP

    def get_stage_results(self) -> list[StageResult]:
        """Get results as ordered list for matrix display."""
        return [
            self.parse,
            self.ast,
            self.ast_valid,
            self.transform,
            self.typecheck,
            self.security_deep,
            self.optimize,
            self.security,
            self.codegen,
            self.execution,
        ]


@dataclass
class TestFileResult:
    """Complete test result for a single ML file."""

    file_path: str
    file_name: str
    category: str
    line_count: int
    char_count: int
    total_time_ms: float

    # Pipeline stage results
    stages: PipelineStageResults

    # Detailed results from each stage
    parse_error: str | None = None
    ast_validation_issues: list = None
    transform_details: dict[str, Any] = None
    type_check_issues: list = None
    type_check_details: dict[str, Any] = None
    information_result: Any = None  # Information collector result
    security_deep_threats: list = None
    security_deep_details: dict[str, Any] = None
    optimization_results: list = None
    optimization_details: dict[str, Any] = None
    security_threats: int = 0
    security_details: dict[str, Any] = None
    transpilation_result: tuple[str, list, dict] | None = None
    execution_result: dict[str, Any] | None = None

    # Overall assessment
    overall_result: StageResult = StageResult.SKIP
    error_message: str | None = None


class UnifiedMLTestRunner:
    """Unified test runner for ML pipeline validation and testing."""

    def __init__(self, test_directory: str | None = None):
        self.test_directory = (
            Path(test_directory) if test_directory else Path(__file__).parent / "ml_integration"
        )
        self.results: list[TestFileResult] = []

        # Initialize pipeline components (lazy loaded)
        self._parser = None
        self._transpiler = None
        self._security_analyzer = None
        self._ast_validator = None
        self._ast_transformer = None
        self._information_collector = None
        self._security_deep_analyzer = None
        self._optimizer = None

        # Test categories and expectations
        self.test_categories = {
            "ml_core": {
                "expected_threats": 0,
                "should_transpile": True,
                "should_execute": True,
                "description": "Core ML language feature tests (pure language, no stdlib)",
            },
            "ml_builtin": {
                "expected_threats": 0,
                "should_transpile": True,
                "should_execute": True,
                "description": "Builtin module function tests (auto-imported stdlib functions)",
            },
            "ml_stdlib": {
                "expected_threats": 0,
                "should_transpile": True,
                "should_execute": True,
                "description": "Standard library module tests (console, math, string, array, datetime, json, collections, functional, regex, random, file, path, http)",
            },
            "ml_module": {
                "expected_threats": 0,
                "should_transpile": True,
                "should_execute": True,
                "description": "User-defined module import tests (custom modules, submodules, packages)",
            },
        }

    @property
    def parser(self) -> MLParser:
        """Lazy-loaded ML parser."""
        if self._parser is None:
            self._parser = MLParser()
        return self._parser

    @property
    def transpiler(self) -> MLTranspiler:
        """Lazy-loaded ML transpiler."""
        if self._transpiler is None:
            self._transpiler = MLTranspiler()
        return self._transpiler

    @property
    def security_analyzer(self) -> ParallelSecurityAnalyzer:
        """Lazy-loaded security analyzer."""
        if self._security_analyzer is None:
            self._security_analyzer = ParallelSecurityAnalyzer(max_workers=3)
        return self._security_analyzer

    @property
    def ast_validator(self) -> ASTValidator:
        """Lazy-loaded AST validator."""
        if self._ast_validator is None:
            self._ast_validator = ASTValidator()
        return self._ast_validator

    @property
    def ast_transformer(self) -> ASTTransformer:
        """Lazy-loaded AST transformer."""
        if self._ast_transformer is None:
            self._ast_transformer = ASTTransformer()
        return self._ast_transformer

    @property
    def information_collector(self) -> MLInformationCollector:
        """Lazy-loaded information collector."""
        if self._information_collector is None:
            self._information_collector = MLInformationCollector()
        return self._information_collector

    @property
    def security_deep_analyzer(self) -> SecurityDeepAnalyzer:
        """Lazy-loaded security deep analyzer."""
        if self._security_deep_analyzer is None:
            self._security_deep_analyzer = SecurityDeepAnalyzer()
        return self._security_deep_analyzer

    @property
    def optimizer(self) -> MLOptimizer:
        """Lazy-loaded optimizer."""
        if self._optimizer is None:
            self._optimizer = MLOptimizer()
        return self._optimizer

    def discover_test_files(self) -> list[str]:
        """Discover all ML test files in the test directory structure."""
        test_files = []

        # Search in category subdirectories
        for category_dir in self.test_directory.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith("."):
                continue

            for ml_file in category_dir.glob("*.ml"):
                test_files.append(str(ml_file))

        return sorted(test_files)

    def categorize_file(self, file_path: str) -> str:
        """Determine the category of a test file."""
        path = Path(file_path)

        # Check if it's in a known category directory
        for category in self.test_categories.keys():
            if category in str(path.parent):
                return category

        # Default to ml_core for uncategorized files
        return "ml_core"

    def run_parse_only(self, file_path: str) -> TestFileResult:
        """Run parsing validation only."""
        start_time = time.perf_counter()

        # Initialize result
        result = TestFileResult(
            file_path=file_path,
            file_name=Path(file_path).name,
            category=self.categorize_file(file_path),
            line_count=0,
            char_count=0,
            total_time_ms=0.0,
            stages=PipelineStageResults(),
        )

        try:
            # Read file
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            result.line_count = len(content.splitlines())
            result.char_count = len(content)

            # Parse stage
            ast = self.parser.parse_file(file_path)
            result.stages.parse = StageResult.PASS
            result.stages.ast = StageResult.PASS  # If parsing succeeded, AST was created

            result.overall_result = StageResult.PASS

        except Exception as e:
            result.stages.parse = StageResult.FAIL
            result.parse_error = str(e)
            result.overall_result = StageResult.FAIL
            result.error_message = f"Parse failed: {e}"

            # Still try to get file stats
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
                result.line_count = len(content.splitlines())
                result.char_count = len(content)
            except:
                pass

        result.total_time_ms = (time.perf_counter() - start_time) * 1000
        return result

    def run_full_pipeline(self, file_path: str) -> TestFileResult:
        """Run complete pipeline: parse → ast → ast_valid → transform → typecheck → security_deep → optimize → security → codegen → execution."""
        start_time = time.perf_counter()

        # Initialize result
        result = TestFileResult(
            file_path=file_path,
            file_name=Path(file_path).name,
            category=self.categorize_file(file_path),
            line_count=0,
            char_count=0,
            total_time_ms=0.0,
            stages=PipelineStageResults(),
        )

        category_config = self.test_categories.get(result.category, {})

        try:
            # Read file
            with open(file_path, encoding="utf-8") as f:
                ml_source = f.read()

            result.line_count = len(ml_source.splitlines())
            result.char_count = len(ml_source)

            # Stage 1: Parse
            try:
                ast = self.parser.parse_file(file_path)
                result.stages.parse = StageResult.PASS
                result.stages.ast = StageResult.PASS
            except Exception as e:
                result.stages.parse = StageResult.FAIL
                result.parse_error = str(e)
                result.overall_result = StageResult.FAIL
                result.error_message = f"Parse failed: {e}"
                return result

            # Stage 2: AST Validation
            try:
                validation_result = self.ast_validator.validate(ast)
                result.ast_validation_issues = validation_result.issues

                if validation_result.is_valid:
                    result.stages.ast_valid = StageResult.PASS
                else:
                    result.stages.ast_valid = StageResult.FAIL
                    result.overall_result = StageResult.FAIL
                    error_messages = [issue.message for issue in validation_result.errors]
                    result.error_message = f"AST validation failed: {'; '.join(error_messages)}"
                    return result
            except Exception as e:
                result.stages.ast_valid = StageResult.ERROR
                result.overall_result = StageResult.ERROR
                result.error_message = f"AST validation error: {e}"
                return result

            # Stage 3: AST Transformation
            try:
                transform_result = self.ast_transformer.transform(ast)
                ast = transform_result.transformed_ast  # Use transformed AST for subsequent stages

                result.transform_details = {
                    "transformations_applied": transform_result.transformations_applied,
                    "transformation_summary": transform_result.transformation_summary,
                    "transformation_time_ms": transform_result.transformation_time_ms,
                    "nodes_before": transform_result.node_count_before,
                    "nodes_after": transform_result.node_count_after,
                }
                result.stages.transform = StageResult.PASS
            except Exception as e:
                result.stages.transform = StageResult.FAIL
                result.overall_result = StageResult.FAIL
                result.error_message = f"AST transformation failed: {e}"
                return result

            # Stage 4: Information Collection (replaces Type Checking)
            try:
                info_result = self.information_collector.collect_information(ast)
                result.type_check_issues = (
                    info_result.issues
                )  # Keep same field name for compatibility

                result.type_check_details = {
                    "is_valid": info_result.is_valid,
                    "error_count": 0,  # Information collector never produces errors
                    "warning_count": len(info_result.issues),
                    "nodes_analyzed": info_result.nodes_analyzed,
                    "type_check_time_ms": info_result.collection_time_ms,
                    "symbol_table_size": len(info_result.variables),
                }

                # Information collection always passes - never blocks pipeline
                result.stages.typecheck = StageResult.PASS

                # Store information result for security analysis
                result.information_result = info_result

            except Exception as e:
                result.stages.typecheck = StageResult.ERROR
                result.overall_result = StageResult.ERROR
                result.error_message = f"Information collection error: {e}"
                return result

            # Stage 5: Security Deep Analysis
            try:
                security_deep_result = self.security_deep_analyzer.analyze_deep(ast, info_result)
                result.security_deep_threats = security_deep_result.threats

                result.security_deep_details = {
                    "is_secure": security_deep_result.is_secure,
                    "total_threats": len(security_deep_result.threats),
                    "critical_threats": len(security_deep_result.critical_threats),
                    "high_threats": len(security_deep_result.high_threats),
                    "analysis_passes": security_deep_result.analysis_passes,
                    "analysis_time_ms": security_deep_result.analysis_time_ms,
                    "false_positive_rate": security_deep_result.false_positive_rate,
                }

                if security_deep_result.is_secure:
                    result.stages.security_deep = StageResult.PASS
                else:
                    result.stages.security_deep = StageResult.FAIL

            except Exception as e:
                result.stages.security_deep = StageResult.ERROR
                result.error_message = f"Security deep analysis error: {e}"
                # Don't return - continue with other stages

            # Stage 6: Optimization
            try:
                optimization_result = self.optimizer.optimize(ast, info_result)
                ast = optimization_result.optimized_ast  # Use optimized AST for subsequent stages

                result.optimization_results = optimization_result.optimizations_applied
                # Convert enum keys to strings for JSON serialization
                optimization_summary_str = {
                    str(opt_type): count
                    for opt_type, count in optimization_result.optimization_summary.items()
                }

                result.optimization_details = {
                    "optimizations_count": len(optimization_result.optimizations_applied),
                    "optimization_summary": optimization_summary_str,
                    "nodes_eliminated": optimization_result.nodes_eliminated,
                    "estimated_performance_gain": optimization_result.estimated_performance_gain,
                    "optimization_time_ms": optimization_result.optimization_time_ms,
                }

                result.stages.optimize = StageResult.PASS

            except Exception as e:
                result.stages.optimize = StageResult.FAIL
                result.error_message = f"Optimization failed: {e}"
                # Don't return - continue with other stages

            # Stage 7: Security Analysis (Original)
            try:
                security_result = self.security_analyzer.analyze_parallel(ml_source, file_path)

                threat_count = (
                    len(security_result.pattern_matches)
                    + len(security_result.ast_violations)
                    + len(security_result.data_flow_results.get("violations", []))
                )

                result.security_threats = threat_count
                result.security_details = {
                    "pattern_matches": len(security_result.pattern_matches),
                    "ast_violations": len(security_result.ast_violations),
                    "data_flow_violations": len(
                        security_result.data_flow_results.get("violations", [])
                    ),
                    "analysis_time_ms": security_result.analysis_time * 1000,
                }

                # Validate security results based on category
                # All remaining categories expect 0 threats
                if threat_count == 0:
                    result.stages.security = StageResult.PASS  # Correctly found no threats
                else:
                    result.stages.security = StageResult.FAIL  # False positive
                    result.error_message = (
                        f"Security false positive: {threat_count} threats in legitimate code"
                    )

            except Exception as e:
                result.stages.security = StageResult.ERROR
                result.error_message = f"Security analysis failed: {e}"

            # Stage 3: Code Generation (if should transpile)
            if category_config.get("should_transpile", True) and result.stages.security in [
                StageResult.PASS,
                StageResult.SKIP,
            ]:
                try:
                    # Prepare import paths for user modules
                    # Get the parent directory of the test file (e.g., tests/ml_integration/ml_module)
                    # This allows tests to import from user_modules subdirectory
                    import_paths = []
                    if file_path:
                        test_dir = Path(file_path).parent
                        import_paths.append(str(test_dir))

                    python_code, issues, source_map = self.transpiler.transpile_to_python(
                        ml_source,
                        source_file=file_path,
                        generate_source_maps=True,
                        import_paths=import_paths,
                        allow_current_dir=True,
                        module_output_mode='separate'  # Use separate .py files for user modules
                    )

                    result.transpilation_result = (python_code, issues, source_map)

                    if python_code and self._validate_generated_code(python_code):
                        result.stages.codegen = StageResult.PASS
                    else:
                        result.stages.codegen = StageResult.FAIL
                        result.error_message = "Code generation produced invalid or unsafe code"

                except Exception as e:
                    result.stages.codegen = StageResult.FAIL
                    result.error_message = f"Code generation failed: {e}"
            else:
                result.stages.codegen = StageResult.SKIP

            # Stage 4: Execution (if should execute and codegen passed)
            if (
                category_config.get("should_execute", True)
                and result.stages.codegen == StageResult.PASS
                and result.transpilation_result
            ):

                try:
                    python_code = result.transpilation_result[0]
                    exec_result = self._execute_in_sandbox(python_code)
                    result.execution_result = exec_result

                    if exec_result.get("success", False):
                        result.stages.execution = StageResult.PASS
                    else:
                        result.stages.execution = StageResult.FAIL
                        result.error_message = (
                            f"Execution failed: {exec_result.get('error', 'Unknown error')}"
                        )

                except Exception as e:
                    result.stages.execution = StageResult.ERROR
                    result.error_message = f"Execution stage error: {e}"
            else:
                result.stages.execution = StageResult.SKIP

            # Determine overall result
            stage_results = result.stages.get_stage_results()
            if any(s == StageResult.ERROR for s in stage_results):
                result.overall_result = StageResult.ERROR
            elif any(s == StageResult.FAIL for s in stage_results):
                result.overall_result = StageResult.FAIL
            elif any(s == StageResult.PASS for s in stage_results):
                result.overall_result = StageResult.PASS
            else:
                result.overall_result = StageResult.SKIP

        except Exception as e:
            result.overall_result = StageResult.ERROR
            result.error_message = f"Pipeline error: {e}"

        result.total_time_ms = (time.perf_counter() - start_time) * 1000
        return result

    def _validate_generated_code(self, python_code: str) -> bool:
        """Validate that generated Python code is safe."""
        if python_code is None:
            return False

        dangerous_patterns = [
            "eval(",
            "exec(",
            "__import__",
            "getattr(",
            "setattr(",
            "__class__.__bases__",
            "__subclasses__",
            "subprocess.",
            "os.system",
            "__builtin__",
        ]

        code_lower = python_code.lower()
        return not any(pattern.lower() in code_lower for pattern in dangerous_patterns)

    def _execute_in_sandbox(self, python_code: str) -> dict[str, Any]:
        """Execute Python code in sandbox with all stdlib capabilities."""
        try:
            config = SandboxConfig()

            # Import capability system components
            from mlpy.runtime.capabilities import get_capability_manager
            from mlpy.runtime.capabilities.tokens import CapabilityToken, CapabilityConstraint

            with MLSandbox(config) as sandbox:
                # Create capability context for testing
                manager = get_capability_manager()
                context = manager.create_context(name="test_execution")

                # Grant all standard library capabilities for testing
                test_capabilities = [
                    "console.write",
                    "console.error",
                    "regex.compile",
                    "regex.match",
                    "file.read",
                    "file.write",
                    "file.append",
                    "file.delete",
                    "path.read",
                    "path.write",
                    "network.http",
                    "network.https",
                    "network.socket",
                    "math.compute",
                    "random.generate",
                    "random.sample",
                    "json.parse",
                    "json.serialize",
                    "datetime.create",
                    "datetime.now",
                    "collections.read",
                    "collections.transform",
                    "functional.compose",
                    "functional.transform",
                    "env.read",
                    "env.write",
                    "crypto.hash",
                    "crypto.random",
                    "log.write",
                    "args.read",
                ]

                for cap_type in test_capabilities:
                    token = CapabilityToken(
                        capability_type=cap_type,
                        constraints=CapabilityConstraint(),  # No restrictions for testing
                        description=f"Test capability for {cap_type}",
                    )
                    context.add_capability(token)

                result = sandbox._execute_python_code(python_code, context)

            success = getattr(result, "success", False)
            return {
                "success": success,
                "result": result,
                "stdout": getattr(result, "stdout", ""),
                "stderr": getattr(result, "stderr", ""),
                "error": str(getattr(result, "error", "")) if not success else None,
                "exit_code": getattr(result, "exit_code", 0),
                "execution_time": getattr(result, "execution_time", 0.0),
            }

        except Exception as e:
            return {"success": False, "error": str(e), "exception_type": type(e).__name__}

    def print_result_matrix(self, results: list[TestFileResult], show_details: bool = False):
        """Print a comprehensive result matrix."""
        if not results:
            print("No results to display.")
            return

        # Headers
        stage_headers = [
            "Parse",
            "AST",
            "AST_V",
            "Trans",
            "Type",
            "Sec_D",
            "Opt",
            "Security",
            "CodeGen",
            "Exec",
        ]

        print("\n" + "=" * 120)
        print("ML PIPELINE RESULT MATRIX")
        print("=" * 120)

        # Print header
        print(
            f"{'File':<40} {'Cat':<12} {'Overall':<8} {' '.join(f'{h:>8}' for h in stage_headers)} {'Time(ms)':<8} {'Lines':<6}"
        )
        print("-" * 120)

        # Group by category for better organization
        categories = {}
        for result in results:
            if result.category not in categories:
                categories[result.category] = []
            categories[result.category].append(result)

        # Print results by category
        for category, cat_results in categories.items():
            print(f"\n[{category.upper()}]")

            for result in cat_results:
                file_name = (
                    result.file_name[:38] if len(result.file_name) > 38 else result.file_name
                )
                stages = result.stages.get_stage_results()
                stage_str = " ".join(f"{s.value:>8}" for s in stages)

                print(
                    f"{file_name:<40} {result.category[:10]:<12} {result.overall_result.value:<8} "
                    f"{stage_str} {result.total_time_ms:>7.1f} {result.line_count:>6}"
                )

                if show_details and result.error_message:
                    print(f"    └─ {result.error_message}")

                # Show execution-specific details if available
                if show_details and hasattr(result, "execution_result") and result.execution_result:
                    exec_result = result.execution_result
                    if not exec_result.get("success", False):
                        error_details = []
                        if exec_result.get("error"):
                            error_details.append(f"Error: {exec_result['error']}")
                        if exec_result.get("stderr"):
                            error_details.append(f"Stderr: {exec_result['stderr']}")
                        if exec_result.get("exit_code", 0) != 0:
                            error_details.append(f"Exit code: {exec_result['exit_code']}")
                        if exec_result.get("execution_time", 0) > 0:
                            error_details.append(f"Time: {exec_result['execution_time']:.3f}s")

                        if error_details:
                            print(f"    └─ Execution details: {' | '.join(error_details)}")

                if show_details and result.security_threats > 0:
                    print(f"    └─ Security: {result.security_threats} threats detected")

        # Summary statistics
        print("\n" + "=" * 120)
        self.print_summary_stats(results)

    def print_summary_stats(self, results: list[TestFileResult]):
        """Print summary statistics."""
        if not results:
            return

        total = len(results)
        by_overall = {
            StageResult.PASS: len([r for r in results if r.overall_result == StageResult.PASS]),
            StageResult.FAIL: len([r for r in results if r.overall_result == StageResult.FAIL]),
            StageResult.ERROR: len([r for r in results if r.overall_result == StageResult.ERROR]),
            StageResult.SKIP: len([r for r in results if r.overall_result == StageResult.SKIP]),
        }

        # Stage-by-stage statistics
        stage_names = [
            "parse",
            "ast",
            "ast_valid",
            "transform",
            "typecheck",
            "security_deep",
            "optimize",
            "security",
            "codegen",
            "execution",
        ]
        stage_stats = {}

        for i, stage_name in enumerate(stage_names):
            stage_results = [r.stages.get_stage_results()[i] for r in results]
            stage_stats[stage_name] = {
                StageResult.PASS: len([s for s in stage_results if s == StageResult.PASS]),
                StageResult.FAIL: len([s for s in stage_results if s == StageResult.FAIL]),
                StageResult.ERROR: len([s for s in stage_results if s == StageResult.ERROR]),
                StageResult.SKIP: len([s for s in stage_results if s == StageResult.SKIP]),
            }

        print("SUMMARY STATISTICS")
        print(f"Total Files: {total}")
        print(
            f"Overall Results: Pass={by_overall[StageResult.PASS]} ({by_overall[StageResult.PASS]/total*100:.1f}%), "
            f"Fail={by_overall[StageResult.FAIL]} ({by_overall[StageResult.FAIL]/total*100:.1f}%), "
            f"Error={by_overall[StageResult.ERROR]} ({by_overall[StageResult.ERROR]/total*100:.1f}%)"
        )

        print("\nStage Success Rates:")
        for stage_name in stage_names:
            stats = stage_stats[stage_name]
            success_rate = stats[StageResult.PASS] / total * 100 if total > 0 else 0
            print(
                f"  {stage_name.capitalize():<10}: {stats[StageResult.PASS]:>3}/{total} ({success_rate:>5.1f}%)"
            )

        # Performance stats
        total_time = sum(r.total_time_ms for r in results)
        avg_time = total_time / total if total > 0 else 0
        total_lines = sum(r.line_count for r in results)

        print("\nPerformance:")
        print(f"  Total Time: {total_time:.1f}ms")
        print(f"  Average Time: {avg_time:.1f}ms per file")
        print(f"  Total Lines: {total_lines:,}")

    def save_results(self, results: list[TestFileResult], filename: str = "ml_test_results.json"):
        """Save detailed results to JSON file."""
        serializable_results = []
        for result in results:
            # Build result dictionary manually to avoid AST node serialization issues
            result_dict = {
                "file_path": result.file_path,
                "file_name": result.file_name,
                "category": result.category,
                "line_count": result.line_count,
                "char_count": result.char_count,
                "total_time_ms": result.total_time_ms,
                "overall_result": result.overall_result.value,
                "error_message": result.error_message,
                "parse_error": result.parse_error,
                "ast_validation_issues": result.ast_validation_issues or [],
                "transform_details": result.transform_details or {},
                "type_check_issues": result.type_check_issues or [],
                "type_check_details": result.type_check_details or {},
                "security_threats": result.security_threats,
                "security_details": result.security_details or {},
                "transpilation_result": result.transpilation_result,
                "execution_result": result.execution_result,
            }

            # Handle stages
            stage_names = [
                "parse",
                "ast",
                "ast_valid",
                "transform",
                "typecheck",
                "security_deep",
                "optimize",
                "security",
                "codegen",
                "execution",
            ]
            stage_results = result.stages.get_stage_results()
            stages_dict = {}
            for name, stage_result in zip(stage_names, stage_results, strict=False):
                stages_dict[name] = stage_result.value
            result_dict["stages"] = stages_dict

            # Handle information_result serialization
            if result.information_result is not None:
                result_dict["information_result"] = result.information_result.to_dict()

            # Handle security_deep_threats serialization
            if hasattr(result, "security_deep_threats") and result.security_deep_threats:
                result_dict["security_deep_threats"] = [
                    threat.to_dict() for threat in result.security_deep_threats
                ]

            # Handle security_deep_details serialization
            if result.security_deep_details:
                result_dict["security_deep_details"] = result.security_deep_details

            # Handle optimization_results and optimization_details (if they contain problematic objects)
            if result.optimization_results:
                result_dict["optimization_results"] = str(
                    result.optimization_results
                )  # Convert to string
            if result.optimization_details:
                # Convert optimization details to safe format
                try:
                    result_dict["optimization_details"] = {
                        k: str(v) for k, v in result.optimization_details.items()
                    }
                except:
                    result_dict["optimization_details"] = str(result.optimization_details)

            serializable_results.append(result_dict)

        with open(filename, "w", encoding="utf-8") as f:
            try:
                json.dump(
                    {
                        "timestamp": time.time(),
                        "total_files": len(results),
                        "results": serializable_results,
                    },
                    f,
                    indent=2,
                )
            except TypeError as e:
                # Fallback: save basic results only
                basic_results = []
                for result in serializable_results:
                    basic_result = {
                        "file_path": result["file_path"],
                        "file_name": result["file_name"],
                        "category": result["category"],
                        "stages": result["stages"],
                        "overall_result": result["overall_result"],
                        "total_time_ms": result["total_time_ms"],
                    }
                    basic_results.append(basic_result)

                json.dump(
                    {
                        "timestamp": time.time(),
                        "total_files": len(results),
                        "results": basic_results,
                        "note": f"Full serialization failed: {str(e)}",
                    },
                    f,
                    indent=2,
                )

        print(f"\nDetailed results saved to: {filename}")

    def print_failures_only(self, results: list[TestFileResult]):
        """Print only failed files with detailed error information."""
        failed_results = [
            r for r in results if r.overall_result in [StageResult.FAIL, StageResult.ERROR]
        ]

        if not failed_results:
            print("🎉 No failures found! All tests passed.")
            return

        print(f"\n{'='*80}")
        print(f"FAILURE ANALYSIS - {len(failed_results)} Failed Files")
        print(f"{'='*80}")

        for i, result in enumerate(failed_results, 1):
            print(f"\n[{i}] {result.file_name} ({result.category})")
            print(f"    Overall Result: {result.overall_result.value}")
            print(f"    Total Time: {result.total_time_ms:.1f}ms")

            # Show stage results
            stages = result.stages.get_stage_results()
            stage_names = [
                "parse",
                "ast",
                "ast_valid",
                "transform",
                "typecheck",
                "security_deep",
                "optimize",
                "security",
                "codegen",
                "execution",
            ]
            failed_stages = []

            for stage_name, stage_result in zip(stage_names, stages, strict=False):
                if stage_result in [StageResult.FAIL, StageResult.ERROR]:
                    failed_stages.append(f"{stage_name}({stage_result.value})")

            if failed_stages:
                print(f"    Failed Stages: {', '.join(failed_stages)}")

            # Show error message
            if result.error_message:
                print(f"    Error: {result.error_message}")

            # Show execution details if available
            if hasattr(result, "execution_result") and result.execution_result:
                exec_result = result.execution_result
                if not exec_result.get("success", False):
                    print("    Execution Details:")
                    if exec_result.get("error"):
                        print(f"      • Error: {exec_result['error']}")
                    if exec_result.get("stderr"):
                        print(f"      • Stderr: {exec_result['stderr']}")
                    if exec_result.get("exit_code", 0) != 0:
                        print(f"      • Exit Code: {exec_result['exit_code']}")
                    if exec_result.get("execution_time", 0) > 0:
                        print(f"      • Execution Time: {exec_result['execution_time']:.3f}s")

            # Show security threats if any
            if result.security_threats > 0:
                print(f"    Security Threats: {result.security_threats} detected")

            print(f"    File Path: {result.file_path}")


def create_cli_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Unified ML Test Runner - Complete Pipeline Testing and Validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
        Examples:
          %(prog)s --parse                    # Parse validation only
          %(prog)s --full                     # Complete pipeline testing
          %(prog)s --full --matrix            # Show detailed result matrix
          %(prog)s --full --matrix --details  # Include error details in matrix
          %(prog)s --full --show-failures     # Show only failed files with detailed errors
          %(prog)s --parse --dir tests/custom # Test custom directory

        Pipeline Stages:
          Parse     - ML source parsing and AST generation
          AST       - AST creation and basic structure
          AST_V     - AST validation and integrity checking
          Trans     - AST transformation and normalization
          Type      - Static type checking and inference
          Sec_D     - Enhanced security analysis with type awareness
          Opt       - Code optimization and performance enhancement
          Security  - Original security analysis and threat detection
          CodeGen   - Python code generation
          Exec      - Sandboxed execution testing

        Result Matrix Legend:
          + = Pass    X = Fail    E = Error    - = Skipped
        """
        ),
    )

    # Main mode options (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--parse", action="store_true", help="Run parsing validation only (fast)"
    )
    mode_group.add_argument(
        "--full",
        action="store_true",
        help="Run complete pipeline testing (parse → security → codegen → execution)",
    )

    # Output options
    parser.add_argument(
        "--matrix",
        action="store_true",
        help="Show result matrix (works with both --parse and --full)",
    )
    parser.add_argument(
        "--details", action="store_true", help="Include error details in matrix output"
    )
    parser.add_argument(
        "--show-failures",
        action="store_true",
        help="Show only failed files with detailed error information",
    )

    # Input options
    parser.add_argument("--dir", type=str, help="Test directory (default: tests/ml_integration)")
    parser.add_argument("--output", type=str, help="Output file for detailed results (JSON format)")

    # Filter options
    parser.add_argument(
        "--category",
        type=str,
        choices=["ml_core", "ml_builtin", "ml_stdlib", "ml_module"],
        help="Run tests only for specific category",
    )

    return parser


def main():
    """Main CLI entry point."""
    parser = create_cli_parser()
    args = parser.parse_args()

    # Initialize test runner
    runner = UnifiedMLTestRunner(test_directory=args.dir)

    print("=" * 80)
    print("UNIFIED ML TEST RUNNER")
    print("=" * 80)

    # Discover test files
    test_files = runner.discover_test_files()

    if not test_files:
        print(f"No ML test files found in directory: {runner.test_directory}")
        return 1

    # Filter by category if specified
    if args.category:
        test_files = [f for f in test_files if args.category in str(Path(f).parent)]
        print(f"Filtered to {args.category} category: {len(test_files)} files")

    print(f"Discovered {len(test_files)} ML test files")
    print(f"Mode: {'Parsing only' if args.parse else 'Full pipeline'}")

    # Run tests
    results = []

    print("\nRunning tests...")
    for i, file_path in enumerate(test_files, 1):
        print(f"  [{i:2d}/{len(test_files)}] {Path(file_path).name}")

        if args.parse:
            result = runner.run_parse_only(file_path)
        else:
            result = runner.run_full_pipeline(file_path)

        results.append(result)

    # Display results
    if args.show_failures:
        runner.print_failures_only(results)
    elif args.matrix:
        runner.print_result_matrix(results, show_details=args.details)
    else:
        runner.print_summary_stats(results)

    # Save detailed results
    output_file = args.output or ("ml_parse_results.json" if args.parse else "ml_full_results.json")
    runner.save_results(results, output_file)

    # Return appropriate exit code
    success_rate = len([r for r in results if r.overall_result == StageResult.PASS]) / len(results)
    return 0 if success_rate >= 0.90 else 1


if __name__ == "__main__":
    sys.exit(main())
