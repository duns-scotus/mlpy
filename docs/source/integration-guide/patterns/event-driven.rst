Event-Driven Integration
==========================

.. note::
   **Chapter Summary:** Integrating ML with event-driven architectures, including message queues, pub/sub systems, and reactive programming patterns.

This chapter covers event-driven integration patterns where ML functions respond to events, process message streams, and participate in reactive architectures. You'll learn how to integrate ML with message queues, implement observer patterns, and build event-sourcing systems.

----

Introduction to Event-Driven Architecture
------------------------------------------

Event-driven architecture (EDA) is a design pattern where system components communicate through events rather than direct calls. ML integrates naturally with EDA, providing event handlers, processors, and transformers.

Benefits of Event-Driven ML Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Decoupling:**
- ML logic separated from event sources
- Independent scaling of components
- Easy to add/remove event handlers

**Scalability:**
- Horizontal scaling through message queues
- Load distribution across workers
- Elastic resource allocation

**Resilience:**
- Fault isolation through queues
- Automatic retry mechanisms
- Graceful degradation

**Flexibility:**
- Multiple handlers per event type
- Dynamic handler registration
- Event filtering and routing

Event-Driven Integration Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
   │ Event Source │────▶│ Message Queue │────▶│ ML Handler   │
   │ (Producer)   │     │ (Broker)      │     │ (Consumer)   │
   └──────────────┘     └───────────────┘     └──────────────┘
                               │
                               ├────▶ ┌──────────────┐
                               │      │ ML Handler 2 │
                               │      └──────────────┘
                               │
                               └────▶ ┌──────────────┐
                                      │ ML Handler 3 │
                                      └──────────────┘

----

Basic Event Handling Patterns
-------------------------------

Simple Event Handler
~~~~~~~~~~~~~~~~~~~~~

The simplest pattern: ML function responds to Python events.

**event_handler.py:**

.. code-block:: python

   from mlpy import MLExecutor
   from typing import Callable, Any, Dict, List

   class MLEventHandler:
       """Execute ML functions in response to events."""

       def __init__(self, ml_script: str):
           """Initialize with ML script containing event handlers.

           Args:
               ml_script: Path to ML file or ML source code
           """
           self.executor = MLExecutor()
           self.executor.load(ml_script)
           self.handlers: Dict[str, str] = {}  # event_type -> ml_function_name

       def register(self, event_type: str, ml_function: str):
           """Register ML function as handler for event type.

           Args:
               event_type: Type of event to handle
               ml_function: Name of ML function to call
           """
           # Verify function exists
           if not self.executor.has_function(ml_function):
               raise ValueError(f"ML function '{ml_function}' not found")

           self.handlers[event_type] = ml_function
           print(f"Registered {ml_function} for {event_type}")

       def handle(self, event_type: str, event_data: Any) -> Any:
           """Handle event by calling registered ML function.

           Args:
               event_type: Type of event
               event_data: Event payload

           Returns:
               Result from ML function

           Raises:
               ValueError: If no handler registered for event type
           """
           if event_type not in self.handlers:
               raise ValueError(f"No handler for event type: {event_type}")

           ml_function = self.handlers[event_type]
           return self.executor.call_function(ml_function, event_data)

       def handle_many(self, events: List[tuple]) -> List[Any]:
           """Handle multiple events in sequence.

           Args:
               events: List of (event_type, event_data) tuples

           Returns:
               List of results
           """
           return [self.handle(evt_type, evt_data)
                   for evt_type, evt_data in events]

**handlers.ml:**

.. code-block:: ml

   # Event handler functions

   function handleUserCreated(event) {
       let user = event.data;
       return {
           "action": "send_welcome_email",
           "email": user.email,
           "name": user.name,
           "timestamp": event.timestamp
       };
   }

   function handleOrderPlaced(event) {
       let order = event.data;
       let total = order.items.reduce(function(sum, item) {
           return sum + (item.price * item.quantity);
       }, 0);

       return {
           "action": "process_payment",
           "order_id": order.id,
           "amount": total,
           "customer_id": order.customer_id
       };
   }

   function handlePaymentReceived(event) {
       let payment = event.data;
       return {
           "action": "fulfill_order",
           "order_id": payment.order_id,
           "payment_method": payment.method,
           "confirmed": true
       };
   }

**Usage:**

.. code-block:: python

   # Create event handler
   handler = MLEventHandler("handlers.ml")

   # Register handlers
   handler.register("user.created", "handleUserCreated")
   handler.register("order.placed", "handleOrderPlaced")
   handler.register("payment.received", "handlePaymentReceived")

   # Handle events
   user_event = {
       "type": "user.created",
       "timestamp": "2025-01-15T10:30:00Z",
       "data": {
           "id": 12345,
           "email": "user@example.com",
           "name": "John Doe"
       }
   }

   result = handler.handle("user.created", user_event)
   print(f"Action: {result['action']}")
   # Output: Action: send_welcome_email

Event Handler with Filters
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add filtering to process only relevant events.

.. code-block:: python

   from typing import Callable

   class FilteredMLEventHandler(MLEventHandler):
       """Event handler with filtering capabilities."""

       def __init__(self, ml_script: str):
           super().__init__(ml_script)
           self.filters: Dict[str, Callable] = {}

       def register_with_filter(
           self,
           event_type: str,
           ml_function: str,
           filter_fn: Callable[[Any], bool]
       ):
           """Register handler with filter function.

           Args:
               event_type: Type of event
               ml_function: ML function name
               filter_fn: Filter function (returns True to process)
           """
           self.register(event_type, ml_function)
           self.filters[event_type] = filter_fn

       def handle(self, event_type: str, event_data: Any) -> Any:
           """Handle event if it passes filter."""
           # Check filter
           if event_type in self.filters:
               if not self.filters[event_type](event_data):
                   return None  # Filtered out

           return super().handle(event_type, event_data)

**Usage:**

.. code-block:: python

   handler = FilteredMLEventHandler("handlers.ml")

   # Only handle high-value orders
   handler.register_with_filter(
       "order.placed",
       "handleOrderPlaced",
       filter_fn=lambda evt: evt["data"]["amount"] > 100.00
   )

   # Only handle verified payments
   handler.register_with_filter(
       "payment.received",
       "handlePaymentReceived",
       filter_fn=lambda evt: evt["data"]["verified"] == True
   )

----

Observer Pattern Implementation
---------------------------------

Implement observer pattern with ML subscribers responding to subject changes.

Observable Subject with ML Observers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from typing import Any, Dict, List
   from mlpy import MLExecutor

   class Observable:
       """Observable subject that notifies ML observers of changes."""

       def __init__(self):
           self.observers: List[MLObserver] = []
           self.state: Any = None

       def attach(self, observer: 'MLObserver'):
           """Attach observer."""
           self.observers.append(observer)
           print(f"Attached observer: {observer}")

       def detach(self, observer: 'MLObserver'):
           """Detach observer."""
           self.observers.remove(observer)

       def notify(self, event_type: str, data: Any):
           """Notify all observers of event."""
           for observer in self.observers:
               observer.update(event_type, data)

       def set_state(self, state: Any):
           """Update state and notify observers."""
           old_state = self.state
           self.state = state
           self.notify("state.changed", {
               "old": old_state,
               "new": state
           })

   class MLObserver:
       """Observer that uses ML function for updates."""

       def __init__(self, name: str, ml_script: str, ml_function: str):
           self.name = name
           self.executor = MLExecutor()
           self.executor.load(ml_script)
           self.ml_function = ml_function

       def update(self, event_type: str, data: Any):
           """Called when observable changes."""
           result = self.executor.call_function(
               self.ml_function,
               {"event": event_type, "data": data}
           )
           print(f"[{self.name}] Processed: {result}")

       def __str__(self):
           return f"MLObserver({self.name})"

**observers.ml:**

.. code-block:: ml

   # Observer functions

   function loggerObserver(update) {
       let timestamp = new Date().toISOString();
       return {
           "level": "info",
           "message": "State changed",
           "event": update.event,
           "old_value": update.data.old,
           "new_value": update.data.new,
           "timestamp": timestamp
       };
   }

   function validatorObserver(update) {
       let newValue = update.data.new;

       if (typeof(newValue) == "number" && newValue < 0) {
           return {
               "valid": false,
               "error": "Value must be non-negative"
           };
       }

       return {"valid": true};
   }

   function alertObserver(update) {
       let newValue = update.data.new;
       let threshold = 1000;

       if (typeof(newValue) == "number" && newValue > threshold) {
           return {
               "alert": true,
               "severity": "warning",
               "message": "Value exceeds threshold",
               "value": newValue,
               "threshold": threshold
           };
       }

       return {"alert": false};
   }

**Usage:**

.. code-block:: python

   # Create observable
   subject = Observable()

   # Create ML observers
   logger = MLObserver("Logger", "observers.ml", "loggerObserver")
   validator = MLObserver("Validator", "observers.ml", "validatorObserver")
   alerter = MLObserver("Alerter", "observers.ml", "alertObserver")

   # Attach observers
   subject.attach(logger)
   subject.attach(validator)
   subject.attach(alerter)

   # Change state - all observers notified
   subject.set_state(500)
   # Output:
   # [Logger] Processed: {'level': 'info', 'message': 'State changed', ...}
   # [Validator] Processed: {'valid': True}
   # [Alerter] Processed: {'alert': False}

   subject.set_state(1500)
   # Output includes alert:
   # [Alerter] Processed: {'alert': True, 'severity': 'warning', ...}

----

Message Queue Integration
---------------------------

Integrate ML with popular message queue systems for distributed event processing.

RabbitMQ Integration
~~~~~~~~~~~~~~~~~~~~~

Consume messages from RabbitMQ and process with ML functions.

**rabbitmq_consumer.py:**

.. code-block:: python

   import pika
   import json
   from mlpy import MLExecutor
   from typing import Callable, Optional

   class RabbitMLConsumer:
       """Consume RabbitMQ messages and process with ML functions."""

       def __init__(
           self,
           ml_script: str,
           host: str = 'localhost',
           port: int = 5672,
           username: str = 'guest',
           password: str = 'guest'
       ):
           """Initialize RabbitMQ consumer.

           Args:
               ml_script: Path to ML script
               host: RabbitMQ host
               port: RabbitMQ port
               username: Authentication username
               password: Authentication password
           """
           self.executor = MLExecutor()
           self.executor.load(ml_script)

           # Connect to RabbitMQ
           credentials = pika.PlainCredentials(username, password)
           parameters = pika.ConnectionParameters(
               host=host,
               port=port,
               credentials=credentials
           )
           self.connection = pika.BlockingConnection(parameters)
           self.channel = self.connection.channel()

       def consume(
           self,
           queue: str,
           ml_function: str,
           auto_ack: bool = False,
           prefetch_count: int = 1
       ):
           """Start consuming messages from queue.

           Args:
               queue: Queue name
               ml_function: ML function to process messages
               auto_ack: Auto-acknowledge messages
               prefetch_count: Number of messages to prefetch
           """
           # Declare queue
           self.channel.queue_declare(queue=queue, durable=True)

           # Set QoS
           self.channel.basic_qos(prefetch_count=prefetch_count)

           def callback(ch, method, properties, body):
               """Process message with ML function."""
               try:
                   # Parse message
                   message = json.loads(body)
                   print(f"Received: {message}")

                   # Process with ML
                   result = self.executor.call_function(ml_function, message)
                   print(f"Processed: {result}")

                   # Acknowledge
                   if not auto_ack:
                       ch.basic_ack(delivery_tag=method.delivery_tag)

               except Exception as e:
                   print(f"Error processing message: {e}")
                   # Reject and requeue
                   if not auto_ack:
                       ch.basic_nack(
                           delivery_tag=method.delivery_tag,
                           requeue=True
                       )

           # Start consuming
           self.channel.basic_consume(
               queue=queue,
               on_message_callback=callback,
               auto_ack=auto_ack
           )

           print(f"Consuming from '{queue}'...")
           self.channel.start_consuming()

       def close(self):
           """Close connection."""
           self.connection.close()

**message_processor.ml:**

.. code-block:: ml

   function processOrder(message) {
       let order = message.order;
       let items = order.items;

       # Calculate totals
       let subtotal = items.reduce(function(sum, item) {
           return sum + (item.price * item.quantity);
       }, 0);

       let tax = subtotal * 0.08;
       let total = subtotal + tax;

       # Apply discount if applicable
       if (order.discount_code) {
           total = total * 0.9;  # 10% off
       }

       return {
           "order_id": order.id,
           "subtotal": subtotal,
           "tax": tax,
           "total": total,
           "status": "processed",
           "processed_at": new Date().toISOString()
       };
   }

   function processPayment(message) {
       let payment = message.payment;

       # Validate payment
       if (payment.amount <= 0) {
           return {
               "status": "rejected",
               "reason": "Invalid amount"
           };
       }

       if (!payment.payment_method) {
           return {
               "status": "rejected",
               "reason": "Missing payment method"
           };
       }

       return {
           "status": "approved",
           "transaction_id": "TXN" + Math.floor(Math.random() * 1000000),
           "amount": payment.amount,
           "payment_method": payment.payment_method
       };
   }

**Usage:**

.. code-block:: python

   # Create consumer
   consumer = RabbitMLConsumer("message_processor.ml")

   # Start consuming orders
   try:
       consumer.consume(
           queue="orders",
           ml_function="processOrder",
           prefetch_count=10
       )
   except KeyboardInterrupt:
       consumer.close()

**Producer Example:**

.. code-block:: python

   import pika
   import json

   # Connect to RabbitMQ
   connection = pika.BlockingConnection(
       pika.ConnectionParameters('localhost')
   )
   channel = connection.channel()

   # Declare queue
   channel.queue_declare(queue='orders', durable=True)

   # Send message
   order = {
       "order": {
           "id": "ORD-12345",
           "items": [
               {"name": "Widget", "price": 29.99, "quantity": 2},
               {"name": "Gadget", "price": 49.99, "quantity": 1}
           ],
           "discount_code": "SAVE10"
       }
   }

   channel.basic_publish(
       exchange='',
       routing_key='orders',
       body=json.dumps(order),
       properties=pika.BasicProperties(
           delivery_mode=2,  # Persistent
       )
   )

   print("Sent order")
   connection.close()

Redis Pub/Sub Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use Redis for lightweight pub/sub messaging.

.. code-block:: python

   import redis
   import json
   from mlpy import MLExecutor
   from typing import Dict, Callable
   import threading

   class RedisMLPubSub:
       """Redis pub/sub with ML message processing."""

       def __init__(
           self,
           ml_script: str,
           host: str = 'localhost',
           port: int = 6379,
           db: int = 0
       ):
           """Initialize Redis pub/sub.

           Args:
               ml_script: Path to ML script
               host: Redis host
               port: Redis port
               db: Redis database number
           """
           self.executor = MLExecutor()
           self.executor.load(ml_script)

           self.redis = redis.Redis(host=host, port=port, db=db)
           self.pubsub = self.redis.pubsub()
           self.handlers: Dict[str, str] = {}
           self.running = False

       def subscribe(self, channel: str, ml_function: str):
           """Subscribe to channel with ML handler.

           Args:
               channel: Channel name
               ml_function: ML function to process messages
           """
           self.pubsub.subscribe(channel)
           self.handlers[channel] = ml_function
           print(f"Subscribed to '{channel}' -> {ml_function}")

       def publish(self, channel: str, message: dict):
           """Publish message to channel.

           Args:
               channel: Channel name
               message: Message dictionary
           """
           self.redis.publish(channel, json.dumps(message))

       def start(self):
           """Start listening for messages."""
           self.running = True
           print("Listening for messages...")

           for message in self.pubsub.listen():
               if not self.running:
                   break

               if message['type'] == 'message':
                   channel = message['channel'].decode('utf-8')
                   data = json.loads(message['data'])

                   if channel in self.handlers:
                       ml_function = self.handlers[channel]
                       result = self.executor.call_function(ml_function, data)
                       print(f"[{channel}] Processed: {result}")

       def start_async(self):
           """Start listening in background thread."""
           thread = threading.Thread(target=self.start, daemon=True)
           thread.start()
           return thread

       def stop(self):
           """Stop listening."""
           self.running = False
           self.pubsub.close()

**pubsub_handlers.ml:**

.. code-block:: ml

   function handleNotification(message) {
       return {
           "type": "notification",
           "user_id": message.user_id,
           "title": message.title,
           "body": message.body,
           "sent_at": new Date().toISOString()
       };
   }

   function handleAnalytics(message) {
       let event = message.event;
       let properties = message.properties;

       return {
           "tracked": true,
           "event_name": event,
           "user_id": properties.user_id,
           "timestamp": new Date().toISOString(),
           "properties": properties
       };
   }

**Usage:**

.. code-block:: python

   # Create pub/sub handler
   pubsub = RedisMLPubSub("pubsub_handlers.ml")

   # Subscribe to channels
   pubsub.subscribe("notifications", "handleNotification")
   pubsub.subscribe("analytics", "handleAnalytics")

   # Start listening in background
   listener = pubsub.start_async()

   # Publish messages
   pubsub.publish("notifications", {
       "user_id": 123,
       "title": "Welcome!",
       "body": "Thanks for signing up"
   })

   pubsub.publish("analytics", {
       "event": "page_view",
       "properties": {
           "user_id": 123,
           "page": "/dashboard",
           "referrer": "/home"
       }
   })

   # Wait for Ctrl+C
   try:
       listener.join()
   except KeyboardInterrupt:
       pubsub.stop()

Kafka Integration
~~~~~~~~~~~~~~~~~~

Process Kafka event streams with ML functions.

.. code-block:: python

   from kafka import KafkaConsumer, KafkaProducer
   import json
   from mlpy import MLExecutor
   from typing import Optional, Callable

   class KafkaMLConsumer:
       """Kafka consumer with ML processing."""

       def __init__(
           self,
           ml_script: str,
           bootstrap_servers: str = 'localhost:9092',
           group_id: str = 'ml-consumer-group'
       ):
           """Initialize Kafka consumer.

           Args:
               ml_script: Path to ML script
               bootstrap_servers: Kafka broker addresses
               group_id: Consumer group ID
           """
           self.executor = MLExecutor()
           self.executor.load(ml_script)

           self.consumer = KafkaConsumer(
               bootstrap_servers=bootstrap_servers,
               group_id=group_id,
               value_deserializer=lambda m: json.loads(m.decode('utf-8')),
               auto_offset_reset='earliest',
               enable_auto_commit=False
           )

       def subscribe_and_process(
           self,
           topics: list,
           ml_function: str,
           batch_size: int = 10
       ):
           """Subscribe to topics and process with ML.

           Args:
               topics: List of topic names
               ml_function: ML function to process messages
               batch_size: Number of messages to process before committing
           """
           self.consumer.subscribe(topics)
           print(f"Subscribed to topics: {topics}")

           batch = []

           try:
               for message in self.consumer:
                   # Process message
                   result = self.executor.call_function(
                       ml_function,
                       message.value
                   )

                   print(f"[{message.topic}] offset={message.offset}, "
                         f"result={result}")

                   batch.append(message)

                   # Commit in batches
                   if len(batch) >= batch_size:
                       self.consumer.commit()
                       batch.clear()

           except KeyboardInterrupt:
               print("Shutting down...")
           finally:
               self.consumer.close()

       def process_with_error_handling(
           self,
           topics: list,
           ml_function: str,
           error_topic: Optional[str] = None
       ):
           """Process messages with error handling.

           Args:
               topics: Topics to consume
               ml_function: ML function name
               error_topic: Topic for failed messages
           """
           self.consumer.subscribe(topics)

           # Create producer for errors if needed
           producer = None
           if error_topic:
               producer = KafkaProducer(
                   bootstrap_servers=self.consumer.config['bootstrap_servers'],
                   value_serializer=lambda m: json.dumps(m).encode('utf-8')
               )

           try:
               for message in self.consumer:
                   try:
                       result = self.executor.call_function(
                           ml_function,
                           message.value
                       )
                       print(f"Success: {result}")
                       self.consumer.commit()

                   except Exception as e:
                       print(f"Error processing message: {e}")

                       # Send to error topic
                       if producer:
                           error_msg = {
                               "original_topic": message.topic,
                               "original_offset": message.offset,
                               "original_value": message.value,
                               "error": str(e)
                           }
                           producer.send(error_topic, error_msg)

                       # Commit to prevent reprocessing
                       self.consumer.commit()

           finally:
               self.consumer.close()
               if producer:
                   producer.close()

**kafka_processor.ml:**

.. code-block:: ml

   function processEvent(event) {
       let eventType = event.type;

       if (eventType == "user_signup") {
           return {
               "action": "send_welcome_email",
               "user_id": event.user_id,
               "email": event.email
           };
       } elif (eventType == "purchase") {
           return {
               "action": "fulfill_order",
               "order_id": event.order_id,
               "amount": event.amount
           };
       } elif (eventType == "support_ticket") {
           return {
               "action": "create_ticket",
               "ticket_id": event.ticket_id,
               "priority": event.priority
           };
       }

       return {"action": "log", "event": event};
   }

**Usage:**

.. code-block:: python

   # Create consumer
   consumer = KafkaMLConsumer(
       "kafka_processor.ml",
       bootstrap_servers='localhost:9092'
   )

   # Process events
   consumer.subscribe_and_process(
       topics=['user-events', 'order-events'],
       ml_function='processEvent',
       batch_size=100
   )

----

Event Sourcing Patterns
-------------------------

Implement event sourcing where ML functions rebuild state from event streams.

Event Store with ML Replay
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from typing import List, Dict, Any
   from mlpy import MLExecutor
   import json
   from datetime import datetime

   class EventStore:
       """Simple event store for event sourcing."""

       def __init__(self, storage_file: str = "events.jsonl"):
           """Initialize event store.

           Args:
               storage_file: File to store events
           """
           self.storage_file = storage_file
           self.events: List[Dict] = []
           self._load_events()

       def append(self, event: Dict):
           """Append event to store."""
           event['timestamp'] = datetime.now().isoformat()
           event['version'] = len(self.events) + 1

           self.events.append(event)

           # Persist
           with open(self.storage_file, 'a') as f:
               f.write(json.dumps(event) + '\n')

       def get_events(
           self,
           entity_id: str = None,
           event_type: str = None,
           from_version: int = 0
       ) -> List[Dict]:
           """Get events with optional filtering."""
           filtered = self.events[from_version:]

           if entity_id:
               filtered = [e for e in filtered
                          if e.get('entity_id') == entity_id]

           if event_type:
               filtered = [e for e in filtered
                          if e.get('type') == event_type]

           return filtered

       def _load_events(self):
           """Load events from storage."""
           try:
               with open(self.storage_file, 'r') as f:
                   for line in f:
                       self.events.append(json.loads(line))
           except FileNotFoundError:
               pass

   class MLEventSourcingProjector:
       """Rebuild entity state from events using ML."""

       def __init__(self, ml_script: str):
           """Initialize projector.

           Args:
               ml_script: ML script with projection functions
           """
           self.executor = MLExecutor()
           self.executor.load(ml_script)

       def project(
           self,
           events: List[Dict],
           ml_function: str,
           initial_state: Any = None
       ) -> Any:
           """Project events into state using ML function.

           Args:
               events: List of events to replay
               ml_function: ML function for projection
               initial_state: Starting state

           Returns:
               Final state after all events
           """
           state = initial_state or {}

           for event in events:
               state = self.executor.call_function(
                   ml_function,
                   {"state": state, "event": event}
               )

           return state

**projections.ml:**

.. code-block:: ml

   # Account balance projection
   function projectAccountBalance(input) {
       let state = input.state;
       let event = input.event;

       # Initialize state if needed
       if (!state.balance) {
           state.balance = 0;
           state.transactions = [];
       }

       # Apply event
       if (event.type == "deposit") {
           state.balance = state.balance + event.amount;
           state.transactions.push({
               "type": "deposit",
               "amount": event.amount,
               "timestamp": event.timestamp
           });
       } elif (event.type == "withdrawal") {
           state.balance = state.balance - event.amount;
           state.transactions.push({
               "type": "withdrawal",
               "amount": event.amount,
               "timestamp": event.timestamp
           });
       } elif (event.type == "interest") {
           let interest = state.balance * event.rate;
           state.balance = state.balance + interest;
           state.transactions.push({
               "type": "interest",
               "amount": interest,
               "timestamp": event.timestamp
           });
       }

       return state;
   }

   # Shopping cart projection
   function projectShoppingCart(input) {
       let state = input.state;
       let event = input.event;

       if (!state.items) {
           state.items = [];
           state.total = 0;
       }

       if (event.type == "item_added") {
           state.items.push(event.item);
           state.total = state.total + event.item.price;
       } elif (event.type == "item_removed") {
           let index = state.items.findIndex(function(item) {
               return item.id == event.item_id;
           });
           if (index >= 0) {
               let removed = state.items.splice(index, 1)[0];
               state.total = state.total - removed.price;
           }
       } elif (event.type == "checkout") {
           state.checked_out = true;
           state.checkout_time = event.timestamp;
       }

       return state;
   }

**Usage:**

.. code-block:: python

   # Create event store
   store = EventStore("account_events.jsonl")

   # Append events
   store.append({
       "type": "deposit",
       "entity_id": "account-123",
       "amount": 1000.00
   })

   store.append({
       "type": "withdrawal",
       "entity_id": "account-123",
       "amount": 250.00
   })

   store.append({
       "type": "interest",
       "entity_id": "account-123",
       "rate": 0.02
   })

   # Rebuild state from events
   projector = MLEventSourcingProjector("projections.ml")
   events = store.get_events(entity_id="account-123")

   final_state = projector.project(
       events,
       "projectAccountBalance",
       initial_state={}
   )

   print(f"Final balance: ${final_state['balance']:.2f}")
   # Output: Final balance: $765.00
   print(f"Transaction count: {len(final_state['transactions'])}")
   # Output: Transaction count: 3

----

Reactive Programming with RxPY
--------------------------------

Integrate ML with reactive programming for complex event stream processing.

ML Operators for Observable Streams
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from rx import operators as ops
   from rx.subject import Subject
   from mlpy import MLExecutor
   from typing import Any, Callable

   class MLOperators:
       """Custom RxPY operators using ML functions."""

       @staticmethod
       def map_ml(ml_script: str, ml_function: str):
           """Map operator using ML function.

           Args:
               ml_script: Path to ML script
               ml_function: ML function name

           Returns:
               RxPY operator
           """
           executor = MLExecutor()
           executor.load(ml_script)

           def mapper(value: Any) -> Any:
               return executor.call_function(ml_function, value)

           return ops.map(mapper)

       @staticmethod
       def filter_ml(ml_script: str, ml_function: str):
           """Filter operator using ML predicate.

           Args:
               ml_script: Path to ML script
               ml_function: ML predicate function (returns boolean)

           Returns:
               RxPY operator
           """
           executor = MLExecutor()
           executor.load(ml_script)

           def predicate(value: Any) -> bool:
               result = executor.call_function(ml_function, value)
               return bool(result)

           return ops.filter(predicate)

       @staticmethod
       def scan_ml(ml_script: str, ml_function: str, initial_state: Any):
           """Scan (reduce) operator using ML function.

           Args:
               ml_script: Path to ML script
               ml_function: ML reducer function
               initial_state: Initial accumulator value

           Returns:
               RxPY operator
           """
           executor = MLExecutor()
           executor.load(ml_script)

           def accumulator(acc: Any, value: Any) -> Any:
               return executor.call_function(
                   ml_function,
                   {"accumulator": acc, "value": value}
               )

           return ops.scan(accumulator, initial_state)

**reactive_handlers.ml:**

.. code-block:: ml

   # Transform event data
   function transformEvent(event) {
       return {
           "id": event.id,
           "type": event.type,
           "value": event.value * 2,
           "processed": true
       };
   }

   # Filter high-value events
   function isHighValue(event) {
       return event.value > 100;
   }

   # Accumulate totals
   function accumulateTotal(input) {
       let acc = input.accumulator;
       let event = input.value;

       return {
           "total": acc.total + event.value,
           "count": acc.count + 1,
           "average": (acc.total + event.value) / (acc.count + 1)
       };
   }

   # Detect patterns
   function detectPattern(input) {
       let acc = input.accumulator;
       let event = input.value;

       # Track last 3 values
       if (!acc.recent) {
           acc.recent = [];
       }

       acc.recent.push(event.value);
       if (acc.recent.length > 3) {
           acc.recent.shift();
       }

       # Detect increasing pattern
       if (acc.recent.length == 3) {
           let increasing = acc.recent[0] < acc.recent[1] &&
                           acc.recent[1] < acc.recent[2];
           acc.pattern = increasing ? "increasing" : "stable";
       }

       return acc;
   }

**Usage:**

.. code-block:: python

   from rx.subject import Subject

   # Create observable stream
   events = Subject()

   # Build pipeline with ML operators
   events.pipe(
       MLOperators.filter_ml("reactive_handlers.ml", "isHighValue"),
       MLOperators.map_ml("reactive_handlers.ml", "transformEvent"),
       MLOperators.scan_ml(
           "reactive_handlers.ml",
           "accumulateTotal",
           initial_state={"total": 0, "count": 0, "average": 0}
       )
   ).subscribe(lambda x: print(f"Accumulated: {x}"))

   # Emit events
   events.on_next({"id": 1, "type": "sale", "value": 50})   # Filtered out
   events.on_next({"id": 2, "type": "sale", "value": 150})  # Processed
   events.on_next({"id": 3, "type": "sale", "value": 200})  # Processed

   # Output:
   # Accumulated: {'total': 300, 'count': 1, 'average': 300.0}
   # Accumulated: {'total': 700, 'count': 2, 'average': 350.0}

Complex Event Processing Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from rx import operators as ops
   from rx.subject import Subject
   import time

   # Create event stream
   stock_prices = Subject()

   # Complex processing pipeline
   stock_prices.pipe(
       # Filter ML stocks
       MLOperators.filter_ml("reactive_handlers.ml", "isHighValue"),

       # Transform to signals
       MLOperators.map_ml("reactive_handlers.ml", "transformEvent"),

       # Detect patterns in sliding window
       ops.buffer_with_time(5.0),  # 5 second windows
       ops.filter(lambda buffer: len(buffer) > 0),
       MLOperators.map_ml("reactive_handlers.ml", "analyzeWindow"),

       # Accumulate insights
       MLOperators.scan_ml(
           "reactive_handlers.ml",
           "detectPattern",
           initial_state={}
       )
   ).subscribe(
       on_next=lambda pattern: print(f"Pattern detected: {pattern}"),
       on_error=lambda e: print(f"Error: {e}"),
       on_completed=lambda: print("Stream completed")
   )

----

Complete Working Examples
---------------------------

Example 1: Real-Time Analytics Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Process user activity events in real-time with ML analytics.

**analytics_pipeline.py:**

.. code-block:: python

   from rx import operators as ops
   from rx.subject import Subject
   from mlpy import MLExecutor
   import json
   from datetime import datetime
   from typing import Dict, Any

   class RealTimeAnalytics:
       """Real-time analytics using ML processors."""

       def __init__(self, ml_script: str):
           """Initialize analytics pipeline."""
           self.executor = MLExecutor()
           self.executor.load(ml_script)

           # Event streams
           self.raw_events = Subject()
           self.processed_events = Subject()
           self.insights = Subject()

           self._setup_pipeline()

       def _setup_pipeline(self):
           """Setup reactive processing pipeline."""

           # Process raw events
           self.raw_events.pipe(
               ops.map(lambda e: self._enrich_event(e)),
               ops.filter(lambda e: self._validate_event(e))
           ).subscribe(self.processed_events)

           # Generate insights
           self.processed_events.pipe(
               ops.buffer_with_time(10.0),  # 10 second windows
               ops.filter(lambda events: len(events) > 0),
               ops.map(lambda events: self._analyze_batch(events))
           ).subscribe(self.insights)

           # Subscribe to insights
           self.insights.subscribe(
               on_next=lambda insight: self._handle_insight(insight)
           )

       def _enrich_event(self, event: Dict) -> Dict:
           """Enrich event with ML processing."""
           return self.executor.call_function("enrichEvent", event)

       def _validate_event(self, event: Dict) -> bool:
           """Validate event."""
           result = self.executor.call_function("validateEvent", event)
           return result.get("valid", False)

       def _analyze_batch(self, events: list) -> Dict:
           """Analyze batch of events."""
           return self.executor.call_function("analyzeBatch", events)

       def _handle_insight(self, insight: Dict):
           """Handle generated insight."""
           print(f"\n=== INSIGHT ===")
           print(f"Type: {insight.get('type')}")
           print(f"Value: {insight.get('value')}")
           print(f"Timestamp: {datetime.now().isoformat()}")

       def track_event(self, event_type: str, properties: Dict):
           """Track user event."""
           event = {
               "type": event_type,
               "properties": properties,
               "timestamp": datetime.now().isoformat()
           }
           self.raw_events.on_next(event)

**analytics.ml:**

.. code-block:: ml

   function enrichEvent(event) {
       # Add computed fields
       event.hour = parseInt(event.timestamp.substring(11, 13));
       event.day_of_week = new Date(event.timestamp).getDay();

       # Categorize event
       if (event.type.startsWith("page_")) {
           event.category = "navigation";
       } elif (event.type.startsWith("click_")) {
           event.category = "interaction";
       } elif (event.type.startsWith("form_")) {
           event.category = "conversion";
       }

       return event;
   }

   function validateEvent(event) {
       # Check required fields
       if (!event.type || !event.timestamp) {
           return {"valid": false, "reason": "Missing required fields"};
       }

       # Check timestamp format
       if (event.timestamp.length < 19) {
           return {"valid": false, "reason": "Invalid timestamp"};
       }

       return {"valid": true};
   }

   function analyzeBatch(events) {
       # Count by category
       let categories = {};
       let i = 0;
       while (i < events.length) {
           let event = events[i];
           let cat = event.category || "other";
           categories[cat] = (categories[cat] || 0) + 1;
           i = i + 1;
       }

       # Find most common
       let maxCat = "";
       let maxCount = 0;
       let keys = Object.keys(categories);
       let j = 0;
       while (j < keys.length) {
           let cat = keys[j];
           if (categories[cat] > maxCount) {
               maxCount = categories[cat];
               maxCat = cat;
           }
           j = j + 1;
       }

       return {
           "type": "batch_analysis",
           "value": {
               "total_events": events.length,
               "by_category": categories,
               "most_common": maxCat,
               "most_common_count": maxCount
           }
       };
   }

**Usage:**

.. code-block:: python

   # Create analytics pipeline
   analytics = RealTimeAnalytics("analytics.ml")

   # Track events
   analytics.track_event("page_view", {"url": "/home"})
   analytics.track_event("click_button", {"button": "signup"})
   analytics.track_event("form_submit", {"form": "contact"})
   analytics.track_event("page_view", {"url": "/pricing"})
   analytics.track_event("click_link", {"link": "documentation"})

   # Wait for batch processing
   import time
   time.sleep(11)  # Wait for 10 second window + processing

   # Output (after 10 seconds):
   # === INSIGHT ===
   # Type: batch_analysis
   # Value: {'total_events': 5, 'by_category': {...}, ...}

Example 2: Event-Driven Workflow Engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Orchestrate multi-step workflows using events and ML state machines.

**workflow_engine.py:**

.. code-block:: python

   from typing import Dict, List, Any, Callable
   from mlpy import MLExecutor
   from enum import Enum
   import uuid

   class WorkflowStatus(Enum):
       PENDING = "pending"
       RUNNING = "running"
       COMPLETED = "completed"
       FAILED = "failed"

   class Workflow:
       """Event-driven workflow with ML step execution."""

       def __init__(
           self,
           workflow_id: str,
           ml_script: str,
           steps: List[str]
       ):
           """Initialize workflow.

           Args:
               workflow_id: Unique workflow identifier
               ml_script: ML script with step functions
               steps: List of ML function names to execute
           """
           self.workflow_id = workflow_id
           self.executor = MLExecutor()
           self.executor.load(ml_script)
           self.steps = steps
           self.current_step = 0
           self.status = WorkflowStatus.PENDING
           self.context: Dict[str, Any] = {}
           self.results: List[Any] = []

       def execute_next_step(self) -> Dict:
           """Execute next step in workflow."""
           if self.current_step >= len(self.steps):
               self.status = WorkflowStatus.COMPLETED
               return {
                   "status": "completed",
                   "workflow_id": self.workflow_id,
                   "results": self.results
               }

           self.status = WorkflowStatus.RUNNING
           step_name = self.steps[self.current_step]

           try:
               # Execute ML step function
               result = self.executor.call_function(
                   step_name,
                   self.context
               )

               # Update context with result
               self.context.update(result)
               self.results.append(result)

               self.current_step += 1

               return {
                   "status": "step_completed",
                   "workflow_id": self.workflow_id,
                   "step": step_name,
                   "result": result
               }

           except Exception as e:
               self.status = WorkflowStatus.FAILED
               return {
                   "status": "failed",
                   "workflow_id": self.workflow_id,
                   "step": step_name,
                   "error": str(e)
               }

   class WorkflowEngine:
       """Manage multiple workflows with event-driven execution."""

       def __init__(self, ml_script: str):
           """Initialize workflow engine."""
           self.ml_script = ml_script
           self.workflows: Dict[str, Workflow] = {}
           self.event_handlers: Dict[str, Callable] = {}

       def create_workflow(self, steps: List[str]) -> str:
           """Create new workflow.

           Args:
               steps: List of ML function names

           Returns:
               Workflow ID
           """
           workflow_id = str(uuid.uuid4())
           workflow = Workflow(workflow_id, self.ml_script, steps)
           self.workflows[workflow_id] = workflow

           # Emit created event
           self._emit_event("workflow.created", {
               "workflow_id": workflow_id,
               "steps": steps
           })

           return workflow_id

       def handle_event(self, event_type: str, event_data: Dict):
           """Handle workflow event."""
           if event_type == "workflow.created":
               # Start workflow
               workflow_id = event_data["workflow_id"]
               self._start_workflow(workflow_id)

           elif event_type == "step.completed":
               # Continue workflow
               workflow_id = event_data["workflow_id"]
               self._continue_workflow(workflow_id)

           elif event_type == "workflow.completed":
               print(f"Workflow {event_data['workflow_id']} completed!")

       def _start_workflow(self, workflow_id: str):
           """Start workflow execution."""
           workflow = self.workflows[workflow_id]
           result = workflow.execute_next_step()

           if result["status"] == "step_completed":
               self._emit_event("step.completed", result)
           elif result["status"] == "failed":
               self._emit_event("workflow.failed", result)

       def _continue_workflow(self, workflow_id: str):
           """Continue workflow execution."""
           workflow = self.workflows[workflow_id]
           result = workflow.execute_next_step()

           if result["status"] == "step_completed":
               self._emit_event("step.completed", result)
           elif result["status"] == "completed":
               self._emit_event("workflow.completed", result)
           elif result["status"] == "failed":
               self._emit_event("workflow.failed", result)

       def _emit_event(self, event_type: str, event_data: Dict):
           """Emit workflow event."""
           print(f"Event: {event_type}")
           self.handle_event(event_type, event_data)

**workflow_steps.ml:**

.. code-block:: ml

   # Step 1: Initialize order
   function initializeOrder(context) {
       return {
           "order_id": "ORD-" + Math.floor(Math.random() * 100000),
           "status": "initialized",
           "created_at": new Date().toISOString()
       };
   }

   # Step 2: Validate inventory
   function validateInventory(context) {
       let orderId = context.order_id;

       # Simulate inventory check
       let available = true;

       return {
           "inventory_validated": available,
           "validation_time": new Date().toISOString()
       };
   }

   # Step 3: Process payment
   function processPayment(context) {
       if (!context.inventory_validated) {
           throw "Inventory not validated";
       }

       return {
           "payment_status": "approved",
           "transaction_id": "TXN-" + Math.floor(Math.random() * 100000),
           "payment_time": new Date().toISOString()
       };
   }

   # Step 4: Fulfill order
   function fulfillOrder(context) {
       if (context.payment_status != "approved") {
           throw "Payment not approved";
       }

       return {
           "fulfillment_status": "shipped",
           "tracking_number": "TRK-" + Math.floor(Math.random() * 100000),
           "shipped_at": new Date().toISOString()
       };
   }

**Usage:**

.. code-block:: python

   # Create workflow engine
   engine = WorkflowEngine("workflow_steps.ml")

   # Create order fulfillment workflow
   workflow_id = engine.create_workflow([
       "initializeOrder",
       "validateInventory",
       "processPayment",
       "fulfillOrder"
   ])

   # Output:
   # Event: workflow.created
   # Event: step.completed
   # Event: step.completed
   # Event: step.completed
   # Event: step.completed
   # Event: workflow.completed
   # Workflow <id> completed!

----

Best Practices
---------------

Event Handler Design
~~~~~~~~~~~~~~~~~~~~~

**1. Keep Handlers Idempotent:**

Handlers should produce same result when called multiple times with same input.

.. code-block:: ml

   # Good: Idempotent
   function handleEvent(event) {
       return {
           "event_id": event.id,
           "processed": true,
           "timestamp": event.timestamp  # Use event timestamp, not current time
       };
   }

   # Avoid: Non-idempotent
   function handleEvent(event) {
       return {
           "processed": true,
           "timestamp": new Date().toISOString()  # Changes each call
       };
   }

**2. Handle Failures Gracefully:**

Always include error handling in event processors.

.. code-block:: python

   def safe_handle(self, event_type: str, event_data: Any) -> dict:
       """Handle event with error recovery."""
       try:
           result = self.executor.call_function(
               self.handlers[event_type],
               event_data
           )
           return {"status": "success", "result": result}

       except Exception as e:
           return {
               "status": "error",
               "error": str(e),
               "event": event_data
           }

**3. Use Dead Letter Queues:**

Route failed messages to dead letter queue for analysis.

.. code-block:: python

   if result["status"] == "error":
       # Send to DLQ
       dlq.publish("failed_events", {
           "original_event": event_data,
           "error": result["error"],
           "timestamp": datetime.now().isoformat()
       })

Message Queue Best Practices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Enable Message Persistence:**

.. code-block:: python

   # RabbitMQ
   channel.queue_declare(queue='events', durable=True)
   properties = pika.BasicProperties(delivery_mode=2)  # Persistent

   # Kafka
   producer = KafkaProducer(acks='all')  # Wait for all replicas

**2. Use Appropriate Acknowledgment:**

.. code-block:: python

   # Manual acknowledgment for reliable processing
   def callback(ch, method, properties, body):
       try:
           process_message(body)
           ch.basic_ack(delivery_tag=method.delivery_tag)
       except Exception:
           ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

**3. Implement Backpressure:**

.. code-block:: python

   # Limit concurrent processing
   channel.basic_qos(prefetch_count=10)

Event Sourcing Best Practices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Never Modify Past Events:**

Events are immutable historical records.

.. code-block:: python

   # Good: Append new event
   store.append({
       "type": "correction",
       "corrects": previous_event_id,
       "amount": corrected_amount
   })

   # Bad: Modify existing event
   # event['amount'] = corrected_amount  # NEVER DO THIS

**2. Use Snapshots for Performance:**

.. code-block:: python

   class SnapshotStore:
       """Store state snapshots to speed up replay."""

       def save_snapshot(self, entity_id: str, version: int, state: Any):
           """Save state snapshot."""
           self.snapshots[entity_id] = {
               "version": version,
               "state": state,
               "timestamp": datetime.now()
           }

       def rebuild_from_snapshot(
           self,
           entity_id: str,
           events: List[Dict]
       ) -> Any:
           """Rebuild state from snapshot + recent events."""
           snapshot = self.snapshots.get(entity_id)
           if snapshot:
               # Start from snapshot
               state = snapshot["state"]
               version = snapshot["version"]
               # Replay only events after snapshot
               events = [e for e in events if e["version"] > version]
           else:
               state = {}

           # Replay remaining events
           for event in events:
               state = self.apply_event(state, event)

           return state

----

Common Pitfalls
----------------

1. Memory Leaks in Long-Running Consumers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Event handlers accumulate state over time.

**Solution:** Clear state periodically or use bounded collections.

.. code-block:: python

   from collections import deque

   class BoundedEventHandler:
       def __init__(self, ml_script: str, max_history: int = 1000):
           self.executor = MLExecutor()
           self.executor.load(ml_script)
           self.recent_events = deque(maxlen=max_history)  # Auto-evicts old

       def handle(self, event: dict):
           result = self.executor.call_function("handleEvent", event)
           self.recent_events.append(event)  # Bounded
           return result

2. Event Ordering Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Events processed out of order in distributed systems.

**Solution:** Use sequence numbers and buffering.

.. code-block:: python

   class OrderedEventHandler:
       def __init__(self):
           self.next_sequence = 0
           self.buffer: Dict[int, dict] = {}  # sequence -> event

       def handle(self, event: dict):
           sequence = event["sequence"]

           if sequence == self.next_sequence:
               # Process immediately
               self._process(event)
               self.next_sequence += 1

               # Process buffered events
               while self.next_sequence in self.buffer:
                   buffered = self.buffer.pop(self.next_sequence)
                   self._process(buffered)
                   self.next_sequence += 1
           else:
               # Buffer for later
               self.buffer[sequence] = event

3. Poison Messages
~~~~~~~~~~~~~~~~~~~

**Problem:** Malformed messages cause repeated failures.

**Solution:** Limit retries and use dead letter queue.

.. code-block:: python

   MAX_RETRIES = 3

   def handle_with_retry(message: dict):
       retries = message.get("_retries", 0)

       try:
           process_message(message)
       except Exception as e:
           if retries < MAX_RETRIES:
               # Retry
               message["_retries"] = retries + 1
               requeue_message(message)
           else:
               # Send to DLQ
               dlq.send(message, error=str(e))

----

Troubleshooting
----------------

Event Not Being Processed
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Check event handler registration:**

.. code-block:: python

   print(f"Registered handlers: {handler.handlers}")

   # Verify ML function exists
   if not executor.has_function("handleEvent"):
       print("ERROR: Function not found")

**Check message format:**

.. code-block:: python

   # Enable debug logging
   import logging
   logging.basicConfig(level=logging.DEBUG)

   def callback(ch, method, properties, body):
       print(f"Raw message: {body}")
       message = json.loads(body)
       print(f"Parsed message: {message}")

Message Queue Connection Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**RabbitMQ connection troubleshooting:**

.. code-block:: python

   try:
       connection = pika.BlockingConnection(parameters)
       print("Connected to RabbitMQ")
   except pika.exceptions.AMQPConnectionError as e:
       print(f"Connection failed: {e}")
       print("Check: host, port, credentials, firewall")

**Kafka connection troubleshooting:**

.. code-block:: python

   from kafka.errors import NoBrokersAvailable

   try:
       consumer = KafkaConsumer(bootstrap_servers='localhost:9092')
       print("Connected to Kafka")
   except NoBrokersAvailable:
       print("No Kafka brokers available")
       print("Check: broker address, broker status")

Performance Degradation
~~~~~~~~~~~~~~~~~~~~~~~~

**Profile ML execution:**

.. code-block:: python

   import time

   start = time.time()
   result = executor.call_function("handleEvent", event)
   duration = time.time() - start

   if duration > 0.1:  # 100ms threshold
       print(f"SLOW: Event processing took {duration:.3f}s")

**Monitor queue depth:**

.. code-block:: python

   # RabbitMQ
   queue_info = channel.queue_declare(queue='events', passive=True)
   message_count = queue_info.method.message_count
   print(f"Queue depth: {message_count}")

   if message_count > 1000:
       print("WARNING: Queue backlog detected")
       # Scale up consumers

----

Summary
--------

Event-driven integration enables ML functions to participate in reactive architectures:

**Key Patterns:**
- Event handlers for decoupled processing
- Observer pattern for state monitoring
- Message queues for distributed systems
- Event sourcing for audit trails
- Reactive programming for stream processing

**Best Practices:**
- Keep handlers idempotent
- Use dead letter queues
- Implement backpressure
- Monitor queue depth
- Profile performance

**Production Considerations:**
- Message persistence
- Error handling and retries
- Connection pooling
- Monitoring and alerting
- Scalability planning

Event-driven architecture with ML provides a powerful foundation for building scalable, resilient systems that respond to real-time events.

----

Next: :doc:`framework-specific` - Framework-specific integration patterns (Flask, Django, Qt, Streamlit)
