# test-project

ML project: test-project

## Getting Started

### Prerequisites
- mlpy v2.0.0 or later

### Installation
```bash
# Clone or create the project
mlpy init test-project
cd test-project
```

### Running
```bash
# Compile and run
mlpy run src/main.ml

# Run tests
mlpy test

# Start development server
mlpy watch src/
```

### Building
```bash
# Build for production
mlpy compile src/main.ml --optimize

# Build documentation
mlpy doc build
```

## Project Structure
- `src/` - ML source files
- `tests/` - Test files
- `dist/` - Compiled output
- `docs/` - Documentation
- `examples/` - Example code

## Security

This project uses mlpy's capability-based security system.
Capabilities are configured in `mlpy.json`.

Current allowed capabilities:
- file_read
- file_write
- network

## License

MIT
