"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access


def main():
    print("=== Testing Object Property Access ===")
    print("Testing basic object operations:")
    test_obj = {
        "name": "test",
        "value": 42,
        "active": True,
        "timeout": 5000,
        "nested": {"inner": "data"},
    }
    try:
        print("Object name: " + str(_safe_attr_access(test_obj, "name")))
        print("Object value: " + str(str(_safe_attr_access(test_obj, "value")) + ""))
        print(
            "Object active: " + str(str(_safe_attr_access(test_obj, "active")) + "")
        )
        print(
            "Object timeout: " + str(str(_safe_attr_access(test_obj, "timeout")) + "")
        )
        print(

                "Nested property: "
                + str(_safe_attr_access(_safe_attr_access(test_obj, "nested"), "inner"))

        )
    except error:
        print("Basic property access FAILED: " + str(str(error) + ""))
    print("Testing dynamic property access:")
    try:
        prop_name = "value"
        print("Dynamic access: Not testing - likely unsupported")
    except error:
        print("Dynamic property access FAILED: " + str(str(error) + ""))
    print("Testing property assignment:")
    try:
        test_obj["name"] = "modified"
        test_obj["value"] = 100
        test_obj["timeout"] = 10000
        print("Modified name: " + str(_safe_attr_access(test_obj, "name")))
        print(
            "Modified value: " + str(str(_safe_attr_access(test_obj, "value")) + "")
        )
        print(

                "Modified timeout: "
                + str(str(_safe_attr_access(test_obj, "timeout")) + "")

        )
    except error:
        print("Property assignment FAILED: " + str(str(error) + ""))
    print("Testing new property addition:")
    try:
        test_obj["new_property"] = "added"
        print("New property: " + str(_safe_attr_access(test_obj, "new_property")))
    except error:
        print("New property addition FAILED: " + str(str(error) + ""))
    print("Testing object methods:")
    calculator = {
        "value": 0,
        "add": lambda x: _safe_attr_access(calculator, "value"),
        "get_value": lambda: _safe_attr_access(calculator, "value"),
    }
    try:
        result1 = _safe_attr_access(calculator, "add")(10)
        result2 = _safe_attr_access(calculator, "add")(5)
        current = _safe_attr_access(calculator, "get_value")()
        print("Calculator add(10): " + str(str(result1) + ""))
        print("Calculator add(5): " + str(str(result2) + ""))
        print("Calculator current value: " + str(str(current) + ""))
    except error:
        print("Object methods FAILED: " + str(str(error) + ""))
    print("Testing property existence:")
    try:
        has_name = _safe_attr_access(test_obj, "name") != None
        has_missing = _safe_attr_access(test_obj, "missing_prop") != None
        print("Has name property: " + str(str(has_name) + ""))
        print("Has missing property: " + str(str(has_missing) + ""))
    except error:
        print("Property existence check FAILED: " + str(str(error) + ""))
    print("=== Object Property Access Test Complete ===")


main()

# End of generated code
