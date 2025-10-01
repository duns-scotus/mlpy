# A Complete Rewrite of the Module and Standard Library System

## Where we are

The existing module system is an ad hoc system that is
way to complicated. Adding python modules for 
ml users is a pain. 

There are no clear integration points with the capability
system and the security system.  

The Standard Library is bloated with
ad hoc additions to get integration tests working, 
the paradigm has been a functional approach,
leaving object oriented parts of the python code 
out or implementing this ad hoc.

As the ML Language is considered a "security first"
language, access to python functionality has to be
carefully designed and to be strictly limited. ML 
is designed to run in a sandbox with no direct
system access. This should be preserved. Sandbox
escape into the "python wild" would be the worst
case.

A complete redesign should be seriously taken into account.

## Where we want to get

### Import statement

The ml import statement should
    * import standard library modules written in python
    * import standard library modules written in ML
    * import user defined ML modules if the system is
      configured for this (CLI/sandbox option import path)

Modules should be accessed from ML as objects, 
as in Python. We want limited self detection, 
self documentation and introspection (see the prospective 
builtin standard library module).

### Decorator syntax

Standard modules should be auto-detected. The pubic
interface accessible to ML should be defined by
decorators (constants, variables, functions and classes,
methods and attributes/properties. Further
decorators should allow for capability-exposure and
(runtime ?) capability control.

### Standard Library with builtin Module

We want to have a carefully designed Standard Library to
make working with basic datatypes easy and comfortable,
and to allow the ML Programmer type-testing, limited exploration 
and detection.

There should be a builtin standard module providing
basic classes

* string, 
* list, 
* dict, 
* float 
* module
* class

and fundamental functions

* str(), int(), float() for conversion, 
* type() for type detection, 
* len() for str/list/dict length,
* info() for reading documentation strings,
* dir() for detecting the published elements of a module/class/object),
* del() for deleting objects,
* print() and input(),
* hasattr(), getattr(), call() for dynamic ML Programming without 
  sandbox escape
* exit() for system exit,
* version() to get some mlpy version information.

at least, but we have to think twice about any function that populates 
the python global namespace.

All the builtin classes and functions should be usable without
module prefix. Carefully designing this builtin module should have 
the highest priority. 

The builtin module should be, at the same time, exemplary of how
to make ample use of all the decorators. 

It should get exhaustive documentation for ML Programmers and mlpy
developers alike.

# Methodology

It is essential to keep the existing infrastructure and unittests 
working as far as feasible, and to write unittests for each element 
we reimplement, as we develop them.

All this work should be done at a separate development branch of
the system with 

# Tasks

## Analyse and understand the existing system

We have to have a thorough and deep understanding of the complex
interplay between the following systems, as our aim is to be able to
integrate the new system into the existing mlpy infrastructure:

* secure module, class, object, method, attribute 
  detection and access (both static and runtime),
* module registration,
* capability registration, granting and control,
* security control and penetration protection,
* code generation,
* code execution.

One idea would be to enhance the existing system so
that we coud add a plug and play new system on the fly
later on.

## Document all our findings

Make a thorough and detailed documentation of all our
findings. Add code excerpts, file locations, calls and interfaces,
make calling and accessing the module system as defined above 
as transparent as possible (flow diagrams, function calls, file position,
code excerpts etc.). Review transpiled python code (.ml code examples in
tests/ml_integration) 

## Design the future system

This should be at least as detailed as your documentation of the 
current system (flow diagrams, function calls, file position, 
interfaces, code excerpts).

## Reimplement an easy to use Module System

Once we understand the existing system, we have to consider:

* carefully rewrite all the existing interfaces,
* delete the existing standard library and the .ml code
  in tests/ml_integration,
* delete current standard module and registry,
* disable current module import
* write minimal examples of string, math, list and
  dictionary functionality, of all control flow statements
  that are working without module import, to have a new
  basis for end-to-end integration testing (with tests/ml_test_runner.py)
* make sure, integration tests with ml_test_runner.py work.

## Reimplement a well thought out Minimal Standard Library

We have to think about what is needed with which priority.
The aim of ML is to provide an embeddable, simple scripting
language with SECURITY in uppercase, to be used with potentially
dangerous untrusted user code in any host program.

Think about 

* math, random, functional
* regex, JSON
* datetime
* sqlite (secure, granular capability controlled)
* file system access (secure, granular capability controlled)

## Retain flexibility

Have in mind that the same import statement to be used with 
ML standard library code written in python should work with
ML standard library code written in ML, and even with user
modules written in ML. 

# What to do next

Create a subfolder "module-rewrite.md" in the docs/proposals directory.
I want you to write a set of documents and place them in this new
directory:

* module-system-now.md
  describe the system as it is. Evaluate the highs and lows of what you see.

* module-system-future.md
  
  Describe the system as it should work. Design the decorators, write the interface
  of the future builtin module as an example.

  Describe the future layout of the module system and the integration of the core components.

* builtin.py

  - Design and implement the builtin module of the new standard library as described above as a python file. 
    Use the decorators you designed. 
  
    Your implementation should show how introspection, type-testing, self-documentation, capability 
    granting and checking would work (make use of interfaces you designed).

  - The idea would be to finally reach a "sweet point" in the development process when we can simply move
    this file into the mlyp.stdlib directory and see the whole thing shine up.
  
  - If possible, this click and collect approach should be usable in later ML Standard Library additions,
    too. 

* module-system-implementation.md

  - Write a detailed phased implementation strategy.
  
  - Indicate any preparatory work that needs to be done before touching the old module system.
    (Have in mind that there in no working .ml codebase in the wild yet, so you do not have to worry 
    about backwards compatibility of the future system; your only worry has to be that the development
    process is working, and the we do not break the whole mlpy system).

  - Maintain working code as far as possible. Incremental changes
    where feasable. Breaking/Deleting code where necessary.

  - Maintain usability of the unittests throughout the implementation process.

  - Write new unittests with every part of the system you implement.

  - Have example .ml code ready do demonstrate end-to-end integration with ml_test-runner.py at 
    any stage.

  - Try never to break the working end-to-end integration with sample code not using the module
    system.
  
  - This document should be used for claude to implement the system, so it has to have enough
    details to be used as a development guide from the beginning to the end. 
  
  - Advise implementation phases, success criteria, deliverables, timelines. Sketch the
    interfaces to be implemented or to be used, and the files to be touched, modified or
    deleted.

*  module-system-cost-benefit.md

   Review the documents you have written and analyse costs/benefits of the whole enterprise. We
   do not want over-engineering, but mlpy has to be elegant and easy to use, for ML Programmers,
   integration architects and ML developers alike. 

   Do you think this is a worthwile project - what does implementing this mean for ml as a 
   secure und serious integration language? Is it necessary to do this work?
