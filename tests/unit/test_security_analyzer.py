"""Unit tests for the security analyzer."""

import pytest
from mlpy.ml.analysis.security_analyzer import SecurityAnalyzer, analyze_security, check_code_security
from mlpy.ml.grammar.parser import parse_ml_code
from mlpy.ml.errors.exceptions import MLSecurityError


class TestSecurityAnalyzer:
    """Test the security analyzer."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = SecurityAnalyzer()

    def test_safe_code(self):
        """Test that safe code produces no security issues."""
        code = '''
        function calculate(a, b) {
            result = a + b;
            return result;
        }

        x = 42;
        y = calculate(x, 10);
        '''

        ast = parse_ml_code(code)
        issues = self.analyzer.analyze(ast)

        assert len(issues) == 0

    def test_dangerous_function_calls(self):
        """Test detection of dangerous function calls."""
        code = '''
        result = eval(user_input);
        data = exec(code_string);
        module = __import__("os");
        '''

        ast = parse_ml_code(code)
        issues = self.analyzer.analyze(ast)

        # Should detect all three dangerous calls
        assert len(issues) >= 3

        # Check that all are security errors
        for issue in issues:
            assert isinstance(issue.error, MLSecurityError)
            assert "code_injection" in issue.error.context.get("category", "")

    def test_unsafe_imports(self):
        """Test detection of unsafe imports."""
        code = '''
        import os;
        import sys as system;
        import subprocess.call;
        import pickle;
        '''

        ast = parse_ml_code(code)
        issues = self.analyzer.analyze(ast)

        # Should detect unsafe imports
        assert len(issues) >= 4

        # Check for unsafe import errors
        unsafe_import_issues = [
            issue for issue in issues
            if "unsafe_import" in issue.error.context.get("category", "")
        ]
        assert len(unsafe_import_issues) >= 4

    def test_reflection_abuse(self):
        """Test detection of reflection abuse."""
        code = '''
        secret = obj.__class__.__bases__[0];
        globals_dict = func.__globals__;
        code_obj = func.__code__;
        '''

        ast = parse_ml_code(code)
        issues = self.analyzer.analyze(ast)

        # Should detect reflection abuse
        assert len(issues) >= 3

        # Check for reflection abuse errors
        reflection_issues = [
            issue for issue in issues
            if "reflection_abuse" in issue.error.context.get("category", "")
        ]
        assert len(reflection_issues) >= 3

    def test_capability_validation(self):
        """Test capability declaration validation."""
        code = '''
        capability TooPermissive {
            resource "*";
            allow system "*";
        }

        capability BetterScoped {
            resource "/tmp/myapp/*";
            allow read "/etc/config";
        }
        '''

        ast = parse_ml_code(code)
        issues = self.analyzer.analyze(ast)

        # Should detect overly broad capability and dangerous permission
        overly_broad = [
            issue for issue in issues
            if "overly_broad_capability" in issue.error.context.get("category", "")
        ]
        dangerous_perm = [
            issue for issue in issues
            if "dangerous_permission" in issue.error.context.get("category", "")
        ]

        assert len(overly_broad) >= 1
        assert len(dangerous_perm) >= 1

    def test_suspicious_strings(self):
        """Test detection of suspicious string content."""
        code = '''
        dangerous = "eval(malicious_code)";
        command = "os.system('rm -rf /')";
        normal = "This is a normal string";
        '''

        ast = parse_ml_code(code)
        issues = self.analyzer.analyze(ast)

        # Should detect suspicious strings
        suspicious_issues = [
            issue for issue in issues
            if "suspicious_string" in issue.error.context.get("category", "")
        ]
        assert len(suspicious_issues) >= 2

    def test_nested_dangerous_operations(self):
        """Test detection in nested code structures."""
        code = '''
        function processData(input) {
            if (input.hasCode) {
                for (item in input.items) {
                    result = eval(item.expression);
                    output[item.id] = result;
                }
            }
            return output;
        }
        '''

        ast = parse_ml_code(code)
        issues = self.analyzer.analyze(ast)

        # Should detect eval even in nested structure
        assert len(issues) >= 1
        eval_issues = [
            issue for issue in issues
            if issue.error.context.get("operation") == "eval"
        ]
        assert len(eval_issues) >= 1

    def test_member_access_patterns(self):
        """Test detection of dangerous member access patterns."""
        code = '''
        base_class = obj.__class__.__bases__;
        dict_access = obj.__dict__;
        method_resolution = cls.__mro__;
        '''

        ast = parse_ml_code(code)
        issues = self.analyzer.analyze(ast)

        # Should detect all dangerous member accesses
        reflection_issues = [
            issue for issue in issues
            if "reflection_abuse" in issue.error.context.get("category", "")
        ]
        assert len(reflection_issues) >= 3

    def test_security_severity_levels(self):
        """Test that different security issues have appropriate severity levels."""
        code = '''
        // Critical: direct code execution
        result = eval(user_input);

        // High: dangerous import
        import os;

        // High: reflection abuse
        secrets = obj.__globals__;

        // Medium: overly broad capability
        capability TooWide {
            resource "*";
        }
        '''

        ast = parse_ml_code(code)
        issues = self.analyzer.analyze(ast)

        # Check severity distribution
        critical_issues = [
            issue for issue in issues
            if issue.error.severity.value == "critical"
        ]
        high_issues = [
            issue for issue in issues
            if issue.error.severity.value == "high"
        ]

        assert len(critical_issues) >= 1  # eval call
        assert len(high_issues) >= 2     # import + reflection

    def test_analyze_security_function(self):
        """Test the convenience analyze_security function."""
        code = 'result = eval("dangerous");'

        ast = parse_ml_code(code)
        issues = analyze_security(ast, "test.ml")

        assert len(issues) >= 1
        assert all(isinstance(issue.error, MLSecurityError) for issue in issues)

    def test_check_code_security_function(self):
        """Test the convenience check_code_security function."""
        code = '''
        import os;
        data = eval(user_input);
        '''

        issues = check_code_security(code, "test.ml")

        assert len(issues) >= 2
        assert all(isinstance(issue.error, MLSecurityError) for issue in issues)

    def test_error_context_information(self):
        """Test that security issues contain proper context information."""
        code = 'dangerous = eval("malicious");'

        issues = check_code_security(code, "test.ml")

        assert len(issues) >= 1
        issue = issues[0]

        # Check error has proper context
        assert issue.error.context is not None
        assert "operation" in issue.error.context
        assert issue.error.context["operation"] == "eval"
        assert issue.error.source_file == "test.ml"

    def test_no_false_positives_safe_operations(self):
        """Test that safe operations don't trigger false positives."""
        code = '''
        // These should be safe
        function evaluate_math(expression) {
            return parse_number(expression);
        }

        import_data = load_from_file("data.json");
        class_name = get_type_name(obj);
        '''

        ast = parse_ml_code(code)
        issues = self.analyzer.analyze(ast)

        # Should have minimal or no issues for safe code
        assert len(issues) == 0

    def test_complex_dangerous_example(self):
        """Test comprehensive dangerous code example."""
        code = '''
        import os;
        import sys;
        import subprocess;

        function dangerous_processor(user_code) {
            // Multiple security issues
            globals_dict = user_code.__globals__;
            result = eval(user_code.expression);
            system_call = __import__("os").system(user_code.command);

            return result;
        }

        capability TooPermissive {
            resource "*";
            allow system;
            allow execute "*";
        }
        '''

        ast = parse_ml_code(code)
        issues = self.analyzer.analyze(ast)

        # Should detect multiple security issues
        assert len(issues) >= 8  # imports + eval + __import__ + reflection + capabilities

        # Verify different categories are detected
        categories = set()
        for issue in issues:
            categories.add(issue.error.context.get("category", "unknown"))

        expected_categories = {
            "unsafe_import", "code_injection", "reflection_abuse",
            "overly_broad_capability", "dangerous_permission"
        }

        # Should have most or all expected categories
        assert len(categories.intersection(expected_categories)) >= 3