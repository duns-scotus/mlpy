// Dynamic import name construction (ML syntax with malicious patterns)
function buildImportName() {
    parts = ["__", "built", "in", "__"];
    return parts[0] + parts[1] + parts[2] + parts[3];
}

function dynamicImport() {
    moduleName = buildImportName();
    return import(moduleName);
}

// Import through indirection
function getImportFunction() {
    importFunc = "__imp" + "ort__";
    return importFunc;
}

// Disguised dangerous imports
function loadUtilities() {
    modules = ["os", "sys", "subprocess", "__builtin__"];

    // These should be caught by security analysis
    mod1 = import(modules[0]);  // os
    mod2 = import(modules[1]);  // sys
    mod3 = import(modules[2]);  // subprocess
    mod4 = import(modules[3]);  // __builtin__

    return [mod1, mod2, mod3, mod4];
}

// Obfuscated eval construction
function buildEvalFunction() {
    evalName = "ev" + "al";
    modules = loadUtilities();
    return evalName;
}

// Test malicious imports
utilities = loadUtilities();
evalFunc = buildEvalFunction();