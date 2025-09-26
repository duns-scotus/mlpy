"""Advanced pattern detection engine for security analysis."""

import ast
import re
from dataclasses import dataclass, field
from enum import Enum
from re import Pattern
from typing import Any

# Import from the correct location
try:
    from ..errors import SecurityError, SecurityWarning
except ImportError:
    # Fallback for missing SecurityError/SecurityWarning classes
    from ..errors.exceptions import MLSecurityError as SecurityError

    SecurityWarning = SecurityError


class ThreatLevel(Enum):
    """Threat severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class SecurityPattern:
    """Security pattern definition."""

    name: str
    pattern: str | Pattern[str]
    threat_level: ThreatLevel
    description: str
    cwe_id: str | None = None
    mitigation: str | None = None
    examples: list[str] = field(default_factory=list)
    ast_node_types: set[type] = field(default_factory=set)


@dataclass
class PatternMatch:
    """Result of pattern matching."""

    pattern: SecurityPattern
    location: dict[str, Any]
    context: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


class AdvancedPatternDetector:
    """Advanced pattern detection engine for security analysis."""

    def __init__(self):
        """Initialize the pattern detector."""
        self.patterns: list[SecurityPattern] = []
        self.compiled_regex: dict[str, Pattern[str]] = {}
        self._initialize_patterns()

    def _initialize_patterns(self) -> None:
        """Initialize comprehensive security patterns."""
        # Code injection patterns
        self.add_pattern(
            SecurityPattern(
                name="dynamic_code_execution",
                pattern=r"\b(eval|exec|compile)\s*\(",
                threat_level=ThreatLevel.CRITICAL,
                description="Dynamic code execution detected",
                cwe_id="CWE-94",
                mitigation="Use safe alternatives or sandboxed execution",
                examples=["eval(user_input)", "exec(dynamic_code)"],
                ast_node_types={ast.Call},
            )
        )

        self.add_pattern(
            SecurityPattern(
                name="dangerous_imports",
                pattern=r"__import__\s*\(|importlib\.import_module\s*\(|from\s+__builtin__|from\s+__builtins__|import\s+__builtin__|import\s+__builtins__",
                threat_level=ThreatLevel.HIGH,
                description="Dynamic or builtin module import detected",
                cwe_id="CWE-94",
                mitigation="Use static imports or capability-controlled dynamic imports",
                examples=[
                    "__import__('os')",
                    "importlib.import_module(module_name)",
                    "from __builtin__ import eval",
                    "import __builtins__",
                ],
                ast_node_types={ast.Call, ast.Import, ast.ImportFrom},
            )
        )

        # Basic reflection and introspection patterns
        self.add_pattern(
            SecurityPattern(
                name="dangerous_reflection",
                pattern=r"\b(getattr|setattr|delattr|hasattr)\s*\(.*,.*\)|vars\s*\(|globals\s*\(|locals\s*\(",
                threat_level=ThreatLevel.HIGH,
                description="Dangerous reflection operations detected",
                cwe_id="CWE-470",
                mitigation="Use explicit attribute access or capability tokens",
                examples=["getattr(obj, attr_name)", "vars()", "globals()"],
                ast_node_types={ast.Call},
            )
        )

        # Advanced reflection patterns - Class hierarchy traversal
        self.add_pattern(
            SecurityPattern(
                name="class_hierarchy_access",
                pattern=r"__class__\.__bases__|\.__mro__|\.__subclasses__\s*\(",
                threat_level=ThreatLevel.CRITICAL,
                description="Class hierarchy traversal detected - potential security bypass",
                cwe_id="CWE-470",
                mitigation="Block access to class hierarchy introspection",
                examples=[
                    "obj.__class__.__bases__[0]",
                    "type(obj).__mro__",
                    "object.__subclasses__()",
                ],
                ast_node_types={ast.Attribute, ast.Call},
            )
        )

        # Advanced reflection patterns - Direct attribute dictionary access
        self.add_pattern(
            SecurityPattern(
                name="attribute_dict_access",
                pattern=r"__dict__\s*\[|__dict__\s*\.|\.get\s*\(\s*['\"]__",
                threat_level=ThreatLevel.CRITICAL,
                description="Direct attribute dictionary access detected",
                cwe_id="CWE-470",
                mitigation="Use controlled attribute access mechanisms",
                examples=["obj.__dict__['private']", "obj.__dict__.get('secret')"],
                ast_node_types={ast.Subscript, ast.Attribute},
            )
        )

        # Advanced reflection patterns - Serialization method abuse
        self.add_pattern(
            SecurityPattern(
                name="serialization_method_abuse",
                pattern=r"__reduce__\s*\(|__reduce_ex__\s*\(|__getstate__\s*\(|__setstate__\s*\(",
                threat_level=ThreatLevel.HIGH,
                description="Serialization method abuse detected",
                cwe_id="CWE-502",
                mitigation="Block access to serialization internals",
                examples=["obj.__reduce__()", "obj.__getstate__()"],
                ast_node_types={ast.Call, ast.Attribute},
            )
        )

        # Advanced reflection patterns - Attribute access bypass
        self.add_pattern(
            SecurityPattern(
                name="attribute_access_bypass",
                pattern=r"__getattribute__\s*\(|__getattr__\s*\(|__setattr__\s*\(",
                threat_level=ThreatLevel.HIGH,
                description="Attribute access bypass methods detected",
                cwe_id="CWE-470",
                mitigation="Use standard attribute access patterns",
                examples=["obj.__getattribute__('private')", "obj.__getattr__('hidden')"],
                ast_node_types={ast.Call},
            )
        )

        # Advanced reflection patterns - Method resolution and inspection
        self.add_pattern(
            SecurityPattern(
                name="method_inspection",
                pattern=r"__code__|__func__|__closure__|__globals__|im_func|im_class",
                threat_level=ThreatLevel.HIGH,
                description="Method introspection detected",
                cwe_id="CWE-470",
                mitigation="Avoid accessing method internals",
                examples=["func.__code__", "method.__globals__", "func.im_func"],
                ast_node_types={ast.Attribute},
            )
        )

        # Advanced reflection patterns - Dynamic execution contexts
        self.add_pattern(
            SecurityPattern(
                name="execution_context_manipulation",
                pattern=r"__import__\s*\(\s*['\"]__builtin__|__builtins__\s*\[|frame\.f_",
                threat_level=ThreatLevel.CRITICAL,
                description="Execution context manipulation detected",
                cwe_id="CWE-94",
                mitigation="Block access to execution context internals",
                examples=["__import__('__builtin__')", "__builtins__['eval']", "frame.f_globals"],
                ast_node_types={ast.Call, ast.Subscript, ast.Attribute},
            )
        )

        # File system access patterns
        self.add_pattern(
            SecurityPattern(
                name="file_system_access",
                pattern=r"\b(open|file)\s*\(.*['\"].*['\"].*\)|pathlib\.|os\.path\.|shutil\.",
                threat_level=ThreatLevel.MEDIUM,
                description="File system access detected",
                cwe_id="CWE-22",
                mitigation="Use file capability tokens",
                examples=["open('/etc/passwd')", "os.path.join(path, file)"],
                ast_node_types={ast.Call, ast.Attribute},
            )
        )

        # Network access patterns
        self.add_pattern(
            SecurityPattern(
                name="network_access",
                pattern=r"\b(urllib|requests|socket|http)\.",
                threat_level=ThreatLevel.MEDIUM,
                description="Network access detected",
                cwe_id="CWE-918",
                mitigation="Use network capability tokens",
                examples=["requests.get(url)", "socket.socket()"],
                ast_node_types={ast.Call, ast.Attribute},
            )
        )

        # Subprocess and system access
        self.add_pattern(
            SecurityPattern(
                name="subprocess_execution",
                pattern=r"\b(subprocess|os\.system|os\.popen|os\.spawn)\.",
                threat_level=ThreatLevel.CRITICAL,
                description="Subprocess execution detected",
                cwe_id="CWE-78",
                mitigation="Use sandbox execution or capability tokens",
                examples=["subprocess.call(['rm', '-rf', '/'])", "os.system('rm -rf /')"],
                ast_node_types={ast.Call, ast.Attribute},
            )
        )

        # Serialization vulnerabilities
        self.add_pattern(
            SecurityPattern(
                name="unsafe_deserialization",
                pattern=r"\b(pickle\.loads?|marshal\.loads?|dill\.loads?)\s*\(",
                threat_level=ThreatLevel.HIGH,
                description="Unsafe deserialization detected",
                cwe_id="CWE-502",
                mitigation="Use safe serialization formats like JSON",
                examples=["pickle.loads(data)", "marshal.loads(bytecode)"],
                ast_node_types={ast.Call},
            )
        )

        # SQL injection patterns - refined to reduce false positives
        self.add_pattern(
            SecurityPattern(
                name="sql_injection_risk",
                pattern=r"(SELECT\s+.*\s+FROM|INSERT\s+INTO|UPDATE\s+.*\s+SET|DELETE\s+FROM|DROP\s+TABLE|CREATE\s+TABLE).*(\+|\%s|\.format\()",
                threat_level=ThreatLevel.HIGH,
                description="Potential SQL injection vulnerability",
                cwe_id="CWE-89",
                mitigation="Use parameterized queries",
                examples=["SELECT * FROM users WHERE id = {}".format("'user_input'")],
                ast_node_types={ast.Str, ast.JoinedStr, ast.BinOp},
            )
        )

        # Path traversal patterns
        self.add_pattern(
            SecurityPattern(
                name="path_traversal",
                pattern=r"\.\.\/|\.\.\\|\.\.[/\\]",
                threat_level=ThreatLevel.HIGH,
                description="Path traversal attempt detected",
                cwe_id="CWE-22",
                mitigation="Validate and sanitize file paths",
                examples=["../../../etc/passwd", "..\\windows\\system32"],
                ast_node_types={ast.Str},
            )
        )

        # Prototype pollution (JavaScript-style, relevant for dynamic languages)
        self.add_pattern(
            SecurityPattern(
                name="prototype_pollution",
                pattern=r"__proto__|constructor\.prototype",
                threat_level=ThreatLevel.MEDIUM,
                description="Potential prototype pollution pattern",
                cwe_id="CWE-1321",
                mitigation="Avoid modifying prototypes or object constructors",
                examples=["obj.__proto__.polluted = True"],
                ast_node_types={ast.Attribute},
            )
        )

        # Template injection
        self.add_pattern(
            SecurityPattern(
                name="template_injection",
                pattern=r"\{\{.*\}\}|\{%.*%\}|<%.*%>",
                threat_level=ThreatLevel.HIGH,
                description="Template injection pattern detected",
                cwe_id="CWE-94",
                mitigation="Use safe template engines with auto-escaping",
                examples=["{{user_input}}", "{%exec 'rm -rf /'%}"],
                ast_node_types={ast.Str, ast.JoinedStr},
            )
        )

        # Obfuscation detection patterns - String concatenation evasion
        self.add_pattern(
            SecurityPattern(
                name="obfuscated_builtin_construction",
                pattern=r'("__"[^"]*"built"[^"]*"in"[^"]*"__")|("built"[^"]*"in")|("__built")',
                threat_level=ThreatLevel.CRITICAL,
                description="Obfuscated __builtin__ construction detected",
                cwe_id="CWE-94",
                mitigation="Block string concatenation patterns building dangerous identifiers",
                examples=['"__" + "built" + "in" + "__"', '"__built" + "in__"'],
                ast_node_types={ast.Str, ast.BinOp},
            )
        )

        self.add_pattern(
            SecurityPattern(
                name="obfuscated_class_construction",
                pattern=r'("__cla"[^"]*"ss__")|("class__")',
                threat_level=ThreatLevel.CRITICAL,
                description="Obfuscated __class__ construction detected",
                cwe_id="CWE-470",
                mitigation="Block string concatenation patterns building class access",
                examples=['"__cla" + "ss__"', '"__class" + "__"'],
                ast_node_types={ast.Str, ast.BinOp},
            )
        )

        self.add_pattern(
            SecurityPattern(
                name="obfuscated_bases_construction",
                pattern=r'("__ba"[^"]*"ses__")|("bases__")',
                threat_level=ThreatLevel.CRITICAL,
                description="Obfuscated __bases__ construction detected",
                cwe_id="CWE-470",
                mitigation="Block string concatenation patterns building bases access",
                examples=['"__ba" + "ses__"', '"__bases" + "__"'],
                ast_node_types={ast.Str, ast.BinOp},
            )
        )

        self.add_pattern(
            SecurityPattern(
                name="obfuscated_subclasses_construction",
                pattern=r'("__sub"[^"]*"classes__")|("subclasses__")',
                threat_level=ThreatLevel.CRITICAL,
                description="Obfuscated __subclasses__ construction detected",
                cwe_id="CWE-470",
                mitigation="Block string concatenation patterns building subclasses access",
                examples=['"__sub" + "classes__"', '"__subclasses" + "__"'],
                ast_node_types={ast.Str, ast.BinOp},
            )
        )

        self.add_pattern(
            SecurityPattern(
                name="obfuscated_import_construction",
                pattern=r'("__imp"[^"]*"ort__")|("import__")',
                threat_level=ThreatLevel.CRITICAL,
                description="Obfuscated __import__ construction detected",
                cwe_id="CWE-94",
                mitigation="Block string concatenation patterns building import access",
                examples=['"__imp" + "ort__"', '"__import" + "__"'],
                ast_node_types={ast.Str, ast.BinOp},
            )
        )

        self.add_pattern(
            SecurityPattern(
                name="obfuscated_eval_construction",
                pattern=r'("ev"[^"]*"al")|("eval")',
                threat_level=ThreatLevel.CRITICAL,
                description="Obfuscated eval construction detected",
                cwe_id="CWE-94",
                mitigation="Block string concatenation patterns building eval",
                examples=['"ev" + "al"'],
                ast_node_types={ast.Str, ast.BinOp},
            )
        )

        # Suspicious string array patterns that might construct dangerous strings
        self.add_pattern(
            SecurityPattern(
                name="suspicious_string_array_patterns",
                pattern=r'\["__"[^]]*"built"[^]]*"in"[^]]*"__"\]|\["os"[^]]*"sys"[^]]*"subprocess"\]',
                threat_level=ThreatLevel.HIGH,
                description="Suspicious string arrays that may construct dangerous identifiers",
                cwe_id="CWE-94",
                mitigation="Validate string array contents for security patterns",
                examples=['["__", "built", "in", "__"]', '["os", "sys", "subprocess"]'],
                ast_node_types={ast.List, ast.Subscript},
            )
        )

    def add_pattern(self, pattern: SecurityPattern) -> None:
        """Add a security pattern to the detector."""
        self.patterns.append(pattern)

        # Compile regex pattern for efficiency
        if isinstance(pattern.pattern, str):
            try:
                self.compiled_regex[pattern.name] = re.compile(
                    pattern.pattern, re.IGNORECASE | re.MULTILINE
                )
            except re.error:
                # Log warning but continue - invalid patterns will be skipped
                pass

    def scan_code(self, code: str, filename: str | None = None) -> list[PatternMatch]:
        """Scan code for security patterns."""
        matches = []

        # Text-based pattern matching
        for pattern in self.patterns:
            regex_pattern = self.compiled_regex.get(pattern.name)
            if regex_pattern:
                for match in regex_pattern.finditer(code):
                    location = {
                        "filename": filename,
                        "line": code[: match.start()].count("\n") + 1,
                        "column": match.start() - code.rfind("\n", 0, match.start()),
                        "start": match.start(),
                        "end": match.end(),
                    }

                    # Extract context around the match
                    lines = code.split("\n")
                    line_num = location["line"] - 1
                    context_lines = []

                    # Include surrounding lines for context
                    for i in range(max(0, line_num - 2), min(len(lines), line_num + 3)):
                        prefix = ">>> " if i == line_num else "    "
                        context_lines.append(f"{prefix}{lines[i]}")

                    context = "\n".join(context_lines)

                    # Calculate confidence based on pattern complexity and context
                    confidence = self._calculate_confidence(pattern, match, code)

                    matches.append(
                        PatternMatch(
                            pattern=pattern,
                            location=location,
                            context=context,
                            confidence=confidence,
                            metadata={
                                "matched_text": match.group(0),
                                "full_line": lines[line_num] if line_num < len(lines) else "",
                            },
                        )
                    )

        return matches

    def scan_ast(
        self, ast_tree: ast.AST, code: str = "", filename: str | None = None
    ) -> list[PatternMatch]:
        """Scan AST for security patterns."""
        matches = []

        class SecurityVisitor(ast.NodeVisitor):
            def __init__(self, detector: "AdvancedPatternDetector"):
                self.detector = detector
                self.code_lines = code.split("\n") if code else []

            def visit(self, node):
                # Check if this node type is relevant for any patterns
                for pattern in self.detector.patterns:
                    if not pattern.ast_node_types or type(node) in pattern.ast_node_types:
                        match_result = self.detector._check_ast_node(
                            node, pattern, self.code_lines, filename
                        )
                        if match_result:
                            matches.append(match_result)

                self.generic_visit(node)

        visitor = SecurityVisitor(self)
        visitor.visit(ast_tree)

        return matches

    def _check_ast_node(
        self,
        node: ast.AST,
        pattern: SecurityPattern,
        code_lines: list[str],
        filename: str | None,
    ) -> PatternMatch | None:
        """Check if AST node matches security pattern."""
        # Convert AST node to string representation for pattern matching
        try:
            node_source = ast.unparse(node) if hasattr(ast, "unparse") else str(node)
        except Exception:
            node_source = str(node)

        # Check if pattern matches the node source
        regex_pattern = self.compiled_regex.get(pattern.name)
        if regex_pattern and regex_pattern.search(node_source):
            # Get location information
            location = {
                "filename": filename,
                "line": getattr(node, "lineno", 0),
                "column": getattr(node, "col_offset", 0),
                "end_line": getattr(node, "end_lineno", 0),
                "end_column": getattr(node, "end_col_offset", 0),
            }

            # Extract context
            if code_lines and location["line"] > 0:
                line_idx = location["line"] - 1
                context_lines = []

                for i in range(max(0, line_idx - 1), min(len(code_lines), line_idx + 2)):
                    prefix = ">>> " if i == line_idx else "    "
                    context_lines.append(f"{prefix}{code_lines[i]}")

                context = "\n".join(context_lines)
            else:
                context = node_source

            # Higher confidence for AST-based matches
            confidence = min(0.9, self._calculate_base_confidence(pattern) + 0.3)

            return PatternMatch(
                pattern=pattern,
                location=location,
                context=context,
                confidence=confidence,
                metadata={"node_type": type(node).__name__, "node_source": node_source},
            )

        return None

    def _calculate_confidence(self, pattern: SecurityPattern, match: re.Match, code: str) -> float:
        """Calculate confidence score for a pattern match."""
        base_confidence = self._calculate_base_confidence(pattern)

        # Adjust based on context
        matched_text = match.group(0)

        # Higher confidence for exact function calls
        if "(" in matched_text and ")" in matched_text:
            base_confidence += 0.2

        # Lower confidence for matches in comments
        line_start = code.rfind("\n", 0, match.start())
        line_end = code.find("\n", match.end())
        line = code[line_start + 1 : line_end] if line_end != -1 else code[line_start + 1 :]

        if line.strip().startswith("#"):
            base_confidence -= 0.4

        # Higher confidence for imports at module level
        if "import" in matched_text.lower() and line_start <= 0:
            base_confidence += 0.1

        return max(0.1, min(1.0, base_confidence))

    def _calculate_base_confidence(self, pattern: SecurityPattern) -> float:
        """Calculate base confidence score for a pattern."""
        confidence_map = {
            ThreatLevel.CRITICAL: 0.8,
            ThreatLevel.HIGH: 0.7,
            ThreatLevel.MEDIUM: 0.6,
            ThreatLevel.LOW: 0.5,
            ThreatLevel.INFO: 0.3,
        }
        return confidence_map.get(pattern.threat_level, 0.5)

    def filter_matches(
        self,
        matches: list[PatternMatch],
        min_confidence: float = 0.5,
        threat_levels: set[ThreatLevel] | None = None,
    ) -> list[PatternMatch]:
        """Filter matches by confidence and threat level."""
        filtered = []

        for match in matches:
            # Filter by confidence
            if match.confidence < min_confidence:
                continue

            # Filter by threat level
            if threat_levels and match.pattern.threat_level not in threat_levels:
                continue

            filtered.append(match)

        # Sort by threat level and confidence
        threat_priority = {
            ThreatLevel.CRITICAL: 0,
            ThreatLevel.HIGH: 1,
            ThreatLevel.MEDIUM: 2,
            ThreatLevel.LOW: 3,
            ThreatLevel.INFO: 4,
        }

        filtered.sort(key=lambda m: (threat_priority[m.pattern.threat_level], -m.confidence))

        return filtered

    def get_pattern_stats(self) -> dict[str, Any]:
        """Get statistics about loaded patterns."""
        stats = {
            "total_patterns": len(self.patterns),
            "by_threat_level": {},
            "with_cwe_mapping": 0,
            "with_ast_support": 0,
        }

        for pattern in self.patterns:
            level = pattern.threat_level.value
            stats["by_threat_level"][level] = stats["by_threat_level"].get(level, 0) + 1

            if pattern.cwe_id:
                stats["with_cwe_mapping"] += 1

            if pattern.ast_node_types:
                stats["with_ast_support"] += 1

        return stats

    def create_security_report(self, matches: list[PatternMatch]) -> dict[str, Any]:
        """Create comprehensive security report from matches."""
        if not matches:
            return {
                "summary": "No security issues detected",
                "total_issues": 0,
                "by_severity": {},
                "recommendations": [],
            }

        report = {
            "total_issues": len(matches),
            "by_severity": {},
            "by_cwe": {},
            "critical_issues": [],
            "recommendations": set(),
        }

        for match in matches:
            # Count by severity
            severity = match.pattern.threat_level.value
            report["by_severity"][severity] = report["by_severity"].get(severity, 0) + 1

            # Count by CWE
            if match.pattern.cwe_id:
                cwe = match.pattern.cwe_id
                report["by_cwe"][cwe] = report["by_cwe"].get(cwe, 0) + 1

            # Track critical issues
            if match.pattern.threat_level == ThreatLevel.CRITICAL:
                report["critical_issues"].append(
                    {
                        "pattern": match.pattern.name,
                        "location": match.location,
                        "description": match.pattern.description,
                    }
                )

            # Collect recommendations
            if match.pattern.mitigation:
                report["recommendations"].add(match.pattern.mitigation)

        report["recommendations"] = list(report["recommendations"])

        # Generate summary
        critical_count = report["by_severity"].get("critical", 0)
        high_count = report["by_severity"].get("high", 0)

        if critical_count > 0:
            report["summary"] = f"CRITICAL: {critical_count} critical security issues found"
        elif high_count > 0:
            report["summary"] = f"HIGH RISK: {high_count} high-severity security issues found"
        else:
            report["summary"] = f"{len(matches)} security issues found (medium/low severity)"

        return report
