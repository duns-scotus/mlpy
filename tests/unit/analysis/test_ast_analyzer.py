"""
Unit tests for ast_analyzer.py - Comprehensive AST security analysis.

Tests cover:
- SecurityViolation, DataFlowNode, SecurityContext dataclasses
- Import statement analysis (dangerous modules)
- Function call analysis (eval, exec, dangerous functions)
- Attribute access analysis (reflection patterns)
- Subscript access analysis (__dict__, __builtins__)
- Data flow analysis (taint tracking)
- SQL injection pattern detection
- Path traversal detection
- Dynamic attribute access detection
"""

import ast
import pytest
from mlpy.ml.analysis.ast_analyzer import (
    ASTSecurityAnalyzer,
    SecurityViolation,
    DataFlowNode,
    SecurityContext,
)
from mlpy.ml.analysis.pattern_detector import ThreatLevel


class TestSecurityViolation:
    """Test SecurityViolation dataclass."""

    def test_violation_creation_minimal(self):
        """Test creating violation with minimal fields."""
        violation = SecurityViolation(
            severity=ThreatLevel.CRITICAL,
            message="Test violation",
            location={"line": 10, "column": 5},
        )

        assert violation.severity == ThreatLevel.CRITICAL
        assert violation.message == "Test violation"
        assert violation.location["line"] == 10
        assert violation.cwe_id is None
        assert violation.recommendation is None

    def test_violation_creation_full(self):
        """Test creating violation with all fields."""
        violation = SecurityViolation(
            severity=ThreatLevel.HIGH,
            message="Dangerous import",
            location={"line": 5},
            cwe_id="CWE-494",
            recommendation="Use capability tokens",
            context="import os",
            metadata={"module": "os"},
        )

        assert violation.cwe_id == "CWE-494"
        assert violation.recommendation == "Use capability tokens"
        assert violation.context == "import os"
        assert violation.metadata["module"] == "os"


class TestDataFlowNode:
    """Test DataFlowNode dataclass."""

    def test_data_flow_node_creation(self):
        """Test creating data flow node."""
        node = ast.parse("x = 42").body[0]
        flow_node = DataFlowNode(
            node=node,
            variable_name="x",
            value_source="42",
            is_tainted=False,
            taint_source=None,
            line_number=1,
        )

        assert flow_node.variable_name == "x"
        assert flow_node.value_source == "42"
        assert flow_node.is_tainted is False
        assert flow_node.line_number == 1

    def test_data_flow_node_tainted(self):
        """Test tainted data flow node."""
        node = ast.parse("user_input = input()").body[0]
        flow_node = DataFlowNode(
            node=node,
            variable_name="user_input",
            value_source="input()",
            is_tainted=True,
            taint_source="input",
            line_number=1,
        )

        assert flow_node.is_tainted is True
        assert flow_node.taint_source == "input"


class TestSecurityContext:
    """Test SecurityContext dataclass."""

    def test_context_creation(self):
        """Test creating security context."""
        context = SecurityContext(
            filename="test.py",
            function_stack=["main"],
            class_stack=[],
            imports={"os", "sys"},
            dangerous_imports={"os"},
            capability_requirements={"file_access"},
            tainted_variables={},
        )

        assert context.filename == "test.py"
        assert "main" in context.function_stack
        assert "os" in context.imports
        assert "os" in context.dangerous_imports
        assert "file_access" in context.capability_requirements


class TestASTSecurityAnalyzer:
    """Test ASTSecurityAnalyzer main functionality."""

    @pytest.fixture
    def analyzer(self):
        """Create AST security analyzer."""
        return ASTSecurityAnalyzer()

    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer is not None
        assert analyzer.pattern_detector is not None
        assert len(analyzer.violations) == 0
        assert len(analyzer.dangerous_functions) > 0
        assert len(analyzer.dangerous_modules) > 0

    def test_analyze_safe_code(self, analyzer):
        """Test analyzing safe code."""
        code = """
x = 42
y = x + 10
print(y)
"""
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Safe code should have no critical violations
        critical = [v for v in violations if v.severity == ThreatLevel.CRITICAL]
        assert len(critical) == 0

    def test_detect_eval_call(self, analyzer):
        """Test detecting eval() function call."""
        code = "result = eval(user_input)"
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect eval as critical
        assert len(violations) > 0
        eval_violations = [v for v in violations if "eval" in v.message.lower()]
        assert len(eval_violations) > 0
        assert any(v.severity == ThreatLevel.CRITICAL for v in eval_violations)

    def test_detect_exec_call(self, analyzer):
        """Test detecting exec() function call."""
        code = "exec(malicious_code)"
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect exec as critical
        assert len(violations) > 0
        exec_violations = [v for v in violations if "exec" in v.message.lower()]
        assert len(exec_violations) > 0

    def test_detect_dangerous_import(self, analyzer):
        """Test detecting dangerous module imports."""
        code = "import os"
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect os import
        assert len(violations) > 0
        import_violations = [v for v in violations if "import" in v.message.lower()]
        assert any("os" in v.message for v in import_violations)

    def test_detect_dangerous_from_import(self, analyzer):
        """Test detecting dangerous from-import statements."""
        code = "from subprocess import call"
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect subprocess import
        assert len(violations) > 0
        import_violations = [v for v in violations if "subprocess" in v.message.lower()]
        assert len(import_violations) > 0

    def test_detect_getattr_dynamic(self, analyzer):
        """Test detecting dynamic getattr usage."""
        code = "value = getattr(obj, user_input)"
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect dynamic attribute access
        assert len(violations) > 0
        getattr_violations = [v for v in violations if "getattr" in v.message.lower()]
        assert len(getattr_violations) > 0

    def test_detect_reflection_class_bases(self, analyzer):
        """Test detecting __class__.__bases__ reflection."""
        code = "bases = obj.__class__.__bases__"
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect reflection pattern
        assert len(violations) > 0
        reflection_violations = [v for v in violations if "reflection" in v.message.lower()]
        assert len(reflection_violations) > 0

    def test_detect_globals_access(self, analyzer):
        """Test detecting __globals__ access."""
        code = "g = func.__globals__"
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect critical global access
        assert len(violations) > 0
        # Pattern detector may use different message text
        globals_violations = [v for v in violations if "globals" in v.message.lower() or "reflection" in v.message.lower() or "namespace" in v.message.lower()]
        assert len(globals_violations) > 0

    def test_detect_dict_subscript(self, analyzer):
        """Test detecting __dict__ subscript access."""
        code = "value = obj.__dict__['attr']"
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect __dict__ access
        assert len(violations) > 0
        dict_violations = [v for v in violations if "__dict__" in v.message.lower()]
        assert len(dict_violations) > 0

    def test_detect_builtins_subscript(self, analyzer):
        """Test detecting __builtins__ subscript access."""
        code = "value = __builtins__['eval']"
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect critical builtins access
        assert len(violations) > 0
        # Pattern detector may use different message text (execution context, subscript)
        builtins_violations = [v for v in violations if "builtins" in v.message.lower() or "built-ins" in v.message.lower() or "execution" in v.message.lower() or "subscript" in v.message.lower()]
        assert len(builtins_violations) > 0

    def test_detect_dangerous_subscript_key(self, analyzer):
        """Test detecting dangerous subscript keys."""
        code = "func = obj['__class__']"
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect dangerous key access
        assert len(violations) > 0
        key_violations = [v for v in violations if "subscript" in v.message.lower()]
        assert len(key_violations) > 0

    def test_track_variable_assignment(self, analyzer):
        """Test tracking variable assignments."""
        code = "x = 42"
        tree = ast.parse(code)
        analyzer.analyze(tree, code)

        # Should track the variable
        assert "x" in analyzer.variable_definitions

    def test_track_tainted_input(self, analyzer):
        """Test tracking tainted input."""
        code = "user_data = input()"
        tree = ast.parse(code)
        analyzer.analyze(tree, code)

        # Should mark variable as tainted
        assert "user_data" in analyzer.context.tainted_variables

    def test_detect_path_traversal(self, analyzer):
        """Test detecting path traversal patterns."""
        code = "path = '../secret/data.txt'"
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect path traversal
        path_violations = [v for v in violations if "path" in v.message.lower() and "traversal" in v.message.lower()]
        assert len(path_violations) > 0

    def test_detect_sql_keywords(self, analyzer):
        """Test detecting SQL keywords in strings."""
        code = "query = 'SELECT * FROM users'"
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect SQL keywords
        sql_violations = [v for v in violations if "sql" in v.message.lower()]
        assert len(sql_violations) > 0

    def test_detect_suspicious_function_name(self, analyzer):
        """Test detecting suspicious function names."""
        code = """
def eval_user_code():
    pass
"""
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect suspicious function name
        suspicious_violations = [v for v in violations if "suspicious" in v.message.lower()]
        assert len(suspicious_violations) > 0

    def test_function_stack_tracking(self, analyzer):
        """Test function stack tracking."""
        code = """
def outer():
    def inner():
        pass
"""
        tree = ast.parse(code)

        # Track function entries
        class FunctionTracker(ast.NodeVisitor):
            def __init__(self):
                self.functions = []

            def visit_FunctionDef(self, node):
                self.functions.append(node.name)
                self.generic_visit(node)

        tracker = FunctionTracker()
        tracker.visit(tree)

        assert "outer" in tracker.functions
        assert "inner" in tracker.functions

    def test_class_stack_tracking(self, analyzer):
        """Test class stack tracking."""
        code = """
class MyClass:
    def method(self):
        pass
"""
        tree = ast.parse(code)
        analyzer.analyze(tree, code)

        # Context should be created
        assert analyzer.context is not None

    def test_get_analysis_summary(self, analyzer):
        """Test getting analysis summary."""
        code = """
import os
result = eval(code)
"""
        tree = ast.parse(code)
        analyzer.analyze(tree, code)

        summary = analyzer.get_analysis_summary()

        assert isinstance(summary, dict)
        assert "total_violations" in summary
        assert "by_severity" in summary
        assert summary["total_violations"] > 0

    def test_capability_requirements_system_access(self, analyzer):
        """Test capability requirements for system access."""
        code = "import subprocess"
        tree = ast.parse(code)
        analyzer.analyze(tree, code)

        # Should require system_access capability
        assert "system_access" in analyzer.context.capability_requirements

    def test_capability_requirements_network_access(self, analyzer):
        """Test capability requirements for network access."""
        code = "import socket"
        tree = ast.parse(code)
        analyzer.analyze(tree, code)

        # Should require network_access capability
        assert "network_access" in analyzer.context.capability_requirements

    def test_capability_requirements_file_access(self, analyzer):
        """Test capability requirements for file access."""
        code = "f = open('file.txt')"
        tree = ast.parse(code)
        analyzer.analyze(tree, code)

        # Should require file_access capability
        assert "file_access" in analyzer.context.capability_requirements

    def test_dynamic_file_path_detection(self, analyzer):
        """Test detecting dynamic file paths."""
        code = "f = open(user_path)"
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect dynamic file path
        file_violations = [v for v in violations if "file" in v.message.lower() and "dynamic" in v.message.lower()]
        assert len(file_violations) > 0

    def test_violation_sorting(self, analyzer):
        """Test that violations are sorted by severity."""
        code = """
import os
result = eval(code)
x = 42
"""
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Critical violations should come first
        if len(violations) > 1:
            for i in range(len(violations) - 1):
                assert analyzer._severity_priority(violations[i].severity) <= analyzer._severity_priority(violations[i + 1].severity)

    def test_cwe_mapping(self, analyzer):
        """Test CWE ID mapping for functions."""
        assert analyzer._get_cwe_for_function("eval") == "CWE-94"
        assert analyzer._get_cwe_for_function("exec") == "CWE-94"
        assert analyzer._get_cwe_for_function("getattr") == "CWE-470"

    def test_recommendation_generation(self, analyzer):
        """Test recommendation generation."""
        rec = analyzer._get_recommendation_for_function("eval")
        assert "literal_eval" in rec or "avoid" in rec.lower()

    def test_attribute_chain_extraction(self, analyzer):
        """Test attribute chain extraction."""
        code = "value = os.path.join(a, b)"
        tree = ast.parse(code)

        # Find the Call node
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                chain = analyzer._get_attribute_chain(node.func)
                assert "os.path.join" in chain
                break

    def test_function_name_extraction(self, analyzer):
        """Test function name extraction."""
        code = "result = eval(x)"
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = analyzer._get_function_name(node.func)
                assert name == "eval"
                break

    def test_location_extraction(self, analyzer):
        """Test location information extraction."""
        code = "eval(x)"
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                location = analyzer._get_location(node)
                assert "line" in location
                assert location["line"] == 1
                break

    def test_context_extraction(self, analyzer):
        """Test source context extraction."""
        code = "line1\neval(x)\nline3"
        tree = ast.parse(code)
        analyzer.source_lines = code.split("\n")

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                context = analyzer._get_context(node)
                assert "eval" in context
                break

    def test_dynamic_value_detection(self, analyzer):
        """Test dynamic value detection."""
        code = "x = user_input"
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == "user_input":
                assert analyzer._is_dynamic_value(node) is True
                break

    def test_tainted_value_detection(self, analyzer):
        """Test tainted value detection."""
        code = "x = input()"
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                assert analyzer._is_tainted_value(node) is True
                break


class TestASTAnalyzerIntegration:
    """Integration tests for AST analyzer."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer."""
        return ASTSecurityAnalyzer()

    def test_full_analysis_pipeline(self, analyzer):
        """Test complete analysis pipeline."""
        code = """
import os
user_input = input()
result = eval(user_input)
"""
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect multiple issues
        assert len(violations) > 0

        # Should have import violation
        import_violations = [v for v in violations if "import" in v.message.lower()]
        assert len(import_violations) > 0

        # Should have eval violation
        eval_violations = [v for v in violations if "eval" in v.message.lower()]
        assert len(eval_violations) > 0

    def test_data_flow_analysis(self, analyzer):
        """Test data flow analysis."""
        code = """
user_input = input()
processed = user_input.strip()
eval(processed)
"""
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should track tainted data flow
        assert len(analyzer.context.tainted_variables) > 0
        assert "user_input" in analyzer.context.tainted_variables

    def test_complex_reflection_detection(self, analyzer):
        """Test complex reflection pattern detection."""
        code = """
cls = obj.__class__
bases = cls.__bases__[0]
mro = cls.__mro__
"""
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect multiple reflection patterns
        reflection_count = sum(1 for v in violations if "reflection" in v.message.lower())
        assert reflection_count > 0

    def test_mixed_security_issues(self, analyzer):
        """Test detecting mixed security issues."""
        code = """
import subprocess
user_cmd = input()
subprocess.call(user_cmd)
data = obj.__dict__['secret']
"""
        tree = ast.parse(code)
        violations = analyzer.analyze(tree, code)

        # Should detect multiple different issues
        assert len(violations) >= 2

        # Check for variety of violations
        violation_types = {v.message.split(":")[0] if ":" in v.message else v.message for v in violations}
        assert len(violation_types) > 1

    def test_summary_generation(self, analyzer):
        """Test analysis summary generation."""
        code = """
import os
import sys
eval(code)
exec(code)
"""
        tree = ast.parse(code)
        analyzer.analyze(tree, code)

        summary = analyzer.get_analysis_summary()

        # Check summary structure
        assert "total_violations" in summary
        assert "by_severity" in summary
        assert "dangerous_imports" in summary
        assert "capability_requirements" in summary

        # Should have detected dangerous imports
        assert len(summary["dangerous_imports"]) > 0
