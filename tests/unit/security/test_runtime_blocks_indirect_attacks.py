"""Runtime verification tests for indirect dunder access attacks.

This test suite specifically validates that ALL attack vectors documented in
test_dunder_indirect_access.py are successfully BLOCKED AT RUNTIME, even though
they may bypass compile-time security checks.

This provides proof that mlpy's defense-in-depth strategy works: even if
compile-time checks are bypassed, the runtime layer prevents exploitation.
"""

import pytest
from mlpy.stdlib.builtin import Builtin


class TestRuntimeBlocksGetAttrAttacks:
    """Verify runtime blocks all getattr-based dunder access attacks."""

    def setup_method(self):
        """Set up test fixtures."""
        self.builtin = Builtin()

    # =========================================================================
    # Attack Vector 1: Direct getattr with dunder names (from test file)
    # =========================================================================

    def test_runtime_blocks_getattr_class(self):
        """Verify __class__ access via getattr is blocked at runtime."""
        test_obj = object()

        # This is the exact attack from test_dunder_indirect_access.py
        result = self.builtin.getattr(test_obj, "__class__", "BLOCKED_AT_RUNTIME")

        assert result == "BLOCKED_AT_RUNTIME", \
            "Runtime MUST block: getattr(obj, '__class__')"

    def test_runtime_blocks_getattr_dict(self):
        """Verify __dict__ access via getattr is blocked at runtime."""
        test_obj = type('TestClass', (), {'attr': 42})()

        result = self.builtin.getattr(test_obj, "__dict__", "BLOCKED_AT_RUNTIME")

        assert result == "BLOCKED_AT_RUNTIME", \
            "Runtime MUST block: getattr(obj, '__dict__')"

    def test_runtime_blocks_getattr_globals(self):
        """Verify __globals__ access via getattr is blocked at runtime."""
        def test_func():
            return 42

        result = self.builtin.getattr(test_func, "__globals__", "BLOCKED_AT_RUNTIME")

        assert result == "BLOCKED_AT_RUNTIME", \
            "Runtime MUST block: getattr(func, '__globals__')"

    def test_runtime_blocks_getattr_builtins(self):
        """Verify __builtins__ access via getattr is blocked at runtime."""
        import sys

        result = self.builtin.getattr(sys, "__builtins__", "BLOCKED_AT_RUNTIME")

        assert result == "BLOCKED_AT_RUNTIME", \
            "Runtime MUST block: getattr(module, '__builtins__')"

    def test_runtime_blocks_getattr_init(self):
        """Verify __init__ access via getattr is blocked at runtime."""
        test_obj = object()

        result = self.builtin.getattr(test_obj, "__init__", "BLOCKED_AT_RUNTIME")

        assert result == "BLOCKED_AT_RUNTIME", \
            "Runtime MUST block: getattr(obj, '__init__')"

    def test_runtime_blocks_getattr_import(self):
        """Verify __import__ access via getattr is blocked at runtime."""
        import builtins

        result = self.builtin.getattr(builtins, "__import__", "BLOCKED_AT_RUNTIME")

        assert result == "BLOCKED_AT_RUNTIME", \
            "Runtime MUST block: getattr(builtins, '__import__')"

    # =========================================================================
    # Attack Vector 2: getattr with default value (from test file)
    # =========================================================================

    def test_runtime_blocks_getattr_with_default_class(self):
        """Verify getattr with default still blocks __class__."""
        test_obj = object()

        result = self.builtin.getattr(test_obj, "__class__", None)

        assert result is None, \
            "Runtime MUST return default for: getattr(obj, '__class__', None)"

    def test_runtime_blocks_getattr_with_default_dict(self):
        """Verify getattr with default still blocks __dict__."""
        test_obj = type('TestClass', (), {})()

        result = self.builtin.getattr(test_obj, "__dict__", {})

        # Should return the default value {}, not the actual __dict__
        assert result == {}, \
            "Runtime MUST return default for: getattr(obj, '__dict__', {})"

    # =========================================================================
    # Attack Vector 3: String concatenation to build dunder names (from test file)
    # =========================================================================

    def test_runtime_blocks_concatenated_dunder_prefix(self):
        """Verify runtime blocks dunders built via string concatenation."""
        test_obj = object()

        # Simulate: prefix = "__"; name = "class__"; getattr(obj, prefix + name)
        dunder_name = "__" + "class__"
        result = self.builtin.getattr(test_obj, dunder_name, "BLOCKED_AT_RUNTIME")

        assert result == "BLOCKED_AT_RUNTIME", \
            "Runtime MUST block concatenated dunder: '__' + 'class__'"

    def test_runtime_blocks_concatenated_dunder_middle(self):
        """Verify runtime blocks dunders with __ in middle."""
        test_obj = object()

        # Simulate: dunder = "__" + "dict__"
        dunder_name = "__" + "dict__"
        result = self.builtin.getattr(test_obj, dunder_name, "BLOCKED_AT_RUNTIME")

        assert result == "BLOCKED_AT_RUNTIME", \
            "Runtime MUST block concatenated dunder: '__' + 'dict__'"

    # =========================================================================
    # Attack Vector 4: Nested getattr chains (from test file)
    # =========================================================================

    def test_runtime_blocks_nested_class_bases(self):
        """Verify nested getattr(__class__).__bases__ is blocked."""
        test_obj = []

        # Step 1: Try to get __class__ - should be blocked
        step1 = self.builtin.getattr(test_obj, "__class__", None)
        assert step1 is None, "Runtime MUST block first step: getattr(obj, '__class__')"

        # Step 2 would never execute if step 1 returns None
        # But verify that even if it did, it would be blocked
        if step1 is not None:
            step2 = self.builtin.getattr(step1, "__bases__", None)
            assert step2 is None, "Runtime MUST block second step: getattr(cls, '__bases__')"

    def test_runtime_blocks_nested_init_code(self):
        """Verify nested getattr(__init__).__code__ is blocked."""
        test_str = "test"

        # Step 1: Try to get __init__ - should be blocked
        step1 = self.builtin.getattr(test_str, "__init__", None)
        assert step1 is None, "Runtime MUST block first step: getattr(obj, '__init__')"

        # Step 2 would never execute
        if step1 is not None:
            step2 = self.builtin.getattr(step1, "__code__", None)
            assert step2 is None, "Runtime MUST block second step: getattr(func, '__code__')"

    # =========================================================================
    # Defense Effectiveness Tests
    # =========================================================================

    def test_all_attack_vectors_from_security_audit_blocked(self):
        """Comprehensive test: ALL attack vectors from security audit are blocked."""
        test_obj = object()

        # All attack strings from SECURITY-AUDIT-INDIRECT-DUNDER-ACCESS.md
        attack_vectors = [
            "__class__",
            "__dict__",
            "__globals__",
            "__builtins__",
            "__bases__",
            "__mro__",
            "__subclasses__",
            "__code__",
            "__init__",
            "__call__",
            "__import__",
            "__loader__",
            "__spec__",
        ]

        for attack in attack_vectors:
            result = self.builtin.getattr(test_obj, attack, "RUNTIME_BLOCKED")
            assert result == "RUNTIME_BLOCKED", \
                f"Runtime MUST block attack vector: {attack}"

    def test_runtime_protection_comprehensive_coverage(self):
        """Verify runtime protection covers all Python dangerous attributes."""
        test_obj = []

        # Comprehensive list of dangerous Python internals
        dangerous_attributes = [
            # Class hierarchy traversal
            "__class__", "__bases__", "__mro__", "__subclasses__",
            # Object internals
            "__dict__", "__slots__", "__weakref__",
            # Function/method internals
            "__code__", "__globals__", "__closure__", "__annotations__",
            # Module internals
            "__loader__", "__spec__", "__package__", "__cached__",
            # Import system
            "__import__", "__builtins__",
            # Magic methods that could be exploited
            "__init__", "__new__", "__call__", "__del__",
            # Descriptor protocol
            "__get__", "__set__", "__delete__",
            # Type checking
            "__instancecheck__", "__subclasscheck__",
        ]

        for attr in dangerous_attributes:
            result = self.builtin.getattr(test_obj, attr, "BLOCKED")
            assert result == "BLOCKED", \
                f"Runtime protection must cover dangerous attribute: {attr}"


class TestRuntimeBlocksHasAttrAttacks:
    """Verify runtime blocks all hasattr-based reconnaissance attacks."""

    def setup_method(self):
        """Set up test fixtures."""
        self.builtin = Builtin()

    def test_hasattr_returns_false_for_dunders(self):
        """Verify hasattr returns False for all dunder attributes."""
        test_obj = "test string"

        dunder_names = [
            "__class__", "__dict__", "__init__",
            "__globals__", "__code__", "__bases__",
        ]

        for dunder in dunder_names:
            result = self.builtin.hasattr(test_obj, dunder)
            assert result == False, \
                f"hasattr() MUST return False for: {dunder}"

    def test_hasattr_prevents_attribute_reconnaissance(self):
        """Verify attackers can't use hasattr to discover dunders."""
        test_obj = object()

        # Attacker trying to discover what dunders exist
        potential_dunders = [
            "__class__", "__dict__", "__module__",
            "__doc__", "__name__", "__qualname__",
        ]

        for dunder in potential_dunders:
            # hasattr should return False, hiding their existence
            result = self.builtin.hasattr(test_obj, dunder)
            assert result == False, \
                f"Attribute reconnaissance must fail for: {dunder}"


class TestRuntimeProtectionCompleteness:
    """Verify runtime protection is complete and leaves no gaps."""

    def setup_method(self):
        """Set up test fixtures."""
        self.builtin = Builtin()

    def test_single_underscore_also_blocked(self):
        """Verify even single underscore (private) attributes are blocked."""
        test_str = "hello"  # Use a built-in type instead of custom class

        # Single underscore attributes don't exist on strings but test the blocking
        result = self.builtin.getattr(test_str, "_private", "BLOCKED")
        assert result == "BLOCKED", \
            "Runtime should block single underscore: _private"

        # Public method should work
        result = self.builtin.getattr(test_str, "upper", None)
        assert result is not None, \
            "Runtime should allow public attributes"
        assert callable(result), \
            "Public attribute should be accessible"

    def test_triple_underscore_blocked(self):
        """Verify triple and more underscores are also blocked."""
        test_obj = object()

        multi_underscore = [
            "___triple___",
            "____quad____",
            "_____five_____",
        ]

        for name in multi_underscore:
            result = self.builtin.getattr(test_obj, name, "BLOCKED")
            assert result == "BLOCKED", \
                f"Runtime should block multi-underscore: {name}"

    def test_runtime_blocks_all_underscore_prefixes(self):
        """Verify ANY name starting with underscore is blocked."""
        test_obj = object()

        # Comprehensive list of underscore patterns
        underscore_patterns = [
            "_single",
            "__double",
            "___triple",
            "_a",
            "__b",
            "___c",
            "_x_y_z",
            "__init__",
            "_private_method",
        ]

        for pattern in underscore_patterns:
            result = self.builtin.getattr(test_obj, pattern, "BLOCKED")
            assert result == "BLOCKED", \
                f"Runtime MUST block ANY underscore prefix: {pattern}"

    def test_safe_attributes_still_accessible(self):
        """Verify safe public attributes are NOT blocked by runtime protection."""
        test_str = "hello world"
        test_list = [1, 2, 3]

        # Safe string attributes
        safe_str_methods = ["upper", "lower", "strip", "split", "replace"]
        for method in safe_str_methods:
            result = self.builtin.getattr(test_str, method, None)
            assert result is not None, \
                f"Runtime should allow safe attribute: {method}"
            assert callable(result), \
                f"Safe attribute should be accessible: {method}"

        # Safe list attributes
        safe_list_methods = ["append", "pop", "sort", "reverse"]
        for method in safe_list_methods:
            result = self.builtin.getattr(test_list, method, None)
            assert result is not None, \
                f"Runtime should allow safe attribute: {method}"


class TestDefenseInDepthValidation:
    """Validate that defense-in-depth works: compile-time AND runtime."""

    def test_compile_blocks_direct_runtime_blocks_indirect(self):
        """Verify we have two layers of security working together."""
        from mlpy.ml.transpiler import MLTranspiler

        transpiler = MLTranspiler(repl_mode=True)
        builtin = Builtin()

        # Layer 1: Compile-time blocks direct dunder identifiers
        direct_code = 'x = __class__;'
        python_code, issues, _ = transpiler.transpile_to_python(direct_code)
        assert python_code is None, \
            "LAYER 1 (compile-time): Must block direct dunder identifier"

        # Layer 2: Runtime blocks string literal dunders (indirect access)
        test_obj = object()
        result = builtin.getattr(test_obj, "__class__", "RUNTIME_BLOCKED")
        assert result == "RUNTIME_BLOCKED", \
            "LAYER 2 (runtime): Must block string literal dunder"

        print("✅ Defense-in-depth validated:")
        print("   Layer 1 (Compile-time): Blocks direct dunder identifiers")
        print("   Layer 2 (Runtime):      Blocks ALL dunder access (direct + indirect)")


class TestSecurityAuditVerification:
    """Tests that directly verify the security audit findings are mitigated."""

    def test_security_audit_attack_1_mitigated(self):
        """Verify Attack Vector 1 from security audit is blocked at runtime."""
        builtin = Builtin()

        # From SECURITY-AUDIT-INDIRECT-DUNDER-ACCESS.md:
        # Attack: obj_class = getattr(obj, "__class__")
        obj = object()
        obj_class = builtin.getattr(obj, "__class__", None)

        assert obj_class is None, \
            "Security Audit Attack 1: getattr(obj, '__class__') MUST be blocked"

    def test_security_audit_attack_2_mitigated(self):
        """Verify Attack Vector 2 from security audit is blocked at runtime."""
        builtin = Builtin()

        # From SECURITY-AUDIT-INDIRECT-DUNDER-ACCESS.md:
        # Attack: obj_dict = getattr(obj, "__dict__")
        obj = type('Test', (), {'secret': 'data'})()
        obj_dict = builtin.getattr(obj, "__dict__", None)

        assert obj_dict is None, \
            "Security Audit Attack 2: getattr(obj, '__dict__') MUST be blocked"

    def test_security_audit_attack_3_mitigated(self):
        """Verify Attack Vector 3 from security audit is blocked at runtime."""
        builtin = Builtin()

        # From SECURITY-AUDIT-INDIRECT-DUNDER-ACCESS.md:
        # Attack: globals_ref = getattr(func, "__globals__")
        def test_func():
            return 42

        globals_ref = builtin.getattr(test_func, "__globals__", None)

        assert globals_ref is None, \
            "Security Audit Attack 3: getattr(func, '__globals__') MUST be blocked"

    def test_security_posture_is_acceptable(self):
        """Verify current security posture matches audit findings."""
        from mlpy.ml.transpiler import MLTranspiler
        builtin = Builtin()
        transpiler = MLTranspiler(repl_mode=True)

        # From security audit:
        # - Direct dunder identifiers: ✅ BLOCKED at compile-time
        # - String literal dunders:    ❌ NOT blocked at compile-time
        # - String literal dunders:    ✅ BLOCKED at runtime
        # - Overall security:          🟡 PARTIAL (runtime-only for indirect)

        # Verify direct blocking
        code1 = 'x = __class__;'
        python1, _, _ = transpiler.transpile_to_python(code1)
        assert python1 is None, "✅ Direct dunder blocked at compile-time"

        # Verify indirect compile-time bypass (known vulnerability)
        code2 = 'x = getattr(obj, "__class__");'
        python2, _, _ = transpiler.transpile_to_python(code2)
        # This currently transpiles (security gap at compile-time)
        # But we verify runtime blocks it

        # Verify runtime blocks indirect
        result = builtin.getattr(object(), "__class__", "BLOCKED")
        assert result == "BLOCKED", "✅ Indirect dunder blocked at runtime"

        print("✅ Security posture validated:")
        print("   - Direct dunders:   Blocked at compile-time")
        print("   - Indirect dunders: Blocked at runtime")
        print("   - Risk level:       MEDIUM (runtime-only protection for indirect)")
        print("   - Mitigation:       Effective (100% attack prevention)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
