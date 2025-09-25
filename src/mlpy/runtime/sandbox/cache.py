"""Performance optimization caching for sandbox execution."""

import hashlib
import json
import pickle
import threading
import time
from collections import OrderedDict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from ..capabilities.context import CapabilityContext
from ..capabilities.tokens import CapabilityToken


@dataclass
class CacheEntry:
    """Single cache entry with metadata."""

    key: str
    value: Any
    created_at: float
    last_accessed: float
    access_count: int = 0
    size_bytes: int = 0
    metadata: dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def is_expired(self, ttl: float) -> bool:
        """Check if entry is expired based on TTL."""
        return (time.time() - self.created_at) > ttl

    def update_access(self) -> None:
        """Update access statistics."""
        self.last_accessed = time.time()
        self.access_count += 1


class SandboxCache:
    """Base cache implementation with LRU eviction and TTL support."""

    def __init__(self, max_size: int = 1000, default_ttl: float = 3600.0):
        """Initialize cache with size limit and TTL."""
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache."""
        with self._lock:
            entry = self._cache.get(key)

            if entry is None:
                self._misses += 1
                return default

            # Check expiration
            if entry.is_expired(self.default_ttl):
                del self._cache[key]
                self._misses += 1
                return default

            # Update access stats and move to end (most recent)
            entry.update_access()
            self._cache.move_to_end(key)
            self._hits += 1

            return entry.value

    def put(
        self, key: str, value: Any, ttl: float | None = None, metadata: dict[str, Any] = None
    ) -> None:
        """Put value in cache."""
        with self._lock:
            # Calculate size
            try:
                size_bytes = len(pickle.dumps(value))
            except (pickle.PicklingError, TypeError):
                size_bytes = len(str(value).encode("utf-8"))

            # Create entry
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=time.time(),
                last_accessed=time.time(),
                size_bytes=size_bytes,
                metadata=metadata or {},
            )

            # Add to cache
            self._cache[key] = entry
            self._cache.move_to_end(key)

            # Evict if necessary
            self._evict_if_needed()

    def remove(self, key: str) -> bool:
        """Remove key from cache."""
        with self._lock:
            return self._cache.pop(key, None) is not None

    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    def _evict_if_needed(self) -> None:
        """Evict entries if cache exceeds max size."""
        while len(self._cache) > self.max_size:
            # Remove least recently used (first item)
            self._cache.popitem(last=False)

    def cleanup_expired(self) -> int:
        """Remove all expired entries."""
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items() if entry.is_expired(self.default_ttl)
            ]

            for key in expired_keys:
                del self._cache[key]

            return len(expired_keys)

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = self._hits / total_requests if total_requests > 0 else 0.0

            total_size = sum(entry.size_bytes for entry in self._cache.values())

            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": hit_rate,
                "total_size_bytes": total_size,
                "default_ttl": self.default_ttl,
            }

    def get_all_keys(self) -> list[str]:
        """Get all cache keys."""
        with self._lock:
            return list(self._cache.keys())


class CompilationCache(SandboxCache):
    """Cache for ML compilation results."""

    def __init__(self, max_size: int = 500, default_ttl: float = 1800.0):  # 30 minutes
        super().__init__(max_size, default_ttl)

    def get_compilation_key(
        self, ml_code: str, capabilities: list[CapabilityToken] | None = None
    ) -> str:
        """Generate cache key for ML code compilation."""
        # Hash ML code
        code_hash = hashlib.sha256(ml_code.encode("utf-8")).hexdigest()[:16]

        # Hash capabilities if present
        if capabilities:
            cap_data = []
            for token in capabilities:
                cap_data.append(
                    {
                        "type": token.capability_type,
                        "patterns": getattr(token, "patterns", []),
                        "operations": list(getattr(token, "operations", [])),
                        "hosts": getattr(token, "hosts", []),
                        "ports": getattr(token, "ports", []),
                    }
                )

            cap_str = json.dumps(cap_data, sort_keys=True)
            cap_hash = hashlib.sha256(cap_str.encode("utf-8")).hexdigest()[:8]
            return f"compile_{code_hash}_{cap_hash}"
        else:
            return f"compile_{code_hash}"

    def cache_compilation(
        self,
        ml_code: str,
        python_code: str,
        capabilities: list[CapabilityToken] | None = None,
        source_map: dict[str, Any] | None = None,
    ) -> str:
        """Cache compilation result."""
        key = self.get_compilation_key(ml_code, capabilities)

        value = {
            "python_code": python_code,
            "source_map": source_map,
            "compilation_time": time.time(),
        }

        metadata = {
            "ml_code_length": len(ml_code),
            "python_code_length": len(python_code),
            "has_source_map": source_map is not None,
            "capability_count": len(capabilities) if capabilities else 0,
        }

        self.put(key, value, metadata=metadata)
        return key

    def get_compilation(
        self, ml_code: str, capabilities: list[CapabilityToken] | None = None
    ) -> tuple[str, dict[str, Any] | None] | None:
        """Get cached compilation result."""
        key = self.get_compilation_key(ml_code, capabilities)
        result = self.get(key)

        if result is None:
            return None

        return result["python_code"], result.get("source_map")


class ExecutionCache(SandboxCache):
    """Cache for sandbox execution results."""

    def __init__(self, max_size: int = 200, default_ttl: float = 600.0):  # 10 minutes
        super().__init__(max_size, default_ttl)

    def get_execution_key(self, python_code: str, context: CapabilityContext | None = None) -> str:
        """Generate cache key for execution."""
        # Hash Python code
        code_hash = hashlib.sha256(python_code.encode("utf-8")).hexdigest()[:16]

        # Hash capability context if present
        if context:
            context_data = {
                "capabilities": {
                    cap_type: {
                        "type": token.capability_type,
                        "patterns": getattr(token, "patterns", []),
                        "operations": list(getattr(token, "operations", [])),
                        "hosts": getattr(token, "hosts", []),
                        "ports": getattr(token, "ports", []),
                    }
                    for cap_type, token in context.get_all_capabilities().items()
                }
            }

            context_str = json.dumps(context_data, sort_keys=True)
            context_hash = hashlib.sha256(context_str.encode("utf-8")).hexdigest()[:8]
            return f"exec_{code_hash}_{context_hash}"
        else:
            return f"exec_{code_hash}"

    def cache_execution(
        self,
        python_code: str,
        result: Any,
        context: CapabilityContext | None = None,
        execution_time: float = 0.0,
    ) -> str:
        """Cache execution result (only if successful and deterministic)."""
        # Only cache simple, deterministic results
        if not self._is_cacheable_result(result):
            return ""

        key = self.get_execution_key(python_code, context)

        value = {"result": result, "execution_time": execution_time, "cached_at": time.time()}

        metadata = {
            "python_code_length": len(python_code),
            "result_type": type(result).__name__,
            "is_deterministic": True,
        }

        self.put(key, value, metadata=metadata)
        return key

    def get_execution(
        self, python_code: str, context: CapabilityContext | None = None
    ) -> Any | None:
        """Get cached execution result."""
        key = self.get_execution_key(python_code, context)
        result = self.get(key)

        if result is None:
            return None

        return result["result"]

    def _is_cacheable_result(self, result: Any) -> bool:
        """Check if result is safe to cache."""
        # Only cache simple types for now
        cacheable_types = (int, float, str, bool, list, tuple, dict, type(None))

        if not isinstance(result, cacheable_types):
            return False

        # Don't cache very large results
        try:
            if len(pickle.dumps(result)) > 1024 * 1024:  # 1MB limit
                return False
        except (pickle.PicklingError, TypeError):
            return False

        return True


class PersistentCache:
    """Persistent cache that survives process restarts."""

    def __init__(self, cache_dir: str = None, name: str = "sandbox_cache"):
        """Initialize persistent cache."""
        if cache_dir is None:
            cache_dir = Path.home() / ".mlpy" / "cache"

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.name = name
        self.cache_file = self.cache_dir / f"{name}.json"
        self._memory_cache = SandboxCache(max_size=100)
        self._lock = threading.Lock()

        # Load existing cache
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Load cache from disk."""
        if not self.cache_file.exists():
            return

        try:
            with open(self.cache_file, encoding="utf-8") as f:
                data = json.load(f)

            for key, entry_data in data.items():
                entry = CacheEntry(**entry_data)
                if not entry.is_expired(3600.0):  # 1 hour default
                    self._memory_cache._cache[key] = entry

        except (json.JSONDecodeError, OSError):
            pass  # Start with empty cache if loading fails

    def _save_to_disk(self) -> None:
        """Save cache to disk."""
        try:
            data = {}
            for key, entry in self._memory_cache._cache.items():
                if not entry.is_expired(3600.0):
                    data[key] = asdict(entry)

            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, default=str, indent=2)

        except (OSError, TypeError):
            pass  # Best effort save

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache."""
        with self._lock:
            return self._memory_cache.get(key, default)

    def put(self, key: str, value: Any, ttl: float | None = None) -> None:
        """Put value in cache."""
        with self._lock:
            self._memory_cache.put(key, value, ttl)
            # Periodically save to disk
            if len(self._memory_cache._cache) % 10 == 0:
                self._save_to_disk()

    def save(self) -> None:
        """Explicitly save cache to disk."""
        with self._lock:
            self._save_to_disk()

    def clear(self) -> None:
        """Clear cache and remove disk file."""
        with self._lock:
            self._memory_cache.clear()
            if self.cache_file.exists():
                try:
                    self.cache_file.unlink()
                except OSError:
                    pass


# Global cache instances
_compilation_cache: CompilationCache | None = None
_execution_cache: ExecutionCache | None = None
_cache_lock = threading.Lock()


def get_compilation_cache() -> CompilationCache:
    """Get global compilation cache."""
    global _compilation_cache
    if _compilation_cache is None:
        with _cache_lock:
            if _compilation_cache is None:
                _compilation_cache = CompilationCache()
    return _compilation_cache


def get_execution_cache() -> ExecutionCache:
    """Get global execution cache."""
    global _execution_cache
    if _execution_cache is None:
        with _cache_lock:
            if _execution_cache is None:
                _execution_cache = ExecutionCache()
    return _execution_cache


def clear_all_caches() -> None:
    """Clear all global caches."""
    global _compilation_cache, _execution_cache
    with _cache_lock:
        if _compilation_cache:
            _compilation_cache.clear()
        if _execution_cache:
            _execution_cache.clear()


def get_cache_stats() -> dict[str, Any]:
    """Get statistics for all caches."""
    return {
        "compilation_cache": get_compilation_cache().get_stats(),
        "execution_cache": get_execution_cache().get_stats(),
    }
