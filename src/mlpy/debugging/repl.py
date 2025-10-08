"""Interactive REPL for ML debugger.

This module provides a command-line interface for interactive debugging,
similar to Python's pdb but specialized for ML source code.
"""

import cmd
import sys
from typing import Optional

from .debugger import MLDebugger, StepMode
from .variable_formatter import VariableFormatter, format_variable_with_type


class DebuggerREPL(cmd.Cmd):
    """Interactive debugging REPL.

    Provides a command-line interface for controlling program execution,
    setting breakpoints, inspecting variables, and navigating source code.

    Example:
        >>> repl = DebuggerREPL(debugger)
        >>> debugger.on_pause = lambda: repl.cmdloop()
        >>> debugger.run()
    """

    intro = "ML Debugger v2.0 - Type 'help' or '?' for commands"
    prompt = "[mldb] "

    def __init__(self, debugger: MLDebugger):
        """Initialize REPL.

        Args:
            debugger: MLDebugger instance to control
        """
        super().__init__()
        self.debugger = debugger
        self.should_continue = False
        self.formatter = VariableFormatter()

    # === Execution Control Commands ===

    def do_continue(self, arg: str):
        """Continue execution until next breakpoint.

        Usage: continue
        Aliases: c, cont
        """
        self.debugger.continue_execution()
        self.should_continue = True
        return True  # Exit cmdloop

    do_c = do_continue
    do_cont = do_continue

    def do_next(self, arg: str):
        """Step to next ML line (step over function calls).

        Usage: next
        Aliases: n
        """
        self.debugger.step_next()
        self.should_continue = True
        return True

    do_n = do_next

    def do_step(self, arg: str):
        """Step into functions.

        Usage: step
        Aliases: s
        """
        self.debugger.step_into()
        self.should_continue = True
        return True

    do_s = do_step

    def do_return(self, arg: str):
        """Continue execution until current function returns.

        Usage: return
        Aliases: r
        """
        self.debugger.step_out()
        self.should_continue = True
        return True

    do_r = do_return

    # === Breakpoint Commands ===

    def do_break(self, arg: str):
        """Set breakpoint at ML source line.

        Usage:
            break <line>         - Set breakpoint at line in current file
            break <file>:<line>  - Set breakpoint at line in specific file

        Examples:
            break 42
            break example.ml:42

        Aliases: b
        """
        if not arg:
            print("Usage: break <line> or break <file>:<line>")
            return

        # Parse argument
        if ":" in arg:
            file_part, line_part = arg.rsplit(":", 1)
            ml_file = file_part
        else:
            ml_file = self.debugger.ml_file
            line_part = arg

        try:
            ml_line = int(line_part)
        except ValueError:
            print(f"Invalid line number: {line_part}")
            return

        # Set breakpoint (may be pending if file not loaded)
        bp_id, is_pending = self.debugger.set_breakpoint(ml_file, ml_line)

        if is_pending:
            print(f"Breakpoint {bp_id} set at {ml_file}:{ml_line} [PENDING - file not loaded yet]")
        else:
            print(f"Breakpoint {bp_id} set at {ml_file}:{ml_line}")

    do_b = do_break

    def do_condition(self, arg: str):
        """Set condition on existing breakpoint.

        Usage:
            condition <bp_id> <expression>  - Add condition to breakpoint
            condition <bp_id>                - Remove condition from breakpoint

        Examples:
            condition 1 x > 10
            condition 2 count == 5 and flag
            condition 1   # Remove condition

        Aliases: cond
        """
        if not arg:
            print("Usage: condition <breakpoint_id> [expression]")
            return

        parts = arg.split(maxsplit=1)
        try:
            bp_id = int(parts[0])
        except ValueError:
            print(f"Invalid breakpoint ID: {parts[0]}")
            return

        # Check active breakpoints
        if bp_id in self.debugger.breakpoints:
            bp = self.debugger.breakpoints[bp_id]

            if len(parts) == 1:
                # Remove condition
                bp.condition = None
                print(f"Breakpoint {bp_id} is now unconditional")
            else:
                # Set condition
                condition = parts[1]
                bp.condition = condition
                print(f"Breakpoint {bp_id} condition set to: {condition}")
            return

        # Check pending breakpoints
        if bp_id in self.debugger.pending_breakpoints:
            pending_bp = self.debugger.pending_breakpoints[bp_id]

            if len(parts) == 1:
                # Remove condition
                pending_bp.condition = None
                print(f"Pending breakpoint {bp_id} is now unconditional")
            else:
                # Set condition
                condition = parts[1]
                pending_bp.condition = condition
                print(f"Pending breakpoint {bp_id} condition set to: {condition}")
            return

        print(f"No breakpoint with ID {bp_id}")

    do_cond = do_condition

    def do_delete(self, arg: str):
        """Delete breakpoint by ID.

        Usage: delete <id>
        Aliases: d
        """
        if not arg:
            print("Usage: delete <breakpoint_id>")
            return

        try:
            bp_id = int(arg)
        except ValueError:
            print(f"Invalid breakpoint ID: {arg}")
            return

        if self.debugger.delete_breakpoint(bp_id):
            print(f"Breakpoint {bp_id} deleted")
        else:
            print(f"No breakpoint with ID {bp_id}")

    do_d = do_delete

    def do_enable(self, arg: str):
        """Enable breakpoint by ID.

        Usage: enable <id>
        """
        if not arg:
            print("Usage: enable <breakpoint_id>")
            return

        try:
            bp_id = int(arg)
        except ValueError:
            print(f"Invalid breakpoint ID: {arg}")
            return

        if self.debugger.enable_breakpoint(bp_id):
            print(f"Breakpoint {bp_id} enabled")
        else:
            print(f"No breakpoint with ID {bp_id}")

    def do_disable(self, arg: str):
        """Disable breakpoint by ID.

        Usage: disable <id>
        """
        if not arg:
            print("Usage: disable <breakpoint_id>")
            return

        try:
            bp_id = int(arg)
        except ValueError:
            print(f"Invalid breakpoint ID: {arg}")
            return

        if self.debugger.disable_breakpoint(bp_id):
            print(f"Breakpoint {bp_id} disabled")
        else:
            print(f"No breakpoint with ID {bp_id}")

    def do_loadmap(self, arg: str):
        """Load source map for ML file to enable debugging.

        Usage: loadmap <ml_file>

        This command loads the source map for an ML file, allowing you to set
        breakpoints and debug code in that file. Pending breakpoints will be
        automatically activated if the file loads successfully.

        Examples:
            loadmap utils.ml
            loadmap src/helpers.ml

        Aliases: load
        """
        if not arg:
            print("Usage: loadmap <ml_file>")
            return

        if self.debugger.load_source_map_for_file(arg):
            print(f"Source map loaded for {arg}")
        else:
            print(f"Failed to load source map for {arg}")
            print("  Make sure the .ml.map file exists alongside the .ml or .py file")

    do_load = do_loadmap

    # === Inspection Commands ===

    def do_print(self, arg: str):
        """Print variable value.

        Usage: print <variable>
        Aliases: p
        """
        if not arg:
            print("Usage: print <variable>")
            return

        value = self.debugger.get_variable(arg)

        if value is None:
            print(f"{arg} = <undefined>")
        else:
            # Use enhanced formatter
            formatted = format_variable_with_type(arg, value)
            print(formatted)

    do_p = do_print

    def do_list(self, arg: str):
        """Show source code around current position.

        Usage: list [lines]
        Aliases: l

        If lines specified, show that many lines before and after.
        Default is 2 lines before and after.
        """
        lines = 2
        if arg:
            try:
                lines = int(arg)
            except ValueError:
                print(f"Invalid line count: {arg}")
                return

        print(self.debugger.show_source_context(lines, lines))

    do_l = do_list

    def do_watch(self, arg: str):
        """Add watch expression.

        Usage: watch <expression>

        Examples:
            watch x
            watch count * 2
            watch x > 10

        Aliases: w
        """
        if not arg:
            print("Usage: watch <expression>")
            return

        watch_id = self.debugger.add_watch(arg)
        print(f"Watch {watch_id} set for expression: {arg}")

    def do_unwatch(self, arg: str):
        """Remove watch expression.

        Usage: unwatch <watch_id>

        Example:
            unwatch 1
        """
        if not arg:
            print("Usage: unwatch <watch_id>")
            return

        try:
            watch_id = int(arg)
        except ValueError:
            print(f"Invalid watch ID: {arg}")
            return

        if self.debugger.remove_watch(watch_id):
            print(f"Watch {watch_id} removed")
        else:
            print(f"No watch with ID {watch_id}")

    def do_info(self, arg: str):
        """Show debugging information.

        Usage:
            info breakpoints  - List all breakpoints
            info watches      - List all watch expressions
            info locals       - List local variables
            info globals      - List global variables
            info args         - List function arguments

        Aliases: i
        """
        if not arg:
            print("Usage: info breakpoints|watches|locals|globals|args")
            return

        cmd = arg.lower()

        if cmd.startswith("b"):  # breakpoints
            self._show_breakpoints()
        elif cmd.startswith("w"):  # watches
            self._show_watches()
        elif cmd.startswith("l"):  # locals
            self._show_locals()
        elif cmd.startswith("g"):  # globals
            self._show_globals()
        elif cmd.startswith("a"):  # args
            self._show_args()
        else:
            print(f"Unknown info command: {arg}")

    do_i = do_info

    def _show_breakpoints(self):
        """Show all breakpoints (active and pending)."""
        all_breakpoints = self.debugger.get_all_breakpoints()

        if not all_breakpoints:
            print("No breakpoints set")
            return

        print("Breakpoints:")

        # Show active breakpoints
        active_count = 0
        for bp_id, (ml_file, ml_line, status, condition, enabled) in all_breakpoints.items():
            if status == "active":
                active_count += 1
                bp = self.debugger.breakpoints[bp_id]
                enabled_str = "enabled" if enabled else "disabled"
                info = f"  {bp_id}: {ml_file}:{ml_line} [ACTIVE] ({enabled_str}, hit {bp.hit_count} times)"
                if condition:
                    info += f"\n      condition: {condition}"
                print(info)

        # Show pending breakpoints
        pending_count = 0
        for bp_id, (ml_file, ml_line, status, condition, enabled) in all_breakpoints.items():
            if status == "pending":
                pending_count += 1
                info = f"  {bp_id}: {ml_file}:{ml_line} [PENDING - file not loaded]"
                if condition:
                    info += f"\n      condition: {condition}"
                print(info)

        # Summary
        print(f"\nTotal: {active_count} active, {pending_count} pending")

    def _show_locals(self):
        """Show local variables."""
        locals_dict = self.debugger.get_all_locals()

        if not locals_dict:
            print("No local variables")
            return

        print("Local variables:")
        for name, value in locals_dict.items():
            # Use enhanced formatter with ML type names
            type_name = self.formatter.format_type(value)
            value_str = self.formatter.format_value(value, depth=0)

            # Single line or multi-line formatting
            if "\n" in value_str:
                print(f"  {name}: {type_name} =")
                # Indent multi-line values
                for line in value_str.split("\n"):
                    print(f"    {line}")
            else:
                print(f"  {name}: {type_name} = {value_str}")

    def _show_globals(self):
        """Show global variables."""
        globals_dict = self.debugger.get_all_globals()

        if not globals_dict:
            print("No global variables")
            return

        print("Global variables:")
        for name, value in globals_dict.items():
            # Use enhanced formatter with ML type names
            type_name = self.formatter.format_type(value)
            value_str = self.formatter.format_value(value, depth=0)

            # Single line or multi-line formatting
            if "\n" in value_str:
                print(f"  {name}: {type_name} =")
                # Indent multi-line values
                for line in value_str.split("\n"):
                    print(f"    {line}")
            else:
                print(f"  {name}: {type_name} = {value_str}")

    def _show_args(self):
        """Show function arguments (if in function)."""
        if not self.debugger.current_frame:
            print("Not in a function")
            return

        # Try to get function arguments from frame
        # This is a simplified version - real implementation would parse function signature
        print("Function arguments:")
        print("(Feature coming soon)")

    def _show_watches(self):
        """Show all watch expressions and their current values."""
        if not self.debugger.watches:
            print("No watches set")
            return

        print("Watch expressions:")
        watch_values = self.debugger.get_watch_values()
        for watch_id, (expression, value, success) in watch_values.items():
            if success:
                # Use enhanced formatter
                type_name = self.formatter.format_type(value)
                value_str = self.formatter.format_value(value, depth=0)

                # Single line or multi-line formatting
                if "\n" in value_str:
                    print(f"  {watch_id}: {expression}: {type_name} =")
                    # Indent multi-line values
                    for line in value_str.split("\n"):
                        print(f"      {line}")
                else:
                    print(f"  {watch_id}: {expression}: {type_name} = {value_str}")
            else:
                print(f"  {watch_id}: {expression} = {value}")

    # === Exception Breakpoints ===

    def do_catch(self, arg: str):
        """Enable breaking on exceptions.

        Usage:
            catch                  - Break on all exceptions
            catch ValueError       - Break only on ValueError
            catch off              - Disable exception breakpoints

        Aliases: except
        """
        if not arg:
            # Enable breaking on all exceptions
            self.debugger.enable_exception_breakpoints()
            print("Breaking on all exceptions enabled")
        elif arg.lower() == "off":
            # Disable exception breakpoints
            self.debugger.disable_exception_breakpoints()
            print("Exception breakpoints disabled")
        else:
            # Enable breaking on specific exception type
            exception_type = arg.strip()
            self.debugger.enable_exception_breakpoints(exception_type)
            print(f"Breaking on {exception_type} enabled")

    do_except = do_catch

    def do_exception(self, arg: str):
        """Show information about the last exception.

        Usage: exception
        Aliases: exc
        """
        exc_info = self.debugger.get_exception_info()
        if not exc_info:
            print("No exception information available")
            return

        print(f"Exception: {exc_info['type']}")
        print(f"Message: {exc_info['message']}")

    do_exc = do_exception

    # === Call Stack Navigation ===

    def do_up(self, arg: str):
        """Navigate up the call stack (towards caller).

        Usage: up [n]
            n: Number of frames to go up (default: 1)
        """
        count = 1
        if arg:
            try:
                count = int(arg)
            except ValueError:
                print(f"Invalid number: {arg}")
                return

        for _ in range(count):
            if not self.debugger.navigate_up_stack():
                print("Already at top of stack")
                break

        # Show context at new position
        self._show_stack_context()

    def do_down(self, arg: str):
        """Navigate down the call stack (towards current frame).

        Usage: down [n]
            n: Number of frames to go down (default: 1)
        """
        count = 1
        if arg:
            try:
                count = int(arg)
            except ValueError:
                print(f"Invalid number: {arg}")
                return

        for _ in range(count):
            if not self.debugger.navigate_down_stack():
                print("Already at bottom of stack")
                break

        # Show context at new position
        self._show_stack_context()

    def do_where(self, arg: str):
        """Show the call stack.

        Usage: where
        Aliases: bt, backtrace
        """
        stack = self.debugger.get_call_stack()
        if not stack:
            print("No stack information available")
            return

        print("Call stack:")
        current_index = self.debugger.current_frame_index
        for i, (ml_file, ml_line, func_name) in enumerate(stack):
            marker = ">" if i == current_index else " "
            print(f"{marker} #{i}: {func_name} at {ml_file}:{ml_line}")

    do_bt = do_where
    do_backtrace = do_where

    def _show_stack_context(self):
        """Show context information for current stack position."""
        frame = self.debugger.get_current_stack_frame()
        if not frame:
            print("No frame information")
            return

        # Get ML position for this frame
        py_file = frame.f_code.co_filename
        py_line = frame.f_lineno
        func_name = frame.f_code.co_name

        ml_pos = self.debugger.source_map_index.py_line_to_ml(py_file, py_line)
        if ml_pos:
            ml_file, ml_line, _ = ml_pos
            print(f"At {func_name} in {ml_file}:{ml_line}")
            print(f"Stack depth: {self.debugger.current_frame_index}")
        else:
            print(f"At {func_name} (Python code)")

    # === Utility Commands ===

    def do_clear(self, arg: str):
        """Clear screen.

        Usage: clear
        """
        import os

        os.system("cls" if os.name == "nt" else "clear")

    def do_quit(self, arg: str):
        """Exit debugger.

        Usage: quit
        Aliases: q, exit
        """
        print("Exiting debugger")
        self.debugger.stop()
        sys.exit(0)

    do_q = do_quit
    do_exit = do_quit

    def do_help(self, arg: str):
        """Show help for commands.

        Usage: help [command]
        """
        if not arg:
            print(
                """
Available commands:

Execution Control:
  continue (c)    - Continue execution until next breakpoint
  next (n)        - Step to next line (step over)
  step (s)        - Step into functions
  return (r)      - Continue until function returns

Breakpoints:
  break (b)       - Set breakpoint at line
  condition (cond)- Set condition on breakpoint
  delete (d)      - Delete breakpoint
  enable          - Enable breakpoint
  disable         - Disable breakpoint
  catch (except)  - Enable breaking on exceptions
  exception (exc) - Show last exception info

Inspection:
  print (p)       - Print variable value
  list (l)        - Show source code
  watch           - Add watch expression
  unwatch         - Remove watch expression
  info (i)        - Show information (breakpoints, watches, locals, globals)

Call Stack:
  where (bt)      - Show call stack with current position
  up              - Navigate up the call stack
  down            - Navigate down the call stack

Utility:
  clear           - Clear screen
  help            - Show this help
  quit (q)        - Exit debugger

Type 'help <command>' for more information about a specific command.
            """
            )
        else:
            super().do_help(arg)

    def emptyline(self):
        """Don't repeat last command on empty line."""
        pass

    def default(self, line: str):
        """Handle unknown commands."""
        print(f"Unknown command: {line}")
        print("Type 'help' for available commands")
