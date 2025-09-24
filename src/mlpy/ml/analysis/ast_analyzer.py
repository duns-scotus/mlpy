"""Comprehensive AST security analyzer for ML code."""

import ast
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from .pattern_detector import AdvancedPatternDetector, PatternMatch, ThreatLevel

# Import from the correct location
try:
    from ..errors import SecurityError, SecurityWarning
except ImportError:
    # Fallback for missing SecurityError/SecurityWarning classes
    from ..errors.exceptions import MLSecurityError as SecurityError

    SecurityWarning = SecurityError


@dataclass
class SecurityViolation:
    """Security violation detected in AST analysis."""

    severity: ThreatLevel
    message: str
    location: dict[str, Any]
    cwe_id: str | None = None
    recommendation: str | None = None
    context: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DataFlowNode:
    """Represents a node in data flow analysis."""

    node: ast.AST
    variable_name: str
    value_source: str | None = None
    is_tainted: bool = False
    taint_source: str | None = None
    line_number: int = 0


@dataclass
class SecurityContext:
    """Security analysis context."""

    filename: str | None = None
    function_stack: list[str] = field(default_factory=list)
    class_stack: list[str] = field(default_factory=list)
    imports: set[str] = field(default_factory=set)
    dangerous_imports: set[str] = field(default_factory=set)
    capability_requirements: set[str] = field(default_factory=set)
    tainted_variables: dict[str, DataFlowNode] = field(default_factory=dict)


class ASTSecurityAnalyzer(ast.NodeVisitor):
    """Comprehensive AST security analyzer."""

    def __init__(self, pattern_detector: AdvancedPatternDetector | None = None):
        """Initialize the AST analyzer."""
        self.pattern_detector = pattern_detector or AdvancedPatternDetector()
        self.violations: list[SecurityViolation] = []
        self.context = SecurityContext()

        # Dangerous functions and modules
        self.dangerous_functions = {
            "eval",
            "exec",
            "compile",
            "__import__",
            "getattr",
            "setattr",
            "delattr",
            "hasattr",
            "vars",
            "globals",
            "locals",
            "dir",
        }

        self.dangerous_modules = {
            "os",
            "subprocess",
            "sys",
            "importlib",
            "pickle",
            "marshal",
            "dill",
            "shelve",
            "socket",
            "urllib",
            "requests",
            "http",
            "ctypes",
            "platform",
            "tempfile",
        }

        self.file_operations = {"open", "file", "input", "raw_input"}

        # Track data flow
        self.variable_definitions: dict[str, DataFlowNode] = {}
        self.function_calls: list[tuple[str, ast.Call]] = []

    def analyze(
        self, tree: ast.AST, source_code: str = "", filename: str | None = None
    ) -> list[SecurityViolation]:
        """Analyze AST for security violations."""
        self.violations = []
        self.context = SecurityContext(filename=filename)

        # Store source code for context extraction
        self.source_lines = source_code.split("\n") if source_code else []

        # Perform AST analysis
        self.visit(tree)

        # Perform pattern-based analysis
        pattern_matches = self.pattern_detector.scan_ast(tree, source_code, filename)

        # Convert pattern matches to violations
        for match in pattern_matches:
            violation = self._pattern_match_to_violation(match)
            self.violations.append(violation)

        # Perform data flow analysis
        self._analyze_data_flows()

        # Sort violations by severity and location
        self.violations.sort(
            key=lambda v: (self._severity_priority(v.severity), v.location.get("line", 0))
        )

        return self.violations

    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statements."""
        for alias in node.names:
            module_name = alias.name
            self.context.imports.add(module_name)

            # Check for dangerous imports
            if module_name in self.dangerous_modules:
                self.context.dangerous_imports.add(module_name)

                violation = SecurityViolation(
                    severity=ThreatLevel.HIGH,
                    message=f"Import of potentially dangerous module: {module_name}",
                    location=self._get_location(node),
                    cwe_id="CWE-494",
                    recommendation=f"Use capability tokens to control {module_name} access",
                    context=self._get_context(node),
                    metadata={"module": module_name, "import_type": "direct"},
                )
                self.violations.append(violation)

                # Add capability requirements
                if module_name in ["os", "subprocess"]:
                    self.context.capability_requirements.add("system_access")
                elif module_name in ["socket", "urllib", "requests", "http"]:
                    self.context.capability_requirements.add("network_access")
                elif module_name == "open" or "file" in module_name:
                    self.context.capability_requirements.add("file_access")

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit from-import statements."""
        if node.module:
            self.context.imports.add(node.module)

            if node.module in self.dangerous_modules:
                self.context.dangerous_imports.add(node.module)

                # Get specific imported names
                imported_names = [alias.name for alias in node.names]

                violation = SecurityViolation(
                    severity=ThreatLevel.HIGH,
                    message=f"Import from potentially dangerous module: {node.module}",
                    location=self._get_location(node),
                    cwe_id="CWE-494",
                    recommendation=f"Use capability tokens to control {node.module} access",
                    context=self._get_context(node),
                    metadata={
                        "module": node.module,
                        "imported_names": imported_names,
                        "import_type": "from",
                    },
                )
                self.violations.append(violation)

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Visit function calls."""
        func_name = self._get_function_name(node.func)

        # Track all function calls for data flow analysis
        self.function_calls.append((func_name, node))

        # Check for dangerous function calls
        if func_name in self.dangerous_functions:
            severity = ThreatLevel.CRITICAL if func_name in ["eval", "exec"] else ThreatLevel.HIGH

            violation = SecurityViolation(
                severity=severity,
                message=f"Dangerous function call: {func_name}",
                location=self._get_location(node),
                cwe_id=self._get_cwe_for_function(func_name),
                recommendation=self._get_recommendation_for_function(func_name),
                context=self._get_context(node),
                metadata={"function": func_name, "args_count": len(node.args)},
            )
            self.violations.append(violation)

        # Check for file operations
        elif func_name in self.file_operations:
            self.context.capability_requirements.add("file_access")

            # Check if file path is dynamic or potentially dangerous
            if node.args:
                first_arg = node.args[0]
                if self._is_dynamic_value(first_arg):
                    violation = SecurityViolation(
                        severity=ThreatLevel.MEDIUM,
                        message=f"Dynamic file path in {func_name} call",
                        location=self._get_location(node),
                        cwe_id="CWE-22",
                        recommendation="Validate and sanitize file paths, use capability tokens",
                        context=self._get_context(node),
                        metadata={"function": func_name, "dynamic_path": True},
                    )
                    self.violations.append(violation)

        # Check for dynamic attribute access
        elif func_name in ["getattr", "setattr", "delattr", "hasattr"]:
            if len(node.args) >= 2:
                attr_arg = node.args[1]
                if self._is_dynamic_value(attr_arg):
                    violation = SecurityViolation(
                        severity=ThreatLevel.HIGH,
                        message=f"Dynamic attribute access via {func_name}",
                        location=self._get_location(node),
                        cwe_id="CWE-470",
                        recommendation="Use static attribute access or whitelist allowed attributes",
                        context=self._get_context(node),
                        metadata={"function": func_name, "dynamic_attr": True},
                    )
                    self.violations.append(violation)

        # Check for SQL injection patterns in string operations
        elif func_name in ["format", "join"] or "%" in str(node):
            self._check_sql_injection_risk(node, func_name)

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """Visit attribute access."""
        # Check for dangerous attribute patterns
        attr_chain = self._get_attribute_chain(node)

        # Check for advanced reflection patterns
        reflection_patterns = {
            "__class__.__bases__": (
                ThreatLevel.CRITICAL,
                "CWE-470",
                "Class hierarchy traversal attempt",
            ),
            "__mro__": (ThreatLevel.CRITICAL, "CWE-470", "Method resolution order access"),
            "__dict__": (ThreatLevel.HIGH, "CWE-470", "Direct attribute dictionary access"),
            "__code__": (ThreatLevel.HIGH, "CWE-470", "Function code object access"),
            "__globals__": (ThreatLevel.CRITICAL, "CWE-94", "Global namespace access"),
            "__closure__": (ThreatLevel.HIGH, "CWE-470", "Function closure access"),
            "__reduce__": (ThreatLevel.HIGH, "CWE-502", "Serialization method access"),
            "__getattribute__": (ThreatLevel.HIGH, "CWE-470", "Attribute access bypass"),
            "im_func": (ThreatLevel.HIGH, "CWE-470", "Bound method function access"),
            "im_class": (ThreatLevel.HIGH, "CWE-470", "Bound method class access"),
            "f_globals": (ThreatLevel.CRITICAL, "CWE-94", "Frame globals access"),
            "f_locals": (ThreatLevel.HIGH, "CWE-470", "Frame locals access"),
        }

        for pattern, (severity, cwe, description) in reflection_patterns.items():
            if pattern in attr_chain:
                violation = SecurityViolation(
                    severity=severity,
                    message=f"Advanced reflection detected: {description}",
                    location=self._get_location(node),
                    cwe_id=cwe,
                    recommendation=f"Block access to {pattern} for security",
                    context=self._get_context(node),
                    metadata={"attribute_chain": attr_chain, "reflection_type": pattern},
                )
                self.violations.append(violation)

        # Check for prototype pollution patterns
        if "__proto__" in attr_chain or "constructor.prototype" in attr_chain:
            violation = SecurityViolation(
                severity=ThreatLevel.MEDIUM,
                message="Potential prototype pollution pattern",
                location=self._get_location(node),
                cwe_id="CWE-1321",
                recommendation="Avoid modifying object prototypes",
                context=self._get_context(node),
                metadata={"attribute_chain": attr_chain},
            )
            self.violations.append(violation)

        # Check for dangerous module usage
        if any(dangerous_mod in attr_chain for dangerous_mod in self.dangerous_modules):
            for dangerous_mod in self.dangerous_modules:
                if dangerous_mod in attr_chain:
                    violation = SecurityViolation(
                        severity=ThreatLevel.HIGH,
                        message=f"Usage of dangerous module: {dangerous_mod}",
                        location=self._get_location(node),
                        cwe_id="CWE-494",
                        recommendation=f"Use capability tokens for {dangerous_mod} access",
                        context=self._get_context(node),
                        metadata={"module": dangerous_mod, "attribute_chain": attr_chain},
                    )
                    self.violations.append(violation)
                    break

        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        """Visit subscript access (e.g., obj[key])."""
        # Check for dangerous subscript patterns
        if isinstance(node.value, ast.Attribute):
            attr_chain = self._get_attribute_chain(node.value)

            # Check for __dict__ subscript access
            if "__dict__" in attr_chain:
                violation = SecurityViolation(
                    severity=ThreatLevel.HIGH,
                    message="Direct __dict__ subscript access detected",
                    location=self._get_location(node),
                    cwe_id="CWE-470",
                    recommendation="Use controlled attribute access instead of __dict__ manipulation",
                    context=self._get_context(node),
                    metadata={"attribute_chain": attr_chain, "access_type": "subscript"},
                )
                self.violations.append(violation)

            # Check for __builtins__ access
            if "__builtins__" in attr_chain or "builtins" in attr_chain:
                violation = SecurityViolation(
                    severity=ThreatLevel.CRITICAL,
                    message="Built-ins namespace access detected",
                    location=self._get_location(node),
                    cwe_id="CWE-94",
                    recommendation="Block direct access to built-ins namespace",
                    context=self._get_context(node),
                    metadata={"attribute_chain": attr_chain, "access_type": "subscript"},
                )
                self.violations.append(violation)

        # Check for subscript access with string literals that could be dangerous
        if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
            dangerous_keys = [
                "__class__",
                "__bases__",
                "__mro__",
                "__dict__",
                "__code__",
                "__globals__",
                "__closure__",
                "__reduce__",
                "__getattribute__",
                "eval",
                "exec",
                "compile",
                "__import__",
            ]

            if node.slice.value in dangerous_keys:
                violation = SecurityViolation(
                    severity=ThreatLevel.HIGH,
                    message=f"Dangerous subscript key access: {node.slice.value}",
                    location=self._get_location(node),
                    cwe_id="CWE-470",
                    recommendation=f"Block subscript access to {node.slice.value}",
                    context=self._get_context(node),
                    metadata={"dangerous_key": node.slice.value, "access_type": "subscript"},
                )
                self.violations.append(violation)

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit assignment statements."""
        # Track variable assignments for data flow analysis
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id

                # Create data flow node
                flow_node = DataFlowNode(
                    node=node,
                    variable_name=var_name,
                    value_source=self._get_value_source(node.value),
                    line_number=getattr(node, "lineno", 0),
                )

                # Check if assigned value is tainted
                if self._is_tainted_value(node.value):
                    flow_node.is_tainted = True
                    flow_node.taint_source = self._get_taint_source(node.value)
                    self.context.tainted_variables[var_name] = flow_node

                self.variable_definitions[var_name] = flow_node

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions."""
        self.context.function_stack.append(node.name)

        # Check for suspicious function names
        suspicious_names = ["eval", "exec", "system", "shell", "cmd"]
        if any(suspicious in node.name.lower() for suspicious in suspicious_names):
            violation = SecurityViolation(
                severity=ThreatLevel.MEDIUM,
                message=f"Suspicious function name: {node.name}",
                location=self._get_location(node),
                recommendation="Review function implementation for security issues",
                context=self._get_context(node),
                metadata={"function_name": node.name},
            )
            self.violations.append(violation)

        self.generic_visit(node)
        self.context.function_stack.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definitions."""
        self.context.class_stack.append(node.name)
        self.generic_visit(node)
        self.context.class_stack.pop()

    def visit_Str(self, node: ast.Str) -> None:
        """Visit string literals."""
        # Check for suspicious string patterns
        if hasattr(node, "s"):
            string_value = node.s

            # Check for path traversal patterns
            if "../" in string_value or "..\\" in string_value:
                violation = SecurityViolation(
                    severity=ThreatLevel.HIGH,
                    message="Path traversal pattern in string literal",
                    location=self._get_location(node),
                    cwe_id="CWE-22",
                    recommendation="Validate and sanitize file paths",
                    context=self._get_context(node),
                    metadata={"string_value": string_value},
                )
                self.violations.append(violation)

            # Check for SQL keywords (potential injection)
            sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER"]
            if any(keyword in string_value.upper() for keyword in sql_keywords):
                violation = SecurityViolation(
                    severity=ThreatLevel.MEDIUM,
                    message="SQL keywords found in string literal",
                    location=self._get_location(node),
                    cwe_id="CWE-89",
                    recommendation="Use parameterized queries for database operations",
                    context=self._get_context(node),
                    metadata={"string_value": string_value, "sql_keywords": True},
                )
                self.violations.append(violation)

        self.generic_visit(node)

    def _analyze_data_flows(self) -> None:
        """Analyze data flows for tainted data propagation."""
        # Track how tainted data flows through the program
        for var_name, flow_node in self.context.tainted_variables.items():
            # Find uses of this tainted variable
            for func_name, call_node in self.function_calls:
                if self._call_uses_variable(call_node, var_name):
                    violation = SecurityViolation(
                        severity=ThreatLevel.HIGH,
                        message=f"Tainted data used in function call: {func_name}",
                        location=self._get_location(call_node),
                        cwe_id="CWE-20",
                        recommendation="Sanitize input data before use",
                        context=self._get_context(call_node),
                        metadata={
                            "tainted_variable": var_name,
                            "function": func_name,
                            "taint_source": flow_node.taint_source,
                        },
                    )
                    self.violations.append(violation)

    def _get_function_name(self, func_node: ast.AST) -> str:
        """Extract function name from function call node."""
        if isinstance(func_node, ast.Name):
            return func_node.id
        elif isinstance(func_node, ast.Attribute):
            return self._get_attribute_chain(func_node)
        else:
            return str(func_node)

    def _get_attribute_chain(self, node: ast.Attribute) -> str:
        """Get the full attribute chain (e.g., 'os.path.join')."""
        if isinstance(node.value, ast.Name):
            return f"{node.value.id}.{node.attr}"
        elif isinstance(node.value, ast.Attribute):
            return f"{self._get_attribute_chain(node.value)}.{node.attr}"
        else:
            return f"{str(node.value)}.{node.attr}"

    def _get_location(self, node: ast.AST) -> dict[str, Any]:
        """Get location information from AST node."""
        return {
            "line": getattr(node, "lineno", 0),
            "column": getattr(node, "col_offset", 0),
            "end_line": getattr(node, "end_lineno", 0),
            "end_column": getattr(node, "end_col_offset", 0),
            "filename": self.context.filename,
        }

    def _get_context(self, node: ast.AST) -> str:
        """Get source code context around a node."""
        line_no = getattr(node, "lineno", 0)
        if line_no > 0 and self.source_lines:
            line_idx = line_no - 1
            context_lines = []

            # Include surrounding lines for context
            for i in range(max(0, line_idx - 1), min(len(self.source_lines), line_idx + 2)):
                prefix = ">>> " if i == line_idx else "    "
                context_lines.append(f"{prefix}{self.source_lines[i]}")

            return "\n".join(context_lines)

        return ""

    def _is_dynamic_value(self, node: ast.AST) -> bool:
        """Check if a value is dynamically determined."""
        # Simple heuristic: variables, function calls, and attribute access are dynamic
        return isinstance(node, (ast.Name, ast.Call, ast.Attribute, ast.Subscript))

    def _is_tainted_value(self, node: ast.AST) -> bool:
        """Check if a value comes from an untrusted source."""
        # Heuristic: input functions, network calls, file reads are tainted sources
        if isinstance(node, ast.Call):
            func_name = self._get_function_name(node.func)
            tainted_functions = [
                "input",
                "raw_input",
                "requests.get",
                "urllib.request.urlopen",
                "open",
            ]
            return any(func in func_name for func in tainted_functions)

        # Variables that are already tainted
        if isinstance(node, ast.Name):
            return node.id in self.context.tainted_variables

        return False

    def _get_taint_source(self, node: ast.AST) -> str | None:
        """Get the source of taint for a value."""
        if isinstance(node, ast.Call):
            return self._get_function_name(node.func)
        elif isinstance(node, ast.Name):
            tainted_var = self.context.tainted_variables.get(node.id)
            return tainted_var.taint_source if tainted_var else None
        return None

    def _get_value_source(self, node: ast.AST) -> str | None:
        """Get a string representation of the value source."""
        try:
            return ast.unparse(node) if hasattr(ast, "unparse") else str(node)
        except:
            return str(type(node).__name__)

    def _call_uses_variable(self, call_node: ast.Call, var_name: str) -> bool:
        """Check if a function call uses a specific variable."""

        class VariableVisitor(ast.NodeVisitor):
            def __init__(self, target_var: str):
                self.target_var = target_var
                self.found = False

            def visit_Name(self, node):
                if node.id == self.target_var:
                    self.found = True

        visitor = VariableVisitor(var_name)
        visitor.visit(call_node)
        return visitor.found

    def _check_sql_injection_risk(self, node: ast.Call, func_name: str) -> None:
        """Check for SQL injection risks in string operations."""
        # This is a simplified check - real implementation would be more sophisticated
        if node.args:
            for arg in node.args:
                if isinstance(arg, ast.Str) and hasattr(arg, "s"):
                    if any(
                        keyword in arg.s.upper()
                        for keyword in ["SELECT", "INSERT", "UPDATE", "DELETE"]
                    ):
                        violation = SecurityViolation(
                            severity=ThreatLevel.MEDIUM,
                            message=f"Potential SQL injection in {func_name} operation",
                            location=self._get_location(node),
                            cwe_id="CWE-89",
                            recommendation="Use parameterized queries",
                            context=self._get_context(node),
                            metadata={"function": func_name, "sql_content": True},
                        )
                        self.violations.append(violation)

    def _get_cwe_for_function(self, func_name: str) -> str:
        """Get CWE ID for dangerous function."""
        cwe_map = {
            "eval": "CWE-94",
            "exec": "CWE-94",
            "compile": "CWE-94",
            "__import__": "CWE-94",
            "getattr": "CWE-470",
            "setattr": "CWE-470",
            "delattr": "CWE-470",
            "hasattr": "CWE-470",
        }
        return cwe_map.get(func_name, "CWE-20")

    def _get_recommendation_for_function(self, func_name: str) -> str:
        """Get security recommendation for dangerous function."""
        recommendations = {
            "eval": "Use ast.literal_eval for safe evaluation or avoid dynamic evaluation",
            "exec": "Avoid dynamic code execution or use sandboxed execution",
            "compile": "Avoid dynamic compilation or use sandboxed execution",
            "__import__": "Use static imports or capability-controlled dynamic imports",
            "getattr": "Use explicit attribute access or whitelist allowed attributes",
            "setattr": "Use explicit attribute assignment or validate attribute names",
            "delattr": "Use explicit attribute deletion or validate attribute names",
            "hasattr": "Use explicit attribute checking or validate attribute names",
        }
        return recommendations.get(func_name, "Review function usage for security implications")

    def _severity_priority(self, severity: ThreatLevel) -> int:
        """Get numeric priority for severity level."""
        priority_map = {
            ThreatLevel.CRITICAL: 0,
            ThreatLevel.HIGH: 1,
            ThreatLevel.MEDIUM: 2,
            ThreatLevel.LOW: 3,
            ThreatLevel.INFO: 4,
        }
        return priority_map.get(severity, 5)

    def _pattern_match_to_violation(self, match: PatternMatch) -> SecurityViolation:
        """Convert pattern match to security violation."""
        return SecurityViolation(
            severity=match.pattern.threat_level,
            message=match.pattern.description,
            location=match.location,
            cwe_id=match.pattern.cwe_id,
            recommendation=match.pattern.mitigation,
            context=match.context,
            metadata=match.metadata,
        )

    def get_analysis_summary(self) -> dict[str, Any]:
        """Get summary of security analysis."""
        summary = {
            "total_violations": len(self.violations),
            "by_severity": defaultdict(int),
            "by_cwe": defaultdict(int),
            "dangerous_imports": list(self.context.dangerous_imports),
            "capability_requirements": list(self.context.capability_requirements),
            "tainted_variables": len(self.context.tainted_variables),
        }

        for violation in self.violations:
            summary["by_severity"][violation.severity.value] += 1
            if violation.cwe_id:
                summary["by_cwe"][violation.cwe_id] += 1

        return dict(summary)
