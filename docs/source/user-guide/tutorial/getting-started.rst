===============
Getting Started
===============

This guide helps you start using the ML language. You'll learn how to run ML code interactively and write your first programs.

.. contents::
   :local:
   :depth: 2

Starting the REPL
=================

The REPL (Read-Eval-Print Loop) lets you run ML code interactively. It's the quickest way to try the language and test ideas.

Start the REPL from your terminal::

    python -m mlpy.repl

You'll see the ML prompt::

    ml>

This means the REPL is ready for your commands.

Your First Commands
===================

Let's try some basic commands. Type each line at the ``ml>`` prompt:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-02-first-repl-session.transcript
   :language: text
   :lines: 9-16

The REPL evaluates each expression and prints the result. You can do arithmetic, create strings, and see the results immediately.

Creating Variables
==================

Variables store values you want to use later:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-02-first-repl-session.transcript
   :language: text
   :lines: 18-27

In ML, you create variables by assigning values to them. The semicolon at the end is required.

.. note::
   Variable names can contain letters, numbers, and underscores, but must start with a letter.

Simple Calculations
===================

You can combine variables in calculations:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-02-first-repl-session.transcript
   :language: text
   :lines: 29-35

The REPL keeps all variables in memory during your session. You can use them in later commands.

Hello, World!
=============

To print text to the console, import the ``console`` module:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-03-hello-world-repl.transcript
   :language: text
   :lines: 9-11

The ``import`` statement makes a module available. After importing ``console``, you can use ``console.log()`` to print messages.

Working with Strings
====================

Strings are text values enclosed in quotes. You can combine them with the ``+`` operator:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-03-hello-world-repl.transcript
   :language: text
   :lines: 13-17

To include a number in a string, convert it with ``str()``:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-03-hello-world-repl.transcript
   :language: text
   :lines: 19-24

Writing ML Files
================

While the REPL is great for trying things, you'll often want to save your code in files. ML files use the ``.ml`` extension.

Here's a simple calculation program:

.. literalinclude:: ../../../ml_snippets/tutorial/02_simple_calculation.ml
   :language: ml

Save this as ``calculation.ml`` and run it::

    python -m mlpy run calculation.ml

The program will print::

    Rectangle dimensions: 10 x 5
    Area: 50
    Perimeter: 30

A Complete Example
==================

Here's a program that shows more features:

.. literalinclude:: ../../../ml_snippets/tutorial/03_greeting_program.ml
   :language: ml

This program demonstrates:

* **String concatenation**: Joining strings with ``+``
* **Type conversion**: Using ``str()`` to convert numbers to strings
* **Multiple statements**: Each statement ends with a semicolon
* **Arithmetic**: Calculating values from variables

Run this program to see::

    Hello, Alice!
    You are 25 years old and live in New York.
    You will be 30 in 5 years.

Exploring on Your Own
======================

Now that you know the basics, try these exercises in the REPL:

1. Create variables for your name and age
2. Calculate what year you'll turn 100
3. Print a message with your results
4. Try different arithmetic operations: ``+``, ``-``, ``*``, ``/``

Tips for Using the REPL
========================

**Semicolons**: ML requires semicolons after most statements. The REPL adds them automatically for simple expressions, but it's good practice to include them.

**Errors**: If you make a mistake, the REPL shows an error message. Read it to understand what went wrong, then try again.

**Exit**: Type ``.exit`` or press Ctrl+D to leave the REPL.

Next Steps
==========

You now know how to:

* Start the REPL and run commands
* Create variables and do calculations
* Print messages with ``console.log()``
* Write ML programs in files

Continue to :doc:`basic-syntax` to learn more about ML's data types and operators.
