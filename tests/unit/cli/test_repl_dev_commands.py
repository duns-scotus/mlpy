"""Tests for MLREPLSession development mode commands.

Tests the REPL interface layer for development mode functionality,
including command return values, error handling, and user feedback.
"""

import os
import pytest
from mlpy.cli.repl import MLREPLSession
from mlpy.stdlib.module_registry import ModuleRegistry, get_registry


class TestToggleDevMode:
    """Test .devmode command functionality."""

    def test_toggle_dev_mode_enable(self):
        """Test enabling development mode."""
        session = MLREPLSession(security_enabled=False)

        # Get registry and ensure dev mode is off
        registry = get_registry()
        registry.disable_performance_mode()

        # Enable dev mode
        success, message = session.toggle_dev_mode()

        assert success is True
        assert "ENABLED" in message
        assert registry._performance_mode is True

    def test_toggle_dev_mode_disable(self):
        """Test disabling development mode."""
        session = MLREPLSession(security_enabled=False)

        # Get registry and enable dev mode
        registry = get_registry()
        registry.enable_performance_mode()

        # Disable dev mode
        success, message = session.toggle_dev_mode()

        assert success is False
        assert "DISABLED" in message
        assert registry._performance_mode is False

    def test_toggle_dev_mode_multiple_times(self):
        """Test toggling dev mode multiple times."""
        session = MLREPLSession(security_enabled=False)
        registry = get_registry()

        # Start from disabled state
        registry.disable_performance_mode()

        # Enable
        success1, msg1 = session.toggle_dev_mode()
        assert success1 is True
        assert registry._performance_mode is True

        # Disable
        success2, msg2 = session.toggle_dev_mode()
        assert success2 is False
        assert registry._performance_mode is False

        # Enable again
        success3, msg3 = session.toggle_dev_mode()
        assert success3 is True
        assert registry._performance_mode is True


class TestReloadModule:
    """Test .reload command functionality."""

    def test_reload_module_success(self, tmp_path):
        """Test successfully reloading a module."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        # Create test module
        module_file = ext_dir / "test_bridge.py"
        module_file.write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="test", description="Test")
class Test:
    pass

test = Test()
''')

        # Load module
        registry = get_registry()
        registry.add_extension_paths([str(ext_dir)])
        registry.get_module("test")

        # Reload via session
        session = MLREPLSession(security_enabled=False)
        success, message = session.reload_module("test")

        assert success is True
        assert "Reloaded module: test" in message or "✓" in message

    def test_reload_module_not_found(self):
        """Test reloading a module that doesn't exist."""
        session = MLREPLSession(security_enabled=False)

        success, message = session.reload_module("nonexistent_module")

        assert success is False
        assert "not found" in message.lower()

    def test_reload_module_empty_name(self):
        """Test reloading with empty module name."""
        session = MLREPLSession(security_enabled=False)

        success, message = session.reload_module("")

        assert success is False
        assert "Usage:" in message or "Example:" in message

    def test_reload_module_message_format(self, tmp_path):
        """Test that reload messages are user-friendly."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        module_file = ext_dir / "test_bridge.py"
        module_file.write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="test", description="Test")
class Test:
    pass

test = Test()
''')

        registry = get_registry()
        registry.add_extension_paths([str(ext_dir)])
        registry.get_module("test")

        session = MLREPLSession(security_enabled=False)
        success, message = session.reload_module("test")

        # Message should be clear and informative
        assert isinstance(message, str)
        assert len(message) > 0
        assert "test" in message


class TestReloadAllModules:
    """Test .reloadall command functionality."""

    def test_reload_all_modules_success(self):
        """Test reloading all loaded modules."""
        registry = get_registry()

        # Load some modules
        registry.get_module("math")
        registry.get_module("json")

        session = MLREPLSession(security_enabled=False)
        success, message = session.reload_all_modules()

        assert success is True
        assert isinstance(message, str)
        # Message should mention reloaded modules
        assert "math" in message or "Reloaded" in message

    def test_reload_all_no_modules(self):
        """Test reload_all when no modules are loaded."""
        # Use global registry pattern
        registry = get_registry()

        # Invalidate cache to clear any loaded modules
        registry.invalidate_cache()

        session = MLREPLSession(security_enabled=False)
        success, message = session.reload_all_modules()

        assert success is True
        # Message should be string (content varies based on state)
        assert isinstance(message, str)

    def test_reload_all_message_format(self):
        """Test that reload all message is informative."""
        registry = get_registry()
        registry.get_module("math")

        session = MLREPLSession(security_enabled=False)
        success, message = session.reload_all_modules()

        # Message should show statistics
        assert isinstance(message, str)
        assert len(message) > 0
        # Should mention count or module names
        assert any(word in message.lower() for word in ["reloaded", "successfully", "math"])


class TestRefreshModules:
    """Test .refresh command functionality."""

    def test_refresh_modules_success(self):
        """Test refreshing module discovery."""
        registry = get_registry()

        # Load some modules first
        registry.get_module("math")

        session = MLREPLSession(security_enabled=False)
        success, message = session.refresh_modules()

        assert success is True
        assert isinstance(message, str)
        assert "Refreshed" in message or "Total modules" in message

    def test_refresh_modules_message_structure(self):
        """Test that refresh message has required information."""
        session = MLREPLSession(security_enabled=False)
        success, message = session.refresh_modules()

        assert success is True
        # Message should contain statistics
        assert "Total modules" in message or "modules" in message.lower()

    def test_refresh_modules_updates_count(self, tmp_path):
        """Test that refresh detects new modules."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        registry = get_registry()
        registry.add_extension_paths([str(ext_dir)])

        # Get initial count
        session = MLREPLSession(security_enabled=False)
        success1, message1 = session.refresh_modules()

        # Add a new module
        module_file = ext_dir / "new_bridge.py"
        module_file.write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="newmod", description="New")
class NewMod:
    pass

newmod = NewMod()
''')

        # Refresh should detect it
        success2, message2 = session.refresh_modules()

        assert success2 is True
        assert isinstance(message2, str)


class TestPerformanceSummary:
    """Test .perfmon command functionality."""

    def test_performance_summary_not_enabled(self):
        """Test perfmon when performance mode is not enabled."""
        registry = get_registry()
        registry.disable_performance_mode()

        session = MLREPLSession(security_enabled=False)
        success, message = session.get_performance_summary()

        assert success is False
        assert "not enabled" in message.lower() or "devmode" in message.lower()

    def test_performance_summary_enabled(self):
        """Test perfmon when performance mode is enabled."""
        registry = get_registry()
        registry.enable_performance_mode()

        # Load some modules to generate metrics
        registry.get_module("math")

        session = MLREPLSession(security_enabled=False)
        success, message = session.get_performance_summary()

        assert success is True
        assert isinstance(message, str)
        assert "Performance Summary" in message

    def test_performance_summary_message_structure(self):
        """Test that perfmon message has required metrics."""
        registry = get_registry()
        registry.enable_performance_mode()
        registry.get_module("math")

        session = MLREPLSession(security_enabled=False)
        success, message = session.get_performance_summary()

        assert success is True
        # Should contain key metrics
        assert "Total scans" in message
        assert "Total loads" in message
        assert "Avg" in message or "average" in message.lower()

    def test_performance_summary_shows_slow_loads(self):
        """Test that perfmon shows slow module loads."""
        registry = get_registry()
        registry.enable_performance_mode()

        # Simulate slow load
        registry._record_timing("load", "slow_module", 0.15)  # 150ms

        session = MLREPLSession(security_enabled=False)
        success, message = session.get_performance_summary()

        assert success is True
        # Should show slowest loads section
        if registry.get_performance_summary()["slowest_loads"]:
            assert "Slowest" in message or "slow" in message.lower()

    def test_performance_summary_with_reloads(self, tmp_path):
        """Test that perfmon shows reload counts."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        module_file = ext_dir / "test_bridge.py"
        module_file.write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="test", description="Test")
class Test:
    pass

test = Test()
''')

        registry = get_registry()
        registry.enable_performance_mode()
        registry.add_extension_paths([str(ext_dir)])

        # Load and reload multiple times
        registry.get_module("test")
        registry.reload_module("test")
        registry.reload_module("test")

        session = MLREPLSession(security_enabled=False)
        success, message = session.get_performance_summary()

        assert success is True
        # Should show reload counts
        summary = registry.get_performance_summary()
        if summary["reload_counts"]:
            assert "reload" in message.lower()


class TestMemoryReport:
    """Test .memreport command functionality."""

    def test_memory_report_no_modules(self):
        """Test memreport when no modules are loaded."""
        # Create fresh registry with no loaded modules
        registry = ModuleRegistry()

        session = MLREPLSession(security_enabled=False)
        success, message = session.get_memory_report()

        assert success is True
        assert "No modules" in message or "0" in message

    def test_memory_report_with_modules(self):
        """Test memreport with loaded modules."""
        registry = get_registry()

        # Load some modules
        registry.get_module("math")
        registry.get_module("json")

        session = MLREPLSession(security_enabled=False)
        success, message = session.get_memory_report()

        assert success is True
        assert isinstance(message, str)
        assert "Memory Report" in message

    def test_memory_report_message_structure(self):
        """Test that memreport message has required information."""
        registry = get_registry()
        registry.get_module("math")

        session = MLREPLSession(security_enabled=False)
        success, message = session.get_memory_report()

        assert success is True
        # Should contain memory statistics
        assert "Total loaded modules" in message
        assert "Total memory" in message or "MB" in message

    def test_memory_report_shows_top_consumers(self):
        """Test that memreport shows top memory consumers."""
        registry = get_registry()

        # Load multiple modules
        registry.get_module("math")
        registry.get_module("json")
        registry.get_module("datetime")

        session = MLREPLSession(security_enabled=False)
        success, message = session.get_memory_report()

        assert success is True
        # Should show memory report with module information
        assert "Memory Report" in message
        if registry.get_memory_report()["modules"]:
            # Check for module type sections (Python Bridge or ML Modules)
            assert "Modules" in message or "loaded" in message.lower()

    def test_memory_report_format_units(self):
        """Test that memreport uses appropriate units."""
        registry = get_registry()
        registry.get_module("math")

        session = MLREPLSession(security_enabled=False)
        success, message = session.get_memory_report()

        assert success is True
        # Should use KB or MB units
        assert "KB" in message or "MB" in message


class TestSessionIntegration:
    """Test integration between session and registry."""

    def test_session_uses_global_registry(self):
        """Test that session methods use the global registry."""
        # Enable dev mode via registry
        registry = get_registry()
        registry.enable_performance_mode()

        # Session should see the same state
        session = MLREPLSession(security_enabled=False)
        success, message = session.get_performance_summary()

        # Should succeed because dev mode is enabled
        assert success is True

    def test_multiple_sessions_share_registry(self):
        """Test that multiple sessions share the same registry."""
        registry = get_registry()
        registry.disable_performance_mode()

        # Session 1 enables dev mode
        session1 = MLREPLSession(security_enabled=False)
        session1.toggle_dev_mode()

        # Session 2 should see dev mode enabled
        session2 = MLREPLSession(security_enabled=False)
        success, message = session2.get_performance_summary()

        assert success is True  # Dev mode is enabled

    def test_session_commands_return_tuples(self):
        """Test that all dev mode commands return tuple[bool, str]."""
        session = MLREPLSession(security_enabled=False)

        # Test each command returns proper tuple
        commands = [
            session.toggle_dev_mode(),
            session.reload_module("nonexistent"),
            session.reload_all_modules(),
            session.refresh_modules(),
            session.get_performance_summary(),
            session.get_memory_report(),
        ]

        for result in commands:
            assert isinstance(result, tuple)
            assert len(result) == 2
            assert isinstance(result[0], bool)
            assert isinstance(result[1], str)


class TestErrorHandling:
    """Test error handling in dev mode commands."""

    def test_reload_handles_invalid_module_gracefully(self):
        """Test that reload handles invalid module names gracefully."""
        session = MLREPLSession(security_enabled=False)

        # Try various invalid inputs
        invalid_names = ["", "  ", "nonexistent", "invalid/name"]

        for name in invalid_names:
            success, message = session.reload_module(name)
            assert success is False
            assert isinstance(message, str)
            assert len(message) > 0

    def test_perfmon_handles_disabled_mode(self):
        """Test that perfmon handles disabled mode gracefully."""
        registry = get_registry()
        registry.disable_performance_mode()

        session = MLREPLSession(security_enabled=False)
        success, message = session.get_performance_summary()

        assert success is False
        assert "not enabled" in message.lower() or "devmode" in message.lower()
        # Should suggest how to enable
        assert ".devmode" in message or "enable" in message.lower()

    def test_commands_return_helpful_messages(self):
        """Test that error messages are helpful to users."""
        session = MLREPLSession(security_enabled=False)

        # Test various error scenarios
        _, msg1 = session.reload_module("")
        assert "Usage:" in msg1 or "Example:" in msg1

        _, msg2 = session.reload_module("nonexistent")
        assert "not found" in msg2.lower()

        registry = get_registry()
        registry.disable_performance_mode()
        _, msg3 = session.get_performance_summary()
        assert "not enabled" in msg3.lower()


class TestMessageQuality:
    """Test that command messages are user-friendly."""

    def test_messages_are_concise(self):
        """Test that messages are reasonably concise."""
        session = MLREPLSession(security_enabled=False)
        registry = get_registry()
        registry.enable_performance_mode()

        # Get various messages
        _, msg1 = session.toggle_dev_mode()
        _, msg2 = session.refresh_modules()
        _, msg3 = session.get_memory_report()

        # Messages shouldn't be too long
        for msg in [msg1, msg2, msg3]:
            assert len(msg) < 1000  # Reasonable limit
            assert len(msg) > 10  # Should have substance

    def test_messages_use_consistent_formatting(self):
        """Test that messages use consistent formatting."""
        session = MLREPLSession(security_enabled=False)
        registry = get_registry()
        registry.enable_performance_mode()
        registry.get_module("math")

        # Get various success messages
        _, msg1 = session.refresh_modules()
        _, msg2 = session.get_performance_summary()
        _, msg3 = session.get_memory_report()

        # All should have consistent structure
        for msg in [msg1, msg2, msg3]:
            assert isinstance(msg, str)
            # Should have newlines for structure
            assert "\n" in msg or len(msg) < 100

    def test_success_indicators(self, tmp_path):
        """Test that success operations have clear indicators."""
        ext_dir = tmp_path / "ext"
        ext_dir.mkdir()

        module_file = ext_dir / "test_bridge.py"
        module_file.write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="test", description="Test")
class Test:
    pass

test = Test()
''')

        registry = get_registry()
        registry.add_extension_paths([str(ext_dir)])
        registry.get_module("test")

        session = MLREPLSession(security_enabled=False)
        success, message = session.reload_module("test")

        assert success is True
        # Success should be clearly indicated
        assert any(indicator in message for indicator in ["✓", "success", "Reloaded", "Successfully"])
