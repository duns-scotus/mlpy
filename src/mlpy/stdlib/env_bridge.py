"""Environment variable access module for ML.

This module provides functions for reading and writing environment variables,
essential for configuration management and secret handling in ML applications.

Required Capabilities:
    - env.read: Read environment variables (may expose secrets)
    - env.write: Modify environment variables (affects process state)

Example:
    ```ml
    import env;

    // Read with default
    api_key = env.get("API_KEY", "default-key");

    // Get required variable (throws if missing)
    db_url = env.require("DATABASE_URL");

    // Type conversion
    port = env.get_int("PORT", 8080);
    debug = env.get_bool("DEBUG", false);
    ```
"""

import os
from typing import Optional

from mlpy.stdlib.decorators import ml_module, ml_function


@ml_module(
    name="env",
    description="Environment variable access and management",
    capabilities=["env.read", "env.write"],
    version="1.0.0"
)
class Env:
    """Environment variable operations."""

    @ml_function(description="Get environment variable", capabilities=["env.read"])
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get environment variable with optional default.

        Args:
            key: Variable name
            default: Default value if not set

        Returns:
            Variable value or default (None if not set and no default)

        Example:
            ```ml
            api_url = env.get("API_URL", "https://api.example.com");
            ```
        """
        return os.environ.get(key, default)

    @ml_function(description="Get required environment variable", capabilities=["env.read"])
    def require(self, key: str) -> str:
        """Get environment variable or raise error if missing.

        Args:
            key: Variable name

        Returns:
            Variable value

        Raises:
            RuntimeError: If variable not set

        Example:
            ```ml
            db_url = env.require("DATABASE_URL");
            ```
        """
        value = os.environ.get(key)
        if value is None:
            raise RuntimeError(f"Required environment variable not set: {key}")
        return value

    @ml_function(description="Set environment variable", capabilities=["env.write"])
    def set(self, key: str, value: str) -> None:
        """Set environment variable.

        Args:
            key: Variable name
            value: Variable value (converted to string)

        Example:
            ```ml
            env.set("DEBUG", "true");
            ```
        """
        os.environ[key] = str(value)

    @ml_function(description="Check if variable exists", capabilities=["env.read"])
    def has(self, key: str) -> bool:
        """Check if environment variable is set.

        Args:
            key: Variable name

        Returns:
            True if variable exists, False otherwise

        Example:
            ```ml
            if (env.has("API_KEY")) {
                api_key = env.get("API_KEY");
            }
            ```
        """
        return key in os.environ

    @ml_function(description="Get all environment variables", capabilities=["env.read"])
    def all(self) -> dict[str, str]:
        """Get all environment variables as dictionary.

        Returns:
            Dictionary of all environment variables

        Security Warning:
            This may expose sensitive data. Use with caution.

        Example:
            ```ml
            all_vars = env.all();
            ```
        """
        return dict(os.environ)

    @ml_function(description="Delete environment variable", capabilities=["env.write"])
    def delete(self, key: str) -> None:
        """Delete environment variable if it exists.

        Args:
            key: Variable name

        Example:
            ```ml
            env.delete("TEMP_VAR");
            ```
        """
        os.environ.pop(key, None)

    @ml_function(description="Get integer environment variable", capabilities=["env.read"])
    def get_int(self, key: str, default: int = 0) -> int:
        """Get environment variable as integer.

        Args:
            key: Variable name
            default: Default value if not set or invalid

        Returns:
            Integer value or default

        Example:
            ```ml
            port = env.get_int("PORT", 8080);
            max_retries = env.get_int("MAX_RETRIES", 3);
            ```
        """
        value = os.environ.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default

    @ml_function(description="Get boolean environment variable", capabilities=["env.read"])
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get environment variable as boolean.

        Treats "true", "1", "yes", "on" as True (case-insensitive).
        All other values are treated as False.

        Args:
            key: Variable name
            default: Default value if not set

        Returns:
            Boolean value or default

        Example:
            ```ml
            debug = env.get_bool("DEBUG", false);
            cache_enabled = env.get_bool("CACHE_ENABLED", true);
            ```
        """
        value = os.environ.get(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")

    @ml_function(description="Get float environment variable", capabilities=["env.read"])
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get environment variable as float.

        Args:
            key: Variable name
            default: Default value if not set or invalid

        Returns:
            Float value or default

        Example:
            ```ml
            timeout = env.get_float("TIMEOUT", 30.0);
            rate_limit = env.get_float("RATE_LIMIT", 100.0);
            ```
        """
        value = os.environ.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError:
            return default


# Create singleton instance for module-level access
env = Env()
