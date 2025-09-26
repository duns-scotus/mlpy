# ML Language Debugger/Profiler Implementation Proposal

## Executive Summary

This proposal outlines the implementation of a comprehensive debugging and profiling system for the ML language, providing IDE-integrated debugging capabilities that work seamlessly with the ML-to-Python transpilation process. The system will use the Debug Adapter Protocol (DAP) for universal IDE support and include advanced features like source mapping, variable inspection, performance profiling, and capability-aware debugging.

## Technical Challenges & Requirements

### Core Challenges
1. **Source Mapping Complexity**: ML code transpiles to Python, requiring bidirectional mapping for debugging
2. **Runtime Translation**: Python execution state must be translated back to ML language semantics
3. **Security Integration**: Debugging must respect capability-based security model
4. **Performance Impact**: Minimal overhead on transpiled code execution
5. **IDE Universality**: Support multiple IDEs through standardized protocols

### Functional Requirements
- **Breakpoint Management**: Set/remove breakpoints in ML source code
- **Step Execution**: Step over, step into, step out with ML language semantics
- **Variable Inspection**: View ML variables, objects, and arrays in their native representation
- **Call Stack Navigation**: Navigate stack frames with ML function context
- **Expression Evaluation**: Evaluate ML expressions in current debugging context
- **Performance Profiling**: Real-time performance and memory monitoring
- **Capability Monitoring**: Track capability usage during debugging

### Non-Functional Requirements
- **Performance**: <5% execution overhead when debugging enabled
- **Compatibility**: Support VSCode, PyCharm, and other DAP-compatible IDEs
- **Security**: Maintain security guarantees during debugging sessions
- **Reliability**: Robust error handling and recovery mechanisms
- **Usability**: Intuitive debugging experience matching language semantics

## System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   IDE Client    │◄──►│  DAP Server     │◄──►│ Debug Session   │
│ (VSCode/PyCharm)│    │ (Protocol Impl) │    │   Manager       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │ Source Mapping  │◄──►│ Runtime Hook    │
                       │    System       │    │   System        │
                       └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Breakpoint    │◄──►│   Variable      │
                       │    Manager      │    │   Inspector     │
                       └─────────────────┘    └─────────────────┘
```

### Component Breakdown

#### 1. Debug Adapter Protocol (DAP) Server
- **File**: `src/mlpy/debugging/dap_server.py`
- **Purpose**: Implements Microsoft's DAP for universal IDE support
- **Key Interfaces**:
  - `initialize()` - Setup debugging capabilities
  - `launch()` - Start debugging session for ML file
  - `setBreakpoints()` - Handle breakpoint requests
  - `continue()`, `next()`, `stepIn()`, `stepOut()` - Execution control
  - `stackTrace()` - Provide call stack information
  - `scopes()`, `variables()` - Variable inspection
  - `evaluate()` - Expression evaluation

#### 2. Debug Session Manager
- **File**: `src/mlpy/debugging/debug_session.py`
- **Purpose**: Manages individual debugging sessions and coordinates components
- **Key Interfaces**:
  - `start_session()` - Initialize debugging for ML program
  - `pause_execution()` - Pause at current location
  - `resume_execution()` - Continue execution
  - `terminate_session()` - Clean up and end session
  - `get_current_state()` - Retrieve execution state

#### 3. Enhanced Source Mapping System
- **File**: `src/mlpy/debugging/source_mapping.py`
- **Purpose**: Bidirectional mapping between ML and Python code locations
- **Key Interfaces**:
  - `ml_to_python_location()` - Map ML line/col to Python location
  - `python_to_ml_location()` - Map Python location back to ML
  - `get_ml_context()` - Get ML source context for Python location
  - `validate_breakpoint_location()` - Ensure breakpoint is on executable line

#### 4. Runtime Instrumentation System
- **File**: `src/mlpy/debugging/debug_instrumentation.py`
- **Purpose**: Inject debugging hooks into transpiled Python code
- **Key Features**:
  - Automatic breakpoint checking
  - Variable capture and inspection
  - Stack frame management
  - Performance data collection
  - Minimal execution overhead

#### 5. Breakpoint Manager
- **File**: `src/mlpy/debugging/breakpoint_manager.py`
- **Purpose**: Handle breakpoint lifecycle and hit detection
- **Key Interfaces**:
  - `set_breakpoint()` - Add breakpoint at ML location
  - `remove_breakpoint()` - Remove existing breakpoint
  - `evaluate_condition()` - Check conditional breakpoint
  - `should_break_here()` - Determine if execution should pause

#### 6. Variable Inspector
- **File**: `src/mlpy/debugging/variable_inspector.py`
- **Purpose**: Translate Python runtime state to ML variable representation
- **Key Features**:
  - Scope traversal (local, global, closure variables)
  - Type translation (Python objects → ML representation)
  - Complex data structure visualization
  - Capability context variables

#### 7. Stack Frame Manager
- **File**: `src/mlpy/debugging/stack_frame.py`
- **Purpose**: Manage call stack and execution context
- **Key Interfaces**:
  - `get_stack_frames()` - Retrieve current call stack
  - `get_frame_variables()` - Get variables for specific frame
  - `navigate_to_frame()` - Switch debugging context to frame
  - `evaluate_in_frame()` - Evaluate expression in frame context

#### 8. Performance Profiler Integration
- **File**: `src/mlpy/debugging/profiler.py`
- **Purpose**: Real-time performance monitoring during debugging
- **Key Features**:
  - Function execution timing
  - Memory usage tracking
  - Capability operation monitoring
  - Performance bottleneck identification

## Implementation Plan

### Phase 1: Core Infrastructure (Sprint 10.1)
**Duration**: 3-4 days
**Goal**: Establish debugging foundation

#### Files to Create:
1. `src/mlpy/debugging/__init__.py` - Module initialization
2. `src/mlpy/debugging/debug_session.py` - Session management
3. `src/mlpy/debugging/source_mapping.py` - Enhanced source mapping
4. `src/mlpy/debugging/breakpoint_manager.py` - Breakpoint handling
5. `tests/debugging/test_debug_session.py` - Core debugging tests

#### Key Tasks:
- [ ] Design debugging session lifecycle
- [ ] Implement bidirectional source mapping
- [ ] Create breakpoint management system
- [ ] Add debugging hooks to transpiler
- [ ] Establish testing framework

#### Success Criteria:
- Can set breakpoints in ML source code
- Source locations correctly map ML ↔ Python
- Basic session management works
- Tests demonstrate core functionality

### Phase 2: DAP Server Implementation (Sprint 10.2)
**Duration**: 4-5 days
**Goal**: Universal IDE protocol support

#### Files to Create:
1. `src/mlpy/debugging/dap_server.py` - DAP protocol implementation
2. `src/mlpy/debugging/dap_types.py` - DAP message types
3. `src/mlpy/debugging/dap_handlers.py` - Request handlers
4. `src/mlpy/cli/debug.py` - CLI debug command
5. `tests/debugging/test_dap_server.py` - Protocol tests

#### Key Tasks:
- [ ] Implement DAP message handling
- [ ] Create request/response processors
- [ ] Add JSON-RPC communication layer
- [ ] Integrate with debug session manager
- [ ] Add CLI debug launcher

#### Success Criteria:
- DAP server responds to standard protocol messages
- Can launch debugging session via CLI
- Basic IDE communication established
- Protocol compliance validated

### Phase 3: Runtime Integration (Sprint 10.3)
**Duration**: 4-5 days
**Goal**: Seamless Python execution debugging

#### Files to Create:
1. `src/mlpy/debugging/debug_instrumentation.py` - Code instrumentation
2. `src/mlpy/debugging/runtime_hooks.py` - Python execution hooks
3. `src/mlpy/debugging/variable_inspector.py` - Variable translation
4. `src/mlpy/debugging/stack_frame.py` - Stack management
5. `src/mlpy/codegen/debug_generator.py` - Debug-aware code generation

#### Key Tasks:
- [ ] Inject debugging hooks into generated Python
- [ ] Implement step execution control
- [ ] Create variable inspection system
- [ ] Handle stack frame navigation
- [ ] Optimize performance impact

#### Success Criteria:
- Can step through ML code execution
- Variables display in ML representation
- Call stack shows ML function context
- <5% performance overhead

### Phase 4: IDE Extensions (Sprint 10.4)
**Duration**: 3-4 days
**Goal**: Native IDE debugging experience

#### Files to Create:
1. `tools/vscode-extension/src/debug.ts` - VSCode debug adapter
2. `tools/vscode-extension/package.json` - Extension manifest (update)
3. `tools/intellij-plugin/src/debug/MLDebugRunner.kt` - PyCharm integration
4. `tools/vscode-extension/debug-config-schema.json` - Debug configuration
5. `docs/source/debugging/ide-setup.rst` - Setup documentation

#### Key Tasks:
- [ ] Create VSCode debug extension
- [ ] Implement PyCharm debug configuration
- [ ] Add debug launch configurations
- [ ] Create debugging documentation
- [ ] Test IDE integration workflows

#### Success Criteria:
- One-click debugging from VSCode
- PyCharm debug configuration works
- Debugging documentation complete
- Smooth IDE user experience

### Phase 5: Advanced Features (Sprint 10.5)
**Duration**: 3-4 days
**Goal**: Production-ready debugging capabilities

#### Files to Create:
1. `src/mlpy/debugging/profiler.py` - Performance profiling
2. `src/mlpy/debugging/expression_evaluator.py` - Expression evaluation
3. `src/mlpy/debugging/debug_console.py` - Interactive console
4. `src/mlpy/debugging/capability_monitor.py` - Security monitoring
5. `tests/debugging/test_advanced_features.py` - Advanced feature tests

#### Key Tasks:
- [ ] Implement real-time profiling
- [ ] Add expression evaluation in debug context
- [ ] Create debug console/REPL
- [ ] Monitor capability usage during debug
- [ ] Add conditional breakpoints

#### Success Criteria:
- Real-time performance monitoring works
- Can evaluate ML expressions during debugging
- Capability usage visible during debug
- Advanced breakpoint features functional

## Technical Specifications

### Debug Adapter Protocol Integration

#### Launch Configuration
```json
{
  "type": "ml-debug",
  "request": "launch",
  "name": "Debug ML Program",
  "program": "${workspaceFolder}/main.ml",
  "stopOnEntry": false,
  "capabilities": ["file:read:source", "math:*"],
  "sandbox": {
    "enabled": true,
    "maxMemoryMB": 100,
    "maxCpuTimeSeconds": 30
  },
  "profiling": {
    "enabled": true,
    "memoryTracking": true,
    "performanceAnalysis": true
  }
}
```

#### DAP Message Flow
1. **Initialize** → Setup debugging capabilities
2. **Launch** → Start ML program with debugging
3. **SetBreakpoints** → Configure breakpoints in ML source
4. **Continue** → Resume execution until breakpoint hit
5. **StackTrace** → Get current call stack
6. **Scopes** → Get variable scopes for current frame
7. **Variables** → Get variables in specific scope
8. **Evaluate** → Evaluate ML expression in current context

### Source Mapping Enhancement

#### Enhanced Source Map Format
```json
{
  "version": 3,
  "sources": ["main.ml"],
  "mappings": "...",  // Base64 VLQ mappings
  "names": [...],
  "debugInfo": {
    "breakpointLines": [1, 5, 10, 15],  // Valid breakpoint locations
    "functionRanges": [
      {
        "mlFunction": "calculateDistance",
        "mlStartLine": 5,
        "mlEndLine": 12,
        "pythonStartLine": 15,
        "pythonEndLine": 28
      }
    ],
    "variableMappings": [
      {
        "mlName": "userInput",
        "pythonName": "_ml_var_userInput",
        "scope": "local"
      }
    ]
  }
}
```

### Runtime Instrumentation Strategy

#### Debug Hook Injection
The transpiler will inject debugging hooks into generated Python code:

```python
# Generated Python with debug hooks
def _ml_function_calculateDistance(_ml_var_x, _ml_var_y):
    __debug_hook__.enter_function("calculateDistance", 5, locals())

    # Original function logic with line hooks
    __debug_hook__.line_executed(6, locals())
    _ml_var_result = _ml_var_x ** 2 + _ml_var_y ** 2

    __debug_hook__.line_executed(7, locals())
    _ml_var_sqrt_result = _ml_var_result ** 0.5

    __debug_hook__.exit_function("calculateDistance", _ml_var_sqrt_result)
    return _ml_var_sqrt_result
```

### Variable Translation System

#### ML ↔ Python Variable Mapping
- **ML Objects** → Python dictionaries with metadata
- **ML Arrays** → Python lists with type preservation
- **ML Functions** → Python functions with signature info
- **Capability Context** → Special debug variables showing active capabilities

### Performance Considerations

#### Optimization Strategies
1. **Conditional Compilation**: Debug hooks only when debugging enabled
2. **Lazy Evaluation**: Variable inspection only on demand
3. **Efficient Mapping**: Cache source mapping lookups
4. **Minimal Overhead**: <5% performance impact target
5. **Memory Management**: Proper cleanup of debug resources

## Security Considerations

### Capability-Aware Debugging
- Debugging sessions inherit capability context from debugged program
- Cannot access resources beyond program's capabilities
- Debug operations logged for security audit
- Capability usage visible during debugging

### Secure Debug Protocol
- DAP communication can be secured with authentication
- Debug access requires appropriate development capabilities
- No information leakage through debug interface
- Sandbox restrictions apply to debugging operations

## Testing Strategy

### Unit Testing
- Each component thoroughly unit tested
- Mock-based testing for external dependencies
- Protocol compliance testing for DAP
- Performance regression testing

### Integration Testing
- End-to-end debugging workflows
- IDE integration testing (automated where possible)
- Complex ML program debugging validation
- Security boundary testing

### Manual Testing
- Real IDE debugging experience validation
- User workflow testing
- Performance impact measurement
- Documentation accuracy verification

## Documentation Plan

### User Documentation
- **Debug Setup Guide**: How to configure debugging in IDEs
- **Debug Features Guide**: Using breakpoints, stepping, inspection
- **Profiling Guide**: Performance monitoring during development
- **Troubleshooting Guide**: Common issues and solutions

### Developer Documentation
- **Debug Architecture**: System design and component interaction
- **DAP Implementation**: Protocol details and extensions
- **Extension Development**: Creating new IDE integrations
- **Advanced Features**: Profiling, expressions, custom tools

## Risk Assessment & Mitigation

### Technical Risks
1. **Performance Impact**: Mitigation through conditional compilation and optimization
2. **IDE Compatibility**: Use standard DAP protocol for universal support
3. **Source Mapping Accuracy**: Extensive testing with complex ML programs
4. **Security Boundaries**: Careful capability integration and access control

### Development Risks
1. **Complexity Underestimation**: Phased approach with clear milestones
2. **IDE-Specific Issues**: Early testing with multiple IDEs
3. **User Experience Problems**: Regular usability testing and feedback
4. **Maintenance Overhead**: Well-documented architecture and automated tests

## Success Metrics

### Functional Metrics
- [ ] Can debug ML programs in VSCode and PyCharm
- [ ] Breakpoints work correctly in ML source code
- [ ] Variable inspection shows ML-native representation
- [ ] Step execution respects ML language semantics
- [ ] Performance profiling provides actionable insights

### Quality Metrics
- [ ] <5% execution overhead when debugging enabled
- [ ] >95% test coverage for debugging components
- [ ] Documentation covers all debugging features
- [ ] User feedback indicates positive debugging experience
- [ ] Security analysis shows no capability leakage

### Adoption Metrics
- [ ] IDE extensions available in official marketplaces
- [ ] Documentation enables self-service debugging setup
- [ ] Advanced features (profiling, expression evaluation) functional
- [ ] Integration with existing mlpy development workflow

## Conclusion

This proposal outlines a comprehensive debugging and profiling system for the ML language that will provide a native, IDE-integrated debugging experience. The phased implementation approach ensures steady progress while maintaining quality and security standards. The use of standard protocols (DAP) ensures broad IDE compatibility, while the focus on ML language semantics provides an intuitive debugging experience for developers.

The proposed system will significantly enhance the developer experience for mlpy, making it a production-ready language for complex software development with enterprise-grade debugging capabilities.