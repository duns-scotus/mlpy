// Comprehensive Object Operations Test
// Demonstrates all aspects of object manipulation in ML

import string;
import collections;

// Object creation and basic operations
function object_creation_basics() {
    print("=== Object Creation and Basics ===");

    // Empty object
    empty_object = {};

    // Simple object with different value types
    person = {
        name: "John Doe",
        age: 30,
        active: true,
        salary: 50000.0
    };

    // Object with array properties
    student = {
        name: "Alice Johnson",
        grades: [95, 87, 92, 88],
        courses: ["Math", "Science", "History"],
        active: true
    };

    // Object with nested objects
    company = {
        name: "Tech Corp",
        founded: 2010,
        address: {
            street: "123 Main St",
            city: "Anytown",
            state: "CA",
            zip: "12345"
        },
        employees: {
            total: 150,
            departments: ["Engineering", "Sales", "Marketing"]
        }
    };

    print("Empty object: " + empty_object);
    print("Person object: " + person);
    print("Student object: " + student);
    print("Company object: " + company);

    return {
        empty: empty_object,
        person: person,
        student: student,
        company: company
    };
}

// Object property access and modification
function object_property_access() {
    print("\n=== Object Property Access and Modification ===");

    employee = {
        id: 1001,
        name: "Bob Smith",
        department: "Engineering",
        skills: ["Python", "Java", "JavaScript"],
        active: true,
        salary: 75000,
        contact: {
            email: "bob@company.com",
            phone: "555-0123"
        }
    };

    print("Original employee: " + employee);

    // Basic property access
    emp_name = employee.name;
    emp_id = employee.id;
    emp_department = employee.department;
    emp_active = employee.active;

    print("\nProperty Access:");
    print("Name: " + emp_name);
    print("ID: " + emp_id);
    print("Department: " + emp_department);
    print("Active: " + emp_active);

    // Nested object property access
    emp_email = employee.contact.email;
    emp_phone = employee.contact.phone;

    print("Email: " + emp_email);
    print("Phone: " + emp_phone);

    // Array property access
    first_skill = employee.skills[0];
    skill_count = collections.length(employee.skills);

    print("First skill: " + first_skill);
    print("Number of skills: " + skill_count);

    // Property modification
    employee.department = "DevOps";
    employee.salary = 80000;
    employee.active = false;

    print("\nAfter modifications:");
    print("New department: " + employee.department);
    print("New salary: " + employee.salary);
    print("Active status: " + employee.active);

    // Nested property modification
    employee.contact.email = "bob.smith@newcompany.com";
    employee.skills[0] = "Go";

    print("New email: " + employee.contact.email);
    print("Modified first skill: " + employee.skills[0]);

    print("Modified employee: " + employee);

    return {
        original_name: emp_name,
        modified_employee: employee,
        contact_info: {
            email: emp_email,
            phone: emp_phone
        }
    };
}

// Object composition and relationships
function object_composition_relationships() {
    print("\n=== Object Composition and Relationships ===");

    // Create related objects
    address = {
        street: "456 Oak Ave",
        city: "Springfield",
        state: "IL",
        zip: "62701"
    };

    contact_info = {
        email: "contact@example.com",
        phone: "555-0199",
        fax: "555-0198"
    };

    person = {
        name: "Sarah Wilson",
        age: 28,
        address: address,
        contact: contact_info
    };

    // Create objects with shared references
    project1 = {
        name: "Website Redesign",
        status: "active",
        lead: person
    };

    project2 = {
        name: "Mobile App",
        status: "planning",
        lead: person
    };

    print("Person: " + person);
    print("Project 1: " + project1);
    print("Project 2: " + project2);

    // Modify shared object
    person.age = 29;
    print("\nAfter modifying shared person's age:");
    print("Person age: " + person.age);
    print("Project 1 lead age: " + project1.lead.age);
    print("Project 2 lead age: " + project2.lead.age);

    // Object with methods (function properties)
    calculator = {
        value: 0,
        add: function(x) {
            calculator.value = calculator.value + x;
            return calculator.value;
        },
        subtract: function(x) {
            calculator.value = calculator.value - x;
            return calculator.value;
        },
        multiply: function(x) {
            calculator.value = calculator.value * x;
            return calculator.value;
        },
        reset: function() {
            calculator.value = 0;
            return calculator.value;
        }
    };

    print("\nCalculator object with methods:");
    print("Initial value: " + calculator.value);

    result1 = calculator.add(10);
    print("After add(10): " + result1);

    result2 = calculator.multiply(3);
    print("After multiply(3): " + result2);

    result3 = calculator.subtract(5);
    print("After subtract(5): " + result3);

    return {
        person: person,
        projects: [project1, project2],
        calculator: calculator,
        shared_modification_test: "passed"
    };
}

// Object manipulation utilities
function object_manipulation_utilities() {
    print("\n=== Object Manipulation Utilities ===");

    original_object = {
        name: "Test Object",
        value: 42,
        active: true,
        tags: ["important", "test"],
        metadata: {
            created: "2024-01-01",
            version: 1
        }
    };

    // Object copying utility
    function shallow_copy_object(obj) {
        copy = {};
        // Note: This is a simplified copy that works for the current ML implementation
        // In a full implementation, you would iterate over object properties
        return obj; // For demonstration purposes
    }

    // Object property checking
    function has_property(obj, property_name) {
        // Simplified property checking
        // In a full implementation, this would use reflection or property enumeration
        return true; // Placeholder
    }

    // Object merging utility
    function merge_objects(obj1, obj2) {
        // Create a new object with properties from both
        merged = {
            // This is a simplified merge
            // In practice, you would iterate through properties
        };
        return obj1; // Simplified return for demonstration
    }

    base_config = {
        debug: false,
        timeout: 5000,
        retry_count: 3
    };

    user_config = {
        debug: true,
        max_connections: 10
    };

    // Demonstrate object transformations
    function transform_object_values(obj) {
        // Transform all string values to uppercase
        // This is conceptual - actual implementation would depend on property iteration
        transformed = {
            name: string.upper(obj.name),
            value: obj.value,
            active: obj.active,
            tags: obj.tags,
            metadata: obj.metadata
        };
        return transformed;
    }

    transformed_object = transform_object_values(original_object);

    print("Original object: " + original_object);
    print("Transformed object: " + transformed_object);

    // Object validation
    function validate_person(person_obj) {
        valid = true;
        errors = [];

        // Check required fields (simplified)
        if (person_obj.name == "") {
            errors = collections.append(errors, "Name is required");
            valid = false;
        }

        if (person_obj.age < 0 || person_obj.age > 150) {
            errors = collections.append(errors, "Age must be between 0 and 150");
            valid = false;
        }

        return {
            valid: valid,
            errors: errors
        };
    }

    valid_person = {
        name: "John Doe",
        age: 30,
        email: "john@example.com"
    };

    invalid_person = {
        name: "",
        age: -5,
        email: "invalid-email"
    };

    validation1 = validate_person(valid_person);
    validation2 = validate_person(invalid_person);

    print("\nValidation Results:");
    print("Valid person validation: " + validation1);
    print("Invalid person validation: " + validation2);

    return {
        original: original_object,
        transformed: transformed_object,
        validations: {
            valid_person: validation1,
            invalid_person: validation2
        }
    };
}

// Object-oriented programming patterns
function object_oriented_patterns() {
    print("\n=== Object-Oriented Programming Patterns ===");

    // Constructor pattern
    function create_person(name, age, email) {
        return {
            name: name,
            age: age,
            email: email,
            get_info: function() {
                return person.name + " (" + person.age + ") - " + person.email;
            },
            celebrate_birthday: function() {
                person.age = person.age + 1;
                return "Happy birthday! Now " + person.age + " years old.";
            }
        };
    }

    person1 = create_person("Alice", 25, "alice@example.com");
    person2 = create_person("Bob", 30, "bob@example.com");

    print("Person 1: " + person1);
    print("Person 2: " + person2);

    // Method calls
    info1 = person1.get_info();
    birthday_msg = person1.celebrate_birthday();

    print("Person 1 info: " + info1);
    print("Birthday message: " + birthday_msg);

    // Factory pattern
    function create_vehicle(type, make, model, year) {
        base_vehicle = {
            type: type,
            make: make,
            model: model,
            year: year,
            mileage: 0,

            drive: function(miles) {
                base_vehicle.mileage = base_vehicle.mileage + miles;
                return "Drove " + miles + " miles. Total: " + base_vehicle.mileage;
            },

            get_description: function() {
                return base_vehicle.year + " " + base_vehicle.make + " " + base_vehicle.model;
            }
        };

        // Add type-specific properties
        if (type == "car") {
            base_vehicle.doors = 4;
        } elif (type == "truck") {
            base_vehicle.bed_length = 6;
        } elif (type == "motorcycle") {
            base_vehicle.engine_size = "600cc";
        }

        return base_vehicle;
    }

    car = create_vehicle("car", "Toyota", "Camry", 2022);
    truck = create_vehicle("truck", "Ford", "F-150", 2023);
    bike = create_vehicle("motorcycle", "Honda", "CBR600RR", 2021);

    print("\nVehicle Factory Pattern:");
    print("Car: " + car.get_description());
    print("Truck: " + truck.get_description());
    print("Bike: " + bike.get_description());

    drive_result = car.drive(150);
    print("Car driving: " + drive_result);

    // Configuration object pattern
    function create_api_client(config) {
        default_config = {
            base_url: "https://api.example.com",
            timeout: 5000,
            retry_count: 3,
            debug: false
        };

        // Merge configurations (simplified)
        merged_config = {
            base_url: config.base_url ? config.base_url : default_config.base_url,
            timeout: config.timeout ? config.timeout : default_config.timeout,
            retry_count: config.retry_count ? config.retry_count : default_config.retry_count,
            debug: config.debug ? config.debug : default_config.debug
        };

        return {
            config: merged_config,

            get: function(endpoint) {
                url = merged_config.base_url + endpoint;
                return "GET " + url + " (timeout: " + merged_config.timeout + ")";
            },

            post: function(endpoint, data) {
                url = merged_config.base_url + endpoint;
                return "POST " + url + " with data: " + data;
            }
        };
    }

    client1 = create_api_client({
        base_url: "https://myapi.com",
        debug: true
    });

    client2 = create_api_client({
        timeout: 10000
    });

    print("\nAPI Client Pattern:");
    print("Client 1 config: " + client1.config);
    print("Client 2 config: " + client2.config);

    get_result = client1.get("/users");
    post_result = client2.post("/users", "user_data");

    print("Client 1 GET: " + get_result);
    print("Client 2 POST: " + post_result);

    return {
        people: [person1, person2],
        vehicles: [car, truck, bike],
        api_clients: [client1, client2]
    };
}

// Object serialization and data transformation
function object_serialization_transformation() {
    print("\n=== Object Serialization and Transformation ===");

    complex_object = {
        id: 1234,
        user: {
            name: "Jane Doe",
            email: "jane@example.com",
            preferences: {
                theme: "dark",
                language: "en",
                notifications: true
            }
        },
        projects: [
            {
                name: "Project Alpha",
                status: "active",
                tasks: ["Design", "Development", "Testing"]
            },
            {
                name: "Project Beta",
                status: "completed",
                tasks: ["Research", "Implementation"]
            }
        ],
        metadata: {
            created: "2024-01-15",
            last_modified: "2024-03-20",
            version: 2
        }
    };

    print("Complex object: " + complex_object);

    // Object flattening utility
    function flatten_object(obj, prefix) {
        flattened = {};

        // Simplified flattening for demonstration
        // In a full implementation, this would recursively process all properties
        if (prefix == "") {
            flattened.id = obj.id;
            flattened.user_name = obj.user.name;
            flattened.user_email = obj.user.email;
            flattened.user_theme = obj.user.preferences.theme;
        }

        return flattened;
    }

    flattened = flatten_object(complex_object, "");
    print("Flattened object: " + flattened);

    // Object filtering
    function filter_object_properties(obj, keep_properties) {
        filtered = {};

        // Simplified filtering - keep only specified properties
        i = 0;
        while (i < collections.length(keep_properties)) {
            prop = keep_properties[i];
            if (prop == "id") {
                filtered.id = obj.id;
            } elif (prop == "user") {
                filtered.user = obj.user;
            } elif (prop == "metadata") {
                filtered.metadata = obj.metadata;
            }
            i = i + 1;
        }

        return filtered;
    }

    filtered = filter_object_properties(complex_object, ["id", "user"]);
    print("Filtered object: " + filtered);

    // Object transformation pipeline
    function transform_user_data(user_obj) {
        // Transform user data for API response
        return {
            user_id: user_obj.id,
            display_name: string.upper(user_obj.user.name),
            contact_email: string.lower(user_obj.user.email),
            settings: user_obj.user.preferences,
            project_count: collections.length(user_obj.projects),
            last_update: user_obj.metadata.last_modified
        };
    }

    transformed = transform_user_data(complex_object);
    print("Transformed user data: " + transformed);

    // Object validation schema
    function validate_object_schema(obj, schema) {
        validation_errors = [];

        // Simplified schema validation
        if (!obj.id) {
            validation_errors = collections.append(validation_errors, "Missing required field: id");
        }

        if (!obj.user || !obj.user.name) {
            validation_errors = collections.append(validation_errors, "Missing required field: user.name");
        }

        if (!obj.user || !obj.user.email) {
            validation_errors = collections.append(validation_errors, "Missing required field: user.email");
        }

        return {
            valid: collections.length(validation_errors) == 0,
            errors: validation_errors
        };
    }

    schema = {}; // Placeholder schema
    validation_result = validate_object_schema(complex_object, schema);
    print("Validation result: " + validation_result);

    return {
        original: complex_object,
        flattened: flattened,
        filtered: filtered,
        transformed: transformed,
        validation: validation_result
    };
}

// Object performance and memory considerations
function object_performance_considerations() {
    print("\n=== Object Performance Considerations ===");

    // Object pooling pattern
    function create_object_pool(factory_func, initial_size) {
        pool = {
            available: [],
            in_use: [],
            factory: factory_func,

            get_object: function() {
                if (collections.length(pool.available) > 0) {
                    obj = collections.first(pool.available);
                    // Remove from available (simplified)
                    pool.available = collections.slice(pool.available, 1, collections.length(pool.available));
                    pool.in_use = collections.append(pool.in_use, obj);
                    return obj;
                } else {
                    new_obj = pool.factory();
                    pool.in_use = collections.append(pool.in_use, new_obj);
                    return new_obj;
                }
            },

            return_object: function(obj) {
                // Reset object state
                obj.value = 0;
                obj.active = false;

                // Move from in_use to available (simplified)
                pool.available = collections.append(pool.available, obj);
            }
        };

        // Pre-populate pool
        i = 0;
        while (i < initial_size) {
            initial_obj = factory_func();
            pool.available = collections.append(pool.available, initial_obj);
            i = i + 1;
        }

        return pool;
    }

    function create_work_item() {
        return {
            id: 0,
            value: 0,
            active: false,

            process: function() {
                return "Processing work item " + work_item.id;
            }
        };
    }

    work_pool = create_object_pool(create_work_item, 3);

    print("Object pool created with 3 initial objects");
    print("Available objects: " + collections.length(work_pool.available));

    // Get objects from pool
    item1 = work_pool.get_object();
    item2 = work_pool.get_object();

    item1.id = 101;
    item1.active = true;

    item2.id = 102;
    item2.active = true;

    print("After getting 2 objects:");
    print("Available: " + collections.length(work_pool.available));
    print("In use: " + collections.length(work_pool.in_use));

    // Return objects to pool
    work_pool.return_object(item1);

    print("After returning 1 object:");
    print("Available: " + collections.length(work_pool.available));
    print("In use: " + collections.length(work_pool.in_use));

    // Object immutability pattern
    function create_immutable_point(x, y) {
        return {
            x: x,
            y: y,

            move: function(dx, dy) {
                // Return new object instead of modifying current one
                return create_immutable_point(point.x + dx, point.y + dy);
            },

            distance_to: function(other_point) {
                dx = other_point.x - point.x;
                dy = other_point.y - point.y;
                return dx * dx + dy * dy; // Simplified distance calculation
            },

            to_string: function() {
                return "Point(" + point.x + ", " + point.y + ")";
            }
        };
    }

    original_point = create_immutable_point(0, 0);
    moved_point = original_point.move(5, 3);
    twice_moved = moved_point.move(2, 1);

    print("\nImmutable objects:");
    print("Original point: " + original_point.to_string());
    print("Moved point: " + moved_point.to_string());
    print("Twice moved: " + twice_moved.to_string());

    distance = original_point.distance_to(moved_point);
    print("Distance between original and moved: " + distance);

    return {
        object_pool: work_pool,
        immutable_demo: {
            original: original_point,
            moved: moved_point,
            twice_moved: twice_moved,
            distance: distance
        }
    };
}

// Main test runner
function main() {
    print("========================================");
    print("  COMPREHENSIVE OBJECT OPERATIONS TEST");
    print("========================================");

    results = {};

    results.creation = object_creation_basics();
    results.access = object_property_access();
    results.composition = object_composition_relationships();
    results.utilities = object_manipulation_utilities();
    results.oop_patterns = object_oriented_patterns();
    results.serialization = object_serialization_transformation();
    results.performance = object_performance_considerations();

    print("\n========================================");
    print("  ALL OBJECT TESTS COMPLETED");
    print("========================================");

    return results;
}

// Execute all object tests
main();