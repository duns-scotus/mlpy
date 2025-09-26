=========================
Project Setup Reference
=========================

**Quick Start Templates and Workflows** - *Get ML projects up and running fast*

Project Initialization
======================

Basic Project Setup
-------------------

.. code-block:: bash

   # Create new ML project
   mlpy init my-project
   cd my-project

   # Project structure created:
   my-project/
   ├── mlpy.json              # Project configuration
   ├── src/                   # Source code
   │   └── main.ml           # Entry point
   ├── tests/                # Test files
   │   └── test_main.ml      # Basic tests
   ├── docs/                 # Documentation
   ├── .gitignore            # Git ignore rules
   └── README.md             # Project description

Project Templates
-----------------

.. code-block:: bash

   # Available project templates
   mlpy init --template basic my-app          # Basic application
   mlpy init --template web-app my-web        # Web application with HTTP
   mlpy init --template cli-tool my-tool      # Command-line tool
   mlpy init --template library my-lib        # Reusable library
   mlpy init --template data-analysis my-data # Data processing pipeline

   # Interactive template selection
   mlpy init --interactive my-project

Project Configuration
=====================

mlpy.json Configuration
----------------------

Basic ``mlpy.json`` structure:

.. code-block:: json

   {
     "name": "my-project",
     "version": "1.0.0",
     "description": "My ML application",
     "author": "Your Name <email@example.com>",
     "license": "MIT",

     "source": {
       "directory": "src",
       "entry": "main.ml"
     },

     "output": {
       "directory": "dist",
       "format": "python",
       "sourceMap": true
     },

     "security": {
       "level": "strict",
       "allowedCapabilities": [
         "file_read",
         "file_write",
         "network"
       ],
       "disallowedPatterns": [
         "eval",
         "exec",
         "__import__"
       ]
     },

     "compiler": {
       "optimization": 2,
       "generateTypes": true,
       "strictTypes": true
     },

     "testing": {
       "directory": "tests",
       "runner": "mlpy-test",
       "coverage": true
     }
   }

Environment-Specific Configuration
---------------------------------

**Development (``mlpy.dev.json``)**:

.. code-block:: json

   {
     "extends": "./mlpy.json",
     "compiler": {
       "optimization": 0,
       "debug": true,
       "sourceMap": true
     },
     "security": {
       "level": "permissive",
       "developmentMode": true
     }
   }

**Production (``mlpy.prod.json``)**:

.. code-block:: json

   {
     "extends": "./mlpy.json",
     "compiler": {
       "optimization": 3,
       "minify": true,
       "sourceMap": false
     },
     "security": {
       "level": "strict",
       "auditLogging": true
     }
   }

Project Types
=============

Basic Application
----------------

**Structure:**

.. code-block:: text

   basic-app/
   ├── mlpy.json
   ├── src/
   │   ├── main.ml            # Application entry point
   │   ├── config.ml          # Configuration handling
   │   └── utils.ml           # Utility functions
   ├── tests/
   │   ├── test_main.ml
   │   └── test_utils.ml
   └── data/                  # Application data
       └── config.json

**Entry Point (``src/main.ml``)**:

.. code-block:: ml

   // Basic application structure
   import { loadConfig } from "./config"
   import { processData, formatOutput } from "./utils"

   function main() {
       // Load configuration
       config = loadConfig("data/config.json")
       if (!config) {
           print("Error: Could not load configuration")
           return 1
       }

       // Process data
       result = processData(config.input)

       // Output results
       output = formatOutput(result)
       print(output)

       return 0
   }

   // Run application
   exit_code = main()
   exit(exit_code)

Web Application
--------------

**Structure:**

.. code-block:: text

   web-app/
   ├── mlpy.json
   ├── src/
   │   ├── main.ml            # Server entry point
   │   ├── routes/            # HTTP route handlers
   │   │   ├── api.ml
   │   │   └── pages.ml
   │   ├── models/            # Data models
   │   │   ├── user.ml
   │   │   └── product.ml
   │   ├── services/          # Business logic
   │   │   ├── auth.ml
   │   │   └── database.ml
   │   └── middleware/        # HTTP middleware
   │       ├── security.ml
   │       └── logging.ml
   ├── static/                # Static files
   │   ├── css/
   │   ├── js/
   │   └── images/
   └── templates/             # HTML templates
       ├── base.html
       └── index.html

**Server Entry Point (``src/main.ml``)**:

.. code-block:: ml

   // Web application with capability-based security
   import { createServer, Router } from "std/http"
   import { setupRoutes } from "./routes/api"
   import { authMiddleware } from "./middleware/security"
   import { loadConfig } from "./config"

   capability (network, file_read) function main() {
       // Load server configuration
       config = loadConfig("config/server.json")

       // Create HTTP server with security middleware
       server = createServer({
           port: config.port || 8080,
           host: config.host || "localhost"
       })

       // Set up middleware
       server.use(authMiddleware)
       server.use(loggingMiddleware)

       // Set up routes
       setupRoutes(server)

       // Start server
       print("Starting server on http://" + config.host + ":" + config.port)
       server.listen()
   }

   main()

Command-Line Tool
----------------

**Structure:**

.. code-block:: text

   cli-tool/
   ├── mlpy.json
   ├── src/
   │   ├── main.ml            # CLI entry point
   │   ├── commands/          # Command implementations
   │   │   ├── init.ml
   │   │   ├── build.ml
   │   │   └── deploy.ml
   │   ├── parsers/           # Argument parsing
   │   │   └── args.ml
   │   └── utils/
   │       ├── files.ml
   │       └── console.ml
   └── man/                   # Manual pages
       └── my-tool.1

**CLI Entry Point (``src/main.ml``)**:

.. code-block:: ml

   // Command-line tool with argument parsing
   import { parseArguments, showHelp } from "./parsers/args"
   import { initCommand } from "./commands/init"
   import { buildCommand } from "./commands/build"
   import { deployCommand } from "./commands/deploy"

   function main(args: string[]) {
       parsed = parseArguments(args)

       if (parsed.help) {
           showHelp()
           return 0
       }

       match parsed.command {
           "init" => {
               return initCommand(parsed.args)
           };
           "build" => {
               return buildCommand(parsed.args)
           };
           "deploy" => {
               return deployCommand(parsed.args)
           };
           _ => {
               print("Error: Unknown command '" + parsed.command + "'")
               showHelp()
               return 1
           };
       }
   }

   // Get command line arguments and run
   args = getProcessArguments()
   exit_code = main(args)
   exit(exit_code)

Library Project
--------------

**Structure:**

.. code-block:: text

   library/
   ├── mlpy.json
   ├── src/
   │   ├── index.ml           # Library entry point (exports)
   │   ├── core/              # Core functionality
   │   │   ├── parser.ml
   │   │   └── validator.ml
   │   ├── utils/             # Utility modules
   │   │   ├── strings.ml
   │   │   └── arrays.ml
   │   └── types/             # Type definitions
   │       └── common.ml
   ├── examples/              # Usage examples
   │   ├── basic.ml
   │   └── advanced.ml
   └── benchmark/             # Performance tests
       └── perf.ml

**Library Entry Point (``src/index.ml``)**:

.. code-block:: ml

   // Library exports - public API
   export { Parser, parseInput, ValidationResult } from "./core/parser"
   export { Validator, validateData } from "./core/validator"
   export { StringUtils } from "./utils/strings"
   export { ArrayUtils } from "./utils/arrays"
   export * from "./types/common"

   // Library metadata
   export const VERSION = "1.0.0"
   export const AUTHOR = "Library Author"

Data Analysis Project
--------------------

**Structure:**

.. code-block:: text

   data-analysis/
   ├── mlpy.json
   ├── src/
   │   ├── main.ml            # Analysis pipeline
   │   ├── readers/           # Data input
   │   │   ├── csv.ml
   │   │   └── json.ml
   │   ├── processors/        # Data transformation
   │   │   ├── clean.ml
   │   │   ├── aggregate.ml
   │   │   └── filter.ml
   │   ├── analyzers/         # Statistical analysis
   │   │   ├── stats.ml
   │   │   └── correlations.ml
   │   └── exporters/         # Output generation
   │       ├── charts.ml
   │       └── reports.ml
   ├── data/                  # Input data
   │   ├── raw/
   │   └── processed/
   └── output/                # Generated reports
       ├── charts/
       └── reports/

**Analysis Pipeline (``src/main.ml``)**:

.. code-block:: ml

   // Data analysis pipeline with functional programming
   import { readCSV } from "./readers/csv"
   import { cleanData, filterOutliers } from "./processors/clean"
   import { calculateStats, findCorrelations } from "./analyzers/stats"
   import { generateCharts, createReport } from "./exporters/reports"

   capability (file_read, file_write) function analyzeData(input_file: string) {
       // Data processing pipeline
       raw_data = readCSV(input_file)

       cleaned_data = raw_data
           |> cleanData
           |> filterOutliers

       // Statistical analysis
       stats = calculateStats(cleaned_data)
       correlations = findCorrelations(cleaned_data)

       // Generate outputs
       charts = generateCharts(stats, correlations)
       report = createReport({
           data: cleaned_data,
           statistics: stats,
           correlations: correlations,
           charts: charts
       })

       // Save results
       writeFile("output/analysis_report.html", report.html)
       writeFile("output/data_summary.json", stringifyJSON(stats, 2))

       print("Analysis complete! Results saved to output/")
       return true
   }

   // Run analysis
   success = analyzeData("data/raw/dataset.csv")
   exit(success ? 0 : 1)

Development Workflows
====================

Local Development
-----------------

.. code-block:: bash

   # Set up development environment
   cd my-project

   # Install dependencies (if any)
   mlpy install

   # Run in development mode
   mlpy run --dev src/main.ml

   # Watch for changes and auto-reload
   mlpy watch src/

   # Run tests continuously
   mlpy test --watch

   # Format code on save
   mlpy format src/ --watch

Build and Test Workflow
-----------------------

.. code-block:: bash

   # Clean previous builds
   mlpy clean

   # Compile project
   mlpy compile src/ --output dist/

   # Run all tests
   mlpy test

   # Run security analysis
   mlpy analyze --security

   # Generate documentation
   mlpy docs --output docs/

   # Check code quality
   mlpy lint src/

   # Create distribution package
   mlpy package --format wheel

Production Deployment
--------------------

.. code-block:: bash

   # Build optimized version
   mlpy compile --config mlpy.prod.json --optimize 3

   # Run security audit
   mlpy analyze --security --strict --output security-report.html

   # Create deployment package
   mlpy package --config mlpy.prod.json --include-runtime

   # Deploy to server (example)
   scp dist/my-app.tar.gz server:/opt/applications/
   ssh server "cd /opt/applications && tar -xzf my-app.tar.gz && ./deploy.sh"

Continuous Integration
=====================

GitHub Actions Workflow
-----------------------

Create ``.github/workflows/ml-ci.yml``:

.. code-block:: yaml

   name: ML Project CI

   on:
     push:
       branches: [ main, develop ]
     pull_request:
       branches: [ main ]

   jobs:
     test:
       runs-on: ubuntu-latest

       steps:
       - uses: actions/checkout@v3

       - name: Set up Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.12'

       - name: Install mlpy
         run: |
           pip install mlpy
           mlpy --version

       - name: Install project dependencies
         run: mlpy install

       - name: Lint code
         run: mlpy lint src/

       - name: Run security analysis
         run: |
           mlpy analyze --security --output security-report.json
           cat security-report.json

       - name: Run tests
         run: |
           mlpy test --coverage --output test-results.xml

       - name: Build project
         run: |
           mlpy compile --output dist/
           mlpy package --output releases/

       - name: Upload artifacts
         uses: actions/upload-artifact@v3
         with:
           name: build-artifacts
           path: |
             dist/
             releases/
             security-report.json
             test-results.xml

GitLab CI Configuration
----------------------

Create ``.gitlab-ci.yml``:

.. code-block:: yaml

   stages:
     - lint
     - security
     - test
     - build
     - deploy

   variables:
     MLPY_VERSION: "latest"

   before_script:
     - pip install mlpy==$MLPY_VERSION

   lint:
     stage: lint
     script:
       - mlpy lint src/
     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"
       - if: $CI_COMMIT_BRANCH == "main"

   security:
     stage: security
     script:
       - mlpy analyze --security --strict --output security-report.json
     artifacts:
       reports:
         security: security-report.json
       paths:
         - security-report.json

   test:
     stage: test
     script:
       - mlpy test --coverage --junit test-results.xml
     artifacts:
       reports:
         junit: test-results.xml
       paths:
         - coverage/

   build:
     stage: build
     script:
       - mlpy compile --optimize 2 --output dist/
       - mlpy package --output packages/
     artifacts:
       paths:
         - dist/
         - packages/

   deploy:
     stage: deploy
     script:
       - ./deploy.sh packages/my-app.tar.gz
     only:
       - main
     when: manual

Development Tips
===============

Project Organization
-------------------

1. **Use Clear Directory Structure**: Separate source, tests, docs, and data
2. **Group Related Code**: Use subdirectories for modules (models/, services/, utils/)
3. **Follow Naming Conventions**: Use kebab-case for directories, camelCase for files
4. **Document Dependencies**: List all external requirements in mlpy.json
5. **Version Control Everything**: Include configuration, exclude generated files

Security Best Practices
-----------------------

1. **Principle of Least Privilege**: Only request needed capabilities
2. **Environment-Specific Config**: Different security levels for dev/prod
3. **Regular Security Audits**: Run ``mlpy analyze --security`` frequently
4. **Input Validation**: Always validate external data
5. **Secure Defaults**: Use strict security mode in production

Performance Optimization
-----------------------

1. **Profile Before Optimizing**: Use ``mlpy profile`` to identify bottlenecks
2. **Optimize Hot Paths**: Focus on frequently executed code
3. **Use Appropriate Data Structures**: Choose efficient algorithms and structures
4. **Cache Expensive Operations**: Store results of costly computations
5. **Minimize Capability Usage**: Reduce I/O and network operations

Quick Commands Reference
=======================

.. code-block:: bash

   # Project management
   mlpy init <name> [--template <template>]  # Create new project
   mlpy install                              # Install dependencies
   mlpy clean                               # Clean build artifacts

   # Development
   mlpy run <file> [--dev]                  # Run ML file
   mlpy watch <directory>                   # Watch and auto-reload
   mlpy format <path> [--watch]             # Format code

   # Building and testing
   mlpy compile <source> --output <dir>     # Compile project
   mlpy test [--watch] [--coverage]         # Run tests
   mlpy package [--format <format>]         # Create package

   # Quality assurance
   mlpy lint <path>                         # Check code quality
   mlpy analyze --security [--strict]       # Security analysis
   mlpy docs --output <dir>                 # Generate documentation

   # Utilities
   mlpy version                             # Show version
   mlpy help [<command>]                    # Show help
   mlpy config [--global] [--list]         # Manage configuration

**Remember:** Start with a template that matches your use case, then customize as needed!