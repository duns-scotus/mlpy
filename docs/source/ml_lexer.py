"""
Pygments lexer for ML programming language syntax highlighting.
Updated to match actual ML grammar and provide accurate, beautiful highlighting.

Version: 2.0
Date: October 27, 2025
"""

from pygments.lexer import RegexLexer, words, bygroups, include
from pygments.token import (
    Comment, Keyword, Name, Number, Operator, Punctuation,
    String, Text, Whitespace
)


class MLLexer(RegexLexer):
    """Lexer for ML programming language with accurate syntax highlighting."""

    name = 'ML'
    aliases = ['ml']
    filenames = ['*.ml']
    mimetypes = ['text/x-ml']

    # ============================================================
    # KEYWORD DEFINITIONS (from ml.lark grammar)
    # ============================================================

    keywords_control = [
        'if', 'elif', 'else', 'while', 'for', 'break', 'continue', 'in'
    ]

    keywords_function = [
        'function', 'return', 'fn'  # fn for arrow functions
    ]

    keywords_import = [
        'import', 'from', 'as'
    ]

    keywords_exception = [
        'try', 'except', 'finally', 'throw'
    ]

    keywords_capability = [
        'capability', 'resource', 'allow'
    ]

    keywords_scope = [
        'nonlocal'
    ]

    # Permission types (special keywords in capability declarations)
    keywords_permission = [
        'read', 'write', 'execute', 'network', 'system'
    ]

    # Boolean literals
    boolean_literals = [
        'true', 'false', 'null', 'undefined'
    ]

    # Combine all keywords
    all_keywords = (
        keywords_control + keywords_function + keywords_import +
        keywords_exception + keywords_capability + keywords_scope
    )

    # ============================================================
    # BUILTIN FUNCTIONS (from builtin.py)
    # Updated: October 27, 2025 - Complete list from src/mlpy/stdlib/builtin.py
    # ============================================================

    builtins_type = [
        'int', 'float', 'str', 'bool', 'typeof', 'isinstance'
    ]

    builtins_collection = [
        'len', 'range', 'enumerate', 'keys', 'values', 'sorted', 'sum', 'zip'
    ]

    builtins_io = [
        'print', 'input'
    ]

    builtins_math = [
        'abs', 'min', 'max', 'round'
    ]

    builtins_introspection = [
        'help', 'methods', 'modules', 'available_modules', 'has_module', 'module_info'
    ]

    builtins_capability = [
        'hasCapability', 'getCapabilities', 'getCapabilityInfo'
    ]

    builtins_dynamic = [
        'hasattr', 'getattr', 'call', 'callable'
    ]

    builtins_iteration = [
        'iter', 'next', 'reversed', 'all', 'any'
    ]

    builtins_conversion = [
        'chr', 'ord', 'hex', 'bin', 'oct', 'repr', 'format'
    ]

    all_builtins = (
        builtins_type + builtins_collection + builtins_io + builtins_math +
        builtins_introspection + builtins_capability + builtins_dynamic +
        builtins_iteration + builtins_conversion
    )

    # ============================================================
    # STANDARD LIBRARY MODULES (require import)
    # ============================================================

    stdlib_modules = [
        'console', 'json', 'math', 'datetime', 'functional',
        'regex', 'string', 'collections', 'file', 'http',
        'path', 'random'
    ]

    # ============================================================
    # TOKEN RULES
    # ============================================================

    tokens = {
        'root': [
            # ========== WHITESPACE ==========
            (r'\s+', Whitespace),

            # ========== COMMENTS (HIGHEST PRIORITY) ==========
            # Single-line comments
            (r'//[^\n]*', Comment.Single),

            # Multi-line comments (use separate state to prevent internal highlighting)
            (r'/\*', Comment.Multiline, 'multiline_comment'),

            # ========== STRINGS ==========
            (r'"(?:[^"\\]|\\.)*"', String.Double),
            (r"'(?:[^'\\]|\\.)*'", String.Single),

            # ========== NUMBERS ==========
            # Scientific notation
            (r'\b\d+\.?\d*[eE][+-]?\d+\b', Number.Float),
            # Floating point
            (r'\b\d+\.\d+\b', Number.Float),
            # Integers
            (r'\b\d+\b', Number.Integer),

            # ========== BOOLEAN LITERALS ==========
            (words(boolean_literals, suffix=r'\b'), Keyword.Constant),

            # ========== CAPABILITY DECLARATIONS ==========
            # capability CapabilityName {
            (r'\b(capability)(\s+)([a-zA-Z_][a-zA-Z0-9_]*)(\s*)(\{)',
             bygroups(Keyword, Whitespace, Name.Decorator, Whitespace, Name.Tag),
             'capability_block'),

            # ========== FUNCTION DEFINITIONS ==========
            # function functionName(
            (r'\b(function)(\s+)([a-zA-Z_][a-zA-Z0-9_]*)',
             bygroups(Keyword, Whitespace, Name.Function)),

            # ========== IMPORT STATEMENTS (before keywords) ==========
            # import console, from json import parse
            (r'\b(import|from)(\s+)(' + '|'.join(stdlib_modules) + r')\b',
             bygroups(Keyword, Whitespace, Name.Namespace)),

            # ========== KEYWORDS ==========
            # Permission types (in capability context)
            (words(keywords_permission, suffix=r'\b'), Keyword.Type),

            # All other keywords
            (words(all_keywords, suffix=r'\b'), Keyword),

            # ========== BUILTINS & STDLIB ==========
            # Builtin functions (always available)
            (words(all_builtins, suffix=r'\b'), Name.Builtin),

            # Standard library modules are NOT highlighted standalone
            # Only in import context (above) or member access (below)

            # ========== OPERATORS ==========
            # Logical operators
            (r'&&|\|\|', Operator),

            # Comparison operators (before single <, >)
            (r'==|!=|<=|>=', Operator),
            (r'<|>', Operator),

            # Arrow function operator
            (r'=>', Operator),

            # Floor division (before comment, but comments are higher priority)
            (r'//', Operator),

            # Arithmetic operators
            (r'[+\-*/%]', Operator),

            # Unary operators
            (r'!', Operator),

            # Ternary operator
            (r'\?|:', Operator),

            # Assignment
            (r'=', Operator),

            # ========== FUNCTION CALLS ==========
            # identifier followed by '('
            (r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*(?=\()', Name.Function),

            # ========== MEMBER ACCESS ==========
            # Module member access: console.log, path.join, etc.
            (r'\b(' + '|'.join(stdlib_modules) + r')(\.)(([a-zA-Z_][a-zA-Z0-9_]*))',
             bygroups(Name.Namespace, Punctuation, Name.Function)),

            # Regular property access: obj.property
            (r'\.([a-zA-Z_][a-zA-Z0-9_]*)', Name.Attribute),

            # ========== PUNCTUATION ==========
            # Braces and brackets (pink, bold) - using Name.Tag for distinct CSS class
            (r'[{}\[\]]', Name.Tag),

            # Parentheses (pink like operators)
            (r'[()]', Operator),

            # Other punctuation (white)
            (r'[;,.]', Punctuation),

            # ========== VARIABLES ==========
            # Catch-all for identifiers (variables)
            (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', Name.Variable),
        ],

        # ========== MULTI-LINE COMMENT STATE ==========
        'multiline_comment': [
            # Non-star characters
            (r'[^*]+', Comment.Multiline),
            # End of comment
            (r'\*/', Comment.Multiline, '#pop'),
            # Lone star
            (r'\*', Comment.Multiline),
        ],

        # ========== CAPABILITY BLOCK STATE ==========
        'capability_block': [
            # End of capability block
            (r'\}', Name.Tag, '#pop'),

            # Whitespace
            (r'\s+', Whitespace),

            # Comments (can appear in capability blocks)
            (r'//[^\n]*', Comment.Single),
            (r'/\*', Comment.Multiline, 'multiline_comment'),

            # resource "pattern";
            (r'\b(resource)(\s+)("(?:[^"\\]|\\.)*")(\s*)(;)',
             bygroups(Keyword, Whitespace, String, Whitespace, Punctuation)),

            # allow permission_type "optional_target";
            (r'\b(allow)(\s+)(read|write|execute|network|system)(?:(\s+)("(?:[^"\\]|\\.)*"))?(\s*)(;)',
             bygroups(Keyword, Whitespace, Keyword.Type, Whitespace, String, Whitespace, Punctuation)),

            # Semicolons
            (r';', Punctuation),
        ],
    }


def setup_ml_lexer():
    """Register the ML lexer with Pygments for Sphinx."""
    try:
        from pygments.lexers import get_lexer_by_name
        # Test if already registered
        get_lexer_by_name('ml')
        return  # Already registered
    except:
        pass

    try:
        # Register the lexer
        from pygments.lexers import _lexer_cache
        _lexer_cache['MLLexer'] = (__name__, 'MLLexer', ('ml',), ('*.ml',))

        try:
            from pygments.lexers import LEXERS
            LEXERS['MLLexer'] = (__name__, 'MLLexer', ('ml',), ('*.ml',), ())
        except ImportError:
            pass

        print("ML lexer registered successfully")
    except Exception as e:
        print(f"Failed to register ML lexer: {e}")


# Auto-register when imported
setup_ml_lexer()
