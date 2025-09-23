# Sprint 1: Foundation & Rich Errors

Setup and implementation of project foundation with Rich Error System.

Usage: /sprint:foundation [component]

## Implementation Process:
1. **Project Structure**: Create complete directory structure
2. **Virtual Environment**: Setup Python 3.12 venv + dependencies
3. **Rich Error System**: Implement ErrorContext with source lines + suggestions
4. **Profiling Foundation**: Profiling decorators for all components
5. **CLI Interface**: Basic CLI with Rich interface
6. **Quality Gates**: Pre-commit hooks, nox sessions, CI/CD basis

## Quality Validation:
- 100% test coverage for implemented components
- Rich error formatting functional
- Profiling data collection active
- All pre-commit hooks passing

## Key Components to Implement:
- `src/mlpy/ml/errors/exceptions.py` - Error hierarchy with CWE mapping
- `src/mlpy/ml/errors/context.py` - Rich error context with source lines
- `src/mlpy/runtime/profiling/decorators.py` - Performance profiling
- `src/mlpy/cli/app.py` - Basic CLI with Rich formatting

Focus: Solid foundation for subsequent sprints.