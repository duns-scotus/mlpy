// Dangerous ML code for testing security analysis
import os;

function processUserInput(userCode) {
    result = eval(userCode);
    systemAccess = obj.__globals__;
    return result;
}