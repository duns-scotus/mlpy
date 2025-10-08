=================
IDE Integration
=================

mlpy provides comprehensive IDE integration through the Language Server Protocol (LSP), supporting popular editors and development environments.

Supported IDEs
==============

mlpy's Language Server works with any editor that supports LSP, including:

- **Visual Studio Code**
- **IntelliJ IDEA / PyCharm**
- **Vim / Neovim**
- **Emacs**
- **Sublime Text**
- **Atom**
- **Eclipse**

Features
========

The mlpy Language Server provides:

✅ **Syntax Highlighting**
   Full ML syntax highlighting with semantic tokens

✅ **IntelliSense/Completion**
   Context-aware code completion with documentation

✅ **Diagnostics**
   Real-time security analysis and error detection

✅ **Hover Information**
   Type information and documentation on hover

✅ **Go to Definition**
   Navigate to symbol definitions

✅ **Document Symbols**
   Outline view with functions, types, and variables

✅ **Code Actions**
   Security fixes and refactoring suggestions

✅ **Signature Help**
   Function parameter hints while typing

Visual Studio Code
==================

Installation
------------

1. **Install mlpy CLI:**

   .. code-block:: bash

      pip install mlpy

2. **Install VS Code Extension:**

   Search for "mlpy" in the VS Code marketplace or install manually:

   .. code-block:: bash

      code --install-extension mlpy.mlpy-vscode

3. **Verify Installation:**

   Open a ``.ml`` file and verify syntax highlighting works.

Configuration
-------------

Add to your VS Code settings (``settings.json``):

.. code-block:: json

   {
     "mlpy.languageServer.enabled": true,
     "mlpy.security.level": "strict",
     "mlpy.completion.enabled": true,
     "mlpy.diagnostics.enabled": true,
     "mlpy.formatting.enabled": true
   }

Features Demo
-------------

.. code-block:: ml

   // Hover over 'greet' to see type information
   function greet(name: string): string {
       // IntelliSense will suggest string methods
       return "Hello, " + name.toUpperCase() + "!"
   }

   // Security diagnostic will appear here
   dangerous_code = eval("1 + 1")  // ❌ Security violation

IntelliJ IDEA / PyCharm
=======================

Installation
------------

1. **Install Plugin:**

   Go to ``File → Settings → Plugins → Marketplace``
   Search for "mlpy Language Support"

2. **Configure Language Server:**

   ``File → Settings → Languages & Frameworks → mlpy``

   - Language Server Path: ``mlpy lsp``
   - Enable diagnostics: ✅
   - Security level: ``strict``

Features
--------

- **Project Templates:** Create new ML projects from IntelliJ
- **Run Configurations:** Execute ML files directly from IDE
- **Debugger Integration:** Debug transpiled Python with source maps
- **Security Inspection:** Real-time security analysis

Vim/Neovim
==========

Using coc.nvim
--------------

1. **Install coc.nvim** if not already installed

2. **Configure coc-settings.json:**

   .. code-block:: json

      {
        "languageserver": {
          "mlpy": {
            "command": "mlpy",
            "args": ["lsp"],
            "filetypes": ["ml"],
            "rootPatterns": ["mlpy.json", ".mlpy.json"]
          }
        }
      }

Using Native LSP (Neovim 0.5+)
-------------------------------

.. code-block:: lua

   -- init.lua or config file
   local nvim_lsp = require('lspconfig')

   nvim_lsp.mlpy = {
     default_config = {
       cmd = {'mlpy', 'lsp'},
       filetypes = {'ml'},
       root_dir = function(fname)
         return nvim_lsp.util.root_pattern('mlpy.json', '.mlpy.json')(fname)
       end,
       settings = {
         mlpy = {
           security = {
             level = "strict"
           }
         }
       }
     }
   }

Emacs
=====

Using lsp-mode
--------------

.. code-block:: elisp

   ;; Add to your Emacs configuration
   (use-package lsp-mode
     :hook (ml-mode . lsp)
     :commands lsp)

   ;; Define mlpy language server
   (lsp-register-client
    (make-lsp-client
     :new-connection (lsp-stdio-connection '("mlpy" "lsp"))
     :major-modes '(ml-mode)
     :server-id 'mlpy-ls))

   ;; ML mode configuration
   (define-derived-mode ml-mode prog-mode "ML"
     "Major mode for ML programming language."
     (setq-local comment-start "// ")
     (setq-local comment-end ""))

   (add-to-list 'auto-mode-alist '("\\.ml\\'" . ml-mode))

Sublime Text
============

Using LSP Package
-----------------

1. **Install Package Control** if not already installed

2. **Install LSP package:**

   ``Tools → Command Palette → Package Control: Install Package → LSP``

3. **Configure LSP settings:**

   ``Preferences → Package Settings → LSP → Settings``

   .. code-block:: json

      {
        "clients": {
          "mlpy": {
            "enabled": true,
            "command": ["mlpy", "lsp"],
            "selector": "source.ml"
          }
        }
      }

4. **Add ML syntax highlighting:**

   Create ``ML.sublime-syntax`` in your User packages directory.

Custom Editor Integration
=========================

If your editor supports LSP, you can integrate mlpy by:

1. **Start the Language Server:**

   .. code-block:: bash

      mlpy lsp --stdio

2. **Configure your editor** to:
   - Launch ``mlpy lsp`` for ``.ml`` files
   - Use ``mlpy.json`` or ``.mlpy.json`` as root markers
   - Send LSP messages over stdio

Language Server Configuration
=============================

The mlpy Language Server supports various configuration options:

.. code-block:: json

   {
     "mlpy": {
       "server": {
         "enabled": true,
         "trace": "messages"
       },
       "security": {
         "level": "strict",
         "diagnostics": true,
         "capabilities": ["file_read", "file_write"]
       },
       "completion": {
         "enabled": true,
         "triggerCharacters": [".", ":", "(", "[", "{"],
         "snippets": true
       },
       "formatting": {
         "enabled": true,
         "lineLength": 100
       },
       "diagnostics": {
         "enabled": true,
         "severity": "warning"
       }
     }
   }

Debugging Integration
====================

Source Map Support
------------------

mlpy generates source maps that enable debugging transpiled Python code with ML source locations:

.. code-block:: bash

   # Compile with source maps
   mlpy compile --source-maps src/main.ml

   # Debug with IDE
   # Breakpoints in .ml files will map to correct Python locations

Advanced Features
=================

Custom Capabilities
-------------------

Configure custom security capabilities per project:

.. code-block:: json

   {
     "mlpy": {
       "security": {
         "customCapabilities": {
           "database": ["db_read", "db_write"],
           "network": ["http_client", "websocket"]
         }
       }
     }
   }

Performance Tuning
------------------

For large projects, optimize the language server:

.. code-block:: json

   {
     "mlpy": {
       "performance": {
         "incrementalSync": true,
         "backgroundAnalysis": true,
         "cacheEnabled": true,
         "parallelAnalysis": true
       }
     }
   }

Troubleshooting
===============

Common Issues
-------------

**Language Server not starting:**

.. code-block:: bash

   # Check mlpy installation
   mlpy --version

   # Test language server manually
   mlpy lsp --stdio

**No syntax highlighting:**
   - Verify file extension is ``.ml``
   - Check editor's language association settings
   - Restart editor after configuration changes

**Diagnostics not showing:**
   - Check security level configuration
   - Verify diagnostics are enabled in editor settings
   - Check language server logs

**Performance issues:**
   - Enable incremental sync
   - Reduce diagnostic frequency
   - Enable caching

Debug Mode
----------

Start language server in debug mode:

.. code-block:: bash

   # Enable verbose logging
   mlpy lsp --verbose

   # TCP mode for external debugging
   mlpy lsp --tcp --port 2087

Log Files
---------

Language server logs are typically found at:

- **Windows:** ``%APPDATA%\mlpy\logs\``
- **macOS:** ``~/Library/Logs/mlpy/``
- **Linux:** ``~/.local/share/mlpy/logs/``