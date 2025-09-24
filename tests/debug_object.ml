// Minimal test case for object property access issue
function testObject() {
    obj = {"name": "test", "value": 42};
    obj.newProp = "added";
    return obj.name;
}