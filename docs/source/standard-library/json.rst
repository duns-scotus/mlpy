============
JSON Module
============

The ``json`` module provides JSON parsing and serialization with security validation and error handling.

.. contents:: Contents
   :local:
   :depth: 2

Overview
========

The JSON module enables safe JSON operations:

- **Parsing**: Convert JSON strings to ML objects
- **Serialization**: Convert ML objects to JSON strings
- **Validation**: Input validation and error handling
- **Security**: Safe parsing without code injection risks

Import and Usage
================

.. code-block:: ml

   import json;

   // Parse JSON string
   data = json.parse('{"name": "Alice", "age": 30}');
   name = data.name;  // "Alice"

   // Serialize to JSON
   obj = {name: "Bob", age: 25};
   json_string = json.stringify(obj);

**Note**: Complete API documentation available in ``json.ml`` and ``json_bridge.py`` source files.

See Also
========

- :doc:`string` - String manipulation
- :doc:`collections` - Object and array operations