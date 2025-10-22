"""Test DateTimeObject conversion to string for JSON serialization"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / 'src'))

from mlpy.stdlib.datetime_bridge import DateTimeObject, DateTime
from mlpy.ml.transpiler import MLTranspiler
from mlpy.runtime.capabilities import CapabilityContext, create_capability_token
from mlpy.runtime.capabilities.context import capability_context
import json


def convert_datetime_objects(data):
    """Convert DateTimeObjects to strings for JSON serialization."""
    print(f"DEBUG: Converting data of type {type(data)}, isinstance check: {isinstance(data, DateTimeObject)}")
    if isinstance(data, DateTimeObject):
        print(f"  -> Converting DateTimeObject to string")
        return str(data)  # Convert to string
    elif isinstance(data, dict):
        print(f"  -> Converting dict with keys: {list(data.keys())}")
        return {key: convert_datetime_objects(value) for key, value in data.items()}
    elif isinstance(data, list):
        print(f"  -> Converting list")
        return [convert_datetime_objects(item) for item in data]
    else:
        print(f"  -> Returning data as-is")
        return data


# Test the conversion
print("Testing DateTimeObject conversion...")

ml_code = """
import datetime;

function generate_report() {
    return {
        generated_at: datetime.now(),
        message: "Test report"
    };
}
"""

# Transpile
transpiler = MLTranspiler()
python_code, issues, _ = transpiler.transpile_to_python(ml_code, strict_security=False)

# Execute
namespace = {}
exec(python_code, namespace)

# Set up capabilities
ctx = CapabilityContext(name="test")
datetime_token = create_capability_token("datetime.now")
ctx.add_capability(datetime_token)

# Call the function
with capability_context(ctx):
    result = namespace['generate_report']()

print(f"\nOriginal result type: {type(result['generated_at'])}")
print(f"Original result: {result}")

# Convert DateTimeObjects
converted = convert_datetime_objects(result)
print(f"\nConverted result type for generated_at: {type(converted['generated_at'])}")
print(f"Converted result: {converted}")

# Try to JSON serialize
json_str = json.dumps(converted)
print(f"\nJSON serialization SUCCESS!")
print(f"JSON: {json_str}")
