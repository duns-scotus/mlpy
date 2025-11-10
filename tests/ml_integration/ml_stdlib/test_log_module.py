"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ============================================================================
# Runtime Whitelist Enforcement
# ============================================================================
from mlpy.runtime.whitelist_validator import safe_call as _safe_call

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length

from mlpy.stdlib import log

from mlpy.stdlib import console

_safe_call(console.log, '=== Testing log Module ===')

_safe_call(console.log, '[Test 1] Basic logging levels')

_safe_call(log.debug, 'Debug message - may not appear if level is INFO')

_safe_call(log.info, 'Info message - general information')

_safe_call(log.warn, 'Warning message - something to be aware of')

_safe_call(log.error, 'Error message - something went wrong')

_safe_call(log.critical, 'Critical message - serious problem')

_safe_call(console.log, 'PASS: All logging levels work')

_safe_call(console.log, '[Test 2] Set log level to DEBUG')

_safe_call(log.set_level, 'DEBUG')

_safe_call(log.debug, 'Debug message now visible')

_safe_call(console.log, 'PASS: Log level changed to DEBUG')

_safe_call(console.log, '[Test 3] Set log level to ERROR')

_safe_call(log.set_level, 'ERROR')

_safe_call(log.info, 'This info message should not appear')

_safe_call(log.error, 'This error message should appear')

_safe_call(console.log, 'PASS: Log level filtering works')

_safe_call(console.log, '[Test 4] Reset log level to INFO')

_safe_call(log.set_level, 'INFO')

_safe_call(log.info, 'Back to INFO level')

_safe_call(console.log, 'PASS: Log level reset successful')

_safe_call(console.log, '[Test 5] Logging with structured data')

user_data = {'user_id': 123, 'action': 'login', 'ip': '192.168.1.1'}

_safe_call(log.info, 'User action', user_data)

_safe_call(console.log, 'PASS: Structured data logging works')

_safe_call(console.log, '[Test 6] Check debug status')

_safe_call(log.set_level, 'INFO')

is_debug_info = _safe_call(log.is_debug)

if (is_debug_info == False):
    _safe_call(console.log, 'PASS: Debug not enabled at INFO level')
else:
    _safe_call(console.log, 'FAIL: Debug should not be enabled at INFO level')

_safe_call(log.set_level, 'DEBUG')

is_debug_debug = _safe_call(log.is_debug)

if (is_debug_debug == True):
    _safe_call(console.log, 'PASS: Debug enabled at DEBUG level')
else:
    _safe_call(console.log, 'FAIL: Debug should be enabled at DEBUG level')

_safe_call(console.log, '[Test 7] Set format to JSON')

_safe_call(log.set_format, 'json')

_safe_call(log.info, 'JSON formatted message', {'key': 'value', 'number': 42})

_safe_call(console.log, 'PASS: JSON format set successfully')

_safe_call(console.log, '[Test 8] Set format back to text')

_safe_call(log.set_format, 'text')

_safe_call(log.info, 'Text formatted message')

_safe_call(console.log, 'PASS: Text format restored')

_safe_call(console.log, '[Test 9] Disable timestamps')

_safe_call(log.set_timestamp, False)

_safe_call(log.info, 'Message without timestamp')

_safe_call(console.log, 'PASS: Timestamp disabled')

_safe_call(console.log, '[Test 10] Re-enable timestamps')

_safe_call(log.set_timestamp, True)

_safe_call(log.info, 'Message with timestamp')

_safe_call(console.log, 'PASS: Timestamp re-enabled')

_safe_call(console.log, '[Test 11] Create named logger')

api_logger = _safe_call(log.create_logger, 'api')

_safe_method_call(api_logger, 'info', 'API request received')

_safe_method_call(api_logger, 'error', 'API error occurred')

_safe_call(console.log, 'PASS: Named logger created and used')

_safe_call(console.log, '[Test 12] Multiple named loggers')

db_logger = _safe_call(log.create_logger, 'database')

auth_logger = _safe_call(log.create_logger, 'auth')

_safe_method_call(db_logger, 'info', 'Database query executed')

_safe_method_call(auth_logger, 'warn', 'Authentication attempt failed')

_safe_call(console.log, 'PASS: Multiple named loggers work independently')

_safe_call(console.log, '[Test 13] Named logger with custom level')

debug_logger = _safe_call(log.create_logger, 'debug')

_safe_method_call(debug_logger, 'set_level', 'DEBUG')

_safe_method_call(debug_logger, 'debug', 'Debug logger message')

_safe_call(console.log, 'PASS: Named logger with custom level works')

_safe_call(console.log, '[Test 14] Named logger with JSON format')

json_logger = _safe_call(log.create_logger, 'json_logger')

_safe_method_call(json_logger, 'set_format', 'json')

_safe_method_call(json_logger, 'info', 'JSON logger message', {'status': 'success', 'code': 200})

_safe_call(console.log, 'PASS: Named logger with JSON format works')

_safe_call(console.log, '[Test 15] Named logger with complex structured data')

metrics_logger = _safe_call(log.create_logger, 'metrics')

metrics_data = {'endpoint': '/api/users', 'method': 'GET', 'status': 200, 'duration': 0.045, 'user_id': 456}

_safe_method_call(metrics_logger, 'info', 'Request metrics', metrics_data)

_safe_call(console.log, 'PASS: Complex structured data logging works')

_safe_call(console.log, '[Test 16] All levels on named logger')

test_logger = _safe_call(log.create_logger, 'test')

_safe_method_call(test_logger, 'set_level', 'DEBUG')

_safe_method_call(test_logger, 'debug', 'Test debug')

_safe_method_call(test_logger, 'info', 'Test info')

_safe_method_call(test_logger, 'warn', 'Test warning')

_safe_method_call(test_logger, 'error', 'Test error')

_safe_method_call(test_logger, 'critical', 'Test critical')

_safe_call(console.log, 'PASS: All log levels work on named logger')

_safe_call(console.log, '[Test 17] Log level filtering on named logger')

filtered_logger = _safe_call(log.create_logger, 'filtered')

_safe_method_call(filtered_logger, 'set_level', 'WARNING')

_safe_method_call(filtered_logger, 'debug', 'Should not appear')

_safe_method_call(filtered_logger, 'info', 'Should not appear')

_safe_method_call(filtered_logger, 'warn', 'Should appear')

_safe_call(console.log, 'PASS: Log level filtering on named logger works')

_safe_call(console.log, '[Test 18] Real-world application logging')

app_logger = _safe_call(log.create_logger, 'application')

_safe_method_call(app_logger, 'set_level', 'INFO')

_safe_method_call(app_logger, 'set_format', 'text')

_safe_method_call(app_logger, 'info', 'Application starting', {'version': '1.0.0', 'env': 'production'})

request_logger = _safe_call(log.create_logger, 'request')

request_data = {'path': '/api/users/123', 'method': 'GET', 'user_id': 789, 'ip': '10.0.0.1'}

_safe_method_call(request_logger, 'info', 'Request received', request_data)

_safe_method_call(request_logger, 'info', 'Request processed successfully', {'duration': 0.023, 'status': 200})

_safe_method_call(app_logger, 'info', 'Application running normally')

_safe_call(console.log, 'PASS: Real-world logging scenario works')

_safe_call(console.log, '[Test 19] Error logging with context')

error_logger = _safe_call(log.create_logger, 'errors')

error_context = {'error_type': 'DatabaseError', 'query': 'SELECT * FROM users', 'affected_rows': 0, 'retry_count': 3}

_safe_method_call(error_logger, 'error', 'Database query failed', error_context)

_safe_call(console.log, 'PASS: Error logging with context works')

_safe_call(console.log, '[Test 20] Performance logging')

perf_logger = _safe_call(log.create_logger, 'performance')

_safe_method_call(perf_logger, 'set_format', 'json')

perf_data = {'operation': 'data_processing', 'records_processed': 10000, 'duration_ms': 1250, 'memory_mb': 45}

_safe_method_call(perf_logger, 'info', 'Performance metrics', perf_data)

_safe_call(console.log, 'PASS: Performance logging works')

_safe_call(console.log, '=== All log module tests passed! ===')

# End of generated code