# ML Sphinx Lexer Improvement Proposal
**Date:** October 24, 2025
**Status:** Proposal
**Priority:** High - Documentation Quality
**Complexity:** Medium

---

## Executive Summary

The current ML Pygments lexer for Sphinx documentation has several critical issues that reduce code readability and documentation quality. This proposal addresses 7 key improvements to make ML code examples in documentation clear, accurate, and visually appealing.

**Current Issues:**
1. ❌ Comments contain syntax highlighting (should be plain comment color)
2. ❌ Keywords list is outdated and includes non-existent features
3. ❌ Missing operator highlighting (unary, ternary, math, boolean)
4. ❌ Stdlib builtins not properly highlighted
5. ❌ Braces and parentheses not distinctly highlighted
6. ❌ Function and variable names not differentiated
7. ❌ Capability declarations not properly supported

---

## Problem Analysis

### Issue 1: Comments Contain Syntax Highlighting

**Current Behavior:**
```python
# Current lexer
(r'//.*?$', Comment.Single),
(r'/\*.*?\*/', Comment.Multiline),
```

**Problem:** These patterns don't prevent the lexer from continuing to highlight keywords, strings, etc. inside comments.

**Example of Bad Output:**
```ml
// This is a comment with function and return keywords <- both get highlighted
/* Multi-line comment with if, else, true <- all highlighted */
```

**Impact:** Comments are visually cluttered, harder to distinguish from code.

---

### Issue 2: Outdated Keywords List

**Current Keywords (docs/source/ml_lexer.py):**
```python
keywords = [
    'if', 'else', 'elif', 'while', 'for', 'break', 'continue', 'return',
    'function', 'async', 'await', 'curry',      # ❌ async/await not in grammar
    'let', 'const', 'var',                      # ❌ let/const/var not in grammar
    'type', 'interface', 'extends', 'implements', # ❌ not implemented
    'match', 'when',                            # ❌ not implemented
    'import', 'export', 'from', 'as',           # ✅ import/from/as correct, export ❌
    'capability', 'secure', 'sandbox',          # ✅ capability, ❌ secure/sandbox
    'borrow', 'mut',                            # ❌ not implemented
    'macro',                                    # ❌ not implemented
    'try', 'catch', 'except', 'throw', 'finally' # ⚠️ catch should be except
]
```

**Actual Keywords (from ml.lark grammar):**
```python
# Control flow
'if', 'elif', 'else', 'while', 'for', 'break', 'continue',

# Functions
'function', 'return', 'fn',  # fn is for arrow functions

# Imports
'import', 'from', 'as',

# Exception handling
'try', 'except', 'finally', 'throw',

# Capability system
'capability', 'resource', 'allow',

# Permission types (special keywords)
'read', 'write', 'execute', 'network', 'system',

# Scope control
'nonlocal',

# Reserved for future
'in',  # used in for loops
```

**Impact:** Incorrect highlighting confuses users about what features exist.

---

### Issue 3: Missing Operator Highlighting

**Current State:** Only has basic operator list, no proper highlighting in tokens.

**Missing Operators:**

**Unary Operators:**
- `!` - logical NOT
- `-` - unary negation

**Binary Operators:**
- `+`, `-`, `*`, `/`, `//`, `%` - arithmetic
- `==`, `!=`, `<`, `>`, `<=`, `>=` - comparison
- `&&`, `||` - logical
- `=>` - arrow function

**Ternary Operator:**
- `? :` - conditional expression

**Impact:** Operators blend with surrounding code, reducing readability.

---

### Issue 4: Stdlib Builtins Not Properly Highlighted

**Current Builtins (incorrect):**
```python
'print', 'console', 'log', 'error', 'warn',
'typeof', 'instanceof', 'hasOwnProperty',  # ❌ instanceof/hasOwnProperty don't exist
'parseInt', 'parseFloat', 'isNaN', 'isFinite',  # ❌ don't exist
'int', 'float', 'str',  # ✅ these exist
'Math', 'Date', 'JSON', 'RegExp',  # ❌ these are modules, not builtins
```

**Actual Builtins (from builtin.py):**
```python
# Type conversion
'int', 'float', 'str', 'bool'

# Type checking
'typeof', 'len'

# I/O
'print', 'input'

# Collections
'range', 'keys', 'values'

# Math utilities
'abs', 'min', 'max', 'round', 'sum', 'sorted'
```

**Actual Stdlib Modules (should be highlighted as Name.Namespace):**
```python
'console', 'json', 'math', 'datetime', 'functional',
'regex', 'string', 'collections', 'file', 'http',
'path', 'random'
```

**Impact:** Users don't know which functions are built-in vs. require imports.

---

### Issue 5: Braces and Parentheses Not Highlighted

**Current State:**
```python
(r'[{}()\[\];,.]', Punctuation),  # All lumped together
```

**Problem:** Braces `{}` and parentheses `()` are critical for code structure but don't stand out.

**Impact:** Harder to see block boundaries and function call syntax.

---

### Issue 6: Function and Variable Names Not Differentiated

**Current State:**
```python
# Function definitions captured
(r'\bfunction\s+([a-zA-Z_][a-zA-Z0-9_]*)', bygroups(Name.Function)),

# But function calls and variables are the same
(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', Name),
```

**Problem:** Can't distinguish between:
- Function calls: `myFunction()`
- Variable references: `myVariable`
- Object properties: `obj.property`

**Impact:** Reduces code clarity, especially in complex expressions.

---

### Issue 7: Capability Declarations Not Properly Supported

**Current State:**
```python
# Only captures capability in function context
(r'\bcapability\s*\(\s*([^)]+)\s*\)', bygroups(Name.Decorator)),
```

**Actual Capability Syntax:**
```ml
capability MyCapability {
    resource "data/*.json";
    allow read "config.json";
    allow write "output/*.txt";
}
```

**Problem:** Block-style capability declarations not recognized.

**Impact:** Security-critical feature not properly highlighted in docs.

---

## Proposed Solution

### Color Scheme

**Based on Dracula theme (professional, high-contrast):**

| Element | Token Type | Color | Hex | Style |
|---------|-----------|-------|-----|-------|
| **Keywords** | Keyword | Purple | `#ff79c6` | bold |
| **Control Flow** | Keyword.Reserved | Purple | `#ff79c6` | bold |
| **Builtins** | Name.Builtin | Cyan | `#8be9fd` | bold |
| **Stdlib Modules** | Name.Namespace | Yellow | `#f1fa8c` | normal |
| **Functions (def)** | Name.Function | Green | `#50fa7b` | normal |
| **Functions (call)** | Name.Function | Green | `#50fa7b` | normal |
| **Variables** | Name.Variable | White | `#f8f8f2` | normal |
| **Properties** | Name.Attribute | White | `#f8f8f2` | italic |
| **Strings** | String | Yellow | `#f1fa8c` | normal |
| **Numbers** | Number | Purple | `#bd93f9` | normal |
| **Comments** | Comment | Gray | `#6272a4` | italic |
| **Operators** | Operator | Pink | `#ff79c6` | normal |
| **Braces** | Punctuation.Bracket | Pink | `#ff79c6` | bold |
| **Parentheses** | Punctuation.Paren | Pink | `#ff79c6` | normal |
| **Capability** | Name.Decorator | Orange | `#ffb86c` | bold |
| **Permissions** | Keyword.Type | Orange | `#ffb86c` | normal |

**Rationale:**
- **Purple keywords** - Traditional, instantly recognizable
- **Cyan builtins** - Distinct from keywords, indicates "always available"
- **Green functions** - Active operations, stands out
- **Yellow strings/modules** - Warm color for data/imports
- **Gray comments** - Recedes to background
- **Pink operators/braces** - Structure and logic highlighted
- **Orange security** - Distinct color for capability system

---

## Implementation Plan

### Phase 1: Fix Comment Handling (Priority 1)

**Goal:** Prevent any highlighting inside comments.

**Implementation:**
```python
tokens = {
    'root': [
        # Comments MUST come first to have priority
        (r'//[^\n]*', Comment.Single),  # Single-line - match to end of line
        (r'/\*', Comment.Multiline, 'multiline_comment'),  # Multi-line - enter state

        # ... rest of tokens
    ],

    'multiline_comment': [
        (r'[^*]+', Comment.Multiline),  # Any non-* characters
        (r'\*/', Comment.Multiline, '#pop'),  # End comment, return to root
        (r'\*', Comment.Multiline),  # Lone * character
    ],
}
```

**Why This Works:**
- Comments are checked first (highest priority)
- Multi-line comments use a separate state that only matches comment content
- No other token rules are applied inside the comment state

**Test Case:**
```ml
// function return if else true false <- all should be gray
/*
   Multi-line with "strings" and keywords like function
   All of this should be gray comment color
*/
```

---

### Phase 2: Update Keywords List (Priority 1)

**Implementation:**
```python
# ACTUAL ML keywords from grammar (ml.lark)
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

keywords_permission = [
    'read', 'write', 'execute', 'network', 'system'
]

keywords_scope = [
    'nonlocal'
]

# Boolean literals (separate for different styling)
boolean_literals = [
    'true', 'false', 'null', 'undefined'
]

# Combine for token matching
all_keywords = (keywords_control + keywords_function + keywords_import +
                keywords_exception + keywords_capability + keywords_scope)
```

**Token Rules:**
```python
# Booleans first (higher specificity)
(words(boolean_literals, suffix=r'\b'), Keyword.Constant),

# Permission types (special keywords)
(words(keywords_permission, suffix=r'\b'), Keyword.Type),

# All other keywords
(words(all_keywords, suffix=r'\b'), Keyword),
```

---

### Phase 3: Add Operator Highlighting (Priority 2)

**Implementation:**
```python
tokens = {
    'root': [
        # ... comments and strings first ...

        # Ternary operator (must come before '?')
        (r'\?(?=.*:)', Operator),  # ? in ternary
        (r':', Operator),           # : in ternary

        # Logical operators
        (r'&&|\|\|', Operator),

        # Comparison operators (must come before single <, >)
        (r'==|!=|<=|>=', Operator),
        (r'<|>', Operator),

        # Arrow function operator
        (r'=>', Operator),

        # Floor division (must come before //)
        (r'//', Operator),

        # Arithmetic operators
        (r'\+|-|\*|/|%', Operator),

        # Unary operators (handled in context)
        (r'!', Operator),  # Logical NOT
        # Unary minus is contextual, handled by '-' above
    ],
}
```

**Why This Order:**
- Multi-character operators before single-character
- `//` before comment check would break things, so comments are first
- Contextual operators (like ternary) use lookahead

---

### Phase 4: Fix Builtin Highlighting (Priority 1)

**Implementation:**
```python
# Actual ML builtins (always available, no import needed)
builtins_type = [
    'int', 'float', 'str', 'bool', 'typeof'
]

builtins_collection = [
    'len', 'range', 'keys', 'values', 'sorted', 'sum'
]

builtins_io = [
    'print', 'input'
]

builtins_math = [
    'abs', 'min', 'max', 'round'
]

all_builtins = (builtins_type + builtins_collection +
                builtins_io + builtins_math)

# Standard library modules (require import)
stdlib_modules = [
    'console', 'json', 'math', 'datetime', 'functional',
    'regex', 'string', 'collections', 'file', 'http',
    'path', 'random'
]
```

**Token Rules:**
```python
# Builtins (cyan, bold)
(words(all_builtins, suffix=r'\b'), Name.Builtin),

# Stdlib modules in import statements or standalone
(words(stdlib_modules, suffix=r'\b'), Name.Namespace),
```

---

### Phase 5: Highlight Braces and Parentheses (Priority 2)

**Implementation:**
```python
# Separate brace and paren highlighting
(r'[{}\[\]]', Punctuation.Bracket),  # Braces and brackets - bold pink
(r'[()]', Punctuation.Paren),        # Parentheses - pink
(r'[;,.]', Punctuation),             # Other punctuation - default
```

**CSS Styling (in custom.css):**
```css
/* Bracket highlighting */
.highlight .p  { color: #ff79c6; }               /* Punctuation */
.highlight .pb { color: #ff79c6; font-weight: bold; }  /* Brackets */
.highlight .pp { color: #ff79c6; }               /* Parens */
```

---

### Phase 6: Function and Variable Differentiation (Priority 3)

**Implementation:**
```python
tokens = {
    'root': [
        # ... earlier rules ...

        # Function definitions
        (r'\bfunction\s+([a-zA-Z_][a-zA-Z0-9_]*)',
         bygroups(Keyword, Name.Function)),

        # Arrow functions (fn keyword)
        (r'\bfn\s*\(', bygroups(Keyword)),

        # Function calls (identifier followed by '(')
        (r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*(?=\()', Name.Function),

        # Member access (obj.property)
        (r'\.([a-zA-Z_][a-zA-Z0-9_]*)', bygroups(Name.Attribute)),

        # Variables (everything else)
        (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', Name.Variable),
    ],
}
```

**Priority Explanation:**
1. Keywords first (function, fn)
2. Function calls (lookahead for `(`)
3. Member access (after dot)
4. Variables (catch-all)

---

### Phase 7: Capability Declaration Support (Priority 2)

**Implementation:**
```python
tokens = {
    'root': [
        # ... earlier rules ...

        # Capability declaration block
        (r'\bcapability\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\{',
         bygroups(Keyword, Name.Decorator, Punctuation.Bracket),
         'capability_block'),

        # ... rest of rules ...
    ],

    'capability_block': [
        # End of capability block
        (r'\}', Punctuation.Bracket, '#pop'),

        # resource keyword and string
        (r'\bresource\s+("(?:[^"\\]|\\.)*")',
         bygroups(Keyword, String)),

        # allow keyword, permission type, optional target
        (r'\ballow\s+(read|write|execute|network|system)(?:\s+("(?:[^"\\]|\\.)*"))?',
         bygroups(Keyword, Keyword.Type, String)),

        # Semicolons
        (r';', Punctuation),

        # Whitespace and comments
        (r'\s+', Text),
        (r'//[^\n]*', Comment.Single),
        (r'/\*', Comment.Multiline, 'multiline_comment'),
    ],
}
```

**Example Output:**
```ml
capability FileAccess {
    resource "data/*.json";      // resource = keyword, string = yellow
    allow read "config.json";    // allow/read = keywords
    allow write "output/*.txt";  // write = permission type
}
```

---

## Complete Proposed Lexer

### File: `docs/source/ml_lexer.py`

```python
"""
Pygments lexer for ML programming language syntax highlighting.
Updated to match actual ML grammar and provide accurate, beautiful highlighting.

Version: 2.0
Date: October 2025
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
    # ============================================================

    builtins_type = [
        'int', 'float', 'str', 'bool', 'typeof'
    ]

    builtins_collection = [
        'len', 'range', 'keys', 'values', 'sorted', 'sum'
    ]

    builtins_io = [
        'print', 'input'
    ]

    builtins_math = [
        'abs', 'min', 'max', 'round'
    ]

    all_builtins = (
        builtins_type + builtins_collection +
        builtins_io + builtins_math
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
            (r'\bcapability\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\{',
             bygroups(Keyword, Name.Decorator, Punctuation.Bracket),
             'capability_block'),

            # ========== FUNCTION DEFINITIONS ==========
            # function functionName(
            (r'\bfunction\s+([a-zA-Z_][a-zA-Z0-9_]*)',
             bygroups(Keyword, Name.Function)),

            # ========== KEYWORDS ==========
            # Permission types (in capability context)
            (words(keywords_permission, suffix=r'\b'), Keyword.Type),

            # All other keywords
            (words(all_keywords, suffix=r'\b'), Keyword),

            # ========== BUILTINS & STDLIB ==========
            # Builtin functions (always available)
            (words(all_builtins, suffix=r'\b'), Name.Builtin),

            # Standard library modules
            (words(stdlib_modules, suffix=r'\b'), Name.Namespace),

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
            # .property
            (r'\.([a-zA-Z_][a-zA-Z0-9_]*)', bygroups(Name.Attribute)),

            # ========== PUNCTUATION ==========
            # Braces and brackets (highlighted)
            (r'[{}\[\]]', Punctuation.Bracket),

            # Parentheses
            (r'[()]', Punctuation.Paren),

            # Other punctuation
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
            (r'\}', Punctuation.Bracket, '#pop'),

            # Whitespace
            (r'\s+', Whitespace),

            # Comments (can appear in capability blocks)
            (r'//[^\n]*', Comment.Single),
            (r'/\*', Comment.Multiline, 'multiline_comment'),

            # resource "pattern";
            (r'\bresource\s+("(?:[^"\\]|\\.)*")\s*;',
             bygroups(Keyword, String, Punctuation)),

            # allow permission_type "optional_target";
            (r'\ballow\s+(read|write|execute|network|system)(?:\s+("(?:[^"\\]|\\.)*"))?\s*;',
             bygroups(Keyword, Keyword.Type, String, Punctuation)),

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

        print("✓ ML lexer registered successfully")
    except Exception as e:
        print(f"✗ Failed to register ML lexer: {e}")


# Auto-register when imported
setup_ml_lexer()
```

---

## CSS Styling

### File: `docs/source/_static/custom.css`

Add or update these rules:

```css
/* ============================================================
   ML CODE HIGHLIGHTING (Dracula-inspired theme)
   ============================================================ */

/* Keywords - Purple, Bold */
.highlight .k  { color: #ff79c6; font-weight: bold; }
.highlight .kc { color: #ff79c6; font-weight: bold; } /* Keyword.Constant (booleans) */
.highlight .kt { color: #ffb86c; }                    /* Keyword.Type (permissions) */

/* Builtins - Cyan, Bold */
.highlight .nb { color: #8be9fd; font-weight: bold; }

/* Names */
.highlight .nf { color: #50fa7b; }                    /* Name.Function - Green */
.highlight .nv { color: #f8f8f2; }                    /* Name.Variable - White */
.highlight .na { color: #f8f8f2; font-style: italic; } /* Name.Attribute - White, Italic */
.highlight .nn { color: #f1fa8c; }                    /* Name.Namespace (stdlib) - Yellow */
.highlight .nd { color: #ffb86c; font-weight: bold; } /* Name.Decorator (capability names) - Orange */

/* Strings - Yellow */
.highlight .s  { color: #f1fa8c; }
.highlight .s1 { color: #f1fa8c; } /* String.Single */
.highlight .s2 { color: #f1fa8c; } /* String.Double */

/* Numbers - Purple */
.highlight .m  { color: #bd93f9; }
.highlight .mi { color: #bd93f9; } /* Number.Integer */
.highlight .mf { color: #bd93f9; } /* Number.Float */

/* Comments - Gray, Italic */
.highlight .c  { color: #6272a4; font-style: italic; }
.highlight .c1 { color: #6272a4; font-style: italic; } /* Comment.Single */
.highlight .cm { color: #6272a4; font-style: italic; } /* Comment.Multiline */

/* Operators - Pink */
.highlight .o  { color: #ff79c6; }

/* Punctuation */
.highlight .p  { color: #f8f8f2; }                    /* Punctuation */
.highlight .pb { color: #ff79c6; font-weight: bold; } /* Punctuation.Bracket */
.highlight .pp { color: #ff79c6; }                    /* Punctuation.Paren */

/* Whitespace */
.highlight .w  { color: #f8f8f2; }

/* Security Highlighting - Make capability blocks stand out */
.highlight .capability {
    background-color: rgba(255, 184, 108, 0.1);
    border-left: 3px solid #ffb86c;
    padding-left: 8px;
}
```

---

## Testing Strategy

### Test File: `docs/source/test_ml_syntax.rst`

Create comprehensive test document to verify all highlighting:

````rst
ML Syntax Highlighting Test
=============================

Keywords and Control Flow
--------------------------

.. code-block:: ml

    // Control flow keywords
    if (condition) {
        return value;
    } elif (other) {
        break;
    } else {
        continue;
    }

    // Loop keywords
    while (running) {
        for (item in collection) {
            // process
        }
    }

    // Exception handling
    try {
        throw { message: "error" };
    } except (e) {
        print(e);
    } finally {
        cleanup();
    }

Comments Test
-------------

.. code-block:: ml

    // This comment should be GRAY with NO highlighting of:
    // function, return, if, else, true, false, "strings"

    /*
       Multi-line comment should also be GRAY
       Keywords like function, if, while should NOT highlight
       Strings like "test" should NOT be yellow
       Numbers like 42 should NOT be purple
    */

Builtins and Stdlib
-------------------

.. code-block:: ml

    // Builtins (CYAN, bold)
    print(typeof(value));
    x = int("42");
    y = float(3.14);
    z = str(true);
    arr = range(10);
    total = sum(arr);

    // Stdlib modules (YELLOW, after import)
    import console;
    import json;
    import math;

    console.log("Hello");
    data = json.parse(text);
    result = math.sqrt(16);

Operators
---------

.. code-block:: ml

    // Arithmetic operators (PINK)
    x = 10 + 5 - 3 * 2 / 4 % 2;

    // Comparison operators (PINK)
    if (x > 5 && y < 10 || z == 0) {
        // ...
    }

    // Ternary operator (PINK)
    result = condition ? valueIfTrue : valueIfFalse;

    // Unary operators (PINK)
    negative = -x;
    inverted = !flag;

Functions and Variables
-----------------------

.. code-block:: ml

    // Function definition (GREEN name)
    function calculateSum(a, b) {
        return a + b;
    }

    // Function call (GREEN name)
    result = calculateSum(5, 10);

    // Arrow function (fn keyword PURPLE, => PINK)
    add = fn(x, y) => x + y;

    // Variables (WHITE)
    myVariable = 42;
    another_var = "test";

Member Access
-------------

.. code-block:: ml

    // Object property access (property in ITALIC WHITE)
    obj.property = value;
    result = data.field.nested;

    // Method calls (GREEN)
    console.log("message");
    arr.push(item);

Braces and Parentheses
----------------------

.. code-block:: ml

    // Braces (PINK, bold)
    object = { key: "value" };

    // Parentheses (PINK)
    result = func(arg1, arg2);

    // Brackets (PINK, bold)
    array = [1, 2, 3];

Capability Declarations
-----------------------

.. code-block:: ml

    // Complete capability block (special highlighting)
    capability FileAccess {
        resource "data/*.json";
        allow read "config.json";
        allow write "output/*.txt";
        allow execute "scripts/*";
    }

    // Function using capability
    function loadData() {
        // Implementation
    }

Complete Example
----------------

.. code-block:: ml

    // Security-first data processing program
    import json;
    import console;

    capability DataAccess {
        resource "data/*.json";
        allow read "data/input.json";
        allow write "data/output.json";
    }

    function processData(filename) {
        // Load and parse data
        raw = file.read(filename);
        data = json.parse(raw);

        // Process each item
        results = [];
        for (item in data) {
            // Transform with ternary
            value = item.valid ? item.value : 0;

            // Apply calculation
            processed = value * 2 + 10;
            results.push(processed);
        }

        // Calculate statistics
        total = sum(results);
        average = total / len(results);

        // Log results
        console.log("Processed " + str(len(results)) + " items");
        console.log("Average: " + str(average));

        return results;
    }

    // Execute with error handling
    try {
        output = processData("data/input.json");
        file.write("data/output.json", json.stringify(output));
    } except (e) {
        console.error("Processing failed: " + e.message);
    }
````

---

## Rollout Plan

### Step 1: Backup Current Lexer
```bash
cp docs/source/ml_lexer.py docs/source/ml_lexer.py.backup
```

### Step 2: Implement New Lexer
- Replace `docs/source/ml_lexer.py` with proposed implementation
- Update `docs/source/_static/custom.css` with new color scheme

### Step 3: Create Test Document
- Add `docs/source/test_ml_syntax.rst` for visual verification
- Build docs: `sphinx-build -b html docs/source docs/build`

### Step 4: Visual Review
- Open `docs/build/test_ml_syntax.html` in browser
- Verify each section matches expected highlighting
- Check that comments are plain gray (no internal highlighting)

### Step 5: Update Existing Documentation
- Review all `.rst` and `.md` files with ML code blocks
- Ensure they display correctly with new lexer
- Fix any issues found

### Step 6: Documentation Update
- Update developer guide with new lexer capabilities
- Document color scheme in style guide
- Add examples of capability syntax

---

## Success Criteria

✅ **Issue 1 Fixed:** Comments are solid gray, no internal highlighting
✅ **Issue 2 Fixed:** Only actual ML keywords are highlighted
✅ **Issue 3 Fixed:** All operators (unary, binary, ternary) highlighted in pink
✅ **Issue 4 Fixed:** Builtins are cyan, stdlib modules are yellow
✅ **Issue 5 Fixed:** Braces `{}` bold pink, parentheses `()` pink
✅ **Issue 6 Fixed:** Functions green, variables white, properties italic
✅ **Issue 7 Fixed:** Capability declarations have special highlighting

**Overall:** ML code examples in documentation are clear, accurate, and beautiful.

---

## Risks and Mitigation

### Risk 1: Breaking Existing Docs
**Impact:** Medium
**Likelihood:** Low
**Mitigation:**
- Keep backup of old lexer
- Test with existing docs before deploying
- Rollback plan: restore `.backup` file

### Risk 2: CSS Not Applying
**Impact:** Low
**Likelihood:** Low
**Mitigation:**
- Verify `custom.css` is loaded in `conf.py`
- Use browser dev tools to check CSS rules
- Test with multiple browsers

### Risk 3: Performance Impact
**Impact:** Low
**Likelihood:** Very Low
**Mitigation:**
- Pygments lexers are highly optimized
- New lexer has similar complexity to old one
- Test build time before/after

---

## Maintenance Plan

### Monthly Review
- Check for new keywords in `ml.lark` grammar
- Verify builtin list matches `builtin.py`
- Update stdlib modules list

### Version Control
- Track lexer version in header comment
- Document changes in CHANGELOG
- Tag releases with grammar version

### Testing
- Add lexer test to CI/CD (syntax validation)
- Automated screenshot testing for visual regression
- User feedback mechanism for highlighting issues

---

## Conclusion

This proposal comprehensively addresses all 7 identified issues with the ML Sphinx lexer:

1. ✅ **Comments** - Separate state prevents internal highlighting
2. ✅ **Keywords** - Accurate list from grammar
3. ✅ **Operators** - All operators highlighted (unary, binary, ternary)
4. ✅ **Builtins** - Correct distinction between builtins and stdlib
5. ✅ **Braces** - Distinct highlighting for structure
6. ✅ **Functions** - Green for functions, white for variables
7. ✅ **Capabilities** - Full support for capability declarations

**Benefits:**
- **Accuracy:** Matches actual ML grammar
- **Clarity:** Clear visual distinction between element types
- **Beauty:** Professional Dracula-inspired color scheme
- **Maintainability:** Well-organized, documented code
- **Testability:** Comprehensive test document

**Next Steps:**
1. Review and approve proposal
2. Implement Phase 1 (comments) as proof-of-concept
3. Complete all phases
4. Deploy and test
5. Roll out to all documentation

---

**Estimated Effort:** 4-6 hours
**Priority:** High (documentation quality directly impacts user experience)
**Dependencies:** None (self-contained change)
**Review Required:** Yes (visual review of generated docs)
