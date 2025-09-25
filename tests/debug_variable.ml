// Minimal test case for variable initialization issue
function testVariable() {
    if (true) {
        result = "success";
    }
    return result;  // ERROR: result not defined in all paths
}

output = testVariable();