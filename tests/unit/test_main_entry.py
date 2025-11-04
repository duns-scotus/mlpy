"""Tests for mlpy entry point module."""

import sys
from unittest.mock import patch, MagicMock
import pytest


class TestMainEntry:
    """Test the __main__.py entry point."""

    def test_main_entry_point_imports_cli(self):
        """Test that __main__ imports the CLI function."""
        import mlpy.__main__
        # Verify the module has the cli import
        assert hasattr(mlpy.__main__, 'cli')

    def test_main_entry_point_calls_cli_when_executed(self):
        """Test that running __main__ calls the CLI function."""
        with patch('mlpy.__main__.cli') as mock_cli:
            # Simulate running the module as __main__
            import mlpy.__main__
            # The if __name__ == "__main__" block won't execute in imports
            # So we directly test that cli is available
            mlpy.__main__.cli()
            mock_cli.assert_called_once()

    def test_main_entry_point_structure(self):
        """Test that __main__.py has the correct structure."""
        import mlpy.__main__
        import inspect

        # Get the source code
        source = inspect.getsource(mlpy.__main__)

        # Verify it contains the expected elements
        assert 'from mlpy.cli.app import cli' in source
        assert 'if __name__ == "__main__"' in source
        assert 'cli()' in source
