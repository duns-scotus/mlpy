# ML Pygments Lexer for Sphinx Documentation

This directory contains the custom Pygments lexer for ML language syntax highlighting in the Sphinx documentation.

## Files

- **`ml_lexer.py`** - Custom Pygments lexer for ML language
- **`_static/custom.css`** - Dracula-inspired color scheme for code blocks
- **`test_ml_syntax.rst`** - Comprehensive test document with all ML features

## Features

### Complete ML Language Support

The lexer provides accurate syntax highlighting for all ML language features:

1. **Keywords (Purple, Bold)** - All ML grammar keywords
   - Control flow: `if`, `elif`, `else`, `while`, `for`, `break`, `continue`, `in`
   - Functions: `function`, `return`, `fn`
   - Imports: `import`, `from`, `as`
   - Exceptions: `try`, `except`, `finally`, `throw`
   - Capabilities: `capability`, `resource`, `allow`
   - Scope: `nonlocal`

2. **Boolean Literals (Purple, Bold)** - `true`, `false`, `null`, `undefined`

3. **Builtin Functions (Cyan, Bold)** - 45 always-available functions
   - Type conversion: `int`, `float`, `str`, `bool`, `typeof`, `isinstance`
   - Collections: `len`, `range`, `enumerate`, `keys`, `values`, `sorted`, `sum`, `zip`
   - I/O: `print`, `input`
   - Math: `abs`, `min`, `max`, `round`
   - Introspection: `help`, `methods`, `modules`, `available_modules`, `has_module`, `module_info`
   - Capability: `hasCapability`, `getCapabilities`, `getCapabilityInfo`
   - Dynamic: `hasattr`, `getattr`, `call`, `callable`
   - Iteration: `iter`, `next`, `reversed`, `all`, `any`
   - Conversion: `chr`, `ord`, `hex`, `bin`, `oct`, `repr`, `format`

4. **Standard Library Modules (Yellow)** - Context-aware highlighting
   - Only highlighted in imports: `import console;`
   - Or member access: `console.log("message");`
   - Not as variable names: `path = "...";` (white)
   - Modules: console, json, math, datetime, functional, regex, string, collections, file, http, path, random

5. **Functions (Green)** - Function definitions and calls

6. **Variables (White)** - All other identifiers

7. **Strings (Yellow)** - All string types including escape characters

8. **Numbers (Purple)** - Integers, floats, scientific notation

9. **Comments (Light Gray, Italic)** - Single-line and multi-line with NO internal highlighting

10. **Operators (Pink)** - All operators including arithmetic, logical, comparison, ternary, arrow functions

11. **Braces/Brackets (Pink, Bold)** - `{ }` `[ ]` stand out prominently

12. **Parentheses (Pink)** - `( )` highlighted but not bold

13. **Capability Declarations (Special)** - Complete capability block support with orange names

## Color Scheme (Dracula-Inspired)

The lexer uses a professional Dracula-inspired color scheme optimized for dark backgrounds:

| Element | Color | Weight | Example |
|---------|-------|--------|---------|
| Background | `#282a36` | - | Dark background |
| Keywords | `#ff79c6` | Bold | `if`, `function`, `return` |
| Builtins | `#8be9fd` | Bold | `print`, `len`, `typeof` |
| Functions | `#50fa7b` | Normal | `processData()` |
| Variables | `#f8f8f2` | Normal | `myVariable` |
| Strings | `#f1fa8c` | Normal | `"Hello, World!"` |
| Numbers | `#bd93f9` | Normal | `42`, `3.14`, `6.022e23` |
| Comments | `#8b92b8` | Italic | `// comment` |
| Operators | `#ff79c6` | Normal | `+`, `-`, `==`, `=>` |
| Braces/Brackets | `#ff79c6` | Bold | `{`, `}`, `[`, `]` |
| Parentheses | `#ff79c6` | Normal | `(`, `)` |
| Stdlib Modules | `#f1fa8c` | Normal | `console`, `json` |
| Capability Names | `#ffb86c` | Bold | `FileAccess` |

## Context-Aware Highlighting

The lexer intelligently highlights based on context:

### Standard Library Modules

```ml
// Variable name (white)
path = "C:\\Users\\Documents";

// Import context (yellow)
import path;

// Member access (yellow module, green method)
result = path.join("a", "b");
```

### Comments

Comments are solid gray with NO internal syntax highlighting:

```ml
// This comment is gray - keywords like function, if, "strings" are NOT highlighted
/* Same for multi-line comments - no highlighting inside */
```

### Whitespace Preservation

All whitespace is properly preserved in constructs like:

```ml
function processData(arg) { }
capability FileAccess { }
import console;
```

## Usage in Sphinx

The lexer is automatically registered when `ml_lexer.py` is imported in `conf.py`:

```python
# In conf.py
from ml_lexer import MLLexer
```

Then use in reStructuredText documents:

```rst
.. code-block:: ml

    function hello(name) {
        print("Hello, " + name + "!");
    }

    hello("World");
```

## Testing

The test document `test_ml_syntax.rst` provides comprehensive examples of all language features and can be used to visually verify highlighting improvements.

Build and view:
```bash
cd docs
sphinx-build -b html source build
start build/test_ml_syntax.html
```

## Implementation Details

### Lexer Architecture

The lexer uses a hierarchical token rule system:

1. **Whitespace** - Preserved and tokenized
2. **Comments** - Highest priority to prevent internal highlighting
3. **Strings** - Before other patterns to capture escape sequences
4. **Numbers** - All numeric formats
5. **Boolean Literals** - Special keyword constants
6. **Capability Declarations** - Special state for capability blocks
7. **Function Definitions** - Keyword + name pattern
8. **Import Statements** - Before general keywords for module name context
9. **Keywords** - All ML grammar keywords
10. **Builtins** - Always-available functions
11. **Operators** - All operator types
12. **Function Calls** - Lookahead for `(`
13. **Member Access** - Module methods and object properties
14. **Punctuation** - Braces/brackets/parentheses/semicolons
15. **Variables** - Catch-all for identifiers

### Token Type Mappings

The lexer uses specific Pygments token types for CSS styling:

- `Keyword` → `.k` - Purple, bold
- `Keyword.Constant` → `.kc` - Boolean literals
- `Keyword.Type` → `.kt` - Permission types
- `Name.Builtin` → `.nb` - Cyan, bold
- `Name.Function` → `.nf` - Green
- `Name.Variable` → `.nv` - White
- `Name.Namespace` → `.nn` - Yellow (stdlib modules)
- `Name.Decorator` → `.nd` - Orange (capability names)
- `Name.Tag` → `.nt` - Pink, bold (braces/brackets)
- `Name.Attribute` → `.na` - White, italic (properties)
- `String.Double` → `.s2` - Yellow
- `String.Single` → `.s1` - Yellow
- `Number.Integer` → `.mi` - Purple
- `Number.Float` → `.mf` - Purple
- `Comment.Single` → `.c1` - Gray, italic
- `Comment.Multiline` → `.cm` - Gray, italic
- `Operator` → `.o` - Pink
- `Punctuation` → `.p` - White
- `Whitespace` → `.w` - Preserved

## Version History

### Version 2.0 (October 27, 2025)

Complete rewrite implementing all improvements from the ML Sphinx Lexer Improvement Proposal:

**Phase 1: Comment Handling**
- Added separate lexer state for multi-line comments
- Prevents internal syntax highlighting in comments

**Phase 2: Keywords Update**
- Replaced outdated keywords with actual ML grammar keywords
- Removed: async/await, let/const/var, match/when, etc.
- Added: elif, nonlocal, in, except

**Phase 3: Operator Highlighting**
- Added all operator types: arithmetic, logical, comparison, ternary, arrow functions

**Phase 4: Builtin Highlighting**
- Complete list of 45 builtin functions properly categorized
- Accurate highlighting in cyan, bold

**Phase 5: Braces & Parentheses**
- Braces/brackets: Pink, bold
- Parentheses: Pink, normal weight

**Phase 6: Functions vs Variables**
- Functions: Green
- Variables: White
- Clear visual distinction

**Phase 7: Capability Declarations**
- Full support for capability blocks
- Special highlighting for capability names (orange)
- Context-aware highlighting for resource/allow statements

**Additional Improvements:**
- Dark background (Dracula theme)
- Lighter, more visible comments
- Context-aware stdlib module highlighting
- Proper whitespace preservation
- String escape character handling
- Scientific notation support

## Maintenance

### Adding New Builtins

To add new builtin functions, update the relevant list in `ml_lexer.py`:

```python
builtins_type = [
    'int', 'float', 'str', 'bool', 'typeof', 'isinstance',
    'newBuiltin'  # Add here
]
```

### Adding New Keywords

Add to the appropriate keyword list:

```python
keywords_control = [
    'if', 'elif', 'else', 'while', 'for', 'break', 'continue', 'in',
    'newKeyword'  # Add here
]
```

### Changing Colors

Update `_static/custom.css`:

```css
/* Change builtin color */
.highlight .nb { color: #8be9fd; font-weight: bold; }
```

## Credits

- **Lexer Implementation:** Claude Code Assistant
- **Proposal:** docs/proposals/ml-sphinx-lexer-improvement.md
- **Color Scheme:** Inspired by Dracula theme
- **Testing:** Comprehensive test document with 400+ lines of ML code

## License

Part of the mlpy project. See main project LICENSE.
