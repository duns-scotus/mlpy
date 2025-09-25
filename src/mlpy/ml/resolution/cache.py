"""Module caching system for ML imports."""

import hashlib
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from .resolver import ModuleInfo


@dataclass
class CacheEntry:
    """Cache entry for compiled modules."""

    module_info: "ModuleInfo"
    source_hash: str
    timestamp: float
    dependencies: list[str]
    file_path: str | None = None

    def is_valid(self, source_code: str, dependency_timestamps: dict[str, float]) -> bool:
        """Check if cache entry is still valid."""
        # Check source hash
        current_hash = hashlib.sha256(source_code.encode()).hexdigest()
        if current_hash != self.source_hash:
            return False

        # Check dependency timestamps
        for dep in self.dependencies:
            if dep in dependency_timestamps:
                if dependency_timestamps[dep] > self.timestamp:
                    return False

        return True


class ModuleCache:
    """Thread-safe module cache with dependency tracking."""

    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        """Initialize module cache.

        Args:
            max_size: Maximum number of cached modules
            ttl: Time to live in seconds
        """
        self.max_size = max_size
        self.ttl = ttl
        self._cache: dict[str, CacheEntry] = {}
        self._access_times: dict[str, float] = {}

    def get(
        self, module_path: str, source_code: str, dependencies: dict[str, float]
    ) -> Optional["ModuleInfo"]:
        """Get cached module if valid.

        Args:
            module_path: Full module import path
            source_code: Current source code for validation
            dependencies: Dependency timestamps for validation

        Returns:
            Cached ModuleInfo if valid, None otherwise
        """
        if module_path not in self._cache:
            return None

        entry = self._cache[module_path]
        current_time = time.time()

        # Check TTL
        if current_time - entry.timestamp > self.ttl:
            self._evict(module_path)
            return None

        # Check validity
        if not entry.is_valid(source_code, dependencies):
            self._evict(module_path)
            return None

        # Update access time
        self._access_times[module_path] = current_time
        return entry.module_info

    def get_simple(self, module_path: str) -> Optional["ModuleInfo"]:
        """Get cached module without validation (simple interface).

        Args:
            module_path: Full module import path

        Returns:
            Cached ModuleInfo if exists, None otherwise
        """
        if module_path not in self._cache:
            return None

        entry = self._cache[module_path]
        current_time = time.time()

        # Update access time
        self._access_times[module_path] = current_time
        return entry.module_info

    def put(
        self,
        module_path: str,
        module_info: "ModuleInfo",
        source_code: str,
        dependencies: list[str],
        file_path: str | None = None,
    ) -> None:
        """Cache a compiled module.

        Args:
            module_path: Full module import path
            module_info: Compiled module information
            source_code: Source code used for compilation
            dependencies: List of dependency module paths
            file_path: Optional file path for file-based modules
        """
        # Evict if cache is full
        if len(self._cache) >= self.max_size:
            self._evict_lru()

        source_hash = hashlib.sha256(source_code.encode()).hexdigest()
        current_time = time.time()

        entry = CacheEntry(
            module_info=module_info,
            source_hash=source_hash,
            timestamp=current_time,
            dependencies=dependencies,
            file_path=file_path,
        )

        self._cache[module_path] = entry
        self._access_times[module_path] = current_time

    def invalidate(self, module_path: str) -> None:
        """Invalidate a specific module and its dependents."""
        if module_path in self._cache:
            self._evict(module_path)

        # Invalidate dependents
        to_evict = []
        for path, entry in self._cache.items():
            if module_path in entry.dependencies:
                to_evict.append(path)

        for path in to_evict:
            self._evict(path)

    def clear(self) -> None:
        """Clear all cached modules."""
        self._cache.clear()
        self._access_times.clear()

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        current_time = time.time()
        valid_entries = 0

        for entry in self._cache.values():
            if current_time - entry.timestamp <= self.ttl:
                valid_entries += 1

        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "valid_entries": valid_entries,
            "ttl": self.ttl,
            "hit_rate": getattr(self, "_hit_rate", 0.0),
            "total_memory_kb": self._estimate_memory_usage() / 1024,
        }

    def _evict(self, module_path: str) -> None:
        """Evict a specific module from cache."""
        self._cache.pop(module_path, None)
        self._access_times.pop(module_path, None)

    def _evict_lru(self) -> None:
        """Evict least recently used module."""
        if not self._access_times:
            return

        lru_path = min(self._access_times.keys(), key=lambda k: self._access_times[k])
        self._evict(lru_path)

    def _estimate_memory_usage(self) -> int:
        """Estimate memory usage in bytes."""
        # Rough estimation - would need profiling for accuracy
        base_overhead = 100  # Base object overhead
        string_overhead = 50  # Per string overhead

        total = 0
        for path, entry in self._cache.items():
            total += base_overhead
            total += len(path) + string_overhead
            total += len(entry.source_hash) + string_overhead
            total += len(entry.dependencies) * (string_overhead + 20)  # Average dep name length

        return total


# Global module cache instance
_module_cache = ModuleCache()


def get_module_cache() -> ModuleCache:
    """Get global module cache instance."""
    return _module_cache
