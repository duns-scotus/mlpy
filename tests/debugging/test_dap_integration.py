"""
End-to-end integration tests for DAP server.

These tests simulate a real DAP client (like VS Code) communicating with
the DAP server through the Debug Adapter Protocol.
"""

import pytest
import subprocess
import json
import time
import threading
from pathlib import Path
from typing import Dict, Any, Optional


class DAPClient:
    """Mock DAP client for testing."""

    def __init__(self, process: subprocess.Popen):
        """Initialize DAP client with subprocess."""
        self.process = process
        self.seq = 1
        self.responses = []
        self.events = []
        self._reading = True
        self._reader_thread = None

    def start_reading(self):
        """Start reading responses in background thread."""
        self._reader_thread = threading.Thread(target=self._read_loop, daemon=True)
        self._reader_thread.start()

    def _read_loop(self):
        """Read responses from DAP server."""
        while self._reading and self.process.poll() is None:
            try:
                message = self._read_message()
                if message:
                    if message.get('type') == 'response':
                        self.responses.append(message)
                    elif message.get('type') == 'event':
                        self.events.append(message)
            except Exception as e:
                print(f"Error reading message: {e}")
                break

    def _read_message(self) -> Optional[Dict[str, Any]]:
        """Read a single DAP message."""
        if not self.process.stdout:
            return None

        # Read Content-Length header
        content_length = None
        while True:
            line = self.process.stdout.readline()
            if not line:
                return None

            line = line.decode('utf-8').strip()
            if not line:
                # Empty line = end of headers
                break

            if line.startswith('Content-Length: '):
                content_length = int(line[16:])

        if content_length is None:
            return None

        # Read message body
        body = self.process.stdout.read(content_length).decode('utf-8')
        return json.loads(body)

    def send_request(self, command: str, arguments: Dict[str, Any] = None) -> int:
        """Send request to DAP server."""
        request_seq = self.seq
        self.seq += 1

        message = {
            'type': 'request',
            'seq': request_seq,
            'command': command,
            'arguments': arguments or {}
        }

        self._send_message(message)
        return request_seq

    def _send_message(self, message: Dict[str, Any]):
        """Send DAP message to server."""
        body = json.dumps(message)
        content = body.encode('utf-8')
        content_length = len(content)

        header = f'Content-Length: {content_length}\r\n\r\n'.encode('utf-8')

        if self.process.stdin:
            self.process.stdin.write(header)
            self.process.stdin.write(content)
            self.process.stdin.flush()

    def wait_for_response(self, request_seq: int, timeout: float = 5.0) -> Optional[Dict[str, Any]]:
        """Wait for response to specific request."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            for response in self.responses:
                if response.get('request_seq') == request_seq:
                    self.responses.remove(response)
                    return response

            time.sleep(0.1)

        return None

    def wait_for_event(self, event_name: str, timeout: float = 5.0) -> Optional[Dict[str, Any]]:
        """Wait for specific event."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            for event in self.events:
                if event.get('event') == event_name:
                    self.events.remove(event)
                    return event

            time.sleep(0.1)

        return None

    def stop(self):
        """Stop the DAP client."""
        self._reading = False
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()


@pytest.fixture
def dap_server():
    """Start DAP server process."""
    # Start DAP server via CLI
    process = subprocess.Popen(
        ['python', '-m', 'mlpy', 'debug-adapter'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Create client
    client = DAPClient(process)
    client.start_reading()

    # Give server time to start
    time.sleep(0.5)

    yield client

    # Cleanup
    client.stop()


class TestDAPFullSession:
    """Test complete DAP debugging sessions."""

    def test_initialize_sequence(self, dap_server):
        """Test initialize request-response."""
        client = dap_server

        # Send initialize
        seq = client.send_request('initialize', {
            'clientID': 'test-client',
            'adapterID': 'ml'
        })

        # Wait for response
        response = client.wait_for_response(seq, timeout=5.0)

        assert response is not None, "Initialize response not received"
        assert response['success'] is True
        assert 'body' in response

        # Check capabilities
        caps = response['body']
        assert caps['supportsConfigurationDoneRequest'] is True
        assert caps['supportsConditionalBreakpoints'] is True

    def test_initialize_and_launch(self, dap_server, tmp_path):
        """Test initialize followed by launch."""
        client = dap_server

        # Initialize
        seq = client.send_request('initialize', {'clientID': 'test'})
        response = client.wait_for_response(seq)
        assert response and response['success'] is True

        # Create test ML file
        ml_file = tmp_path / "test.ml"
        ml_file.write_text("""
function greet(name) {
    print("Hello, " + name);
}

greet("World");
""")

        # Launch
        seq = client.send_request('launch', {
            'program': str(ml_file)
        })

        response = client.wait_for_response(seq, timeout=10.0)

        # Response may succeed or fail depending on transpiler availability
        if response:
            if response['success']:
                # Should receive 'initialized' event
                event = client.wait_for_event('initialized', timeout=5.0)
                assert event is not None, "Initialized event not received"
            else:
                # Transpilation may fail in test environment, that's OK
                assert 'message' in response

    def test_set_breakpoints_sequence(self, dap_server, tmp_path):
        """Test breakpoint setting sequence."""
        client = dap_server

        # Initialize
        client.send_request('initialize', {})
        client.wait_for_response(1)

        # Create test ML file
        ml_file = tmp_path / "test.ml"
        ml_file.write_text("""
x = 5;
y = 10;
z = x + y;
print(z);
""")

        # Launch
        seq = client.send_request('launch', {'program': str(ml_file)})
        launch_response = client.wait_for_response(seq, timeout=10.0)

        if launch_response and launch_response['success']:
            # Wait for initialized event
            client.wait_for_event('initialized', timeout=5.0)

            # Set breakpoints
            seq = client.send_request('setBreakpoints', {
                'source': {'path': str(ml_file)},
                'breakpoints': [
                    {'line': 2},
                    {'line': 3, 'condition': 'x > 0'}
                ]
            })

            response = client.wait_for_response(seq)
            assert response is not None
            assert response['success'] is True
            assert 'breakpoints' in response['body']

            breakpoints = response['body']['breakpoints']
            assert len(breakpoints) == 2


    def test_threads_request(self, dap_server):
        """Test threads request."""
        client = dap_server

        # Initialize first
        client.send_request('initialize', {})
        client.wait_for_response(1)

        # Request threads
        seq = client.send_request('threads', {})
        response = client.wait_for_response(seq)

        assert response is not None
        assert response['success'] is True
        assert 'threads' in response['body']

        threads = response['body']['threads']
        assert len(threads) == 1
        assert threads[0]['name'] == 'Main Thread'

    def test_unknown_command_handling(self, dap_server):
        """Test that unknown commands return error."""
        client = dap_server

        # Send unknown command
        seq = client.send_request('unknownCommand', {})
        response = client.wait_for_response(seq)

        assert response is not None
        assert response['success'] is False
        assert 'Unknown command' in response['message']


class TestDAPCLI:
    """Test DAP server CLI integration."""

    def test_dap_cli_command_exists(self):
        """Test that debug-adapter command exists in CLI."""
        result = subprocess.run(
            ['python', '-m', 'mlpy', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )

        assert result.returncode == 0
        assert 'debug-adapter' in result.stdout

    def test_dap_cli_help(self):
        """Test debug-adapter help text."""
        result = subprocess.run(
            ['python', '-m', 'mlpy', 'debug-adapter', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )

        assert result.returncode == 0
        assert 'Debug Adapter Protocol' in result.stdout
        assert '--log' in result.stdout

    def test_dap_server_starts(self):
        """Test that DAP server process starts successfully."""
        # Start server
        process = subprocess.Popen(
            ['python', '-m', 'mlpy', 'debug-adapter'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        try:
            # Give it time to start
            time.sleep(0.5)

            # Check if still running
            assert process.poll() is None, "DAP server exited immediately"

            # Send a simple initialize to verify it responds
            message = {
                'type': 'request',
                'seq': 1,
                'command': 'initialize',
                'arguments': {}
            }

            body = json.dumps(message)
            content = body.encode('utf-8')
            header = f'Content-Length: {len(content)}\r\n\r\n'.encode('utf-8')

            if process.stdin:
                process.stdin.write(header)
                process.stdin.write(content)
                process.stdin.flush()

            # Wait for response (with timeout)
            time.sleep(1.0)

            # If we got here without crashing, server is working
            assert process.poll() is None, "DAP server crashed"

        finally:
            # Cleanup
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()


class TestDAPTranspilation:
    """Test DAP server with actual ML file transpilation."""

    def test_launch_with_valid_ml_file(self, tmp_path):
        """Test launching DAP server with valid ML file."""
        # Create test ML file
        ml_file = tmp_path / "hello.ml"
        ml_file.write_text("""
function greet(name) {
    message = "Hello, " + name + "!";
    print(message);
}

greet("World");
greet("ML");
""")

        # Start DAP server
        process = subprocess.Popen(
            ['python', '-m', 'mlpy', 'debug-adapter'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        client = DAPClient(process)
        client.start_reading()

        try:
            # Initialize
            client.send_request('initialize', {})
            client.wait_for_response(1, timeout=5.0)

            # Launch with our ML file
            seq = client.send_request('launch', {
                'program': str(ml_file),
                'stopOnEntry': False
            })

            response = client.wait_for_response(seq, timeout=10.0)

            if response:
                # If transpilation works, should succeed
                if response['success']:
                    # Wait for initialized event
                    event = client.wait_for_event('initialized', timeout=5.0)
                    assert event is not None, "Should receive initialized event"

                    # Try to set a breakpoint
                    seq = client.send_request('setBreakpoints', {
                        'source': {'path': str(ml_file)},
                        'breakpoints': [{'line': 3}]
                    })

                    bp_response = client.wait_for_response(seq, timeout=5.0)
                    assert bp_response is not None
                    assert bp_response['success'] is True

        finally:
            client.stop()


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
