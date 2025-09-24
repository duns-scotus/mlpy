# mlpy v2.0 Claude Code Commands

Custom Claude Code slash commands for accelerated mlpy v2.0 development.

## Available Commands

### 🏗️ Sprint Commands
- `/sprint-status` - Current sprint status and progress overview
- `/sprint:capabilities` - Sprint 4: Capability System ✅ **COMPLETED**
- `/sprint:sandbox` - Sprint 5: Sandbox Execution & Performance (CURRENT)
- `/sprint:foundation` - Sprint 1: Foundation & Rich Errors ✅ **COMPLETED**
- `/sprint:parser` - Sprint 2: Security-First Parser ✅ **COMPLETED**

### 🔧 ML Compiler Commands
- `/ml-compiler:transpile-test` - Comprehensive ML → Python transpilation testing
- `/ml-compiler:security-audit` - Security analysis of ML language features
- `/ml-compiler:performance-bench` - Performance benchmarking (planned)
- `/ml-compiler:debug-pipeline` - Debug transpilation pipeline (planned)

### 💻 Development Commands
- `/development:setup-env` - Complete development environment setup
- `/development:run-tests` - Test execution with coverage (planned)
- `/development:code-review` - Code review checklist (planned)

### 🔒 Security Commands
- `/security:capability-test` - Capability system testing (planned)
- `/security:sandbox-verify` - Sandbox security verification (planned)
- `/security:exploit-prevention` - Exploit prevention testing (planned)

### 📊 Quality Commands
- `/quality:sprint-health-check` - Sprint quality metrics analysis
- `/performance:benchmark-comprehensive` - Full performance analysis

## Usage Examples

### Sprint Development
```bash
# Start Sprint 4 capability system work
/sprint:capabilities

# Run comprehensive security audit
/ml-compiler:security-audit

# Check sprint quality metrics
/quality:sprint-health-check
```

### Development Workflow
```bash
# Set up development environment
/development:setup-env

# Run transpilation tests
/ml-compiler:transpile-test

# Performance benchmarking
/performance:benchmark-comprehensive
```

## Command Structure

Each command follows this structure:
- **Command File**: `.claude/commands/{category}/{command}.md`
- **Usage Pattern**: `/{category}:{command} [options]`
- **Focus**: Specific to mlpy v2.0 security-first development approach

## Sprint 4 Status: ✅ COMPLETED (September 24, 2025)

**Capability-Based Security System** - Successfully implemented:
- ✅ Zero-trust capability token system with UUID-based tokens
- ✅ Thread-safe CapabilityManager with context hierarchy
- ✅ @requires_capability decorators for function protection
- ✅ Safe built-in modules (math_safe, file_safe) with capability enforcement
- ✅ CallbackBridge for secure inter-process communication
- ✅ Complete ML language integration with capability declarations
- ✅ 15/15 core capability tests passing
- ✅ End-to-end ML→Python capability transpilation working

**Current**: Sprint 5 - Sandbox Execution & Performance Optimization

## Quality Gates

All commands support mlpy v2.0 quality standards:
- **Test Coverage**: 95%+ for core components
- **Security**: 100% dangerous operation blocking
- **Performance**: <10ms transpilation for typical programs
- **Code Quality**: Black + Ruff + MyPy strict compliance

**Ready for Sprint 5: Sandbox Execution & Performance Optimization! 🚀**