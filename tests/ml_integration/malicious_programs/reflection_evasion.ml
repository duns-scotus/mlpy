// Obfuscated reflection through string construction (corrected ML syntax)
function getHiddenClass(obj) {
    cls = "__cla" + "ss__";
    return obj[cls];
}

function accessBases(classObj) {
    basesKey = "__ba";
    basesKey = basesKey + "ses__";
    return classObj[basesKey];
}

function buildSubclassCall() {
    methodName = "__sub";
    methodName = methodName + "classes__";
    return methodName + "()";
}

// Dynamic property access chains
function chainedReflection(startObj) {
    obj = startObj;
    steps = ["__class__", "__bases__", "0", "__subclasses__"];
    i = 0;

    while (i < 4) {
        step = steps[i];
        if (step == "0") {
            obj = obj[0];
        } else {
            obj = obj[step];
        }
        i = i + 1;
    }

    return obj;
}

// Reflection through computed properties
function computedReflection(target) {
    classKey = "__" + "class" + "__";
    basesKey = "__" + "bases" + "__";
    dictKey = "__" + "dict" + "__";

    cls = target[classKey];
    bases = cls[basesKey];
    dict = cls[dictKey];

    return cls;
}

// Test malicious reflection
testObj = {};
hiddenClass = getHiddenClass(testObj);
computedProps = computedReflection(testObj);