"""
Pygments lexer for ML programming language syntax highlighting.
Supports all ML language features including pattern matching, capabilities, and advanced types.
"""

from pygments.lexer import RegexLexer, words, bygroups, using, this
from pygments.token import *

class MLLexer(RegexLexer):
    """
    Lexer for ML programming language.
    """
    name = 'ML'
    aliases = ['ml']
    filenames = ['*.ml']
    mimetypes = ['text/x-ml']

    keywords = [
        # Control flow
        'if', 'else', 'while', 'for', 'break', 'continue', 'return',

        # Functions
        'function', 'async', 'await', 'curry',

        # Types and interfaces
        'type', 'interface', 'extends', 'implements',

        # Pattern matching
        'match', 'when',

        # Module system
        'import', 'export', 'from', 'as',

        # Capability system
        'capability', 'secure', 'sandbox',

        # Memory annotations
        'borrow', 'mut',

        # Metaprogramming
        'macro',

        # Error handling
        'try', 'catch', 'throw', 'finally'
    ]

    builtins = [
        # Built-in types
        'number', 'string', 'boolean', 'void', 'any',
        'Array', 'Object', 'Promise', 'Result', 'Option',

        # Built-in functions
        'print', 'console', 'log', 'error', 'warn',
        'typeof', 'instanceof', 'hasOwnProperty',
        'parseInt', 'parseFloat', 'isNaN', 'isFinite',
        'Math', 'Date', 'JSON', 'RegExp',

        # Special values
        'true', 'false', 'null', 'undefined', 'this'
    ]

    operators = [
        # Arithmetic
        r'\+', r'-', r'\*', r'/', r'%', r'\*\*',

        # Assignment
        r'=', r'\+=', r'-=', r'\*=', r'/=', r'%=',

        # Comparison
        r'==', r'!=', r'<', r'>', r'<=', r'>=', r'===', r'!==',

        # Logical
        r'&&', r'\|\|', r'!',

        # Bitwise
        r'&', r'\|', r'\^', r'~', r'<<', r'>>',

        # Special operators
        r'\|>', r'<<', r'\?', r'\.\.', r'=>', r'\?\.', r'\?\?'
    ]

    tokens = {
        'root': [
            # Whitespace
            (r'\s+', Text),

            # Comments
            (r'//.*?$', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),

            # Strings
            (r'"(?:[^"\\]|\\.)*"', String.Double),
            (r"'(?:[^'\\]|\\.)*'", String.Single),
            (r'`(?:[^`\\]|\\.)*`', String.Backtick),

            # Template literals
            (r'`(?:[^`$\\]|\\.|$\{[^}]*\})*`', String.Backtick),

            # Numbers
            (r'\b\d+\.?\d*([eE][+-]?\d+)?\b', Number.Float),
            (r'\b0x[0-9a-fA-F]+\b', Number.Hex),
            (r'\b0b[01]+\b', Number.Bin),
            (r'\b0o[0-7]+\b', Number.Oct),
            (r'\b\d+\b', Number.Integer),

            # Keywords
            (words(keywords, suffix=r'\b'), Keyword),
            (words(builtins, suffix=r'\b'), Name.Builtin),

            # Type annotations
            (r':\s*([A-Z][a-zA-Z0-9_]*)', bygroups(Name.Class)),
            (r'<([A-Z][a-zA-Z0-9_,\s]*?)>', bygroups(Name.Class)),

            # Function definitions
            (r'\bfunction\s+([a-zA-Z_][a-zA-Z0-9_]*)', bygroups(Name.Function)),
            (r'\basync\s+function\s+([a-zA-Z_][a-zA-Z0-9_]*)', bygroups(Name.Function)),

            # Type definitions
            (r'\btype\s+([A-Z][a-zA-Z0-9_]*)', bygroups(Name.Class)),
            (r'\binterface\s+([A-Z][a-zA-Z0-9_]*)', bygroups(Name.Class)),

            # Capability annotations
            (r'\bcapability\s*\(\s*([^)]+)\s*\)', bygroups(Name.Decorator)),

            # Pattern matching
            (r'\bmatch\b', Keyword),
            (r'\bwhen\b', Keyword),
            (r'=>', Operator),
            (r'_\s*=>', bygroups(Keyword)),

            # Operators
            (r'(' + '|'.join(operators) + r')', Operator),

            # Punctuation
            (r'[{}()\[\];,.]', Punctuation),

            # Identifiers
            (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', Name),

            # Array/object literals
            (r'\[', Punctuation, 'array'),
            (r'\{', Punctuation, 'object'),
            (r'#\{', Punctuation, 'set'),
            (r'#\s*\{', Punctuation, 'map'),

            # Tuples
            (r'\([^)]*,', Punctuation),

            # Pipeline operator
            (r'\|>', Operator),

            # Error propagation
            (r'\?', Operator),

            # Lifetime annotations
            (r"'[a-zA-Z_][a-zA-Z0-9_]*", Name.Label),

            # Macro calls
            (r'@[a-zA-Z_][a-zA-Z0-9_]*', Name.Decorator),
        ],

        'array': [
            (r'\]', Punctuation, '#pop'),
            (r'[^,\]]+', Text),
            (r',', Punctuation),
        ],

        'object': [
            (r'\}', Punctuation, '#pop'),
            (r'[^,}:]+', Text),
            (r'[:,]', Punctuation),
        ],

        'set': [
            (r'\}', Punctuation, '#pop'),
            (r'[^,}]+', Text),
            (r',', Punctuation),
        ],

        'map': [
            (r'\}', Punctuation, '#pop'),
            (r'[^,}:]+', Text),
            (r'[:,]', Punctuation),
        ],
    }


def setup_ml_lexer():
    """
    Register the ML lexer with Pygments.
    Call this function to enable ML syntax highlighting in Sphinx.
    """
    try:
        from pygments.lexers import get_lexer_by_name
        # Test if already registered
        get_lexer_by_name('ml')
    except:
        # Register the lexer
        from pygments.lexers import _lexer_cache
        _lexer_cache['MLLexer'] = ('ml_lexer', 'MLLexer', (), ('*.ml',))

        # Also register with setuptools entry point style
        import pkg_resources
        dist = pkg_resources.Distribution(__file__)
        entry_point = pkg_resources.EntryPoint.parse(
            'ml = ml_lexer:MLLexer',
            dist=dist
        )
        dist._ep_map = {'pygments.lexers': {'ml': entry_point}}
        pkg_resources.working_set.add(dist)


# Auto-register when imported
setup_ml_lexer()