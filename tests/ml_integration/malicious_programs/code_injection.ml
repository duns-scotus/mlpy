// Template injection vulnerabilities (corrected ML syntax)
function processUserTemplate(userInput) {
    // This could inject arbitrary Python code
    template = "def user_function(): result = " + userInput + "; return result";
    return template;
}

function buildDynamicCode(commands) {
    code = "def process_data():";
    i = 0;

    while (i < 3) {
        command = commands[i];
        code = code + " " + command;
        i = i + 1;
    }

    code = code + " return 'done'";
    return code;
}

// String interpolation injection - should detect eval
function formatCommand(userInput) {
    return "eval(" + userInput + ")";
}

// Indirect code construction - should detect exec
function buildExecutionString(operation, data) {
    if (operation == "evaluate") {
        return "eval(" + data + ")";
    } else {
        if (operation == "execute") {
            return "exec(" + data + ")";
        } else {
            return data;
        }
    }
}

// Multi-stage code injection
function processWorkflow(stepType, stepData) {
    if (stepType == "eval") {
        return "eval(" + stepData + ")";
    } else {
        if (stepType == "system") {
            return "os.system(" + stepData + ")";
        } else {
            return "__import__(" + stepData + ")";
        }
    }
}

// Test malicious code injection
userTemplate = processUserTemplate("1 + 1");
dynamicCode = buildDynamicCode(["print('hello')", "exec('malicious')", "exit()"]);
formatted = formatCommand("print('injected')");
workflow = processWorkflow("eval", "malicious_code");