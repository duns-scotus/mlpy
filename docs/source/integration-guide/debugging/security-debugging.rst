Security Debugging
==================

This chapter provides comprehensive guidance for debugging security-related issues in ML-Python integrations. Understanding security violations, capability restrictions, and audit logs is essential for maintaining secure ML application deployments.

.. contents:: Chapter Contents
   :local:
   :depth: 2

Overview
--------

Security debugging involves identifying, analyzing, and resolving security violations, capability issues, and policy enforcement problems. The mlpy security system uses a multi-layered approach:

- **Static Analysis**: Compile-time threat detection
- **Capability System**: Runtime access control
- **Sandbox Isolation**: Process-level security boundaries
- **Audit Logging**: Comprehensive security event tracking

Common Security Issues
^^^^^^^^^^^^^^^^^^^^^^

**Security Violations**:

- Unauthorized resource access attempts
- Capability token misuse
- Sandbox escape attempts
- Dangerous code pattern detection

**Capability Issues**:

- Missing capability tokens
- Insufficient permissions
- Capability inheritance problems
- Token expiration issues

**Policy Enforcement**:

- Custom security policy violations
- Resource limit breaches
- Network access control failures
- File system permission denials

Security Violation Analysis
----------------------------

Understanding Security Errors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Security violations occur when ML code attempts unauthorized operations. The security analyzer detects threats during compilation:

.. code-block:: python

   from mlpy import transpile_ml_code
   from mlpy.ml.errors import SecurityError

   def analyze_security_violation():
       """Analyze and diagnose security violations."""
       dangerous_code = """
       import os
       result = eval('os.system("ls")');
       """

       try:
           result = transpile_ml_code(dangerous_code)
       except SecurityError as e:
           # Extract violation details
           print(f"Threat Type: {e.threat_type}")
           print(f"Severity: {e.severity}")
           print(f"Location: {e.source_location}")
           print(f"Description: {e.description}")

           # Check for specific threat patterns
           if e.threat_type == "CODE_INJECTION":
               print("⚠️ Code injection attempt detected")
               print(f"Pattern: {e.pattern_matched}")
           elif e.threat_type == "DANGEROUS_IMPORT":
               print("⚠️ Dangerous module import blocked")
               print(f"Module: {e.module_name}")

**Output**:

.. code-block:: text

   Threat Type: CODE_INJECTION
   Severity: HIGH
   Location: line 3, column 15
   Description: Use of eval() function enables arbitrary code execution
   ⚠️ Code injection attempt detected
   Pattern: eval\s*\([^)]*\)

Static Analysis Violations
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The security analyzer performs multi-pass threat detection:

.. code-block:: python

   from mlpy.ml.analysis import SecurityAnalyzer
   from mlpy.ml.parser import parse_ml_code

   def detailed_security_analysis(ml_code):
       """Perform detailed security analysis with full reporting."""
       # Parse ML code
       ast = parse_ml_code(ml_code)

       # Create security analyzer
       analyzer = SecurityAnalyzer()

       # Run analysis
       result = analyzer.analyze(ast)

       # Examine violations
       for violation in result.violations:
           print(f"\n{'='*60}")
           print(f"Violation: {violation.violation_type}")
           print(f"Severity: {violation.severity}")
           print(f"Line: {violation.line_number}")
           print(f"Code: {violation.code_snippet}")
           print(f"Reason: {violation.reason}")

           # Show remediation
           if violation.suggested_fix:
               print(f"\nSuggested Fix:")
               print(f"  {violation.suggested_fix}")

           # Show related CWE
           if violation.cwe_id:
               print(f"\nRelated CWE: CWE-{violation.cwe_id}")
               print(f"  {violation.cwe_description}")

**Example Analysis**:

.. code-block:: python

   malicious_code = """
   // Attempt SQL injection
   import sqlite3

   function getUserData(userId) {
       let query = "SELECT * FROM users WHERE id = " + userId;
       return database.execute(query);
   }
   """

   detailed_security_analysis(malicious_code)

**Output**:

.. code-block:: text

   ============================================================
   Violation: SQL_INJECTION
   Severity: HIGH
   Line: 6
   Code: let query = "SELECT * FROM users WHERE id = " + userId;
   Reason: SQL query constructed using string concatenation with user input

   Suggested Fix:
     Use parameterized queries: "SELECT * FROM users WHERE id = ?", [userId]

   Related CWE: CWE-89
     Improper Neutralization of Special Elements used in an SQL Command

Data Flow Tracking
^^^^^^^^^^^^^^^^^^

The security analyzer tracks data flow from untrusted sources:

.. code-block:: python

   from mlpy.ml.analysis import DataFlowTracker

   def analyze_taint_propagation(ml_code):
       """Track tainted data through the program."""
       # Parse and analyze
       ast = parse_ml_code(ml_code)
       tracker = DataFlowTracker()

       # Identify taint sources
       sources = tracker.find_taint_sources(ast)
       print(f"Found {len(sources)} taint sources:")
       for source in sources:
           print(f"  - {source.name} (type: {source.source_type})")

       # Track propagation
       propagation = tracker.track_propagation(ast)

       # Find dangerous sinks
       dangerous_sinks = [
           sink for sink in propagation.sinks
           if sink.is_dangerous and sink.is_tainted
       ]

       if dangerous_sinks:
           print(f"\n⚠️ Found {len(dangerous_sinks)} dangerous tainted sinks:")
           for sink in dangerous_sinks:
               print(f"\nSink: {sink.function_name}")
               print(f"  Location: line {sink.line_number}")
               print(f"  Taint source: {sink.taint_source}")
               print(f"  Data flow path:")
               for step in sink.flow_path:
                   print(f"    → {step}")

**Example**:

.. code-block:: ml

   // Tainted data flow example
   import http
   import database

   function processRequest(request) {
       let userId = request.getParameter("user_id");  // Taint source
       let userName = getUserName(userId);             // Propagation
       let query = "DELETE FROM users WHERE name = " + userName;  // Dangerous sink
       return database.execute(query);
   }

**Analysis Output**:

.. code-block:: text

   Found 1 taint sources:
     - userId (type: HTTP_PARAMETER)

   ⚠️ Found 1 dangerous tainted sinks:

   Sink: database.execute
     Location: line 7
     Taint source: userId (HTTP_PARAMETER)
     Data flow path:
       → userId = request.getParameter("user_id")
       → userName = getUserName(userId)
       → query = "DELETE FROM users WHERE name = " + userName
       → database.execute(query)

Capability Debugging
--------------------

Understanding Capability Tokens
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Capability tokens provide fine-grained access control. Debugging capability issues requires understanding token structure and validation:

.. code-block:: python

   from mlpy.runtime.capabilities import CapabilityToken, CapabilityManager

   def debug_capability_token(token):
       """Debug capability token issues."""
       print(f"Token ID: {token.token_id}")
       print(f"Resource Pattern: {token.resource_pattern}")
       print(f"Permissions: {', '.join(token.permissions)}")
       print(f"Expires: {token.expiration_time}")
       print(f"Revoked: {token.is_revoked}")

       # Validate token
       if token.is_expired():
           print("❌ Token has expired")
           print(f"   Expired at: {token.expiration_time}")

       if token.is_revoked:
           print("❌ Token has been revoked")
           print(f"   Revocation reason: {token.revocation_reason}")

       # Check resource access
       test_resources = [
           "/data/users.db",
           "/config/settings.json",
           "/tmp/cache.tmp"
       ]

       print("\nResource Access Test:")
       for resource in test_resources:
           can_access = token.matches_resource(resource)
           status = "✅" if can_access else "❌"
           print(f"  {status} {resource}")

**Example Token Inspection**:

.. code-block:: python

   # Create capability manager
   manager = CapabilityManager()

   # Get token for inspection
   token = manager.get_token("file_read_token_123")

   # Debug the token
   debug_capability_token(token)

**Output**:

.. code-block:: text

   Token ID: file_read_token_123
   Resource Pattern: /data/*.db
   Permissions: read
   Expires: 2025-10-22 14:30:00
   Revoked: False

   Resource Access Test:
     ✅ /data/users.db
     ❌ /config/settings.json
     ❌ /tmp/cache.tmp

Capability Hierarchy Debugging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Capabilities can inherit from parent contexts. Debug inheritance chains:

.. code-block:: python

   from mlpy.runtime.capabilities import CapabilityContext

   def debug_capability_hierarchy(context):
       """Debug capability context hierarchy."""
       print(f"Context: {context.name}")
       print(f"Level: {context.level}")

       # Show capabilities
       print("\nDirect Capabilities:")
       for cap in context.capabilities:
           print(f"  - {cap.resource_pattern}: {', '.join(cap.permissions)}")

       # Show inherited capabilities
       if context.parent:
           print("\nInherited Capabilities:")
           inherited = context.get_inherited_capabilities()
           for cap in inherited:
               print(f"  - {cap.resource_pattern}: {', '.join(cap.permissions)}")
               print(f"    (from: {cap.context_name})")

       # Test resource access
       def test_access(resource, permission):
           can_access = context.has_permission(resource, permission)
           source = context.find_permission_source(resource, permission)
           status = "✅" if can_access else "❌"
           origin = f" (from {source})" if source else ""
           print(f"  {status} {permission} {resource}{origin}")

       print("\nAccess Tests:")
       test_access("/data/db.sqlite", "read")
       test_access("/data/db.sqlite", "write")
       test_access("/logs/app.log", "write")

**Example with Nested Contexts**:

.. code-block:: python

   # Create parent context (application level)
   app_context = CapabilityContext("application")
   app_context.add_capability(
       CapabilityToken("/data/*", ["read"])
   )

   # Create child context (request level)
   request_context = CapabilityContext("request", parent=app_context)
   request_context.add_capability(
       CapabilityToken("/tmp/*", ["read", "write"])
   )

   # Debug hierarchy
   debug_capability_hierarchy(request_context)

**Output**:

.. code-block:: text

   Context: request
   Level: 1

   Direct Capabilities:
     - /tmp/*: read, write

   Inherited Capabilities:
     - /data/*: read
       (from: application)

   Access Tests:
     ✅ read /data/db.sqlite (from application)
     ❌ write /data/db.sqlite
     ✅ write /tmp/cache.tmp (from request)

Missing Capability Diagnosis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Diagnose why capability checks fail:

.. code-block:: python

   from mlpy.runtime.capabilities import CapabilityViolation

   def diagnose_capability_violation(violation):
       """Diagnose why a capability check failed."""
       print(f"Violation Type: {violation.violation_type}")
       print(f"Resource: {violation.resource}")
       print(f"Permission: {violation.permission}")
       print(f"Context: {violation.context_name}")

       # Determine root cause
       if violation.violation_type == "NO_TOKEN":
           print("\n❌ No capability token found")
           print("Solution: Create capability token for this resource")
           print(f"  Example:")
           print(f"    token = CapabilityToken('{violation.resource}', ['{violation.permission}'])")
           print(f"    context.add_capability(token)")

       elif violation.violation_type == "INSUFFICIENT_PERMISSIONS":
           print("\n❌ Token exists but lacks required permission")
           print(f"Current permissions: {', '.join(violation.current_permissions)}")
           print(f"Required permission: {violation.permission}")
           print("Solution: Add permission to existing token or create new token")

       elif violation.violation_type == "PATTERN_MISMATCH":
           print("\n❌ Resource doesn't match any token pattern")
           print(f"Available patterns:")
           for pattern in violation.available_patterns:
               print(f"  - {pattern}")
           print("\nSolution: Update token pattern to include this resource")

       elif violation.violation_type == "EXPIRED_TOKEN":
           print("\n❌ Capability token has expired")
           print(f"Expired at: {violation.expiration_time}")
           print("Solution: Renew or create new token")

       # Show similar resources
       if violation.similar_resources:
           print("\n💡 Similar resources with access:")
           for resource in violation.similar_resources:
               print(f"  ✅ {resource}")

**Integration with Execution**:

.. code-block:: python

   from mlpy.integration import execute_ml_code_sandbox

   def execute_with_capability_debugging(ml_code, capabilities):
       """Execute ML code with detailed capability debugging."""
       try:
           result = execute_ml_code_sandbox(
               ml_code,
               capabilities=capabilities,
               debug_capabilities=True
           )
           return result

       except CapabilityViolation as e:
           print("⚠️ Capability Violation Detected\n")
           diagnose_capability_violation(e)

           # Show required capabilities
           print("\n📋 Required Capabilities:")
           for req in e.required_capabilities:
               print(f"  Resource: {req.resource}")
               print(f"  Permission: {req.permission}")
               print(f"  Context: {req.context}")
               print()

Audit Log Analysis
------------------

Security Event Logging
^^^^^^^^^^^^^^^^^^^^^^^

The mlpy security system logs all security-relevant events:

.. code-block:: python

   from mlpy.runtime.audit import AuditLogger, AuditEvent

   def setup_audit_logging():
       """Configure comprehensive audit logging."""
       logger = AuditLogger(
           log_file="/var/log/mlpy/security.log",
           log_level="INFO",
           include_stack_traces=True,
           log_successful_access=True  # Log both successes and failures
       )

       # Configure event filters
       logger.add_filter(
           event_type="CAPABILITY_CHECK",
           severity=["HIGH", "CRITICAL"]
       )

       # Add custom handler
       def security_alert_handler(event):
           if event.severity == "CRITICAL":
               send_security_alert(event)

       logger.add_handler(security_alert_handler)

       return logger

**Audit Event Structure**:

.. code-block:: python

   def examine_audit_event(event):
       """Examine structure of audit events."""
       print(f"Event ID: {event.event_id}")
       print(f"Timestamp: {event.timestamp}")
       print(f"Event Type: {event.event_type}")
       print(f"Severity: {event.severity}")
       print(f"User: {event.user_id}")
       print(f"Context: {event.context_name}")

       # Event-specific data
       if event.event_type == "CAPABILITY_VIOLATION":
           print(f"\nViolation Details:")
           print(f"  Resource: {event.data['resource']}")
           print(f"  Permission: {event.data['permission']}")
           print(f"  Reason: {event.data['reason']}")

       elif event.event_type == "SECURITY_THREAT":
           print(f"\nThreat Details:")
           print(f"  Threat Type: {event.data['threat_type']}")
           print(f"  Pattern: {event.data['pattern']}")
           print(f"  Code: {event.data['code_snippet']}")

       elif event.event_type == "SANDBOX_VIOLATION":
           print(f"\nSandbox Details:")
           print(f"  Violation: {event.data['violation_type']}")
           print(f"  Resource: {event.data['resource_usage']}")

Log Analysis Tools
^^^^^^^^^^^^^^^^^^

Analyze audit logs for security patterns:

.. code-block:: python

   from mlpy.runtime.audit import AuditLogAnalyzer
   from datetime import datetime, timedelta

   def analyze_security_logs(log_file):
       """Analyze security logs for patterns and anomalies."""
       analyzer = AuditLogAnalyzer(log_file)

       # Time range for analysis
       end_time = datetime.now()
       start_time = end_time - timedelta(hours=24)

       # Get security summary
       summary = analyzer.get_summary(start_time, end_time)

       print("Security Log Summary (Last 24 Hours)")
       print("=" * 60)
       print(f"Total Events: {summary['total_events']}")
       print(f"Critical Events: {summary['critical_events']}")
       print(f"High Severity: {summary['high_severity_events']}")
       print(f"Capability Violations: {summary['capability_violations']}")
       print(f"Security Threats: {summary['security_threats']}")
       print(f"Sandbox Violations: {summary['sandbox_violations']}")

       # Identify patterns
       print("\n\nSecurity Patterns:")
       patterns = analyzer.detect_patterns(start_time, end_time)

       for pattern in patterns:
           print(f"\n⚠️ {pattern.pattern_type}")
           print(f"   Occurrences: {pattern.count}")
           print(f"   First: {pattern.first_occurrence}")
           print(f"   Last: {pattern.last_occurrence}")

           if pattern.pattern_type == "REPEATED_CAPABILITY_VIOLATION":
               print(f"   Resource: {pattern.resource}")
               print(f"   User: {pattern.user_id}")
               print("   → Possible unauthorized access attempt")

           elif pattern.pattern_type == "MULTIPLE_THREAT_DETECTIONS":
               print(f"   Threat Type: {pattern.threat_type}")
               print(f"   Source: {pattern.source_ip}")
               print("   → Possible attack in progress")

**Anomaly Detection**:

.. code-block:: python

   def detect_security_anomalies(log_file):
       """Detect anomalous security events."""
       analyzer = AuditLogAnalyzer(log_file)

       # Baseline normal behavior
       baseline = analyzer.create_baseline(days=7)

       # Detect anomalies
       anomalies = analyzer.detect_anomalies(baseline)

       for anomaly in anomalies:
           print(f"\n🚨 Anomaly Detected: {anomaly.anomaly_type}")
           print(f"   Severity: {anomaly.severity}")
           print(f"   Timestamp: {anomaly.timestamp}")

           if anomaly.anomaly_type == "UNUSUAL_RESOURCE_ACCESS":
               print(f"   Resource: {anomaly.resource}")
               print(f"   User: {anomaly.user_id}")
               print(f"   Normal access rate: {anomaly.baseline_rate:.2f}/hour")
               print(f"   Current rate: {anomaly.current_rate:.2f}/hour")
               print(f"   Deviation: {anomaly.deviation_percent:.1f}%")

           elif anomaly.anomaly_type == "OFF_HOURS_ACTIVITY":
               print(f"   User: {anomaly.user_id}")
               print(f"   Time: {anomaly.timestamp.strftime('%H:%M')}")
               print(f"   Normal hours: {anomaly.normal_hours}")

           elif anomaly.anomaly_type == "SPIKE_IN_VIOLATIONS":
               print(f"   Violation type: {anomaly.violation_type}")
               print(f"   Count: {anomaly.count}")
               print(f"   Expected: {anomaly.expected_count}")

Query and Filter Logs
^^^^^^^^^^^^^^^^^^^^^^

Complex log queries for investigation:

.. code-block:: python

   def query_audit_logs(log_file):
       """Execute complex queries on audit logs."""
       analyzer = AuditLogAnalyzer(log_file)

       # Query 1: Find all capability violations for specific resource
       print("Query 1: Capability violations for /data/sensitive.db")
       results = analyzer.query(
           event_type="CAPABILITY_VIOLATION",
           filters={
               "resource": "/data/sensitive.db"
           },
           limit=10
       )

       for event in results:
           print(f"  {event.timestamp}: {event.user_id} - {event.data['permission']}")

       # Query 2: Find security threats by severity
       print("\n\nQuery 2: Critical security threats")
       threats = analyzer.query(
           event_type="SECURITY_THREAT",
           filters={
               "severity": "CRITICAL"
           },
           order_by="timestamp",
           order="desc"
       )

       for threat in threats:
           print(f"  {threat.timestamp}: {threat.data['threat_type']}")
           print(f"    {threat.data['description']}")

       # Query 3: Find events by user with time range
       print("\n\nQuery 3: Events for user 'admin' in last hour")
       user_events = analyzer.query(
           filters={
               "user_id": "admin",
               "timestamp_start": datetime.now() - timedelta(hours=1)
           }
       )

       for event in user_events:
           print(f"  {event.timestamp}: {event.event_type}")

       # Query 4: Correlation query - find related events
       print("\n\nQuery 4: Correlated security events")
       correlated = analyzer.find_correlated_events(
           event_id="evt_12345",
           correlation_window=timedelta(minutes=5)
       )

       print(f"Found {len(correlated)} correlated events:")
       for event in correlated:
           print(f"  {event.timestamp}: {event.event_type}")
           print(f"    Correlation score: {event.correlation_score:.2f}")

Penetration Testing
-------------------

Security Testing Framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Test ML security using systematic penetration testing:

.. code-block:: python

   from mlpy.testing.security import SecurityTester

   class MLSecurityPenetrationTest:
       """Comprehensive security penetration testing."""

       def __init__(self):
           self.tester = SecurityTester()
           self.results = []

       def test_code_injection(self):
           """Test code injection vulnerabilities."""
           print("\n[TEST] Code Injection Attacks")

           injection_payloads = [
               'result = eval("__import__(\\"os\\").system(\\"ls\\")");',
               'result = exec("import sys; sys.exit()");',
               'result = compile("malicious_code", "<string>", "exec");',
               'result = __import__("os").system("whoami");'
           ]

           for payload in injection_payloads:
               try:
                   self.tester.test_payload(payload)
                   self.results.append({
                       "test": "code_injection",
                       "payload": payload,
                       "blocked": False,
                       "severity": "CRITICAL"
                   })
                   print(f"  ❌ VULNERABILITY: Payload executed")
               except SecurityError as e:
                   self.results.append({
                       "test": "code_injection",
                       "payload": payload,
                       "blocked": True,
                       "severity": "CRITICAL"
                   })
                   print(f"  ✅ Blocked: {e.threat_type}")

       def test_capability_bypass(self):
           """Test capability system bypass attempts."""
           print("\n[TEST] Capability Bypass Attacks")

           bypass_payloads = [
               # Try to access parent context
               'result = __context__.__parent__.capabilities;',
               # Try to modify capability tokens
               'result = __capability_manager__.revoke_all();',
               # Try to access protected resources
               'result = read_file("/etc/passwd");',
               # Try reflection to access internals
               'result = __builtins__.__dict__["eval"];'
           ]

           for payload in bypass_payloads:
               try:
                   self.tester.test_payload(
                       payload,
                       capabilities=CapabilityToken("/tmp/*", ["read"])
                   )
                   self.results.append({
                       "test": "capability_bypass",
                       "payload": payload,
                       "blocked": False,
                       "severity": "HIGH"
                   })
                   print(f"  ❌ VULNERABILITY: Bypass successful")
               except (SecurityError, CapabilityViolation) as e:
                   self.results.append({
                       "test": "capability_bypass",
                       "payload": payload,
                       "blocked": True,
                       "severity": "HIGH"
                   })
                   print(f"  ✅ Blocked: {type(e).__name__}")

       def test_sandbox_escape(self):
           """Test sandbox escape attempts."""
           print("\n[TEST] Sandbox Escape Attacks")

           escape_payloads = [
               # Try to access process info
               'import os; result = os.getpid();',
               # Try to spawn subprocess
               'import subprocess; result = subprocess.run(["ls"]);',
               # Try to access file system
               'import pathlib; result = pathlib.Path("/").glob("*");',
               # Try to access network
               'import socket; result = socket.socket();'
           ]

           for payload in escape_payloads:
               try:
                   self.tester.test_payload_sandbox(payload)
                   self.results.append({
                       "test": "sandbox_escape",
                       "payload": payload,
                       "blocked": False,
                       "severity": "CRITICAL"
                   })
                   print(f"  ❌ VULNERABILITY: Escape successful")
               except (SecurityError, SandboxViolation) as e:
                   self.results.append({
                       "test": "sandbox_escape",
                       "payload": payload,
                       "blocked": True,
                       "severity": "CRITICAL"
                   })
                   print(f"  ✅ Blocked: {type(e).__name__}")

       def test_resource_exhaustion(self):
           """Test resource exhaustion (DoS) attacks."""
           print("\n[TEST] Resource Exhaustion Attacks")

           exhaustion_payloads = [
               # Infinite loop
               'while (true) { result = result + 1; }',
               # Memory exhaustion
               'let arr = []; while (true) { arr.push(new Array(1000000)); }',
               # Recursive bomb
               'function bomb() { bomb(); bomb(); } bomb();'
           ]

           for payload in exhaustion_payloads:
               try:
                   self.tester.test_payload_sandbox(
                       payload,
                       timeout=2.0,  # 2 second timeout
                       memory_limit=100 * 1024 * 1024  # 100MB
                   )
                   self.results.append({
                       "test": "resource_exhaustion",
                       "payload": payload,
                       "blocked": False,
                       "severity": "HIGH"
                   })
                   print(f"  ❌ VULNERABILITY: No limits enforced")
               except (TimeoutError, MemoryError, SandboxViolation) as e:
                   self.results.append({
                       "test": "resource_exhaustion",
                       "payload": payload,
                       "blocked": True,
                       "severity": "HIGH"
                   })
                   print(f"  ✅ Blocked: {type(e).__name__}")

       def generate_report(self):
           """Generate penetration test report."""
           print("\n" + "="*60)
           print("PENETRATION TEST REPORT")
           print("="*60)

           total_tests = len(self.results)
           blocked = sum(1 for r in self.results if r["blocked"])
           vulnerabilities = total_tests - blocked

           print(f"\nTotal Tests: {total_tests}")
           print(f"Blocked: {blocked}")
           print(f"Vulnerabilities: {vulnerabilities}")
           print(f"Security Score: {(blocked/total_tests)*100:.1f}%")

           if vulnerabilities > 0:
               print(f"\n⚠️ FOUND {vulnerabilities} VULNERABILITIES:")
               for result in self.results:
                   if not result["blocked"]:
                       print(f"\n  Severity: {result['severity']}")
                       print(f"  Test: {result['test']}")
                       print(f"  Payload: {result['payload'][:60]}...")
           else:
               print("\n✅ No vulnerabilities found - all attacks blocked")

**Run Penetration Tests**:

.. code-block:: python

   def run_security_penetration_test():
       """Execute comprehensive penetration test suite."""
       print("Starting ML Security Penetration Test")
       print("="*60)

       tester = MLSecurityPenetrationTest()

       # Run all tests
       tester.test_code_injection()
       tester.test_capability_bypass()
       tester.test_sandbox_escape()
       tester.test_resource_exhaustion()

       # Generate report
       tester.generate_report()

Automated Security Scanning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Integrate security testing into CI/CD:

.. code-block:: python

   from mlpy.testing.security import SecurityScanner

   def automated_security_scan(project_path):
       """Run automated security scan on ML project."""
       scanner = SecurityScanner(project_path)

       # Configure scan
       scanner.configure(
           scan_malicious_patterns=True,
           scan_capability_usage=True,
           scan_dependencies=True,
           fail_on_high_severity=True
       )

       # Run scan
       print("Running automated security scan...")
       results = scanner.scan()

       # Report results
       print(f"\nScan Results:")
       print(f"  Files scanned: {results.files_scanned}")
       print(f"  Issues found: {results.total_issues}")
       print(f"  Critical: {results.critical_issues}")
       print(f"  High: {results.high_issues}")
       print(f"  Medium: {results.medium_issues}")
       print(f"  Low: {results.low_issues}")

       # Detail issues
       if results.critical_issues > 0:
           print("\n⚠️ CRITICAL ISSUES:")
           for issue in results.get_issues(severity="CRITICAL"):
               print(f"\n  File: {issue.file_path}:{issue.line_number}")
               print(f"  Issue: {issue.issue_type}")
               print(f"  Description: {issue.description}")
               print(f"  Remediation: {issue.remediation}")

       # Exit with appropriate code for CI/CD
       if results.critical_issues > 0 or results.high_issues > 0:
           sys.exit(1)  # Fail CI/CD pipeline
       else:
           sys.exit(0)

Security Incident Response
---------------------------

Incident Detection
^^^^^^^^^^^^^^^^^^

Detect security incidents in real-time:

.. code-block:: python

   from mlpy.runtime.security import SecurityMonitor

   class SecurityIncidentDetector:
       """Real-time security incident detection."""

       def __init__(self):
           self.monitor = SecurityMonitor()
           self.alert_handlers = []

       def start_monitoring(self):
           """Start real-time security monitoring."""
           print("Starting security monitoring...")

           # Monitor security events
           self.monitor.on_event("SECURITY_THREAT", self.handle_threat)
           self.monitor.on_event("CAPABILITY_VIOLATION", self.handle_violation)
           self.monitor.on_event("SANDBOX_VIOLATION", self.handle_sandbox_violation)

           # Start monitoring
           self.monitor.start()

       def handle_threat(self, event):
           """Handle detected security threat."""
           severity = event.data["severity"]
           threat_type = event.data["threat_type"]

           if severity in ["CRITICAL", "HIGH"]:
               incident = self.create_incident(
                   incident_type="SECURITY_THREAT",
                   severity=severity,
                   event=event
               )

               # Immediate response
               if severity == "CRITICAL":
                   self.execute_immediate_response(incident)

               # Alert team
               self.send_alert(incident)

       def handle_violation(self, event):
           """Handle capability violation."""
           resource = event.data["resource"]
           user = event.data["user_id"]

           # Check for repeated violations
           recent_violations = self.monitor.get_recent_events(
               event_type="CAPABILITY_VIOLATION",
               user_id=user,
               time_window=timedelta(minutes=5)
           )

           if len(recent_violations) >= 5:
               incident = self.create_incident(
                   incident_type="REPEATED_CAPABILITY_VIOLATION",
                   severity="HIGH",
                   event=event,
                   related_events=recent_violations
               )

               # Possible attack in progress
               self.execute_immediate_response(incident)
               self.send_alert(incident)

       def handle_sandbox_violation(self, event):
           """Handle sandbox violation."""
           violation_type = event.data["violation_type"]

           # Sandbox violations are always serious
           incident = self.create_incident(
               incident_type="SANDBOX_VIOLATION",
               severity="CRITICAL",
               event=event
           )

           # Immediate response required
           self.execute_immediate_response(incident)
           self.send_alert(incident)

       def create_incident(self, incident_type, severity, event, related_events=None):
           """Create security incident record."""
           incident = {
               "incident_id": generate_incident_id(),
               "incident_type": incident_type,
               "severity": severity,
               "timestamp": datetime.now(),
               "event": event,
               "related_events": related_events or [],
               "status": "OPEN",
               "responder": None
           }

           # Log incident
           self.monitor.log_incident(incident)

           return incident

       def execute_immediate_response(self, incident):
           """Execute immediate incident response actions."""
           print(f"\n🚨 SECURITY INCIDENT: {incident['incident_type']}")
           print(f"   Severity: {incident['severity']}")
           print(f"   Incident ID: {incident['incident_id']}")

           # Automatic response actions
           if incident["severity"] == "CRITICAL":
               # Suspend user/session
               user_id = incident["event"].data.get("user_id")
               if user_id:
                   self.suspend_user(user_id)
                   print(f"   Action: Suspended user {user_id}")

               # Revoke capabilities
               context = incident["event"].data.get("context_name")
               if context:
                   self.revoke_context_capabilities(context)
                   print(f"   Action: Revoked capabilities for context {context}")

               # Isolate sandbox
               sandbox_id = incident["event"].data.get("sandbox_id")
               if sandbox_id:
                   self.terminate_sandbox(sandbox_id)
                   print(f"   Action: Terminated sandbox {sandbox_id}")

       def send_alert(self, incident):
           """Send security alert to team."""
           alert = {
               "type": "SECURITY_INCIDENT",
               "severity": incident["severity"],
               "incident_id": incident["incident_id"],
               "description": self.format_incident_description(incident),
               "timestamp": incident["timestamp"],
               "requires_response": incident["severity"] in ["CRITICAL", "HIGH"]
           }

           # Send via configured channels
           for handler in self.alert_handlers:
               handler(alert)

Incident Response Playbook
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Structured response procedures for different incident types:

.. code-block:: python

   class IncidentResponsePlaybook:
       """Structured incident response procedures."""

       def respond_to_incident(self, incident):
           """Execute appropriate response playbook."""
           incident_type = incident["incident_type"]

           playbooks = {
               "SECURITY_THREAT": self.playbook_security_threat,
               "CAPABILITY_VIOLATION": self.playbook_capability_violation,
               "SANDBOX_VIOLATION": self.playbook_sandbox_violation,
               "DATA_BREACH": self.playbook_data_breach,
               "DOS_ATTACK": self.playbook_dos_attack
           }

           playbook = playbooks.get(incident_type)
           if playbook:
               playbook(incident)
           else:
               self.playbook_generic(incident)

       def playbook_security_threat(self, incident):
           """Response playbook for security threats."""
           print("\n📋 PLAYBOOK: Security Threat Response")
           print("="*60)

           # Step 1: Containment
           print("\n[STEP 1] CONTAINMENT")
           print("  ▸ Isolating affected components...")
           self.isolate_threat_source(incident)

           # Step 2: Analysis
           print("\n[STEP 2] ANALYSIS")
           print("  ▸ Analyzing threat characteristics...")
           threat_analysis = self.analyze_threat(incident)
           print(f"    Threat type: {threat_analysis['threat_type']}")
           print(f"    Attack vector: {threat_analysis['attack_vector']}")
           print(f"    Impact scope: {threat_analysis['impact_scope']}")

           # Step 3: Eradication
           print("\n[STEP 3] ERADICATION")
           print("  ▸ Removing threat...")
           self.eradicate_threat(incident)

           # Step 4: Recovery
           print("\n[STEP 4] RECOVERY")
           print("  ▸ Restoring normal operations...")
           self.recover_from_threat(incident)

           # Step 5: Post-Incident
           print("\n[STEP 5] POST-INCIDENT")
           print("  ▸ Documenting incident...")
           self.document_incident(incident)
           print("  ▸ Updating security rules...")
           self.update_security_rules(threat_analysis)

       def playbook_capability_violation(self, incident):
           """Response playbook for capability violations."""
           print("\n📋 PLAYBOOK: Capability Violation Response")
           print("="*60)

           # Determine if legitimate or attack
           print("\n[ANALYSIS] Determining violation nature...")

           is_attack = self.is_attack_pattern(incident)

           if is_attack:
               print("  ⚠️ Attack pattern detected")
               print("\n[RESPONSE] Executing defensive measures...")
               self.block_attacker(incident)
               self.alert_security_team(incident)
           else:
               print("  ℹ️ Likely configuration issue")
               print("\n[RESPONSE] Alerting development team...")
               self.alert_dev_team(incident)
               print("  Suggested fix:")
               self.suggest_capability_fix(incident)

       def playbook_sandbox_violation(self, incident):
           """Response playbook for sandbox violations."""
           print("\n📋 PLAYBOOK: Sandbox Violation Response")
           print("="*60)

           # Immediate actions
           print("\n[IMMEDIATE] Critical security breach")
           print("  ▸ Terminating sandbox...")
           self.terminate_sandbox_immediately(incident)

           print("  ▸ Suspending user session...")
           self.suspend_session(incident)

           print("  ▸ Alerting security team...")
           self.alert_security_team(incident, priority="URGENT")

           # Forensics
           print("\n[FORENSICS] Collecting evidence...")
           self.collect_sandbox_forensics(incident)

           # Investigation
           print("\n[INVESTIGATION] Analyzing breach attempt...")
           breach_analysis = self.analyze_sandbox_breach(incident)

           print(f"  Breach type: {breach_analysis['breach_type']}")
           print(f"  Entry point: {breach_analysis['entry_point']}")
           print(f"  Affected resources: {', '.join(breach_analysis['affected_resources'])}")

Incident Documentation
^^^^^^^^^^^^^^^^^^^^^^

Document incidents for learning and compliance:

.. code-block:: python

   from mlpy.runtime.security import IncidentReport

   def document_security_incident(incident):
       """Create comprehensive incident documentation."""
       report = IncidentReport()

       # Basic information
       report.incident_id = incident["incident_id"]
       report.incident_type = incident["incident_type"]
       report.severity = incident["severity"]
       report.timestamp = incident["timestamp"]

       # Timeline
       report.add_timeline_entry(
           timestamp=incident["timestamp"],
           event="Incident detected",
           details=f"Detected {incident['incident_type']} event"
       )

       # Evidence
       report.add_evidence(
           evidence_type="AUDIT_LOG",
           description="Audit log entries related to incident",
           data=incident["event"]
       )

       if incident.get("related_events"):
           report.add_evidence(
               evidence_type="RELATED_EVENTS",
               description="Related security events",
               data=incident["related_events"]
           )

       # Analysis
       report.analysis = {
           "root_cause": "Identify root cause here",
           "attack_vector": "How the attack was attempted",
           "impact": "What systems/data were affected",
           "containment_actions": ["List of actions taken"],
           "eradication_actions": ["How threat was removed"],
           "recovery_actions": ["Steps to restore normal operations"]
       }

       # Lessons learned
       report.lessons_learned = [
           "What went well in the response",
           "What could be improved",
           "New security measures to implement"
       ]

       # Save report
       report.save(f"/var/log/mlpy/incidents/{incident['incident_id']}.json")

       print(f"\n📄 Incident report saved: {incident['incident_id']}")

Security Hardening
------------------

Defensive Security Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Configure mlpy for maximum security:

.. code-block:: python

   from mlpy.runtime.security import SecurityConfig

   def configure_maximum_security():
       """Configure mlpy with maximum security settings."""
       config = SecurityConfig()

       # Static analysis settings
       config.static_analysis.enabled = True
       config.static_analysis.strict_mode = True
       config.static_analysis.fail_on_warnings = True
       config.static_analysis.check_data_flow = True
       config.static_analysis.check_reflection = True

       # Capability system
       config.capabilities.enabled = True
       config.capabilities.require_explicit_grants = True
       config.capabilities.deny_by_default = True
       config.capabilities.audit_all_checks = True
       config.capabilities.token_expiration = 3600  # 1 hour

       # Sandbox settings
       config.sandbox.enabled = True
       config.sandbox.isolation_level = "MAXIMUM"
       config.sandbox.cpu_limit = 50  # 50% CPU
       config.sandbox.memory_limit = 256 * 1024 * 1024  # 256MB
       config.sandbox.timeout = 30  # 30 seconds
       config.sandbox.network_access = False
       config.sandbox.file_system_access = "NONE"

       # Audit logging
       config.audit.enabled = True
       config.audit.log_level = "DEBUG"
       config.audit.log_successful_access = True
       config.audit.log_capability_checks = True
       config.audit.log_sandbox_events = True
       config.audit.retention_days = 90

       # Security monitoring
       config.monitoring.enabled = True
       config.monitoring.real_time_alerts = True
       config.monitoring.anomaly_detection = True
       config.monitoring.threat_intelligence = True

       # Apply configuration
       config.apply()

       print("✅ Maximum security configuration applied")

Security Best Practices
^^^^^^^^^^^^^^^^^^^^^^^^

Implement security best practices:

.. code-block:: python

   def implement_security_best_practices():
       """Implement comprehensive security best practices."""

       # 1. Principle of Least Privilege
       print("[1] Implementing Least Privilege")

       def create_minimal_capabilities(required_resources):
           """Create minimal capability set for required resources."""
           capabilities = []

           for resource, operations in required_resources.items():
               # Only grant specific permissions needed
               token = CapabilityToken(
                   resource_pattern=resource,
                   permissions=operations,
                   expiration=timedelta(hours=1)  # Short-lived tokens
               )
               capabilities.append(token)

           return capabilities

       # Example usage
       user_capabilities = create_minimal_capabilities({
           "/data/public/*": ["read"],
           "/tmp/user_123/*": ["read", "write"]
       })

       # 2. Defense in Depth
       print("[2] Implementing Defense in Depth")

       def execute_with_defense_in_depth(ml_code, capabilities):
           """Execute ML code with multiple security layers."""
           # Layer 1: Static analysis
           threats = analyze_security(ml_code)
           if threats:
               raise SecurityError("Static analysis detected threats")

           # Layer 2: Capability enforcement
           context = CapabilityContext("execution", capabilities=capabilities)

           # Layer 3: Sandbox isolation
           result = execute_ml_code_sandbox(
               ml_code,
               capabilities=context,
               timeout=30,
               memory_limit=100 * 1024 * 1024
           )

           # Layer 4: Output validation
           validate_output(result)

           return result

       # 3. Audit Everything
       print("[3] Implementing Comprehensive Auditing")

       def execute_with_full_auditing(ml_code, user_id, request_id):
           """Execute ML code with comprehensive audit trail."""
           audit_context = {
               "user_id": user_id,
               "request_id": request_id,
               "timestamp": datetime.now(),
               "ml_code_hash": hashlib.sha256(ml_code.encode()).hexdigest()
           }

           # Log execution start
           audit_log.info("ML execution started", context=audit_context)

           try:
               result = execute_ml_code_sandbox(ml_code)
               audit_log.info("ML execution succeeded", context=audit_context)
               return result
           except Exception as e:
               audit_log.error(
                   f"ML execution failed: {e}",
                   context=audit_context,
                   exception=e
               )
               raise

       # 4. Regular Security Assessments
       print("[4] Scheduling Regular Security Assessments")

       def schedule_security_assessments():
           """Schedule regular security assessments."""
           from apscheduler.schedulers.background import BackgroundScheduler

           scheduler = BackgroundScheduler()

           # Daily security scan
           scheduler.add_job(
               run_security_scan,
               'cron',
               hour=2,  # 2 AM
               args=["/path/to/project"]
           )

           # Weekly penetration test
           scheduler.add_job(
               run_penetration_test,
               'cron',
               day_of_week='sun',
               hour=3
           )

           # Monthly security audit
           scheduler.add_job(
               run_comprehensive_security_audit,
               'cron',
               day='1',  # First day of month
               hour=4
           )

           scheduler.start()

       print("\n✅ Security best practices implemented")

Security Checklist
^^^^^^^^^^^^^^^^^^

Pre-deployment security verification:

.. code-block:: python

   def security_checklist():
       """Comprehensive security checklist for deployment."""
       checklist = {
           "Static Analysis": [
               "Security analyzer enabled and configured",
               "All threat patterns up to date",
               "Data flow tracking enabled",
               "Reflection abuse detection enabled"
           ],

           "Capability System": [
               "All resources protected by capabilities",
               "Default deny policy enabled",
               "Capability tokens have expiration",
               "Sensitive resources have strong patterns",
               "Regular capability audit performed"
           ],

           "Sandbox Security": [
               "Sandbox isolation enabled",
               "Resource limits configured",
               "Network access properly restricted",
               "File system access minimized",
               "Timeout configured appropriately"
           ],

           "Audit Logging": [
               "Audit logging enabled",
               "All security events logged",
               "Log retention policy configured",
               "Log monitoring and alerting active",
               "Logs stored securely"
           ],

           "Incident Response": [
               "Incident response plan documented",
               "Security monitoring active",
               "Alert handlers configured",
               "Response playbooks tested",
               "Security team contacts updated"
           ],

           "Code Security": [
               "All ML code reviewed for security",
               "No hardcoded credentials",
               "Input validation implemented",
               "Output sanitization implemented",
               "Error messages don't leak information"
           ],

           "Testing": [
               "Security tests passing",
               "Penetration testing completed",
               "Vulnerability scan performed",
               "No known security issues",
               "Security regression tests in CI/CD"
           ]
       }

       # Check each item
       print("Security Checklist")
       print("="*60)

       all_passed = True
       for category, items in checklist.items():
           print(f"\n{category}:")
           for item in items:
               # Actual check implementation would go here
               status = verify_checklist_item(category, item)
               symbol = "✅" if status else "❌"
               print(f"  {symbol} {item}")
               if not status:
                   all_passed = False

       print("\n" + "="*60)
       if all_passed:
           print("✅ All security checks passed - ready for deployment")
       else:
           print("❌ Security issues found - address before deployment")

       return all_passed

Summary
-------

This chapter covered comprehensive security debugging techniques for ML-Python integrations:

**Security Violation Analysis**:
- Understanding security errors and threat types
- Static analysis violations with CWE mapping
- Data flow tracking for taint propagation
- Pattern detection and remediation

**Capability Debugging**:
- Debugging capability tokens and permissions
- Understanding capability hierarchy
- Diagnosing missing capabilities
- Testing capability enforcement

**Audit Log Analysis**:
- Security event logging configuration
- Log analysis for patterns and anomalies
- Complex log queries and correlation
- Audit trail investigation

**Penetration Testing**:
- Systematic security testing framework
- Code injection, capability bypass, sandbox escape tests
- Automated security scanning
- CI/CD integration

**Security Incident Response**:
- Real-time incident detection
- Structured response playbooks
- Incident documentation and learning
- Post-incident analysis

**Security Hardening**:
- Maximum security configuration
- Defense-in-depth implementation
- Security best practices
- Pre-deployment security checklist

Key Takeaways
^^^^^^^^^^^^^

1. **Proactive Security**: Use static analysis and security testing before deployment
2. **Defense in Depth**: Multiple security layers provide better protection
3. **Comprehensive Auditing**: Log all security events for analysis and compliance
4. **Incident Preparedness**: Have response playbooks ready before incidents occur
5. **Continuous Improvement**: Learn from incidents and update security measures
6. **Regular Testing**: Perform security assessments and penetration testing regularly

Related Documentation
---------------------

- :doc:`/debugging/debugging-integration` - General debugging techniques
- :doc:`/debugging/error-analysis` - Error handling and recovery
- :doc:`/security/capability-system` - Capability system details
- :doc:`/security/sandbox` - Sandbox isolation
- :doc:`/testing/security-testing` - Security testing guide
- :doc:`/reference/security-api` - Security API reference
