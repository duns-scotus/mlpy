"""Security tests for REPL mode to ensure namespace access is blocked."""

import pytest
from mlpy.ml.transpiler import MLTranspiler


class TestREPLSecurityNamespaceProtection:
    """Test that REPL mode blocks dangerous Python namespace access."""

    def setup_method(self):
        """Set up test fixtures."""
        self.repl_transpiler = MLTranspiler(repl_mode=True)
        self.normal_transpiler = MLTranspiler(repl_mode=False)

    def test_block_builtins_access(self):
        """Test that __builtins__ access is blocked in REPL mode."""
        code = "builtins = __builtins__;"

        # Should fail in REPL mode
        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None  # Transpilation should fail

    def test_block_import_access(self):
        """Test that __import__ access is blocked in REPL mode."""
        code = "imp = __import__;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None

    def test_block_globals_access(self):
        """Test that globals access is blocked in REPL mode."""
        code = "g = globals;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None

    def test_block_locals_access(self):
        """Test that locals access is blocked in REPL mode."""
        code = "l = locals;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None

    def test_block_eval_identifier(self):
        """Test that eval as identifier is blocked in REPL mode."""
        code = "e = eval;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None

    def test_block_exec_identifier(self):
        """Test that exec as identifier is blocked in REPL mode."""
        code = "e = exec;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None

    def test_block_dict_access(self):
        """Test that __dict__ access is blocked in REPL mode."""
        code = "d = __dict__;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None

    def test_block_class_access(self):
        """Test that __class__ access is blocked in REPL mode."""
        code = "c = __class__;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None

    def test_block_bases_access(self):
        """Test that __bases__ access is blocked in REPL mode."""
        code = "b = __bases__;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None

    def test_block_subclasses_access(self):
        """Test that __subclasses__ access is blocked in REPL mode."""
        code = "s = __subclasses__;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None

    def test_block_code_access(self):
        """Test that __code__ access is blocked in REPL mode."""
        code = "c = __code__;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None

    def test_block_globals_dunder_access(self):
        """Test that __globals__ access is blocked in REPL mode."""
        code = "g = __globals__;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None

    def test_block_open_identifier(self):
        """Test that open as identifier is blocked in REPL mode."""
        code = "f = open;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is None

    def test_allow_safe_undefined_variables(self):
        """Test that safe undefined variables are still allowed in REPL mode."""
        code = "result = previous_value + 10;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        # Should succeed - assumes previous_value exists from previous statement
        assert python_code is not None
        assert len(issues) == 0

    def test_allow_safe_variables_with_underscores(self):
        """Test that safe variables with underscores are allowed."""
        code = "my_variable = other_variable + 5;"

        python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
        assert python_code is not None
        assert len(issues) == 0

    def test_namespace_attack_scenario_blocked(self):
        """Test that a complete namespace attack is blocked."""
        # This would be a real attack: get builtins, extract eval, execute code
        attack_codes = [
            "builtins = __builtins__;",
            "imp = __import__;",
            "g = globals;",
        ]

        for attack_code in attack_codes:
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(attack_code)
            assert python_code is None, f"Attack code should be blocked: {attack_code}"

    def test_reflection_attack_blocked(self):
        """Test that reflection-based attacks are blocked."""
        reflection_attacks = [
            "c = __class__;",
            "b = __bases__;",
            "s = __subclasses__;",
            "m = __mro__;",
        ]

        for attack_code in reflection_attacks:
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(attack_code)
            assert python_code is None, f"Reflection attack should be blocked: {attack_code}"

    def test_code_object_attack_blocked(self):
        """Test that code object access is blocked."""
        code_attacks = [
            "c = __code__;",
            "g = __globals__;",
            "closure = __closure__;",
        ]

        for attack_code in code_attacks:
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(attack_code)
            assert python_code is None, f"Code object attack should be blocked: {attack_code}"

    def test_normal_mode_still_blocks_all_undefined(self):
        """Test that normal mode still blocks all undefined identifiers."""
        # In normal mode, even safe undefined variables should be blocked
        code = "result = undefined_var + 10;"

        python_code, issues, _ = self.normal_transpiler.transpile_to_python(code)
        assert python_code is None  # Normal mode blocks undefined vars

    def test_dangerous_identifiers_comprehensive_list(self):
        """Test all dangerous identifiers in the blocklist."""
        dangerous_ids = [
            '__builtins__', '__import__', '__loader__', '__spec__',
            'eval', 'exec', 'compile', 'execfile',
            'globals', 'locals', 'vars', 'dir',
            '__dict__', '__class__', '__bases__', '__subclasses__',
            '__mro__', '__init__', '__new__', '__call__',
            '__code__', '__globals__', '__closure__',
            '__name__', '__file__', '__package__', '__path__',
            'open', '__input__',  # Note: 'input' is allowed - it's a safe ML builtin wrapper
            'exit', 'quit', 'copyright', 'credits', 'license'
        ]

        # Note: 'help' and 'input' are excluded from this list because they are
        # legitimate ML builtin functions that are safely wrapped and don't
        # provide direct Python namespace access

        for dangerous_id in dangerous_ids:
            code = f"x = {dangerous_id};"
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            assert python_code is None, f"Dangerous identifier '{dangerous_id}' should be blocked"

    def test_security_error_message_helpful(self):
        """Test that security error messages are helpful."""
        code = "builtins = __builtins__;"

        try:
            python_code, issues, _ = self.repl_transpiler.transpile_to_python(code)
            # Check that we got an error (python_code is None)
            assert python_code is None
        except ValueError as e:
            # If ValueError is raised directly, check the message
            assert "Security" in str(e)
            assert "__builtins__" in str(e)
            assert "not allowed" in str(e)
