"""Core code generation infrastructure."""

from .context import SourceMapping, CodeGenerationContext
from .generator_base import GeneratorBase

__all__ = ['SourceMapping', 'CodeGenerationContext', 'GeneratorBase']
