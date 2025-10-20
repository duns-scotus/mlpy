External API Integration
=========================

.. note::
   **Chapter Summary:** Integrating ML with external HTTP APIs, REST services, GraphQL, WebSockets, and third-party platforms.

This chapter covers integration patterns for external APIs where ML functions process requests, responses, and handle API-specific logic like authentication, rate limiting, and error recovery.

----

HTTP Client Integration
------------------------

Basic REST API Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ML to process API responses and build requests.

**api_client.py:**

.. code-block:: python

   import requests
   from mlpy import MLExecutor
   from typing import Dict, Any, Optional
   import time

   class MLAPIClient:
       """HTTP client with ML request/response processing."""

       def __init__(self, ml_script: str, base_url: str):
           """Initialize API client.

           Args:
               ml_script: Path to ML script
               base_url: Base URL for API
           """
           self.executor = MLExecutor()
           self.executor.load(ml_script)
           self.base_url = base_url.rstrip('/')
           self.session = requests.Session()

       def request(
           self,
           method: str,
           endpoint: str,
           data: Optional[Dict] = None,
           params: Optional[Dict] = None,
           process_request: str = None,
           process_response: str = None
       ) -> Any:
           """Make HTTP request with ML processing.

           Args:
               method: HTTP method (GET, POST, etc.)
               endpoint: API endpoint
               data: Request body data
               params: Query parameters
               process_request: ML function to process request
               process_response: ML function to process response

           Returns:
               Processed response from ML or raw response
           """
           url = f"{self.base_url}{endpoint}"

           # Process request with ML
           if process_request and data:
               data = self.executor.call_function(process_request, data)

           # Make request
           response = self.session.request(
               method=method,
               url=url,
               json=data,
               params=params
           )

           response.raise_for_status()

           # Process response with ML
           if process_response:
               result = self.executor.call_function(process_response, {
                   "status_code": response.status_code,
                   "headers": dict(response.headers),
                   "data": response.json() if response.content else None
               })
               return result

           return response.json()

       def get(self, endpoint: str, **kwargs) -> Any:
           """GET request."""
           return self.request('GET', endpoint, **kwargs)

       def post(self, endpoint: str, data: Dict, **kwargs) -> Any:
           """POST request."""
           return self.request('POST', endpoint, data=data, **kwargs)

       def put(self, endpoint: str, data: Dict, **kwargs) -> Any:
           """PUT request."""
           return self.request('PUT', endpoint, data=data, **kwargs)

       def delete(self, endpoint: str, **kwargs) -> Any:
           """DELETE request."""
           return self.request('DELETE', endpoint, **kwargs)

**api_processors.ml:**

.. code-block:: ml

   function processRequest(data) {
       # Add request metadata
       data.timestamp = new Date().toISOString();
       data.version = "v1";

       # Validate required fields
       if (!data.user_id) {
           throw "Missing required field: user_id";
       }

       return data;
   }

   function processResponse(response) {
       let status = response.status_code;
       let data = response.data;

       # Parse and transform response
       if (status >= 200 && status < 300) {
           return {
               "success": true,
               "data": data,
               "processed_at": new Date().toISOString()
           };
       } else {
           return {
               "success": false,
               "error": data.message || "Unknown error",
               "status": status
           };
       }
   }

   function transformUserData(data) {
       # Transform API response to internal format
       return {
           "id": data.id,
           "name": data.full_name,
           "email": data.email_address,
           "created": data.created_at,
           "is_active": data.status == "active"
       };
   }

**Usage:**

.. code-block:: python

   # Create API client
   api = MLAPIClient("api_processors.ml", "https://api.example.com")

   # POST with request processing
   result = api.post(
       "/users",
       data={"user_id": 123, "name": "John Doe"},
       process_request="processRequest",
       process_response="processResponse"
   )

   if result["success"]:
       print(f"User created: {result['data']}")
   else:
       print(f"Error: {result['error']}")

   # GET with response transformation
   user_data = api.get(
       "/users/123",
       process_response="transformUserData"
   )
   print(f"User: {user_data['name']} ({user_data['email']})")

Authentication Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Handle various authentication methods with ML.

**authenticated_client.py:**

.. code-block:: python

   import requests
   from mlpy import MLExecutor
   from typing import Dict, Any, Optional
   from datetime import datetime, timedelta

   class AuthenticatedMLClient:
       """API client with authentication handling."""

       def __init__(self, ml_script: str, base_url: str):
           self.executor = MLExecutor()
           self.executor.load(ml_script)
           self.base_url = base_url
           self.session = requests.Session()
           self.token = None
           self.token_expires = None

       def authenticate(self, credentials: Dict[str, str]):
           """Authenticate and obtain token."""
           # Process credentials with ML
           processed_creds = self.executor.call_function(
               "processCredentials",
               credentials
           )

           # Make auth request
           response = self.session.post(
               f"{self.base_url}/auth/token",
               json=processed_creds
           )
           response.raise_for_status()

           # Process auth response
           auth_data = self.executor.call_function(
               "processAuthResponse",
               response.json()
           )

           self.token = auth_data["token"]
           self.token_expires = datetime.now() + timedelta(
               seconds=auth_data.get("expires_in", 3600)
           )

           # Add token to session headers
           self.session.headers['Authorization'] = f"Bearer {self.token}"

       def ensure_authenticated(self):
           """Ensure valid authentication."""
           if not self.token or datetime.now() >= self.token_expires:
               raise RuntimeError("Not authenticated or token expired")

       def request(
           self,
           method: str,
           endpoint: str,
           data: Optional[Dict] = None,
           **kwargs
       ) -> Any:
           """Make authenticated request."""
           self.ensure_authenticated()

           response = self.session.request(
               method=method,
               url=f"{self.base_url}{endpoint}",
               json=data,
               **kwargs
           )

           response.raise_for_status()
           return response.json()

**auth_processors.ml:**

.. code-block:: ml

   function processCredentials(creds) {
       # Validate credentials
       if (!creds.username || !creds.password) {
           throw "Username and password required";
       }

       # Add client metadata
       return {
           "username": creds.username,
           "password": creds.password,
           "client_id": "ml-client",
           "grant_type": "password"
       };
   }

   function processAuthResponse(response) {
       # Extract token info
       return {
           "token": response.access_token,
           "refresh_token": response.refresh_token,
           "expires_in": response.expires_in,
           "token_type": response.token_type
       };
   }

**Usage:**

.. code-block:: python

   # Create authenticated client
   client = AuthenticatedMLClient("auth_processors.ml", "https://api.example.com")

   # Authenticate
   client.authenticate({
       "username": "user@example.com",
       "password": "secret"
   })

   # Make authenticated requests
   data = client.request('GET', '/protected/resource')

----

REST API Integration
---------------------

CRUD Operations with ML
~~~~~~~~~~~~~~~~~~~~~~~~~

Implement complete CRUD operations with ML processing.

.. code-block:: python

   from typing import List, Dict, Any, Optional
   import requests
   from mlpy import MLExecutor

   class MLResourceClient:
       """RESTful resource client with ML processing."""

       def __init__(
           self,
           ml_script: str,
           base_url: str,
           resource_name: str
       ):
           """Initialize resource client.

           Args:
               ml_script: Path to ML script
               base_url: API base URL
               resource_name: Resource name (e.g., 'users', 'products')
           """
           self.executor = MLExecutor()
           self.executor.load(ml_script)
           self.base_url = base_url
           self.resource_name = resource_name
           self.endpoint = f"{base_url}/{resource_name}"

       def list(
           self,
           filters: Optional[Dict] = None,
           page: int = 1,
           per_page: int = 10
       ) -> Dict[str, Any]:
           """List resources with pagination."""
           # Build query parameters with ML
           params = self.executor.call_function("buildListParams", {
               "filters": filters or {},
               "page": page,
               "per_page": per_page
           })

           # Make request
           response = requests.get(self.endpoint, params=params)
           response.raise_for_status()

           # Process response
           return self.executor.call_function(
               "processListResponse",
               response.json()
           )

       def get(self, resource_id: str) -> Dict[str, Any]:
           """Get single resource by ID."""
           response = requests.get(f"{self.endpoint}/{resource_id}")
           response.raise_for_status()

           # Transform response
           return self.executor.call_function(
               "transformResource",
               response.json()
           )

       def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
           """Create new resource."""
           # Validate and prepare data
           prepared = self.executor.call_function("prepareCreate", data)

           # Make request
           response = requests.post(self.endpoint, json=prepared)
           response.raise_for_status()

           # Process created resource
           return self.executor.call_function(
               "processCreated",
               response.json()
           )

       def update(
           self,
           resource_id: str,
           data: Dict[str, Any]
       ) -> Dict[str, Any]:
           """Update existing resource."""
           # Prepare update data
           prepared = self.executor.call_function("prepareUpdate", data)

           # Make request
           response = requests.put(
               f"{self.endpoint}/{resource_id}",
               json=prepared
           )
           response.raise_for_status()

           return response.json()

       def delete(self, resource_id: str) -> bool:
           """Delete resource."""
           response = requests.delete(f"{self.endpoint}/{resource_id}")
           response.raise_for_status()

           return response.status_code == 204

**crud_processors.ml:**

.. code-block:: ml

   function buildListParams(params) {
       let filters = params.filters;
       let page = params.page;
       let perPage = params.per_page;

       # Build query parameters
       let queryParams = {
           "page": page,
           "per_page": perPage
       };

       # Add filters
       let keys = Object.keys(filters);
       let i = 0;
       while (i < keys.length) {
           let key = keys[i];
           queryParams[key] = filters[key];
           i = i + 1;
       }

       return queryParams;
   }

   function processListResponse(response) {
       return {
           "items": response.data || response.items || [],
           "total": response.total || response.data.length,
           "page": response.page || 1,
           "pages": response.pages || 1
       };
   }

   function transformResource(resource) {
       # Transform API format to internal format
       return {
           "id": resource.id,
           "name": resource.name,
           "created_at": resource.created_at,
           "updated_at": resource.updated_at
       };
   }

   function prepareCreate(data) {
       # Validate required fields
       if (!data.name) {
           throw "Name is required";
       }

       # Add metadata
       data.created_at = new Date().toISOString();

       return data;
   }

   function prepareUpdate(data) {
       # Add update timestamp
       data.updated_at = new Date().toISOString();

       return data;
   }

   function processCreated(resource) {
       return {
           "id": resource.id,
           "created": true,
           "resource": resource
       };
   }

**Usage:**

.. code-block:: python

   # Create resource client
   users = MLResourceClient(
       "crud_processors.ml",
       "https://api.example.com/v1",
       "users"
   )

   # List users with filters
   result = users.list(
       filters={"active": True},
       page=1,
       per_page=20
   )
   print(f"Found {result['total']} users")

   # Get single user
   user = users.get("user-123")
   print(f"User: {user['name']}")

   # Create user
   new_user = users.create({
       "name": "Jane Doe",
       "email": "jane@example.com"
   })
   print(f"Created user ID: {new_user['id']}")

   # Update user
   users.update("user-123", {"name": "Jane Smith"})

   # Delete user
   users.delete("user-456")

----

GraphQL Integration
--------------------

ML with GraphQL Queries
~~~~~~~~~~~~~~~~~~~~~~~~~

Process GraphQL queries and responses with ML.

.. code-block:: python

   import requests
   from mlpy import MLExecutor
   from typing import Dict, Any, Optional

   class MLGraphQLClient:
       """GraphQL client with ML query building."""

       def __init__(self, ml_script: str, endpoint: str):
           """Initialize GraphQL client.

           Args:
               ml_script: Path to ML script
               endpoint: GraphQL endpoint URL
           """
           self.executor = MLExecutor()
           self.executor.load(ml_script)
           self.endpoint = endpoint

       def query(
           self,
           query_name: str,
           variables: Optional[Dict] = None,
           fields: Optional[List[str]] = None
       ) -> Any:
           """Execute GraphQL query with ML processing.

           Args:
               query_name: Name of query operation
               variables: Query variables
               fields: Fields to select

           Returns:
               Processed query results
           """
           # Build query with ML
           query_def = self.executor.call_function("buildQuery", {
               "operation": query_name,
               "variables": variables or {},
               "fields": fields or []
           })

           # Execute GraphQL query
           response = requests.post(
               self.endpoint,
               json={
                   "query": query_def["query"],
                   "variables": query_def["variables"]
               }
           )

           response.raise_for_status()
           result = response.json()

           # Check for GraphQL errors
           if "errors" in result:
               raise RuntimeError(f"GraphQL errors: {result['errors']}")

           # Process response
           return self.executor.call_function(
               "processQueryResult",
               result["data"]
           )

       def mutation(
           self,
           mutation_name: str,
           input_data: Dict[str, Any]
       ) -> Any:
           """Execute GraphQL mutation.

           Args:
               mutation_name: Name of mutation operation
               input_data: Mutation input data

           Returns:
               Processed mutation results
           """
           # Build mutation with ML
           mutation_def = self.executor.call_function("buildMutation", {
               "operation": mutation_name,
               "input": input_data
           })

           # Execute mutation
           response = requests.post(
               self.endpoint,
               json={
                   "query": mutation_def["mutation"],
                   "variables": {"input": mutation_def["input"]}
               }
           )

           response.raise_for_status()
           result = response.json()

           if "errors" in result:
               raise RuntimeError(f"GraphQL errors: {result['errors']}")

           return result["data"]

**graphql_processors.ml:**

.. code-block:: ml

   function buildQuery(params) {
       let operation = params.operation;
       let variables = params.variables;
       let fields = params.fields;

       # Build field selection
       let fieldList = fields.length > 0
           ? fields.join(" ")
           : "id name createdAt";

       # Build query string
       let query = "query " + operation + " {";
       query = query + " " + operation + " {";
       query = query + " " + fieldList;
       query = query + " }";
       query = query + "}";

       return {
           "query": query,
           "variables": variables
       };
   }

   function buildMutation(params) {
       let operation = params.operation;
       let input = params.input;

       # Build mutation string
       let mutation = "mutation " + operation + "($input: " + operation + "Input!) {";
       mutation = mutation + " " + operation + "(input: $input) {";
       mutation = mutation + " id success message";
       mutation = mutation + " }";
       mutation = mutation + "}";

       return {
           "mutation": mutation,
           "input": input
       };
   }

   function processQueryResult(data) {
       # Transform GraphQL response
       let keys = Object.keys(data);
       if (keys.length > 0) {
           return data[keys[0]];
       }
       return data;
   }

**Usage:**

.. code-block:: python

   # Create GraphQL client
   gql = MLGraphQLClient(
       "graphql_processors.ml",
       "https://api.example.com/graphql"
   )

   # Execute query
   users = gql.query(
       "users",
       variables={"active": True},
       fields=["id", "name", "email", "createdAt"]
   )
   print(f"Users: {users}")

   # Execute mutation
   result = gql.mutation(
       "createUser",
       input_data={
           "name": "John Doe",
           "email": "john@example.com"
       }
   )
   print(f"Created: {result}")

----

WebSocket Integration
----------------------

Real-Time API Communication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ML with WebSocket connections for real-time data.

.. code-block:: python

   import websocket
   import json
   from mlpy import MLExecutor
   from typing import Callable, Any
   import threading

   class MLWebSocketClient:
       """WebSocket client with ML message processing."""

       def __init__(self, ml_script: str, ws_url: str):
           """Initialize WebSocket client.

           Args:
               ml_script: Path to ML script
               ws_url: WebSocket URL
           """
           self.executor = MLExecutor()
           self.executor.load(ml_script)
           self.ws_url = ws_url
           self.ws = None
           self.message_handlers = {}

       def on_message(self, ws, message):
           """Handle incoming message."""
           try:
               # Parse message
               data = json.loads(message)

               # Process with ML
               processed = self.executor.call_function("processMessage", data)

               # Route to handlers
               msg_type = processed.get("type", "default")
               if msg_type in self.message_handlers:
                   self.message_handlers[msg_type](processed)

           except Exception as e:
               print(f"Error processing message: {e}")

       def on_error(self, ws, error):
           """Handle error."""
           print(f"WebSocket error: {error}")

       def on_close(self, ws, close_status_code, close_msg):
           """Handle connection close."""
           print(f"WebSocket closed: {close_status_code} - {close_msg}")

       def on_open(self, ws):
           """Handle connection open."""
           print("WebSocket connection opened")

           # Send initial message with ML
           initial = self.executor.call_function("buildInitialMessage", {})
           ws.send(json.dumps(initial))

       def register_handler(self, message_type: str, handler: Callable):
           """Register message handler.

           Args:
               message_type: Type of message to handle
               handler: Handler function
           """
           self.message_handlers[message_type] = handler

       def connect(self):
           """Connect to WebSocket."""
           self.ws = websocket.WebSocketApp(
               self.ws_url,
               on_open=self.on_open,
               on_message=self.on_message,
               on_error=self.on_error,
               on_close=self.on_close
           )

           # Run in separate thread
           wst = threading.Thread(target=self.ws.run_forever)
           wst.daemon = True
           wst.start()

       def send(self, data: Any):
           """Send message through WebSocket."""
           if not self.ws:
               raise RuntimeError("Not connected")

           # Process with ML before sending
           processed = self.executor.call_function("prepareMessage", data)

           self.ws.send(json.dumps(processed))

       def close(self):
           """Close WebSocket connection."""
           if self.ws:
               self.ws.close()

**websocket_processors.ml:**

.. code-block:: ml

   function processMessage(message) {
       # Parse and route message
       return {
           "type": message.type || "default",
           "data": message.data,
           "timestamp": message.timestamp,
           "processed_at": new Date().toISOString()
       };
   }

   function buildInitialMessage() {
       # Build connection message
       return {
           "type": "connect",
           "client": "ml-client",
           "version": "1.0",
           "timestamp": new Date().toISOString()
       };
   }

   function prepareMessage(data) {
       # Add metadata to outgoing message
       data.timestamp = new Date().toISOString();
       data.client_id = "ml-client";

       return data;
   }

**Usage:**

.. code-block:: python

   # Create WebSocket client
   ws_client = MLWebSocketClient(
       "websocket_processors.ml",
       "wss://api.example.com/ws"
   )

   # Register message handlers
   def handle_update(message):
       print(f"Update: {message['data']}")

   def handle_notification(message):
       print(f"Notification: {message['data']}")

   ws_client.register_handler("update", handle_update)
   ws_client.register_handler("notification", handle_notification)

   # Connect
   ws_client.connect()

   # Send messages
   ws_client.send({
       "type": "subscribe",
       "channel": "updates"
   })

   # Keep running
   try:
       import time
       while True:
           time.sleep(1)
   except KeyboardInterrupt:
       ws_client.close()

----

Rate Limiting and Retry Logic
-------------------------------

Intelligent API Client
~~~~~~~~~~~~~~~~~~~~~~~

Handle rate limits and retries with ML.

.. code-block:: python

   import requests
   import time
   from mlpy import MLExecutor
   from typing import Dict, Any, Optional
   from datetime import datetime, timedelta

   class RateLimitedMLClient:
       """API client with rate limiting and retry logic."""

       def __init__(
           self,
           ml_script: str,
           base_url: str,
           rate_limit: int = 60,
           rate_window: int = 60
       ):
           """Initialize rate-limited client.

           Args:
               ml_script: Path to ML script
               base_url: API base URL
               rate_limit: Requests per window
               rate_window: Window duration in seconds
           """
           self.executor = MLExecutor()
           self.executor.load(ml_script)
           self.base_url = base_url
           self.rate_limit = rate_limit
           self.rate_window = rate_window
           self.request_times = []

       def wait_for_rate_limit(self):
           """Wait if rate limit would be exceeded."""
           now = datetime.now()
           cutoff = now - timedelta(seconds=self.rate_window)

           # Remove old requests
           self.request_times = [
               t for t in self.request_times if t > cutoff
           ]

           # Check if limit reached
           if len(self.request_times) >= self.rate_limit:
               # Calculate wait time
               oldest = self.request_times[0]
               wait_until = oldest + timedelta(seconds=self.rate_window)
               wait_seconds = (wait_until - now).total_seconds()

               if wait_seconds > 0:
                   print(f"Rate limit reached, waiting {wait_seconds:.1f}s")
                   time.sleep(wait_seconds)

           # Record this request
           self.request_times.append(datetime.now())

       def request_with_retry(
           self,
           method: str,
           endpoint: str,
           data: Optional[Dict] = None,
           max_retries: int = 3
       ) -> Any:
           """Make request with retry logic.

           Args:
               method: HTTP method
               endpoint: API endpoint
               data: Request data
               max_retries: Maximum retry attempts

           Returns:
               API response

           Raises:
               Exception: If all retries fail
           """
           url = f"{self.base_url}{endpoint}"
           attempt = 0

           while attempt < max_retries:
               try:
                   # Check rate limit
                   self.wait_for_rate_limit()

                   # Make request
                   response = requests.request(
                       method=method,
                       url=url,
                       json=data,
                       timeout=30
                   )

                   # Handle rate limit response
                   if response.status_code == 429:
                       retry_after = int(response.headers.get('Retry-After', 60))
                       print(f"Rate limited by server, waiting {retry_after}s")
                       time.sleep(retry_after)
                       attempt += 1
                       continue

                   response.raise_for_status()
                   return response.json()

               except requests.exceptions.RequestException as e:
                   attempt += 1

                   if attempt >= max_retries:
                       raise

                   # Calculate backoff with ML
                   backoff = self.executor.call_function(
                       "calculateBackoff",
                       {"attempt": attempt, "max_retries": max_retries}
                   )

                   wait_time = backoff["wait_seconds"]
                   print(f"Request failed (attempt {attempt}), retrying in {wait_time}s")
                   time.sleep(wait_time)

           raise RuntimeError(f"Failed after {max_retries} attempts")

**retry_processors.ml:**

.. code-block:: ml

   function calculateBackoff(params) {
       let attempt = params.attempt;
       let maxRetries = params.max_retries;

       # Exponential backoff with jitter
       let baseDelay = 1;
       let maxDelay = 60;

       let delay = Math.min(
           maxDelay,
           baseDelay * Math.pow(2, attempt - 1)
       );

       # Add random jitter (0-50% of delay)
       let jitter = delay * Math.random() * 0.5;
       let waitSeconds = delay + jitter;

       return {
           "attempt": attempt,
           "wait_seconds": waitSeconds,
           "should_retry": attempt < maxRetries
       };
   }

**Usage:**

.. code-block:: python

   # Create rate-limited client
   client = RateLimitedMLClient(
       "retry_processors.ml",
       "https://api.example.com",
       rate_limit=60,  # 60 requests
       rate_window=60  # per minute
   )

   # Make requests (automatically rate limited and retried)
   try:
       result = client.request_with_retry(
           'GET',
           '/data',
           max_retries=5
       )
       print(f"Success: {result}")
   except Exception as e:
       print(f"Failed after all retries: {e}")

----

Third-Party Platform Integration
----------------------------------

Stripe Integration Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import stripe
   from mlpy import MLExecutor
   from typing import Dict, Any

   class MLStripeClient:
       """Stripe payment processing with ML."""

       def __init__(self, ml_script: str, api_key: str):
           """Initialize Stripe client with ML.

           Args:
               ml_script: Path to ML script
               api_key: Stripe API key
           """
           stripe.api_key = api_key
           self.executor = MLExecutor()
           self.executor.load(ml_script)

       def create_payment_intent(
           self,
           amount: int,
           currency: str,
           customer_data: Dict[str, Any]
       ) -> Dict[str, Any]:
           """Create payment intent with ML processing.

           Args:
               amount: Amount in cents
               currency: Currency code
               customer_data: Customer information

           Returns:
               Payment intent details
           """
           # Process customer data with ML
           processed = self.executor.call_function(
               "processCustomerData",
               customer_data
           )

           # Validate amount with ML
           validation = self.executor.call_function(
               "validatePayment",
               {"amount": amount, "currency": currency}
           )

           if not validation["valid"]:
               raise ValueError(f"Invalid payment: {validation['errors']}")

           # Create payment intent
           intent = stripe.PaymentIntent.create(
               amount=amount,
               currency=currency,
               customer=processed.get("stripe_customer_id"),
               metadata=processed.get("metadata", {})
           )

           # Process result
           return self.executor.call_function(
               "processPaymentIntent",
               {
                   "id": intent.id,
                   "status": intent.status,
                   "amount": intent.amount,
                   "currency": intent.currency
               }
           )

**stripe_processors.ml:**

.. code-block:: ml

   function processCustomerData(customer) {
       # Prepare customer data for Stripe
       return {
           "stripe_customer_id": customer.id,
           "metadata": {
               "user_id": customer.user_id,
               "order_id": customer.order_id,
               "timestamp": new Date().toISOString()
           }
       };
   }

   function validatePayment(payment) {
       let errors = [];

       # Validate amount
       if (payment.amount <= 0) {
           errors.push("Amount must be positive");
       }

       if (payment.amount > 1000000) {
           errors.push("Amount exceeds maximum");
       }

       # Validate currency
       let validCurrencies = ["usd", "eur", "gbp"];
       if (validCurrencies.indexOf(payment.currency) < 0) {
           errors.push("Invalid currency");
       }

       return {
           "valid": errors.length == 0,
           "errors": errors
       };
   }

   function processPaymentIntent(intent) {
       return {
           "payment_id": intent.id,
           "status": intent.status,
           "amount": intent.amount / 100,  # Convert from cents
           "currency": intent.currency.toUpperCase(),
           "requires_action": intent.status == "requires_action"
       };
   }

----

Best Practices
---------------

Error Handling
~~~~~~~~~~~~~~~

**Handle API errors gracefully:**

.. code-block:: python

   try:
       result = api.request('GET', '/data')
   except requests.exceptions.HTTPError as e:
       if e.response.status_code == 404:
           # Handle not found
           pass
       elif e.response.status_code == 429:
           # Handle rate limit
           pass
       else:
           # Handle other errors
           raise

Request Optimization
~~~~~~~~~~~~~~~~~~~~~

**Batch requests when possible:**

.. code-block:: python

   # Good: Batch request
   result = api.post('/batch', {
       "requests": [
           {"id": 1, "data": "..."},
           {"id": 2, "data": "..."}
       ]
   })

   # Avoid: Multiple individual requests
   # for item in items:
   #     api.post('/item', item)

Caching
~~~~~~~~

**Cache API responses:**

.. code-block:: python

   from functools import lru_cache
   from hashlib import md5
   import json

   def cache_key(url, params):
       """Generate cache key."""
       key_data = f"{url}{json.dumps(params, sort_keys=True)}"
       return md5(key_data.encode()).hexdigest()

   @lru_cache(maxsize=128)
   def cached_api_call(url, params_key):
       """Cached API call."""
       return api.get(url, params=json.loads(params_key))

----

Summary
--------

External API integration with ML enables:

**HTTP/REST:**
- Request/response processing with ML
- Authentication handling
- CRUD operations with validation

**GraphQL:**
- Dynamic query building
- Response transformation
- Mutation processing

**WebSockets:**
- Real-time message processing
- Event routing with ML
- Bidirectional communication

**Advanced Features:**
- Rate limiting with intelligent backoff
- Retry logic with exponential backoff
- Third-party platform integration

**Best Practices:**
- Handle errors gracefully
- Implement rate limiting
- Cache responses
- Batch requests
- Validate input/output with ML

ML functions provide powerful data transformation and business logic for API integration while maintaining clean separation of concerns.

----

**Part 3 Complete!** You've now mastered data integration patterns including marshalling, databases, and external APIs.
