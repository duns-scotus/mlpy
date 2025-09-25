"""
Enhanced ML CLI Application
Provides comprehensive command-line interface with project management, IDE integration, and development workflow.
"""

import sys
import os
import argparse
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from .project_manager import MLProjectManager
from .commands import (
    InitCommand, CompileCommand, RunCommand, TestCommand, AnalyzeCommand,
    WatchCommand, ServeCommand, FormatCommand, DocCommand, LSPCommand
)

class MLCLIApp:
    """Enhanced ML CLI application with comprehensive tooling."""

    def __init__(self):
        self.project_manager = MLProjectManager()
        self.commands = self._register_commands()
        self.logger = self._setup_logging()

    def _register_commands(self) -> Dict[str, Any]:
        """Register all available CLI commands."""
        return {
            'init': InitCommand(self.project_manager),
            'compile': CompileCommand(self.project_manager),
            'run': RunCommand(self.project_manager),
            'test': TestCommand(self.project_manager),
            'analyze': AnalyzeCommand(self.project_manager),
            'watch': WatchCommand(self.project_manager),
            'serve': ServeCommand(self.project_manager),
            'format': FormatCommand(self.project_manager),
            'doc': DocCommand(self.project_manager),
            'lsp': LSPCommand(self.project_manager)
        }

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger('mlpy-cli')
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def create_parser(self) -> argparse.ArgumentParser:
        """Create the main argument parser."""
        parser = argparse.ArgumentParser(
            prog='mlpy',
            description='ML Programming Language Compiler and Tools',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''
Examples:
  mlpy init my-project              Create new ML project
  mlpy compile src/main.ml          Compile ML file to Python
  mlpy run src/main.ml              Compile and run ML file
  mlpy test                         Run project tests
  mlpy analyze --security           Run security analysis
  mlpy watch src/                   Watch directory for changes
  mlpy serve --lsp                  Start Language Server
  mlpy format src/                  Format ML code
  mlpy doc build                    Build documentation

For more information, visit: https://mlpy.dev/docs
            '''
        )

        # Global options
        parser.add_argument(
            '--version', '-V',
            action='version',
            version='mlpy 2.0.0'
        )

        parser.add_argument(
            '--verbose', '-v',
            action='count',
            default=0,
            help='Increase verbosity (use -vv for debug)'
        )

        parser.add_argument(
            '--quiet', '-q',
            action='store_true',
            help='Suppress all output except errors'
        )

        parser.add_argument(
            '--config',
            type=Path,
            help='Path to configuration file'
        )

        parser.add_argument(
            '--project-root',
            type=Path,
            help='Override project root directory'
        )

        # Subcommands
        subparsers = parser.add_subparsers(
            dest='command',
            metavar='COMMAND',
            help='Available commands'
        )

        # Register command parsers
        for name, command in self.commands.items():
            command.register_parser(subparsers)

        return parser

    def configure_logging(self, verbosity: int, quiet: bool) -> None:
        """Configure logging based on verbosity level."""
        if quiet:
            level = logging.ERROR
        elif verbosity >= 2:
            level = logging.DEBUG
        elif verbosity >= 1:
            level = logging.INFO
        else:
            level = logging.WARNING

        self.logger.setLevel(level)
        logging.getLogger('mlpy').setLevel(level)

    def run(self, args: Optional[List[str]] = None) -> int:
        """Run the CLI application."""
        parser = self.create_parser()

        # Parse arguments
        if args is None:
            args = sys.argv[1:]

        parsed_args = parser.parse_args(args)

        # Configure logging
        self.configure_logging(parsed_args.verbose, parsed_args.quiet)

        # Load project configuration
        if parsed_args.project_root:
            self.project_manager.set_project_root(parsed_args.project_root)

        if parsed_args.config:
            self.project_manager.load_config(parsed_args.config)
        else:
            self.project_manager.discover_and_load_config()

        # Execute command
        if not parsed_args.command:
            parser.print_help()
            return 1

        command = self.commands.get(parsed_args.command)
        if not command:
            self.logger.error(f"Unknown command: {parsed_args.command}")
            return 1

        try:
            return command.execute(parsed_args)
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user")
            return 130
        except Exception as e:
            self.logger.error(f"Command failed: {e}")
            if parsed_args.verbose >= 2:
                import traceback
                traceback.print_exc()
            return 1

    def print_banner(self) -> None:
        """Print the mlpy banner."""
        banner = """
╭─────────────────────────────────────────────╮
│                                             │
│  ███╗   ███╗██╗     ██████╗ ██╗   ██╗       │
│  ████╗ ████║██║     ██╔══██╗╚██╗ ██╔╝       │
│  ██╔████╔██║██║     ██████╔╝ ╚████╔╝        │
│  ██║╚██╔╝██║██║     ██╔═══╝   ╚██╔╝         │
│  ██║ ╚═╝ ██║███████╗██║        ██║          │
│  ╚═╝     ╚═╝╚══════╝╚═╝        ╚═╝          │
│                                             │
│  Security-First ML Language System v2.0     │
│  Enterprise-grade transpiler with           │
│  capability-based security                  │
│                                             │
╰─────────────────────────────────────────────╯
        """
        print(banner)


def main():
    """Main entry point for the CLI."""
    app = MLCLIApp()

    # Print banner for interactive usage
    if len(sys.argv) == 1:
        app.print_banner()

    sys.exit(app.run())


if __name__ == '__main__':
    main()