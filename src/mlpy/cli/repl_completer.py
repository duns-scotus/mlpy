"""Auto-completion for ML REPL.

Provides intelligent auto-completion for:
- User-defined variables and functions
- Builtin functions (typeof, len, print, etc.)
- Standard library modules (console, json, math, etc.)
- Keywords (function, return, if, else, etc.)
"""

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document


class MLCompleter(Completer):
    """Auto-completer for ML language in REPL.

    Provides context-aware completion for:
    - Variables and functions defined in the REPL session
    - ML builtin functions
    - Standard library modules
    - Language keywords
    """

    # ML language keywords
    ML_KEYWORDS = [
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
        "true",
        "false",
        "null",
        "undefined",
    ]

    # ML builtin functions
    ML_BUILTINS = [
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
    ]

    # ML standard library modules
    ML_STDLIB_MODULES = [
        "console",
        "json",
        "math",
        "datetime",
        "functional",
        "regex",
        "string",
    ]

    def __init__(self, session):
        """Initialize completer with REPL session.

        Args:
            session: MLREPLSession instance for accessing user-defined symbols
        """
        self.session = session

    def get_completions(self, document: Document, complete_event):
        """Generate completion suggestions based on current input.

        Args:
            document: The current document (text before cursor)
            complete_event: Completion event from prompt_toolkit

        Yields:
            Completion objects for matching symbols
        """
        # Get the word before cursor
        word_before_cursor = document.get_word_before_cursor()

        if not word_before_cursor:
            return

        # Convert to lowercase for case-insensitive matching
        word_lower = word_before_cursor.lower()

        # === USER-DEFINED SYMBOLS ===
        # Highest priority: variables and functions from current session
        for symbol in self.session.symbol_tracker.get_symbols():
            if symbol.lower().startswith(word_lower):
                symbol_type = self.session.symbol_tracker.get_symbol_type(symbol)
                yield Completion(
                    text=symbol,
                    start_position=-len(word_before_cursor),
                    display_meta=f"<{symbol_type}>",
                    style="fg:ansigreen",
                )

        # === BUILTIN FUNCTIONS ===
        for builtin in self.ML_BUILTINS:
            if builtin.lower().startswith(word_lower):
                yield Completion(
                    text=builtin,
                    start_position=-len(word_before_cursor),
                    display_meta="<builtin>",
                    style="fg:ansicyan bold",
                )

        # === STANDARD LIBRARY MODULES ===
        for module in self.ML_STDLIB_MODULES:
            if module.lower().startswith(word_lower):
                yield Completion(
                    text=module,
                    start_position=-len(word_before_cursor),
                    display_meta="<stdlib>",
                    style="fg:ansiyellow",
                )

        # === KEYWORDS ===
        for keyword in self.ML_KEYWORDS:
            if keyword.lower().startswith(word_lower):
                yield Completion(
                    text=keyword,
                    start_position=-len(word_before_cursor),
                    display_meta="<keyword>",
                    style="fg:ansimagenta bold",
                )


class MLDotCompleter(Completer):
    """Completer for module methods (e.g., console.log, math.sqrt).

    Handles completions after a dot (.) for standard library modules.
    """

    # Module methods for common stdlib modules
    MODULE_METHODS = {
        "console": ["log", "error", "warn", "info", "debug", "clear"],
        "json": ["parse", "stringify", "load", "dump"],
        "math": [
            "sqrt",
            "pow",
            "abs",
            "floor",
            "ceil",
            "round",
            "sin",
            "cos",
            "tan",
            "log",
            "exp",
            "pi",
            "e",
        ],
        "datetime": [
            "now",
            "parse",
            "format",
            "timestamp",
            "add_days",
            "add_hours",
            "diff",
        ],
        "functional": [
            "map",
            "filter",
            "reduce",
            "forEach",
            "find",
            "some",
            "every",
            "curry2",
            "partition",
            "ifElse",
            "cond",
            "times",
            "zipWith",
            "takeWhile",
            "juxt",
        ],
        "regex": [
            "match",
            "test",
            "replace",
            "split",
            "findAll",
            "extract_emails",
            "extract_phone_numbers",
            "is_url",
            "find_first",
            "remove_html_tags",
        ],
        "string": [
            "upper",
            "lower",
            "trim",
            "split",
            "join",
            "replace",
            "substring",
            "indexOf",
            "contains",
            "startsWith",
            "endsWith",
            "camel_case",
            "pascal_case",
            "kebab_case",
        ],
    }

    def __init__(self, session):
        """Initialize dot completer with REPL session.

        Args:
            session: MLREPLSession instance
        """
        self.session = session

    def get_completions(self, document: Document, complete_event):
        """Generate completions for module.method patterns.

        Args:
            document: The current document
            complete_event: Completion event

        Yields:
            Completion objects for module methods
        """
        text_before_cursor = document.text_before_cursor

        # Check if we're completing after a dot
        if "." not in text_before_cursor:
            return

        # Extract module name and partial method
        parts = text_before_cursor.rsplit(".", 1)
        if len(parts) != 2:
            return

        module_expr = parts[0].strip()
        partial_method = parts[1]

        # Simple module name extraction (just get last identifier)
        module_tokens = module_expr.split()
        if not module_tokens:
            return

        module_name = module_tokens[-1]

        # Check if this is a known module
        if module_name in self.MODULE_METHODS:
            methods = self.MODULE_METHODS[module_name]

            for method in methods:
                if method.startswith(partial_method):
                    yield Completion(
                        text=method,
                        start_position=-len(partial_method),
                        display_meta=f"<{module_name}>",
                        style="fg:ansicyan",
                    )
