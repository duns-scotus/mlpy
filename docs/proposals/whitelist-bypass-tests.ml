// Systematic Whitelist Bypass Test Suite
// This file tests various ways the current implementation can be bypassed

// ============================================================================
// Test Category 1: call() Function Bypasses
// ============================================================================

// Test 1.1: Direct call() with Python builtin - SHOULD FAIL but might succeed
// Expected: Should be blocked
// Actual: Likely succeeds (call() doesn't validate)
// builtin.call(help);

// Test 1.2: call() with eval - CRITICAL SECURITY ISSUE
// Expected: Should be blocked
// Actual: Likely succeeds
// builtin.call(eval, ["print('bypassed!)')"]);

// Test 1.3: call() with exec - CRITICAL SECURITY ISSUE
// Expected: Should be blocked
// Actual: Likely succeeds
// builtin.call(exec, ["import os; os.system('echo hacked')"]);

// Test 1.4: call() with open - FILE ACCESS BYPASS
// Expected: Should be blocked
// Actual: Likely succeeds
// builtin.call(open, ["secrets.txt"]);

// Test 1.5: call() with __import__ - IMPORT BYPASS
// Expected: Should be blocked
// Actual: Likely succeeds
// let os = builtin.call(__import__, ["os"]);


// ============================================================================
// Test Category 2: Variable Function Storage Issues
// ============================================================================

// Test 2.1: Store function in variable then call
// Expected: Should work if function is whitelisted
// Actual: Fails with "m not in whitelist"
let m = builtin.len;
builtin.print("Stored len in variable m");

// This should fail:
// let result = m([1, 2, 3]);

// Test 2.2: Store user-defined function
function myFunc(x) {
    return x * 2;
}

let fn = myFunc;
// This might work since myFunc is user-defined
// let result2 = fn(5);


// ============================================================================
// Test Category 3: getattr() Bypasses
// ============================================================================

// Test 3.1: getattr to access Python builtins
// Expected: Should be blocked
// Actual: Depends on safe_attribute_registry implementation
// let danger = builtin.getattr(open, "__call__");

// Test 3.2: getattr on __builtins__
// Expected: Should be blocked
// Actual: Might succeed in REPL (has __builtins__)
// let builtins_dict = builtin.getattr(__builtins__, "__dict__");


// ============================================================================
// Test Category 4: REPL-Specific Bypasses
// ============================================================================

// Test 4.1: Access Python builtins directly (REPL only)
// Expected: Should fail (not in ML)
// Actual: Succeeds in REPL due to __builtins__ in namespace
// help;
// eval;
// open;

// Test 4.2: Python builtin shadowing
// Expected: ML functions should take precedence
// Actual: Python builtins might be accessible
// let shadowed = len;  // Should get builtin.len, not Python's len


// ============================================================================
// Test Category 5: Import System Bypasses
// ============================================================================

// Test 5.1: Dynamic module import via getattr
// Expected: Should be blocked
// Actual: Might succeed
// let sys = builtin.getattr(__import__("sys"), "modules");


// ============================================================================
// Test Category 6: Method Call Edge Cases
// ============================================================================

// Test 6.1: Call method through getattr
let str_test = "hello";
let upper_method = builtin.getattr(str_test, "upper");
// This should work since "upper" is safe
// let result3 = builtin.call(upper_method);

// Test 6.2: Call dangerous method through getattr
// Expected: Should be blocked
// Actual: Might succeed if call() doesn't validate
// let dangerous = builtin.getattr(str_test, "__class__");
// builtin.call(dangerous);


// ============================================================================
// Test Category 7: Compile-time vs Runtime Validation Gaps
// ============================================================================

// Test 7.1: Function passed as argument isn't validated at compile-time
function applyFunc(fn, arg) {
    return fn(arg);  // fn is unknown at compile-time
}

// This should be blocked but compilation might succeed
// let result4 = applyFunc(eval, "2 + 2");


// ============================================================================
// Test Category 8: Lambda/Anonymous Function Issues
// ============================================================================

// Test 8.1: Lambda with call()
// let lambda_test = function(fn) { return builtin.call(fn); };
// lambda_test(eval);  // CRITICAL: Bypasses validation


// ============================================================================
// Summary of Expected Vulnerabilities
// ============================================================================

/*
CRITICAL VULNERABILITIES DISCOVERED:

1. builtin.call() Runtime Bypass (HIGH SEVERITY)
   - Location: src/mlpy/stdlib/builtin.py:464-492
   - Issue: call() executes ANY callable without whitelist validation
   - Impact: Complete security bypass - can call eval, exec, open, __import__
   - Fix: call() must validate func against AllowedFunctionsRegistry

2. REPL __builtins__ Exposure (HIGH SEVERITY)
   - Location: src/mlpy/cli/repl.py:62
   - Issue: REPL adds Python's __builtins__ to namespace
   - Impact: All Python builtins accessible in REPL, bypassing whitelist
   - Fix: Create restricted __builtins__ dict with only safe functions

3. Variable Function Calls Not Supported (MEDIUM SEVERITY)
   - Location: src/mlpy/ml/codegen/python_generator.py:686-696
   - Issue: Compiler checks variable NAME against whitelist, not contents
   - Impact: Cannot store whitelisted functions in variables
   - Fix: Runtime validation or different code generation strategy

4. getattr() Security Unknown (NEEDS INVESTIGATION)
   - Location: src/mlpy/stdlib/builtin.py:424-462
   - Issue: Routes through safe_attribute_registry, but effectiveness unclear
   - Impact: Might allow access to dangerous attributes
   - Fix: Comprehensive testing and verification needed

RECOMMENDATIONS:

Phase 1 (Immediate - Critical Fixes):
1. Fix builtin.call() to validate against whitelist
2. Secure REPL __builtins__ exposure
3. Test getattr() security thoroughly

Phase 2 (Runtime Enhancement):
1. Implement runtime whitelist validation system
2. Add function call interceptor for dynamic calls
3. Create comprehensive security test suite

Phase 3 (Architecture Improvement):
1. Unified compile-time + runtime whitelist
2. Capability-based validation for dynamic calls
3. Defense-in-depth security layers
*/
