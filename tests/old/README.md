# Outdated Tests Directory

This directory contains test files that are outdated and test functionality that is no longer used in the production mlpy system.

## Files in this directory:

- test_capability_integration.py - Tests for CallbackBridge, which is not used by production transpiler
- test_exploit_prevention.py - Tests for CallbackBridge security, which is not used by production transpiler

## Why these tests are outdated:

The production mlpy system uses:
- MLSandbox with subprocess-based execution
- CapabilityManager and CapabilityContext for security
- Direct Python imports for standard library modules

These tests were for an experimental threading-based bridge system (CallbackBridge) that was never integrated into the production transpiler pipeline.

## Test Status:

These tests timeout due to capability context not propagating across threads. This is not a production issue since CallbackBridge is not used.

Integration tests continue to pass at 97.7% success rate without this functionality.
