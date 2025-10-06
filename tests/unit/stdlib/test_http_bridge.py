"""Unit tests for http_bridge module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import urllib.error

from mlpy.stdlib.http_bridge import HttpModule, HttpResponse, http as http_module
from mlpy.stdlib.decorators import get_module_metadata, _MODULE_REGISTRY


class TestHttpModuleRegistration:
    """Test that HTTP module is properly registered with decorators."""

    def test_http_module_registered(self):
        """Test that http module is in global registry."""
        assert "http" in _MODULE_REGISTRY
        assert _MODULE_REGISTRY["http"] == HttpModule

    def test_http_module_metadata(self):
        """Test http module metadata is correct."""
        metadata = get_module_metadata("http")
        assert metadata is not None
        assert metadata.name == "http"
        assert metadata.description == "HTTP client for making web requests"
        assert "network.http" in metadata.capabilities
        assert "network.https" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_http_has_function_metadata(self):
        """Test that http module has registered functions."""
        metadata = get_module_metadata("http")

        # Check key methods are registered
        assert "get" in metadata.functions
        assert "post" in metadata.functions
        assert "put" in metadata.functions
        assert "delete" in metadata.functions
        assert "patch" in metadata.functions
        assert "head" in metadata.functions
        assert "request" in metadata.functions
        assert "encodeURI" in metadata.functions
        assert "decodeURI" in metadata.functions
        assert "encodeQuery" in metadata.functions
        assert "parseQuery" in metadata.functions

        # Should have 11 functions
        assert len(metadata.functions) == 11

    def test_http_function_capabilities(self):
        """Test that http functions have correct capabilities."""
        metadata = get_module_metadata("http")

        # HTTP methods require network.http
        assert metadata.functions["get"].capabilities == ["network.http"]
        assert metadata.functions["post"].capabilities == ["network.http"]
        assert metadata.functions["put"].capabilities == ["network.http"]
        assert metadata.functions["delete"].capabilities == ["network.http"]

        # URL utilities require no capabilities
        assert metadata.functions["encodeURI"].capabilities == []
        assert metadata.functions["decodeURI"].capabilities == []
        assert metadata.functions["encodeQuery"].capabilities == []
        assert metadata.functions["parseQuery"].capabilities == []


class TestHttpResponse:
    """Test HttpResponse class."""

    def test_response_creation(self):
        """Test creating HttpResponse."""
        response = HttpResponse(200, "OK", {"Content-Type": "text/plain"}, "Hello")

        assert response.status() == 200
        assert response.statusText() == "OK"
        assert response.headers() == {"Content-Type": "text/plain"}
        assert response.body() == "Hello"

    def test_response_ok_true(self):
        """Test ok() returns True for 2xx status."""
        response = HttpResponse(200, "OK", {}, "")
        assert response.ok() is True

        response = HttpResponse(204, "No Content", {}, "")
        assert response.ok() is True

    def test_response_ok_false(self):
        """Test ok() returns False for non-2xx status."""
        response = HttpResponse(404, "Not Found", {}, "")
        assert response.ok() is False

        response = HttpResponse(500, "Internal Server Error", {}, "")
        assert response.ok() is False

    def test_response_json_parsing(self):
        """Test json() parses body as JSON."""
        response = HttpResponse(200, "OK", {}, '{"key": "value"}')
        data = response.json()

        assert data == {"key": "value"}

    def test_response_text(self):
        """Test text() returns body."""
        response = HttpResponse(200, "OK", {}, "Hello World")
        assert response.text() == "Hello World"


class TestHttpGetRequest:
    """Test HTTP GET requests."""

    @patch('urllib.request.urlopen')
    def test_get_request_success(self, mock_urlopen):
        """Test successful GET request."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.read.return_value = b'{"result": "success"}'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        mock_urlopen.return_value = mock_response

        # Make request
        response = http_module.get("https://api.example.com/data")

        assert response.status() == 200
        assert response.ok() is True
        assert response.body() == '{"result": "success"}'

    @patch('urllib.request.urlopen')
    def test_get_request_with_headers(self, mock_urlopen):
        """Test GET request with custom headers."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.headers = {}
        mock_response.read.return_value = b'response'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        mock_urlopen.return_value = mock_response

        # Make request with headers
        headers = {"Authorization": "Bearer token123"}
        response = http_module.get("https://api.example.com/data", headers=headers)

        assert response.ok() is True

    @patch('urllib.request.urlopen')
    def test_get_request_404_error(self, mock_urlopen):
        """Test GET request returns 404 response (not exception)."""
        # Create a minimal HTTPError mock that works with our error handling
        class MockHTTPError(urllib.error.HTTPError):
            def __init__(self):
                # Don't call super().__init__ to avoid constructor issues
                self.code = 404
                self.msg = "Not Found"
                self.headers = {}

            def read(self):
                return b'Not Found'

        mock_urlopen.side_effect = MockHTTPError()

        # Should return response, not raise exception
        response = http_module.get("https://example.com/notfound")

        assert response.status() == 404
        assert response.ok() is False


class TestHttpPostRequest:
    """Test HTTP POST requests."""

    @patch('urllib.request.urlopen')
    def test_post_request_with_body(self, mock_urlopen):
        """Test POST request with body."""
        mock_response = MagicMock()
        mock_response.status = 201
        mock_response.reason = "Created"
        mock_response.headers = {}
        mock_response.read.return_value = b'{"id": 123}'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        mock_urlopen.return_value = mock_response

        # Make POST request
        options = {
            "body": '{"name": "Test"}',
            "headers": {"Content-Type": "application/json"}
        }
        response = http_module.post("https://api.example.com/items", options)

        assert response.status() == 201
        assert response.ok() is True

    @patch('urllib.request.urlopen')
    def test_post_request_no_options(self, mock_urlopen):
        """Test POST request without options."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.headers = {}
        mock_response.read.return_value = b'success'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        mock_urlopen.return_value = mock_response

        response = http_module.post("https://api.example.com/action")
        assert response.ok() is True


class TestHttpOtherMethods:
    """Test other HTTP methods (PUT, DELETE, PATCH, HEAD)."""

    @patch('urllib.request.urlopen')
    def test_put_request(self, mock_urlopen):
        """Test PUT request."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.headers = {}
        mock_response.read.return_value = b'updated'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        mock_urlopen.return_value = mock_response

        options = {"body": '{"status": "updated"}'}
        response = http_module.put("https://api.example.com/item/1", options)

        assert response.ok() is True

    @patch('urllib.request.urlopen')
    def test_delete_request(self, mock_urlopen):
        """Test DELETE request."""
        mock_response = MagicMock()
        mock_response.status = 204
        mock_response.reason = "No Content"
        mock_response.headers = {}
        mock_response.read.return_value = b''
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        mock_urlopen.return_value = mock_response

        response = http_module.delete("https://api.example.com/item/1")

        assert response.status() == 204
        assert response.ok() is True

    @patch('urllib.request.urlopen')
    def test_patch_request(self, mock_urlopen):
        """Test PATCH request."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.headers = {}
        mock_response.read.return_value = b'patched'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        mock_urlopen.return_value = mock_response

        options = {"body": '{"field": "value"}'}
        response = http_module.patch("https://api.example.com/item/1", options)

        assert response.ok() is True

    @patch('urllib.request.urlopen')
    def test_head_request(self, mock_urlopen):
        """Test HEAD request."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.headers = {"Content-Length": "12345"}
        mock_response.read.return_value = b''
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        mock_urlopen.return_value = mock_response

        response = http_module.head("https://example.com/file.zip")

        assert response.ok() is True
        assert response.headers()["Content-Length"] == "12345"


class TestHttpRequestMethod:
    """Test generic request() method."""

    @patch('urllib.request.urlopen')
    def test_request_with_all_options(self, mock_urlopen):
        """Test request() with all options."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.headers = {}
        mock_response.read.return_value = b'response'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        mock_urlopen.return_value = mock_response

        options = {
            "method": "GET",
            "url": "https://api.example.com/data",
            "headers": {"Authorization": "Bearer token"},
            "timeout": 60
        }
        response = http_module.request(options)

        assert response.ok() is True

    def test_request_invalid_url(self):
        """Test request with invalid URL raises error."""
        with pytest.raises(ValueError, match="Invalid URL"):
            http_module.request({"url": "not-a-valid-url"})


class TestUrlEncodingUtilities:
    """Test URL encoding/decoding utilities."""

    def test_encode_uri(self):
        """Test URL encoding."""
        result = http_module.encodeURI("hello world")
        assert result == "hello%20world"

        result = http_module.encodeURI("test@example.com")
        assert "test" in result
        assert "%40" in result  # @ encoded

    def test_decode_uri(self):
        """Test URL decoding."""
        result = http_module.decodeURI("hello%20world")
        assert result == "hello world"

        result = http_module.decodeURI("test%40example.com")
        assert result == "test@example.com"

    def test_encode_query(self):
        """Test query string encoding."""
        params = {"name": "John Doe", "age": 30}
        result = http_module.encodeQuery(params)

        # Order might vary, check both keys present
        assert "name=John" in result or "name=John+Doe" in result
        assert "age=30" in result
        assert "&" in result

    def test_parse_query(self):
        """Test query string parsing."""
        result = http_module.parseQuery("name=John&age=30")

        assert result["name"] == "John"
        assert result["age"] == "30"

    def test_parse_query_with_question_mark(self):
        """Test parsing query string with leading ?."""
        result = http_module.parseQuery("?name=John&age=30")

        assert result["name"] == "John"
        assert result["age"] == "30"

    def test_parse_query_multiple_values(self):
        """Test parsing query with multiple values for same key."""
        result = http_module.parseQuery("tag=python&tag=ml&tag=code")

        # Multiple values returned as list
        assert "tag" in result


class TestHttpErrorHandling:
    """Test HTTP error handling."""

    @patch('urllib.request.urlopen')
    def test_network_error_raises_runtime_error(self, mock_urlopen):
        """Test network error raises RuntimeError."""
        url_error = urllib.error.URLError("Connection refused")
        mock_urlopen.side_effect = url_error

        with pytest.raises(RuntimeError, match="Network error"):
            http_module.get("https://unreachable.example.com")

    @patch('urllib.request.urlopen')
    def test_timeout_error(self, mock_urlopen):
        """Test timeout handling."""
        import socket
        mock_urlopen.side_effect = socket.timeout("Request timed out")

        with pytest.raises(RuntimeError):
            http_module.get("https://example.com", timeout=1)


class TestHttpConstants:
    """Test HTTP module constants."""

    def test_default_timeout(self):
        """Test default timeout constant."""
        assert http_module.DEFAULT_TIMEOUT == 30

    def test_max_response_size(self):
        """Test max response size constant."""
        assert http_module.MAX_RESPONSE_SIZE == 10 * 1024 * 1024  # 10MB
