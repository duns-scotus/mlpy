# ML Language Extension - Installation Guide

## Quick Installation

### 1. Prerequisites
```bash
# Ensure Node.js and npm are installed
node --version  # Should be 16.x or higher
npm --version

# Ensure Python 3.12+ is installed
python --version  # Should be 3.12+
```

### 2. Build the Extension
```bash
# Navigate to the extension directory
cd ext/vscode

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Package the extension
npm run package
```

This creates `mlpy-language-support-2.0.0.vsix`

### 3. Install in VS Code

**Option A: Command Line**
```bash
code --install-extension mlpy-language-support-2.0.0.vsix
```

**Option B: VS Code UI**
1. Open VS Code
2. Open Command Palette (`Ctrl+Shift+P`)
3. Type "Extensions: Install from VSIX..."
4. Select the `.vsix` file

### 4. Verify Installation
1. Create a test file: `test.ml`
2. Add some ML code:
   ```ml
   function hello() {
       print("Hello, ML!");
   }
   ```
3. You should see:
   - ✅ Syntax highlighting
   - ✅ IntelliSense suggestions
   - ✅ ML Language Server status in status bar

### 5. Configure Language Server
The extension will automatically try to find your ML Language Server. If needed, configure:

```json
{
  "ml.languageServer.enabled": true,
  "ml.languageServer.stdio": true
}
```

## Development Installation

For development and debugging:

```bash
# Clone the repository
git clone https://github.com/your-org/mlpy.git
cd mlpy/ext/vscode

# Install dependencies
npm install

# Start development mode
npm run watch

# In VS Code: Press F5 to launch Extension Development Host
```

## Troubleshooting

### Language Server Not Found
Make sure the ML Language Server is accessible:
```bash
# From mlpy project root
python -m src.mlpy.lsp.server --help
```

### Extension Not Activating
1. Check file extension is `.ml`
2. Reload VS Code window
3. Check Extension Host output for errors

### No Syntax Highlighting
1. Verify language mode: Command Palette → "Change Language Mode" → "ML"
2. Restart Language Server: Command Palette → "ML: Restart Language Server"