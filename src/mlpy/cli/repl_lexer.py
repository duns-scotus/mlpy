"""ML Language Lexer for Syntax Highlighting in REPL.

Provides syntax highlighting for ML language using Pygments lexer.
ML syntax is similar to JavaScript, so we leverage JavascriptLexer
with ML-specific customizations.
"""

from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
    Whitespace,
)


class MLLexer(RegexLexer):
    """Lexer for ML language syntax highlighting.

    Highlights:
    - Keywords: function, return, if, elif, else, while, for, import, etc.
    - Builtin functions: typeof, len, print, int, float, etc.
    - Operators: +, -, *, /, =, ==, !=, etc.
    - Strings: "..." and '...'
    - Numbers: 42, 3.14, 1.5e6, etc.
    - Comments: // and /* */
    - Booleans: true, false
    """

    name = "ML"
    aliases = ["ml"]
    filenames = ["*.ml"]

    tokens = {
        "root": [
            # Whitespace
            (r"\s+", Whitespace),
            # Single-line comments
            (r"//.*?$", Comment.Single),
            # Multi-line comments
            (r"/\*", Comment.Multiline, "comment"),
            # Keywords
            (
                words(
                    (
                        "function",
                        "return",
                        "if",
                        "elif",
                        "else",
                        "while",
                        "for",
                        "in",
                        "break",
                        "continue",
                        "import",
                        "from",
                        "as",
                        "try",
                        "except",
                        "finally",
                        "throw",
                        "new",
                        "delete",
                        "typeof",
                        "true",
                        "false",
                        "null",
                        "undefined",
                    ),
                    suffix=r"\b",
                ),
                Keyword,
            ),
            # Builtin functions (ML-specific)
            (
                words(
                    (
                        "typeof",
                        "len",
                        "print",
                        "input",
                        "int",
                        "float",
                        "str",
                        "bool",
                        "range",
                        "abs",
                        "min",
                        "max",
                        "round",
                        "sorted",
                        "sum",
                        "keys",
                        "values",
                    ),
                    suffix=r"\b",
                ),
                Name.Builtin,
            ),
            # Function calls
            (r"([a-zA-Z_][a-zA-Z0-9_]*)\s*(\()", bygroups(Name.Function, Punctuation)),
            # Numbers
            (r"\d+\.\d*([eE][+-]?\d+)?", Number.Float),  # Float with optional exponent
            (r"\d+[eE][+-]?\d+", Number.Float),  # Integer with exponent (becomes float)
            (r"\d+", Number.Integer),  # Integer
            # Strings
            (r'"(?:[^"\\]|\\.)*"', String.Double),
            (r"'(?:[^'\\]|\\.)*'", String.Single),
            # Operators
            (r"(\+\+|--|&&|\|\||==|!=|<=|>=|=>)", Operator),
            (r"[+\-*/%=<>!&|^~]", Operator),
            # Punctuation
            (r"[{}()\[\],.;:]", Punctuation),
            # Identifiers
            (r"[a-zA-Z_][a-zA-Z0-9_]*", Name),
        ],
        "comment": [
            (r"[^*/]+", Comment.Multiline),
            (r"\*/", Comment.Multiline, "#pop"),
            (r"[*/]", Comment.Multiline),
        ],
    }


# Prompt_toolkit style definitions for ML syntax
ML_STYLE = {
    # Keywords (purple)
    "pygments.keyword": "#ff79c6 bold",
    # Builtin functions (cyan)
    "pygments.name.builtin": "#8be9fd bold",
    # Functions (green)
    "pygments.name.function": "#50fa7b",
    # Strings (yellow)
    "pygments.literal.string": "#f1fa8c",
    "pygments.literal.string.double": "#f1fa8c",
    "pygments.literal.string.single": "#f1fa8c",
    # Numbers (purple)
    "pygments.literal.number": "#bd93f9",
    "pygments.literal.number.integer": "#bd93f9",
    "pygments.literal.number.float": "#bd93f9",
    # Comments (gray, italic)
    "pygments.comment": "#6272a4 italic",
    "pygments.comment.single": "#6272a4 italic",
    "pygments.comment.multiline": "#6272a4 italic",
    # Operators (pink)
    "pygments.operator": "#ff79c6",
    # Punctuation (white)
    "pygments.punctuation": "#f8f8f2",
    # Identifiers (white)
    "pygments.name": "#f8f8f2",
    # Prompt
    "prompt": "#50fa7b bold",
    "continuation": "#ffb86c",
    # Completion
    "completion": "",
    "completion.current": "bg:#44475a #ffffff",
    "completion.menu": "bg:#282a36 #f8f8f2",
    "completion-menu.meta": "bg:#282a36 #6272a4",
    # Scrollbar
    "scrollbar.background": "bg:#44475a",
    "scrollbar.button": "bg:#6272a4",
}
