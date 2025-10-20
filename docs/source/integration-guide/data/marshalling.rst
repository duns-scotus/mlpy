Data Marshalling Deep Dive
============================

.. note::
   **Chapter Summary:** Comprehensive guide to data type conversion, marshalling strategies, and performance optimization for Python-ML data exchange.

This chapter provides an in-depth exploration of data marshalling between Python and ML. You'll learn how types are converted, how to handle complex data structures, implement custom type handlers, and optimize performance for high-throughput applications.

----

Understanding ML Type System
------------------------------

ML uses a dynamic type system similar to JavaScript. Understanding the type mapping between Python and ML is essential for effective integration.

Type Mapping Overview
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Python to ML Type Mapping
   :header-rows: 1
   :widths: 20 20 30 30

   * - Python Type
     - ML Type
     - Example (Python)
     - Example (ML)
   * - ``None``
     - ``null``
     - ``None``
     - ``null``
   * - ``bool``
     - ``boolean``
     - ``True``, ``False``
     - ``true``, ``false``
   * - ``int``
     - ``number``
     - ``42``, ``-17``
     - ``42``, ``-17``
   * - ``float``
     - ``number``
     - ``3.14``, ``1.5e6``
     - ``3.14``, ``1.5e6``
   * - ``str``
     - ``string``
     - ``"hello"``
     - ``"hello"``
   * - ``list``
     - ``array``
     - ``[1, 2, 3]``
     - ``[1, 2, 3]``
   * - ``tuple``
     - ``array``
     - ``(1, 2, 3)``
     - ``[1, 2, 3]``
   * - ``dict``
     - ``object``
     - ``{"key": "value"}``
     - ``{"key": "value"}``
   * - ``function``
     - ``function``
     - ``lambda x: x * 2``
     - ``function(x) { return x * 2; }``

Type Conversion Rules
~~~~~~~~~~~~~~~~~~~~~

**Automatic Conversions:**

ML automatically converts between compatible types following these rules:

1. **Numeric Widening:** ``int`` → ``float`` (automatic)
2. **Boolean to Number:** ``true`` → ``1``, ``false`` → ``0``
3. **String Coercion:** Any type can be converted to string
4. **Truthy/Falsy:** Any value can be evaluated in boolean context

**Lossy Conversions (Require Explicit Cast):**

1. **Float to Int:** Truncates decimal (``3.14`` → ``3``)
2. **String to Number:** Parses numeric strings (``"42"`` → ``42``)
3. **Array to Boolean:** Empty array is ``false``, non-empty is ``true``

----

Basic Type Conversion
-----------------------

Primitive Type Marshalling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Python to ML:**

.. code-block:: python

   from mlpy import MLExecutor

   executor = MLExecutor()
   executor.load("types.ml")

   # Numbers
   result = executor.call_function("processNumber", 42)
   print(result)  # ML receives: 42 (number)

   # Floats
   result = executor.call_function("processNumber", 3.14)
   print(result)  # ML receives: 3.14 (number)

   # Strings
   result = executor.call_function("processString", "hello")
   print(result)  # ML receives: "hello" (string)

   # Booleans
   result = executor.call_function("processBool", True)
   print(result)  # ML receives: true (boolean)

   # None
   result = executor.call_function("processNull", None)
   print(result)  # ML receives: null

**types.ml:**

.. code-block:: ml

   function processNumber(n) {
       return {
           "value": n,
           "type": typeof(n),
           "doubled": n * 2
       };
   }

   function processString(s) {
       return {
           "value": s,
           "type": typeof(s),
           "length": s.length,
           "upper": s.toUpperCase()
       };
   }

   function processBool(b) {
       return {
           "value": b,
           "type": typeof(b),
           "negated": !b
       };
   }

   function processNull(val) {
       return {
           "value": val,
           "type": typeof(val),
           "is_null": val == null
       };
   }

**ML to Python:**

.. code-block:: python

   # ML returns are automatically converted to Python types
   result = executor.call_function("getTypes", {})

   print(type(result["number"]))   # <class 'int'> or <class 'float'>
   print(type(result["string"]))   # <class 'str'>
   print(type(result["boolean"]))  # <class 'bool'>
   print(type(result["null"]))     # <class 'NoneType'>
   print(type(result["array"]))    # <class 'list'>
   print(type(result["object"]))   # <class 'dict'>

.. code-block:: ml

   function getTypes() {
       return {
           "number": 42,
           "string": "hello",
           "boolean": true,
           "null": null,
           "array": [1, 2, 3],
           "object": {"key": "value"}
       };
   }

String Encoding
~~~~~~~~~~~~~~~~

Strings are UTF-8 encoded by default.

.. code-block:: python

   # Unicode handling
   result = executor.call_function("processUnicode", "Hello 🌍 世界")

   # Output: ML correctly handles Unicode
   print(result)  # {'text': 'Hello 🌍 世界', 'length': 11}

.. code-block:: ml

   function processUnicode(text) {
       return {
           "text": text,
           "length": text.length,
           "upper": text.toUpperCase()
       };
   }

**Handling Special Characters:**

.. code-block:: python

   # Escape sequences
   data = {
       "newline": "line1\nline2",
       "tab": "col1\tcol2",
       "quote": 'He said "hello"',
       "backslash": "path\\to\\file"
   }

   result = executor.call_function("processEscapes", data)

----

Complex Data Structures
-------------------------

Array Marshalling
~~~~~~~~~~~~~~~~~~

**Simple Arrays:**

.. code-block:: python

   # Python list to ML array
   numbers = [1, 2, 3, 4, 5]
   result = executor.call_function("sumArray", numbers)
   print(result)  # {'sum': 15, 'count': 5}

.. code-block:: ml

   function sumArray(arr) {
       let sum = arr.reduce(function(a, b) { return a + b; }, 0);
       return {
           "sum": sum,
           "count": arr.length
       };
   }

**Nested Arrays:**

.. code-block:: python

   # 2D array (matrix)
   matrix = [
       [1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]
   ]

   result = executor.call_function("processMatrix", matrix)
   print(result)
   # Output: {'rows': 3, 'cols': 3, 'flat': [1,2,3,4,5,6,7,8,9]}

.. code-block:: ml

   function processMatrix(matrix) {
       let rows = matrix.length;
       let cols = matrix[0].length;

       # Flatten matrix
       let flat = [];
       let i = 0;
       while (i < rows) {
           let j = 0;
           while (j < cols) {
               flat.push(matrix[i][j]);
               j = j + 1;
           }
           i = i + 1;
       }

       return {
           "rows": rows,
           "cols": cols,
           "flat": flat
       };
   }

**Heterogeneous Arrays:**

.. code-block:: python

   # Mixed types in array
   mixed = [42, "hello", True, None, [1, 2], {"key": "value"}]

   result = executor.call_function("analyzeMixed", mixed)

.. code-block:: ml

   function analyzeMixed(arr) {
       let types = arr.map(function(item) {
           return typeof(item);
       });

       let typeCounts = {};
       let i = 0;
       while (i < types.length) {
           let t = types[i];
           typeCounts[t] = (typeCounts[t] || 0) + 1;
           i = i + 1;
       }

       return {
           "types": types,
           "counts": typeCounts,
           "length": arr.length
       };
   }

Object Marshalling
~~~~~~~~~~~~~~~~~~~

**Simple Objects:**

.. code-block:: python

   # Python dict to ML object
   user = {
       "name": "John Doe",
       "age": 30,
       "email": "john@example.com"
   }

   result = executor.call_function("processUser", user)

.. code-block:: ml

   function processUser(user) {
       return {
           "original": user,
           "greeting": "Hello, " + user.name,
           "is_adult": user.age >= 18,
           "domain": user.email.split("@")[1]
       };
   }

**Nested Objects:**

.. code-block:: python

   # Deeply nested structure
   data = {
       "user": {
           "profile": {
               "name": "John",
               "contact": {
                   "email": "john@example.com",
                   "phone": "555-1234"
               }
           },
           "settings": {
               "theme": "dark",
               "notifications": True
           }
       }
   }

   result = executor.call_function("extractDeep", data)

.. code-block:: ml

   function extractDeep(data) {
       # Access nested properties
       let name = data.user.profile.name;
       let email = data.user.profile.contact.email;
       let theme = data.user.settings.theme;

       return {
           "name": name,
           "email": email,
           "theme": theme,
           "path": "user.profile.contact.email"
       };
   }

**Dynamic Property Access:**

.. code-block:: python

   config = {
       "database": {
           "host": "localhost",
           "port": 5432
       },
       "cache": {
           "host": "localhost",
           "port": 6379
       }
   }

   result = executor.call_function("getProperty", {
       "obj": config,
       "path": "database.host"
   })

.. code-block:: ml

   function getProperty(params) {
       let obj = params.obj;
       let path = params.path;

       # Split path and traverse
       let parts = path.split(".");
       let current = obj;

       let i = 0;
       while (i < parts.length) {
           current = current[parts[i]];
           i = i + 1;
       }

       return {
           "path": path,
           "value": current,
           "found": current != null
       };
   }

Collection Marshalling
~~~~~~~~~~~~~~~~~~~~~~~

**Python Sets:**

Sets are converted to arrays (order not preserved).

.. code-block:: python

   # Python set
   unique_items = {1, 2, 3, 4, 5}

   # ML receives as array
   result = executor.call_function("processSet", list(unique_items))

**Python Tuples:**

Tuples are converted to arrays (immutability not preserved in ML).

.. code-block:: python

   # Python tuple
   coordinates = (10, 20, 30)

   # ML receives as array
   result = executor.call_function("processCoordinates", coordinates)

.. code-block:: ml

   function processCoordinates(coords) {
       return {
           "x": coords[0],
           "y": coords[1],
           "z": coords[2],
           "dimension": coords.length
       };
   }

**Return Value Preservation:**

.. code-block:: python

   # ML array returns as Python list
   result = executor.call_function("getArray", {})
   print(type(result))  # <class 'list'>

   # To convert back to tuple:
   result_tuple = tuple(result)

----

Custom Type Handlers
---------------------

Handling Custom Python Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Convert custom Python objects to ML-compatible dictionaries.

**Simple Custom Class:**

.. code-block:: python

   from dataclasses import dataclass
   from datetime import datetime

   @dataclass
   class Person:
       name: str
       age: int
       email: str

       def to_dict(self):
           """Convert to ML-compatible dict."""
           return {
               "name": self.name,
               "age": self.age,
               "email": self.email,
               "type": "Person"
           }

       @classmethod
       def from_dict(cls, data):
           """Create from ML return value."""
           return cls(
               name=data["name"],
               age=data["age"],
               email=data["email"]
           )

   # Usage
   person = Person("John", 30, "john@example.com")
   result = executor.call_function("processPerson", person.to_dict())

   # Convert result back to Person
   updated_person = Person.from_dict(result)

**Complex Custom Class:**

.. code-block:: python

   from datetime import datetime
   from typing import List, Optional

   class Order:
       def __init__(
           self,
           order_id: str,
           items: List[dict],
           total: float,
           created_at: Optional[datetime] = None
       ):
           self.order_id = order_id
           self.items = items
           self.total = total
           self.created_at = created_at or datetime.now()

       def to_dict(self):
           """Convert to ML-compatible format."""
           return {
               "order_id": self.order_id,
               "items": self.items,
               "total": self.total,
               "created_at": self.created_at.isoformat(),
               "item_count": len(self.items)
           }

       @classmethod
       def from_dict(cls, data):
           """Reconstruct from ML result."""
           created_at = datetime.fromisoformat(data["created_at"])
           return cls(
               order_id=data["order_id"],
               items=data["items"],
               total=data["total"],
               created_at=created_at
           )

   # Process order with ML
   order = Order(
       order_id="ORD-123",
       items=[
           {"name": "Widget", "price": 29.99, "qty": 2},
           {"name": "Gadget", "price": 49.99, "qty": 1}
       ],
       total=109.97
   )

   result = executor.call_function("processOrder", order.to_dict())
   processed_order = Order.from_dict(result)

Type Handler Registry
~~~~~~~~~~~~~~~~~~~~~~

Create a registry for automatic type conversion.

.. code-block:: python

   from typing import Any, Callable, Dict, Type

   class TypeRegistry:
       """Registry for custom type handlers."""

       def __init__(self):
           self.to_ml_handlers: Dict[Type, Callable] = {}
           self.from_ml_handlers: Dict[str, Callable] = {}

       def register(
           self,
           python_type: Type,
           to_ml: Callable,
           from_ml: Callable,
           type_name: str
       ):
           """Register type handlers.

           Args:
               python_type: Python type to handle
               to_ml: Function to convert Python -> ML
               from_ml: Function to convert ML -> Python
               type_name: Type identifier in ML
           """
           self.to_ml_handlers[python_type] = to_ml
           self.from_ml_handlers[type_name] = from_ml

       def to_ml(self, obj: Any) -> Any:
           """Convert Python object to ML-compatible format."""
           obj_type = type(obj)

           if obj_type in self.to_ml_handlers:
               return self.to_ml_handlers[obj_type](obj)

           # Default: try to_dict method
           if hasattr(obj, 'to_dict'):
               return obj.to_dict()

           # Fallback: return as-is
           return obj

       def from_ml(self, data: Any) -> Any:
           """Convert ML result to Python object."""
           if isinstance(data, dict) and "_type" in data:
               type_name = data["_type"]
               if type_name in self.from_ml_handlers:
                   return self.from_ml_handlers[type_name](data)

           return data

   # Create global registry
   type_registry = TypeRegistry()

   # Register datetime
   from datetime import datetime

   type_registry.register(
       datetime,
       to_ml=lambda dt: {
           "_type": "datetime",
           "iso": dt.isoformat(),
           "timestamp": dt.timestamp()
       },
       from_ml=lambda data: datetime.fromisoformat(data["iso"]),
       type_name="datetime"
   )

   # Register Person class
   type_registry.register(
       Person,
       to_ml=lambda p: {
           "_type": "Person",
           "name": p.name,
           "age": p.age,
           "email": p.email
       },
       from_ml=lambda data: Person(
           name=data["name"],
           age=data["age"],
           email=data["email"]
       ),
       type_name="Person"
   )

   # Usage with executor
   class TypeAwareExecutor:
       """ML executor with type conversion."""

       def __init__(self, registry: TypeRegistry):
           self.executor = MLExecutor()
           self.registry = registry

       def load(self, script: str):
           self.executor.load(script)

       def call_function(self, name: str, data: Any) -> Any:
           # Convert to ML format
           ml_data = self.registry.to_ml(data)

           # Execute
           result = self.executor.call_function(name, ml_data)

           # Convert from ML format
           return self.registry.from_ml(result)

   # Use type-aware executor
   executor = TypeAwareExecutor(type_registry)
   executor.load("handlers.ml")

   # Automatic conversion
   person = Person("Alice", 25, "alice@example.com")
   result = executor.call_function("processPerson", person)
   # Result is automatically converted back to Person object

Handling Dates and Times
~~~~~~~~~~~~~~~~~~~~~~~~~~

**DateTime Marshalling:**

.. code-block:: python

   from datetime import datetime, date, time, timedelta

   # ISO 8601 format (recommended)
   now = datetime.now()
   result = executor.call_function("processDateTime", {
       "timestamp": now.isoformat(),
       "date": date.today().isoformat(),
       "time": time(14, 30, 0).isoformat()
   })

.. code-block:: ml

   function processDateTime(data) {
       # Parse ISO 8601 strings
       let dt = new Date(data.timestamp);

       return {
           "parsed": data.timestamp,
           "year": dt.getFullYear(),
           "month": dt.getMonth() + 1,
           "day": dt.getDate(),
           "hour": dt.getHours(),
           "minute": dt.getMinutes()
       };
   }

**Unix Timestamp:**

.. code-block:: python

   # Unix timestamp
   timestamp = datetime.now().timestamp()
   result = executor.call_function("processTimestamp", timestamp)

.. code-block:: ml

   function processTimestamp(ts) {
       let dt = new Date(ts * 1000);  # Convert to milliseconds
       return {
           "timestamp": ts,
           "date_string": dt.toISOString(),
           "readable": dt.toLocaleString()
       };
   }

**Timedelta Handling:**

.. code-block:: python

   # Duration as seconds
   duration = timedelta(hours=2, minutes=30)
   result = executor.call_function("processDuration", {
       "seconds": duration.total_seconds(),
       "description": str(duration)
   })

----

Serialization Strategies
--------------------------

JSON Serialization
~~~~~~~~~~~~~~~~~~~

**Custom JSON Encoder:**

.. code-block:: python

   import json
   from datetime import datetime, date
   from decimal import Decimal

   class MLJSONEncoder(json.JSONEncoder):
       """Custom JSON encoder for ML-compatible serialization."""

       def default(self, obj):
           # Handle datetime
           if isinstance(obj, datetime):
               return {
                   "_type": "datetime",
                   "iso": obj.isoformat()
               }

           # Handle date
           if isinstance(obj, date):
               return {
                   "_type": "date",
                   "iso": obj.isoformat()
               }

           # Handle Decimal
           if isinstance(obj, Decimal):
               return float(obj)

           # Handle sets
           if isinstance(obj, set):
               return list(obj)

           # Handle custom objects
           if hasattr(obj, 'to_dict'):
               return obj.to_dict()

           return super().default(obj)

   # Usage
   data = {
       "created": datetime.now(),
       "amount": Decimal("99.99"),
       "tags": {"python", "ml", "integration"}
   }

   json_str = json.dumps(data, cls=MLJSONEncoder)
   parsed = json.loads(json_str)

   result = executor.call_function("processData", parsed)

**Custom JSON Decoder:**

.. code-block:: python

   class MLJSONDecoder(json.JSONDecoder):
       """Custom JSON decoder for ML results."""

       def __init__(self, *args, **kwargs):
           super().__init__(object_hook=self.object_hook, *args, **kwargs)

       def object_hook(self, obj):
           # Reconstruct datetime
           if obj.get("_type") == "datetime":
               return datetime.fromisoformat(obj["iso"])

           # Reconstruct date
           if obj.get("_type") == "date":
               return date.fromisoformat(obj["iso"])

           return obj

   # Usage
   result_json = json.dumps(result)
   reconstructed = json.loads(result_json, cls=MLJSONDecoder)

Binary Serialization
~~~~~~~~~~~~~~~~~~~~~

For high-performance scenarios, use binary formats.

**Using MessagePack:**

.. code-block:: python

   import msgpack
   from mlpy import MLExecutor

   class MessagePackExecutor:
       """ML executor using MessagePack for serialization."""

       def __init__(self):
           self.executor = MLExecutor()

       def load(self, script: str):
           self.executor.load(script)

       def call_function(self, name: str, data: Any) -> Any:
           # Serialize to MessagePack
           packed = msgpack.packb(data, use_bin_type=True)

           # Convert to base64 for ML
           import base64
           encoded = base64.b64encode(packed).decode('ascii')

           # Call ML function
           result = self.executor.call_function(name, {
               "_format": "msgpack",
               "_data": encoded
           })

           # Decode result
           if isinstance(result, dict) and result.get("_format") == "msgpack":
               decoded = base64.b64decode(result["_data"])
               return msgpack.unpackb(decoded, raw=False)

           return result

**Using Pickle (Caution):**

.. code-block:: python

   import pickle
   import base64

   # Only use pickle for trusted data
   def serialize_for_ml(obj):
       """Serialize Python object with pickle."""
       pickled = pickle.dumps(obj)
       encoded = base64.b64encode(pickled).decode('ascii')
       return {"_pickle": encoded}

   def deserialize_from_ml(data):
       """Deserialize from ML result."""
       if isinstance(data, dict) and "_pickle" in data:
           decoded = base64.b64decode(data["_pickle"])
           return pickle.loads(decoded)
       return data

   # ⚠️ WARNING: Only use with trusted ML scripts
   # Pickle can execute arbitrary code

Schema Validation
~~~~~~~~~~~~~~~~~~

Validate data before sending to ML.

.. code-block:: python

   from typing import Any, Dict
   from pydantic import BaseModel, Field, validator

   class UserInput(BaseModel):
       """Validated user input schema."""

       name: str = Field(..., min_length=1, max_length=100)
       age: int = Field(..., ge=0, le=150)
       email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
       tags: list = Field(default_factory=list)

       @validator('tags')
       def validate_tags(cls, v):
           if len(v) > 10:
               raise ValueError('Maximum 10 tags allowed')
           return v

       def to_ml_dict(self) -> Dict[str, Any]:
           """Convert to ML-compatible dict."""
           return self.dict()

   # Usage
   try:
       user_input = UserInput(
           name="John Doe",
           age=30,
           email="john@example.com",
           tags=["python", "ml"]
       )

       # Data is validated before sending to ML
       result = executor.call_function(
           "processUser",
           user_input.to_ml_dict()
       )

   except ValueError as e:
       print(f"Validation error: {e}")

----

Performance Optimization
--------------------------

Batch Processing
~~~~~~~~~~~~~~~~~

Process multiple items in a single ML call.

.. code-block:: python

   # Inefficient: Multiple calls
   results = []
   for item in items:
       result = executor.call_function("processItem", item)
       results.append(result)

   # Efficient: Single batch call
   result = executor.call_function("processBatch", {"items": items})
   results = result["results"]

.. code-block:: ml

   function processBatch(params) {
       let items = params.items;
       let results = items.map(function(item) {
           return processItem(item);
       });

       return {
           "results": results,
           "count": results.length
       };
   }

   function processItem(item) {
       # Individual item processing
       return {
           "processed": true,
           "data": item
       };
   }

Data Streaming
~~~~~~~~~~~~~~~

Stream large datasets instead of loading all at once.

.. code-block:: python

   class StreamingExecutor:
       """Process data in chunks."""

       def __init__(self, ml_script: str, chunk_size: int = 1000):
           self.executor = MLExecutor()
           self.executor.load(ml_script)
           self.chunk_size = chunk_size

       def process_stream(self, data_iter, function_name: str):
           """Process iterator in chunks."""
           chunk = []

           for item in data_iter:
               chunk.append(item)

               if len(chunk) >= self.chunk_size:
                   # Process chunk
                   result = self.executor.call_function(
                       function_name,
                       {"items": chunk}
                   )
                   yield result

                   chunk = []

           # Process remaining
           if chunk:
               result = self.executor.call_function(
                   function_name,
                   {"items": chunk}
               )
               yield result

   # Usage
   streaming = StreamingExecutor("processor.ml", chunk_size=500)

   # Process large dataset
   def data_generator():
       for i in range(10000):
           yield {"id": i, "value": i * 2}

   for chunk_result in streaming.process_stream(data_generator(), "processChunk"):
       print(f"Processed chunk: {chunk_result['count']} items")

Lazy Evaluation
~~~~~~~~~~~~~~~~

Defer expensive conversions until needed.

.. code-block:: python

   class LazyMLResult:
       """Lazy evaluation wrapper for ML results."""

       def __init__(self, executor, function_name: str, data: Any):
           self.executor = executor
           self.function_name = function_name
           self.data = data
           self._result = None
           self._evaluated = False

       def evaluate(self):
           """Evaluate ML function (cached)."""
           if not self._evaluated:
               self._result = self.executor.call_function(
                   self.function_name,
                   self.data
               )
               self._evaluated = True
           return self._result

       def __getitem__(self, key):
           return self.evaluate()[key]

       def __repr__(self):
           if self._evaluated:
               return f"LazyMLResult(evaluated={self._result})"
           return f"LazyMLResult(pending)"

   # Usage
   lazy_result = LazyMLResult(executor, "expensiveOperation", large_data)

   # Not evaluated yet
   print(lazy_result)  # LazyMLResult(pending)

   # Evaluated on first access
   value = lazy_result["result"]  # Triggers evaluation

   # Cached on subsequent access
   value2 = lazy_result["result"]  # Uses cached result

Memory Optimization
~~~~~~~~~~~~~~~~~~~~

Minimize memory usage for large data transfers.

**Use Generators:**

.. code-block:: python

   def process_large_file(filename: str, ml_function: str):
       """Process large file line by line."""

       def line_generator():
           with open(filename, 'r') as f:
               for line in f:
                   yield {"line": line.strip()}

       # Process without loading entire file
       for batch in chunked(line_generator(), 100):
           result = executor.call_function(ml_function, {"lines": batch})
           yield result

   def chunked(iterable, size):
       """Split iterator into chunks."""
       chunk = []
       for item in iterable:
           chunk.append(item)
           if len(chunk) >= size:
               yield chunk
               chunk = []
       if chunk:
           yield chunk

**Reference Passing (Advanced):**

.. code-block:: python

   # Instead of copying large arrays
   large_array = list(range(1000000))

   # Option 1: Send metadata only
   result = executor.call_function("processMetadata", {
       "length": len(large_array),
       "sample": large_array[:10]  # Send small sample
   })

   # Option 2: Process in chunks
   chunk_size = 10000
   for i in range(0, len(large_array), chunk_size):
       chunk = large_array[i:i + chunk_size]
       executor.call_function("processChunk", {
           "chunk": chunk,
           "offset": i
       })

----

Edge Cases and Gotchas
-----------------------

Circular References
~~~~~~~~~~~~~~~~~~~~

**Problem:** Circular references cause infinite loops.

.. code-block:: python

   # This will fail
   obj = {"name": "root"}
   obj["self"] = obj  # Circular reference

   # ML executor will raise error
   try:
       result = executor.call_function("process", obj)
   except RecursionError as e:
       print("Circular reference detected")

**Solution:** Break circular references before sending.

.. code-block:: python

   def remove_circular_refs(obj, seen=None):
       """Remove circular references from object."""
       if seen is None:
           seen = set()

       obj_id = id(obj)
       if obj_id in seen:
           return None  # Break circular reference

       seen.add(obj_id)

       if isinstance(obj, dict):
           return {
               k: remove_circular_refs(v, seen)
               for k, v in obj.items()
           }
       elif isinstance(obj, list):
           return [remove_circular_refs(item, seen) for item in obj]
       else:
           return obj

   # Usage
   safe_obj = remove_circular_refs(obj)
   result = executor.call_function("process", safe_obj)

NaN and Infinity
~~~~~~~~~~~~~~~~~

**Problem:** JavaScript NaN and Infinity handling differs from Python.

.. code-block:: python

   import math

   # Python NaN and Infinity
   data = {
       "nan": float('nan'),
       "inf": float('inf'),
       "neg_inf": float('-inf')
   }

   result = executor.call_function("processSpecial", data)

.. code-block:: ml

   function processSpecial(data) {
       return {
           "nan_is_nan": isNaN(data.nan),           # true
           "inf_is_finite": isFinite(data.inf),     # false
           "values": {
               "nan": data.nan,
               "inf": data.inf,
               "neg_inf": data.neg_inf
           }
       };
   }

**Handling NaN:**

.. code-block:: python

   import math

   def sanitize_numbers(obj):
       """Replace NaN/Inf with None."""
       if isinstance(obj, float):
           if math.isnan(obj) or math.isinf(obj):
               return None
       elif isinstance(obj, dict):
           return {k: sanitize_numbers(v) for k, v in obj.items()}
       elif isinstance(obj, list):
           return [sanitize_numbers(item) for item in obj]
       return obj

Large Numbers
~~~~~~~~~~~~~~

**Problem:** JavaScript number precision limits (53-bit integers).

.. code-block:: python

   # Large integer
   large_num = 9007199254740993  # Exceeds JS safe integer

   result = executor.call_function("processLargeNumber", large_num)
   # May lose precision in ML

**Solution:** Use strings for very large numbers.

.. code-block:: python

   # Send as string
   result = executor.call_function("processLargeNumber", {
       "value": str(large_num),
       "is_string": True
   })

.. code-block:: ml

   function processLargeNumber(data) {
       # Work with string representation
       let numStr = data.value;

       return {
           "length": numStr.length,
           "last_digit": numStr[numStr.length - 1],
           "value": numStr
       };
   }

Empty Collections
~~~~~~~~~~~~~~~~~~

**Problem:** Ambiguity between empty array and empty object.

.. code-block:: python

   # Python empty list
   empty_list = []

   # Python empty dict
   empty_dict = {}

   # Both are falsy in ML
   result = executor.call_function("checkEmpty", {
       "list": empty_list,
       "dict": empty_dict
   })

.. code-block:: ml

   function checkEmpty(data) {
       return {
           "list_type": typeof(data.list),        # "array"
           "dict_type": typeof(data.dict),        # "object"
           "list_empty": data.list.length == 0,   # true
           "dict_empty": Object.keys(data.dict).length == 0  # true
       };
   }

None vs Undefined
~~~~~~~~~~~~~~~~~~

**Problem:** Python ``None`` maps to ML ``null``, not ``undefined``.

.. code-block:: python

   # Python None
   data = {
       "value": None,
       # Missing key is different from None
   }

   result = executor.call_function("checkNone", data)

.. code-block:: ml

   function checkNone(data) {
       return {
           "value_is_null": data.value == null,           # true
           "missing_is_undefined": data.missing == undefined  # true
       };
   }

**Handling Optional Fields:**

.. code-block:: python

   # Explicitly include None for optional fields
   data = {
       "required": "value",
       "optional": None  # Explicitly None
   }

   # Or omit optional fields
   data = {
       "required": "value"
       # optional field omitted
   }

----

Best Practices
---------------

Type Conversion Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Prefer Simple Types:**

.. code-block:: python

   # Good: Use simple types when possible
   data = {
       "count": 42,
       "name": "example",
       "active": True
   }

   # Avoid: Complex Python-specific types
   # from collections import OrderedDict
   # data = OrderedDict([("a", 1), ("b", 2)])  # Lost in translation

**2. Document Type Expectations:**

.. code-block:: python

   def process_user_data(executor, user_data: dict) -> dict:
       """Process user data with ML.

       Args:
           executor: ML executor instance
           user_data: User data dict with keys:
               - name (str): User's full name
               - age (int): User's age (0-150)
               - email (str): Valid email address
               - tags (list[str]): Optional tags

       Returns:
           dict: Processed user data with additional fields:
               - processed (bool): Processing status
               - timestamp (str): ISO 8601 timestamp
               - validation (dict): Validation results
       """
       return executor.call_function("processUser", user_data)

**3. Validate Input Data:**

.. code-block:: python

   def safe_call(executor, function_name: str, data: Any) -> Any:
       """Call ML function with validation."""

       # Validate types
       if not isinstance(data, (dict, list, str, int, float, bool, type(None))):
           raise TypeError(f"Unsupported type: {type(data)}")

       # Check for circular references
       check_circular_refs(data)

       # Execute
       return executor.call_function(function_name, data)

Performance Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

**1. Batch When Possible:**

.. code-block:: python

   # Good: Batch processing
   results = executor.call_function("processBatch", {
       "items": items
   })

   # Avoid: Individual calls in loop
   # for item in items:
   #     result = executor.call_function("processItem", item)

**2. Cache Results:**

.. code-block:: python

   from functools import lru_cache

   @lru_cache(maxsize=128)
   def cached_ml_call(function_name: str, data_key: str):
       """Cache ML results for expensive operations."""
       return executor.call_function(function_name, {"key": data_key})

**3. Use Appropriate Data Structures:**

.. code-block:: python

   # Good: Use dict for key-value lookups
   lookup = {"id_123": "value", "id_456": "value2"}

   # Avoid: List of tuples (slower in ML)
   # lookup = [("id_123", "value"), ("id_456", "value2")]

Error Handling
~~~~~~~~~~~~~~~

**1. Handle Type Errors Gracefully:**

.. code-block:: python

   try:
       result = executor.call_function("process", data)
   except TypeError as e:
       # Log type error with context
       logger.error(f"Type error processing data: {e}")
       logger.debug(f"Data: {data}")
       raise

**2. Provide Fallbacks:**

.. code-block:: python

   def safe_process(data: dict, default=None):
       """Process with fallback."""
       try:
           return executor.call_function("process", data)
       except Exception as e:
           logger.warning(f"ML processing failed: {e}")
           return default

**3. Validate Return Types:**

.. code-block:: python

   result = executor.call_function("getData", {})

   # Validate result structure
   if not isinstance(result, dict):
       raise ValueError(f"Expected dict, got {type(result)}")

   if "required_field" not in result:
       raise ValueError("Missing required field in result")

----

Summary
--------

Data marshalling between Python and ML requires understanding of:

**Type System:**
- Automatic conversion for primitive types
- Arrays and objects map naturally
- Special handling for dates, custom objects

**Serialization:**
- JSON for human-readable format
- MessagePack for performance
- Custom encoders/decoders for complex types

**Performance:**
- Batch processing for multiple items
- Streaming for large datasets
- Lazy evaluation for expensive operations

**Edge Cases:**
- Circular references (break before sending)
- NaN/Infinity (sanitize or handle explicitly)
- Large numbers (use strings if > 53-bit)
- Empty collections (type preserved)

**Best Practices:**
- Prefer simple, ML-compatible types
- Validate input and output data
- Document type expectations
- Handle errors gracefully
- Batch operations when possible

Effective data marshalling ensures reliable, performant integration between Python and ML.

----

Next: :doc:`database` - Integrating ML with SQL and NoSQL databases
