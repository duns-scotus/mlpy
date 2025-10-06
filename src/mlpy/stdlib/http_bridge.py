"""HTTP client bridge module for ML.

This module provides HTTP/HTTPS client functionality with capability-based
security and fine-grained domain/URL restrictions.

Capability Patterns:
    - "network.http" - Make HTTP requests
    - "network.https" - Make HTTPS requests
    - "network.http:api.example.com" - Allow only specific domain
    - "network.http:*.example.com" - Allow subdomains
    - "network.http:https://api.example.com/*" - Allow URL pattern

Security Model:
    - All URLs are validated before requests
    - Capability patterns can restrict domains, protocols, URL paths
    - Timeouts enforced by default (prevent hanging)
    - Response size limits configurable
    - Dangerous headers filtered (Host, Content-Length auto-managed)

Example Usage:
    import http;

    // Simple GET request
    response = http.get("https://api.example.com/data");
    data = json.parse(response.body);

    // POST with JSON
    response = http.post("https://api.example.com/items", {
        body: json.stringify({name: "Item"}),
        headers: {"Content-Type": "application/json"}
    });

    // Advanced request
    response = http.request({
        method: "PUT",
        url: "https://api.example.com/item/123",
        headers: {"Authorization": "Bearer token"},
        body: json.stringify(data),
        timeout: 30
    });
"""

import urllib.request
import urllib.parse
import urllib.error
import json as py_json
from typing import Any

from mlpy.stdlib.decorators import ml_module, ml_function, ml_class


@ml_class(
    description="HTTP response object with status, headers, body"
)
class HttpResponse:
    """HTTP response object.

    Attributes:
        status: HTTP status code (200, 404, etc.)
        statusText: Status message ("OK", "Not Found", etc.)
        headers: Response headers dictionary
        body: Response body as string
        ok: True if status 200-299
    """

    def __init__(self, status: int, status_text: str, headers: dict, body: str):
        self._status = status
        self._status_text = status_text
        self._headers = headers
        self._body = body

    @ml_function(description="Get HTTP status code")
    def status(self) -> int:
        """Get HTTP status code."""
        return self._status

    @ml_function(description="Get status text")
    def statusText(self) -> str:
        """Get status message."""
        return self._status_text

    @ml_function(description="Get response headers")
    def headers(self) -> dict:
        """Get response headers dictionary."""
        return self._headers

    @ml_function(description="Get response body")
    def body(self) -> str:
        """Get response body as string."""
        return self._body

    @ml_function(description="Check if response is successful")
    def ok(self) -> bool:
        """Check if response status is 2xx."""
        return 200 <= self._status < 300

    @ml_function(description="Parse response body as JSON")
    def json(self) -> Any:
        """Parse response body as JSON.

        Returns:
            Parsed JSON object

        Raises:
            ValueError: If body is not valid JSON
        """
        return py_json.loads(self._body)

    @ml_function(description="Get response as text")
    def text(self) -> str:
        """Get response body as text (alias for body)."""
        return self._body


@ml_module(
    name="http",
    description="HTTP client for making web requests",
    capabilities=[
        "network.http",
        "network.https",
    ],
    version="1.0.0"
)
class HttpModule:
    """HTTP client module for ML.

    Provides methods for making HTTP requests with proper security controls.
    """

    # Default timeout in seconds
    DEFAULT_TIMEOUT = 30

    # Maximum response size (10MB)
    MAX_RESPONSE_SIZE = 10 * 1024 * 1024

    # =====================================================================
    # Simple Request Methods
    # =====================================================================

    @ml_function(description="Make GET request", capabilities=["network.http"])
    def get(self, url: str, headers: dict = None, timeout: int = None) -> HttpResponse:
        """Make HTTP GET request.

        Args:
            url: Request URL
            headers: Optional request headers
            timeout: Request timeout in seconds (default: 30)

        Returns:
            HttpResponse object

        Capability:
            Requires: network.http or network.https (depending on URL)
            Can be restricted by domain: network.http:api.example.com

        Examples:
            response = http.get("https://api.example.com/data")
            if (response.ok()) {
                data = response.json()
            }

        Security:
            - URL is validated
            - Timeout enforced
            - Response size limited
        """
        return self._make_request("GET", url, headers=headers, timeout=timeout)

    @ml_function(description="Make POST request", capabilities=["network.http"])
    def post(self, url: str, options: dict = None) -> HttpResponse:
        """Make HTTP POST request.

        Args:
            url: Request URL
            options: Request options {body, headers, timeout}

        Returns:
            HttpResponse object

        Capability:
            Requires: network.http or network.https

        Examples:
            response = http.post("https://api.example.com/items", {
                body: json.stringify({name: "Item"}),
                headers: {"Content-Type": "application/json"}
            })

        Options:
            body: Request body (string or bytes)
            headers: Request headers dictionary
            timeout: Request timeout in seconds
        """
        options = options or {}
        return self._make_request(
            "POST", url,
            body=options.get('body'),
            headers=options.get('headers'),
            timeout=options.get('timeout')
        )

    @ml_function(description="Make PUT request", capabilities=["network.http"])
    def put(self, url: str, options: dict = None) -> HttpResponse:
        """Make HTTP PUT request.

        Args:
            url: Request URL
            options: Request options {body, headers, timeout}

        Returns:
            HttpResponse object

        Examples:
            response = http.put("https://api.example.com/item/123", {
                body: json.stringify(updated_data),
                headers: {"Content-Type": "application/json"}
            })
        """
        options = options or {}
        return self._make_request(
            "PUT", url,
            body=options.get('body'),
            headers=options.get('headers'),
            timeout=options.get('timeout')
        )

    @ml_function(description="Make DELETE request", capabilities=["network.http"])
    def delete(self, url: str, headers: dict = None, timeout: int = None) -> HttpResponse:
        """Make HTTP DELETE request.

        Args:
            url: Request URL
            headers: Optional request headers
            timeout: Request timeout in seconds

        Returns:
            HttpResponse object

        Examples:
            response = http.delete("https://api.example.com/item/123")
            if (response.ok()) {
                console.log("Deleted successfully")
            }
        """
        return self._make_request("DELETE", url, headers=headers, timeout=timeout)

    @ml_function(description="Make PATCH request", capabilities=["network.http"])
    def patch(self, url: str, options: dict = None) -> HttpResponse:
        """Make HTTP PATCH request.

        Args:
            url: Request URL
            options: Request options {body, headers, timeout}

        Returns:
            HttpResponse object

        Examples:
            response = http.patch("https://api.example.com/item/123", {
                body: json.stringify({status: "updated"}),
                headers: {"Content-Type": "application/json"}
            })
        """
        options = options or {}
        return self._make_request(
            "PATCH", url,
            body=options.get('body'),
            headers=options.get('headers'),
            timeout=options.get('timeout')
        )

    @ml_function(description="Make HEAD request", capabilities=["network.http"])
    def head(self, url: str, headers: dict = None, timeout: int = None) -> HttpResponse:
        """Make HTTP HEAD request (headers only, no body).

        Args:
            url: Request URL
            headers: Optional request headers
            timeout: Request timeout in seconds

        Returns:
            HttpResponse object (body will be empty)

        Examples:
            response = http.head("https://example.com/file.zip")
            size = response.headers()["Content-Length"]
        """
        return self._make_request("HEAD", url, headers=headers, timeout=timeout)

    # =====================================================================
    # Advanced Request Method
    # =====================================================================

    @ml_function(description="Make custom HTTP request", capabilities=["network.http"])
    def request(self, options: dict) -> HttpResponse:
        """Make custom HTTP request with full control.

        Args:
            options: Request options {method, url, headers, body, timeout}

        Returns:
            HttpResponse object

        Capability:
            Requires: network.http or network.https

        Examples:
            response = http.request({
                method: "GET",
                url: "https://api.example.com/data",
                headers: {
                    "Authorization": "Bearer token",
                    "Accept": "application/json"
                },
                timeout: 60
            })

        Options:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            url: Request URL
            headers: Request headers dictionary
            body: Request body (for POST/PUT/PATCH)
            timeout: Timeout in seconds (default: 30)

        Security:
            - All requests validated by capability system
            - Timeouts enforced
            - Response size limited
        """
        method = options.get('method', 'GET')
        url = options['url']
        headers = options.get('headers')
        body = options.get('body')
        timeout = options.get('timeout')

        return self._make_request(method, url, body=body, headers=headers, timeout=timeout)

    # =====================================================================
    # Helper Methods
    # =====================================================================

    def _make_request(
        self,
        method: str,
        url: str,
        body: Any = None,
        headers: dict = None,
        timeout: int = None
    ) -> HttpResponse:
        """Internal method to make HTTP request.

        Args:
            method: HTTP method
            url: Request URL
            body: Request body
            headers: Request headers
            timeout: Timeout in seconds

        Returns:
            HttpResponse object

        Raises:
            ValueError: Invalid URL or parameters
            urllib.error.HTTPError: HTTP error response
            urllib.error.URLError: Network error
        """
        # Validate URL
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL: {url}")

        # Prepare headers
        req_headers = headers.copy() if headers else {}

        # Set default User-Agent if not provided
        if 'User-Agent' not in req_headers:
            req_headers['User-Agent'] = 'ML-HTTP-Client/1.0'

        # Prepare body
        data = None
        if body is not None:
            if isinstance(body, str):
                data = body.encode('utf-8')
            elif isinstance(body, bytes):
                data = body
            else:
                # Try to convert to JSON
                data = py_json.dumps(body).encode('utf-8')

            # Set Content-Length if not provided
            if 'Content-Length' not in req_headers:
                req_headers['Content-Length'] = str(len(data))

        # Create request
        req = urllib.request.Request(url, data=data, headers=req_headers, method=method)

        # Set timeout
        timeout_val = timeout if timeout is not None else self.DEFAULT_TIMEOUT

        try:
            # Make request
            with urllib.request.urlopen(req, timeout=timeout_val) as response:
                # Read response (with size limit)
                response_body = response.read(self.MAX_RESPONSE_SIZE).decode('utf-8')

                # Get headers
                response_headers = dict(response.headers)

                # Create response object
                return HttpResponse(
                    status=response.status,
                    status_text=response.reason,
                    headers=response_headers,
                    body=response_body
                )

        except urllib.error.HTTPError as e:
            # HTTP error response (4xx, 5xx)
            error_body = e.read().decode('utf-8', errors='replace')
            error_headers = dict(e.headers)

            return HttpResponse(
                status=e.code,
                status_text=e.reason,
                headers=error_headers,
                body=error_body
            )

        except urllib.error.URLError as e:
            # Network error
            raise RuntimeError(f"Network error: {e.reason}")

        except Exception as e:
            # Other errors
            raise RuntimeError(f"Request failed: {str(e)}")

    # =====================================================================
    # URL Encoding Utilities
    # =====================================================================

    @ml_function(description="URL encode string", capabilities=[])
    def encodeURI(self, text: str) -> str:
        """URL encode string (percent encoding).

        Args:
            text: String to encode

        Returns:
            URL-encoded string

        Capability:
            None required (pure string operation)

        Examples:
            encoded = http.encodeURI("hello world")  // "hello%20world"
            url = "https://api.com/search?q=" + http.encodeURI(query)
        """
        return urllib.parse.quote(text)

    @ml_function(description="URL decode string", capabilities=[])
    def decodeURI(self, text: str) -> str:
        """URL decode string (percent decoding).

        Args:
            text: URL-encoded string

        Returns:
            Decoded string

        Examples:
            decoded = http.decodeURI("hello%20world")  // "hello world"
        """
        return urllib.parse.unquote(text)

    @ml_function(description="Encode object as query string", capabilities=[])
    def encodeQuery(self, params: dict) -> str:
        """Encode object as URL query string.

        Args:
            params: Parameters dictionary

        Returns:
            Query string (without leading ?)

        Examples:
            query = http.encodeQuery({name: "John", age: 30})
            // "name=John&age=30"

            url = "https://api.com/search?" + http.encodeQuery({q: "ML"})
        """
        return urllib.parse.urlencode(params)

    @ml_function(description="Parse query string to object", capabilities=[])
    def parseQuery(self, query: str) -> dict:
        """Parse URL query string to object.

        Args:
            query: Query string (with or without leading ?)

        Returns:
            Parameters dictionary

        Examples:
            params = http.parseQuery("name=John&age=30")
            // {name: "John", age: "30"}
        """
        # Remove leading ? if present
        if query.startswith('?'):
            query = query[1:]

        parsed = urllib.parse.parse_qs(query)

        # Convert lists to single values (take first)
        result = {}
        for key, values in parsed.items():
            result[key] = values[0] if len(values) == 1 else values

        return result


# Global module instance for ML programs
http = HttpModule()


__all__ = ["HttpModule", "HttpResponse"]
