# ML Language Security Audit

Comprehensive security analysis of ML language features and runtime.

Usage: /ml-compiler:security-audit [scope]

## Audit Scope:
1. **Language Features**: Security implications of all ML constructs
2. **Runtime Security**: Capability system, sandbox, safe built-ins
3. **Transpilation Security**: Code injection prevention, output validation
4. **System Integration**: CLI tools, IDE integration

## Security Analysis Process:
1. **Static Analysis**: Scan all dangerous operation patterns
2. **Dynamic Testing**: Execute exploit test suite
3. **Capability Validation**: Test capability system boundaries
4. **Sandbox Testing**: Verify process isolation + resource limits
5. **Penetration Testing**: Attempt known bypass techniques

## Exploit Prevention Testing:
- **Code Injection**: eval(), exec(), compile() bypasses
- **Reflection Abuse**: __class__, __globals__ access attempts
- **Import Bypasses**: sys.modules, importlib manipulation
- **Sandbox Escapes**: Process isolation, resource limit bypasses
- **Capability Bypasses**: Token manipulation, context pollution

## Report Generation:
- Security issue summary with CWE mappings
- Exploit test results with prevention verification
- Performance impact of security measures
- Recommendations for security hardening

Focus: Comprehensive security validation with zero tolerance for bypasses.