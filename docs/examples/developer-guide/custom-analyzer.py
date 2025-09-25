"""
Custom Security Analyzer Example
Demonstrates how to create custom security analysis rules
"""

from mlpy.ml.analysis.base_analyzer import BaseAnalyzer
from mlpy.ml.analysis.security_issue import SecurityIssue, Severity
from mlpy.ml.grammar.ast_nodes import FunctionCall, StringLiteral

class CustomDatabaseAnalyzer(BaseAnalyzer):
    """
    Custom analyzer that detects potential database security issues.
    """

    def __init__(self):
        super().__init__()
        self.dangerous_db_functions = {
            'execute_raw_sql',
            'run_query',
            'db_execute',
            'execute_statement'
        }

    def analyze(self, ast_node):
        """Analyze AST node for custom security issues."""
        issues = []

        if isinstance(ast_node, FunctionCall):
            issues.extend(self._check_database_calls(ast_node))

        # Recursively analyze child nodes
        for child in ast_node.get_children():
            issues.extend(self.analyze(child))

        return issues

    def _check_database_calls(self, node):
        """Check for dangerous database function calls."""
        issues = []

        if node.name in self.dangerous_db_functions:
            # Check if query is dynamically constructed
            for arg in node.arguments:
                if self._is_dynamic_string(arg):
                    issue = SecurityIssue(
                        issue_type="SQL_INJECTION_RISK",
                        severity=Severity.HIGH,
                        message=f"Potential SQL injection in {node.name}() call with dynamic query",
                        line_number=node.line_number,
                        column=node.column,
                        code_snippet=str(node),
                        cwe_id=89,  # SQL Injection
                        recommendation="Use parameterized queries or prepared statements"
                    )
                    issues.append(issue)

        return issues

    def _is_dynamic_string(self, node):
        """Check if a string is dynamically constructed."""
        # Simple heuristic: if it's not a string literal, it might be dynamic
        return not isinstance(node, StringLiteral)


class CustomCapabilityAnalyzer(BaseAnalyzer):
    """
    Custom analyzer for capability-specific security rules.
    """

    def __init__(self):
        super().__init__()
        self.required_capabilities = {
            'file_read': ['read_file', 'load_data', 'import_csv'],
            'file_write': ['write_file', 'save_data', 'export_csv'],
            'network': ['http_request', 'fetch_url', 'send_email'],
            'system': ['execute_command', 'run_process', 'get_env']
        }

    def analyze(self, ast_node):
        """Analyze for capability violations."""
        issues = []

        if isinstance(ast_node, FunctionCall):
            issues.extend(self._check_capability_requirements(ast_node))

        for child in ast_node.get_children():
            issues.extend(self.analyze(child))

        return issues

    def _check_capability_requirements(self, node):
        """Check if function call requires specific capabilities."""
        issues = []

        for capability, functions in self.required_capabilities.items():
            if node.name in functions:
                # In a real implementation, you'd check if the current context
                # has the required capability token
                if not self._has_capability(capability):
                    issue = SecurityIssue(
                        issue_type="MISSING_CAPABILITY",
                        severity=Severity.MEDIUM,
                        message=f"Function {node.name}() requires '{capability}' capability",
                        line_number=node.line_number,
                        column=node.column,
                        code_snippet=str(node),
                        recommendation=f"Add capability requirement: capability({capability})"
                    )
                    issues.append(issue)

        return issues

    def _has_capability(self, capability):
        """Check if current context has the required capability."""
        # Placeholder - in real implementation, check capability context
        return False


# Example usage
def demonstrate_custom_analyzers():
    """Demonstrate how to use custom analyzers."""

    from mlpy.ml.parser import MLParser
    from mlpy.ml.analysis.analyzer_registry import AnalyzerRegistry

    # Sample ML code with potential issues
    ml_code = '''
    capability(file_read) function load_user_data(user_id) {
        // This should be OK - has capability
        data = read_file("users/" + user_id + ".json")
        return data
    }

    function dangerous_query(user_input) {
        // This should trigger SQL injection warning
        query = "SELECT * FROM users WHERE name = '" + user_input + "'"
        return execute_raw_sql(query)
    }

    function unauthorized_access() {
        // This should trigger capability warning
        secret_data = read_file("/etc/passwd")
        return secret_data
    }
    '''

    # Parse the code
    parser = MLParser()
    ast = parser.parse_string(ml_code)

    # Register custom analyzers
    registry = AnalyzerRegistry()
    registry.register_analyzer('custom_db', CustomDatabaseAnalyzer())
    registry.register_analyzer('custom_capability', CustomCapabilityAnalyzer())

    # Run analysis
    all_issues = []
    for analyzer_name, analyzer in registry.get_analyzers():
        issues = analyzer.analyze(ast)
        all_issues.extend(issues)

    # Report results
    print(f"Found {len(all_issues)} security issues:")
    for issue in all_issues:
        print(f"  [{issue.severity.name}] {issue.issue_type}: {issue.message}")
        print(f"    Line {issue.line_number}: {issue.code_snippet}")
        print(f"    Recommendation: {issue.recommendation}")
        print()

    return all_issues


if __name__ == "__main__":
    print("=== Custom Security Analyzer Demo ===")
    demonstrate_custom_analyzers()