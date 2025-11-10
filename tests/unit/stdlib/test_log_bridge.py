"""Unit tests for log_bridge module."""

import os
import tempfile
import logging
import json
import pytest
from io import StringIO

from mlpy.stdlib.log_bridge import Log, Logger


class TestLoggerClass:
    """Test suite for Logger class."""

    def setup_method(self):
        """Setup for each test method."""
        # Reset logging for each test
        for logger_name in list(logging.Logger.manager.loggerDict.keys()):
            if logger_name.startswith('ml.'):
                logger = logging.getLogger(logger_name)
                logger.handlers.clear()
                logger.setLevel(logging.NOTSET)

    def test_logger_initialization(self):
        """Test logger initialization with defaults."""
        logger = Logger("test")
        assert logger.name == "test"
        assert logger.format_type == "text"
        assert logger.include_timestamp is True

    def test_logger_custom_level(self):
        """Test logger with custom log level."""
        logger = Logger("test", level="DEBUG")
        assert logger.is_debug() is True

        logger2 = Logger("test2", level="ERROR")
        assert logger2.is_debug() is False

    def test_logger_debug(self, capsys):
        """Test debug level logging."""
        logger = Logger("test", level="DEBUG")
        logger.debug("Debug message")

        captured = capsys.readouterr()
        assert "DEBUG" in captured.out
        assert "Debug message" in captured.out

    def test_logger_info(self, capsys):
        """Test info level logging."""
        logger = Logger("test")
        logger.info("Info message")

        captured = capsys.readouterr()
        assert "INFO" in captured.out
        assert "Info message" in captured.out

    def test_logger_warn(self, capsys):
        """Test warning level logging."""
        logger = Logger("test")
        logger.warn("Warning message")

        captured = capsys.readouterr()
        assert "WARNING" in captured.out
        assert "Warning message" in captured.out

    def test_logger_error(self, capsys):
        """Test error level logging."""
        logger = Logger("test")
        logger.error("Error message")

        captured = capsys.readouterr()
        assert "ERROR" in captured.out
        assert "Error message" in captured.out

    def test_logger_critical(self, capsys):
        """Test critical level logging."""
        logger = Logger("test")
        logger.critical("Critical message")

        captured = capsys.readouterr()
        assert "CRITICAL" in captured.out
        assert "Critical message" in captured.out

    def test_logger_with_structured_data(self, capsys):
        """Test logging with structured data."""
        logger = Logger("test")
        logger.info("User login", {"user_id": 123, "ip": "192.168.1.1"})

        captured = capsys.readouterr()
        assert "User login" in captured.out
        assert "user_id=123" in captured.out
        assert "ip=192.168.1.1" in captured.out

    def test_logger_json_format(self, capsys):
        """Test JSON format logging."""
        logger = Logger("test", format_type="json")
        logger.info("Test message", {"key": "value"})

        captured = capsys.readouterr()
        log_entry = json.loads(captured.out.strip())

        assert log_entry["message"] == "Test message"
        assert log_entry["level"] == "INFO"
        assert log_entry["logger"] == "test"
        assert log_entry["data"]["key"] == "value"
        assert "timestamp" in log_entry

    def test_logger_set_level(self, capsys):
        """Test changing log level."""
        logger = Logger("test", level="INFO")
        logger.debug("Should not appear")
        captured = capsys.readouterr()
        assert captured.out == ""

        logger.set_level("DEBUG")
        logger.debug("Should appear")
        captured = capsys.readouterr()
        assert "Should appear" in captured.out

    def test_logger_is_debug(self):
        """Test debug level checking."""
        logger = Logger("test", level="INFO")
        assert logger.is_debug() is False

        logger.set_level("DEBUG")
        assert logger.is_debug() is True

    def test_logger_add_file(self):
        """Test file output logging."""
        fd, temp_file = tempfile.mkstemp(suffix='.log', text=True)
        os.close(fd)

        try:
            logger = Logger("test")
            logger.add_file(temp_file)
            logger.info("File log message")

            # Close all handlers before reading file
            for handler in logger._logger.handlers[:]:
                handler.close()
                logger._logger.removeHandler(handler)

            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "INFO" in content
                assert "File log message" in content
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_logger_set_format(self, capsys):
        """Test changing log format."""
        logger = Logger("test", format_type="text")
        logger.info("Text format")
        captured = capsys.readouterr()
        assert "INFO" in captured.out

        logger.set_format("json")
        logger.info("JSON format")
        captured = capsys.readouterr()
        log_entry = json.loads(captured.out.strip())
        assert log_entry["message"] == "JSON format"

    def test_logger_set_timestamp(self, capsys):
        """Test timestamp control."""
        logger = Logger("test", format_type="json")
        logger.set_timestamp(False)
        logger.info("No timestamp")

        captured = capsys.readouterr()
        log_entry = json.loads(captured.out.strip())
        assert "timestamp" not in log_entry

        logger.set_timestamp(True)
        logger.info("With timestamp")

        captured = capsys.readouterr()
        log_entry = json.loads(captured.out.strip())
        assert "timestamp" in log_entry

    def test_logger_level_filtering(self, capsys):
        """Test log level filtering."""
        logger = Logger("test", level="ERROR")

        logger.debug("Debug - should not appear")
        logger.info("Info - should not appear")
        logger.warn("Warn - should not appear")
        logger.error("Error - should appear")

        captured = capsys.readouterr()
        assert "Debug" not in captured.out
        assert "Info" not in captured.out
        assert "Warn" not in captured.out
        assert "Error - should appear" in captured.out


class TestLogModule:
    """Test suite for Log module."""

    def setup_method(self):
        """Setup for each test method."""
        # Reset logging BEFORE creating new Log instance
        for logger_name in list(logging.Logger.manager.loggerDict.keys()):
            if logger_name.startswith('ml.'):
                logger = logging.getLogger(logger_name)
                logger.handlers.clear()
                logger.setLevel(logging.NOTSET)
        # Now create test instance with clean loggers
        self.log_module = Log()
        # Enable propagation for caplog to work
        self.log_module._default_logger._logger.propagate = True

    def test_log_debug(self, caplog):
        """Test module-level debug logging."""
        self.log_module.set_level("DEBUG")

        with caplog.at_level(logging.DEBUG, logger="ml.default"):
            self.log_module.debug("Debug test")

        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "DEBUG"
        assert "Debug test" in caplog.records[0].message

    def test_log_info(self, caplog):
        """Test module-level info logging."""
        with caplog.at_level(logging.INFO, logger="ml.default"):
            self.log_module.info("Info test")

        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "INFO"
        assert "Info test" in caplog.records[0].message

    def test_log_warn(self, caplog):
        """Test module-level warning logging."""
        with caplog.at_level(logging.WARNING, logger="ml.default"):
            self.log_module.warn("Warning test")

        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "WARNING"
        assert "Warning test" in caplog.records[0].message

    def test_log_error(self, caplog):
        """Test module-level error logging."""
        with caplog.at_level(logging.ERROR, logger="ml.default"):
            self.log_module.error("Error test")

        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "ERROR"
        assert "Error test" in caplog.records[0].message

    def test_log_critical(self, caplog):
        """Test module-level critical logging."""
        with caplog.at_level(logging.CRITICAL, logger="ml.default"):
            self.log_module.critical("Critical test")

        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "CRITICAL"
        assert "Critical test" in caplog.records[0].message

    def test_log_with_data(self, caplog):
        """Test logging with structured data."""
        with caplog.at_level(logging.INFO, logger="ml.default"):
            self.log_module.info("Event occurred", {"event_id": 456})

        assert len(caplog.records) == 1
        assert "Event occurred" in caplog.records[0].message
        assert "event_id=456" in caplog.records[0].message

    def test_log_set_level(self, caplog):
        """Test setting log level."""
        # Set logger to ERROR level
        self.log_module.set_level("ERROR")

        # INFO message should not be logged
        self.log_module.info("Should not appear")
        info_records = [r for r in caplog.records if r.levelno == logging.INFO]
        assert len(info_records) == 0

        # ERROR message should be logged
        caplog.clear()
        self.log_module.error("Should appear")
        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) == 1
        assert "Should appear" in error_records[0].message

    def test_log_set_format(self, caplog):
        """Test setting log format."""
        self.log_module.set_format("json")

        with caplog.at_level(logging.INFO, logger="ml.default"):
            self.log_module.info("JSON test")

        # Check that the message was formatted
        assert len(caplog.records) == 1
        # The formatted message should be JSON
        message = caplog.records[0].message
        log_entry = json.loads(message)
        assert log_entry["message"] == "JSON test"
        assert log_entry["level"] == "INFO"

    def test_log_add_file(self):
        """Test adding file output."""
        fd, temp_file = tempfile.mkstemp(suffix='.log', text=True)
        os.close(fd)

        try:
            self.log_module.add_file(temp_file)
            self.log_module.info("File output test")

            # Close all handlers before reading file
            for handler in self.log_module._default_logger._logger.handlers[:]:
                handler.close()
                self.log_module._default_logger._logger.removeHandler(handler)

            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "File output test" in content
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_log_set_timestamp(self, caplog):
        """Test timestamp control."""
        self.log_module.set_format("json")
        self.log_module.set_timestamp(False)

        with caplog.at_level(logging.INFO, logger="ml.default"):
            self.log_module.info("No timestamp")

        message = caplog.records[0].message
        log_entry = json.loads(message)
        assert "timestamp" not in log_entry

    def test_log_is_debug(self):
        """Test debug level checking."""
        self.log_module.set_level("INFO")
        assert self.log_module.is_debug() is False

        self.log_module.set_level("DEBUG")
        assert self.log_module.is_debug() is True

    def test_log_create_logger(self, capsys):
        """Test creating named logger."""
        db_logger = self.log_module.create_logger("database")
        assert isinstance(db_logger, Logger)
        assert db_logger.name == "database"

        db_logger.info("Database query")
        captured = capsys.readouterr()
        assert "Database query" in captured.out

    def test_multiple_named_loggers(self, capsys):
        """Test multiple independent named loggers."""
        api_logger = self.log_module.create_logger("api")
        db_logger = self.log_module.create_logger("database")

        api_logger.set_level("DEBUG")
        db_logger.set_level("ERROR")

        api_logger.debug("API debug")
        captured = capsys.readouterr()
        assert "API debug" in captured.out

        db_logger.debug("DB debug - should not appear")
        captured = capsys.readouterr()
        assert captured.out == ""

        db_logger.error("DB error")
        captured = capsys.readouterr()
        assert "DB error" in captured.out


class TestLogModuleMetadata:
    """Test module metadata and decorators."""

    def test_module_has_metadata(self):
        """Test that module has required metadata."""
        assert hasattr(Log, '_ml_module_metadata')
        metadata = Log._ml_module_metadata

        assert metadata.name == "log"
        assert "log.write" in metadata.capabilities
        assert "file.write" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_function_capabilities(self):
        """Test that functions have correct capability metadata."""
        log_module = Log()

        # Basic logging operations
        assert hasattr(log_module.info, '_ml_function_metadata')
        assert "log.write" in log_module.info._ml_function_metadata.capabilities

        # File operations
        assert hasattr(log_module.add_file, '_ml_function_metadata')
        assert "log.write" in log_module.add_file._ml_function_metadata.capabilities
        assert "file.write" in log_module.add_file._ml_function_metadata.capabilities

        # Read-only operations
        assert hasattr(log_module.is_debug, '_ml_function_metadata')
        assert len(log_module.is_debug._ml_function_metadata.capabilities) == 0
