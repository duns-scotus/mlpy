# ML Capability Inspection API - Gap Analysis

**Date:** October 27, 2025
**Status:** Analysis
**Purpose:** Identify missing essential capability inspection features

---

## Current API Coverage

### ✅ Context Capabilities (What I Have)

| Function | Purpose | Status |
|----------|---------|--------|
| `hasCapability(name)` | Check if specific capability available | ✅ Complete |
| `getCapabilities()` | List all available capabilities | ✅ Complete |
| `getCapabilityInfo(name)` | Get detailed capability information | ✅ Complete |

### ✅ Function Requirements (What Function Needs)

| Function | Purpose | Status |
|----------|---------|--------|
| `requiredCapabilities(func)` | Get list of required capabilities | ✅ Complete |
| `help(func)` | Get documentation with capabilities | ✅ Complete |

---

## Gap Analysis

### 1. ✅ COVERED: Basic Inspection
- Check if I have a capability: `hasCapability()` ✅
- List all my capabilities: `getCapabilities()` ✅
- Check what a function needs: `requiredCapabilities()` ✅

### 2. ✅ COVERED: Detailed Information
- Get capability constraints: `getCapabilityInfo()` ✅
- Get usage statistics: `getCapabilityInfo()` ✅
- Get expiration info: `getCapabilityInfo()` ✅

### 3. ⚠️ POTENTIAL GAP: Batch Operations

**Missing:**
```ml
// Check multiple capabilities at once
canCallAll = checkCapabilities(["file.read", "file.write", "network.http"]);

// Check if can call multiple functions
canCallFuncs = canCallAll([file.read, http.get, db.query]);
```

**Workaround Available:**
```ml
// Can be implemented by users
function hasAllCapabilities(caps) {
    for (cap in caps) {
        if (!hasCapability(cap)) {
            return false;
        }
    }
    return true;
}
```

**Assessment:** Not essential - easily implemented by users

### 4. ⚠️ POTENTIAL GAP: Capability Discovery

**Missing:**
```ml
// Discover all available capability types in the system
allKnownCapabilities = getSystemCapabilities();
// ["file.read", "file.write", "network.http", "network.dns", "gui.create", ...]

// Get capability categories
categories = getCapabilityCategories();
// ["file", "network", "gui", "database", ...]
```

**Assessment:**
- Current system doesn't expose system-wide capability catalog
- Only shows what YOU have, not what EXISTS
- Could be useful for development/debugging
- Not essential for production code

### 5. ⚠️ POTENTIAL GAP: Transitive Analysis

**Missing:**
```ml
// Find ALL capabilities needed by a function including nested calls
function processData() {
    content = file.read("data.txt");
    result = http.post("https://api.com", content);
    db.save(result);
}

allRequired = getAllRequiredCapabilities(processData);
// ["file.read", "network.http", "database.write"]
```

**Assessment:**
- Very complex to implement (requires full call graph analysis)
- Would need static analysis of function body
- Current system only checks direct function metadata
- Nice-to-have but not essential

### 6. ✅ COVERED: Capability Validation

**Current:**
```ml
// Check if capability is valid/expired
info = getCapabilityInfo("file.read");
isValid = info.available;  // ✅ Available
```

**Assessment:** Already handled by `getCapabilityInfo()`

### 7. ⚠️ POTENTIAL GAP: Capability Comparison

**Missing:**
```ml
// Compare capability requirements with available capabilities
analysis = compareCapabilities(file.read);
// {
//   "required": ["file.read"],
//   "available": ["file.read", "file.write"],
//   "missing": [],
//   "can_call": true
// }
```

**Workaround Available:**
```ml
function analyzeFunction(func) {
    required = requiredCapabilities(func);
    available = getCapabilities();
    missing = [];

    for (cap in required) {
        if (!hasCapability(cap)) {
            missing = missing + [cap];
        }
    }

    return {
        required: required,
        available: available,
        missing: missing,
        can_call: len(missing) == 0
    };
}
```

**Assessment:** Not essential - easily implemented by users

### 8. ⚠️ POTENTIAL GAP: Capability Request/Grant

**Missing:**
```ml
// Request additional capability at runtime
requestCapability("network.http", {timeout: 60});

// Grant temporary capability (if permitted)
grantCapability("file.read", {patterns: ["*.txt"]}, expiration);

// Revoke capability
revokeCapability("network.http");
```

**Assessment:**
- This is **runtime capability management**, not inspection
- Different feature category
- Potentially dangerous (security implications)
- May require privileged context
- Not part of inspection API

### 9. ✅ COVERED: Help/Documentation

**Current:**
```ml
help(file.read);  // Shows description + "Requires: file.read"
```

**Assessment:** Complete with recent enhancement

### 10. ⚠️ POTENTIAL GAP: Capability Metadata

**Missing:**
```ml
// Get information about a capability TYPE (not instance)
capabilitySpec = getCapabilitySpec("file.read");
// {
//   "name": "file.read",
//   "category": "file",
//   "description": "Read file contents",
//   "risk_level": "medium",
//   "typical_constraints": ["patterns", "max_size"]
// }
```

**Assessment:**
- System-level metadata, not user-specific
- Useful for development/documentation
- Not essential for production code
- Could be added to documentation instead

---

## Recommendations

### Essential Missing Features: NONE ✅

The current capability inspection API is **comprehensive** for essential use cases:

1. ✅ Check if I have a capability
2. ✅ List all my capabilities
3. ✅ Get detailed capability info (constraints, usage, expiration)
4. ✅ Check what a function needs
5. ✅ Get function documentation with capabilities

### Nice-to-Have Enhancements (Low Priority)

#### 1. Batch Capability Check (Low Priority)
**Utility:** Convenience function
**Implementation Effort:** Trivial
**User Workaround:** Easy (users can implement in ML)

```ml
// Proposed addition
function hasAllCapabilities(capabilities) {
    for (cap in capabilities) {
        if (!hasCapability(cap)) {
            return false;
        }
    }
    return true;
}

// Or as builtin
@ml_function(description="Check if all capabilities are available", capabilities=[])
def hasAllCapabilities(self, capabilities: list) -> bool:
    return all(self.hasCapability(cap) for cap in capabilities)
```

#### 2. System Capability Discovery (Low Priority)
**Utility:** Development/debugging
**Implementation Effort:** Moderate
**User Workaround:** Check documentation

```ml
// Proposed addition
function getSystemCapabilities() {
    // Return catalog of all capability types defined in system
    // Useful for development, not production
}
```

#### 3. Capability Analysis Helper (Low Priority)
**Utility:** Convenience wrapper
**Implementation Effort:** Trivial
**User Workaround:** Easy (users can implement in ML)

```ml
// Proposed addition
function canExecute(func) {
    required = requiredCapabilities(func);
    for (cap in required) {
        if (!hasCapability(cap)) {
            return false;
        }
    }
    return true;
}
```

---

## Conclusion

### ✅ Current State: COMPREHENSIVE

The ML capability inspection API is **complete and comprehensive** for essential use cases:

**Strengths:**
- ✅ Complete coverage of context capabilities
- ✅ Complete coverage of function requirements
- ✅ Detailed capability information (constraints, usage, limits)
- ✅ Enhanced help system
- ✅ Security-first design

**No Critical Gaps Identified**

All "missing" features are either:
1. Easily implemented by users in ML code (helper functions)
2. Development/debugging conveniences (not essential)
3. Different feature category (runtime management, not inspection)

### Recommended Action: NONE REQUIRED

The capability inspection API is **production-ready** and **feature-complete** for essential use cases. Any additional features should be considered as future enhancements based on actual user demand, not essential gaps.

---

## Future Enhancement Candidates (If Demanded)

**Only implement if users actually request:**

1. **`hasAllCapabilities(caps)`** - Batch capability check
   - Priority: Low
   - Effort: 1 hour
   - User can implement in ML

2. **`canExecute(func)`** - Simplified "can I call this" check
   - Priority: Low
   - Effort: 1 hour
   - User can implement in ML

3. **`getSystemCapabilities()`** - Discover all capability types
   - Priority: Very Low
   - Effort: 4 hours
   - Primarily for development/debugging

4. **Capability type specifications** - Documentation for each capability
   - Priority: Low
   - Effort: Documentation work
   - Better addressed in user documentation

---

**Status:** Analysis Complete
**Conclusion:** No essential gaps identified - API is comprehensive ✅
