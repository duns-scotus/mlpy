Database Integration
=====================

.. note::
   **Chapter Summary:** Integrating ML with SQL and NoSQL databases for data processing, query building, and transaction management.

This chapter covers database integration patterns where ML functions interact with relational and non-relational databases. You'll learn how to use ML for query building, data transformation, and business logic while maintaining database integrity.

----

SQL Database Integration
-------------------------

ML functions can process database results, build queries, and transform data for persistence.

SQLite Integration
~~~~~~~~~~~~~~~~~~~

Simple SQL database integration with ML processing.

**sql_integration.py:**

.. code-block:: python

   import sqlite3
   from mlpy import MLExecutor
   from typing import List, Dict, Any

   class MLSQLiteDB:
       """SQLite database with ML processing."""

       def __init__(self, db_path: str, ml_script: str):
           self.conn = sqlite3.connect(db_path)
           self.conn.row_factory = sqlite3.Row  # Enable column access by name
           self.executor = MLExecutor()
           self.executor.load(ml_script)

       def query_and_process(
           self,
           query: str,
           params: tuple,
           ml_function: str
       ) -> Any:
           """Execute query and process results with ML.

           Args:
               query: SQL query
               params: Query parameters
               ml_function: ML function to process results

           Returns:
               Processed results from ML function
           """
           cursor = self.conn.cursor()
           cursor.execute(query, params)

           # Fetch results as dicts
           rows = [dict(row) for row in cursor.fetchall()]

           # Process with ML
           result = self.executor.call_function(ml_function, {
               "rows": rows,
               "count": len(rows)
           })

           return result

       def insert_with_ml(
           self,
           table: str,
           data: Dict[str, Any],
           ml_function: str
       ):
           """Process data with ML before inserting.

           Args:
               table: Table name
               data: Data to insert
               ml_function: ML function to process data
           """
           # Process data with ML
           processed = self.executor.call_function(ml_function, data)

           # Build INSERT query
           columns = ', '.join(processed.keys())
           placeholders = ', '.join(['?' for _ in processed])
           query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

           # Execute
           cursor = self.conn.cursor()
           cursor.execute(query, tuple(processed.values()))
           self.conn.commit()

           return cursor.lastrowid

       def close(self):
           """Close database connection."""
           self.conn.close()

**db_processors.ml:**

.. code-block:: ml

   function processUsers(data) {
       let rows = data.rows;

       # Calculate statistics
       let totalAge = rows.reduce(function(sum, user) {
           return sum + user.age;
       }, 0);

       let avgAge = totalAge / rows.length;

       # Group by domain
       let domains = {};
       let i = 0;
       while (i < rows.length) {
           let user = rows[i];
           let domain = user.email.split("@")[1];
           domains[domain] = (domains[domain] || 0) + 1;
           i = i + 1;
       }

       return {
           "total_users": rows.length,
           "average_age": avgAge,
           "domains": domains,
           "users": rows
       };
   }

   function validateUser(user) {
       let errors = [];

       # Validate name
       if (!user.name || user.name.length < 2) {
           errors.push("Name must be at least 2 characters");
       }

       # Validate email
       if (!user.email || user.email.indexOf("@") < 0) {
           errors.push("Invalid email address");
       }

       # Validate age
       if (!user.age || user.age < 0 || user.age > 150) {
           errors.push("Age must be between 0 and 150");
       }

       if (errors.length > 0) {
           throw "Validation failed: " + errors.join(", ");
       }

       return user;
   }

**Usage:**

.. code-block:: python

   # Create database
   db = MLSQLiteDB("users.db", "db_processors.ml")

   # Create table
   db.conn.execute('''
       CREATE TABLE IF NOT EXISTS users (
           id INTEGER PRIMARY KEY,
           name TEXT NOT NULL,
           email TEXT NOT NULL,
           age INTEGER
       )
   ''')
   db.conn.commit()

   # Insert with ML validation
   try:
       user_id = db.insert_with_ml(
           "users",
           {"name": "John Doe", "email": "john@example.com", "age": 30},
           "validateUser"
       )
       print(f"Inserted user ID: {user_id}")
   except Exception as e:
       print(f"Validation failed: {e}")

   # Query and process
   result = db.query_and_process(
       "SELECT * FROM users WHERE age > ?",
       (25,),
       "processUsers"
   )

   print(f"Total users: {result['total_users']}")
   print(f"Average age: {result['average_age']:.1f}")
   print(f"Domains: {result['domains']}")

PostgreSQL Integration
~~~~~~~~~~~~~~~~~~~~~~~

Production-grade PostgreSQL integration with connection pooling.

.. code-block:: python

   import psycopg2
   from psycopg2 import pool
   from mlpy import MLExecutor
   from typing import List, Dict, Any
   import json

   class MLPostgresDB:
       """PostgreSQL database with ML processing."""

       def __init__(
           self,
           ml_script: str,
           min_connections: int = 1,
           max_connections: int = 10,
           **db_params
       ):
           """Initialize with connection pool.

           Args:
               ml_script: Path to ML script
               min_connections: Minimum connections in pool
               max_connections: Maximum connections in pool
               **db_params: Database connection parameters
           """
           self.pool = pool.SimpleConnectionPool(
               min_connections,
               max_connections,
               **db_params
           )
           self.executor = MLExecutor()
           self.executor.load(ml_script)

       def execute_with_ml(
           self,
           query: str,
           params: tuple,
           ml_function: str,
           return_results: bool = True
       ) -> Any:
           """Execute query and process with ML."""
           conn = self.pool.getconn()
           try:
               cursor = conn.cursor()
               cursor.execute(query, params)

               if return_results:
                   # Fetch results
                   columns = [desc[0] for desc in cursor.description]
                   rows = cursor.fetchall()

                   # Convert to dicts
                   data = [dict(zip(columns, row)) for row in rows]

                   # Process with ML
                   result = self.executor.call_function(ml_function, {
                       "rows": data,
                       "count": len(data)
                   })

                   return result
               else:
                   conn.commit()
                   return {"affected_rows": cursor.rowcount}

           finally:
               self.pool.putconn(conn)

       def batch_insert(
           self,
           table: str,
           records: List[Dict[str, Any]],
           ml_function: str = None
       ):
           """Batch insert with optional ML processing."""
           conn = self.pool.getconn()
           try:
               # Process records with ML if function provided
               if ml_function:
                   processed = self.executor.call_function(ml_function, {
                       "records": records
                   })
                   records = processed["records"]

               # Build batch insert
               if not records:
                   return 0

               columns = list(records[0].keys())
               placeholders = ', '.join(['%s' for _ in columns])
               column_names = ', '.join(columns)

               query = f"""
                   INSERT INTO {table} ({column_names})
                   VALUES ({placeholders})
               """

               cursor = conn.cursor()
               cursor.executemany(
                   query,
                   [tuple(r[col] for col in columns) for r in records]
               )

               conn.commit()
               return cursor.rowcount

           finally:
               self.pool.putconn(conn)

       def close(self):
           """Close all connections."""
           self.pool.closeall()

**postgres_processors.ml:**

.. code-block:: ml

   function processOrders(data) {
       let rows = data.rows;

       # Calculate totals
       let totalRevenue = rows.reduce(function(sum, order) {
           return sum + order.total;
       }, 0);

       # Group by status
       let byStatus = {};
       let i = 0;
       while (i < rows.length) {
           let order = rows[i];
           let status = order.status;

           if (!byStatus[status]) {
               byStatus[status] = {
                   "count": 0,
                   "revenue": 0
               };
           }

           byStatus[status].count = byStatus[status].count + 1;
           byStatus[status].revenue = byStatus[status].revenue + order.total;

           i = i + 1;
       }

       return {
           "total_orders": rows.length,
           "total_revenue": totalRevenue,
           "average_order": totalRevenue / rows.length,
           "by_status": byStatus
       };
   }

   function processRecords(data) {
       let records = data.records;

       # Add timestamps and validate
       let processed = records.map(function(record) {
           record.created_at = new Date().toISOString();
           record.processed = true;
           return record;
       });

       return {"records": processed};
   }

**Usage:**

.. code-block:: python

   # Create database connection
   db = MLPostgresDB(
       "postgres_processors.ml",
       database="mydb",
       user="user",
       password="password",
       host="localhost",
       port=5432
   )

   # Query and process
   result = db.execute_with_ml(
       "SELECT * FROM orders WHERE created_at > %s",
       (datetime.now() - timedelta(days=7),),
       "processOrders"
   )

   print(f"Weekly revenue: ${result['total_revenue']:.2f}")
   print(f"Orders by status: {result['by_status']}")

   # Batch insert with processing
   new_records = [
       {"product": "Widget", "quantity": 10, "price": 29.99},
       {"product": "Gadget", "quantity": 5, "price": 49.99}
   ]

   count = db.batch_insert("products", new_records, "processRecords")
   print(f"Inserted {count} records")

   db.close()

----

ORM Integration
----------------

Integrate ML with SQLAlchemy ORM for object-relational mapping.

SQLAlchemy with ML
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker, Session
   from mlpy import MLExecutor
   from datetime import datetime
   from typing import List, Dict, Any

   Base = declarative_base()

   class Product(Base):
       """Product model."""

       __tablename__ = 'products'

       id = Column(Integer, primary_key=True)
       name = Column(String, nullable=False)
       price = Column(Float, nullable=False)
       stock = Column(Integer, default=0)
       created_at = Column(DateTime, default=datetime.now)

       def to_dict(self):
           """Convert to dict for ML processing."""
           return {
               "id": self.id,
               "name": self.name,
               "price": self.price,
               "stock": self.stock,
               "created_at": self.created_at.isoformat()
           }

       @classmethod
       def from_dict(cls, data: dict):
           """Create from dict."""
           return cls(
               name=data["name"],
               price=data["price"],
               stock=data.get("stock", 0)
           )

   class MLQueryBuilder:
       """Build queries with ML assistance."""

       def __init__(self, session: Session, ml_script: str):
           self.session = session
           self.executor = MLExecutor()
           self.executor.load(ml_script)

       def query_and_process(
           self,
           model,
           filters: Dict[str, Any],
           ml_function: str
       ) -> Any:
           """Query ORM and process with ML.

           Args:
               model: SQLAlchemy model class
               filters: Query filters
               ml_function: ML function to process results

           Returns:
               Processed results from ML
           """
           # Build query
           query = self.session.query(model)

           # Apply filters
           for key, value in filters.items():
               if hasattr(model, key):
                   query = query.filter(getattr(model, key) == value)

           # Execute query
           results = query.all()

           # Convert to dicts
           data = [item.to_dict() for item in results]

           # Process with ML
           return self.executor.call_function(ml_function, {
               "items": data,
               "count": len(data)
           })

       def create_with_ml(
           self,
           model,
           data: Dict[str, Any],
           ml_function: str
       ):
           """Create record with ML processing.

           Args:
               model: SQLAlchemy model class
               data: Data for new record
               ml_function: ML function to process data

           Returns:
               Created model instance
           """
           # Process data with ML
           processed = self.executor.call_function(ml_function, data)

           # Create model instance
           instance = model.from_dict(processed)

           # Save to database
           self.session.add(instance)
           self.session.commit()

           return instance

**orm_processors.ml:**

.. code-block:: ml

   function analyzeProducts(data) {
       let items = data.items;

       # Calculate statistics
       let totalValue = items.reduce(function(sum, product) {
           return sum + (product.price * product.stock);
       }, 0);

       let avgPrice = items.reduce(function(sum, p) {
           return sum + p.price;
       }, 0) / items.length;

       # Find low stock items
       let lowStock = items.filter(function(p) {
           return p.stock < 10;
       });

       # Group by price range
       let priceRanges = {
           "budget": 0,      # < $20
           "mid": 0,         # $20-$50
           "premium": 0      # > $50
       };

       let i = 0;
       while (i < items.length) {
           let price = items[i].price;
           if (price < 20) {
               priceRanges.budget = priceRanges.budget + 1;
           } elif (price < 50) {
               priceRanges.mid = priceRanges.mid + 1;
           } else {
               priceRanges.premium = priceRanges.premium + 1;
           }
           i = i + 1;
       }

       return {
           "total_products": items.length,
           "total_inventory_value": totalValue,
           "average_price": avgPrice,
           "low_stock_count": lowStock.length,
           "low_stock_items": lowStock,
           "price_distribution": priceRanges
       };
   }

   function validateProduct(product) {
       let errors = [];

       if (!product.name || product.name.length < 3) {
           errors.push("Name must be at least 3 characters");
       }

       if (!product.price || product.price <= 0) {
           errors.push("Price must be positive");
       }

       if (product.stock && product.stock < 0) {
           errors.push("Stock cannot be negative");
       }

       if (errors.length > 0) {
           throw "Validation failed: " + errors.join(", ");
       }

       # Add default values
       if (!product.stock) {
           product.stock = 0;
       }

       return product;
   }

**Usage:**

.. code-block:: python

   # Setup database
   engine = create_engine('sqlite:///products.db')
   Base.metadata.create_all(engine)

   Session = sessionmaker(bind=engine)
   session = Session()

   # Create ML query builder
   ml_query = MLQueryBuilder(session, "orm_processors.ml")

   # Create product with ML validation
   try:
       product = ml_query.create_with_ml(
           Product,
           {"name": "Super Widget", "price": 39.99, "stock": 100},
           "validateProduct"
       )
       print(f"Created product: {product.id}")
   except Exception as e:
       print(f"Validation error: {e}")

   # Query and analyze
   result = ml_query.query_and_process(
       Product,
       {},  # No filters = all products
       "analyzeProducts"
   )

   print(f"Total products: {result['total_products']}")
   print(f"Inventory value: ${result['total_inventory_value']:.2f}")
   print(f"Low stock items: {result['low_stock_count']}")
   print(f"Price distribution: {result['price_distribution']}")

Django ORM Integration
~~~~~~~~~~~~~~~~~~~~~~~

Integrate ML with Django models.

**models.py:**

.. code-block:: python

   from django.db import models
   from mlpy import MLExecutor
   import json

   class Product(models.Model):
       """Product model with ML processing."""

       name = models.CharField(max_length=200)
       description = models.TextField()
       price = models.DecimalField(max_digits=10, decimal_places=2)
       stock = models.IntegerField(default=0)
       created_at = models.DateTimeField(auto_now_add=True)

       # ML executor (class-level)
       _ml_executor = None

       @classmethod
       def get_ml_executor(cls):
           """Get or create ML executor."""
           if cls._ml_executor is None:
               cls._ml_executor = MLExecutor()
               cls._ml_executor.load("product_processors.ml")
           return cls._ml_executor

       def to_ml_dict(self):
           """Convert to ML-compatible dict."""
           return {
               "id": self.id,
               "name": self.name,
               "description": self.description,
               "price": float(self.price),
               "stock": self.stock,
               "created_at": self.created_at.isoformat()
           }

       @classmethod
       def analyze_inventory(cls):
           """Analyze inventory using ML."""
           executor = cls.get_ml_executor()

           # Get all products
           products = cls.objects.all()
           data = [p.to_ml_dict() for p in products]

           # Analyze with ML
           return executor.call_function("analyzeInventory", {
               "products": data
           })

       def calculate_optimal_price(self):
           """Calculate optimal price using ML."""
           executor = self.get_ml_executor()

           result = executor.call_function("calculateOptimalPrice", {
               "current_price": float(self.price),
               "stock": self.stock,
               "name": self.name
           })

           return result["optimal_price"]

**product_processors.ml:**

.. code-block:: ml

   function analyzeInventory(data) {
       let products = data.products;

       # Calculate total value
       let totalValue = products.reduce(function(sum, p) {
           return sum + (p.price * p.stock);
       }, 0);

       # Find best sellers (assumed based on low stock)
       let bestSellers = products.filter(function(p) {
           return p.stock < 20;
       }).sort(function(a, b) {
           return a.stock - b.stock;
       });

       return {
           "total_products": products.length,
           "total_value": totalValue,
           "best_sellers": bestSellers.slice(0, 5),
           "average_stock": products.reduce(function(s, p) {
               return s + p.stock;
           }, 0) / products.length
       };
   }

   function calculateOptimalPrice(data) {
       let currentPrice = data.current_price;
       let stock = data.stock;

       # Simple pricing algorithm
       let multiplier = 1.0;

       if (stock > 100) {
           multiplier = 0.9;  # Discount for overstocked
       } elif (stock < 10) {
           multiplier = 1.1;  # Premium for low stock
       }

       return {
           "current_price": currentPrice,
           "optimal_price": currentPrice * multiplier,
           "adjustment": (multiplier - 1.0) * 100
       };
   }

**Usage in Django views:**

.. code-block:: python

   from django.http import JsonResponse
   from .models import Product

   def inventory_analysis(request):
       """Analyze inventory using ML."""
       result = Product.analyze_inventory()
       return JsonResponse(result)

   def optimize_product_price(request, product_id):
       """Get optimal price for product."""
       product = Product.objects.get(id=product_id)
       optimal_price = product.calculate_optimal_price()

       return JsonResponse({
           "product_id": product_id,
           "current_price": float(product.price),
           "optimal_price": optimal_price
       })

----

NoSQL Database Integration
----------------------------

MongoDB Integration
~~~~~~~~~~~~~~~~~~~~

Integrate ML with MongoDB for document processing.

.. code-block:: python

   from pymongo import MongoClient
   from mlpy import MLExecutor
   from typing import List, Dict, Any
   from datetime import datetime

   class MLMongoDB:
       """MongoDB integration with ML processing."""

       def __init__(
           self,
           ml_script: str,
           connection_string: str = "mongodb://localhost:27017/"
       ):
           """Initialize MongoDB connection.

           Args:
               ml_script: Path to ML script
               connection_string: MongoDB connection string
           """
           self.client = MongoClient(connection_string)
           self.executor = MLExecutor()
           self.executor.load(ml_script)

       def find_and_process(
           self,
           database: str,
           collection: str,
           query: Dict[str, Any],
           ml_function: str,
           limit: int = None
       ) -> Any:
           """Find documents and process with ML.

           Args:
               database: Database name
               collection: Collection name
               query: MongoDB query
               ml_function: ML function to process results
               limit: Maximum documents to retrieve

           Returns:
               Processed results from ML
           """
           db = self.client[database]
           coll = db[collection]

           # Execute query
           cursor = coll.find(query)
           if limit:
               cursor = cursor.limit(limit)

           # Convert to list
           documents = list(cursor)

           # Convert ObjectId to string
           for doc in documents:
               if '_id' in doc:
                   doc['_id'] = str(doc['_id'])

           # Process with ML
           return self.executor.call_function(ml_function, {
               "documents": documents,
               "count": len(documents)
           })

       def insert_with_ml(
           self,
           database: str,
           collection: str,
           document: Dict[str, Any],
           ml_function: str
       ) -> str:
           """Process document with ML before inserting.

           Args:
               database: Database name
               collection: Collection name
               document: Document to insert
               ml_function: ML function to process document

           Returns:
               Inserted document ID
           """
           # Process with ML
           processed = self.executor.call_function(ml_function, document)

           # Add metadata
           processed['created_at'] = datetime.now()
           processed['processed_by_ml'] = True

           # Insert
           db = self.client[database]
           coll = db[collection]
           result = coll.insert_one(processed)

           return str(result.inserted_id)

       def aggregate_with_ml(
           self,
           database: str,
           collection: str,
           pipeline: List[Dict[str, Any]],
           ml_function: str
       ) -> Any:
           """Run aggregation pipeline and process with ML."""
           db = self.client[database]
           coll = db[collection]

           # Execute aggregation
           results = list(coll.aggregate(pipeline))

           # Convert ObjectId to string
           for doc in results:
               if '_id' in doc:
                   doc['_id'] = str(doc['_id'])

           # Process with ML
           return self.executor.call_function(ml_function, {
               "results": results,
               "count": len(results)
           })

       def close(self):
           """Close MongoDB connection."""
           self.client.close()

**mongo_processors.ml:**

.. code-block:: ml

   function processUsers(data) {
       let documents = data.documents;

       # Analyze user activity
       let activeUsers = documents.filter(function(user) {
           return user.last_login != null;
       });

       # Group by country
       let byCountry = {};
       let i = 0;
       while (i < documents.length) {
           let user = documents[i];
           let country = user.country || "Unknown";
           byCountry[country] = (byCountry[country] || 0) + 1;
           i = i + 1;
       }

       return {
           "total_users": documents.length,
           "active_users": activeUsers.length,
           "by_country": byCountry,
           "activity_rate": (activeUsers.length / documents.length) * 100
       };
   }

   function enrichUser(user) {
       # Add computed fields
       user.full_name = user.first_name + " " + user.last_name;
       user.email_domain = user.email.split("@")[1];
       user.age_group = user.age < 30 ? "young" : (user.age < 60 ? "adult" : "senior");

       # Validate
       if (!user.email || user.email.indexOf("@") < 0) {
           throw "Invalid email address";
       }

       return user;
   }

   function analyzeAggregation(data) {
       let results = data.results;

       # Process aggregation results
       let summary = {
           "total_records": results.length,
           "data": results
       };

       if (results.length > 0) {
           # Calculate totals
           summary.total_value = results.reduce(function(sum, item) {
               return sum + (item.total || 0);
           }, 0);
       }

       return summary;
   }

**Usage:**

.. code-block:: python

   # Create MongoDB ML client
   mongo_ml = MLMongoDB("mongo_processors.ml")

   # Find and process users
   result = mongo_ml.find_and_process(
       database="myapp",
       collection="users",
       query={"active": True},
       ml_function="processUsers",
       limit=1000
   )

   print(f"Total users: {result['total_users']}")
   print(f"Active: {result['active_users']}")
   print(f"Activity rate: {result['activity_rate']:.1f}%")
   print(f"By country: {result['by_country']}")

   # Insert with ML processing
   try:
       user_id = mongo_ml.insert_with_ml(
           database="myapp",
           collection="users",
           document={
               "first_name": "John",
               "last_name": "Doe",
               "email": "john@example.com",
               "age": 30,
               "country": "USA"
           },
           ml_function="enrichUser"
       )
       print(f"Inserted user: {user_id}")
   except Exception as e:
       print(f"Error: {e}")

   # Aggregation with ML
   pipeline = [
       {"$match": {"active": True}},
       {"$group": {
           "_id": "$country",
           "count": {"$sum": 1},
           "total": {"$sum": "$amount"}
       }}
   ]

   result = mongo_ml.aggregate_with_ml(
       database="myapp",
       collection="orders",
       pipeline=pipeline,
       ml_function="analyzeAggregation"
   )

   mongo_ml.close()

Redis Integration
~~~~~~~~~~~~~~~~~~

Use ML with Redis for caching and data processing.

.. code-block:: python

   import redis
   import json
   from mlpy import MLExecutor
   from typing import Any, Dict

   class MLRedis:
       """Redis integration with ML processing."""

       def __init__(self, ml_script: str, **redis_params):
           """Initialize Redis connection.

           Args:
               ml_script: Path to ML script
               **redis_params: Redis connection parameters
           """
           self.redis = redis.Redis(**redis_params)
           self.executor = MLExecutor()
           self.executor.load(ml_script)

       def get_and_process(
           self,
           key: str,
           ml_function: str,
           default: Any = None
       ) -> Any:
           """Get value from Redis and process with ML.

           Args:
               key: Redis key
               ml_function: ML function to process value
               default: Default value if key doesn't exist

           Returns:
               Processed value from ML
           """
           # Get from Redis
           value = self.redis.get(key)

           if value is None:
               return default

           # Parse JSON
           data = json.loads(value)

           # Process with ML
           return self.executor.call_function(ml_function, data)

       def set_with_ml(
           self,
           key: str,
           data: Any,
           ml_function: str,
           ex: int = None
       ):
           """Process data with ML before storing in Redis.

           Args:
               key: Redis key
               data: Data to store
               ml_function: ML function to process data
               ex: Expiration time in seconds
           """
           # Process with ML
           processed = self.executor.call_function(ml_function, data)

           # Store in Redis
           value = json.dumps(processed)
           self.redis.set(key, value, ex=ex)

       def process_cached_data(
           self,
           pattern: str,
           ml_function: str
       ) -> Any:
           """Process multiple cached values matching pattern.

           Args:
               pattern: Redis key pattern (e.g., "user:*")
               ml_function: ML function to process all values

           Returns:
               Processed results from ML
           """
           # Get all matching keys
           keys = self.redis.keys(pattern)

           # Get all values
           values = []
           for key in keys:
               value = self.redis.get(key)
               if value:
                   values.append(json.loads(value))

           # Process with ML
           return self.executor.call_function(ml_function, {
               "items": values,
               "count": len(values)
           })

**redis_processors.ml:**

.. code-block:: ml

   function processCachedUser(user) {
       # Add analytics
       user.last_accessed = new Date().toISOString();
       user.access_count = (user.access_count || 0) + 1;

       return user;
   }

   function enrichCache(data) {
       # Add metadata
       data.cached_at = new Date().toISOString();
       data.ttl = 3600;  # 1 hour

       return data;
   }

   function analyzeCache(data) {
       let items = data.items;

       # Analyze cached data
       let totalSize = items.reduce(function(sum, item) {
           return sum + JSON.stringify(item).length;
       }, 0);

       return {
           "total_items": items.length,
           "estimated_size_bytes": totalSize,
           "items": items
       };
   }

**Usage:**

.. code-block:: python

   # Create Redis ML client
   redis_ml = MLRedis(
       "redis_processors.ml",
       host='localhost',
       port=6379,
       db=0
   )

   # Set with ML processing
   redis_ml.set_with_ml(
       "user:123",
       {"name": "John", "email": "john@example.com"},
       "enrichCache",
       ex=3600
   )

   # Get and process
   user = redis_ml.get_and_process(
       "user:123",
       "processCachedUser"
   )
   print(f"User accessed {user['access_count']} times")

   # Analyze all cached users
   result = redis_ml.process_cached_data(
       "user:*",
       "analyzeCache"
   )
   print(f"Cached users: {result['total_items']}")
   print(f"Total size: {result['estimated_size_bytes']} bytes")

----

Transaction Management
-----------------------

ML with Database Transactions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ensure data integrity with transactions.

.. code-block:: python

   from sqlalchemy.orm import Session
   from mlpy import MLExecutor
   from typing import List, Dict, Any

   class MLTransactionManager:
       """Manage database transactions with ML processing."""

       def __init__(self, session: Session, ml_script: str):
           """Initialize transaction manager.

           Args:
               session: SQLAlchemy session
               ml_script: Path to ML script
           """
           self.session = session
           self.executor = MLExecutor()
           self.executor.load(ml_script)

       def execute_transaction(
           self,
           operations: List[Dict[str, Any]],
           ml_function: str
       ):
           """Execute transaction with ML validation.

           Args:
               operations: List of operations to execute
               ml_function: ML function to validate transaction

           Raises:
               Exception: If validation fails or transaction fails
           """
           try:
               # Validate transaction with ML
               validation = self.executor.call_function(ml_function, {
                   "operations": operations
               })

               if not validation.get("valid", False):
                   raise ValueError(f"Validation failed: {validation.get('errors')}")

               # Execute operations
               for op in operations:
                   self._execute_operation(op)

               # Commit transaction
               self.session.commit()

           except Exception as e:
               # Rollback on error
               self.session.rollback()
               raise

       def _execute_operation(self, operation: Dict[str, Any]):
           """Execute single operation."""
           op_type = operation["type"]

           if op_type == "insert":
               # Handle insert
               pass
           elif op_type == "update":
               # Handle update
               pass
           elif op_type == "delete":
               # Handle delete
               pass

**transaction_validators.ml:**

.. code-block:: ml

   function validateTransaction(data) {
       let operations = data.operations;
       let errors = [];

       # Check for conflicting operations
       let i = 0;
       while (i < operations.length) {
           let op = operations[i];

           # Validate operation type
           if (op.type != "insert" && op.type != "update" && op.type != "delete") {
               errors.push("Invalid operation type: " + op.type);
           }

           # Check business rules
           if (op.type == "update" && !op.id) {
               errors.push("Update requires ID");
           }

           i = i + 1;
       }

       return {
           "valid": errors.length == 0,
           "errors": errors,
           "operation_count": operations.length
       };
   }

----

Best Practices
---------------

Connection Pooling
~~~~~~~~~~~~~~~~~~~

**Always use connection pools for production:**

.. code-block:: python

   # Good: Connection pool
   from psycopg2 import pool

   db_pool = pool.SimpleConnectionPool(
       minconn=1,
       maxconn=10,
       database="mydb"
   )

   # Bad: New connection every time
   # conn = psycopg2.connect(database="mydb")

Error Handling
~~~~~~~~~~~~~~~

**Handle database errors gracefully:**

.. code-block:: python

   from sqlalchemy.exc import SQLAlchemyError

   try:
       result = db.execute_with_ml(query, params, "process")
   except SQLAlchemyError as e:
       logger.error(f"Database error: {e}")
       # Handle appropriately
       raise

Query Optimization
~~~~~~~~~~~~~~~~~~~

**Use ML for query optimization:**

.. code-block:: ml

   function optimizeQuery(params) {
       # Add appropriate indexes
       # Limit result set
       # Use efficient joins

       if (params.limit > 1000) {
           params.limit = 1000;  # Cap at 1000
       }

       return params;
   }

----

Summary
--------

Database integration with ML enables:

**SQL Databases:**
- Query result processing with ML functions
- Data validation before insertion
- Business logic in ML functions
- ORM integration (SQLAlchemy, Django)

**NoSQL Databases:**
- Document processing with MongoDB
- Cache optimization with Redis
- Aggregation pipeline processing

**Best Practices:**
- Use connection pooling
- Validate data with ML before persistence
- Handle transactions properly
- Optimize queries with ML logic
- Cache processed results

ML functions provide a powerful layer for business logic, validation, and data transformation while maintaining database integrity and performance.

----

Next: :doc:`external-apis` - Integrating ML with external HTTP APIs and web services
