"""Command-line argument parsing module for ML.

This module provides functions for parsing command-line arguments with support
for flags, options, positional arguments, and automatic help text generation.

Required Capabilities:
    - args.read: Read command-line arguments

Example:
    ```ml
    import args;

    // Create parser
    parser = args.create_parser("My Tool", "Process files");

    // Add arguments
    parser.add_flag("verbose", "v", "Enable verbose output");
    parser.add_option("output", "o", "Output file", "output.txt");
    parser.add_positional("input", "Input file", true);

    // Parse and use
    parsed = parser.parse();
    if (parsed.get_bool("verbose")) {
        console.log("Processing: " + parsed.get("input"));
    }
    ```
"""

import sys
from typing import Any, Optional

from mlpy.stdlib.decorators import ml_module, ml_function, ml_class


@ml_class(description="Command-line argument parser with schema-based validation")
class ArgParser:
    """Command-line argument parser with schema-based validation."""

    def __init__(self, name: str, description: str = ""):
        """Initialize argument parser.

        Args:
            name: Program name
            description: Program description
        """
        self.name = name
        self.description = description
        self.flags = {}  # {name: {short, help}}
        self.options = {}  # {name: {short, help, default}}
        self.positionals = []  # [{name, help, required}]
        self._parsed = None

    def add_flag(self, name: str, short: Optional[str], help_text: str):
        """Add boolean flag argument.

        Args:
            name: Long flag name (e.g., "verbose")
            short: Short flag name (e.g., "v"), or null
            help_text: Help text for this flag

        Example:
            ```ml
            parser.add_flag("verbose", "v", "Enable verbose output");
            ```
        """
        self.flags[name] = {"short": short, "help": help_text}

    def add_option(
        self, name: str, short: Optional[str], help_text: str, default: Any
    ):
        """Add option argument with value.

        Args:
            name: Long option name (e.g., "output")
            short: Short option name (e.g., "o"), or null
            help_text: Help text for this option
            default: Default value if not provided

        Example:
            ```ml
            parser.add_option("output", "o", "Output file", "output.txt");
            ```
        """
        self.options[name] = {"short": short, "help": help_text, "default": default}

    def add_positional(self, name: str, help_text: str, required: bool = False):
        """Add positional argument.

        Args:
            name: Argument name
            help_text: Help text for this argument
            required: Whether argument is required (default: False)

        Example:
            ```ml
            parser.add_positional("input", "Input file to process", true);
            ```
        """
        self.positionals.append({"name": name, "help": help_text, "required": required})

    def parse(self, argv: Optional[list[str]] = None):
        """Parse command-line arguments.

        Args:
            argv: Arguments to parse (defaults to sys.argv[1:])

        Returns:
            ParsedArgs object with parsed values

        Raises:
            ValueError: If invalid arguments or missing required values

        Example:
            ```ml
            parsed = parser.parse();
            ```
        """
        if argv is None:
            argv = sys.argv[1:]  # Skip script name

        result = ParsedArgs()
        positional_values = []
        i = 0

        while i < len(argv):
            arg = argv[i]

            # Long flag/option (--verbose)
            if arg.startswith("--"):
                name = arg[2:]

                # Check for help flag
                if name == "help":
                    result._flags["help"] = True
                    i += 1
                    continue

                # Check if it's a known flag
                if name in self.flags:
                    result._flags[name] = True
                # Check if it's a known option
                elif name in self.options:
                    if i + 1 >= len(argv):
                        raise ValueError(f"Option --{name} requires a value")
                    result._options[name] = argv[i + 1]
                    i += 1
                else:
                    raise ValueError(f"Unknown option: {arg}")

            # Short flag/option (-v or -vf)
            elif arg.startswith("-") and len(arg) > 1 and arg != "-":
                shorts = arg[1:]

                # Handle -h for help
                if "h" in shorts:
                    result._flags["help"] = True

                for ch in shorts:
                    if ch == "h":
                        continue  # Already handled

                    # Find flag by short name
                    found = False
                    for fname, fdata in self.flags.items():
                        if fdata["short"] == ch:
                            result._flags[fname] = True
                            found = True
                            break

                    if not found:
                        # Find option by short name
                        for oname, odata in self.options.items():
                            if odata["short"] == ch:
                                if i + 1 >= len(argv):
                                    raise ValueError(f"Option -{ch} requires a value")
                                result._options[oname] = argv[i + 1]
                                i += 1
                                found = True
                                break

                    if not found:
                        raise ValueError(f"Unknown option: -{ch}")

            # Positional argument
            else:
                positional_values.append(arg)

            i += 1

        # Set defaults for options
        for name, data in self.options.items():
            if name not in result._options and data["default"] is not None:
                result._options[name] = data["default"]

        # Validate and assign positionals
        for i, pos_def in enumerate(self.positionals):
            if i < len(positional_values):
                result._positionals[pos_def["name"]] = positional_values[i]
            elif pos_def["required"]:
                raise ValueError(
                    f"Required positional argument missing: {pos_def['name']}"
                )

        self._parsed = result
        return result

    def help(self) -> str:
        """Generate help text.

        Returns:
            Formatted help text string

        Example:
            ```ml
            console.log(parser.help());
            ```
        """
        lines = []

        # Header
        if self.name:
            lines.append(self.name)
        if self.description:
            lines.append(self.description)

        # Usage
        usage = "Usage: script.ml [options]"
        for pos in self.positionals:
            if pos["required"]:
                usage += f" <{pos['name']}>"
            else:
                usage += f" [{pos['name']}]"
        lines.append("")
        lines.append(usage)

        # Positional Arguments
        if self.positionals:
            lines.append("")
            lines.append("Positional Arguments:")
            for pos in self.positionals:
                req = "(required)" if pos["required"] else "(optional)"
                lines.append(f"  {pos['name']:<18} {pos['help']} {req}")

        # Options
        lines.append("")
        lines.append("Options:")

        # Flags
        for name, data in self.flags.items():
            short = f"-{data['short']}, " if data["short"] else "    "
            lines.append(f"  {short}--{name:<15} {data['help']}")

        # Options with values
        for name, data in self.options.items():
            short = f"-{data['short']}, " if data["short"] else "    "
            opt_name = f"--{name} VALUE"
            help_text = data["help"]
            if data["default"] is not None:
                help_text += f" (default: {data['default']})"
            lines.append(f"  {short}{opt_name:<15} {help_text}")

        # Help flag
        lines.append("  -h, --help         Show this help message")

        return "\n".join(lines)


@ml_class(description="Parsed command-line arguments container")
class ParsedArgs:
    """Parsed command-line arguments container."""

    def __init__(self):
        """Initialize empty parsed arguments."""
        self._flags = {}
        self._options = {}
        self._positionals = {}

    def has(self, name: str) -> bool:
        """Check if flag or option is present.

        Args:
            name: Flag or option name

        Returns:
            True if present, False otherwise

        Example:
            ```ml
            if (parsed.has("verbose")) {
                console.log("Verbose mode enabled");
            }
            ```
        """
        return name in self._flags or name in self._options or name in self._positionals

    def get(self, name: str, default: Any = None) -> Any:
        """Get option or positional value.

        Args:
            name: Option or positional name
            default: Default value if not found

        Returns:
            Value or default

        Example:
            ```ml
            output = parsed.get("output", "default.txt");
            ```
        """
        if name in self._options:
            return self._options[name]
        if name in self._positionals:
            return self._positionals[name]
        if name in self._flags:
            return self._flags[name]
        return default

    def get_bool(self, name: str) -> bool:
        """Get flag value as boolean.

        Args:
            name: Flag name

        Returns:
            True if flag present, False otherwise

        Example:
            ```ml
            is_verbose = parsed.get_bool("verbose");
            ```
        """
        return self._flags.get(name, False)

    def flags(self) -> dict:
        """Get all flags as dictionary.

        Returns:
            Dictionary of flag names to boolean values

        Example:
            ```ml
            all_flags = parsed.flags();
            ```
        """
        return dict(self._flags)

    def options(self) -> dict:
        """Get all options as dictionary.

        Returns:
            Dictionary of option names to values

        Example:
            ```ml
            all_options = parsed.options();
            ```
        """
        return dict(self._options)

    def positionals(self) -> list:
        """Get all positional values as list.

        Returns:
            List of positional argument values

        Example:
            ```ml
            pos_values = parsed.positionals();
            ```
        """
        return list(self._positionals.values())


@ml_module(
    name="args",
    description="Command-line argument parsing",
    capabilities=["args.read"],
    version="1.0.0",
)
class Args:
    """Command-line argument operations."""

    @ml_function(
        description="Get all command-line arguments", capabilities=["args.read"]
    )
    def all(self) -> list[str]:
        """Get all command-line arguments including script name.

        Returns:
            List of all arguments

        Example:
            ```ml
            all_args = args.all();  // ["script.ml", "--verbose", "input.txt"]
            ```
        """
        return sys.argv

    @ml_function(description="Get script name", capabilities=["args.read"])
    def script(self) -> str:
        """Get script name (first argument).

        Returns:
            Script name or empty string

        Example:
            ```ml
            name = args.script();  // "script.ml"
            ```
        """
        return sys.argv[0] if sys.argv else ""

    @ml_function(
        description="Get arguments without script name", capabilities=["args.read"]
    )
    def rest(self) -> list[str]:
        """Get arguments without script name.

        Returns:
            List of arguments excluding script name

        Example:
            ```ml
            rest = args.rest();  // ["--verbose", "input.txt"]
            ```
        """
        return sys.argv[1:] if len(sys.argv) > 1 else []

    @ml_function(description="Create argument parser", capabilities=[])
    def create_parser(self, name: str = "", description: str = "") -> ArgParser:
        """Create new argument parser.

        Args:
            name: Program name
            description: Program description

        Returns:
            New ArgParser instance

        Example:
            ```ml
            parser = args.create_parser("My Tool", "Process files");
            ```
        """
        return ArgParser(name, description)


# Create singleton instance for module-level access
args = Args()
