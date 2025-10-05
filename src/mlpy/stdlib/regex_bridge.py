"""Python bridge implementation for ML regex module.

Complete rewrite exposing full Python re module functionality including:
- Match objects with group access and position information
- Pattern compilation with flags (IGNORECASE, MULTILINE, DOTALL, etc.)
- Named groups and group dictionaries
- Multiple search methods (search, match, fullmatch)
- Advanced features (finditer, subn, escape)

Usage in ML:
    import regex;

    // Basic matching
    match = regex.search(r'\d+', 'The answer is 42');
    if (match != null) {
        value = match.group(0);  // "42"
        start = match.start();   // 14
    }

    // Group capturing
    pattern = regex.compile(r'(\d{3})-(\d{4})');
    match = pattern.search('Call 555-1234');
    if (match != null) {
        area = match.group(1);    // "555"
        number = match.group(2);  // "1234"
    }

    // Named groups
    pattern = regex.compile(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})');
    match = pattern.search('Date: 2025-10-05');
    if (match != null) {
        year = match.group('year');   // "2025"
        groups = match.groupDict();   // {year: "2025", month: "10", day: "05"}
    }

    // Flags
    pattern = regex.compile(r'hello', regex.IGNORECASE());
    if (pattern.search('HELLO WORLD') != null) {
        print('Match found!');
    }
"""

import re as _re
from typing import Any
from mlpy.stdlib.decorators import ml_module, ml_function, ml_class


@ml_class(description="Regular expression match result with group access and position info")
class Match:
    """Match object representing a successful regex match.

    Provides access to:
    - Matched text and captured groups
    - Named groups
    - Position information (start, end, span)
    - Match metadata
    """

    def __init__(self, match_obj: _re.Match):
        """Wrap Python Match object.

        Args:
            match_obj: Python re.Match object
        """
        self._match = match_obj

    # =====================================================================
    # Group Access
    # =====================================================================

    @ml_function(description="Get matched text or captured group")
    def group(self, group_id: int | str = 0) -> str | None:
        """Get matched text or captured group by index or name.

        Args:
            group_id: Group index (0 = full match, 1+ = captured groups) or group name

        Returns:
            Matched string or None if group didn't participate in match

        Examples:
            match.group(0)      // Full matched text
            match.group(1)      // First captured group
            match.group('name') // Named group
        """
        try:
            result = self._match.group(group_id)
            return result if result is not None else None
        except (IndexError, KeyError):
            return None

    @ml_function(description="Get all captured groups as array")
    def groups(self) -> list[str | None]:
        """Get all captured groups (excluding group 0).

        Returns:
            Array of captured groups (None for groups that didn't participate)

        Examples:
            // Pattern: r'(\d+)-(\d+)'
            // Text: '555-1234'
            groups = match.groups();  // ["555", "1234"]
        """
        return list(self._match.groups())

    @ml_function(description="Get named groups as object")
    def groupDict(self, default: Any = None) -> dict[str, str | None]:
        """Get all named groups as dictionary.

        Args:
            default: Default value for groups that didn't participate (default None)

        Returns:
            Dictionary mapping group names to matched text

        Examples:
            // Pattern: r'(?P<area>\d+)-(?P<num>\d+)'
            dict = match.groupDict();  // {area: "555", num: "1234"}
        """
        return self._match.groupdict(default)

    # =====================================================================
    # Position Information
    # =====================================================================

    @ml_function(description="Get start position of matched group")
    def start(self, group: int = 0) -> int:
        """Get start index of matched group in string.

        Args:
            group: Group index (default 0 for full match)

        Returns:
            Start position (0-based index)

        Examples:
            // Text: 'The answer is 42'
            // Pattern: r'\d+'
            start = match.start();  // 14
        """
        try:
            return self._match.start(group)
        except IndexError:
            return -1

    @ml_function(description="Get end position of matched group")
    def end(self, group: int = 0) -> int:
        """Get end index of matched group in string (exclusive).

        Args:
            group: Group index (default 0 for full match)

        Returns:
            End position (0-based index, exclusive)

        Examples:
            // Text: 'The answer is 42'
            // Pattern: r'\d+'
            end = match.end();  // 16
        """
        try:
            return self._match.end(group)
        except IndexError:
            return -1

    @ml_function(description="Get (start, end) span of matched group")
    def span(self, group: int = 0) -> list[int]:
        """Get [start, end] span of matched group.

        Args:
            group: Group index (default 0 for full match)

        Returns:
            Array [start, end] with positions

        Examples:
            span = match.span();  // [14, 16]
        """
        try:
            start, end = self._match.span(group)
            return [start, end]
        except IndexError:
            return [-1, -1]

    # =====================================================================
    # Metadata and Utilities
    # =====================================================================

    @ml_function(description="Get full matched text")
    def value(self) -> str:
        """Get full matched text (same as group(0)).

        Returns:
            Full matched string

        Examples:
            text = match.value();  // Convenience method
        """
        return self._match.group(0)

    @ml_function(description="Get last matched group name")
    def lastGroup(self) -> str | None:
        """Get name of last matched group.

        Returns:
            Name of last matched group or None

        Examples:
            // Pattern with named groups
            name = match.lastGroup();
        """
        return self._match.lastgroup

    @ml_function(description="Get number of groups in pattern")
    def groupCount(self) -> int:
        """Get total number of groups in pattern (excluding group 0).

        Returns:
            Number of captured groups

        Examples:
            // Pattern: r'(\d+)-(\d+)-(\d+)'
            count = match.groupCount();  // 3
        """
        return len(self._match.groups())

    @ml_function(description="Expand template with backreferences")
    def expand(self, template: str) -> str:
        """Expand template string with backreferences.

        Args:
            template: Template with backreferences like \\1, \\2, \\g<name>

        Returns:
            Expanded string

        Examples:
            // Pattern: r'(\w+)-(\w+)'
            // Match: 'foo-bar'
            result = match.expand(r'\\2-\\1');  // 'bar-foo'
        """
        return self._match.expand(template)

    @ml_function(description="Get string representation of match")
    def toString(self) -> str:
        """Get string representation of match.

        Returns:
            String representation

        Examples:
            str = match.toString();
        """
        return f"Match(value={repr(self.value())}, span={self.span()})"


@ml_class(description="Compiled regular expression pattern with search methods")
class Pattern:
    """Compiled regex pattern for efficient reuse.

    Provides all regex search and manipulation methods:
    - search() - Find anywhere in string
    - match() - Match from start
    - fullmatch() - Match entire string
    - findall() - Find all matches
    - finditer() - Iterate over matches
    - split() - Split by pattern
    - sub() - Replace matches
    - subn() - Replace with count
    """

    def __init__(self, pattern: str, flags: int = 0):
        """Compile regex pattern with optional flags.

        Args:
            pattern: Regular expression pattern string
            flags: Optional regex flags (use regex.IGNORECASE(), etc.)

        Raises:
            ValueError: If pattern is invalid
        """
        self.pattern = pattern
        self.flags = flags
        try:
            self._compiled = _re.compile(pattern, flags)
        except _re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

    # =====================================================================
    # Search Methods (return Match objects)
    # =====================================================================

    @ml_function(description="Search for pattern anywhere in string")
    def search(self, text: str, pos: int = 0, endpos: int | None = None) -> Match | None:
        """Search for pattern anywhere in string.

        Args:
            text: String to search
            pos: Start position (default 0)
            endpos: End position (default end of string)

        Returns:
            Match object if found, None otherwise

        Examples:
            match = pattern.search('The answer is 42');
            if (match != null) {
                value = match.group(0);
                start = match.start();
            }
        """
        if endpos is None:
            match = self._compiled.search(text, pos)
        else:
            match = self._compiled.search(text, pos, endpos)
        return Match(match) if match else None

    @ml_function(description="Match pattern from start of string")
    def match(self, text: str, pos: int = 0, endpos: int | None = None) -> Match | None:
        """Match pattern from start of string.

        Args:
            text: String to match
            pos: Start position (default 0)
            endpos: End position (default end of string)

        Returns:
            Match object if pattern matches from start, None otherwise

        Examples:
            // Only matches if pattern is at start
            match = pattern.match('42 is the answer');
        """
        if endpos is None:
            match = self._compiled.match(text, pos)
        else:
            match = self._compiled.match(text, pos, endpos)
        return Match(match) if match else None

    @ml_function(description="Match entire string against pattern")
    def fullmatch(self, text: str, pos: int = 0, endpos: int | None = None) -> Match | None:
        """Match entire string against pattern.

        Args:
            text: String to match
            pos: Start position (default 0)
            endpos: End position (default end of string)

        Returns:
            Match object if entire string matches, None otherwise

        Examples:
            // Only matches if entire string matches pattern
            match = pattern.fullmatch('42');
        """
        if endpos is None:
            match = self._compiled.fullmatch(text, pos)
        else:
            match = self._compiled.fullmatch(text, pos, endpos)
        return Match(match) if match else None

    # =====================================================================
    # Find Methods (return arrays/lists)
    # =====================================================================

    @ml_function(description="Find all non-overlapping matches")
    def findall(self, text: str, pos: int = 0, endpos: int | None = None) -> list[str]:
        """Find all non-overlapping matches as strings.

        Args:
            text: String to search
            pos: Start position (default 0)
            endpos: End position (default end of string)

        Returns:
            Array of matched strings

        Examples:
            // Pattern: r'\d+'
            // Text: 'I have 5 apples and 3 oranges'
            numbers = pattern.findall(text);  // ["5", "3"]
        """
        if endpos is None:
            return self._compiled.findall(text, pos)
        else:
            return self._compiled.findall(text, pos, endpos)

    @ml_function(description="Find all matches as Match objects")
    def finditer(self, text: str, pos: int = 0, endpos: int | None = None) -> list[Match]:
        """Find all non-overlapping matches as Match objects.

        Args:
            text: String to search
            pos: Start position (default 0)
            endpos: End position (default end of string)

        Returns:
            Array of Match objects

        Examples:
            matches = pattern.finditer('Call 555-1234 or 800-5678');
            for (match in matches) {
                area = match.group(1);
                number = match.group(2);
            }
        """
        if endpos is None:
            iterator = self._compiled.finditer(text, pos)
        else:
            iterator = self._compiled.finditer(text, pos, endpos)
        return [Match(m) for m in iterator]

    # =====================================================================
    # Manipulation Methods
    # =====================================================================

    @ml_function(description="Split string by pattern")
    def split(self, text: str, maxsplit: int = 0) -> list[str]:
        """Split string by pattern occurrences.

        Args:
            text: String to split
            maxsplit: Maximum splits (0 = unlimited)

        Returns:
            Array of split strings

        Examples:
            // Pattern: r'[,;]'
            parts = pattern.split('a,b;c,d');  // ["a", "b", "c", "d"]
        """
        return self._compiled.split(text, maxsplit)

    @ml_function(description="Replace matches with replacement")
    def sub(self, replacement: str, text: str, count: int = 0) -> str:
        """Replace pattern matches with replacement string.

        Args:
            replacement: Replacement string (can use \\1, \\2 for groups)
            text: String to process
            count: Maximum replacements (0 = all)

        Returns:
            String with replacements

        Examples:
            // Pattern: r'\d+'
            result = pattern.sub('X', 'I have 5 apples');  // 'I have X apples'

            // With backreferences
            // Pattern: r'(\w+)-(\w+)'
            result = pattern.sub(r'\\2-\\1', 'foo-bar');  // 'bar-foo'
        """
        return self._compiled.sub(replacement, text, count)

    @ml_function(description="Replace matches and return count")
    def subn(self, replacement: str, text: str, count: int = 0) -> dict:
        """Replace matches and return result with count.

        Args:
            replacement: Replacement string
            text: String to process
            count: Maximum replacements (0 = all)

        Returns:
            Object {result: string, count: number}

        Examples:
            result = pattern.subn('X', 'I have 5 apples and 3 oranges');
            // {result: "I have X apples and X oranges", count: 2}
        """
        result, n = self._compiled.subn(replacement, text, count)
        return {"result": result, "count": n}

    # =====================================================================
    # Test and Utility Methods
    # =====================================================================

    @ml_function(description="Test if pattern matches text")
    def test(self, text: str) -> bool:
        """Test if pattern matches anywhere in text.

        Args:
            text: String to test

        Returns:
            True if pattern matches, False otherwise

        Examples:
            if (pattern.test('hello world')) {
                print('Match found!');
            }
        """
        return bool(self._compiled.search(text))

    @ml_function(description="Count number of matches")
    def count(self, text: str) -> int:
        """Count number of non-overlapping matches.

        Args:
            text: String to search

        Returns:
            Number of matches

        Examples:
            // Pattern: r'\d+'
            count = pattern.count('I have 5 apples and 3 oranges');  // 2
        """
        return len(self._compiled.findall(text))

    @ml_function(description="Get pattern string")
    def getPattern(self) -> str:
        """Get pattern string.

        Returns:
            Pattern string
        """
        return self.pattern

    @ml_function(description="Get pattern flags")
    def getFlags(self) -> int:
        """Get pattern flags.

        Returns:
            Flags value
        """
        return self.flags

    @ml_function(description="Get string representation")
    def toString(self) -> str:
        """Get string representation.

        Returns:
            String representation
        """
        flag_names = []
        if self.flags & _re.IGNORECASE:
            flag_names.append("IGNORECASE")
        if self.flags & _re.MULTILINE:
            flag_names.append("MULTILINE")
        if self.flags & _re.DOTALL:
            flag_names.append("DOTALL")
        if self.flags & _re.VERBOSE:
            flag_names.append("VERBOSE")

        flags_str = f", flags={' | '.join(flag_names)}" if flag_names else ""
        return f"Pattern({repr(self.pattern)}{flags_str})"


@ml_module(
    name="regex",
    description="Regular expression pattern matching with full Python re module support",
    capabilities=["regex.compile", "regex.match"],
    version="2.0.0"
)
class Regex:
    """Regex module providing complete regular expression functionality.

    Features:
    - Match objects with group access and position information
    - Pattern compilation with flags
    - Named groups and group dictionaries
    - Multiple search methods (search, match, fullmatch)
    - Find methods (findall, finditer)
    - Text manipulation (split, sub, subn)
    - Regex flags (IGNORECASE, MULTILINE, DOTALL, VERBOSE)
    """

    # =====================================================================
    # Regex Flags
    # =====================================================================

    @ml_function(description="Case-insensitive matching flag")
    def IGNORECASE(self) -> int:
        """Get IGNORECASE flag for case-insensitive matching.

        Returns:
            IGNORECASE flag value

        Examples:
            pattern = regex.compile(r'hello', regex.IGNORECASE());
            match = pattern.search('HELLO WORLD');  // Matches!
        """
        return _re.IGNORECASE

    @ml_function(description="Multiline mode flag")
    def MULTILINE(self) -> int:
        """Get MULTILINE flag where ^ and $ match line boundaries.

        Returns:
            MULTILINE flag value

        Examples:
            // ^ and $ match start/end of each line
            pattern = regex.compile(r'^ERROR', regex.MULTILINE());
            matches = pattern.findall('INFO\\nERROR\\nWARN');
        """
        return _re.MULTILINE

    @ml_function(description="Dot matches newline flag")
    def DOTALL(self) -> int:
        """Get DOTALL flag where . matches newlines.

        Returns:
            DOTALL flag value

        Examples:
            // . matches any character including newline
            pattern = regex.compile(r'<div>.*</div>', regex.DOTALL());
        """
        return _re.DOTALL

    @ml_function(description="Verbose regex flag")
    def VERBOSE(self) -> int:
        """Get VERBOSE flag for readable regex with whitespace and comments.

        Returns:
            VERBOSE flag value

        Examples:
            pattern = regex.compile(r'''
                \\d{3}  # Area code
                -       # Separator
                \\d{4}  # Number
            ''', regex.VERBOSE());
        """
        return _re.VERBOSE

    @ml_function(description="ASCII-only matching flag")
    def ASCII(self) -> int:
        """Get ASCII flag for ASCII-only matching.

        Returns:
            ASCII flag value
        """
        return _re.ASCII

    @ml_function(description="Unicode matching flag")
    def UNICODE(self) -> int:
        """Get UNICODE flag for Unicode matching (default in Python 3).

        Returns:
            UNICODE flag value
        """
        return _re.UNICODE

    # =====================================================================
    # Pattern Compilation
    # =====================================================================

    @ml_function(description="Compile regex pattern", capabilities=["regex.compile"])
    def compile(self, pattern: str, flags: int = 0) -> Pattern:
        """Compile regex pattern with optional flags.

        Args:
            pattern: Regular expression pattern string
            flags: Optional flags (use IGNORECASE(), MULTILINE(), etc.)

        Returns:
            Compiled Pattern object

        Raises:
            ValueError: If pattern is invalid

        Examples:
            // Simple pattern
            pattern = regex.compile(r'\\d+');

            // With flags
            pattern = regex.compile(r'hello', regex.IGNORECASE());

            // Combine multiple flags with bitwise OR
            flags = regex.IGNORECASE() | regex.MULTILINE();
            pattern = regex.compile(r'^hello', flags);
        """
        return Pattern(pattern, flags)

    # =====================================================================
    # Module-Level Search Methods
    # =====================================================================

    @ml_function(description="Search for pattern in string", capabilities=["regex.match"])
    def search(self, pattern: str, text: str, flags: int = 0) -> Match | None:
        """Search for pattern anywhere in string.

        Args:
            pattern: Regular expression pattern
            text: String to search
            flags: Optional flags

        Returns:
            Match object if found, None otherwise

        Raises:
            ValueError: If pattern is invalid

        Examples:
            match = regex.search(r'\\d+', 'The answer is 42');
            if (match != null) {
                value = match.group(0);  // "42"
            }
        """
        try:
            match = _re.search(pattern, text, flags)
            return Match(match) if match else None
        except _re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

    @ml_function(description="Match pattern from start of string", capabilities=["regex.match"])
    def match(self, pattern: str, text: str, flags: int = 0) -> Match | None:
        """Match pattern from start of string.

        Args:
            pattern: Regular expression pattern
            text: String to match
            flags: Optional flags

        Returns:
            Match object if pattern matches from start, None otherwise

        Raises:
            ValueError: If pattern is invalid

        Examples:
            match = regex.match(r'\\d+', '42 is the answer');
            if (match != null) {
                value = match.group(0);  // "42"
            }
        """
        try:
            match = _re.match(pattern, text, flags)
            return Match(match) if match else None
        except _re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

    @ml_function(description="Match entire string against pattern", capabilities=["regex.match"])
    def fullmatch(self, pattern: str, text: str, flags: int = 0) -> Match | None:
        """Match entire string against pattern.

        Args:
            pattern: Regular expression pattern
            text: String to match
            flags: Optional flags

        Returns:
            Match object if entire string matches, None otherwise

        Raises:
            ValueError: If pattern is invalid

        Examples:
            match = regex.fullmatch(r'\\d+', '42');  // Matches
            match2 = regex.fullmatch(r'\\d+', '42 extra');  // null
        """
        try:
            match = _re.fullmatch(pattern, text, flags)
            return Match(match) if match else None
        except _re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

    # =====================================================================
    # Module-Level Find Methods
    # =====================================================================

    @ml_function(description="Find all non-overlapping matches", capabilities=["regex.match"])
    def findall(self, pattern: str, text: str, flags: int = 0) -> list[str]:
        """Find all non-overlapping matches.

        Args:
            pattern: Regular expression pattern
            text: String to search
            flags: Optional flags

        Returns:
            Array of matched strings

        Raises:
            ValueError: If pattern is invalid

        Examples:
            numbers = regex.findall(r'\\d+', 'I have 5 apples and 3 oranges');
            // ["5", "3"]
        """
        try:
            return _re.findall(pattern, text, flags)
        except _re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

    @ml_function(description="Find all matches as Match objects", capabilities=["regex.match"])
    def finditer(self, pattern: str, text: str, flags: int = 0) -> list[Match]:
        """Find all non-overlapping matches as Match objects.

        Args:
            pattern: Regular expression pattern
            text: String to search
            flags: Optional flags

        Returns:
            Array of Match objects

        Raises:
            ValueError: If pattern is invalid

        Examples:
            matches = regex.finditer(r'(\\d+)-(\\d+)', 'Call 555-1234 or 800-5678');
            for (match in matches) {
                area = match.group(1);
                number = match.group(2);
            }
        """
        try:
            return [Match(m) for m in _re.finditer(pattern, text, flags)]
        except _re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

    # =====================================================================
    # Module-Level Manipulation Methods
    # =====================================================================

    @ml_function(description="Split string by pattern", capabilities=["regex.match"])
    def split(self, pattern: str, text: str, maxsplit: int = 0, flags: int = 0) -> list[str]:
        """Split string by pattern occurrences.

        Args:
            pattern: Regular expression pattern
            text: String to split
            maxsplit: Maximum splits (0 = unlimited)
            flags: Optional flags

        Returns:
            Array of split strings

        Raises:
            ValueError: If pattern is invalid

        Examples:
            parts = regex.split(r'[,;]', 'a,b;c,d');  // ["a", "b", "c", "d"]
        """
        try:
            return _re.split(pattern, text, maxsplit, flags)
        except _re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

    @ml_function(description="Replace matches with replacement", capabilities=["regex.match"])
    def sub(self, pattern: str, replacement: str, text: str, count: int = 0, flags: int = 0) -> str:
        """Replace pattern matches with replacement string.

        Args:
            pattern: Regular expression pattern
            replacement: Replacement string (can use \\1, \\2 for backreferences)
            text: String to process
            count: Maximum replacements (0 = all)
            flags: Optional flags

        Returns:
            String with replacements

        Raises:
            ValueError: If pattern is invalid

        Examples:
            result = regex.sub(r'\\d+', 'X', 'I have 5 apples');
            // "I have X apples"
        """
        try:
            return _re.sub(pattern, replacement, text, count, flags)
        except _re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

    @ml_function(description="Replace matches and return count", capabilities=["regex.match"])
    def subn(self, pattern: str, replacement: str, text: str, count: int = 0, flags: int = 0) -> dict:
        """Replace matches and return result with count.

        Args:
            pattern: Regular expression pattern
            replacement: Replacement string
            text: String to process
            count: Maximum replacements (0 = all)
            flags: Optional flags

        Returns:
            Object {result: string, count: number}

        Raises:
            ValueError: If pattern is invalid

        Examples:
            result = regex.subn(r'\\d+', 'X', 'I have 5 apples and 3 oranges');
            // {result: "I have X apples and X oranges", count: 2}
        """
        try:
            result, n = _re.subn(pattern, replacement, text, count, flags)
            return {"result": result, "count": n}
        except _re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

    # =====================================================================
    # Utility Methods
    # =====================================================================

    @ml_function(description="Escape special regex characters")
    def escape(self, text: str) -> str:
        """Escape special regex characters in text.

        Args:
            text: String to escape

        Returns:
            String with special characters escaped

        Examples:
            escaped = regex.escape('Price: $5.99');
            // "Price: \\$5\\.99"
        """
        return _re.escape(text)

    @ml_function(description="Test if pattern is valid regex")
    def isValid(self, pattern: str) -> bool:
        """Check if pattern is valid regex.

        Args:
            pattern: Pattern string to validate

        Returns:
            True if valid, False otherwise

        Examples:
            if (regex.isValid(r'\\d+')) {
                print('Valid pattern');
            }
        """
        try:
            _re.compile(pattern)
            return True
        except _re.error:
            return False

    @ml_function(description="Test if pattern matches text", capabilities=["regex.match"])
    def test(self, pattern: str, text: str, flags: int = 0) -> bool:
        """Test if pattern matches anywhere in text.

        Args:
            pattern: Regular expression pattern
            text: String to test
            flags: Optional flags

        Returns:
            True if pattern matches, False otherwise

        Raises:
            ValueError: If pattern is invalid

        Examples:
            if (regex.test(r'\\d+', 'hello 42')) {
                print('Contains numbers!');
            }
        """
        try:
            return bool(_re.search(pattern, text, flags))
        except _re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

    @ml_function(description="Count number of matches", capabilities=["regex.match"])
    def count(self, pattern: str, text: str, flags: int = 0) -> int:
        """Count number of non-overlapping matches.

        Args:
            pattern: Regular expression pattern
            text: String to search
            flags: Optional flags

        Returns:
            Number of matches

        Raises:
            ValueError: If pattern is invalid

        Examples:
            count = regex.count(r'\\d+', 'I have 5 apples and 3 oranges');
            // 2
        """
        try:
            return len(_re.findall(pattern, text, flags))
        except _re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")


# Global regex instance for ML import
regex = Regex()

# Export public API
__all__ = [
    "Regex",
    "Pattern",
    "Match",
    "regex",
]
