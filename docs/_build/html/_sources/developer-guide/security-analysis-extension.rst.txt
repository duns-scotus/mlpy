============================
Security Analysis Extension
============================

This guide covers extending mlpy's security analysis system to detect new threats, add custom security rules, and integrate domain-specific security patterns. The security analyzer is designed for extensibility while maintaining high performance and accuracy.

Security Analysis Architecture
==============================

The security analysis system uses a multi-layered approach:

.. code-block:: text

    ┌─────────────────────┐    ┌─────────────────────┐
    │   Pattern-Based     │    │   Data Flow         │
    │   Detection         │◄──►│   Analysis          │
    └─────────────────────┘    └─────────────────────┘
             │                          │
             ▼                          ▼
    ┌─────────────────────┐    ┌─────────────────────┐
    │   AST Traversal     │◄──►│   Parallel          │
    │   Analysis          │    │   Processing        │
    └─────────────────────┘    └─────────────────────┘

Core Extension Points
====================

**File**: ``src/mlpy/ml/analysis/security_analyzer.py``

The SecurityAnalyzer class provides several extension mechanisms:

1. **Custom Visitor Methods** - Add new AST node analysis
2. **Pattern Detection Rules** - Define threat patterns
3. **Data Flow Tracking** - Track tainted data propagation
4. **Capability Validation** - Custom capability checks
5. **CWE Classification** - Map threats to security standards

Adding Custom Security Rules
============================

Example: Adding SQL Injection Detection
---------------------------------------

.. code-block:: python

    class CustomSecurityAnalyzer(SecurityAnalyzer):
        """Extended security analyzer with custom rules."""

        def __init__(self, source_file: str | None = None):
            super().__init__(source_file)

            # Add SQL-specific dangerous patterns
            self.sql_injection_patterns = {
                r"SELECT\s+\*\s+FROM\s+\w+\s+WHERE\s+.*=.*",
                r"INSERT\s+INTO\s+\w+.*VALUES.*",
                r"UPDATE\s+\w+\s+SET\s+.*=.*WHERE.*",
                r"DELETE\s+FROM\s+\w+\s+WHERE.*",
                r"DROP\s+TABLE\s+\w+",
                r"UNION\s+SELECT.*",
                r"OR\s+1\s*=\s*1",
                r"AND\s+1\s*=\s*1"
            }

            # Track SQL-related functions
            self.sql_functions = {
                "executeQuery", "rawQuery", "exec", "query"
            }

        def visit_function_call(self, node: FunctionCall):
            """Enhanced function call analysis with SQL injection detection."""

            # Call parent analysis first
            super().visit_function_call(node)

            # Check for SQL injection vulnerabilities
            if node.function in self.sql_functions:
                self.analyze_sql_injection_risk(node)

            # Check for dynamic query construction
            if self.is_dynamic_query_construction(node):
                self.analyze_dynamic_query_risk(node)

        def analyze_sql_injection_risk(self, node: FunctionCall):
            """Analyze SQL injection risk in database queries."""

            if not node.arguments:
                return

            query_arg = node.arguments[0]

            # Check for string concatenation in queries
            if isinstance(query_arg, BinaryExpression) and query_arg.operator == "+":
                if self.contains_user_input(query_arg):
                    self._add_issue(
                        severity="critical",
                        category="sql_injection",
                        message="Potential SQL injection via string concatenation",
                        node=node,
                        context={
                            "function": node.function,
                            "vulnerability_type": "string_concatenation",
                            "cwe": "CWE-89"
                        }
                    )

            # Check for template literals with variables
            if isinstance(query_arg, TemplateLiteral):
                if self.has_unvalidated_variables(query_arg):
                    self._add_issue(
                        severity="high",
                        category="sql_injection",
                        message="SQL query uses unvalidated template variables",
                        node=node,
                        context={
                            "vulnerability_type": "template_injection",
                            "variables": self.extract_template_variables(query_arg)
                        }
                    )

            # Pattern-based detection
            if isinstance(query_arg, StringLiteral):
                for pattern in self.sql_injection_patterns:
                    if re.search(pattern, query_arg.value, re.IGNORECASE):
                        self._add_issue(
                            severity="medium",
                            category="suspicious_sql",
                            message=f"SQL query matches injection pattern: {pattern}",
                            node=node,
                            context={"pattern": pattern}
                        )

        def contains_user_input(self, expr: Expression) -> bool:
            """Check if expression contains potentially unsafe user input."""

            user_input_sources = {
                "request.params", "request.query", "request.body",
                "process.argv", "process.env", "window.location",
                "document.cookie", "localStorage", "sessionStorage"
            }

            if isinstance(expr, MemberAccess):
                full_path = self.get_member_access_path(expr)
                return any(source in full_path for source in user_input_sources)

            elif isinstance(expr, BinaryExpression):
                return (self.contains_user_input(expr.left) or
                       self.contains_user_input(expr.right))

            return False

Advanced Pattern Detection
==========================

Creating Domain-Specific Security Rules
---------------------------------------

.. code-block:: python

    class CryptographySecurityAnalyzer(SecurityAnalyzer):
        """Security analyzer for cryptographic operations."""

        def __init__(self, source_file: str | None = None):
            super().__init__(source_file)

            self.weak_algorithms = {
                "md5", "sha1", "des", "3des", "rc4"
            }

            self.deprecated_functions = {
                "crypto.createHash": {"md5", "sha1"},
                "crypto.createCipher": {"des", "3des", "rc4"}
            }

            self.minimum_key_sizes = {
                "rsa": 2048,
                "ecdsa": 256,
                "aes": 128
            }

        def visit_function_call(self, node: FunctionCall):
            """Analyze cryptographic function calls."""

            super().visit_function_call(node)

            # Check for weak cryptographic algorithms
            if self.is_crypto_function(node.function):
                self.analyze_crypto_strength(node)

            # Check for hardcoded cryptographic keys
            if self.is_key_function(node.function):
                self.analyze_key_security(node)

        def analyze_crypto_strength(self, node: FunctionCall):
            """Analyze cryptographic algorithm strength."""

            if not node.arguments:
                return

            algorithm_arg = node.arguments[0]

            if isinstance(algorithm_arg, StringLiteral):
                algorithm = algorithm_arg.value.lower()

                if algorithm in self.weak_algorithms:
                    self._add_issue(
                        severity="high",
                        category="weak_cryptography",
                        message=f"Use of weak cryptographic algorithm: {algorithm}",
                        node=node,
                        context={
                            "algorithm": algorithm,
                            "cwe": "CWE-327",
                            "recommendation": "Use SHA-256 or stronger algorithms"
                        }
                    )

        def analyze_key_security(self, node: FunctionCall):
            """Analyze cryptographic key security."""

            for arg in node.arguments:
                if isinstance(arg, StringLiteral):
                    # Check for hardcoded keys
                    if self.looks_like_crypto_key(arg.value):
                        self._add_issue(
                            severity="critical",
                            category="hardcoded_key",
                            message="Hardcoded cryptographic key detected",
                            node=node,
                            context={
                                "key_length": len(arg.value),
                                "cwe": "CWE-798"
                            }
                        )

                # Check key length for generated keys
                if isinstance(arg, NumberLiteral):
                    key_size = int(arg.value)
                    if key_size < self.minimum_key_sizes.get("default", 128):
                        self._add_issue(
                            severity="medium",
                            category="weak_key_size",
                            message=f"Cryptographic key size too small: {key_size} bits",
                            node=node,
                            context={"key_size": key_size}
                        )

Data Flow Security Analysis
===========================

Tracking Tainted Data Flow
--------------------------

.. code-block:: python

    class TaintAnalyzer(SecurityAnalyzer):
        """Advanced taint analysis for data flow security."""

        def __init__(self, source_file: str | None = None):
            super().__init__(source_file)

            self.taint_sources = {
                # Network sources
                "http.request", "fetch", "axios.get", "request",
                # File system sources
                "fs.readFile", "fs.readFileSync", "readFile",
                # User input sources
                "prompt", "readline", "process.stdin",
                # Environment sources
                "process.env", "os.environ", "getenv"
            }

            self.taint_sinks = {
                # Code execution sinks
                "eval", "exec", "Function", "vm.runInThisContext",
                # File system sinks
                "fs.writeFile", "fs.writeFileSync", "writeFile",
                # Database sinks
                "db.query", "executeQuery", "db.exec",
                # Command execution sinks
                "child_process.exec", "spawn", "system"
            }

            self.sanitizers = {
                "escape", "sanitize", "validate", "htmlEscape",
                "sqlEscape", "shellEscape", "JSON.stringify"
            }

            # Track tainted variables
            self.tainted_vars: set[str] = set()
            self.sanitized_vars: set[str] = set()

        def visit_assignment_statement(self, node: AssignmentStatement):
            """Track taint propagation through assignments."""

            super().visit_assignment_statement(node)

            if isinstance(node.target, Identifier):
                target_name = node.target.name

                # Check if assigned value is tainted
                if self.is_tainted_expression(node.value):
                    self.tainted_vars.add(target_name)

                    # Check if value goes through sanitizer
                    if self.is_sanitized_expression(node.value):
                        self.sanitized_vars.add(target_name)
                else:
                    # Remove from tainted set if assigned clean value
                    self.tainted_vars.discard(target_name)
                    self.sanitized_vars.discard(target_name)

        def visit_function_call(self, node: FunctionCall):
            """Analyze function calls for taint sources and sinks."""

            super().visit_function_call(node)

            # Check for taint sinks with tainted arguments
            if self.is_taint_sink(node.function):
                for arg in node.arguments:
                    if self.is_tainted_expression(arg):
                        # Check if argument was sanitized
                        if not self.is_sanitized_expression(arg):
                            self._add_issue(
                                severity="critical",
                                category="taint_flow",
                                message=f"Tainted data flows to dangerous sink: {node.function}",
                                node=node,
                                context={
                                    "sink": node.function,
                                    "taint_source": self.get_taint_source(arg),
                                    "cwe": "CWE-20"
                                }
                            )

        def is_tainted_expression(self, expr: Expression) -> bool:
            """Check if expression contains tainted data."""

            if isinstance(expr, Identifier):
                return expr.name in self.tainted_vars

            elif isinstance(expr, FunctionCall):
                return self.is_taint_source(expr.function)

            elif isinstance(expr, BinaryExpression):
                return (self.is_tainted_expression(expr.left) or
                       self.is_tainted_expression(expr.right))

            elif isinstance(expr, MemberAccess):
                path = self.get_member_access_path(expr)
                return any(source in path for source in self.taint_sources)

            return False

Performance Optimization for Security Analysis
==============================================

Parallel Security Analysis
--------------------------

.. code-block:: python

    class ParallelSecurityAnalyzer:
        """High-performance parallel security analysis."""

        def __init__(self, max_workers: int = 4):
            self.max_workers = max_workers
            self.analyzers = {
                'core': SecurityAnalyzer,
                'sql': SQLInjectionAnalyzer,
                'xss': XSSAnalyzer,
                'crypto': CryptographyAnalyzer,
                'taint': TaintAnalyzer
            }

        def analyze_parallel(self, ast_node: Program, source_file: str = None) -> list[SecurityIssue]:
            """Run multiple security analyzers in parallel."""

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit analysis tasks
                futures = {}
                for name, analyzer_class in self.analyzers.items():
                    analyzer = analyzer_class(source_file)
                    future = executor.submit(analyzer.analyze, ast_node)
                    futures[name] = future

                # Collect results
                all_issues = []
                for name, future in futures.items():
                    try:
                        issues = future.result(timeout=30)
                        all_issues.extend(issues)
                    except TimeoutError:
                        logger.warning(f"Security analyzer '{name}' timed out")
                    except Exception as e:
                        logger.error(f"Security analyzer '{name}' failed: {e}")

                return self.deduplicate_issues(all_issues)

        def deduplicate_issues(self, issues: list[SecurityIssue]) -> list[SecurityIssue]:
            """Remove duplicate security issues."""

            seen = set()
            unique_issues = []

            for issue in issues:
                # Create hash based on location and type
                issue_hash = (issue.line, issue.column, issue.category, issue.message)

                if issue_hash not in seen:
                    seen.add(issue_hash)
                    unique_issues.append(issue)

            return unique_issues

Custom Security Metrics
=======================

Security Score Calculation
--------------------------

.. code-block:: python

    class SecurityMetricsCalculator:
        """Calculate security metrics for code analysis."""

        def __init__(self):
            self.severity_weights = {
                'critical': 10.0,
                'high': 7.0,
                'medium': 4.0,
                'low': 1.0
            }

            self.category_multipliers = {
                'code_injection': 2.0,
                'sql_injection': 1.8,
                'xss': 1.5,
                'hardcoded_secrets': 1.7,
                'weak_cryptography': 1.4
            }

        def calculate_security_score(self, issues: list[SecurityIssue]) -> SecurityScore:
            """Calculate overall security score."""

            if not issues:
                return SecurityScore(
                    score=100.0,
                    grade='A+',
                    risk_level='MINIMAL',
                    total_issues=0
                )

            # Calculate weighted severity score
            total_weight = 0.0
            category_counts = {}

            for issue in issues:
                base_weight = self.severity_weights.get(issue.severity, 1.0)
                multiplier = self.category_multipliers.get(issue.category, 1.0)

                total_weight += base_weight * multiplier
                category_counts[issue.category] = category_counts.get(issue.category, 0) + 1

            # Normalize score (100 = perfect, 0 = critical issues)
            max_possible_weight = len(issues) * max(self.severity_weights.values())
            normalized_weight = min(total_weight / max_possible_weight * 100, 100)

            security_score = max(0, 100 - normalized_weight)

            return SecurityScore(
                score=security_score,
                grade=self.calculate_grade(security_score),
                risk_level=self.calculate_risk_level(security_score),
                total_issues=len(issues),
                severity_breakdown=self.calculate_severity_breakdown(issues),
                category_breakdown=category_counts,
                recommendations=self.generate_recommendations(issues)
            )

Integration with IDE and CI/CD
==============================

Real-time Security Analysis
---------------------------

.. code-block:: python

    class RealtimeSecurityAnalyzer:
        """Real-time security analysis for IDE integration."""

        def __init__(self):
            self.analyzer_cache = {}
            self.analysis_debouncer = Debouncer(delay=0.5)

        def analyze_incremental(self,
                               source_code: str,
                               changed_lines: set[int]) -> IncrementalAnalysisResult:
            """Perform incremental security analysis on changed code."""

            # Parse only changed sections when possible
            if self.can_parse_incrementally(changed_lines):
                ast_changes = self.parse_incremental(source_code, changed_lines)
                issues = self.analyze_ast_changes(ast_changes)
            else:
                # Fall back to full analysis
                issues = self.analyze_full(source_code)

            return IncrementalAnalysisResult(
                issues=issues,
                analysis_type='incremental' if self.can_parse_incrementally(changed_lines) else 'full',
                performance_metrics=self.get_performance_metrics()
            )

        @self.analysis_debouncer
        def analyze_on_change(self, source_code: str, file_path: str):
            """Debounced analysis for real-time feedback."""

            try:
                result = self.analyze_incremental(source_code, set())
                self.notify_ide(file_path, result.issues)
            except Exception as e:
                logger.error(f"Real-time analysis failed: {e}")

CI/CD Integration
----------------

.. code-block:: python

    class CICDSecurityGate:
        """Security gate for CI/CD pipelines."""

        def __init__(self, config: SecurityGateConfig):
            self.config = config
            self.analyzer = ParallelSecurityAnalyzer()

        def validate_security_gate(self, source_files: list[str]) -> SecurityGateResult:
            """Validate code against security gate criteria."""

            all_issues = []

            for file_path in source_files:
                with open(file_path, 'r') as f:
                    source_code = f.read()

                issues = self.analyzer.analyze_code(source_code, file_path)
                all_issues.extend(issues)

            # Apply gate criteria
            gate_result = self.apply_gate_criteria(all_issues)

            # Generate report
            report = self.generate_security_report(all_issues, gate_result)

            return SecurityGateResult(
                passed=gate_result.passed,
                issues=all_issues,
                report=report,
                metrics=gate_result.metrics
            )

        def apply_gate_criteria(self, issues: list[SecurityIssue]) -> GateResult:
            """Apply security gate pass/fail criteria."""

            critical_count = sum(1 for issue in issues if issue.severity == 'critical')
            high_count = sum(1 for issue in issues if issue.severity == 'high')

            # Gate criteria
            if critical_count > self.config.max_critical_issues:
                return GateResult(passed=False, reason=f"Too many critical issues: {critical_count}")

            if high_count > self.config.max_high_issues:
                return GateResult(passed=False, reason=f"Too many high severity issues: {high_count}")

            # Calculate security score
            metrics = SecurityMetricsCalculator().calculate_security_score(issues)
            if metrics.score < self.config.minimum_security_score:
                return GateResult(passed=False, reason=f"Security score below threshold: {metrics.score}")

            return GateResult(passed=True, reason="All security criteria met")

This comprehensive security analysis extension guide provides the tools and patterns needed to build sophisticated, domain-specific security analyzers while maintaining high performance and integration capabilities.