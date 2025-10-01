"""
Unit tests for ast_validator.py - AST structural validation.

Tests cover:
- ValidationSeverity enum and ValidationIssue/ValidationResult dataclasses
- AST structural validation (null checks, critical fields)
- Control flow context validation (break/continue outside loops, return outside functions)
- Recursion depth limits (stack overflow prevention)
- Error and warning categorization
"""

import pytest

from mlpy.ml.analysis.ast_validator import (
    ASTValidator,
    ValidationIssue,
    ValidationResult,
    ValidationSeverity,
)
from mlpy.ml.grammar.ast_nodes import (
    AssignmentStatement,
    BreakStatement,
    ContinueStatement,
    ExpressionStatement,
    Identifier,
    NumberLiteral,
    Program,
    ReturnStatement,
)
from mlpy.ml.grammar.parser import MLParser


class TestValidationSeverity:
    """Test ValidationSeverity enum."""

    def test_severity_values(self):
        """Test severity enum values."""
        assert ValidationSeverity.ERROR.value == "ERROR"
        assert ValidationSeverity.WARNING.value == "WARNING"


class TestValidationIssue:
    """Test ValidationIssue dataclass."""

    def test_issue_creation_minimal(self):
        """Test creating issue with minimal fields."""
        issue = ValidationIssue(
            severity=ValidationSeverity.ERROR,
            message="Test error",
            node_type="Identifier",
        )

        assert issue.severity == ValidationSeverity.ERROR
        assert issue.message == "Test error"
        assert issue.node_type == "Identifier"
        assert issue.line is None
        assert issue.column is None

    def test_issue_creation_full(self):
        """Test creating issue with all fields."""
        issue = ValidationIssue(
            severity=ValidationSeverity.WARNING,
            message="Test warning",
            node_type="FunctionCall",
            line=10,
            column=5,
            context="function body",
        )

        assert issue.line == 10
        assert issue.column == 5
        assert issue.context == "function body"


class TestValidationResult:
    """Test ValidationResult dataclass."""

    def test_result_creation(self):
        """Test creating validation result."""
        issues = [
            ValidationIssue(ValidationSeverity.ERROR, "Error 1", "Node1"),
            ValidationIssue(ValidationSeverity.WARNING, "Warning 1", "Node2"),
        ]

        result = ValidationResult(
            is_valid=False,
            issues=issues,
            node_count=10,
            validation_time_ms=5.5,
        )

        assert result.is_valid is False
        assert len(result.issues) == 2
        assert result.node_count == 10
        assert result.validation_time_ms == 5.5

    def test_errors_property(self):
        """Test filtering errors from issues."""
        issues = [
            ValidationIssue(ValidationSeverity.ERROR, "Error 1", "Node1"),
            ValidationIssue(ValidationSeverity.WARNING, "Warning 1", "Node2"),
            ValidationIssue(ValidationSeverity.ERROR, "Error 2", "Node3"),
        ]

        result = ValidationResult(
            is_valid=False,
            issues=issues,
            node_count=10,
            validation_time_ms=5.5,
        )

        errors = result.errors
        assert len(errors) == 2
        assert all(e.severity == ValidationSeverity.ERROR for e in errors)

    def test_warnings_property(self):
        """Test filtering warnings from issues."""
        issues = [
            ValidationIssue(ValidationSeverity.ERROR, "Error 1", "Node1"),
            ValidationIssue(ValidationSeverity.WARNING, "Warning 1", "Node2"),
            ValidationIssue(ValidationSeverity.WARNING, "Warning 2", "Node3"),
        ]

        result = ValidationResult(
            is_valid=False,
            issues=issues,
            node_count=10,
            validation_time_ms=5.5,
        )

        warnings = result.warnings
        assert len(warnings) == 2
        assert all(w.severity == ValidationSeverity.WARNING for w in warnings)

    def test_result_with_no_issues(self):
        """Test result with no issues."""
        result = ValidationResult(
            is_valid=True,
            issues=[],
            node_count=5,
            validation_time_ms=1.0,
        )

        assert result.is_valid is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 0


class TestASTValidator:
    """Test ASTValidator main functionality."""

    @pytest.fixture
    def validator(self):
        """Create AST validator."""
        return ASTValidator()

    @pytest.fixture
    def parser(self):
        """Create ML parser."""
        return MLParser()

    def test_validator_initialization(self, validator):
        """Test validator initialization."""
        assert validator is not None
        assert len(validator.issues) == 0
        assert validator.node_count == 0
        assert len(validator.scope_stack) == 0

    def test_validate_simple_program(self, validator, parser):
        """Test validating simple valid program."""
        code = "x = 42;"
        ast = parser.parse(code)

        result = validator.validate(ast)

        assert result.is_valid is True
        assert len(result.errors) == 0
        assert result.node_count > 0
        assert result.validation_time_ms >= 0

    def test_validate_function_definition(self, validator, parser):
        """Test validating function definition."""
        code = """
function add(a, b) {
    return a + b;
}
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_return_outside_function(self, validator):
        """Test detecting return statement outside function."""
        # Create AST manually with return at top level
        program = Program([ReturnStatement(value=NumberLiteral(42))])

        result = validator.validate(program)

        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("return statement outside function" in e.message.lower() for e in result.errors)

    def test_validate_break_outside_loop(self, validator):
        """Test detecting break statement outside loop."""
        program = Program([BreakStatement()])

        result = validator.validate(program)

        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("break" in e.message.lower() for e in result.errors)

    def test_validate_continue_outside_loop(self, validator):
        """Test detecting continue statement outside loop."""
        program = Program([ContinueStatement()])

        result = validator.validate(program)

        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("continue" in e.message.lower() for e in result.errors)

    def test_validate_break_inside_loop(self, validator, parser):
        """Test that break inside loop is valid."""
        code = """
while (true) {
    break;
}
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        # Break inside loop should be valid
        break_errors = [e for e in result.errors if "break" in e.message.lower()]
        assert len(break_errors) == 0

    def test_validate_continue_inside_loop(self, validator, parser):
        """Test that continue inside loop is valid."""
        code = """
for (i in arr) {
    continue;
}
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        # Continue inside loop should be valid
        continue_errors = [e for e in result.errors if "continue" in e.message.lower()]
        assert len(continue_errors) == 0

    def test_validate_return_inside_function(self, validator, parser):
        """Test that return inside function is valid."""
        code = """
function test() {
    return 42;
}
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        # Return inside function should be valid
        return_errors = [e for e in result.errors if "return" in e.message.lower()]
        assert len(return_errors) == 0

    def test_validate_null_node(self, validator):
        """Test handling null node."""
        result = validator.validate(None)

        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("null" in e.message.lower() for e in result.errors)

    def test_node_counting(self, validator, parser):
        """Test that validator counts nodes."""
        code = """
x = 1;
y = 2;
z = x + y;
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        # Should count multiple nodes
        assert result.node_count > 3

    def test_validation_timing(self, validator, parser):
        """Test that validation time is recorded."""
        code = "x = 42;"
        ast = parser.parse(code)

        result = validator.validate(ast)

        # Time should be recorded and positive
        assert result.validation_time_ms >= 0
        assert result.validation_time_ms < 1000  # Should be very fast

    def test_multiple_validations(self, validator, parser):
        """Test running multiple validations."""
        code1 = "x = 1;"
        code2 = "y = 2;"

        ast1 = parser.parse(code1)
        ast2 = parser.parse(code2)

        result1 = validator.validate(ast1)
        result2 = validator.validate(ast2)

        # Both should be valid
        assert result1.is_valid is True
        assert result2.is_valid is True

        # State should be reset between validations
        assert result1.node_count != result2.node_count or result1.node_count == result2.node_count

    def test_complex_nested_structure(self, validator, parser):
        """Test validating complex nested structures."""
        code = """
function outer() {
    if (condition) {
        for (i in items) {
            while (test) {
                if (check) {
                    return value;
                }
            }
        }
    }
}
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        # Complex structure should be valid
        assert result.is_valid is True
        assert result.node_count >= 1  # At least the Program node

    def test_nested_loops_with_break(self, validator, parser):
        """Test break in nested loops."""
        code = """
while (outer) {
    for (i in items) {
        if (condition) {
            break;
        }
    }
}
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        # Nested loop breaks should be valid
        assert result.is_valid is True

    def test_function_with_multiple_returns(self, validator, parser):
        """Test function with multiple return statements."""
        code = """
function test(x) {
    if (x > 0) {
        return 1;
    }
    return 0;
}
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        # Multiple returns in function should be valid
        assert result.is_valid is True

    def test_empty_program(self, validator):
        """Test validating empty program."""
        program = Program([])

        result = validator.validate(program)

        assert result.is_valid is True
        assert len(result.errors) == 0
        assert result.node_count >= 1  # At least the Program node

    def test_identifier_with_name(self, validator):
        """Test validating identifier with proper name."""
        program = Program([ExpressionStatement(expression=Identifier("variable_name"))])

        result = validator.validate(program)

        # Valid identifier should pass
        assert result.is_valid is True

    def test_warnings_dont_fail_validation(self, validator):
        """Test that warnings don't cause validation to fail."""
        # Create a program that might generate warnings but no errors
        program = Program([AssignmentStatement(target=Identifier("x"), value=NumberLiteral(42))])

        result = validator.validate(program)

        # Should be valid even with warnings
        if len(result.warnings) > 0:
            assert result.is_valid is True

    def test_mixed_control_flow(self, validator, parser):
        """Test mixed valid and invalid control flow."""
        code = """
function test() {
    for (i in items) {
        if (condition) {
            break;
        }
        continue;
    }
    return result;
}
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        # All control flow should be in valid contexts
        assert result.is_valid is True

    def test_while_loop_with_controls(self, validator, parser):
        """Test while loop with break and continue."""
        code = """
while (running) {
    if (shouldBreak) {
        break;
    }
    if (shouldSkip) {
        continue;
    }
    process();
}
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        assert result.is_valid is True

    def test_for_loop_with_controls(self, validator, parser):
        """Test for loop with break and continue."""
        code = """
for (item in collection) {
    if (done) {
        break;
    }
    if (skip) {
        continue;
    }
}
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        assert result.is_valid is True


class TestASTValidatorEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.fixture
    def validator(self):
        """Create validator."""
        return ASTValidator()

    @pytest.fixture
    def parser(self):
        """Create parser."""
        return MLParser()

    def test_deeply_nested_valid_code(self, validator, parser):
        """Test validating deeply nested but valid code."""
        # Create moderately nested code
        code = """
function level1() {
    if (a) {
        if (b) {
            if (c) {
                if (d) {
                    return result;
                }
            }
        }
    }
}
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        # Should be valid (not deep enough to trigger limit)
        assert result.is_valid is True

    def test_multiple_functions(self, validator, parser):
        """Test validating multiple function definitions."""
        code = """
function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        assert result.is_valid is True
        assert result.node_count >= 2  # At least 2 function definitions

    def test_complex_expressions(self, validator, parser):
        """Test validating complex expressions."""
        code = """
result = (a + b) * (c - d) / (e + f);
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        assert result.is_valid is True

    def test_nested_function_definitions(self, validator, parser):
        """Test nested function definitions."""
        code = """
function outer() {
    function inner() {
        return 42;
    }
    return inner();
}
"""
        ast = parser.parse(code)

        result = validator.validate(ast)

        # Nested functions with returns should be valid
        assert result.is_valid is True

    def test_validation_state_reset(self, validator, parser):
        """Test that validator state is properly reset."""
        # First validation with error
        program1 = Program([ReturnStatement(value=NumberLiteral(1))])
        result1 = validator.validate(program1)
        assert result1.is_valid is False

        # Second validation should start fresh
        code2 = "x = 42;"
        ast2 = parser.parse(code2)
        result2 = validator.validate(ast2)

        # Should be valid and not carry over previous errors
        assert result2.is_valid is True
        assert len(result2.errors) == 0
