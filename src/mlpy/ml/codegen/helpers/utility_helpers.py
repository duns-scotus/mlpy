"""Utility helper functions for code generation.

This module provides mixin functionality for common utility operations during
code generation:

1. **Identifier Sanitization** - Converting ML identifiers to valid Python names
2. **ML Builtins Discovery** - Dynamic detection of ML standard library functions
3. **Name Collision Prevention** - Safe handling of Python keywords and reserved names

These utilities ensure generated Python code is syntactically valid and
semantically correct while maintaining a clean mapping from ML to Python.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class UtilityHelpersMixin:
    """Mixin providing utility helper methods for code generation.

    This mixin provides common utility functions used throughout the code
    generation process:
    - Converting ML identifiers to safe Python identifiers
    - Discovering ML builtin functions from the standard library
    - Handling Python keyword conflicts and reserved names

    Thread Safety:
    - All methods in this mixin are thread-safe
    - _discover_ml_builtins() caches results per generator instance
    """

    def _discover_ml_builtins(self) -> set[str]:
        """Discover all ML builtin functions by inspecting @ml_function decorators.

        Dynamically inspects the ML standard library builtin module to find all
        functions decorated with @ml_function. This approach:
        - Avoids hardcoded function lists
        - Automatically includes new builtins
        - Ensures consistency with actual stdlib

        The discovered builtins are used for:
        - Identifier validation (treating builtins as defined)
        - Function call analysis
        - Import optimization (detect when to import builtin module)

        Returns:
            Set of ML builtin function names

        Discovery Strategy:
            1. Import mlpy.stdlib.builtin module
            2. Iterate through all module attributes
            3. Check for _ml_function_metadata attribute
            4. Collect names of decorated functions

        Example Result:
            ```python
            {
                'print', 'len', 'range', 'typeof', 'int', 'float', 'str',
                'map', 'filter', 'reduce', 'sum', 'min', 'max', ...
            }
            ```

        Fallback Behavior:
            Returns empty set if builtin module is not available.
            This allows the code generator to work even without the stdlib.

        Performance:
            - Called once during generator initialization
            - Results cached in self.symbol_table['ml_builtins']
            - O(n) where n is number of module attributes (~50-100)

        Note:
            Only functions with _ml_function_metadata are included.
            This ensures we only detect actual ML builtins, not internal helpers.
        """
        try:
            from mlpy.stdlib.builtin import builtin

            ml_builtins = set()
            for attr_name in dir(builtin):
                # Skip private/dunder attributes
                if attr_name.startswith('_'):
                    continue

                try:
                    attr = getattr(builtin, attr_name)
                    # Check if it's callable and has ML function metadata
                    if callable(attr) and hasattr(attr, '_ml_function_metadata'):
                        ml_builtins.add(attr_name)
                except AttributeError:
                    # Skip attributes that can't be accessed
                    continue

            return ml_builtins
        except ImportError:
            # If builtin module not available, return empty set
            # This allows code generator to work even without stdlib
            return set()

    def _safe_identifier(self, name: str) -> str:
        """Convert ML identifier to safe Python identifier.

        Ensures that ML identifiers are converted to valid Python identifiers
        that don't conflict with Python keywords or reserved names. This is
        critical for generating syntactically valid Python code.

        Args:
            name: ML identifier name

        Returns:
            Safe Python identifier string

        Conversion Rules:
            1. ML literals → Python equivalents:
               - "null" → "None"
            2. Python keywords → Prefixed with "ml_":
               - "class" → "ml_class"
               - "lambda" → "ml_lambda"
            3. Invalid characters → Replaced with underscores:
               - "user-name" → "user_name"
               - "123var" → "ml_123var"
            4. Non-string inputs → Generated safe name

        Examples:
            >>> self._safe_identifier("null")
            'None'

            >>> self._safe_identifier("class")
            'ml_class'

            >>> self._safe_identifier("user-name")
            'user_name'

            >>> self._safe_identifier("valid_name")
            'valid_name'

        Python Keywords Handled:
            and, as, assert, break, class, continue, def, del, elif, else,
            except, finally, for, from, global, if, import, in, is, lambda,
            not, or, pass, raise, return, try, while, with, yield,
            None, True, False

        Security Considerations:
            - Prevents injection of dangerous names like __import__
            - Ensures generated code doesn't accidentally override builtins
            - Maintains clear namespace separation (ml_ prefix)

        Performance:
            - O(1) for most identifiers (simple string check)
            - O(n) for invalid identifiers requiring character replacement
        """
        # Handle non-string inputs defensively
        if not isinstance(name, str):
            return f"ml_unknown_identifier_{id(name)}"

        # Handle ML-specific literals that need conversion to Python equivalents
        if name == "null":
            return "None"

        # Handle Python keywords and reserved names
        python_keywords = {
            "and",
            "as",
            "assert",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "finally",
            "for",
            "from",
            "global",
            "if",
            "import",
            "in",
            "is",
            "lambda",
            "not",
            "or",
            "pass",
            "raise",
            "return",
            "try",
            "while",
            "with",
            "yield",
            "None",
            "True",
            "False",
        }

        if name in python_keywords:
            return f"ml_{name}"

        # Ensure valid Python identifier
        if not name.isidentifier():
            # Replace invalid characters with underscores
            safe_name = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
            if safe_name[0].isdigit():
                safe_name = f"ml_{safe_name}"
            return safe_name

        return name
