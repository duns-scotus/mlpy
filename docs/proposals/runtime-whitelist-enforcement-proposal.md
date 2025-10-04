# Runtime Whitelist Enforcement Proposal

**Status**: DRAFT - Requires Analysis
**Created**: January 2025
**Dependencies**: Compile-time whitelist implementation (auto-import-proposal.md)
**Priority**: HIGH - Critical security hardening

---

## Executive Summary

**Problem**: Compile-time whitelist can be bypassed at runtime through:
- `getattr()` accessing Python builtins/non-whitelisted attributes
- Function variables storing and calling non-whitelisted functions
- Method calls on non-whitelisted classes
- Dynamic attribute access bypassing static analysis

**Solution**: Runtime enforcement that validates all dynamic operations against the same whitelist used at compile-time.

---

## Security Bypass Scenarios (Current Risk)

### Bypass 1: getattr() to Python Builtins
```javascript
// Compile-time: open() blocked ✓
// Runtime bypass: getattr() accesses it ✗
danger = getattr(open, "__call__");
content = danger("secrets.txt");  // Capability system bypassed!
```

### Bypass 2: Function Variables
```javascript
// Compile-time: eval() blocked ✓
// Runtime bypass: Store in variable ✗
func_var = eval;
func_var("malicious code");  // Executes anyway!
```

### Bypass 3: Non-Whitelisted Class Methods
```javascript
// Compile-time: Unknown class blocked ✓
// Runtime bypass: Instantiate and call ✗
obj = SomeNonWhitelistedClass();
obj.dangerous_method();  // No validation!
```

### Bypass 4: Dynamic Attribute Access
```javascript
// Compile-time: Static access blocked ✓
// Runtime bypass: Dynamic access ✗
attr_name = "open";
builtin[attr_name]("file.txt");  // Bypasses static analysis!
```

---

## Architecture Principles

### 1. Compile-Time Artifacts Reused at Runtime ✓
- AllowedFunctionsRegistry generated at compile-time
- Embedded in generated Python code or passed to sandbox
- Single source of truth for both compile and runtime

### 2. Defense in Depth ✓
```
Layer 1: Compile-time whitelist (code generator)
Layer 2: Runtime whitelist (builtin functions)
Layer 3: Sandbox restrictions (safe_attribute_registry)
Layer 4: Capability enforcement (for allowed operations)
```

### 3. Existing System Integration ✓
- Leverage `safe_attribute_registry.py` (already exists)
- Enhance `builtin.getattr()` with whitelist checks
- Integrate with `runtime_helpers.py` validation
- Work with sandbox execution context

---

## Analysis Required (Before Implementation)

### Phase 1: Understand Current System
- [ ] **Analyze `safe_attribute_registry.py`**: How does it whitelist attributes?
- [ ] **Analyze `builtin.getattr()`**: Current implementation and security
- [ ] **Analyze `runtime_helpers.py`**: `safe_attr_access()` functionality
- [ ] **Analyze sandbox execution**: How are restrictions enforced?
- [ ] **Identify gaps**: Where can runtime bypass compile-time checks?

### Phase 2: Design Runtime Enforcement
- [ ] **Registry passing**: How to pass AllowedFunctionsRegistry to runtime?
- [ ] **getattr() enhancement**: Integrate whitelist validation
- [ ] **Function call validation**: Wrap or intercept `__call__`?
- [ ] **Method call validation**: Integrate with safe_attribute_registry
- [ ] **Performance impact**: Minimize overhead for legitimate operations

### Phase 3: Implementation Strategy
- [ ] **Choose integration point**: builtin.py, safe_attribute_registry.py, or new layer?
- [ ] **Error handling**: Clear error messages for blocked operations
- [ ] **Backward compatibility**: Don't break existing working code
- [ ] **Testing strategy**: Unit tests, integration tests, security tests

---

## Open Questions

### 1. Registry Distribution
**How should AllowedFunctionsRegistry reach runtime?**

**Option A**: Embed in generated Python code
```python
# Generated code includes:
_ALLOWED_FUNCTIONS = {"len", "print", "range", ...}
_ALLOWED_MODULES = {"math": {...}, "string": {...}}
```

**Option B**: Pass through sandbox context
```python
sandbox = MLSandbox(allowed_functions=registry)
sandbox.execute(generated_code)
```

**Option C**: Build at runtime from decorator metadata
```python
# Runtime builds registry by scanning @ml_function decorators
registry = build_registry_from_decorators()
```

### 2. getattr() Implementation
**How should builtin.getattr() validate access?**

**Option A**: Check safe_attribute_registry only
```python
def getattr(obj, name):
    if not registry.is_safe_access(type(obj), name):
        raise SecurityError(...)
```

**Option B**: Check AllowedFunctionsRegistry + safe_attribute_registry
```python
def getattr(obj, name):
    if is_function(result) and not allowed_functions.contains(name):
        raise SecurityError(...)
    if not registry.is_safe_access(type(obj), name):
        raise SecurityError(...)
```

### 3. Function Variable Calls
**How to validate function calls through variables?**

**Option A**: Runtime type checking before call
```python
# Generated code wraps calls:
def _validate_call(func, name):
    if not is_allowed_function(func, name):
        raise SecurityError(...)
    return func
```

**Option B**: Sandbox-level call interception
```python
# Sandbox intercepts all function calls
class MLSandbox:
    def validate_call(self, func):
        # Check whitelist
```

### 4. Performance vs Security
**How to balance validation overhead?**

**Option A**: Validate every operation (secure, slow)
**Option B**: Validate only dynamic operations (fast, gaps?)
**Option C**: Cache validation results (balanced)

---

## Success Criteria (After Implementation)

### Security Tests
```python
# All runtime bypass attempts should fail:
test_getattr_blocks_python_builtins()
test_function_variables_validated()
test_non_whitelisted_classes_blocked()
test_dynamic_attribute_access_blocked()
```

### Integration with Compile-Time
```python
# Compile-time and runtime use same whitelist:
test_registry_consistency()
test_allowed_functions_match()
test_imported_modules_accessible()
```

### Performance
```python
# Minimal overhead for legitimate operations:
test_runtime_overhead_acceptable()  # < 5% slowdown
```

---

## Next Steps

1. **Complete compile-time implementation** (auto-import-proposal.md)
2. **Analyze existing runtime systems** (safe_attribute_registry, builtin.py, sandbox)
3. **Document findings** in this proposal
4. **Design runtime enforcement strategy**
5. **Implement runtime whitelist validation**
6. **Test security bypass prevention**

---

## Dependencies

- **Requires**: Compile-time whitelist (AllowedFunctionsRegistry)
- **Integrates with**: safe_attribute_registry, builtin.py, sandbox
- **Affects**: All dynamic operations in ML runtime

---

## Notes

- Runtime enforcement is **critical** - compile-time alone is insufficient
- Must maintain **defense-in-depth** architecture
- **Reuse compile-time artifacts** - don't duplicate whitelist logic
- Analyze **existing systems first** before choosing implementation strategy
- Balance **security vs performance** carefully

---

**Current Status**: Waiting for compile-time implementation completion
**Next Action**: Complete AllowedFunctionsRegistry implementation
**Future Work**: Deep analysis of runtime systems and bypass scenarios
