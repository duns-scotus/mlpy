"""Unit tests for args_bridge module."""

import sys
import pytest

from mlpy.stdlib.args_bridge import Args, ArgParser, ParsedArgs


class TestArgsModule:
    """Test suite for basic args module operations."""

    def setup_method(self):
        """Setup for each test method."""
        self.args = Args()
        self.original_argv = sys.argv.copy()

    def teardown_method(self):
        """Cleanup after each test method."""
        sys.argv = self.original_argv

    def test_all_returns_all_arguments(self):
        """Test all() returns all command-line arguments."""
        sys.argv = ["script.ml", "--verbose", "input.txt"]
        result = self.args.all()
        assert result == ["script.ml", "--verbose", "input.txt"]

    def test_all_with_empty_argv(self):
        """Test all() with empty argv."""
        sys.argv = []
        result = self.args.all()
        assert result == []

    def test_script_returns_script_name(self):
        """Test script() returns script name."""
        sys.argv = ["script.ml", "--verbose"]
        result = self.args.script()
        assert result == "script.ml"

    def test_script_with_empty_argv(self):
        """Test script() with empty argv returns empty string."""
        sys.argv = []
        result = self.args.script()
        assert result == ""

    def test_rest_returns_arguments_without_script(self):
        """Test rest() returns arguments without script name."""
        sys.argv = ["script.ml", "--verbose", "input.txt"]
        result = self.args.rest()
        assert result == ["--verbose", "input.txt"]

    def test_rest_with_only_script(self):
        """Test rest() with only script name returns empty list."""
        sys.argv = ["script.ml"]
        result = self.args.rest()
        assert result == []

    def test_rest_with_empty_argv(self):
        """Test rest() with empty argv returns empty list."""
        sys.argv = []
        result = self.args.rest()
        assert result == []

    def test_create_parser_returns_parser_instance(self):
        """Test create_parser() returns ArgParser instance."""
        parser = self.args.create_parser("Test Tool", "Test description")
        assert isinstance(parser, ArgParser)
        assert parser.name == "Test Tool"
        assert parser.description == "Test description"

    def test_create_parser_with_empty_args(self):
        """Test create_parser() with no arguments."""
        parser = self.args.create_parser()
        assert isinstance(parser, ArgParser)
        assert parser.name == ""
        assert parser.description == ""


class TestArgParser:
    """Test suite for ArgParser class."""

    def setup_method(self):
        """Setup for each test method."""
        self.parser = ArgParser("Test Tool", "A test command-line tool")

    def test_parser_initialization(self):
        """Test parser initializes correctly."""
        assert self.parser.name == "Test Tool"
        assert self.parser.description == "A test command-line tool"
        assert self.parser.flags == {}
        assert self.parser.options == {}
        assert self.parser.positionals == []

    def test_add_flag(self):
        """Test adding a flag."""
        self.parser.add_flag("verbose", "v", "Enable verbose output")
        assert "verbose" in self.parser.flags
        assert self.parser.flags["verbose"]["short"] == "v"
        assert self.parser.flags["verbose"]["help"] == "Enable verbose output"

    def test_add_flag_without_short(self):
        """Test adding flag without short name."""
        self.parser.add_flag("debug", None, "Enable debug mode")
        assert "debug" in self.parser.flags
        assert self.parser.flags["debug"]["short"] is None

    def test_add_option(self):
        """Test adding an option."""
        self.parser.add_option("output", "o", "Output file", "output.txt")
        assert "output" in self.parser.options
        assert self.parser.options["output"]["short"] == "o"
        assert self.parser.options["output"]["help"] == "Output file"
        assert self.parser.options["output"]["default"] == "output.txt"

    def test_add_option_with_null_default(self):
        """Test adding option with null default."""
        self.parser.add_option("config", "c", "Config file", None)
        assert "config" in self.parser.options
        assert self.parser.options["config"]["default"] is None

    def test_add_positional_required(self):
        """Test adding required positional argument."""
        self.parser.add_positional("input", "Input file", True)
        assert len(self.parser.positionals) == 1
        assert self.parser.positionals[0]["name"] == "input"
        assert self.parser.positionals[0]["required"] is True

    def test_add_positional_optional(self):
        """Test adding optional positional argument."""
        self.parser.add_positional("extra", "Extra files", False)
        assert len(self.parser.positionals) == 1
        assert self.parser.positionals[0]["required"] is False

    def test_parse_long_flag(self):
        """Test parsing long flag."""
        self.parser.add_flag("verbose", "v", "Verbose")
        parsed = self.parser.parse(["--verbose"])
        assert parsed.get_bool("verbose") is True

    def test_parse_short_flag(self):
        """Test parsing short flag."""
        self.parser.add_flag("verbose", "v", "Verbose")
        parsed = self.parser.parse(["-v"])
        assert parsed.get_bool("verbose") is True

    def test_parse_multiple_short_flags(self):
        """Test parsing multiple short flags combined."""
        self.parser.add_flag("verbose", "v", "Verbose")
        self.parser.add_flag("force", "f", "Force")
        parsed = self.parser.parse(["-vf"])
        assert parsed.get_bool("verbose") is True
        assert parsed.get_bool("force") is True

    def test_parse_long_option(self):
        """Test parsing long option with value."""
        self.parser.add_option("output", "o", "Output", "default.txt")
        parsed = self.parser.parse(["--output", "custom.txt"])
        assert parsed.get("output") == "custom.txt"

    def test_parse_short_option(self):
        """Test parsing short option with value."""
        self.parser.add_option("output", "o", "Output", "default.txt")
        parsed = self.parser.parse(["-o", "custom.txt"])
        assert parsed.get("output") == "custom.txt"

    def test_parse_option_uses_default(self):
        """Test parsing uses default when option not provided."""
        self.parser.add_option("output", "o", "Output", "default.txt")
        parsed = self.parser.parse([])
        assert parsed.get("output") == "default.txt"

    def test_parse_option_without_value_raises_error(self):
        """Test parsing option without value raises ValueError."""
        self.parser.add_option("output", "o", "Output", "default.txt")
        with pytest.raises(ValueError, match="Option --output requires a value"):
            self.parser.parse(["--output"])

    def test_parse_short_option_without_value_raises_error(self):
        """Test parsing short option without value raises ValueError."""
        self.parser.add_option("output", "o", "Output", "default.txt")
        with pytest.raises(ValueError, match="Option -o requires a value"):
            self.parser.parse(["-o"])

    def test_parse_unknown_long_option_raises_error(self):
        """Test parsing unknown long option raises ValueError."""
        with pytest.raises(ValueError, match="Unknown option: --unknown"):
            self.parser.parse(["--unknown"])

    def test_parse_unknown_short_option_raises_error(self):
        """Test parsing unknown short option raises ValueError."""
        with pytest.raises(ValueError, match="Unknown option: -x"):
            self.parser.parse(["-x"])

    def test_parse_positional_argument(self):
        """Test parsing positional argument."""
        self.parser.add_positional("input", "Input file", True)
        parsed = self.parser.parse(["file.txt"])
        assert parsed.get("input") == "file.txt"

    def test_parse_multiple_positional_arguments(self):
        """Test parsing multiple positional arguments."""
        self.parser.add_positional("input", "Input file", True)
        self.parser.add_positional("output", "Output file", False)
        parsed = self.parser.parse(["input.txt", "output.txt"])
        assert parsed.get("input") == "input.txt"
        assert parsed.get("output") == "output.txt"

    def test_parse_missing_required_positional_raises_error(self):
        """Test parsing missing required positional raises ValueError."""
        self.parser.add_positional("input", "Input file", True)
        with pytest.raises(ValueError, match="Required positional argument missing: input"):
            self.parser.parse([])

    def test_parse_missing_optional_positional_ok(self):
        """Test parsing missing optional positional is ok."""
        self.parser.add_positional("input", "Input file", True)
        self.parser.add_positional("output", "Output file", False)
        parsed = self.parser.parse(["input.txt"])
        assert parsed.get("input") == "input.txt"
        assert parsed.get("output") is None

    def test_parse_complex_arguments(self):
        """Test parsing complex combination of arguments."""
        self.parser.add_flag("verbose", "v", "Verbose")
        self.parser.add_flag("force", "f", "Force")
        self.parser.add_option("output", "o", "Output", "out.txt")
        self.parser.add_option("format", None, "Format", "json")
        self.parser.add_positional("input", "Input", True)

        parsed = self.parser.parse(["-vf", "--output", "custom.txt", "--format", "xml", "input.txt"])

        assert parsed.get_bool("verbose") is True
        assert parsed.get_bool("force") is True
        assert parsed.get("output") == "custom.txt"
        assert parsed.get("format") == "xml"
        assert parsed.get("input") == "input.txt"

    def test_parse_help_flag(self):
        """Test parsing help flag."""
        parsed = self.parser.parse(["--help"])
        assert parsed.get_bool("help") is True

    def test_parse_short_help_flag(self):
        """Test parsing short help flag."""
        parsed = self.parser.parse(["-h"])
        assert parsed.get_bool("help") is True

    def test_help_generates_help_text(self):
        """Test help() generates proper help text."""
        self.parser.add_flag("verbose", "v", "Enable verbose output")
        self.parser.add_option("output", "o", "Output file", "out.txt")
        self.parser.add_positional("input", "Input file", True)

        help_text = self.parser.help()

        assert "Test Tool" in help_text
        assert "A test command-line tool" in help_text
        assert "Usage:" in help_text
        assert "<input>" in help_text
        assert "--verbose" in help_text
        assert "-v" in help_text
        assert "--output" in help_text
        assert "-o" in help_text
        assert "default: out.txt" in help_text
        assert "--help" in help_text

    def test_help_with_optional_positional(self):
        """Test help text with optional positional argument."""
        self.parser.add_positional("extra", "Extra files", False)
        help_text = self.parser.help()
        assert "[extra]" in help_text

    def test_help_with_required_positional(self):
        """Test help text with required positional argument."""
        self.parser.add_positional("input", "Input file", True)
        help_text = self.parser.help()
        assert "<input>" in help_text


class TestParsedArgs:
    """Test suite for ParsedArgs class."""

    def setup_method(self):
        """Setup for each test method."""
        self.parsed = ParsedArgs()

    def test_initialization(self):
        """Test ParsedArgs initializes correctly."""
        assert self.parsed._flags == {}
        assert self.parsed._options == {}
        assert self.parsed._positionals == {}

    def test_has_flag(self):
        """Test has() for flag."""
        self.parsed._flags["verbose"] = True
        assert self.parsed.has("verbose") is True

    def test_has_option(self):
        """Test has() for option."""
        self.parsed._options["output"] = "file.txt"
        assert self.parsed.has("output") is True

    def test_has_positional(self):
        """Test has() for positional."""
        self.parsed._positionals["input"] = "file.txt"
        assert self.parsed.has("input") is True

    def test_has_missing(self):
        """Test has() for missing argument."""
        assert self.parsed.has("missing") is False

    def test_get_option(self):
        """Test get() for option."""
        self.parsed._options["output"] = "file.txt"
        assert self.parsed.get("output") == "file.txt"

    def test_get_positional(self):
        """Test get() for positional."""
        self.parsed._positionals["input"] = "file.txt"
        assert self.parsed.get("input") == "file.txt"

    def test_get_flag(self):
        """Test get() for flag."""
        self.parsed._flags["verbose"] = True
        assert self.parsed.get("verbose") is True

    def test_get_with_default(self):
        """Test get() with default value."""
        assert self.parsed.get("missing", "default") == "default"

    def test_get_bool_true(self):
        """Test get_bool() for true flag."""
        self.parsed._flags["verbose"] = True
        assert self.parsed.get_bool("verbose") is True

    def test_get_bool_false(self):
        """Test get_bool() for missing flag."""
        assert self.parsed.get_bool("verbose") is False

    def test_flags_returns_dict(self):
        """Test flags() returns dictionary."""
        self.parsed._flags["verbose"] = True
        self.parsed._flags["force"] = True
        flags = self.parsed.flags()
        assert flags == {"verbose": True, "force": True}

    def test_flags_returns_copy(self):
        """Test flags() returns copy not reference."""
        self.parsed._flags["verbose"] = True
        flags = self.parsed.flags()
        flags["new"] = True
        assert "new" not in self.parsed._flags

    def test_options_returns_dict(self):
        """Test options() returns dictionary."""
        self.parsed._options["output"] = "file.txt"
        self.parsed._options["format"] = "json"
        options = self.parsed.options()
        assert options == {"output": "file.txt", "format": "json"}

    def test_options_returns_copy(self):
        """Test options() returns copy not reference."""
        self.parsed._options["output"] = "file.txt"
        options = self.parsed.options()
        options["new"] = "value"
        assert "new" not in self.parsed._options

    def test_positionals_returns_list(self):
        """Test positionals() returns list of values."""
        self.parsed._positionals["input"] = "file1.txt"
        self.parsed._positionals["output"] = "file2.txt"
        positionals = self.parsed.positionals()
        assert isinstance(positionals, list)
        assert len(positionals) == 2

    def test_positionals_returns_copy(self):
        """Test positionals() returns copy not reference."""
        self.parsed._positionals["input"] = "file.txt"
        positionals = self.parsed.positionals()
        positionals.append("new")
        assert len(list(self.parsed._positionals.values())) == 1


class TestArgsIntegration:
    """Integration tests for complete arg parsing workflows."""

    def test_cli_tool_workflow(self):
        """Test complete CLI tool argument parsing workflow."""
        args = Args()
        parser = args.create_parser("Data Processor", "Process CSV files")

        parser.add_flag("verbose", "v", "Verbose output")
        parser.add_flag("force", "f", "Force overwrite")
        parser.add_option("output", "o", "Output file", "output.csv")
        parser.add_option("format", None, "Format", "csv")
        parser.add_positional("input", "Input file", True)

        parsed = parser.parse(["-vf", "--output", "result.csv", "data.csv"])

        assert parsed.get_bool("verbose") is True
        assert parsed.get_bool("force") is True
        assert parsed.get("output") == "result.csv"
        assert parsed.get("format") == "csv"
        assert parsed.get("input") == "data.csv"

    def test_minimal_cli_tool(self):
        """Test minimal CLI tool with just positional."""
        args = Args()
        parser = args.create_parser("Simple Tool")
        parser.add_positional("file", "File to process", True)

        parsed = parser.parse(["input.txt"])
        assert parsed.get("file") == "input.txt"

    def test_help_requested_workflow(self):
        """Test help request workflow."""
        args = Args()
        parser = args.create_parser("My Tool", "Does things")
        parser.add_flag("verbose", "v", "Verbose")

        parsed = parser.parse(["--help"])

        if parsed.has("help"):
            help_text = parser.help()
            assert "My Tool" in help_text
            assert "Does things" in help_text
