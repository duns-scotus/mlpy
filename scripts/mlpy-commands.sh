#!/bin/bash
# mlpy Claude Code Command Shortcuts

case "$1" in
    "sprint:capabilities")
        echo "📖 Loading Sprint 4 Capability System Guide..."
        cat .claude/commands/sprint/capabilities.md
        ;;
    "ml-compiler:transpile-test")
        echo "🧪 Loading ML Transpilation Test Guide..."
        cat .claude/commands/ml-compiler/transpile-test.md
        ;;
    "ml-compiler:security-audit")
        echo "🔒 Loading Security Audit Guide..."
        cat .claude/commands/ml-compiler/security-audit.md
        ;;
    "development:setup-env")
        echo "🛠️ Loading Development Setup Guide..."
        cat .claude/commands/development/setup-env.md
        ;;
    "quality:sprint-health-check")
        echo "📊 Loading Quality Health Check Guide..."
        cat .claude/commands/quality/sprint-health-check.md
        ;;
    *)
        echo "Available commands:"
        echo "  sprint:capabilities"
        echo "  ml-compiler:transpile-test"
        echo "  ml-compiler:security-audit"
        echo "  development:setup-env"
        echo "  quality:sprint-health-check"
        ;;
esac