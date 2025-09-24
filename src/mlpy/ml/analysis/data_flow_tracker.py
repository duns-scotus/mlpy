"""Data flow tracking for security analysis."""

import ast
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .pattern_detector import ThreatLevel


class TaintType(Enum):
    """Types of data taint."""

    USER_INPUT = "user_input"
    NETWORK_DATA = "network_data"
    FILE_DATA = "file_data"
    ENVIRONMENT = "environment"
    EXTERNAL_CALL = "external_call"
    REFLECTION = "reflection"
    DESERIALIZATION = "deserialization"


@dataclass
class TaintSource:
    """Source of data taint."""

    taint_type: TaintType
    location: dict[str, Any]
    description: str
    source_function: str | None = None
    confidence: float = 1.0


@dataclass
class Variable:
    """Represents a variable in the program."""

    name: str
    node: ast.AST
    scope: str
    value_type: type | None = None
    is_tainted: bool = False
    taint_sources: list[TaintSource] = field(default_factory=list)
    dependencies: set[str] = field(default_factory=set)
    line_number: int = 0


@dataclass
class DataFlowPath:
    """Represents a path of data flow."""

    start_variable: str
    end_variable: str
    path: list[str]
    taint_propagated: bool
    sink_function: str | None = None
    risk_level: ThreatLevel = ThreatLevel.LOW


@dataclass
class SecuritySink:
    """Represents a security-sensitive operation."""

    function_name: str
    node: ast.AST
    location: dict[str, Any]
    sink_type: str  # 'code_execution', 'file_access', 'network', 'reflection', etc.
    tainted_inputs: list[str] = field(default_factory=list)
    risk_level: ThreatLevel = ThreatLevel.MEDIUM


class DataFlowTracker(ast.NodeVisitor):
    """Advanced data flow tracker for security analysis."""

    def __init__(self):
        """Initialize the data flow tracker."""
        self.variables: dict[str, Variable] = {}
        self.scopes: list[str] = ["global"]
        self.taint_sources: list[TaintSource] = []
        self.security_sinks: list[SecuritySink] = []
        self.data_flows: list[DataFlowPath] = []

        # Configuration
        self.taint_source_functions = {
            # User input sources
            "input": TaintType.USER_INPUT,
            "raw_input": TaintType.USER_INPUT,
            "sys.stdin.readline": TaintType.USER_INPUT,
            "sys.stdin.read": TaintType.USER_INPUT,
            "sys.argv": TaintType.USER_INPUT,
            # Network data sources
            "requests.get": TaintType.NETWORK_DATA,
            "requests.post": TaintType.NETWORK_DATA,
            "requests.put": TaintType.NETWORK_DATA,
            "requests.patch": TaintType.NETWORK_DATA,
            "requests.delete": TaintType.NETWORK_DATA,
            "requests.request": TaintType.NETWORK_DATA,
            "urllib.request.urlopen": TaintType.NETWORK_DATA,
            "urllib.request.urlretrieve": TaintType.NETWORK_DATA,
            "urllib2.urlopen": TaintType.NETWORK_DATA,
            "httplib.HTTPConnection": TaintType.NETWORK_DATA,
            "http.client.HTTPConnection": TaintType.NETWORK_DATA,
            "socket.recv": TaintType.NETWORK_DATA,
            "socket.recvfrom": TaintType.NETWORK_DATA,
            "socket.accept": TaintType.NETWORK_DATA,
            # File data sources
            "open": TaintType.FILE_DATA,
            "file": TaintType.FILE_DATA,
            "file.read": TaintType.FILE_DATA,
            "file.readline": TaintType.FILE_DATA,
            "file.readlines": TaintType.FILE_DATA,
            "io.open": TaintType.FILE_DATA,
            "codecs.open": TaintType.FILE_DATA,
            "pathlib.Path.read_text": TaintType.FILE_DATA,
            "pathlib.Path.read_bytes": TaintType.FILE_DATA,
            # Environment sources
            "os.environ": TaintType.ENVIRONMENT,
            "os.getenv": TaintType.ENVIRONMENT,
            "os.environ.get": TaintType.ENVIRONMENT,
            "sys.environ": TaintType.ENVIRONMENT,
            # Reflection sources
            "getattr": TaintType.REFLECTION,
            "vars": TaintType.REFLECTION,
            "globals": TaintType.REFLECTION,
            "locals": TaintType.REFLECTION,
            "dir": TaintType.REFLECTION,
            # Deserialization sources
            "pickle.loads": TaintType.DESERIALIZATION,
            "pickle.load": TaintType.DESERIALIZATION,
            "marshal.loads": TaintType.DESERIALIZATION,
            "marshal.load": TaintType.DESERIALIZATION,
            "dill.loads": TaintType.DESERIALIZATION,
            "dill.load": TaintType.DESERIALIZATION,
            "yaml.load": TaintType.DESERIALIZATION,
            "json.loads": TaintType.DESERIALIZATION,
            # External execution sources
            "eval": TaintType.EXTERNAL_CALL,
            "exec": TaintType.EXTERNAL_CALL,
            "compile": TaintType.EXTERNAL_CALL,
            "subprocess.call": TaintType.EXTERNAL_CALL,
            "subprocess.run": TaintType.EXTERNAL_CALL,
            "subprocess.Popen": TaintType.EXTERNAL_CALL,
            "os.system": TaintType.EXTERNAL_CALL,
            "os.popen": TaintType.EXTERNAL_CALL,
            "commands.getoutput": TaintType.EXTERNAL_CALL,
        }

        self.security_sink_functions = {
            "eval": ("code_execution", ThreatLevel.CRITICAL),
            "exec": ("code_execution", ThreatLevel.CRITICAL),
            "compile": ("code_execution", ThreatLevel.CRITICAL),
            "subprocess.call": ("command_injection", ThreatLevel.HIGH),
            "subprocess.run": ("command_injection", ThreatLevel.HIGH),
            "os.system": ("command_injection", ThreatLevel.HIGH),
            "open": ("file_access", ThreatLevel.MEDIUM),
            "file": ("file_access", ThreatLevel.MEDIUM),
            "__import__": ("dynamic_import", ThreatLevel.HIGH),
            "importlib.import_module": ("dynamic_import", ThreatLevel.HIGH),
            "getattr": ("reflection", ThreatLevel.MEDIUM),
            "setattr": ("reflection", ThreatLevel.MEDIUM),
            "delattr": ("reflection", ThreatLevel.MEDIUM),
            "pickle.dumps": ("serialization", ThreatLevel.LOW),
            "pickle.loads": ("deserialization", ThreatLevel.HIGH),
        }

        self.source_lines: list[str] = []

    def track_data_flows(
        self, tree: ast.AST, source_code: str = "", filename: str | None = None
    ) -> dict[str, Any]:
        """Track data flows in the AST."""
        self.source_lines = source_code.split("\n") if source_code else []
        self.filename = filename

        # Reset state
        self.variables.clear()
        self.scopes = ["global"]
        self.taint_sources.clear()
        self.security_sinks.clear()
        self.data_flows.clear()

        # Visit AST
        self.visit(tree)

        # Analyze data flows
        self._analyze_taint_propagation()
        self._identify_security_violations()

        return {
            "variables": len(self.variables),
            "taint_sources": len(self.taint_sources),
            "security_sinks": len(self.security_sinks),
            "data_flows": len(self.data_flows),
            "tainted_variables": len([v for v in self.variables.values() if v.is_tainted]),
            "high_risk_flows": len(
                [
                    f
                    for f in self.data_flows
                    if f.risk_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]
                ]
            ),
            "violations": [sink for sink in self.security_sinks if sink.tainted_inputs],
        }

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition."""
        self.scopes.append(node.name)
        self.generic_visit(node)
        self.scopes.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition."""
        self.scopes.append(f"class:{node.name}")
        self.generic_visit(node)
        self.scopes.pop()

    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit assignment statements."""
        # Get value information
        value_info = self._analyze_value(node.value)

        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = self._get_variable_key(target.id)

                # Create or update variable
                variable = Variable(
                    name=target.id,
                    node=node,
                    scope=self._get_current_scope(),
                    line_number=getattr(node, "lineno", 0),
                )

                # Check if value is from taint source
                if value_info["is_tainted"]:
                    variable.is_tainted = True
                    variable.taint_sources.extend(value_info["taint_sources"])

                # Track dependencies
                variable.dependencies.update(value_info["dependencies"])

                # Propagate taint from dependencies
                for dep_name in value_info["dependencies"]:
                    dep_key = self._get_variable_key(dep_name)
                    if dep_key in self.variables and self.variables[dep_key].is_tainted:
                        variable.is_tainted = True
                        variable.taint_sources.extend(self.variables[dep_key].taint_sources)

                self.variables[var_name] = variable

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Visit function calls."""
        func_name = self._get_function_name(node.func)

        # Check if this is a taint source
        taint_type = self._get_taint_type(func_name)
        if taint_type:
            taint_source = TaintSource(
                taint_type=taint_type,
                location=self._get_location(node),
                description=f"Data from {func_name}",
                source_function=func_name,
            )
            self.taint_sources.append(taint_source)

        # Check if this is a security sink
        sink_info = self._get_sink_info(func_name)
        if sink_info:
            sink_type, risk_level = sink_info

            # Analyze arguments for tainted data
            tainted_inputs = []
            for i, arg in enumerate(node.args):
                arg_variables = self._extract_variables_from_node(arg)
                for var_name in arg_variables:
                    var_key = self._get_variable_key(var_name)
                    if var_key in self.variables and self.variables[var_key].is_tainted:
                        tainted_inputs.append(var_name)

            security_sink = SecuritySink(
                function_name=func_name,
                node=node,
                location=self._get_location(node),
                sink_type=sink_type,
                tainted_inputs=tainted_inputs,
                risk_level=risk_level,
            )
            self.security_sinks.append(security_sink)

        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        """Visit name references."""
        if isinstance(node.ctx, ast.Load):
            # This is a variable use - we'll track this in parent nodes
            pass
        self.generic_visit(node)

    def _analyze_value(self, node: ast.AST) -> dict[str, Any]:
        """Analyze a value node for taint and dependencies."""
        result = {
            "is_tainted": False,
            "taint_sources": [],
            "dependencies": set(),
            "value_type": None,
        }

        if isinstance(node, ast.Call):
            func_name = self._get_function_name(node.func)

            # Check if this call produces tainted data
            taint_type = self._get_taint_type(func_name)
            if taint_type:
                result["is_tainted"] = True
                taint_source = TaintSource(
                    taint_type=taint_type,
                    location=self._get_location(node),
                    description=f"Data from {func_name}",
                    source_function=func_name,
                )
                result["taint_sources"].append(taint_source)

            # Check if this is a method call on a tainted object
            elif isinstance(node.func, ast.Attribute):
                base_analysis = self._analyze_value(node.func.value)
                if base_analysis["is_tainted"]:
                    # Method calls on tainted data preserve taint
                    # This handles cases like tainted_string.strip()
                    method_name = node.func.attr
                    if method_name in {
                        "strip",
                        "replace",
                        "format",
                        "join",
                        "split",
                        "lower",
                        "upper",
                        "text",
                        "content",
                        "decode",
                    }:
                        result["is_tainted"] = True
                        result["taint_sources"].extend(base_analysis["taint_sources"])

            # Extract variable dependencies from arguments
            for arg in node.args:
                result["dependencies"].update(self._extract_variables_from_node(arg))

        elif isinstance(node, ast.Name):
            # Direct variable reference
            result["dependencies"].add(node.id)

        elif isinstance(node, ast.BinOp):
            # Binary operation - check both operands
            result["dependencies"].update(self._extract_variables_from_node(node.left))
            result["dependencies"].update(self._extract_variables_from_node(node.right))

        elif isinstance(node, ast.Attribute):
            # Attribute access - check if base object is tainted
            result["dependencies"].update(self._extract_variables_from_node(node))

            # Handle attribute access on tainted data (e.g., response.text)
            if isinstance(node.value, ast.Name):
                var_key = self._get_variable_key(node.value.id)
                if var_key in self.variables and self.variables[var_key].is_tainted:
                    # Attribute access preserves taint
                    result["is_tainted"] = True
                    result["taint_sources"].extend(self.variables[var_key].taint_sources)
            elif isinstance(node.value, ast.Call):
                # Handle chained calls like requests.get(...).text
                call_analysis = self._analyze_value(node.value)
                if call_analysis["is_tainted"]:
                    result["is_tainted"] = True
                    result["taint_sources"].extend(call_analysis["taint_sources"])

        elif isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            # Container literals
            for elt in node.elts:
                result["dependencies"].update(self._extract_variables_from_node(elt))

        elif isinstance(node, ast.Dict):
            # Dictionary literal
            for key, value in zip(node.keys, node.values, strict=False):
                if key:
                    result["dependencies"].update(self._extract_variables_from_node(key))
                result["dependencies"].update(self._extract_variables_from_node(value))

        elif isinstance(node, ast.JoinedStr):
            # F-string formatting - check all values for taint
            for value in node.values:
                if isinstance(value, ast.FormattedValue):
                    value_analysis = self._analyze_value(value.value)
                    result["dependencies"].update(value_analysis["dependencies"])
                    if value_analysis["is_tainted"]:
                        result["is_tainted"] = True
                        result["taint_sources"].extend(value_analysis["taint_sources"])

        return result

    def _extract_variables_from_node(self, node: ast.AST) -> set[str]:
        """Extract all variable names referenced in a node."""
        variables = set()

        class VariableExtractor(ast.NodeVisitor):
            def visit_Name(self, n):
                if isinstance(n.ctx, ast.Load):
                    variables.add(n.id)

        extractor = VariableExtractor()
        extractor.visit(node)
        return variables

    def _get_function_name(self, func_node: ast.AST) -> str:
        """Extract function name from function call node."""
        if isinstance(func_node, ast.Name):
            return func_node.id
        elif isinstance(func_node, ast.Attribute):
            return self._get_attribute_chain(func_node)
        else:
            return str(func_node)

    def _get_attribute_chain(self, node: ast.Attribute) -> str:
        """Get the full attribute chain."""
        if isinstance(node.value, ast.Name):
            return f"{node.value.id}.{node.attr}"
        elif isinstance(node.value, ast.Attribute):
            return f"{self._get_attribute_chain(node.value)}.{node.attr}"
        else:
            return f"{str(node.value)}.{node.attr}"

    def _get_taint_type(self, func_name: str) -> TaintType | None:
        """Get taint type for a function name."""
        # Direct match first
        if func_name in self.taint_source_functions:
            return self.taint_source_functions[func_name]

        # Pattern matching for partial matches
        for pattern, taint_type in self.taint_source_functions.items():
            if ("." in pattern and pattern in func_name) or (
                "." not in pattern and pattern == func_name.split(".")[-1]
            ):
                return taint_type

        # Additional heuristic matching
        func_lower = func_name.lower()
        if any(
            keyword in func_lower for keyword in ["request", "get", "post", "fetch", "download"]
        ):
            return TaintType.NETWORK_DATA
        elif any(keyword in func_lower for keyword in ["read", "load", "open"]):
            return TaintType.FILE_DATA
        elif any(keyword in func_lower for keyword in ["input", "raw_input"]):
            return TaintType.USER_INPUT

        return None

    def _get_sink_info(self, func_name: str) -> tuple[str, ThreatLevel] | None:
        """Get security sink information for a function name."""
        for pattern, (sink_type, risk_level) in self.security_sink_functions.items():
            if pattern in func_name or func_name in pattern:
                return (sink_type, risk_level)
        return None

    def _get_variable_key(self, var_name: str) -> str:
        """Get unique key for variable including scope."""
        scope = self._get_current_scope()
        return f"{scope}::{var_name}"

    def _get_current_scope(self) -> str:
        """Get current scope string."""
        return ".".join(self.scopes)

    def _get_location(self, node: ast.AST) -> dict[str, Any]:
        """Get location information from AST node."""
        return {
            "line": getattr(node, "lineno", 0),
            "column": getattr(node, "col_offset", 0),
            "end_line": getattr(node, "end_lineno", 0),
            "end_column": getattr(node, "end_col_offset", 0),
            "filename": getattr(self, "filename", None),
        }

    def _analyze_taint_propagation(self) -> None:
        """Analyze how taint propagates through the program."""
        # Build dependency graph
        dependency_graph = defaultdict(set)

        for var_key, variable in self.variables.items():
            for dep in variable.dependencies:
                dep_key = self._get_variable_key(dep)
                if dep_key in self.variables:
                    dependency_graph[dep_key].add(var_key)

        # Propagate taint through dependencies using BFS
        queue = deque()

        # Start with initially tainted variables
        for var_key, variable in self.variables.items():
            if variable.is_tainted:
                queue.append(var_key)

        visited = set()

        while queue:
            current_var = queue.popleft()
            if current_var in visited:
                continue

            visited.add(current_var)
            current_variable = self.variables.get(current_var)

            if not current_variable or not current_variable.is_tainted:
                continue

            # Propagate taint to dependent variables
            for dependent_var in dependency_graph[current_var]:
                if dependent_var not in self.variables:
                    continue

                dependent_variable = self.variables[dependent_var]

                if not dependent_variable.is_tainted:
                    dependent_variable.is_tainted = True
                    dependent_variable.taint_sources.extend(current_variable.taint_sources)
                    queue.append(dependent_var)

                    # Create data flow path
                    self._create_data_flow_path(
                        current_var, dependent_var, current_variable.taint_sources
                    )

    def _create_data_flow_path(
        self, source_var: str, target_var: str, taint_sources: list[TaintSource]
    ) -> None:
        """Create a data flow path between variables."""
        # Simplify variable names for display
        source_name = source_var.split("::")[-1]
        target_name = target_var.split("::")[-1]

        # Determine risk level based on taint sources
        risk_level = ThreatLevel.LOW
        for source in taint_sources:
            if source.taint_type in [TaintType.USER_INPUT, TaintType.NETWORK_DATA]:
                risk_level = ThreatLevel.MEDIUM
            elif source.taint_type in [TaintType.EXTERNAL_CALL, TaintType.DESERIALIZATION]:
                risk_level = ThreatLevel.HIGH

        flow_path = DataFlowPath(
            start_variable=source_name,
            end_variable=target_name,
            path=[source_name, target_name],
            taint_propagated=True,
            risk_level=risk_level,
        )

        self.data_flows.append(flow_path)

    def _identify_security_violations(self) -> None:
        """Identify security violations from tainted data reaching sinks."""
        for sink in self.security_sinks:
            if sink.tainted_inputs:
                # This sink receives tainted data - potential security violation

                # Find the most severe taint source
                max_risk = ThreatLevel.LOW
                for var_name in sink.tainted_inputs:
                    var_key = self._get_variable_key(var_name)
                    if var_key in self.variables:
                        variable = self.variables[var_key]
                        for source in variable.taint_sources:
                            source_risk = self._get_taint_risk_level(source.taint_type)
                            if self._compare_risk_levels(source_risk, max_risk) > 0:
                                max_risk = source_risk

                # Combine sink risk with taint risk
                combined_risk = self._combine_risk_levels(sink.risk_level, max_risk)
                sink.risk_level = combined_risk

    def _get_taint_risk_level(self, taint_type: TaintType) -> ThreatLevel:
        """Get risk level for taint type."""
        risk_map = {
            TaintType.USER_INPUT: ThreatLevel.HIGH,
            TaintType.NETWORK_DATA: ThreatLevel.HIGH,
            TaintType.FILE_DATA: ThreatLevel.MEDIUM,
            TaintType.ENVIRONMENT: ThreatLevel.MEDIUM,
            TaintType.EXTERNAL_CALL: ThreatLevel.CRITICAL,
            TaintType.REFLECTION: ThreatLevel.HIGH,
            TaintType.DESERIALIZATION: ThreatLevel.HIGH,
        }
        return risk_map.get(taint_type, ThreatLevel.LOW)

    def _compare_risk_levels(self, risk1: ThreatLevel, risk2: ThreatLevel) -> int:
        """Compare two risk levels. Returns 1 if risk1 > risk2, -1 if risk1 < risk2, 0 if equal."""
        priority_map = {
            ThreatLevel.CRITICAL: 4,
            ThreatLevel.HIGH: 3,
            ThreatLevel.MEDIUM: 2,
            ThreatLevel.LOW: 1,
            ThreatLevel.INFO: 0,
        }

        priority1 = priority_map.get(risk1, 0)
        priority2 = priority_map.get(risk2, 0)

        if priority1 > priority2:
            return 1
        elif priority1 < priority2:
            return -1
        else:
            return 0

    def _combine_risk_levels(self, risk1: ThreatLevel, risk2: ThreatLevel) -> ThreatLevel:
        """Combine two risk levels, returning the higher risk."""
        if self._compare_risk_levels(risk1, risk2) >= 0:
            return risk1
        else:
            return risk2

    def get_tainted_variables(self) -> list[Variable]:
        """Get all tainted variables."""
        return [var for var in self.variables.values() if var.is_tainted]

    def get_high_risk_flows(self) -> list[DataFlowPath]:
        """Get high-risk data flows."""
        return [
            flow
            for flow in self.data_flows
            if flow.risk_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]
        ]

    def get_security_violations(self) -> list[SecuritySink]:
        """Get security sinks that receive tainted data."""
        return [sink for sink in self.security_sinks if sink.tainted_inputs]

    def generate_flow_report(self) -> dict[str, Any]:
        """Generate comprehensive data flow report."""
        tainted_vars = self.get_tainted_variables()
        high_risk_flows = self.get_high_risk_flows()
        violations = self.get_security_violations()

        return {
            "summary": {
                "total_variables": len(self.variables),
                "tainted_variables": len(tainted_vars),
                "data_flows": len(self.data_flows),
                "high_risk_flows": len(high_risk_flows),
                "security_violations": len(violations),
            },
            "taint_sources": [
                {
                    "type": source.taint_type.value,
                    "function": source.source_function,
                    "location": source.location,
                    "description": source.description,
                }
                for source in self.taint_sources
            ],
            "security_violations": [
                {
                    "function": sink.function_name,
                    "sink_type": sink.sink_type,
                    "risk_level": sink.risk_level.value,
                    "tainted_inputs": sink.tainted_inputs,
                    "location": sink.location,
                }
                for sink in violations
            ],
            "high_risk_flows": [
                {
                    "from": flow.start_variable,
                    "to": flow.end_variable,
                    "risk_level": flow.risk_level.value,
                    "path": flow.path,
                }
                for flow in high_risk_flows
            ],
        }
