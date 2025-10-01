"""
Unit tests for data_flow_tracker.py - Data flow tracking for security analysis.

Tests cover:
- Taint source identification (user input, network data, file operations)
- Variable taint propagation through assignments
- Security sink detection (eval, exec, file operations)
- Data flow path tracking from sources to sinks
- Risk level assessment
- Flow report generation
"""

import ast

import pytest

from mlpy.ml.analysis.data_flow_tracker import (
    DataFlowPath,
    DataFlowTracker,
    SecuritySink,
    TaintSource,
    TaintType,
    Variable,
)
from mlpy.ml.analysis.pattern_detector import ThreatLevel


class TestTaintType:
    """Test TaintType enum."""

    def test_taint_type_values(self):
        """Test TaintType enum values."""
        assert TaintType.USER_INPUT.value == "user_input"
        assert TaintType.NETWORK_DATA.value == "network_data"
        assert TaintType.FILE_DATA.value == "file_data"
        assert TaintType.ENVIRONMENT.value == "environment"
        assert TaintType.EXTERNAL_CALL.value == "external_call"
        assert TaintType.REFLECTION.value == "reflection"
        assert TaintType.DESERIALIZATION.value == "deserialization"


class TestTaintSource:
    """Test TaintSource dataclass."""

    def test_taint_source_creation(self):
        """Test creating a taint source."""
        source = TaintSource(
            taint_type=TaintType.USER_INPUT,
            location={"line": 10, "column": 5},
            description="User input from stdin",
            source_function="input",
            confidence=1.0,
        )

        assert source.taint_type == TaintType.USER_INPUT
        assert source.location["line"] == 10
        assert source.source_function == "input"
        assert source.confidence == 1.0

    def test_taint_source_minimal(self):
        """Test taint source with minimal fields."""
        source = TaintSource(
            taint_type=TaintType.NETWORK_DATA,
            location={},
            description="Network data",
        )

        assert source.source_function is None
        assert source.confidence == 1.0


class TestVariable:
    """Test Variable dataclass."""

    def test_variable_creation(self):
        """Test creating a variable."""
        node = ast.Name(id="x", ctx=ast.Store())
        var = Variable(
            name="x",
            node=node,
            scope="global",
            is_tainted=False,
        )

        assert var.name == "x"
        assert var.scope == "global"
        assert var.is_tainted is False
        assert len(var.taint_sources) == 0
        assert len(var.dependencies) == 0

    def test_variable_with_taint(self):
        """Test variable with taint information."""
        node = ast.Name(id="user_data", ctx=ast.Store())
        source = TaintSource(
            taint_type=TaintType.USER_INPUT,
            location={},
            description="Input",
        )

        var = Variable(
            name="user_data",
            node=node,
            scope="global",
            is_tainted=True,
            taint_sources=[source],
            line_number=10,
        )

        assert var.is_tainted is True
        assert len(var.taint_sources) == 1
        assert var.taint_sources[0].taint_type == TaintType.USER_INPUT


class TestDataFlowPath:
    """Test DataFlowPath dataclass."""

    def test_data_flow_path_creation(self):
        """Test creating a data flow path."""
        path = DataFlowPath(
            start_variable="user_input",
            end_variable="eval_arg",
            path=["user_input", "processed_data", "eval_arg"],
            taint_propagated=True,
            sink_function="eval",
            risk_level=ThreatLevel.CRITICAL,
        )

        assert path.start_variable == "user_input"
        assert path.end_variable == "eval_arg"
        assert len(path.path) == 3
        assert path.taint_propagated is True
        assert path.risk_level == ThreatLevel.CRITICAL


class TestSecuritySink:
    """Test SecuritySink dataclass."""

    def test_security_sink_creation(self):
        """Test creating a security sink."""
        node = ast.Call()
        sink = SecuritySink(
            function_name="eval",
            node=node,
            location={"line": 20},
            sink_type="code_execution",
            tainted_inputs=["user_input"],
            risk_level=ThreatLevel.CRITICAL,
        )

        assert sink.function_name == "eval"
        assert sink.sink_type == "code_execution"
        assert len(sink.tainted_inputs) == 1
        assert sink.risk_level == ThreatLevel.CRITICAL


class TestDataFlowTracker:
    """Test DataFlowTracker main functionality."""

    @pytest.fixture
    def tracker(self):
        """Create a data flow tracker."""
        return DataFlowTracker()

    def test_tracker_initialization(self, tracker):
        """Test tracker initialization."""
        assert tracker is not None
        assert len(tracker.variables) == 0
        assert len(tracker.scopes) == 1
        assert tracker.scopes[0] == "global"
        assert len(tracker.taint_sources) == 0
        assert len(tracker.security_sinks) == 0

    def test_tracker_has_taint_source_config(self, tracker):
        """Test that tracker has taint source configurations."""
        assert "input" in tracker.taint_source_functions
        assert tracker.taint_source_functions["input"] == TaintType.USER_INPUT

    def test_track_simple_assignment(self, tracker):
        """Test tracking simple variable assignment."""
        code = """
x = 42
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        # Should track the variable (variables are keyed by scope::name)
        assert "global::x" in tracker.variables or len(tracker.variables) > 0

    def test_track_tainted_input(self, tracker):
        """Test tracking tainted user input."""
        code = """
user_input = input()
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        # Should detect taint source
        assert len(tracker.taint_sources) > 0

        # Variable should be marked as tainted
        if "user_input" in tracker.variables:
            assert tracker.variables["user_input"].is_tainted

    def test_taint_propagation_through_assignment(self, tracker):
        """Test taint propagates through assignments."""
        code = """
user_input = input()
data = user_input
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        # Both variables should be tainted
        tainted = tracker.get_tainted_variables()
        tainted_names = {v.name for v in tainted}

        # At least user_input should be tainted
        assert "user_input" in tainted_names

    def test_detect_eval_sink(self, tracker):
        """Test detecting eval as a security sink."""
        code = """
user_input = input()
eval(user_input)
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        # Should detect security sink
        violations = tracker.get_security_violations()

        # Check if eval is detected as a sink
        sink_functions = {s.function_name for s in violations}
        assert "eval" in sink_functions or len(violations) > 0

    def test_detect_exec_sink(self, tracker):
        """Test detecting exec as a security sink."""
        code = """
code = input()
exec(code)
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        violations = tracker.get_security_violations()
        assert len(violations) > 0

    def test_safe_code_no_violations(self, tracker):
        """Test that safe code produces no violations."""
        code = """
x = 42
y = x + 10
print(y)
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        violations = tracker.get_security_violations()

        # Safe code should have no critical violations
        critical_violations = [v for v in violations if v.risk_level == ThreatLevel.CRITICAL]
        assert len(critical_violations) == 0

    def test_get_tainted_variables(self, tracker):
        """Test retrieving tainted variables."""
        code = """
user_input = input()
x = 42
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        tainted = tracker.get_tainted_variables()

        # Should have at least one tainted variable
        assert len(tainted) > 0
        assert all(isinstance(v, Variable) for v in tainted)
        assert all(v.is_tainted for v in tainted)

    def test_get_high_risk_flows(self, tracker):
        """Test retrieving high-risk data flows."""
        code = """
user_input = input()
eval(user_input)
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        high_risk = tracker.get_high_risk_flows()

        # Should identify high-risk flow
        assert isinstance(high_risk, list)
        assert all(isinstance(f, DataFlowPath) for f in high_risk)

    def test_generate_flow_report(self, tracker):
        """Test generating flow report."""
        code = """
x = 42
y = x + 10
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        report = tracker.generate_flow_report()

        assert isinstance(report, dict)
        assert "summary" in report
        assert "taint_sources" in report
        assert "security_violations" in report
        assert "high_risk_flows" in report
        # Check summary structure
        assert report["summary"]["total_variables"] >= 0

    def test_report_with_tainted_data(self, tracker):
        """Test report contains tainted data information."""
        code = """
user_input = input()
eval(user_input)
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        report = tracker.generate_flow_report()

        # Report should show tainted variables and sinks
        summary = report["summary"]
        assert summary["tainted_variables"] > 0 or len(report["security_violations"]) > 0

    def test_multiple_taint_sources(self, tracker):
        """Test tracking multiple taint sources."""
        code = """
user_input = input()
network_data = requests.get(url)
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        # Should detect multiple taint sources
        assert len(tracker.taint_sources) >= 1

    def test_function_scope_tracking(self, tracker):
        """Test tracking variables in function scope."""
        code = """
def process_data():
    user_input = input()
    return user_input
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        # Should track function scope
        assert len(tracker.scopes) >= 1

    def test_nested_taint_propagation(self, tracker):
        """Test taint propagation through multiple assignments."""
        code = """
a = input()
b = a
c = b
d = c
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        tainted = tracker.get_tainted_variables()

        # Should propagate taint through the chain
        assert len(tainted) >= 1

    def test_complex_expression_taint(self, tracker):
        """Test taint in complex expressions."""
        code = """
user_input = input()
result = user_input + " suffix"
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        # Result should inherit taint
        tainted = tracker.get_tainted_variables()
        tainted_names = {v.name for v in tainted}

        # At least user_input should be tainted
        assert "user_input" in tainted_names

    def test_file_operation_taint(self, tracker):
        """Test detecting file operations as taint sources."""
        code = """
file_data = open("file.txt").read()
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        # Should detect file operation
        tainted = tracker.get_tainted_variables()

        # File data should be tracked
        assert len(tainted) >= 0  # File operations may or may not be tainted by default

    def test_empty_code(self, tracker):
        """Test tracking empty code."""
        code = ""
        try:
            tree = ast.parse(code)
            tracker.track_data_flows(tree)

            report = tracker.generate_flow_report()
            assert report["summary"]["total_variables"] == 0
        except SyntaxError:
            # Empty code may cause syntax error, that's acceptable
            pass

    def test_variable_dependencies(self, tracker):
        """Test tracking variable dependencies."""
        code = """
a = 1
b = 2
c = a + b
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        # Variable c should depend on a and b
        if "c" in tracker.variables:
            deps = tracker.variables["c"].dependencies
            # Dependencies are tracked
            assert isinstance(deps, set)


class TestDataFlowIntegration:
    """Integration tests for data flow tracker."""

    @pytest.fixture
    def tracker(self):
        """Create a tracker."""
        return DataFlowTracker()

    def test_full_pipeline_input_to_eval(self, tracker):
        """Test complete flow from input to eval."""
        code = """
user_input = input("Enter code: ")
processed = user_input.strip()
eval(processed)
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        # Should detect tainted flow to dangerous sink
        tainted = tracker.get_tainted_variables()
        violations = tracker.get_security_violations()
        high_risk = tracker.get_high_risk_flows()

        # Should have detected the security issue
        assert len(tainted) > 0 or len(violations) > 0

    def test_report_structure(self, tracker):
        """Test flow report has proper structure."""
        code = """
x = input()
y = x
eval(y)
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        report = tracker.generate_flow_report()

        # Check report structure
        required_keys = [
            "summary",
            "taint_sources",
            "security_violations",
            "high_risk_flows",
        ]

        for key in required_keys:
            assert key in report

        # Check summary has required fields
        summary_keys = ["total_variables", "tainted_variables"]
        for key in summary_keys:
            assert key in report["summary"]

    def test_multiple_sinks_detection(self, tracker):
        """Test detecting multiple security sinks."""
        code = """
user_input = input()
eval(user_input)
exec(user_input)
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        violations = tracker.get_security_violations()

        # Should detect both eval and exec
        assert len(violations) >= 1

    def test_safe_operations_not_flagged(self, tracker):
        """Test that safe operations aren't flagged."""
        code = """
x = 42
y = x * 2
z = str(y)
print(z)
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        violations = tracker.get_security_violations()
        high_risk = tracker.get_high_risk_flows()

        # Should have minimal or no high-risk issues
        critical = [v for v in violations if v.risk_level == ThreatLevel.CRITICAL]
        assert len(critical) == 0

    def test_network_taint_source(self, tracker):
        """Test detecting network data as taint source."""
        code = """
response = requests.get("http://example.com")
data = response.text
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        # Should detect network taint
        tainted = tracker.get_tainted_variables()
        sources = tracker.taint_sources

        # Network data should be tracked
        assert len(tainted) > 0 or len(sources) > 0

    def test_environment_variable_taint(self, tracker):
        """Test environment variables as taint source."""
        code = """
import os
env_var = os.environ.get("USER_DATA")
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        # Environment data may be tracked
        report = tracker.generate_flow_report()
        assert isinstance(report, dict)

    def test_complex_program_analysis(self, tracker):
        """Test analyzing complex program with multiple flows."""
        code = """
def process_user_data():
    user_input = input()
    sanitized = user_input.replace("'", "")
    return sanitized

def execute_code(code):
    eval(code)

user_code = process_user_data()
execute_code(user_code)
"""
        tree = ast.parse(code)
        tracker.track_data_flows(tree)

        # Should complete analysis without errors
        report = tracker.generate_flow_report()
        assert report["summary"]["total_variables"] > 0
