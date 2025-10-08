=======================
IDE Integration Reference
=======================

**Quick Setup Guides for Popular Code Editors** - *Get ML language support in your favorite editor*

Visual Studio Code
==================

Extension Installation
---------------------

.. code-block:: bash

   # Install the ML Language Extension
   code --install-extension mlpy-lang.ml-vscode

   # Or search "ML Language Support" in VS Code Extensions panel

Configuration
------------

Add to your VS Code ``settings.json``:

.. code-block:: json

   {
     "mlpy.languageServer.enable": true,
     "mlpy.languageServer.path": "/usr/local/bin/mlpy",
     "mlpy.security.enableAnalysis": true,
     "mlpy.formatting.enable": true,
     "mlpy.debugging.sourceMap": true,

     // File associations
     "files.associations": {
       "*.ml": "ml"
     },

     // Syntax highlighting
     "editor.tokenColorCustomizations": {
       "textMateRules": [
         {
           "scope": "keyword.capability.ml",
           "settings": {
             "foreground": "#FF6B35",
             "fontStyle": "bold"
           }
         }
       ]
     }
   }

Workspace Settings
-----------------

Create ``.vscode/settings.json`` in your project:

.. code-block:: json

   {
     "mlpy.project.root": "${workspaceFolder}",
     "mlpy.project.source": "src",
     "mlpy.project.output": "dist",
     "mlpy.security.strictMode": true,

     // Tasks for building and running
     "tasks.version": "2.0.0",
     "tasks": [
       {
         "label": "Build ML Project",
         "type": "shell",
         "command": "mlpy",
         "args": ["compile", "src/", "--output", "dist/"],
         "group": "build",
         "presentation": {
           "echo": true,
           "reveal": "always",
           "focus": false,
           "panel": "shared"
         }
       },
       {
         "label": "Run ML Project",
         "type": "shell",
         "command": "mlpy",
         "args": ["run", "src/main.ml"],
         "group": "test"
       }
     ]
   }

Keyboard Shortcuts
-----------------

Add to your VS Code ``keybindings.json``:

.. code-block:: json

   [
     {
       "key": "ctrl+shift+b",
       "command": "workbench.action.tasks.runTask",
       "args": "Build ML Project"
     },
     {
       "key": "f5",
       "command": "workbench.action.tasks.runTask",
       "args": "Run ML Project"
     },
     {
       "key": "ctrl+shift+f",
       "command": "mlpy.format.document"
     },
     {
       "key": "ctrl+shift+s",
       "command": "mlpy.security.analyze"
     }
   ]

Debugging Setup
--------------

Create ``.vscode/launch.json``:

.. code-block:: json

   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Debug ML Application",
         "type": "python",
         "request": "launch",
         "program": "${workspaceFolder}/dist/main.py",
         "console": "integratedTerminal",
         "preLaunchTask": "Build ML Project",
         "sourceMaps": true,
         "stopOnEntry": false
       },
       {
         "name": "Debug Current ML File",
         "type": "mlpy",
         "request": "launch",
         "file": "${file}",
         "stopOnEntry": true,
         "trace": true
       }
     ]
   }

IntelliJ IDEA / PyCharm
=======================

Plugin Installation
-------------------

.. code-block:: bash

   # From JetBrains Marketplace
   # Search "ML Language Plugin" in Settings > Plugins
   # Or install from file:

   # Download mlpy-intellij-plugin.jar
   # Go to Settings > Plugins > Install Plugin from Disk

Project Setup
-------------

1. **Create New Project:**

   - File → New → Project
   - Select "ML Language" from project types
   - Choose project template (Basic, Web App, CLI Tool)
   - Configure project SDK (Python 3.12+)

2. **Configure Existing Project:**

   Add to ``.idea/mlpy.xml``:

   .. code-block:: xml

      <?xml version="1.0" encoding="UTF-8"?>
      <project version="4">
        <component name="MLPyConfiguration">
          <option name="sourceRoot" value="$PROJECT_DIR$/src" />
          <option name="outputRoot" value="$PROJECT_DIR$/dist" />
          <option name="enableLSP" value="true" />
          <option name="securityAnalysis" value="true" />
          <option name="autoFormat" value="true" />
        </component>
      </project>

Code Completion
--------------

The plugin provides:
- **Smart completion** for ML keywords and built-ins
- **Context-aware suggestions** based on capabilities
- **Type-aware completion** for function parameters
- **Import suggestions** for standard library modules

Configuration in Settings:

.. code-block:: text

   Settings > Languages & Frameworks > ML Language
   ✅ Enable smart completion
   ✅ Show parameter hints
   ✅ Auto-import standard library
   ✅ Capability-aware suggestions
   ✅ Security warnings in completion

Build Configuration
------------------

Create run configuration:

.. code-block:: text

   Run > Edit Configurations > Add New > ML Application

   Name: Build and Run
   ML File: src/main.ml
   Working Directory: $PROJECT_DIR$
   Environment Variables:
     MLPY_PROJECT_ROOT=$PROJECT_DIR$
     MLPY_DEBUG=true

   Before Launch:
   ✅ Build ML Project (mlpy compile)
   ✅ Run security analysis

Security Analysis Integration
----------------------------

.. code-block:: text

   Settings > Tools > ML Security Analysis

   Analysis Level: Strict
   ✅ Real-time analysis
   ✅ Highlight security violations
   ✅ Show capability requirements
   ✅ Detect potential vulnerabilities

   Custom Rules: security-rules.yaml
   Report Format: HTML + JSON
   Auto-fix: Conservative

Vim/Neovim
==========

Plugin Installation
------------------

Using **vim-plug**:

.. code-block:: vim

   " In your .vimrc or init.vim
   Plug 'mlpy-lang/vim-ml'
   Plug 'neovim/nvim-lspconfig'  " For LSP support
   Plug 'hrsh7th/nvim-cmp'       " For completion

   " Install plugins
   :PlugInstall

Using **packer.nvim** (Neovim):

.. code-block:: lua

   -- In your plugins.lua
   use {
     'mlpy-lang/vim-ml',
     'neovim/nvim-lspconfig',
     'hrsh7th/nvim-cmp',
   }

LSP Configuration
----------------

Add to your Neovim ``init.lua``:

.. code-block:: lua

   -- ML Language Server setup
   local lspconfig = require('lspconfig')

   lspconfig.mlpy_lsp.setup {
     cmd = { 'mlpy', 'lsp' },
     filetypes = { 'ml' },
     root_dir = lspconfig.util.root_pattern('mlpy.json', '.git'),
     settings = {
       mlpy = {
         security = {
           enableAnalysis = true,
           strictMode = true
         },
         completion = {
           enableCapabilityHints = true,
           showTypeInfo = true
         },
         diagnostics = {
           enableSecurityWarnings = true,
           showCapabilityErrors = true
         }
       }
     },
     on_attach = function(client, bufnr)
       -- Keybindings
       local opts = { noremap=true, silent=true, buffer=bufnr }
       vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
       vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)
       vim.keymap.set('n', '<leader>ca', vim.lsp.buf.code_action, opts)
       vim.keymap.set('n', '<leader>rn', vim.lsp.buf.rename, opts)
       vim.keymap.set('n', '<leader>f', vim.lsp.buf.format, opts)
     end
   }

Syntax Highlighting
------------------

The plugin provides syntax highlighting for:
- ML keywords (``capability``, ``match``, ``async``)
- Built-in functions and types
- Security annotations
- String interpolation
- Comments and documentation

Customize colors in your ``.vimrc``:

.. code-block:: vim

   " ML syntax highlighting customization
   hi mlCapability ctermfg=208 guifg=#FF6B35 cterm=bold gui=bold
   hi mlSecurityAnnotation ctermfg=196 guifg=#FF0000
   hi mlBuiltinFunction ctermfg=33 guifg=#0087FF
   hi mlTypeAnnotation ctermfg=105 guifg=#8787FF

Key Mappings
-----------

Add to your ``.vimrc`` or ``init.vim``:

.. code-block:: vim

   " ML-specific key mappings
   autocmd FileType ml nmap <buffer> <leader>r :!mlpy run %<CR>
   autocmd FileType ml nmap <buffer> <leader>c :!mlpy compile %<CR>
   autocmd FileType ml nmap <buffer> <leader>t :!mlpy test<CR>
   autocmd FileType ml nmap <buffer> <leader>s :!mlpy analyze --security %<CR>
   autocmd FileType ml nmap <buffer> <leader>f :!mlpy format %<CR>

   " Quick capability insertion
   autocmd FileType ml imap <buffer> cap capability ()<Left>
   autocmd FileType ml imap <buffer> fn function ()<Left>

Build Integration
----------------

Create ML build commands:

.. code-block:: vim

   " In your .vimrc
   command! MLRun !mlpy run %
   command! MLCompile !mlpy compile %
   command! MLTest !mlpy test
   command! MLFormat !mlpy format %
   command! MLSecurity !mlpy analyze --security %

   " Set makeprg for :make command
   autocmd FileType ml setlocal makeprg=mlpy\ compile\ %

Emacs
=====

Package Installation
-------------------

Using **MELPA**:

.. code-block:: elisp

   ;; In your init.el
   (require 'package)
   (add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/"))
   (package-initialize)

   ;; Install packages
   (package-install 'ml-mode)
   (package-install 'lsp-mode)
   (package-install 'company)

Using **use-package**:

.. code-block:: elisp

   (use-package ml-mode
     :ensure t
     :mode "\\.ml\\'")

   (use-package lsp-mode
     :ensure t
     :hook (ml-mode . lsp-deferred)
     :commands lsp)

   (use-package company
     :ensure t
     :hook (ml-mode . company-mode))

ML Mode Configuration
--------------------

.. code-block:: elisp

   ;; ML language configuration
   (add-to-list 'auto-mode-alist '("\\.ml\\'" . ml-mode))

   ;; ML mode hooks
   (add-hook 'ml-mode-hook
             (lambda ()
               (setq-local tab-width 4)
               (setq-local indent-tabs-mode nil)
               (setq-local comment-start "// ")
               (setq-local comment-end "")
               (electric-pair-mode 1)
               (show-paren-mode 1)))

LSP Mode Setup
-------------

.. code-block:: elisp

   ;; ML Language Server configuration
   (with-eval-after-load 'lsp-mode
     (add-to-list 'lsp-language-id-configuration '(ml-mode . "ml"))
     (lsp-register-client
      (make-lsp-client
       :new-connection (lsp-stdio-connection '("mlpy" "lsp"))
       :major-modes '(ml-mode)
       :server-id 'mlpy-lsp)))

   ;; LSP UI configuration
   (use-package lsp-ui
     :ensure t
     :hook (lsp-mode . lsp-ui-mode)
     :config
     (setq lsp-ui-doc-enable t
           lsp-ui-doc-position 'at-point
           lsp-ui-sideline-enable t
           lsp-ui-sideline-show-code-actions t))

Compilation and Running
----------------------

.. code-block:: elisp

   ;; ML compilation functions
   (defun ml-compile ()
     "Compile current ML file"
     (interactive)
     (compile (format "mlpy compile %s" (buffer-file-name))))

   (defun ml-run ()
     "Run current ML file"
     (interactive)
     (compile (format "mlpy run %s" (buffer-file-name))))

   (defun ml-test ()
     "Run ML tests"
     (interactive)
     (compile "mlpy test"))

   (defun ml-format ()
     "Format current ML file"
     (interactive)
     (shell-command (format "mlpy format %s" (buffer-file-name)))
     (revert-buffer t t))

   ;; Key bindings
   (define-key ml-mode-map (kbd "C-c C-c") 'ml-compile)
   (define-key ml-mode-map (kbd "C-c C-r") 'ml-run)
   (define-key ml-mode-map (kbd "C-c C-t") 'ml-test)
   (define-key ml-mode-map (kbd "C-c C-f") 'ml-format)

Org-Mode Integration
-------------------

.. code-block:: elisp

   ;; ML code blocks in org-mode
   (org-babel-do-load-languages
    'org-babel-load-languages
    '((ml . t)))

   ;; ML source block execution
   (defun org-babel-execute:ml (body params)
     "Execute ML code block"
     (let ((temp-file (make-temp-file "org-babel-ml" nil ".ml")))
       (with-temp-file temp-file
         (insert body))
       (shell-command-to-string
        (format "mlpy run %s" temp-file))))

Sublime Text
============

Package Installation
-------------------

1. **Install Package Control** (if not already installed)
2. **Install ML Language Package:**

   - Cmd/Ctrl + Shift + P
   - Type "Package Control: Install Package"
   - Search "ML Language Support"
   - Install the package

Syntax Highlighting
------------------

Create ``ML.sublime-syntax`` in your User packages:

.. code-block:: yaml

   %YAML 1.2
   ---
   name: ML
   file_extensions: [ml]
   scope: source.ml

   contexts:
     main:
       - match: '\b(capability|function|if|else|for|while|match|async|await|import|export|type)\b'
         scope: keyword.control.ml
       - match: '\b(string|number|boolean|null|undefined)\b'
         scope: storage.type.ml
       - match: '".*?"'
         scope: string.quoted.double.ml
       - match: '//.*$'
         scope: comment.line.double-slash.ml

Build System
-----------

Create ``ML.sublime-build``:

.. code-block:: json

   {
     "shell_cmd": "mlpy run $file",
     "file_regex": "^(.+?):(\\d+):(\\d+): (.*)$",
     "working_dir": "${project_path}",
     "selector": "source.ml",

     "variants": [
       {
         "name": "Compile Only",
         "shell_cmd": "mlpy compile $file"
       },
       {
         "name": "Run Tests",
         "shell_cmd": "mlpy test"
       },
       {
         "name": "Security Analysis",
         "shell_cmd": "mlpy analyze --security $file"
       }
     ]
   }

Common IDE Features
===================

Language Server Protocol Support
-------------------------------

All modern editors can use the ML Language Server:

.. code-block:: bash

   # Start ML Language Server
   mlpy lsp

   # With specific configuration
   mlpy lsp --config mlpy-lsp.json

   # Debug mode
   mlpy lsp --debug --log-file lsp.log

Features provided by LSP:
- **Code Completion** with capability awareness
- **Error Diagnostics** including security warnings
- **Go to Definition** for functions and types
- **Hover Information** with type details
- **Document Formatting** according to ML style guide
- **Code Actions** for security fixes

Project Configuration
--------------------

Create ``mlpy-lsp.json`` in project root:

.. code-block:: json

   {
     "languageServer": {
       "completion": {
         "enableSnippets": true,
         "showCapabilityHints": true,
         "prioritizeSecure": true
       },
       "diagnostics": {
         "enableSecurity": true,
         "securityLevel": "strict",
         "showTypeErrors": true,
         "showUnusedVariables": true
       },
       "formatting": {
         "indentSize": 4,
         "insertFinalNewline": true,
         "trimTrailingWhitespace": true
       },
       "security": {
         "enableRealTimeAnalysis": true,
         "highlightViolations": true,
         "showCapabilityRequirements": true
       }
     }
   }

General Integration Tips
=======================

1. **Always Enable LSP**: Use the ML Language Server for best experience
2. **Configure Security Analysis**: Enable real-time security checking
3. **Set Up Build Tasks**: Configure compilation and execution shortcuts
4. **Use Source Maps**: Enable debugging with generated Python code
5. **Format on Save**: Auto-format ML code for consistency
6. **Capability Hints**: Enable completion hints for required capabilities
7. **Project Templates**: Use ``mlpy init`` for consistent project structure

**Remember:** The ML Language Server provides the richest development experience across all editors!