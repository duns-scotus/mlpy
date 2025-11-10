"""Structured logging module for ML.

This module provides structured logging capabilities with support for
multiple log levels, formatting options, and output destinations.

Example:
    import log;

    log.info("Application started");
    log.warn("Cache miss", {key: "user_123"});
    log.error("Connection failed", {error: "Timeout"});
"""

import logging
import json
import sys
from datetime import datetime
from typing import Any, Optional, Dict
from mlpy.stdlib.decorators import ml_module, ml_function, ml_class


@ml_class(description="Named logger instance with configurable formatting and outputs")
class Logger:
    """Named logger instance with configurable formatting and outputs."""

    def __init__(self, name: str = "default", level: str = "INFO",
                 format_type: str = "text"):
        """
        Initialize named logger.

        Args:
            name: Logger name for identification
            level: Log level (DEBUG, INFO, WARN, ERROR, CRITICAL)
            format_type: Output format ("text" or "json")
        """
        self.name = name
        self._logger = logging.getLogger(f"ml.{name}")
        self._logger.propagate = False  # Don't propagate to root logger
        self._set_level(level)
        self.format_type = format_type
        self.include_timestamp = True
        self._current_level = "INFO"

        # Setup console handler if not already configured
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(self._get_formatter())
            # Force all log levels to stdout (not stderr)
            handler.setLevel(logging.DEBUG)
            self._logger.addHandler(handler)

    def _set_level(self, level: str):
        """Set logging level from string."""
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARN": logging.WARNING,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        self._logger.setLevel(level_map.get(level.upper(), logging.INFO))

    def _get_formatter(self) -> logging.Formatter:
        """Get log formatter based on format type."""
        if self.format_type == "json":
            # JSON format uses custom formatting
            return logging.Formatter('%(message)s')
        else:
            # Text format with timestamp and level
            return logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')

    def _format_message(self, message: str, data: Optional[Dict[str, Any]] = None) -> str:
        """
        Format log message with optional structured data.

        Args:
            message: Primary log message
            data: Optional dictionary of structured data

        Returns:
            Formatted message string
        """
        if self.format_type == "json":
            log_entry = {
                "message": message,
                "level": self._current_level,
                "logger": self.name
            }
            if self.include_timestamp:
                log_entry["timestamp"] = datetime.utcnow().isoformat() + "Z"
            if data:
                log_entry["data"] = data
            return json.dumps(log_entry)
        else:
            # Text format with inline data
            if data:
                data_str = " | " + ", ".join(f"{k}={v}" for k, v in data.items())
                return message + data_str
            return message

    def debug(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log debug level message."""
        self._current_level = "DEBUG"
        self._logger.debug(self._format_message(message, data))

    def info(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log info level message."""
        self._current_level = "INFO"
        self._logger.info(self._format_message(message, data))

    def warn(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log warning level message."""
        self._current_level = "WARN"
        self._logger.warning(self._format_message(message, data))

    def error(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log error level message."""
        self._current_level = "ERROR"
        self._logger.error(self._format_message(message, data))

    def critical(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Log critical level message."""
        self._current_level = "CRITICAL"
        self._logger.critical(self._format_message(message, data))

    def is_debug(self) -> bool:
        """Check if debug logging is enabled."""
        return self._logger.isEnabledFor(logging.DEBUG)

    def set_level(self, level: str):
        """Change logging level."""
        self._set_level(level)

    def add_file(self, file_path: str):
        """
        Add file output handler.

        Args:
            file_path: Path to log file
        """
        handler = logging.FileHandler(file_path, mode='a', encoding='utf-8')
        handler.setFormatter(self._get_formatter())
        self._logger.addHandler(handler)

    def set_format(self, format_type: str):
        """
        Set log format.

        Args:
            format_type: "text" or "json"
        """
        self.format_type = format_type
        formatter = self._get_formatter()
        for handler in self._logger.handlers:
            handler.setFormatter(formatter)

    def set_timestamp(self, enabled: bool):
        """Enable or disable timestamps in logs."""
        self.include_timestamp = enabled


@ml_module(
    name="log",
    description="Structured logging with levels, formatting, and multiple outputs",
    capabilities=["log.write", "file.write"],
    version="1.0.0"
)
class Log:
    """Logging operations for ML programs."""

    def __init__(self):
        """Initialize logging module with default logger."""
        self._default_logger = Logger("default")

    @ml_function(
        description="Log debug level message",
        capabilities=["log.write"]
    )
    def debug(self, message: str, data: Optional[Dict[str, Any]] = None):
        """
        Log debug level message.

        Args:
            message: Log message
            data: Optional structured data dictionary
        """
        self._default_logger.debug(message, data)

    @ml_function(
        description="Log info level message",
        capabilities=["log.write"]
    )
    def info(self, message: str, data: Optional[Dict[str, Any]] = None):
        """
        Log info level message.

        Args:
            message: Log message
            data: Optional structured data dictionary
        """
        self._default_logger.info(message, data)

    @ml_function(
        description="Log warning message",
        capabilities=["log.write"]
    )
    def warn(self, message: str, data: Optional[Dict[str, Any]] = None):
        """
        Log warning level message.

        Args:
            message: Log message
            data: Optional structured data dictionary
        """
        self._default_logger.warn(message, data)

    @ml_function(
        description="Log error message",
        capabilities=["log.write"]
    )
    def error(self, message: str, data: Optional[Dict[str, Any]] = None):
        """
        Log error level message.

        Args:
            message: Log message
            data: Optional structured data dictionary
        """
        self._default_logger.error(message, data)

    @ml_function(
        description="Log critical message",
        capabilities=["log.write"]
    )
    def critical(self, message: str, data: Optional[Dict[str, Any]] = None):
        """
        Log critical level message.

        Args:
            message: Log message
            data: Optional structured data dictionary
        """
        self._default_logger.critical(message, data)

    @ml_function(
        description="Set logging level",
        capabilities=["log.write"]
    )
    def set_level(self, level: str):
        """
        Set logging level.

        Args:
            level: Log level (DEBUG, INFO, WARN, ERROR, CRITICAL)
        """
        self._default_logger.set_level(level)

    @ml_function(
        description="Set log output format",
        capabilities=["log.write"]
    )
    def set_format(self, format_type: str):
        """
        Set log output format.

        Args:
            format_type: "text" or "json"
        """
        self._default_logger.set_format(format_type)

    @ml_function(
        description="Add file output destination",
        capabilities=["log.write", "file.write"]
    )
    def add_file(self, file_path: str):
        """
        Add file logging output.

        Args:
            file_path: Path to log file
        """
        self._default_logger.add_file(file_path)

    @ml_function(
        description="Enable or disable timestamps",
        capabilities=["log.write"]
    )
    def set_timestamp(self, enabled: bool):
        """
        Enable or disable timestamps in logs.

        Args:
            enabled: True to include timestamps
        """
        self._default_logger.set_timestamp(enabled)

    @ml_function(
        description="Check if debug logging is enabled",
        capabilities=[]
    )
    def is_debug(self) -> bool:
        """
        Check if debug logging is enabled.

        Returns:
            True if debug level is active
        """
        return self._default_logger.is_debug()

    @ml_function(
        description="Create named logger instance",
        capabilities=[]
    )
    def create_logger(self, name: str) -> Logger:
        """
        Create named logger instance.

        Args:
            name: Logger name

        Returns:
            New Logger instance
        """
        return Logger(name)


# Module singleton instance
log = Log()
