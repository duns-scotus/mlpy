"""
ML Language Server Semantic Tokens Provider
Main provider class that integrates semantic tokens with the LSP server.
"""

import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from .semantic_tokens import MLSemanticTokenMapper, SemanticTokensEncoder, SemanticToken
from ..ml.grammar.parser import MLParser
from ..ml.grammar.ast_nodes import ASTNode

logger = logging.getLogger(__name__)


@dataclass
class SemanticTokensResult:
    """Result of semantic tokens analysis."""
    tokens: List[int]  # Encoded tokens in LSP format
    result_id: Optional[str] = None  # For delta updates


@dataclass
class DocumentTokenInfo:
    """Cached token information for a document."""
    tokens: List[SemanticToken]
    encoded_tokens: List[int]
    version: int
    result_id: str


class MLSemanticTokensProvider:
    """Provides semantic tokens for ML language documents."""

    def __init__(self, parser: Optional[MLParser] = None):
        """Initialize the semantic tokens provider."""
        self.parser = parser or MLParser()
        self.mapper = MLSemanticTokenMapper()
        self.encoder = SemanticTokensEncoder()
        self.document_cache: Dict[str, DocumentTokenInfo] = {}
        self._next_result_id = 1

    def get_semantic_tokens_full(self, uri: str, text: str, version: int = 0) -> SemanticTokensResult:
        """Get full semantic tokens for a document."""
        try:
            # Check cache first
            if uri in self.document_cache:
                cached_info = self.document_cache[uri]
                if cached_info.version == version:
                    logger.debug(f"Returning cached semantic tokens for {uri}")
                    return SemanticTokensResult(
                        tokens=cached_info.encoded_tokens,
                        result_id=cached_info.result_id
                    )

            # Parse the document
            logger.debug(f"Parsing document for semantic tokens: {uri}")
            ast = self.parser.parse(text)

            # Generate semantic tokens
            tokens = self.mapper.map_ast_to_tokens(ast, text)

            # Encode tokens
            encoded_tokens = self.encoder.encode_tokens(tokens)

            # Generate result ID
            result_id = str(self._next_result_id)
            self._next_result_id += 1

            # Cache the result
            self.document_cache[uri] = DocumentTokenInfo(
                tokens=tokens,
                encoded_tokens=encoded_tokens,
                version=version,
                result_id=result_id
            )

            logger.debug(f"Generated {len(tokens)} semantic tokens for {uri}")
            return SemanticTokensResult(tokens=encoded_tokens, result_id=result_id)

        except Exception as e:
            logger.error(f"Failed to generate semantic tokens for {uri}: {e}")
            return SemanticTokensResult(tokens=[])

    def get_semantic_tokens_range(self, uri: str, text: str, start_line: int,
                                end_line: int, version: int = 0) -> SemanticTokensResult:
        """Get semantic tokens for a specific range in a document."""
        try:
            # For simplicity, get full tokens and filter
            full_result = self.get_semantic_tokens_full(uri, text, version)

            if uri not in self.document_cache:
                return SemanticTokensResult(tokens=[])

            cached_info = self.document_cache[uri]

            # Filter tokens by line range
            range_tokens = [
                token for token in cached_info.tokens
                if start_line <= token.line <= end_line
            ]

            # Re-encode the filtered tokens
            encoded_tokens = self.encoder.encode_tokens(range_tokens)

            logger.debug(f"Generated {len(range_tokens)} range semantic tokens for {uri} (lines {start_line}-{end_line})")
            return SemanticTokensResult(tokens=encoded_tokens)

        except Exception as e:
            logger.error(f"Failed to generate range semantic tokens for {uri}: {e}")
            return SemanticTokensResult(tokens=[])

    def get_semantic_tokens_delta(self, uri: str, text: str, previous_result_id: str,
                                version: int = 0) -> SemanticTokensResult:
        """Get semantic tokens delta from a previous result."""
        try:
            # For now, implement as full refresh
            # A proper delta implementation would calculate differences
            logger.debug(f"Delta tokens requested for {uri}, returning full tokens")
            return self.get_semantic_tokens_full(uri, text, version)

        except Exception as e:
            logger.error(f"Failed to generate delta semantic tokens for {uri}: {e}")
            return SemanticTokensResult(tokens=[])

    def invalidate_cache(self, uri: str) -> None:
        """Invalidate cached tokens for a document."""
        if uri in self.document_cache:
            del self.document_cache[uri]
            logger.debug(f"Invalidated semantic tokens cache for {uri}")

    def clear_cache(self) -> None:
        """Clear all cached tokens."""
        self.document_cache.clear()
        logger.debug("Cleared all semantic tokens cache")

    def get_token_types(self) -> List[str]:
        """Get supported token types."""
        return self.encoder.get_token_types()

    def get_token_modifiers(self) -> List[str]:
        """Get supported token modifiers."""
        return self.encoder.get_token_modifiers()

    def analyze_document_performance(self, uri: str, text: str) -> Dict[str, Any]:
        """Analyze semantic tokens performance for a document."""
        import time

        start_time = time.time()

        try:
            # Parse
            parse_start = time.time()
            ast = self.parser.parse(text)
            parse_time = time.time() - parse_start

            # Map tokens
            map_start = time.time()
            tokens = self.mapper.map_ast_to_tokens(ast, text)
            map_time = time.time() - map_start

            # Encode tokens
            encode_start = time.time()
            encoded_tokens = self.encoder.encode_tokens(tokens)
            encode_time = time.time() - encode_start

            total_time = time.time() - start_time

            return {
                "success": True,
                "total_time_ms": round(total_time * 1000, 2),
                "parse_time_ms": round(parse_time * 1000, 2),
                "map_time_ms": round(map_time * 1000, 2),
                "encode_time_ms": round(encode_time * 1000, 2),
                "token_count": len(tokens),
                "encoded_length": len(encoded_tokens),
                "document_length": len(text),
                "lines": len(text.split('\n'))
            }

        except Exception as e:
            total_time = time.time() - start_time
            return {
                "success": False,
                "total_time_ms": round(total_time * 1000, 2),
                "error": str(e),
                "document_length": len(text),
                "lines": len(text.split('\n'))
            }

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_tokens = sum(len(info.tokens) for info in self.document_cache.values())
        total_encoded_size = sum(len(info.encoded_tokens) for info in self.document_cache.values())

        return {
            "cached_documents": len(self.document_cache),
            "total_tokens": total_tokens,
            "total_encoded_size": total_encoded_size,
            "next_result_id": self._next_result_id,
            "cache_entries": {
                uri: {
                    "token_count": len(info.tokens),
                    "encoded_size": len(info.encoded_tokens),
                    "version": info.version,
                    "result_id": info.result_id
                }
                for uri, info in self.document_cache.items()
            }
        }