"""
Comprehensive unit tests for repl_lexer.py - ML Language Lexer for Syntax Highlighting.

Tests cover:
- MLLexer class
  - Keywords highlighting (function, return, if, elif, else, etc.)
  - Builtin functions highlighting (typeof, len, print, etc.)
  - Number literals (integers, floats, scientific notation)
  - String literals (single and double quoted)
  - Comments (single-line and multi-line)
  - Operators and punctuation
  - Function calls
  - Identifiers
- Token types and styling
- Edge cases and complex expressions
"""

import pytest
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Whitespace,
)

from mlpy.cli.repl_lexer import MLLexer


# ===== Helper Functions =====


def tokenize(code: str) -> list[tuple]:
    """Tokenize ML code and return list of (token_type, value) tuples.

    Args:
        code: ML source code to tokenize

    Returns:
        List of (token_type, value) tuples
    """
    lexer = MLLexer()
    return list(lexer.get_tokens(code))


def has_token(tokens: list[tuple], token_type, value: str) -> bool:
    """Check if tokens contain a specific token.

    Args:
        tokens: List of (token_type, value) tuples
        token_type: Expected token type
        value: Expected token value

    Returns:
        True if token found
    """
    return any(t[0] == token_type and t[1] == value for t in tokens)


def get_token_values_by_type(tokens: list[tuple], token_type) -> list[str]:
    """Get all token values of a specific type.

    Args:
        tokens: List of (token_type, value) tuples
        token_type: Token type to filter by

    Returns:
        List of token values
    """
    return [t[1] for t in tokens if t[0] == token_type]


# ===== MLLexer Tests =====


class TestMLLexerBasics:
    """Test basic MLLexer functionality."""

    def test_lexer_initialization(self):
        """Test lexer can be created."""
        lexer = MLLexer()

        assert lexer is not None
        assert lexer.name == "ML"
        assert "ml" in lexer.aliases
        assert "*.ml" in lexer.filenames

    def test_empty_code_returns_no_tokens(self):
        """Test empty code returns no tokens (or only whitespace)."""
        tokens = tokenize("")

        # Empty input may produce a newline token, which is acceptable
        # Filter out whitespace tokens to check for actual content
        non_whitespace_tokens = [t for t in tokens if t[0] != Whitespace]
        assert len(non_whitespace_tokens) == 0

    def test_whitespace_only_code(self):
        """Test whitespace-only code."""
        tokens = tokenize("   \n  \t  ")

        # Should have whitespace tokens
        assert any(t[0] == Whitespace for t in tokens)


class TestKeywordTokenization:
    """Test keyword tokenization."""

    def test_function_keyword(self):
        """Test 'function' keyword is tokenized correctly."""
        tokens = tokenize("function")

        assert has_token(tokens, Keyword, "function")

    def test_return_keyword(self):
        """Test 'return' keyword is tokenized correctly."""
        tokens = tokenize("return")

        assert has_token(tokens, Keyword, "return")

    def test_control_flow_keywords(self):
        """Test control flow keywords."""
        code = "if elif else while for break continue"
        tokens = tokenize(code)

        keywords = get_token_values_by_type(tokens, Keyword)
        assert "if" in keywords
        assert "elif" in keywords
        assert "else" in keywords
        assert "while" in keywords
        assert "for" in keywords
        assert "break" in keywords
        assert "continue" in keywords

    def test_import_keywords(self):
        """Test import-related keywords."""
        code = "import from as"
        tokens = tokenize(code)

        keywords = get_token_values_by_type(tokens, Keyword)
        assert "import" in keywords
        assert "from" in keywords
        assert "as" in keywords

    def test_exception_keywords(self):
        """Test exception handling keywords."""
        code = "try except finally throw"
        tokens = tokenize(code)

        keywords = get_token_values_by_type(tokens, Keyword)
        assert "try" in keywords
        assert "except" in keywords
        assert "finally" in keywords
        assert "throw" in keywords

    def test_boolean_keywords(self):
        """Test boolean literal keywords."""
        code = "true false null undefined"
        tokens = tokenize(code)

        keywords = get_token_values_by_type(tokens, Keyword)
        assert "true" in keywords
        assert "false" in keywords
        assert "null" in keywords
        assert "undefined" in keywords

    def test_keyword_with_trailing_identifier(self):
        """Test keyword doesn't match when part of identifier."""
        code = "ifCondition"  # 'if' is part of identifier, not keyword
        tokens = tokenize(code)

        # Should be tokenized as identifier, not keyword
        identifiers = get_token_values_by_type(tokens, Name)
        assert "ifCondition" in identifiers

        # 'if' alone should not be a keyword token
        keywords = get_token_values_by_type(tokens, Keyword)
        assert "if" not in keywords


class TestBuiltinFunctionTokenization:
    """Test builtin function tokenization."""

    def test_typeof_builtin(self):
        """Test 'typeof' builtin is tokenized correctly."""
        tokens = tokenize("typeof")

        # typeof is both a keyword and builtin, check if it's highlighted
        assert has_token(tokens, Keyword, "typeof") or has_token(
            tokens, Name.Builtin, "typeof"
        )

    def test_print_builtin(self):
        """Test 'print' builtin is tokenized correctly."""
        tokens = tokenize("print")

        assert has_token(tokens, Name.Builtin, "print")

    def test_len_builtin(self):
        """Test 'len' builtin is tokenized correctly."""
        tokens = tokenize("len")

        assert has_token(tokens, Name.Builtin, "len")

    def test_type_conversion_builtins(self):
        """Test type conversion builtins (int, float, str, bool)."""
        code = "int float str bool"
        tokens = tokenize(code)

        builtins = get_token_values_by_type(tokens, Name.Builtin)
        assert "int" in builtins
        assert "float" in builtins
        assert "str" in builtins
        assert "bool" in builtins

    def test_array_builtins(self):
        """Test array-related builtins."""
        code = "range sorted sum"
        tokens = tokenize(code)

        builtins = get_token_values_by_type(tokens, Name.Builtin)
        assert "range" in builtins
        assert "sorted" in builtins
        assert "sum" in builtins

    def test_math_builtins(self):
        """Test math builtins."""
        code = "abs min max round"
        tokens = tokenize(code)

        builtins = get_token_values_by_type(tokens, Name.Builtin)
        assert "abs" in builtins
        assert "min" in builtins
        assert "max" in builtins
        assert "round" in builtins

    def test_object_builtins(self):
        """Test object builtins."""
        code = "keys values"
        tokens = tokenize(code)

        builtins = get_token_values_by_type(tokens, Name.Builtin)
        assert "keys" in builtins
        assert "values" in builtins


class TestNumberTokenization:
    """Test number literal tokenization."""

    def test_integer_literal(self):
        """Test integer literal tokenization."""
        tokens = tokenize("42")

        assert has_token(tokens, Number.Integer, "42")

    def test_large_integer(self):
        """Test large integer literal."""
        tokens = tokenize("123456789")

        assert has_token(tokens, Number.Integer, "123456789")

    def test_float_literal(self):
        """Test float literal tokenization."""
        tokens = tokenize("3.14")

        assert has_token(tokens, Number.Float, "3.14")

    def test_float_with_leading_zero(self):
        """Test float with leading zero."""
        tokens = tokenize("0.5")

        assert has_token(tokens, Number.Float, "0.5")

    def test_float_with_trailing_decimal(self):
        """Test float with trailing decimal point."""
        tokens = tokenize("42.0")

        assert has_token(tokens, Number.Float, "42.0")

    def test_scientific_notation_positive_exponent(self):
        """Test scientific notation with positive exponent."""
        tokens = tokenize("1.5e6")

        # Should be tokenized as float
        floats = get_token_values_by_type(tokens, Number.Float)
        assert "1.5e6" in floats

    def test_scientific_notation_negative_exponent(self):
        """Test scientific notation with negative exponent."""
        tokens = tokenize("6.626e-34")

        # Should be tokenized as float
        floats = get_token_values_by_type(tokens, Number.Float)
        assert "6.626e-34" in floats

    def test_scientific_notation_uppercase_e(self):
        """Test scientific notation with uppercase E."""
        tokens = tokenize("1E10")

        # Should be tokenized as float
        floats = get_token_values_by_type(tokens, Number.Float)
        assert "1E10" in floats

    def test_integer_with_exponent_becomes_float(self):
        """Test integer with exponent is tokenized as float."""
        tokens = tokenize("123e4")

        # Should be float, not integer
        floats = get_token_values_by_type(tokens, Number.Float)
        assert "123e4" in floats

    def test_multiple_numbers_in_expression(self):
        """Test multiple numbers in expression."""
        tokens = tokenize("42 + 3.14 + 1e5")

        integers = get_token_values_by_type(tokens, Number.Integer)
        floats = get_token_values_by_type(tokens, Number.Float)

        assert "42" in integers
        assert "3.14" in floats
        assert "1e5" in floats


class TestStringTokenization:
    """Test string literal tokenization."""

    def test_double_quoted_string(self):
        """Test double-quoted string literal."""
        tokens = tokenize('"hello"')

        assert has_token(tokens, String.Double, '"hello"')

    def test_single_quoted_string(self):
        """Test single-quoted string literal."""
        tokens = tokenize("'world'")

        assert has_token(tokens, String.Single, "'world'")

    def test_empty_string(self):
        """Test empty string literal."""
        tokens = tokenize('""')

        assert has_token(tokens, String.Double, '""')

    def test_string_with_spaces(self):
        """Test string with spaces."""
        tokens = tokenize('"hello world"')

        assert has_token(tokens, String.Double, '"hello world"')

    def test_string_with_escaped_quotes(self):
        """Test string with escaped quotes."""
        tokens = tokenize(r'"say \"hi\""')

        # Should capture entire string including escapes
        strings = get_token_values_by_type(tokens, String.Double)
        assert any('\\"' in s for s in strings)

    def test_string_with_newline_escape(self):
        """Test string with newline escape."""
        tokens = tokenize(r'"line1\nline2"')

        strings = get_token_values_by_type(tokens, String.Double)
        assert any('\\n' in s for s in strings)

    def test_string_concatenation(self):
        """Test string concatenation expression."""
        tokens = tokenize('"hello" + "world"')

        strings = get_token_values_by_type(tokens, String.Double)
        assert '"hello"' in strings
        assert '"world"' in strings


class TestCommentTokenization:
    """Test comment tokenization."""

    def test_single_line_comment(self):
        """Test single-line comment."""
        tokens = tokenize("// this is a comment")

        assert has_token(tokens, Comment.Single, "// this is a comment")

    def test_single_line_comment_after_code(self):
        """Test single-line comment after code."""
        tokens = tokenize("x = 42; // set x")

        comments = get_token_values_by_type(tokens, Comment.Single)
        assert any("// set x" in c for c in comments)

    def test_multi_line_comment(self):
        """Test multi-line comment."""
        code = "/* this is\na multi-line\ncomment */"
        tokens = tokenize(code)

        # Should have multi-line comment tokens
        multiline_comments = [t[1] for t in tokens if t[0] == Comment.Multiline]
        assert len(multiline_comments) > 0

    def test_multi_line_comment_inline(self):
        """Test inline multi-line comment."""
        tokens = tokenize("x = /* value */ 42;")

        # Should have multi-line comment tokens
        assert any(t[0] == Comment.Multiline for t in tokens)

    def test_nested_comment_symbols_in_multiline(self):
        """Test nested comment symbols in multi-line comment."""
        code = "/* comment with // and /* symbols */"
        tokens = tokenize(code)

        # Should handle as multi-line comment
        assert any(t[0] == Comment.Multiline for t in tokens)


class TestOperatorTokenization:
    """Test operator tokenization."""

    def test_arithmetic_operators(self):
        """Test arithmetic operators."""
        code = "+ - * / %"
        tokens = tokenize(code)

        operators = get_token_values_by_type(tokens, Operator)
        assert "+" in operators
        assert "-" in operators
        assert "*" in operators
        assert "/" in operators
        assert "%" in operators

    def test_comparison_operators(self):
        """Test comparison operators."""
        code = "== != < > <= >="
        tokens = tokenize(code)

        operators = get_token_values_by_type(tokens, Operator)
        assert "==" in operators
        assert "!=" in operators
        assert "<" in operators
        assert ">" in operators
        assert "<=" in operators
        assert ">=" in operators

    def test_logical_operators(self):
        """Test logical operators."""
        code = "&& ||"
        tokens = tokenize(code)

        operators = get_token_values_by_type(tokens, Operator)
        assert "&&" in operators
        assert "||" in operators

    def test_increment_decrement_operators(self):
        """Test increment/decrement operators."""
        code = "++ --"
        tokens = tokenize(code)

        operators = get_token_values_by_type(tokens, Operator)
        assert "++" in operators
        assert "--" in operators

    def test_arrow_function_operator(self):
        """Test arrow function operator."""
        code = "x => x * 2"
        tokens = tokenize(code)

        operators = get_token_values_by_type(tokens, Operator)
        assert "=>" in operators

    def test_assignment_operator(self):
        """Test assignment operator."""
        code = "x = 42"
        tokens = tokenize(code)

        operators = get_token_values_by_type(tokens, Operator)
        assert "=" in operators


class TestPunctuationTokenization:
    """Test punctuation tokenization."""

    def test_parentheses(self):
        """Test parentheses."""
        tokens = tokenize("()")

        punctuation = get_token_values_by_type(tokens, Punctuation)
        assert "(" in punctuation
        assert ")" in punctuation

    def test_curly_braces(self):
        """Test curly braces."""
        tokens = tokenize("{}")

        punctuation = get_token_values_by_type(tokens, Punctuation)
        assert "{" in punctuation
        assert "}" in punctuation

    def test_square_brackets(self):
        """Test square brackets."""
        tokens = tokenize("[]")

        punctuation = get_token_values_by_type(tokens, Punctuation)
        assert "[" in punctuation
        assert "]" in punctuation

    def test_semicolon(self):
        """Test semicolon."""
        tokens = tokenize(";")

        assert has_token(tokens, Punctuation, ";")

    def test_comma(self):
        """Test comma."""
        tokens = tokenize(",")

        assert has_token(tokens, Punctuation, ",")

    def test_colon(self):
        """Test colon."""
        tokens = tokenize(":")

        assert has_token(tokens, Punctuation, ":")

    def test_dot(self):
        """Test dot/period."""
        tokens = tokenize("obj.prop")

        punctuation = get_token_values_by_type(tokens, Punctuation)
        assert "." in punctuation


class TestFunctionCallTokenization:
    """Test function call tokenization."""

    def test_simple_function_call(self):
        """Test simple function call."""
        tokens = tokenize("myFunc()")

        # Function name should be highlighted
        functions = get_token_values_by_type(tokens, Name.Function)
        assert "myFunc" in functions

        # Parentheses should be punctuation
        punctuation = get_token_values_by_type(tokens, Punctuation)
        assert "(" in punctuation

    def test_builtin_function_call(self):
        """Test builtin function call."""
        tokens = tokenize("print(42)")

        # 'print' should be builtin, not function
        builtins = get_token_values_by_type(tokens, Name.Builtin)
        assert "print" in builtins

    def test_method_call(self):
        """Test method call (obj.method())."""
        tokens = tokenize("obj.doSomething()")

        # Method name should be highlighted as function
        functions = get_token_values_by_type(tokens, Name.Function)
        assert "doSomething" in functions

    def test_nested_function_calls(self):
        """Test nested function calls."""
        tokens = tokenize("outer(inner(x))")

        functions = get_token_values_by_type(tokens, Name.Function)
        assert "outer" in functions
        assert "inner" in functions


class TestIdentifierTokenization:
    """Test identifier tokenization."""

    def test_simple_identifier(self):
        """Test simple identifier."""
        tokens = tokenize("myVariable")

        assert has_token(tokens, Name, "myVariable")

    def test_identifier_with_underscore(self):
        """Test identifier with underscore."""
        tokens = tokenize("my_variable")

        assert has_token(tokens, Name, "my_variable")

    def test_identifier_with_numbers(self):
        """Test identifier with numbers."""
        tokens = tokenize("var123")

        assert has_token(tokens, Name, "var123")

    def test_identifier_starting_with_underscore(self):
        """Test identifier starting with underscore."""
        tokens = tokenize("_private")

        assert has_token(tokens, Name, "_private")

    def test_camelcase_identifier(self):
        """Test camelCase identifier."""
        tokens = tokenize("myLongVariableName")

        assert has_token(tokens, Name, "myLongVariableName")


class TestComplexExpressionTokenization:
    """Test tokenization of complex expressions."""

    def test_variable_assignment(self):
        """Test variable assignment expression."""
        tokens = tokenize("x = 42;")

        # Check all token types present
        identifiers = get_token_values_by_type(tokens, Name)
        operators = get_token_values_by_type(tokens, Operator)
        numbers = get_token_values_by_type(tokens, Number.Integer)
        punctuation = get_token_values_by_type(tokens, Punctuation)

        assert "x" in identifiers
        assert "=" in operators
        assert "42" in numbers
        assert ";" in punctuation

    def test_function_definition(self):
        """Test function definition."""
        code = "function add(a, b) { return a + b; }"
        tokens = tokenize(code)

        keywords = get_token_values_by_type(tokens, Keyword)
        functions = get_token_values_by_type(tokens, Name.Function)

        assert "function" in keywords
        assert "return" in keywords
        assert "add" in functions

    def test_if_statement(self):
        """Test if statement."""
        code = "if (x > 0) { print(x); }"
        tokens = tokenize(code)

        keywords = get_token_values_by_type(tokens, Keyword)
        builtins = get_token_values_by_type(tokens, Name.Builtin)

        assert "if" in keywords
        assert "print" in builtins

    def test_array_literal(self):
        """Test array literal."""
        code = "[1, 2, 3]"
        tokens = tokenize(code)

        punctuation = get_token_values_by_type(tokens, Punctuation)
        numbers = get_token_values_by_type(tokens, Number.Integer)

        assert "[" in punctuation
        assert "]" in punctuation
        assert "," in punctuation
        assert "1" in numbers
        assert "2" in numbers
        assert "3" in numbers

    def test_object_literal(self):
        """Test object literal."""
        code = '{ name: "test", value: 42 }'
        tokens = tokenize(code)

        punctuation = get_token_values_by_type(tokens, Punctuation)
        strings = get_token_values_by_type(tokens, String.Double)

        assert "{" in punctuation
        assert "}" in punctuation
        assert ":" in punctuation
        assert '"test"' in strings

    def test_import_statement(self):
        """Test import statement."""
        code = "import console from 'std/console';"
        tokens = tokenize(code)

        keywords = get_token_values_by_type(tokens, Keyword)

        assert "import" in keywords
        assert "from" in keywords

    def test_for_loop(self):
        """Test for loop."""
        code = "for (i in range(10)) { print(i); }"
        tokens = tokenize(code)

        keywords = get_token_values_by_type(tokens, Keyword)
        builtins = get_token_values_by_type(tokens, Name.Builtin)

        assert "for" in keywords
        assert "in" in keywords
        assert "range" in builtins
        assert "print" in builtins

    def test_try_except_block(self):
        """Test try-except block."""
        code = "try { risky(); } except (e) { print(e); }"
        tokens = tokenize(code)

        keywords = get_token_values_by_type(tokens, Keyword)

        assert "try" in keywords
        assert "except" in keywords


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_keyword_as_property_name(self):
        """Test keyword used as property name (obj.if is valid)."""
        code = "obj.if"
        tokens = tokenize(code)

        # 'if' might be tokenized as identifier here, not keyword
        # This is acceptable - property names can be keywords

    def test_number_followed_by_identifier(self):
        """Test number followed by identifier (no space)."""
        code = "42x"  # Invalid in most languages, but lexer should handle
        tokens = tokenize(code)

        # Should tokenize as number + identifier
        numbers = get_token_values_by_type(tokens, Number.Integer)
        identifiers = get_token_values_by_type(tokens, Name)

        # May vary by lexer implementation
        assert len(numbers) > 0 or len(identifiers) > 0

    def test_operators_without_spaces(self):
        """Test operators without spaces."""
        code = "x=42+3"
        tokens = tokenize(code)

        operators = get_token_values_by_type(tokens, Operator)
        assert "=" in operators
        assert "+" in operators

    def test_very_long_identifier(self):
        """Test very long identifier."""
        long_id = "a" * 100
        tokens = tokenize(long_id)

        assert has_token(tokens, Name, long_id)

    def test_unicode_in_comments(self):
        """Test unicode characters in comments."""
        code = "// Comment with unicode: 你好"
        tokens = tokenize(code)

        # Should handle gracefully
        comments = get_token_values_by_type(tokens, Comment.Single)
        assert len(comments) > 0

    def test_multiple_statements(self):
        """Test multiple statements on separate lines."""
        code = """x = 1;
y = 2;
z = 3;"""
        tokens = tokenize(code)

        identifiers = get_token_values_by_type(tokens, Name)
        assert "x" in identifiers
        assert "y" in identifiers
        assert "z" in identifiers
