Language Reference
==================

Complete reference documentation for the ML programming language. This covers syntax, semantics, types, operators, statements, and built-in functionality.

.. toctree::
   :maxdepth: 2

   lexical-structure
   data-types
   expressions
   statements
   control-flow
   functions
   builtin-functions

Reference Overview
------------------

This reference documents ML language features based on the actual grammar and implementation, not aspirational designs. Every feature documented here works in the current version of ML.

**Organization:**

1. **Lexical Structure** - Tokens, keywords, literals, comments
2. **Data Types** - Numbers, strings, booleans, arrays, objects, functions
3. **Expressions** - Operators, precedence, evaluation order
4. **Statements** - Variable declarations, assignments, imports
5. **Control Flow** - Conditionals, loops, exceptions
6. **Functions** - Definitions, parameters, closures, recursion
7. **Built-in Functions** - Core language functions available without import

Using This Reference
--------------------

**Finding Syntax**

Use the table of contents or search functionality to find specific language constructs. Each section includes:

* Syntax specifications
* Executable examples
* Common patterns and idioms
* Limitations and edge cases

**Code Examples**

All code examples are complete, executable ML programs. They have been validated through ML's pipeline and represent correct, working code.

**Cross-References**

This reference frequently links to:

* :doc:`../../standard-library/index` - Standard library documentation
* :doc:`../tutorial/index` - Learning-focused tutorial content

Language Philosophy
-------------------

**Dynamic Typing with Safety**

ML uses dynamic typing - variables don't have fixed types, and types are checked at runtime. This provides flexibility while maintaining safety through ML's type checking functions (``typeof()``, ``isinstance()``).

**Security by Default**

Every ML program runs through static security analysis before execution. The language blocks dangerous operations by design (no ``eval``, restricted reflection, capability-controlled I/O).

**Python Interoperability**

ML transpiles to Python, providing access to Python's ecosystem. The :doc:`../../standard-library/builtin` module bridges ML and Python, handling type conversions and formatting differences.

Language Design Decisions
--------------------------

**ML-Compatible Formatting**

* Booleans: ``true`` and ``false`` (lowercase)
* Comments: ``//`` for single-line only
* Strings: Double or single quotes
* Arrays: Zero-indexed, square bracket syntax
* Objects: JavaScript-style object literals

**Notable Features**

* Arrow functions: ``fn(x) => x * 2``
* Destructuring: ``{name, age} = person``
* Ternary operator: ``condition ? trueValue : falseValue``
* String interpolation: Not yet implemented
* List comprehensions: Not yet implemented

**Current Limitations**

* Array element assignment has restrictions (document current behavior)
* No module system yet (uses Python-style imports)
* No class definitions (uses functional programming patterns)

See individual reference sections for detailed limitations and workarounds.

Grammar Source
--------------

The ML language grammar is defined in ``src/mlpy/ml/grammar/ml.lark``. This reference documentation is based on that grammar, ensuring accuracy with the actual implementation.

Next Steps
----------

* Start with :doc:`lexical-structure` to understand tokens and syntax
* Or jump to specific topics using the table of contents
* For learning-focused content, see the :doc:`../tutorial/index`
